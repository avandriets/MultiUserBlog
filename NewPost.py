from BaseHandler import BaseHandler
from Post import Post, blog_key


class NewPost(BaseHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject', default_value=None)
        content = self.request.get('content', default_value=None)

        if subject and content:
            subject = subject.strip()
            content = content.strip()

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content,
                     owner=self.user.key())
            p.put()
            self.redirect('/blog/{}'.format(str(p.key().id())))
        else:
            error = "subject and content, please!"
            param = dict(subject=subject, content=content,
                         error=error, is_errors=True)

            self.render("newpost.html", **param)
