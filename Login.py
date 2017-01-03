from User import User
from Utility import SITE_NAME
from BaseHandler import BaseHandler


class Login(BaseHandler):
    def get(self):
        template_values = {
        }
        self.render('login-form.html', **template_values)

    def post(self):
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
