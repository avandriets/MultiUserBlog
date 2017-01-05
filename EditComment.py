"""Comment edit tols module"""
from google.appengine.ext import db

from BaseHandler import BaseHandler
from Comment import comment_key
from Post import blog_key


class EditComment(BaseHandler):
    """Edit comment handler class"""

    def post(self):
        """POST edit comment"""

        # check if user have login
        if not self.user:
            self.redirect('/login')
            return

        # get parameters from header
        comment_id = self.request.get("comment_id", None)
        post_id = self.request.get("blog_id", None)
        save = self.request.get("save", None)
        cancel = self.request.get("cancel", None)
        body = self.request.get('body', default_value=None)

        # check if user input just spaces to page
        if body:
            body = body.strip()

        # find post
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        # find comment
        key_comment = db.Key.from_path('Comment', int(comment_id),
                                       parent=comment_key())
        comment = db.get(key_comment)

        # if there is no any posts
        if not (post or comment):
            self.error(404)
            return

        # prepare parameters for rendering page
        param = dict(p=post, subject=post.subject, content=post.content,
                     c=comment, body=comment.body)

        # check if user is owner of post
        if comment.author.key() != self.user.key():
            param["permission_error"] = "You cannot edit this comment," \
                                        " you are not owner!"

            self.render("edit-comment.html", **param)
        else:
            # handle user choice save or not
            if save or cancel:
                if save:
                    if body:
                        comment.body = body
                        comment.save()

                        self.redirect("/blog/{}".format(post_id))
                    else:
                        param["error"] = "Add comment, please!"
                        self.render("edit-comment.html", **param)
                else:
                    self.redirect("/blog/{}".format(post_id))
            else:
                self.render("edit-comment.html", **param)
