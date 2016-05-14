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

def sendsms1(publisher, title, person, mobile):
    d = {'#publisher#': publisher, '#title#': title}
    tpl_value = urllib.urlencode(d)
    finalstr = ''
    getdata = urllib.urlencode({'mobile':mobile,'tpl_id':13216,'tpl_value':tpl_value,'key': 'b32c625ffb38e4ad07f86bb1101548e1'})
    url = 'http://v.juhe.cn/sms/send?%s'%getdata
    req = urllib.urlopen(url)
    result = json.loads(req.read())
    finalstr += '发送给%s的短信的发送结果：%s\n' %(person, result['reason'].encode('utf-8'))
    return finalstr

@app.route('/api/login')
def login():
    phone1 = request.args.get('phone')
    password = request.args.get('password')
    if (phone1 == '' or password == ''):
        resp = make_response('信息不完整', 200)
        return resp
    phone = int(phone1)

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

@app.route('/api/logout')
def logout():
    resp = make_response('success', 200)
    resp.set_cookie('All_Hell_Fqs', '')
    return resp

@app.route('/api/signup', methods=['POST'])
def signup():
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
    text = request.json
    if (text['phone'] == '' or text['name'] == '' or text['password'] == '' or text['code'] == ''):
        resp = make_response('信息不完整', 200)
        return resp
    db = client['timesum']
    coll_verification = db['verification']
    coll_users = db['users']
    if (coll_users.find_one({'phone': int(text['phone'])}) != None):
        resp = make_response('该手机号已经注册', 200)
        return resp
    info = coll_verification.find_one({'phone': int(text['phone'])})
    if (info == None):
        resp = make_response('未发送验证码', 200)
        return resp
    if (int(text['code']) != info['verify_code']):
        resp = make_response('验证码错误', 200)
        return resp
    if (int(time.time() * 1000) - info['last_verify'] > 1200000):
        resp = make_response('验证码已过期', 200)
        return resp
    del text['code']
    coll_meta = db['meta']
    sum = coll_meta.find_one({'meta': 'auto_increase'})['uid']
    sum = sum + 1
    coll_meta.update({'meta': 'auto_increase'}, {'$set': {'uid': sum}})
    text['password'] =hashlib.md5(str(text['password']) + salt).hexdigest()
    text['phone'] = int(text['phone'])
    text.update({'uid': sum, 'last_login': int(time.time() * 1000), 'login_count': 1})
    coll_users.insert(text)
    resp = make_response('success', 200)
    resp.set_cookie('All_Hell_Fqs', base64.b64encode(salt + str(sum)))
    return resp

@app.route('/api/short_message_code')
def short_message_code():
    phone = int(request.args.get('phone'))
    db = client['timesum']
    coll_verification = db['verification']
    info = coll_verification.find_one({'phone': phone})
    code = random.randint(1000,9999)
    flag = True
    if (info == None):
        info = {'phone': phone, 'last_verify': int(time.time() * 1000), 'verify_code': code}
        coll_verification.insert(info)
        flag = False
    if (int(time.time() * 1000) - info['last_verify'] < 60000 and flag):
        resp = make_response('一分钟之内只能发送一次验证码！', 200)
        return resp
    print sendsms1(str(code), 'fuck', 'shit', phone)
    coll_verification.update({'phone': phone}, {'$set': {'last_verify': int(time.time() * 1000), 'verify_code': code}})
    resp = make_response('success', 200)
    return resp


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port= 5001)