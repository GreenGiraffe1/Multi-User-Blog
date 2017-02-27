from handlerparent import Handler
from google.appengine.ext import db
from time import sleep




class DeleteComment(Handler):

    def get(self, comm_id):
        key = db.Key.from_path("Comment", int(comm_id))
        comment = db.get(key)
        post = comment.post_id
        db.delete(key)
        sleep(.2)
        self.redirect("/blog/%s" % str(post))
