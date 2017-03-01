from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Post
from myapp.functions.decorators import user_logged_in


class NewPost(Handler):

    """Accept user input of a blog post, and save it in the Post entity."""

    def render_newpost(self, subject="", content="", error=""):
        """Render newpost page where user can create blog posts."""
        uname = self.identify()
        self.render("newpost.html", subject=subject, content=content,
                    error=error, uname=uname)

    @user_logged_in
    def get(self):
        """Call method that renders the newpost page if user is logged in."""
        self.render_newpost()

    @user_logged_in
    def post(self):
        """Coditionally create new blog posts.

        Accept user input for blog post subject and content, and if the user
        is signed in (checked for by examining cookies), and they have
        included both a subject and content, create a new post object in the
        Post entity. If the visitor is not logged in, redirect them to the
        login page to do so. If the user doesn't enter both a subject and
        content, prompt them to do so with an error message.

        """
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            name = (self.request.cookies.get("user")).split("|")[0]
            creator = (self.request.cookies.get("user_id")).split("|")[0]
            p = Post(subject=subject, content=content, creator=creator,
                     name=name)
            p.put()  # sends Post object "p" to the GAE datastore
            sleep(.2)
            self.redirect("/blog/%s" % str(p.key().id()))
        else:
            error = ("You need to enter both a Subject and Content to create "
                     "a new post.")
            self.render_newpost(subject, content, error)
