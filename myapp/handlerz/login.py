from handlerparent import Handler
from myapp.modelz import Credential
from myapp.functions import appfunctions


class Login(Handler):

    """Handle user input and errors on the login webpage, set cookies."""

    def get(self):
        """Render login page."""
        uname = self.identify()
        self.render("login.html", uname=uname)

    def post(self):
        """Accept login credentials, conditionally log user in.

        Check user input to against the Credential entity, and log them in if
        the user is found. The hash of the entered password is compared with
        the stored hash to determine validity. Upon successful login set
        secure cookies 'user' and 'user_id'. If login is unsuccessful display
        error message.

        """
        uname = self.identify()
        username = self.request.get("username")
        password = self.request.get("password")
        proceed = False
        # Query the Google App Engine (GAE) datastore, Credential entity
        self.query = Credential.all()
        for self.credential in self.query:
            if (self.credential.username == username and
                            appfunctions.valid_pw(username,
                            password, self.credential.hashed_password)):
                self.response.headers.add_header("Set-Cookie",
                           ("user=%s; Path=/" %
                           str(appfunctions.make_secure_val(username))))
                u = self.credential
                self.login(u)  # set secure "user_id" cookie
                proceed = True
                self.redirect("/blog")
        if not proceed:
            self.render("login.html", error_login="Login Invalid",
                        uname=uname)
