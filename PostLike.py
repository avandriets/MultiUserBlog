from google.appengine.ext import db

from BaseHandler import BaseHandler
from Like import Like, like_key
from Post import blog_key


class PostLike(BaseHandler):
    def post(self):

        if not self.user:
            self.redirect('/login')
            return

        post_id = self.request.get("blog_id", None)

        if not post_id:
            self.error(404)
            return

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        likes_list = post.like_collection
        set_like = False

        for acc in likes_list:
            if acc.author.key() ==self.user.key():
                set_like = True

        param = dict(post=post)

        if post.owner.key() == self.user.key():
            param["error"] = "You cannot like this post, you are owner!"
            self.render("like-post.html", **param)
        else:
            if set_like:
                param["error"] = "You have liked this post already!"
                self.render("like-post.html", **param)
            else:
                n_l = Like(parent=like_key(), post=post,
                              author=self.user.key())
                n_l.put()
                self.redirect('/blog/{}'.format(post_id))