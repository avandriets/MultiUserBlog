"""
Front Page module
"""
from BaseHandler import BaseHandler
from Post import Post
from User import User


class BlogFrontPage(BaseHandler):
    """Front page class"""

    def get(self):
        """ GET method to render front page with posts list"""
        user_id = self.request.get('user_id', None)
        if user_id is not None:
            user = User.by_id(int(user_id))

            posts = user.blogs_collection.order('-created')
        else:
            posts = Post.all().order('-created')

        context = dict(posts=posts, )
        self.render("blog_front_page.html", **context)
