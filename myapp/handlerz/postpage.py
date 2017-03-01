from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Post, Comment, Likez
from myapp.functions.decorators import user_logged_in, post_exists


class PostPage(Handler):

    """Display individual posts with corresponding comments & 'Likes'."""

    @post_exists
    def get(self, post_id):
        """Display individual blog posts and all related content.

        Display individual blog posts corresponding to the id in the url
        (will match the id in the Post entity), and corresponding 'Likes',
        comments, and editing options based on user permissions. Retrieve
        these objects by querying the Post, Likez, and Comment entities
        respectively. Display only the objects that match the current post's
        Post id.

        If the visitor is not logged in they will only see the post, 'Likes'
        and comments, but not the editing options.

        If a user is logged in show buttons allowing them to edit or
        delete posts they have created, and comments they have created.
        Display a button to 'Like' the post if they haven't 'Liked' it yet, or
        an 'Unlike' button if they have.

        Determine these permissions by comparing their user_id
        (stored in a cookie) with the user_id of the post and comment
        creators.

        """
        # Retrieve object key with entity name and attribute id number
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        uname = self.identify()
        if self.read_secure_cookie("user_id"):
            current_user = (self.request.cookies.get("user_id")).split("|")[0]
        else:
            current_user = None
        likez = db.GqlQuery("SELECT * FROM Likez ORDER BY created DESC")
        count = 0  # Count the number of likes for post from the database.
        for likey in likez:
            if likey.does_like and likey.post_id == post_id:
                count = count + 1
        display = "like"
        for li in likez:
            if (li.post_id == post_id and li.creator == current_user and
                            li.does_like):
                display = "unlike"
        self.query = Comment.all().order("-created")
        self.render("permalink.html", post=post, current_user=current_user,
                    comments=self.query, cur_post_id=post_id, count=count,
                    likez=likez, display=display, uname=uname)

    @user_logged_in
    @post_exists
    def post(self, post_id):
        """Allow user to comment and Like posts, and edit their contributions.

        Take user input and conditionally allow them to make contributions,
        and modify past contributions. If a visitor is not logged in redirect
        them to the login page upon them sending requests to the server
        for 'Liking' or commenting posts.

        Allow logged in users to comment on post, and 'Like' or 'Unlike' post
        by clicking the appropriate buttons, which will send info to the
        server and in some cases modify the Comment or Likez entities
        where those items are held.

        Display comments and 'Likes' based on the post's Post post_id, which
        is saved in the respective Comment and Likez entities.

        Users can edit or delete a comment, or the post if they created it.
        This is established by checking if their user_id (stored in a cookie)
        matches the post/comment creator id.

        """
        # Retrieve object key with entity name and attribute id number
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        comment = self.request.get("comment")
        current_user = (self.request.cookies.get("user_id")).split("|")[0]
        current_name = (self.request.cookies.get("user")).split("|")[0]
        if comment:
            # User submitted new comment, save it in the Comment entity
            c = Comment(content=comment, name=current_name,
                        creator=current_user, post_id=post_id)
            c.put()  # sends Comment object "c" to the GAE datastore
            sleep(.2)
        self.redirect("/blog/%s" % str(post_id))
