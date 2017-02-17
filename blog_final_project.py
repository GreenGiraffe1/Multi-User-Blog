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


# The following 2 lines of code create the template directory, and create an
# instance of the jinja object (for templating) respectively.
# Templates are stored in the same directory as the .py file
# I chose not to create a template directory for ease of use while learning.
# In the future I'll store them in a seperate folder with the following code:
# template_dir = os.path.join(os.path.dirname(__file__, "templates"))
template_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


# value to hash with cookie values to make them secure. (normally this would be
# held in another secure module, but is here for ease of learning.)
SECRET = "LYtOJ9kweSza7sBszlB79z5WEELkEY8O3t6Ll5F4nmj7bWzNLR"


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    """Check username entered to determine if it's valid (with REGEX)."""
    return USER_RE.match(username)


PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    """Check password entered to determine if it's valid (with REGEX)."""
    return PASSWORD_RE.match(password)


EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    """Check email entered to determine if it's valid (with REGEX)."""
    return EMAIL_RE.match(email)


def hash_str(s):
    """Hashes the user_id and SECRET (a constant) to create a cookie hash."""
    return hmac.new(SECRET,s).hexdigest()


def make_secure_val(s):
    """Takes the user_id as input, and returns the value that will be set for
    the cookie, a string containing the user_id and the hashed user_id.
    """
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    """Checks the cookie value from the current webpage, and determines
    whether it's valid.
    """
    if h:
        val = h.split("|")[0]
        if h == make_secure_val(val):
            return val


def make_salt(length = 5):
    """Creates a unique salt for hashing with a user's password during signup.
    """
    return "".join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt = None):
    """Creates a new password hash during signup, or checks a password hash's
    validity during login. Calls a function to create a salt during signup.
    """
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s|%s" % (salt,h)


def valid_pw(name, password, h):
    """Checks validity of a user's inputed password during login by hashing it
    and comparing it to the stored value in the Credential table/entity."""
    salt = h.split("|")[0]
    return h == make_pw_hash(name, password, salt)


class Handler(webapp2.RequestHandler):
    """Parent Handler of all other Handlers. Handles user interaction."""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header("Set-Cookie",
                        "%s=%s; Path=/" % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie("user_id", str(user.key().id()))

    def logout(self):
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")

    def identify(self):
        if self.read_secure_cookie("user"):
            uname = self.read_secure_cookie("user").split("|")[0]
        else:
            uname = None
        return uname


class Credential(db.Model):
    """Entity stores all attributes of user login credentials."""

    username = db.StringProperty(required = True)
    email = db.StringProperty(required = False)
    hashed_password = db.TextProperty(required = True)


class Post(db.Model):
    """Entity Stores all attributes of blog posts."""

    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    creator = db.StringProperty(required = False)
    name = db.StringProperty(required = False)


class Signup(Handler):
    """Handles user input and errors on the signup webpage, sets cookies."""

    def get(self):
        uname = self.identify()
        self.render("register.html", uname=uname)

    def post(self):
        uname = self.identify()
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        #### New Logic - with Dictionary Error Handling
        params = dict(username = username,
                      email = email, uname=uname)
        have_error = False
        if not valid_username(username):
            params["error_username"] = "That's not a valid username."
            have_error = True
        if not valid_password(password):
            params["error_password"] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params["error_verify"] = "Your passwords didn't match."
            have_error = True
        if email:
            if not valid_email(email):
                params["error_email"] = "That's not a valid email."
                have_error = True
        # check here if the username is already in the database - if so - throw an error - make them Pick a new username
        credentials = db.GqlQuery("SELECT * FROM Credential")
        for cr in credentials:
            if cr.username == username:
                params["error_username"] = ("That username already exists. "
                                            "Choose another and try again.")
                have_error = True
        if have_error:
            self.render("register.html", **params)
        else:
            c = Credential(username=username, email=email,
                           hashed_password=make_pw_hash(username, verify))
            c.put()
            self.response.headers.add_header("Set-Cookie", "user=%s; Path=/"
                                             % str(make_secure_val(username)))
            self.login(c)
            self.redirect("/blog")


class WelcomeHandler(Handler):
    """Display a welcome message to user upon successful login or signup."""

    def get(self):
        usn = self.request.cookies.get("user")
        if check_secure_val(usn):
            self.render("welcome.html", username = usn.split("|")[0])
        else:
            self.redirect("/blog/logout")


class Login(Handler):
    """Handles user input and errors on the login webpage, sets cookies."""

    def get(self):
        uname = self.identify()
        self.render("login.html", uname=uname)

    def post(self):
        uname = self.identify()
        username = self.request.get("username")
        password = self.request.get("password")
        proceed = False
        self.query = Credential.all()
        for self.credential in self.query:
            if self.credential.username == username and valid_pw(username,
                        password, self.credential.hashed_password):
                self.response.headers.add_header("Set-Cookie",
                        "user=%s; Path=/" % str(make_secure_val(username)))
                u = self.credential
                self.login(u)
                proceed = True
                self.redirect("/blog")
        if not proceed:
            self.render("login.html", error_login="Login Invalid",
                        uname=uname)


class Logout(Handler):
    """Logs a user out by reseting cookies. (No webpage / user interface)."""

    def get(self):
        # delete cookie
        usn = self.request.cookies.get("user")  # TODO: Remove this once I confirm it isn"t necessary. (getting the user cookie before deleting it)
        self.response.headers.add_header("Set-Cookie",
                                         "user=%s; Path=/" % (""))
        self.logout()
        self.redirect("/blog/signup")


class MainPage(Handler):
    """Redirects users to the main blog page."""

    def get(self):
        self.redirect("/blog")


class NewPost(Handler):
    """Allows user to input a blog post, and saves it in the Post Entity."""

    def render_newpost(self,subject="",content="", error=""):
        uname = self.identify()
        self.render("newpost.html",subject=subject, content=content,
                    error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if (subject and content and self.read_secure_cookie("user")
                        and self.read_secure_cookie("user_id")):
            name1 = self.request.cookies.get("user")
            name = name1.split("|")[0]
            creator1 = self.request.cookies.get("user_id")
            creator = creator1.split("|")[0]
            p = Post(subject=subject, content=content, creator=creator,
                     name=name)
            p.put()
            self.redirect("/blog/%s" % str(p.key().id()))
        elif not self.read_secure_cookie("user"):
            error = "You must be logged in to create a new post."
            self.render_newpost(subject,content,error)
        else:
            error = ("You need to enter both a Subject and Content to create "
                     "a new post.")
            self.render_newpost(subject, content, error)


class Blog(Handler):
    """Displays the 10 most recent posts from Post entity on main blog page."""

    def render_fpage(self):
        # posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")  # Only delete this, if I"m REALLY sure it"s all working
        posts = Post.all().order("-created").fetch(limit=10)
        uname = self.identify()
        self.render("blog.html", posts=posts, uname=uname)

    def get(self):
        self.render_fpage()

    def post(self):
        uname=self.identify()
        if self.request.get("create-post") and uname:
            self.redirect("/blog/newpost")
        elif self.request.get("create-post") and not uname:
            self.redirect("/blog/login")


class Comment(db.Model):
    """Entity Stores all attributes of comments (written on blog posts)."""

    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    creator = db.StringProperty(required = True)
    name = db.StringProperty(required = False)
    post_id = db.StringProperty(required = True)
    mod = db.BooleanProperty(required = False)


class Likez(db.Model):
    """Entity Stores all attributes of 'Likes' for blog posts."""

    does_like = db.BooleanProperty(required = True) #I need a True / False Value..., then I'll need to count up the "True's"
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    creator = db.StringProperty(required = True)
    name = db.StringProperty(required = False)
    post_id = db.StringProperty(required = True)


class PostPage(Handler):
    """Displays individual posts with corresponding comments & 'Likes'."""

    def get(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        uname = self.identify()
        if self.read_secure_cookie("user_id"):
            current_user = (self.request.cookies.get("user_id")).split("|")[0]
        else:
            current_user = None
        if not post:
            self.error(404)
            return
        likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
        count = 0  # This counts the number of likes for this post from the database.
        for likey in likez:
            if likey.does_like and likey.post_id == post_id: # Second condition is if the ID matches..
                count = count + 1
        display = "like"
        for li in likez:
            if (li.post_id == post_id and li.creator == current_user
                            and li.does_like):
                display = "unlike"
        self.query = Comment.all().order("-created")
        self.render("permalink.html", post=post, current_user=current_user,
                    comments=self.query, cur_post_id=post_id, count=count,
                    likez=likez, display=display, uname=uname)

    def post(self, post_id):
        uname = self.identify()
        have_error = False
        delete_post = False
        edit_post = False
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        comment = self.request.get("comment")
        if self.read_secure_cookie("user_id"):
            current_user = (self.request.cookies.get("user_id")).split("|")[0]
            current_name = (self.request.cookies.get("user")).split("|")[0]
        else:
            current_user = None
            current_name = None
        # I'll attempt to create the liking here
        if self.request.get("like1") and uname:
            l = Likez(creator=current_user, name=current_name,
                      post_id=post_id, does_like=True)
            l.put()
            sleep(.2)
        elif self.request.get("like1") and not uname:
            have_error = True
        if self.request.get("unlike"):
            likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
            delkey = None
            for likey in likez:
                if likey.creator == current_user and likey.does_like:
                    delkey = likey.key()
            if delkey:
                db.delete(delkey)
                sleep(.2)
        if self.request.get("edit_c"):
            ckey = self.request.get("edit_c")
            e = db.get(ckey)
            e.mod = True
            e.put()
            sleep(.2)
        if self.request.get("update_c"):
            ucom = self.request.get("updated_comment")
            ukey = self.request.get("update_c")
            u = db.get(ukey)
            u.content = ucom
            u.mod = False
            u.put()
            sleep(.2)
        if self.request.get("cancel_u_c"):
            cankey = self.request.get("cancel_u_c")
            can = db.get(cankey)
            can.mod = False
            can.put()
            sleep(.2)
        if self.request.get("delete_c"):
            dd_key = self.request.get("delete_c")
            # dd = db.get(dd_key)
            db.delete(dd_key)
            sleep(.2)
        if self.request.get("delete_p"):
            dpk = self.request.get("delete_p")
            db.delete(dpk)
            delete_post = True
            sleep(.2)
        if self.request.get("edit_p"):
            epk = self.request.get("edit_p")
            edit_post = True
        if comment and uname:
            c = Comment(content=comment, name=current_name,
                        creator=current_user, post_id=post_id)
            c.put()
            sleep(.2)
        elif comment and not uname:
            have_error = True
        if delete_post:
            self.redirect("/blog")
        elif edit_post:
            self.redirect("/blog/edit/%s" % str(post_id))
        elif have_error:
            self.redirect("/blog/login")
        else:
            self.redirect("/blog/%s" % str(post_id))


class EditPage(Handler):
    """Allows user to edit a post they've created"""

    def get(self, post_id):
        uname = self.identify()
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        self.render("edit.html", post=post, uname=uname, display="NoShow")

    def post(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        update_p_text = self.request.get("post_update")
        if update_p_text:
            post.content = update_p_text
            post.put()
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))


app = webapp2.WSGIApplication([("/", MainPage),
                               ("/blog/welcome",WelcomeHandler),
                               ("/blog/signup", Signup),
                               ("/blog/login", Login),
                               ("/blog/logout", Logout),
                               ("/blog", Blog),
                               ("/blog/newpost", NewPost),
                               ("/blog/([0-9]+)", PostPage),
                               ("/blog/edit/([0-9]+)", EditPage),
                                ],
                                debug=True)
