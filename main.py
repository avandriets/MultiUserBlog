import webapp2
from BaseHandler import BaseHandler
from Login import Login
from Logout import Logout
from Registration import Register
from Utility import SITE_NAME


class MainPage(BaseHandler):
    def get(self):
        template_values = {
            'site_name': SITE_NAME,
            'is_authenticated': False,
        }
        self.render("main_page.html", **template_values)

    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', Login),
    ('/logout', Logout),
    ('/signup', Register)
], debug=True)
