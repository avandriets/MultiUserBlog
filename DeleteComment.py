"""
Module provide tools to delete comment from database
"""
from google.appengine.ext import db
from BaseHandler import BaseHandler
from Comment import comment_key
from Post import blog_key


class DeleteComment(BaseHandler):
    """
        Delete comment render class provide methods to show interface for
        deleting comment from db
    """

    def post(self):
        """POST method to show delete page and manage deleting process"""

        if not self.user:
            # if user is not login redirect him to login page
            self.redirect('/login')
            return

        # get post id and user choice whether delete or not (yes/no
        # parameters)
        comment_id = self.request.get("comment_id", None)
        post_id = self.request.get("blog_id", None)
        yes = self.request.get("yes", None)
        no = self.request.get("no", None)

        # get post by key
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        # find comment
        key_comment = db.Key.from_path('Comment', int(comment_id),
                                       parent=comment_key())
        comment = db.get(key_comment)

        # show 404 if something go wrong with post
        if not (post or comment):
            self.error(404)
            return

        # fill parameters for render page
        param = dict(p=post, c=comment)

        # check if user if owner of post
        if post.owner.key() != self.user.key():
            param["is_errors"] = True
            param["error"] = "You cannot delete this comment," \
                             " you are not owner!"

            self.render("delete-comment.html", **param)
        else:
            # handle user choice delete or not
            if yes or no:
                if yes:
                    comment.delete()
                    self.redirect("/blog/{}".format(post_id))
                else:
                    self.redirect("/blog/{}".format(post_id))
                pass
            else:
                self.render("delete-comment.html", **param)
