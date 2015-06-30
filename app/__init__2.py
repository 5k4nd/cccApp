#!/usr/bin/env python2
# -*- coding: utf8 -*-

from importandconfig import *




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bat:bat@127.0.0.1:5432/bat"

db = SQLAlchemy(app)
#Bootstrap(app) # à reprendre
mail = Mail(app)
#bcrypt = Bcrypt(app) #useless 'cause included in werkzeug






# configuration et lancement de l'appli
def setup():
    #Jormungandr-remove: replace app by self
    app.add_url_rule('/login', 'login', login, methods = {'GET', 'POST'})
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/test', 'test', test, methods = {'GET', 'POST'})
    #app.add_url_rule(u'/editUser', 'editUser', editUser, methods = {'POST'})
    #app.add_url_rule('/signup', 'signup', signup)

    #les route ci-dessous garantissent la continuité du service (ces redirections sont actuellement utilisées en prod.
    #idélement, elles seront retirées dans une verison ultérieure.

    #Jormungandr-remove
    app.secret_key = 'iAmBaptAbl'

    # Flask-Mail settings
    app.MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    app.MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    app.MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    app.MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    app.MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    app.MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))
    app.USER_APP_NAME =           "AppName" # Used by email templates


# Jormungandr-remove
#class DRTReservation(ABlueprint):
def __init__(self, api, name):
    super(DRTReservation, self).__init__(api, name, __name__, index_endpoint='index',
            description="DRT reservation app", status="testing",
            static_folder='static', template_folder='templates'
            )

    #Jormungandr-remove
#il faut également réinstaurer les paramètres implicites 'self' dans quasiment toutes les def
if __name__ == "__main__":
    setup()
    db.init_app(app)
    #db.create_all()
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)
    app.run(host='0.0.0.0',
            port=7776,
            debug=True,
            )

