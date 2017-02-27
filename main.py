"""This module performs all the backend functions of Matt's Blog.

This document, the HTML pages, and the database entities are stored / hosted
by Google App Engine. This module supports registration, login, and logging
out with password hashing and secure cookies. Logged in users may create blog
posts, comment on posts, like other's posts, and delete or edit their own blog
posts or comments.

"""

import os
import re

import hmac
import hashlib
from string import letters
import random
from time import sleep

import webapp2
import jinja2
from google.appengine.ext import db
from myapp.modelz import Credential, Post, Comment, Likez
from myapp.handlerz import DeleteComment, DeletePost, LikePost, LogOut,
                           MainPage, UnlikePost, EditComment, EditPost, Blog,
                           Login, NewPost, PostPage, Signup
from myapp.handlerz.handlerparent import Handler


# The following 2 lines of code create the template directory, and create an
# instance of the jinja object (for templating) respectively.
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

#
# # value to hash with cookie values to make them secure. (normally this would be
# # held in another secure module, but is here for ease of learning.)
# SECRET = "LYtOJ9kweSza7sBszlB79z5WEELkEY8O3t6Ll5F4nmj7bWzNLR"
#
# # REGEX to validate user registration inputs
# USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
# PASSWORD_RE = re.compile(r"^.{3,20}$")
# EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
#
#
# def valid_username(username):
#     """Check username entered to determine if it's valid (with REGEX)."""
#     return USER_RE.match(username)
#
#
# def valid_password(password):
#     """Check password entered to determine if it's valid (with REGEX)."""
#     return PASSWORD_RE.match(password)
#
#
# def valid_email(email):
#     """Check email entered to determine if it's valid (with REGEX)."""
#     return EMAIL_RE.match(email)
#
#
# def hash_str(s):
#     """Hash the user_id and SECRET (a constant) to create a cookie hash."""
#     return hmac.new(SECRET, s).hexdigest()
#
#
# def make_secure_val(s):
#     """When user_id is input, it return the value to set for the cookie."""
#     return "%s|%s" % (s, hash_str(s))
#
#
# def check_secure_val(h):
#     """Check whether the cookie value from the current webpage is valid."""
#     if h:
#         val = h.split("|")[0]
#         if h == make_secure_val(val):
#             return val
#
#
# def make_salt(length=5):
#     """Create a unique salt for hashing a user's password during signup."""
#     return "".join(random.choice(letters) for x in xrange(length))
#
#
# def make_pw_hash(name, pw, salt=None):
#     """Make password hash on signup, or check password hash on login."""
#     if not salt:
#         salt = make_salt()
#     h = hashlib.sha256(name + pw + salt).hexdigest()  # sha256 hash algorithm
#     return "%s|%s" % (salt, h)
#
#
# def valid_pw(name, password, h):
#     """Check hash of user's login against value in the Credential entity."""
#     salt = h.split("|")[0]
#     return h == make_pw_hash(name, password, salt)
#
#






# class Handler(webapp2.RequestHandler):
#
#     """Handle user interaction. (Parent Handler of all other Handlers.)"""
#
#     def write(self, *a, **kw):
#         """Write text/elements to HTML page"""
#         self.response.out.write(*a, **kw)
#
#     def render_str(self, template, **params):
#         """Create jinja template object with input parameters"""
#         t = jinja_env.get_template(template)
#         return t.render(params)
#
#     def render(self, template, **kw):
#         """Display HTML page, pass parameters to template object"""
#         self.write(self.render_str(template, **kw))
#
#     def set_secure_cookie(self, name, val):
#         """Create and set secure cookie upon login or signup"""
#         cookie_val = make_secure_val(val)
#         self.response.headers.add_header("Set-Cookie",
#                                          "%s=%s; Path=/" % (name, cookie_val))
#
#     def read_secure_cookie(self, name):
#         """Verify that inputed cookie is secure/ hasn't been modified."""
#         cookie_val = self.request.cookies.get(name)
#         return cookie_val and check_secure_val(cookie_val)
#
#     def login(self, user):
#         """Create and set secure cookie 'user_id' upon login or signup"""
#         self.set_secure_cookie("user_id", str(user.key().id()))
#
#     def logout(self):
#         """Reset 'user_id' cookie to = '' upon logout"""
#         self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")
#
#     def identify(self):
#         """Read cookie 'user', and return the 'name' value if secure.
#
#         All classes employ this method, and often use it to determine the
#         user's identity, and what permissions to grant them.
#
#         All webpages use the result of this method in determining which HTML
#         header code to display to the user / visitor. If the method returns
#         any result other than 'None' that means the user is logged in, and the
#         page displays the user's name, and the option to logout. If it returns
#         'None' that means the visitor isn't logged in, and therefore it asks
#         them to login or register.
#
#         """
#         if self.read_secure_cookie("user"):
#             uname = self.read_secure_cookie("user").split("|")[0]
#         else:
#             uname = None
#         return uname

#
# class Signup(Handler):
#
#     """Handle user input and errors on the signup webpage, set cookies."""
#
#     def get(self):
#         """Render signup page."""
#         uname = self.identify()
#         self.render("register.html", uname=uname)
#
#     def post(self):
#         """Accept user inputs and conditionally register user.
#
#         Verify that all inputs meet the established criteria, if not render
#         appropriate error message and ask for new input. Upon valid input
#         create a new object in the Credential entity for the registered user,
#         and set 2 cookies: 'user' and 'user_id'.
#
#         """
#         uname = self.identify()
#         username = self.request.get("username")
#         password = self.request.get("password")
#         verify = self.request.get("verify")
#         email = self.request.get("email")
#         # params dictionary used for error handling
#         params = dict(username=username, email=email, uname=uname)
#         have_error = False
#         if not valid_username(username):
#             params["error_username"] = "That's not a valid username."
#             have_error = True
#         if not valid_password(password):
#             params["error_password"] = "That wasn't a valid password."
#             have_error = True
#         elif password != verify:
#             params["error_verify"] = "Your passwords didn't match."
#             have_error = True
#         if email:
#             if not valid_email(email):
#                 params["error_email"] = "That's not a valid email."
#                 have_error = True
#         # GQL query the Google App Engine (GAE) datastore, Credential entity
#         credentials = db.GqlQuery("SELECT * FROM Credential")
#         for cr in credentials:
#             if cr.username == username:
#                 params["error_username"] = ("That username already exists. "
#                                             "Choose another and try again.")
#                 have_error = True
#         if have_error:
#             self.render("register.html", **params)
#         else:
#             c = Credential(username=username, email=email,
#                            hashed_password=make_pw_hash(username, verify))
#             c.put()  # sends Credential object "c" to the GAE datastore
#             self.response.headers.add_header("Set-Cookie", "user=%s; Path=/"
#                                              % str(make_secure_val(username)))
#             self.login(c)  # set secure cookie "user_id"
#             self.redirect("/blog")
#
#
# class Login(Handler):
#
#     """Handle user input and errors on the login webpage, set cookies."""
#
#     def get(self):
#         """Render login page."""
#         uname = self.identify()
#         self.render("login.html", uname=uname)
#
#     def post(self):
#         """Accept login credentials, conditionally log user in.
#
#         Check user input to against the Credential entity, and log them in if
#         the user is found. The hash of the entered password is compared with
#         the stored hash to determine validity. Upon successful login set
#         secure cookies 'user' and 'user_id'. If login is unsuccessful display
#         error message.
#
#         """
#         uname = self.identify()
#         username = self.request.get("username")
#         password = self.request.get("password")
#         proceed = False
#         # Query the Google App Engine (GAE) datastore, Credential entity
#         self.query = Credential.all()
#         for self.credential in self.query:
#             if self.credential.username == username and valid_pw(username,
#                            password, self.credential.hashed_password):
#                 self.response.headers.add_header("Set-Cookie",
#                            "user=%s; Path=/" % str(make_secure_val(username)))
#                 u = self.credential
#                 self.login(u)  # set secure "user_id" cookie
#                 proceed = True
#                 self.redirect("/blog")
#         if not proceed:
#             self.render("login.html", error_login="Login Invalid",
#                         uname=uname)


# class Logout(Handler):
#
#     """Log a user out by reseting cookies. (No webpage / user interface)."""
#
#     def get(self):
#         """Log user out by setting cookie values to ''."""
#         usn = self.request.cookies.get("user")
#         self.response.headers.add_header("Set-Cookie",
#                                          "user=%s; Path=/" % (""))
#         self.logout()  # Reset the "user_id" cookie to ""
#         self.redirect("/blog/signup")


# class MainPage(Handler):
#
#     """Redirect visitors to the main blog page."""
#
#     def get(self):
#         """Redirect visitors to the main blog page."""
#         self.redirect("/blog")


# class NewPost(Handler):
#
#     """Accept user input of a blog post, and save it in the Post entity."""
#
#     def render_newpost(self, subject="", content="", error=""):
#         """Render newpost page where user can create blog posts."""
#         uname = self.identify()
#         self.render("newpost.html", subject=subject, content=content,
#                     error=error, uname=uname)
#
#     def get(self):
#         """Call method that renders the newpost page."""
#
#         if self.read_secure_cookie("user_id"):
#             self.render_newpost()
#         else:
#             self.redirect("/blog/login")
#
#     def post(self):
#         """Coditionally create new blog posts.
#
#         Accept user input for blog post subject and content, and if the user
#         is signed in (checked for be examining cookies), and they have
#         included both a subject and content, create a new post object in the
#         Post entity. If the visitor is not logged in, redirect them to the
#         login page to do so. If the user doesn't enter both a subject and
#         content, prompt them to do so with an error message.
#
#         """
#         subject = self.request.get("subject")
#         content = self.request.get("content")
#         if (subject and content and self.read_secure_cookie("user") and
#                         self.read_secure_cookie("user_id")):
#             name1 = self.request.cookies.get("user")
#             name = name1.split("|")[0]
#             creator1 = self.request.cookies.get("user_id")
#             creator = creator1.split("|")[0]
#             p = Post(subject=subject, content=content, creator=creator,
#                      name=name)
#             p.put()  # sends Post object "p" to the GAE datastore
#             self.redirect("/blog/%s" % str(p.key().id()))
#         elif not self.read_secure_cookie("user"):
#             error = "You must be logged in to create a new post."
#             self.render_newpost(subject, content, error)
#         else:
#             error = ("You need to enter both a Subject and Content to create "
#                      "a new post.")
#             self.render_newpost(subject, content, error)


# class Blog(Handler):
#
#     """Display 10 most recent posts from Post entity on main blog page."""
#
#     def render_fpage(self):
#         """Display the main blog page.
#
#         Query the Post entity for the 10 most recent blog posts and display
#         them in descending order of their creation date / time, along with
#         their author and when they were first posted.
#
#         """
#         # Query the Google App Engine (GAE) datastore, Post entity, return the
#         # 10 most recent posts in descending order of creation time.
#         posts = Post.all().order("-created").fetch(limit=10)
#         uname = self.identify()
#         self.render("blog.html", posts=posts, uname=uname)
#
#     def get(self):
#         """Call function that renders the main blog page."""
#         self.render_fpage()







# class PostPage(Handler):
#
#     """Display individual posts with corresponding comments & 'Likes'."""
#
#     def get(self, post_id):
#         """Display individual blog posts and all related content.
#
#         Display individual blog posts corresponding to the id in the url
#         (will match the id in the Post entity), and corresponding 'Likes',
#         comments, and editing options based on user permissions. Retrieve
#         these objects by querying the Post, Likez, and Comment entities
#         respectively. Display only the objects that match the current post's
#         Post id.
#
#         If the visitor is not logged in they will only see the post, 'Likes'
#         and comments, but not the editing options.
#
#         If a user is logged in show buttons allowing them to edit or
#         delete posts they have created, and comments they have created.
#         Display a button to 'Like' the post if they haven't 'Liked' it yet, or
#         an 'Unlike' button if they have.
#
#         Determine these permissions by comparing their user_id
#         (stored in a cookie) with the user_id of the post and comment
#         creators.
#
#         """
#         # Retrieve object key with entity name and attribute id number
#         key = db.Key.from_path("Post", int(post_id))
#         post = db.get(key)
#         uname = self.identify()
#         if self.read_secure_cookie("user_id"):
#             current_user = (self.request.cookies.get("user_id")).split("|")[0]
#         else:
#             current_user = None
#         if not post:
#             self.error(404)
#             return
#         likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
#         count = 0  # Count the number of likes for post from the database.
#         for likey in likez:
#             if likey.does_like and likey.post_id == post_id:
#                 count = count + 1
#         display = "like"
#         for li in likez:
#             if (li.post_id == post_id and li.creator == current_user and
#                             li.does_like):
#                 display = "unlike"
#         self.query = Comment.all().order("-created")
#         self.render("permalink.html", post=post, current_user=current_user,
#                     comments=self.query, cur_post_id=post_id, count=count,
#                     likez=likez, display=display, uname=uname)
#
#     def post(self, post_id):
#         """Allow user to comment and Like posts, and edit their contributions.
#
#         Take user input and conditionally allow them to make contributions,
#         and modify past contributions. If a visitor is not logged in redirect
#         them to the login page upon them sending requests to the server
#         for 'Liking' or commenting posts.
#
#         Allow logged in users to comment on post, and 'Like' or 'Unlike' post
#         by clicking the appropriate buttons, which will send info to the
#         server and in some cases modify the Comment or Likez entities
#         where those items are held.
#
#         Display comments and 'Likes' based on the post's Post post_id, which
#         is saved in the respective Comment and Likez entities.
#
#         Users can edit or delete a comment, or the post if they created it.
#         This is established by checking if their user_id (stored in a cookie)
#         matches the post/comment creator id.
#
#         """
#         # Retrieve object key with entity name and attribute id number
#         key = db.Key.from_path("Post", int(post_id))
#         post = db.get(key)
#         comment = self.request.get("comment")
#         if self.read_secure_cookie("user_id"):
#             current_user = (self.request.cookies.get("user_id")).split("|")[0]
#             current_name = (self.request.cookies.get("user")).split("|")[0]
#         else:
#             current_user = None
#             current_name = None
#         if current_user:
#             if comment:
#                 # User submitted new comment, save it in the Comment entity
#                 c = Comment(content=comment, name=current_name,
#                             creator=current_user, post_id=post_id)
#                 c.put()  # sends Comment object "c" to the GAE datastore
#                 sleep(.2)
#             self.redirect("/blog/%s" % str(post_id))
#         else:
#             self.redirect("/blog/login")
#






# class DeletePost(Handler):
#
#     def get(self, post_id):
#         key = db.Key.from_path("Post", int(post_id))
#         db.delete(key)
#         sleep(.2)
#         self.redirect("/blog")


# class DeleteComment(Handler):
#
#     def get(self, comm_id):
#         key = db.Key.from_path("Comment", int(comm_id))
#         comment = db.get(key)
#         post = comment.post_id
#         db.delete(key)
#         sleep(.2)
#         self.redirect("/blog/%s" % str(post))


# class EditComment(Handler):
#
#     def get(self, post_id):
#         uname = self.identify()
#         # Retrieve object key with entity name and attribute id number
#         key = db.Key.from_path("Comment", int(post_id))
#         comment = db.get(key)
#         self.render("editcomment.html", comment=comment, uname=uname)
#
#     def post(self, post_id):
#         key = db.Key.from_path("Comment", int(post_id))
#         comment = db.get(key)
#         update_c_text = self.request.get("comment_update")
#         if update_c_text:
#             comment.content = update_c_text
#             comment.put()  # sends updated Post object "post" to GAE datastore
#             sleep(.2)
#         self.redirect("/blog/%s" % str(comment.post_id))

#
# class LikePost(Handler):
#
#     """Do the 'Like' Functionality."""
#
#     def get(self, post_id):
#         # uname = self.identify()
#         if self.read_secure_cookie("user_id"):
#             current_user = (self.request.cookies.get("user_id")).split("|")[0]
#             current_name = (self.request.cookies.get("user")).split("|")[0]
#             l = Likez(creator=current_user, name=current_name,
#                       post_id=post_id, does_like=True)
#             l.put()  # sends Likez object "l" to the GAE datastore
#             sleep(.2)
#             self.redirect("/blog/%s" % str(post_id))
#         else:
#             self.redirect("/blog/login")


# class UnlikePost(Handler):
#
#     """Do the 'Unlike' Functionality."""
#
#     def get(self, post_id):
#         if self.read_secure_cookie("user_id"):
#             current_user = (self.request.cookies.get("user_id")).split("|")[0]
#             current_name = (self.request.cookies.get("user")).split("|")[0]
#             likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
#             delkey = None
#             for likey in likez:
#                 if likey.creator == current_user and likey.does_like:
#                     delkey = likey.key()
#             if delkey:
#                 db.delete(delkey)  # Deletes the "Like"
#                 sleep(.2)
#                 self.redirect("/blog/%s" % str(post_id))
#             else:
#                 self.redirect("/blog/%s" % str(post_id))
#         else:
#             self.redirect("/blog/login")


# class EditPost(Handler):
#
#     """Allow user to edit a post they've created."""
#
#     def get(self, post_id):
#         """Render page where a poster can edit post, post_id passed in URL."""
#         uname = self.identify()
#         # Retrieve object key with entity name and attribute id number
#         key = db.Key.from_path("Post", int(post_id))
#         post = db.get(key)
#         self.render("edit.html", post=post, uname=uname)
#
#     def post(self, post_id):
#         """Accept user input and save or cancel editing accordingly.
#
#         Receive an update request from server when user pushes the submit
#         button. Update the post.content attribute of the corresponding Post
#         entity. This Post object is determined by retrieving the post_id from
#         the URL.
#
#         If the user pushes the cancel button don't send anything to the server
#         and redirect the user to the post's main display page.
#
#         """
#         # Retrieve object key with entity name and attribute id number
#         key = db.Key.from_path("Post", int(post_id))
#         post = db.get(key)
#         update_p_text = self.request.get("post_update")
#         if update_p_text:
#             post.content = update_p_text
#             post.put()  # sends updated Post object "post" to GAE datastore
#             sleep(.2)
#         self.redirect("/blog/%s" % str(post_id))


app = webapp2.WSGIApplication([("/", MainPage),
                               ("/blog/signup", Signup),
                               ("/blog/login", Login),
                               ("/blog/logout", LogOut),
                               ("/blog", Blog),
                               ("/blog/newpost", NewPost),
                               ("/blog/([0-9]+)", PostPage),
                               ("/blog/unlike/([0-9]+)", UnlikePost),
                               ("/blog/like/([0-9]+)", LikePost),
                               ("/blog/edit/([0-9]+)", EditPost),
                               ("/blog/editcomment/([0-9]+)", EditComment),
                               ("/blog/deletecomment/([0-9]+)", DeleteComment),
                               ("/blog/deletepost/([0-9]+)", DeletePost),
                               ],
                              debug=True)
