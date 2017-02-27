from handlerparent import Handler
from myapp.modelz import Post
# from google.appengine.ext import db  # might not need this


class Blog(Handler):

    """Display 10 most recent posts from Post entity on main blog page."""

    def render_fpage(self):
        """Display the main blog page.

        Query the Post entity for the 10 most recent blog posts and display
        them in descending order of their creation date / time, along with
        their author and when they were first posted.

        """
        # Query the Google App Engine (GAE) datastore, Post entity, return the
        # 10 most recent posts in descending order of creation time.
        posts = Post.all().order("-created").fetch(limit=10)
        uname = self.identify()
        self.render("blog.html", posts=posts, uname=uname)

    def get(self):
        """Call function that renders the main blog page."""
        self.render_fpage()
