from handlerparent import Handler
from google.appengine.ext import db
from time import sleep
from myapp.modelz import Comment


class EditComment(Handler):

    def get(self, post_id):
        uname = self.identify()
        # Retrieve object key with entity name and attribute id number
        key = db.Key.from_path("Comment", int(post_id))
        comment = db.get(key)
        self.render("editcomment.html", comment=comment, uname=uname)

    def post(self, post_id):
        key = db.Key.from_path("Comment", int(post_id))
        comment = db.get(key)
        update_c_text = self.request.get("comment_update")
        if update_c_text:
            comment.content = update_c_text
            comment.put()  # sends updated Post object "post" to GAE datastore
            sleep(.2)
        self.redirect("/blog/%s" % str(comment.post_id))
