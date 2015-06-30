# -*- coding: utf8 -*-

# for the database

from app import db
from babel.dates import format_date

class User(db.Model):
    "main class of users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(64))
    firstname = db.Column(db.String(64), index=True)
    last_connection = db.Column(db.DateTime)
    timezone = db.Column(db.String(5), default='fr_FR')

    posts = db.relationship('Post', backref='author', lazy='dynamic') # so we can use post.author to get the User instance that created a post

    @staticmethod
    def useless_method():
        "I am static, that's why you can call me without any user (self) parameter !"
        print 'i am an useless static method'

    def avatar(self):
        return 'chemin-vers-l-image'

    def is_authenticated(self):
        "should just return True unless the object represents a user that should not be allowed to authenticate for some reason"
        print 'AUTHENTICATED'
        print 'user_id:', self.get_id()
        return True 

    def is_active(self):
    #TODO: useless function?
        "should return True for users unless they are inactive, for example because they have been banned"
        return True
    def is_anonymous(self):
    #TODO: useless function?
        "should return True only for fake users that are not supposed to log in to the system"
        return False

    def get_id(self):
        "should return a unique identifier for the user, in unicode format"
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def getPasswd(self):
        "envoie un mail avec un nouveau mot de passe"
        #à implémenter
        return True
        #si ça ne fonctionne pas
        return False

    def getLastConnection(self):
        """return user (self) lastConnection attribute according to user timezone"""
        return format_date(self.last_connection, locale=self.timezone)


    def __repr__(self):
        return '<User %r> (%r)' % (self.email, self.firstname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime) # attention, à l'utilisation : enregistrer le temps UTC, parce qu'on a potentiellement des users du monde entier !
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
