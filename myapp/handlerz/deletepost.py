from handlerparent import Handler
from google.appengine.ext import db
from time import sleep


class DeletePost(Handler):

    def get(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        db.delete(key)
        sleep(.2)
        self.redirect("/blog")
