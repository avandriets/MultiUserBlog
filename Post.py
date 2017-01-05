from google.appengine.ext import db
from BaseHandler import render_str
from User import User


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    owner = db.ReferenceProperty(User, collection_name='blogs_collection')
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def get_lead(self):
        words_list = self.content.split()
        last_word = ""

        if len(words_list) > 50:
            lst = words_list[:50]
            last_word = " ..."
        else:
            lst = words_list

        output_str = ""
        for word in lst:
            output_str += word + " "
        return output_str + last_word

    def get_owner_id(self):
        if self.owner:
            return self.owner.key().id()
        else:
            return None

    def render_short(self):
        self._render_text = self.get_lead().replace('\n', '<br>')
        param = dict(p=self)
        return render_str("post.html", **param)

    def render_full(self):
        self._render_text = self.content.replace('\n', '<br>')
        param = dict(p=self)
        return render_str("post.html", **param)
