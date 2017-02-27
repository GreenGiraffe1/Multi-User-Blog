from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Likez


class LikePost(Handler):

    """Do the 'Like' Functionality."""

    def get(self, post_id):
        # uname = self.identify()
        if self.read_secure_cookie("user_id"):
            current_user = (self.request.cookies.get("user_id")).split("|")[0]
            current_name = (self.request.cookies.get("user")).split("|")[0]
            l = Likez(creator=current_user, name=current_name,
                      post_id=post_id, does_like=True)
            l.put()  # sends Likez object "l" to the GAE datastore
            sleep(.2)
            self.redirect("/blog/%s" % str(post_id))
        else:
            self.redirect("/blog/login")
