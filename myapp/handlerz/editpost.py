from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Post


class EditPost(Handler):

    """Allow user to edit a post they've created."""

    def get(self, post_id):
        """Render page where a poster can edit post, post_id passed in URL."""
        uname = self.identify()
        # Retrieve object key with entity name and attribute id number
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        self.render("edit.html", post=post, uname=uname)

    def post(self, post_id):
        """Accept user input and save or cancel editing accordingly.

        Receive an update request from server when user pushes the submit
        button. Update the post.content attribute of the corresponding Post
        entity. This Post object is determined by retrieving the post_id from
        the URL.

        If the user pushes the cancel button don't send anything to the server
        and redirect the user to the post's main display page.

        """
        # Retrieve object key with entity name and attribute id number
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        update_p_text = self.request.get("post_update")
        if update_p_text:
            post.content = update_p_text
            post.put()  # sends updated Post object "post" to GAE datastore
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))
