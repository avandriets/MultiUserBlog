"""
New post handler module
"""
from BaseHandler import BaseHandler
from Post import Post, blog_key


class NewPost(BaseHandler):
    """NewPost manage class"""
    def get(self):
        """GET method to show newpost form"""

        # check if user is in system or redirect to login page
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        """POST method to handle actions related with creating new post"""

        # check if user is login otherwise redirecy to mai page
        if not self.user:
            self.redirect('/blog')
            return

        # get parameters from header
        subject = self.request.get('subject', default_value=None)
        content = self.request.get('content', default_value=None)

        # check if parameters are not empty
        if subject and content:
            subject = subject.strip()
            content = content.strip()

            # create new post
            p = Post(parent=blog_key(), subject=subject, content=content,
                     owner=self.user.key())
            p.put()
            # redirect to post page
            self.redirect('/blog/{}'.format(str(p.key().id())))
        else:
            # something go wrong
            error = "subject and content, please!"
            param = dict(subject=subject, content=content,
                         error=error, is_errors=True)

            self.render("newpost.html", **param)
