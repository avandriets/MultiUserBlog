"""
secure methods for cookies
"""
import hmac

SECRET_KEY = 'ijxz135d#8b2+t1&5#_g_zu&5juj_(828-7cr6a&!0m'


def make_secure_val(val):
    """make secure cookie"""
    return '%s|%s' % (val, hmac.new(SECRET_KEY, val).hexdigest())


def check_secure_val(secure_val):
    """check cookie"""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val