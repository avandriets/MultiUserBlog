"""
Module for base classes
"""
import os
import jinja2
import webapp2
from User import User
from security import make_secure_val, check_secure_val

SITE_NAME = "Multi-User-Blog"
"""Site name variable"""

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    """render jinja template function"""
    t = jinja_env.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):
    """Base HTTP request handler."""

    def write(self, *a, **kw):
        """method for render html string"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """method for render html from template"""
        params['user'] = self.user
        params['site_name'] = SITE_NAME

        return render_str(template, **params)

    def render(self, template, **kw):
        """method for render html from template"""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """method for setting cookies"""
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """method for reading cookies"""
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """login and set cooke"""
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """logout and erase cooke"""
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """Init RequestHandler and set user attribute"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))