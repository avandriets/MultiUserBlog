"""
Main dispatcher module
"""
import webapp2

from BaseHandler import BaseHandler
from BlogFrontPage import BlogFrontPage
from DeleteComment import DeleteComment
from DeletePost import DeletePost
from EditComment import EditComment
from EditPost import EditPost
from Login import Login
from Logout import Logout
from NewPost import NewPost
from PostLike import PostLike
from PostPage import PostPage
from Registration import Register
from Welcome import Welcome


class MainPage(BaseHandler):
    """Main page handler"""

    def get(self):
        self.render("main_page.html")


# routes
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', Login),
    ('/logout', Logout),
    ('/signup', Register),
    ('/blog/newpost', NewPost),
    ('/blog/?', BlogFrontPage),
    ('/blog/([0-9]+)', PostPage),
    ('/welcome', Welcome),
    ('/blog/delete-post', DeletePost),
    ('/blog/edit-post', EditPost),
    ('/blog/like', PostLike),
    ('/blog/comment/edit-comment', EditComment),
    ('/blog/comment/delete-comment', DeleteComment),
], debug=True)
