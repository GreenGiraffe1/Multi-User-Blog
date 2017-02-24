from google.appengine.ext import db


class Post(db.Model):

    """Store all attributes of blog posts in this entity."""

    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    creator = db.StringProperty(required=False)
    name = db.StringProperty(required=False)
