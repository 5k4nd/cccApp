# -*- coding: utf8 -*-


# main
from flask import Flask
cccApp = Flask(__name__)
cccApp.config.from_object('config')


# db
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(cccApp) ### à terme, cccDb ?


# sessions, users and logins
import os
from flask.ext.login import LoginManager # handle our users logged in state
from config import basedir
lm = LoginManager() ### à terme, cccLm ?
lm.init_app(cccApp)
lm.login_view = 'login' # specifies the view which logs users in (for @login_required decorator)


from app import views, models


# bug mail report on production
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
if not cccApp.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'cccApp failure on baptabl production server', credentials)
    mail_handler.setLevel(logging.ERROR)
    cccApp.logger.addHandler(mail_handler)



# log into file
if not cccApp.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('data/cccApp.log', 'a', 1 * 1024 * 1024, 10) # log file size limited to 1Mb ; keep last 10 log files as backup
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    cccApp.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    cccApp.logger.addHandler(file_handler)
    cccApp.logger.info('cccApp startup')
