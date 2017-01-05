from google.appengine.ext import db

from BaseHandler import BaseHandler
from Post import blog_key


class DeletePost(BaseHandler):
    def post(self):

        if not self.user:
            self.redirect('/login')
        else:
            post_id = self.request.get("blog_id", None)
            yes = self.request.get("yes", None)
            no = self.request.get("no", None)

            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            param = dict(p=post)

            if post.owner.key() != self.user.key():
                param["is_errors"] = True
                param["error"] = "You cannot delete this post, you are not owner!"

                self.render("delete-post.html", **param)
            else:
                if yes or no:
                    if yes:
                        post.delete()
                        self.redirect("/")
                    else:
                        self.redirect("/blog/{}".format(post_id))
                    pass
                else:
                    self.render("delete-post.html", **param)

