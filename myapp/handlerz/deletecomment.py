from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.functions.decorators import (user_logged_in, comment_exists,
                                        user_owns_comment)


class DeleteComment(Handler):

    """Delete comment from blog post page."""

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comm_id):
        """Delete comment if it exists, and logged in user was its creator."""
        key = db.Key.from_path("Comment", int(comm_id))
        comment = db.get(key)
        post = comment.post_id
        db.delete(key)
        sleep(.2)
        self.redirect("/blog/%s" % str(post))
