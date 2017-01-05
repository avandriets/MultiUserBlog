from BaseHandler import BaseHandler
from User import User
from Utility import USER_RE, PASS_RE, EMAIL_RE, SITE_NAME


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(BaseHandler):
    def get(self):
        if not self.user:
            self.render("signup-form.html")
        else:
            self.redirect('/welcome')

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

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
        raise NotImplementedError


class Register(Signup):
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
