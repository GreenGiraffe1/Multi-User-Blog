
import webapp2
import jinja2
import os


from google.appengine.ext import db

from functions import appfunctions

# template_dir = os.path.join(os.path.dirname(__file__), "templates")

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)



class Handler(webapp2.RequestHandler):

    """Handle user interaction. (Parent Handler of all other Handlers.)"""

    def write(self, *a, **kw):
        """Write text/elements to HTML page"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Create jinja template object with input parameters"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """Display HTML page, pass parameters to template object"""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """Create and set secure cookie upon login or signup"""
        cookie_val = make_secure_val(val)
        self.response.headers.add_header("Set-Cookie",
                                         "%s=%s; Path=/" % (name, cookie_val))

    def read_secure_cookie(self, name):
        """Verify that inputed cookie is secure/ hasn't been modified."""
        cookie_val = self.request.cookies.get(name)
        return cookie_val and appfunctions.check_secure_val(cookie_val)

    def login(self, user):
        """Create and set secure cookie 'user_id' upon login or signup"""
        self.set_secure_cookie("user_id", str(user.key().id()))

    def logout(self):
        """Reset 'user_id' cookie to = '' upon logout"""
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")

    def identify(self):
        """Read cookie 'user', and return the 'name' value if secure.

        All classes employ this method, and often use it to determine the
        user's identity, and what permissions to grant them.

        All webpages use the result of this method in determining which HTML
        header code to display to the user / visitor. If the method returns
        any result other than 'None' that means the user is logged in, and the
        page displays the user's name, and the option to logout. If it returns
        'None' that means the visitor isn't logged in, and therefore it asks
        them to login or register.

        """
        if self.read_secure_cookie("user"):
            uname = self.read_secure_cookie("user").split("|")[0]
        else:
            uname = None
        return uname
