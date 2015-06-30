#!../maelstromEnv/bin/python
# -*- coding: utf8 -*-

import os
import unittest

from config import basedir
from app import cccApp, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        cccApp.config['TESTING'] = True
        cccApp.config['WTF_CSRF_ENABLED'] = False
        cccApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.cccApp = cccApp.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_unique_email(self):
        u = User(firstname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        email1 = u.email
        u = User(firstname='susan', email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        email2 = u.email
        assert email1 != 'john@example.com'
        assert email1 != email2

if __name__ == '__main__':
    unittest.main()