import hmac
from Utility import SECRET_KEY


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(SECRET_KEY, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val