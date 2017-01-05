"""
This module are used to register new user in the site
"""
from BaseHandler import BaseHandler
from User import User
import re

# Regular expressions to check user input
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")


def valid_username(username):
    """This function check if user correct input username"""
    return username and USER_RE.match(username)


def valid_password(password):
    """This function check if user correct input password"""
    return password and PASS_RE.match(password)


def valid_email(email):
    """This function check if user correct input email"""
    return not email or EMAIL_RE.match(email)


class Signup(BaseHandler):
    """Base Signup user class. It implements user registration methods"""

    def get(self):
        """GET method shows user registration form if user is not login and
        welcome page if he is"""
        if not self.user:
            self.render("signup-form.html")
        else:
            self.redirect('/welcome')

    def post(self):
        """POST method registers user in system"""

        # get parameters
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        # save parameters to dictionary for form rendering
        params = dict(username=self.username,
                      email=self.email)

        # checking input parameters
        if not valid_username(self.username):
            params['is_username_errors'] = True
            params['username_error'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['is_password_errors'] = True
            params['password_error'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['is_verify_errors'] = True
            params['verify_error'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['is_email_errors'] = True
            params['email_error'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        """ this method registers user"""
        raise NotImplementedError


class Register(Signup):
    """Child signup class that implements methods for crating user """

    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)

        params = dict(username=self.username,
                      email=self.email)

        if u:
            params['is_username_errors'] = True
            params['username_error'] = "That user already exists."
            self.render('signup-form.html', **params)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')
