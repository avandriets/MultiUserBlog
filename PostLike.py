"""
Post liking module
"""
from google.appengine.ext import db
from BaseHandler import BaseHandler
from Like import Like, like_key
from Post import blog_key


class PostLike(BaseHandler):
    """Post liking handler class"""

    def post(self):
        """handle POST like request"""

        # redirect user to login page if he doesnt login yet
        if not self.user:
            self.redirect('/login')
            return

        # get blog_id parameter
        post_id = self.request.get("blog_id", None)

        # get post from DB by key
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        # get post likes from DB
        likes_list = post.like_collection

        # check if user already likes this post
        set_like_already = False
        for acc in likes_list:
            if acc.author.key() == self.user.key():
                set_like_already = True

        # prepare params for render page
        param = dict(post=post)

        # check that you cannot like your own post
        if post.owner.key() == self.user.key():
            param["error"] = "You cannot like this post, you are owner!"
            self.render("like-post.html", **param)
        else:
            # check if you like post already
            if set_like_already:
                param["error"] = "You have liked this post already!"
                self.render("like-post.html", **param)
            else:
                # add like to db
                n_l = Like(parent=like_key(), post=post,
                           author=self.user.key())
                n_l.put()
                self.redirect('/blog/{}'.format(post_id))
