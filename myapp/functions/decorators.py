from myapp.handlerz.handlerparent import Handler
from google.appengine.ext import db
from myapp.modelz import Comment, Post


def user_logged_in(f):
    """Verify the user is logged in."""
    def wrapper(self, *a, **kw):
        if self.read_secure_cookie("user_id"):
            return f(self, *a, **kw)
        else:
            return self.redirect("/blog/login")
    return wrapper


def comment_exists(f):
    """Verify the requested comment exists."""
    def wrapper(self, post_id):
        key = db.Key.from_path("Comment", int(post_id))
        comment = db.get(key)
        if comment:
            return f(self, post_id)
        else:
            return self.error(404)
    return wrapper


def post_exists(f):
    """Verify the requested post exists."""
    def wrapper(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        if post:
            return f(self, post_id)
        else:
            return self.error(404)
    return wrapper


def user_owns_comment(f):
    """Verify the current user owns the current comment."""
    def wrapper(self, post_id):
        key = db.Key.from_path("Comment", int(post_id))
        comment = db.get(key)
        if self.read_secure_cookie("user_id") == comment.creator:
            return f(self, post_id)
        else:
            return self.redirect("/blog/login")
    return wrapper


def user_owns_post(f):
        """Verify the current user owns the current post."""
    def wrapper(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        if self.read_secure_cookie("user_id") == post.creator:
            return f(self, post_id)
        else:
            return self.redirect("/blog/login")
    return wrapper
