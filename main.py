"""This module performs all the backend functions of Matt's Blog.

This document, the HTML pages, and the database entities are stored / hosted
by Google App Engine. This module supports registration, login, and logging
out with password hashing and secure cookies. Logged in users may create blog
posts, comment on posts, like other's posts, and delete or edit their own blog
posts or comments.

"""


import webapp2
from myapp.handlerz import (DeleteComment, DeletePost, LikePost, LogOut,
                           MainPage, UnlikePost, EditComment, EditPost, Blog,
                           Login, NewPost, PostPage, Signup)


app = webapp2.WSGIApplication([("/", MainPage),
                               ("/blog/signup", Signup),
                               ("/blog/login", Login),
                               ("/blog/logout", LogOut),
                               ("/blog", Blog),
                               ("/blog/newpost", NewPost),
                               ("/blog/([0-9]+)", PostPage),
                               ("/blog/unlike/([0-9]+)", UnlikePost),
                               ("/blog/like/([0-9]+)", LikePost),
                               ("/blog/edit/([0-9]+)", EditPost),
                               ("/blog/editcomment/([0-9]+)", EditComment),
                               ("/blog/deletecomment/([0-9]+)", DeleteComment),
                               ("/blog/deletepost/([0-9]+)", DeletePost),
                               ],
                              debug=True)
