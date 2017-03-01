from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.functions.decorators import (user_logged_in, post_exists,
                                        user_owns_post)


class DeletePost(Handler):

    """Delete post from the blog."""

    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id):
        """Delete post if it exists, and logged in user was its creator."""
        key = db.Key.from_path("Post", int(post_id))
        db.delete(key)
        sleep(.2)
        self.redirect("/blog")
