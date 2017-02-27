from handlerparent import Handler
from google.appengine.ext import db
from myapp.modelz import Credential
from myapp.functions import appfunctions


class Signup(Handler):

    """Handle user input and errors on the signup webpage, set cookies."""

    def get(self):
        """Render signup page."""
        uname = self.identify()
        self.render("register.html", uname=uname)

    def post(self):
        """Accept user inputs and conditionally register user.

        Verify that all inputs meet the established criteria, if not render
        appropriate error message and ask for new input. Upon valid input
        create a new object in the Credential entity for the registered user,
        and set 2 cookies: 'user' and 'user_id'.

        """
        uname = self.identify()
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        # params dictionary used for error handling
        params = dict(username=username, email=email, uname=uname)
        have_error = False
        if not appfunctions.valid_username(username):
            params["error_username"] = "That's not a valid username."
            have_error = True
        if not appfunctions.valid_password(password):
            params["error_password"] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params["error_verify"] = "Your passwords didn't match."
            have_error = True
        if email:
            if not appfunctions.valid_email(email):
                params["error_email"] = "That's not a valid email."
                have_error = True
        # GQL query the Google App Engine (GAE) datastore, Credential entity
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
                           hashed_password=appfunctions.make_pw_hash(username, verify))
            c.put()  # sends Credential object "c" to the GAE datastore
            self.response.headers.add_header("Set-Cookie", "user=%s; Path=/"
                                             % str(appfunctions.make_secure_val(username)))
            self.login(c)  # set secure cookie "user_id"
            self.redirect("/blog")
