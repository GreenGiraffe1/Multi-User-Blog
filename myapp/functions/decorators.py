from myapp.handlerz.handlerparent import Handler
from google.appengine.ext import db
from myapp.modelz import Comment




def user_logged_in(f):
    def wrapper(self, *a, **kw):
        if self.read_secure_cookie("user_id"):
            return f(self, *a, **kw)
        else:
            return self.redirect("/blog/login")
    return wrapper


def comment_exists(f):
    def wrapper(self, post_id):
        key = db.Key.from_path('Comment', int(post_id))
        comment = db.get(key)
        if comment:
            return f(self, post_id)
        else:
            # return self.redirect("/blog/login")
            self.error(404)
            # self.redirect("/blog")
            return
    return wrapper


def user_owns_comment(f):
    def wrapper(self, post_id):
        key = db.Key.from_path('Comment', int(post_id))
        comment = db.get(key)
        if self.read_secure_cookie("user_id") == comment.creator:
            return f(self, post_id)
        else:
            return self.redirect("/blog/login")
            # self.error(404)
            # self.redirect("/blog")
            return
    return wrapper












# END
