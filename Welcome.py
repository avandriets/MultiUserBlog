"""
Welcome page handler module
"""
from BaseHandler import BaseHandler


class Welcome(BaseHandler):
    """page handler"""
    def get(self):
        if self.user:
            self.render('welcome.html')
        else:
            self.redirect('/signup')
