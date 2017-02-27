from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Likez


class UnlikePost(Handler):

    """Do the 'Unlike' Functionality."""

    def get(self, post_id):
        if self.read_secure_cookie("user_id"):
            current_user = (self.request.cookies.get("user_id")).split("|")[0]
            current_name = (self.request.cookies.get("user")).split("|")[0]
            likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
            delkey = None
            for likey in likez:
                if likey.creator == current_user and likey.does_like:
                    delkey = likey.key()
            if delkey:
                db.delete(delkey)  # Deletes the "Like"
                sleep(.2)
                self.redirect("/blog/%s" % str(post_id))
            else:
                self.redirect("/blog/%s" % str(post_id))
        else:
            self.redirect("/blog/login")
