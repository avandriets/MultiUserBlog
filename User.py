"""Used model module"""
import random
import hashlib
from string import letters
from google.appengine.ext import db


def make_salt(length=5):
    """make salt function"""
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """make password hash"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    """password validation function"""
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    """user key function"""
    return db.Key.from_path('users', group)


class User(db.Model):
    """User model class"""
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """get user by id"""
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """get user by name"""
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """register user"""
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        """login user"""
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
