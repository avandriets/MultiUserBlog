from google.appengine.ext import db
from Post import Post
from User import User


def like_key(name='default'):
    return db.Key.from_path('likes', name)


class Like(db.Model):
    post = db.ReferenceProperty(Post, collection_name='like_collection')
    author = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)
