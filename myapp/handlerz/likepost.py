from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Likez
from myapp.functions.decorators import user_logged_in, post_exists


class LikePost(Handler):

    """Do the 'Like' Functionality."""

    @user_logged_in
    # does not own post
    # has not liked before (no likes in db for them currently)
    @post_exists
    def get(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        current_user = (self.request.cookies.get("user_id")).split("|")[0]
        # Prevents users who've previously liked the post from "re-liking" it.
        likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
        for li in likez:
            if (li.post_id == post_id and li.creator == current_user and
                            li.does_like):
                self.redirect("/blog/%s" % str(post_id))
        if self.read_secure_cookie("user_id") != post.creator:
            # current_user = (self.request.cookies.get("user_id")).split("|")[0]
            current_name = (self.request.cookies.get("user")).split("|")[0]
            l = Likez(creator=current_user, name=current_name,
                      post_id=post_id, does_like=True)
            l.put()  # sends Likez object "l" to the GAE datastore
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))
        # else:
        #     self.redirect("/blog/login")
