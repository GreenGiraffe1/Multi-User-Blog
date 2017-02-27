
import os
import re

import hmac
import hashlib
from string import letters
import random
from time import sleep



# value to hash with cookie values to make them secure. (normally this would be
# held in another secure module, but is here for ease of learning.)
SECRET = "LYtOJ9kweSza7sBszlB79z5WEELkEY8O3t6Ll5F4nmj7bWzNLR"

# REGEX to validate user registration inputs
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    """Check username entered to determine if it's valid (with REGEX)."""
    return USER_RE.match(username)


def valid_password(password):
    """Check password entered to determine if it's valid (with REGEX)."""
    return PASSWORD_RE.match(password)


def valid_email(email):
    """Check email entered to determine if it's valid (with REGEX)."""
    return EMAIL_RE.match(email)


def hash_str(s):
    """Hash the user_id and SECRET (a constant) to create a cookie hash."""
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    """When user_id is input, it return the value to set for the cookie."""
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    """Check whether the cookie value from the current webpage is valid."""
    if h:
        val = h.split("|")[0]
        if h == make_secure_val(val):
            return val


def make_salt(length=5):
    """Create a unique salt for hashing a user's password during signup."""
    return "".join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """Make password hash on signup, or check password hash on login."""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()  # sha256 hash algorithm
    return "%s|%s" % (salt, h)


def valid_pw(name, password, h):
    """Check hash of user's login against value in the Credential entity."""
    salt = h.split("|")[0]
    return h == make_pw_hash(name, password, salt)
