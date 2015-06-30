#!/usr/bin/env python2
# -*- coding: utf8 -*-


#from jormungandr.libraries.libsynthese.utils.controller import ServiceCall
#from jormungandr.libraries.libsynthese.utils.l10n_config import string_content
#from jormungandr.libraries.libsynthese.utils.l10n_date import strftime
#from jormungandr.modules_loader import ABlueprint
#from collections import defaultdict
#import datetime

import os
from flask import Flask, render_template, session, jsonify, request, g, redirect, url_for, flash, make_response#, abort, Response
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func, Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from flask.ext.wtf import Form
from jinja2 import TemplateNotFound
from werkzeug import generate_password_hash, check_password_hash
from wtforms import TextField, TextAreaField, SubmitField, ValidationError, PasswordField, DateTimeField, HiddenField
from wtforms.validators import Required, Email, length
from wtforms_components import DateRange
from datetime import datetime, date, time
#from flask.ext.bcrypt import Bcrypt, gensalt
import bcrypt
import random, string
from flask_bootstrap import Bootstrap
from flask.ext.mail import Mail, Message
import json
#from flask.ext.admin import Admin, BaseView, expose
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, roles_required


#import psycopg2
#import psycopg2.extras


