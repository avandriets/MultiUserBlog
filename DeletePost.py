"""
Module provide tools to delete post from database
"""
from google.appengine.ext import db
from BaseHandler import BaseHandler
from Post import blog_key


class DeletePost(BaseHandler):
    """
    Delete post render class provide methods to show interface for deleting
    post from db
    """

    def post(self):
        """POST method to show delete page and manage deleting process"""

        if not self.user:
            # if user is not login redirect him to login page
            self.redirect('/login')
        else:
            # get post id and user choice whether delete or not (yes/no
            # parameters)
            post_id = self.request.get("blog_id", None)
            yes = self.request.get("yes", None)
            no = self.request.get("no", None)

            # get post by key
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            # show 404 if something go wrong with post
            if not post:
                self.error(404)
                return

            # fill parameters for render page
            param = dict(p=post)

            # check if user if owner of post
            if post.owner.key() != self.user.key():
                param["is_errors"] = True
                param[
                    "error"] = "You cannot delete this post, you are not owner!"

                self.render("delete-post.html", **param)
            else:
                # handle user choice delete or not
                if yes or no:
                    if yes:
                        post.delete()
                        self.redirect("/")
                    else:
                        self.redirect("/blog/{}".format(post_id))
                    pass
                else:
                    self.render("delete-post.html", **param)
