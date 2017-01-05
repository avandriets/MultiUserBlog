from BaseHandler import BaseHandler


class Welcome(BaseHandler):
    def get(self):
        if self.user:
            self.render('welcome.html')
        else:
            self.redirect('/signup')
