from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Likez
from myapp.functions.decorators import user_logged_in, post_exists


class UnlikePost(Handler):

    """Do the 'Unlike' Functionality."""

    @user_logged_in
    @post_exists
    def get(self, post_id):
        # if self.read_secure_cookie("user_id"):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        current_user = (self.request.cookies.get("user_id")).split("|")[0]
        current_name = (self.request.cookies.get("user")).split("|")[0]
        likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
        delkey = None
        # Check to see if the user has liked the post in the past, if so,
        # delete that "Like" entry.
        for likey in likez:
            if (likey.creator == current_user) and (likey.does_like) and (likey.post_id == post_id):  # post.key().id()):
                delkey = likey.key()
        if delkey:
            db.delete(delkey)  # Deletes the "Like"
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))
        # self.render("test.html", likepostid=)
        # else:
        #     self.redirect("/blog/%s" % str(post_id))
        # else:
        #     self.redirect("/blog/login")
