"""
Module manages logout process
"""
from BaseHandler import BaseHandler


class Logout(BaseHandler):
    """Logout handler class"""

    def get(self):
        """logout and redirect to main page"""
        self.logout()
        self.redirect('/')
