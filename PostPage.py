from google.appengine.ext import db
from BaseHandler import BaseHandler
from Comment import Comment, comment_key
from NewPost import blog_key


class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        comments = post.comments_collection.order('-created')
        like_count = post.like_collection.count()

        param = dict(post=post, comments=comments, like_count = like_count)
        self.render("permalink.html", **param)

    def post(self, post_id):
        if not self.user:
            self.redirect('/login')
        else:
            comment = self.request.get('comment', default_value=None)
            # post_id = self.request.get("blog_id", None)

            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            comments = post.comments_collection.order('-created')

            if comment:
                comment = comment.strip()

            if comment:
                n_c = Comment(parent=comment_key(), post=post, body=comment,
                        author=self.user.key())
                n_c.put()
                self.redirect('/blog/{}'.format(str(post.key().id())))
            else:
                like_count = post.like_collection.count()
                error = "Enter comment, please!"
                param = dict(error=error, post=post, comments=comments
                             , like_count = like_count)

                self.render("permalink.html", **param)

