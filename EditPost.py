from google.appengine.ext import db
from BaseHandler import BaseHandler
from Post import blog_key


class EditPost(BaseHandler):
    def post(self):

        if not self.user:
            self.redirect('/login')
        else:
            post_id = self.request.get("blog_id", None)
            save = self.request.get("save", None)
            cancel = self.request.get("cancel", None)
            subject = self.request.get('subject', default_value=None)
            content = self.request.get('content', default_value=None)

            if subject and content:
                subject = subject.strip()
                content = content.strip()

            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            param = dict(p=post, subject=post.subject,
                         content=post.content)

            if post.owner.key() != self.user.key():
                param["is_errors"] = True
                param["error"] = "You cannot edit this post, you are not owner!"

                self.render("edit-post.html", **param)
            else:
                if save or cancel:
                    if save:
                        if subject and content:
                            post.subject = subject
                            post.content = content
                            post.save()

                            self.redirect("/blog/{}".format(post_id))
                        else:
                            param["edit_error"] = "subject and content, please!"
                            self.render("edit-post.html", **param)
                    else:
                        self.redirect("/blog/{}".format(post_id))
                else:
                    self.render("edit-post.html", **param)
