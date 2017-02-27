from google.appengine.ext import db


class Credential(db.Model):

    """Store all attributes of user login credentials in this entity."""

    username = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    hashed_password = db.TextProperty(required=True)
