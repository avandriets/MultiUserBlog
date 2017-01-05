"""
Post managing module
"""
from google.appengine.ext import db
from BaseHandler import BaseHandler
from Comment import Comment, comment_key
from NewPost import blog_key


class PostPage(BaseHandler):
    """class handler for PostPage"""

    def get(self, post_id):
        """GET method to show post page """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        # check if post exists
        if not post:
            self.error(404)
            return

        # get post comments from DB
        comments = post.comments_collection.order('-created')
        like_count = post.like_collection.count()

        # prepare variables to render
        param = dict(post=post, comments=comments, like_count=like_count)
        self.render("permalink.html", **param)

    def post(self, post_id):
        """POST method for handle add comment action"""
        if not self.user:
            self.redirect('/login')
        else:
            # get post
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            # if post not exists go to 404 !!!
            if not post:
                self.error(404)
                return

            # get post comments from DB
            comments = post.comments_collection.order('-created')

            # get entered comment and check if it is not empty
            comment = self.request.get('comment', default_value=None)
            if comment:
                comment = comment.strip()

            # add comment to db and render or show error page
            if comment:
                n_c = Comment(parent=comment_key(), post=post, body=comment,
                              author=self.user.key())
                n_c.put()
                self.redirect('/blog/{}'.format(str(post.key().id())))
            else:
                like_count = post.like_collection.count()
                error = "Enter comment, please!"
                param = dict(error=error, post=post, comments=comments
                             , like_count=like_count)

                self.render("permalink.html", **param)
