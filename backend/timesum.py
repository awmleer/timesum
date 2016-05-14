# coding:utf-8

from flask import Flask, request, make_response
import time
import random
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

# @app.route('/timesum/api/signin', methonds=['POST'])
# def signin():
    # flag = False
    # uid = request.cookies.get('All_Hell_Fqs')
    # if (uid == None) or (uid == ''):
    #     resp = make_response('no login', 401)
    #     return resp
    # usernam = base64.b64decode(uid)
    # usernam = usernam[18:]
    # for user in client['timesum']['users'].find():
    #     if (str(user['uid']) == usernam):
    #         flag = True
    #         break
    # if (not flag):
    #     resp = make_response('wrong cookies', 401)
    #     return resp

    # return None

@app.route('/timesum/api/short_message_code')
def short_message_code():
    phone = request.args.get('phone')
    db = client['timesum']
    coll_verification = db['verification']
    info = coll_verification.find_one({'phone': phone})
    code = random.randint(1000,9999)
    if (info == None):
        info = {'phone': phone, 'last_verify': int(time.time() * 1000), 'verify_code': code}
        coll_verification.insert(info)
    if (int(time.time() * 1000)-info['last_verify'] < 60000):
        resp = make_response('一分钟之内只能发送一次验证码！', 200)
        return resp
    #发送短信
    coll_verification.update({'phone': phone}, {'$set': {'last_verify': int(time.time() * 1000), 'verify_code': code}})
    resp = make_response('success', 200)
    return resp


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port= 5001)