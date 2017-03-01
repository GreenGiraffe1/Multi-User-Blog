from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Likez
from myapp.functions.decorators import user_logged_in, post_exists


class UnlikePost(Handler):

    """Remove a 'Like' from a post on the users behalf."""

    @user_logged_in
    @post_exists
    def get(self, post_id):
        """Delete a like from the 'Likez' database associated with the post.

        Verify that the user is logged in, that the post exists, that they
        aren't the post creator, and that the user has liked the post
        previously before allowing the database to delete the stored object.

        """
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        current_user = (self.request.cookies.get("user_id")).split("|")[0]
        current_name = (self.request.cookies.get("user")).split("|")[0]
        likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
        delkey = None
        # Check to see if the user has liked the post in the past.
        for likey in likez:
            if ((likey.creator == current_user) and (likey.does_like) and
                            (likey.post_id == post_id)):
                delkey = likey.key()
        if delkey:
            db.delete(delkey)  # Deletes the "Like"
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))
