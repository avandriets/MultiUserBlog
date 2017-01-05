"""
Comments model module
describe Comment model
"""
from google.appengine.ext import db
from BaseHandler import render_str
from Post import Post
from User import User


def comment_key(name='default'):
    """Provide comment key method"""
    return db.Key.from_path('comments', name)


class Comment(db.Model):
    """Class describe comment model"""
    post = db.ReferenceProperty(Post, collection_name='comments_collection')
    body = db.TextProperty()
    author = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        """mthod for render single user comment"""
        self._render_text = self.body.replace('\n', '<br>')
        param = dict(c=self)
        return render_str("comment.html", **param)
