from handlerparent import Handler


class LogOut(Handler):

    """Log a user out by reseting cookies. (No webpage / user interface)."""

    def get(self):
        """Log user out by setting cookie values to ''."""
        usn = self.request.cookies.get("user")
        self.response.headers.add_header("Set-Cookie",
                                         "user=%s; Path=/" % (""))
        self.logout()  # Reset the "user_id" cookie to ""
        self.redirect("/blog/signup")
