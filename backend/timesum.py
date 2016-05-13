# coding:utf-8

from flask import Flask, request, make_response
import time
import urllib
import urllib2
import hashlib
import base64
import pymongo
import json
import datetime
from pymongo import MongoClient
import bson
from bson import Binary, Code
from bson.json_util import dumps, loads
from flask.ext.cors import CORS      #跨域访问

app = Flask(__name__)
CORS(app)   #跨域访问

#登录及用户认证
client = MongoClient('121.42.209.162', 27017)
client.admin.authenticate('fqs', '123456', mechanism='MONGODB-CR')
uri = "mongodb://fqs:123456@121.42.209.162/admin?authMechanism=MONGODB-CR"
client = MongoClient(uri)

salt = '5aWZak2n35Wk fqsws'

@app.route('/timesum/api/login')
def login():
    phone = request.args.get('phone')
    password = request.args.get('password')

    db = client['timesum']
    coll_users = db['users']
    userinfo = coll_users.find_one({'phone': phone})
    if (userinfo == None):
        resp = make_response('wrong phone', 200)
        return resp
    passwo = userinfo['password']
    password_hash = hashlib.md5(password + salt).hexdigest()
    if passwo == password_hash:
        resp = make_response('success', 200)
        resp.set_cookie('All_Hell_Fqs', base64.b64encode(salt + str(userinfo['uid'])))
    else:
        resp = make_response('wrong password', 200)
    return resp

@app.route('/timesum/api/logout')
def logout():
    resp = make_response('success', 200)
    resp.set_cookie('All_Hell_Fqs', '')
    return resp


