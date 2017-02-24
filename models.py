from google.appengine.ext import db


class Credential(db.Model):

    """Store all attributes of user login credentials in this entity."""

    username = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    hashed_password = db.TextProperty(required=True)


class Post(db.Model):

    """Store all attributes of blog posts in this entity."""

    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    creator = db.StringProperty(required=False)
    name = db.StringProperty(required=False)


class Comment(db.Model):

    """Store all attributes of comments (written on blog posts)."""

    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    creator = db.StringProperty(required=True)
    name = db.StringProperty(required=False)
    post_id = db.StringProperty(required=True)
    mod = db.BooleanProperty(required=False)


class Likez(db.Model):

    """Store all attributes of 'Likes' for blog posts."""

    does_like = db.BooleanProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    creator = db.StringProperty(required=True)
    name = db.StringProperty(required=False)
    post_id = db.StringProperty(required=True)
