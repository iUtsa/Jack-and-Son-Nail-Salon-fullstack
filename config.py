import os

class Config:
    SECRET_KEY = os.urandom(24)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'noreplyjackandsonnailsspa@gmail.com'
    MAIL_PASSWORD = 'ujex srdw lnne yzvs'
    MAIL_DEFAULT_SENDER = 'noreply-Jack&SonNailSpa@gmail.com'