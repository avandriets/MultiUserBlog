import re

SECRET_KEY = 'ijxz135d#8b2+t1&5#_g_zu&5juj_(828-7cr6a&!0m'
SITE_NAME = "Multi-User-Blog"
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')