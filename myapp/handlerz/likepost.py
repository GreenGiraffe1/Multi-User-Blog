from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Likez
from myapp.functions.decorators import user_logged_in, post_exists


class LikePost(Handler):

    """Add a 'Like' to a post on the users behalf."""

    @user_logged_in
    @post_exists
    def get(self, post_id):
        """Add a like to the 'Likez' database associated with the post.

        Verify that the user is logged in, that the post exists, that they
        aren't the post creator, and that the user hasn't liked the post
        previously before allowing the database to update to the new value.

        """
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
            current_name = (self.request.cookies.get("user")).split("|")[0]
            l = Likez(creator=current_user, name=current_name,
                      post_id=post_id, does_like=True)
            l.put()  # sends Likez object "l" to the GAE datastore
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))
