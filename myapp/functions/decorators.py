from myapp.handlerz.handlerparent import Handler
from google.appengine.ext import db
from myapp.modelz import Comment, Post




def user_logged_in(f):
    def wrapper(self, *a, **kw):
        if self.read_secure_cookie("user_id"):
            return f(self, *a, **kw)
        else:
            # return
            return self.redirect("/blog/login")
            # return
    return wrapper


def comment_exists(f):
    def wrapper(self, post_id):
        key = db.Key.from_path('Comment', int(post_id))
        comment = db.get(key)
        if comment:
            return f(self, post_id)
        else:
            # return self.redirect("/blog/login")
            return self.error(404)
            # self.redirect("/blog")
            # return
    return wrapper


def post_exists(f):
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if post:
            return f(self, post_id)
        else:
            # return self.redirect("/blog/login")
            return self.error(404)
            # self.redirect("/blog")
            # return
    return wrapper


def user_owns_comment(f):
    def wrapper(self, post_id):
        key = db.Key.from_path('Comment', int(post_id))
        comment = db.get(key)
        if self.read_secure_cookie("user_id") == comment.creator:
            return f(self, post_id)
        else:
            # return self.redirect("/blog/login")
            return self.redirect("/blog/login")
            # self.error(404)
            # self.redirect("/blog")
            # return
    return wrapper


def user_owns_post(f):
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if self.read_secure_cookie("user_id") == post.creator:
            return f(self, post_id)
        else:
            # return self.redirect("/blog/login")
            return self.redirect("/blog/login")
            # self.error(404)
            # self.redirect("/blog")
            # return
    return wrapper









# END
