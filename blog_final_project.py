import os
import re

import hmac
import hashlib
from string import letters
import random
from time import sleep


import webapp2
import jinja2




SECRET = 'LYtOJ9kweSza7sBszlB79z5WEELkEY8O3t6Ll5F4nmj7bWzNLR'  # "salt" for the secure cookie (normally this would be held in another secure module)


from google.appengine.ext import db
# from google.appengine.api import users  # I think this is only if I want people to login through their Google accounts


template_dir = os.path.join(os.path.dirname(__file__))#, 'templates') - I chose not to create a template directory for ease of use while learning.
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)



#  REGEX - to verify user registration input

# username verification
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

# password verification
PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

# email verification
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)







def hash_str(s):
    # return hashlib.md5(s).hexdigest()
    return hmac.new(SECRET,s).hexdigest()

# returns a string of the format: s,HASH
def make_secure_val(s):
    # output = s + "," + hash_str(s)
    # return output
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    # string,hashstr = h.split(',')
    if h:
        val = h.split('|')[0]
        if h == make_secure_val(val):
            return val



## Password Hashing / Manipulation - this is new & it is untested
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (salt,h)

def valid_pw(name, password, h):
    salt = h.split('|')[0]
    return h == make_pw_hash(name, password, salt)



def pwhasher(pw):
    return hmac.new('salt',pw).hexdigest()




class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    ### Alert - these 2 should work, but I haven't put them in my code yet.
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)


    ### Alert - these naming comventions don't match with the rest of mine, and aren't implemented, but do seem like they may be useful in the future
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # def initialize(self, *a, **k):
    #     webapp2.RequestHandler.initialize(self, *a, **k)
    #     uid = self.read_secure_cookie('user')
    #     if uid:
    #         self.user = uid




class Credential(db.Model):
    username = db.StringProperty(required = True)
    email = db.StringProperty(required = False)
    hashed_password = db.TextProperty(required = True)




class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    creator = db.StringProperty(required = True)



class Signup(Handler):
    def get(self):
        self.render("register.html")


    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')



        #### New Logic - with Dictionary Error Handling
        params = dict(username = username,
                      email = email)

        have_error = False

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if email:
            if not valid_email(email):
                params['error_email'] = "That's not a valid email."
                have_error = True

        # check here if the username is already in the database - if so - throw an error - make them Pick a new username
        credentials = db.GqlQuery("SELECT * FROM Credential")
        for cr in credentials:
            if cr.username == username:
                params['error_username'] = "That username already exists. Choose another and try again."
                # self.write("NOOO")
                have_error = True

        if have_error:
            self.render('register.html', **params)
        else:
            # c = Credential(username=username, email=email, hashed_password=pwhasher(verify))        #  TODO: Implement Secure Password Hashing
            c = Credential(username=username, email=email, hashed_password=make_pw_hash(username, verify))        #  TODO: Do it Here!
            c.put()
            # self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % (str(username)))  # Set a Cookie in App Engine
                                                   # I think this should be: % make_secure_val(username))
            self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % str(make_secure_val(username)))
            self.login(c)
            # global passer
            # passer = str(c.key().id())
            # global passer
            # passer = c
            self.redirect("/welcome")


class WelcomeHandler(Handler):
    def get(self):
        usn = self.request.cookies.get('user')
        if check_secure_val(usn):
            self.render("welcome.html", username = usn.split('|')[0])#, credentials=credentials)
        else:
            self.redirect('/logout')



class Login(Handler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        proceed = False



        # credentials = db.GqlQuery("SELECT * FROM Credential ORDER BY created")
        #
        # for cr in credentials:
        #     if cr.username == username and valid_pw(username, password, cr.hashed_password):  # TODO: implement hashed_password Verification
        #
        #         # send to welcome screen, and set the cookie
        #         self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % str(make_secure_val(username)))
        #         u = cr
        #         self.login(u)
        #
        #         proceed = True
        #         self.redirect("/welcome")



        # Try alternate syntax, without using GQL:
        self.query = Credential.all()
        for self.credential in self.query:
            if self.credential.username == username and valid_pw(username, password, self.credential.hashed_password):
                self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % str(make_secure_val(username)))
                u = self.credential  #.key().id()
                self.login(u)

                proceed = True
                self.redirect("/welcome")



        if not proceed:
            self.render('login.html', error_login='Login Invalid')


class Logout(Handler):
    def get(self):
        # delete cookie
        usn = self.request.cookies.get('user')  # TODO: Remove this once I confirm it isn't necessary. (getting the user cookie before deleting it)
        self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % (''))
        self.logout()
        self.redirect("/signup")

class MainPage(Handler):
    def get(self):
        self.redirect("/signup")

########  TODO:  Add BLOG Functionality Here     #######

class NewPost(Handler):
    def render_newpost(self,subject="",content="", error=""):
        self.render("newpost.html",subject=subject, content=content,error=error)

    def get(self):
        # if read_secure_cookie('user'):
        #     self.render_newpost()
        # else:
        #     self.redirect()
        # if not self.read_secure_cookie('user'):
        #     self.redirect('/login', error_login='Must be Logged in to Post')
        self.render_newpost()

    def post(self):

        subject = self.request.get("subject")
        content = self.request.get("content")

        # if not self.read_secure_cookie('user'):
        #     error = 'Must be logged in to Post.'
        #     self.render_newpost(subject,content,error)
            # error = 'You must be logged in to create a new post.'
            # self.render_newpost(subject, content, error)



        if subject and content and self.read_secure_cookie('user'):
            p = Post(subject=subject, content=content)
            p.put()
            self.write("This worked - now you need to create a redirect.")
            self.redirect("/blog/%s" % str(p.key().id()))

        elif not self.read_secure_cookie('user'):
            error = 'You must be logged in to create a new post.'
            self.render_newpost(subject,content,error)

        else:
            error = "You need to enter both a Subject and Content to create a new post."
            self.render_newpost(subject, content, error)


class Blog(Handler):
    def render_fpage(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("blog.html", posts=posts)

    def get(self):
        self.render_fpage()


class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)



#######   END   #########

class Email(db.Model):
    subject = db.StringProperty(required = True)
    email = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    creator = db.StringProperty(required = True)
    name = db.StringProperty(required = False)


class Tester(Handler):
    def get(self):
        # self.write("the user is currently: %s" % self.user.key())
        emails = db.GqlQuery("SELECT * FROM Email ORDER BY created DESC LIMIT 10")
        self.render('testerform.html', emails=emails)


    def post(self):
        subject = self.request.get('subject')
        email = self.request.get('email')
        if self.read_secure_cookie('user_id'):
            creator1 = self.request.cookies.get('user_id')
            # val = h.split('|')[0]
            creator = creator1.split('|')[0]
            name1 = self.request.cookies.get('user')
            name = name1.split('|')[0]
        else:
            creator = 'no user set'
            name = 'no user set'

        if subject and email:  # and self.read_secure_cookie('user'):
            e = Email(subject=subject, email=email, creator=creator, name=name)
            e.put()
            sleep(1)
            self.redirect("/tester")

        # emails = db.GqlQuery("SELECT * FROM Email ORDER BY created DESC LIMIT 10")
        # self.render("testerform.html", emails=emails)









app = webapp2.WSGIApplication([('/', MainPage),
                               ('/welcome',WelcomeHandler),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ("/blog", Blog),
                               ("/blog/newpost", NewPost),
                               ("/blog/([0-9]+)", PostPage),
                               ("/tester", Tester),
                                ],
                                debug=True)
