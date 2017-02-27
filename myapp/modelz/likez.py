from google.appengine.ext import db


class Likez(db.Model):

    """Store all attributes of 'Likes' for blog posts."""

    does_like = db.BooleanProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    creator = db.StringProperty(required=True)
    name = db.StringProperty(required=False)
    post_id = db.StringProperty(required=True)
