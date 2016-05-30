# coding:utf-8

from flask import Flask, request, make_response
import random
import urllib
import urllib2
import hashlib
import base64
import pymongo
import json
import time
import datetime
from pymongo import MongoClient
from mongoengine import *
import bson
from bson import Binary, Code
from bson.json_util import dumps, loads
from flask.ext.cors import CORS      #跨域访问
# --------------------我是分界线--------------------
connect('timesum', host='121.42.209.162', username='fqs1', password='123456')    #登录及用户认证
# --------------------我是分界线--------------------
class participators_in(EmbeddedDocument):
    uid=IntField(required=True)
    time_inputed=BooleanField(required=True, default=False)

class date_in(EmbeddedDocument):
    year = StringField(required=True)
    month = StringField(required=True)
    day = StringField(required=True)

class data_in(EmbeddedDocument):
    date = EmbeddedDocumentField(date_in, required=True)
    timeblocks = StringField(required=True)

class time_format(EmbeddedDocument):
    year = StringField(required=True)
    month = StringField(required=True)
    day = StringField(required=True)
    time = StringField(required=True)

class time_collection_in(EmbeddedDocument):
    uid = IntField(required=True)
    data = ListField(EmbeddedDocumentField(data_in), required=True)

class comments_in(EmbeddedDocument):
    uid = IntField(required=True)
    time = IntField(required=True)
    text = StringField(required=True)
# --------------------我是分界线--------------------
class me_ta(Document):
    me_ta = StringField(required=True)
    aid = IntField(required=True)
    uid = IntField(required=True)
# --------------------我是分界线--------------------
class activity(Document):
    aid = IntField(required=True)
    publisher = IntField(required=True)
    title = StringField(required=True, default='')
    description = StringField(required=True, default='')
    place = StringField(required=True, default='')
    organizer = StringField(required=True, default='')
    opening = BooleanField(required=True, default=True)
    history = BooleanField(required=True, default=False)
    participators = ListField(EmbeddedDocumentField(participators_in), default=[])
    time_collection = ListField(EmbeddedDocumentField(time_collection_in), default=[])
    expected_number = IntField(required=True)
    duration = IntField(required=True)
    published_time = IntField(required=True)
    time_determined = ListField(EmbeddedDocumentField(time_format), default=[])
    date_range = ListField(EmbeddedDocumentField(date_in), default=[])
    comments = ListField(EmbeddedDocumentField(comments_in), default=[])
# --------------------我是分界线--------------------
class ac_deleted(Document):
    aid = IntField(required=True)
    publisher = IntField(required=True)
    title = StringField(required=True, default='')
    description = StringField(required=True, default='')
    place = StringField(required=True, default='')
    organizer = StringField(required=True, default='')
    opening = BooleanField(required=True, default=True)
    history = BooleanField(required=True, default=False)
    participators = ListField(EmbeddedDocumentField(participators_in), default=[])
    time_collection = ListField(EmbeddedDocumentField(time_collection_in), default=[])
    expected_number = IntField(required=True)
    duration = IntField(required=True)
    published_time = IntField(required=True)
    time_determined = ListField(EmbeddedDocumentField(time_format), default=[])
    date_range = ListField(EmbeddedDocumentField(date_in), default=[])
    comments = ListField(EmbeddedDocumentField(comments_in), default=[])
# --------------------我是分界线--------------------
class users(Document):
    uid = IntField(required=True)
    name = StringField(required=True)
    phone = StringField(required=True)
    password = StringField(required=True)
    last_login = IntField(required=True)
    login_count = IntField(required=True)
# --------------------我是分界线--------------------
class verification(Document):
    phone = StringField(required=True)
    last_verify = IntField(required=True)
    verify_code = StringField(required=True)
# --------------------我是分界线--------------------