"""
Login handler request module
"""
from User import User
from BaseHandler import BaseHandler


class Login(BaseHandler):
    """Login handler class to manage user login"""
    def get(self):
        """to show login method form"""
        self.render('login-form.html')

    def post(self):
        """handle POST login request"""

        # get username and password
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            template_values = {
                'is_errors': True,
                'login_error': 'Invalid login',
            }
            self.render('login-form.html', **template_values)
