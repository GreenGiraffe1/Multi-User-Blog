from google.appengine.ext import db


class Comment(db.Model):

    """Store all attributes of comments (written on blog posts)."""

    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    creator = db.StringProperty(required=True)
    name = db.StringProperty(required=False)
    post_id = db.StringProperty(required=True)
    mod = db.BooleanProperty(required=False)
