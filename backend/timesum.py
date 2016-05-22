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
from mongoengine import *
from datetime import datetime
import bson
from bson import Binary, Code
from bson.json_util import dumps, loads
from flask.ext.cors import CORS      #跨域访问
# --------------------我是分界线--------------------
app = Flask(__name__)
CORS(app)   #跨域访问
# --------------------我是分界线--------------------
connect('timesum', host='121.42.209.162', username='fqs1', password='123456')    #登录及用户认证
# --------------------我是分界线--------------------
class me_ta(Document):
    me_ta = StringField(required=True)
    activity = IntField(required=True)
    uid = IntField(required=True)
# --------------------我是分界线--------------------
class participators_in(EmbeddedDocument):
    uid=IntField(required=True)
    time_inputed=BooleanField(required=True)

class date_in(EmbeddedDocument):
    year = StringField(required=True)
    month = StringField(required=True)
    day = StringField(required=True)

class data_in(EmbeddedDocument):
    date = EmbeddedDocumentField(date_in, required=True)
    timeblocks = StringField(required=True)

class time_collection_in(EmbeddedDocument):
    uid = IntField(required=True)
    data = ListField(EmbeddedDocumentField(data_in), required=True)

class comments_in(EmbeddedDocument):
    uid = IntField(required=True)
    time = IntField(required=True)
    text = StringField(required=True)

class activity(Document):
    aid = IntField(requird=True)
    publisher = IntField(requird=True)
    title = StringField(required=True)
    description = StringField(required=True)
    place = StringField(required=True)
    organizer = StringField(required=True)
    opening = BooleanField(required=True)
    history = BooleanField(required=True)
    participators = ListField(EmbeddedDocumentField(participators_in), required=True)
    time_collection = ListField(EmbeddedDocumentField(time_collection_in), required=True)
    expected_number = IntField(required=True)
    expected_duration = IntField(required=True)
    published_time = IntField(required=True)
    time_determined = IntField(required=True)
    date_range = ListField(EmbeddedDocumentField(date_in), required=True)
    comments = ListField(EmbeddedDocumentField(comments_in), required=True)
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
salt = '5aWZak2n35Wk fqsws'

# aaaa = dict(users.objects(uid=1).first().to_mongo())
# print aaaa
# aaa = {'phone':'65466','last_verify':312351,'verify_code': '6546'}
# bbbb = dumps(aaa)
# cc = verification.from_json(bbbb)
# cc.save()

def islogin():
    uid_code = request.cookies.get('All_Hail_Fqs')
    if (uid_code == None) or (uid_code == ''):
        return [False, 'fqsws']
    uid = base64.b64decode(uid_code)
    uid = uid[18:]
    for user in users.objects.all():
        if (str(user['uid']) == uid):
            return [True, int(uid)]
    return [False, 'fqsws']

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
# --------------------我是分界线--------------------
@app.route('/api/login')
def login():
    phone = request.args.get('phone')
    password = request.args.get('password')
    if (phone == '' or password == ''):
        resp = make_response('信息不完整', 200)
        return resp

    user_info = users.objects(phone=phone).first()
    if (user_info == None):
        resp = make_response('wrong phone', 200)
        return resp
    password_real = user_info['password']
    password_hash = hashlib.md5(password + salt).hexdigest()
    if password_real == password_hash:
        resp = make_response('success', 200)
        resp.set_cookie('All_Hail_Fqs', base64.b64encode(salt + str(user_info['uid'])), max_age=2592000)
    else:
        resp = make_response('wrong password', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/logout')
def logout():
    resp = make_response('success', 200)
    resp.set_cookie('All_Hail_Fqs', '')
    return resp
# --------------------我是分界线--------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    text = request.json
    if (text['phone'] == '' or text['name'] == '' or text['password'] == '' or text['code'] == ''):
        resp = make_response('信息不完整', 200)
        return resp

    if (users.objects(phone=text['phone']).first() != None):
        resp = make_response('该手机号已经注册', 200)
        return resp
    info = verification.objects(phone=text['phone']).first()
    if (info == None):
        resp = make_response('未发送验证码', 200)
        return resp
    if (text['code'] != info['verify_code']):
        resp = make_response('验证码错误', 200)
        return resp
    if (int(time.time() * 1000) - info['last_verify'] > 1200000):
        resp = make_response('验证码已过期', 200)
        return resp
    sum = me_ta.objects(me_ta='auto_increase').first()['uid']
    sum = sum + 1
    me_ta.objects(me_ta='auto_increase').update_one(set__uid=sum)
    text['password'] =hashlib.md5(str(text['password']) + salt).hexdigest()
    text_save = users(uid=sum, name=text['name'], phone=text['phone'], password=text['password'], last_login=int(time.time() * 1000), login_count=1)
    text_save.save()
    resp = make_response('success', 200)
    resp.set_cookie('All_Hail_Fqs', base64.b64encode(salt + str(sum)), max_age=2592000)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/short_message_code')
def short_message_code():
    phone = request.args.get('phone')
    info = verification.objects(phone=phone).first()
    code = str(random.randint(1000,9999))
    flag = True
    if (info == None):
        info_save = verification(phone=phone, last_verify=int(time.time() * 1000), verify_code=code)
        info_save.save()
        flag = False
    if (flag and (int(time.time() * 1000) - info['last_verify'] < 60000)):
        resp = make_response('一分钟之内只能发送一次验证码！', 200)
        return resp
    print sendsms1(code, 'fuck', 'shit', int(phone))
    info['last_verify'] = int(time.time() * 1000)
    info['verify_code'] = code
    info.update()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/userinfo')
def userinfo():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('cookies error', 401)
        return resp
    uid = flag[1]

    user_info = dict(users.objects(uid=uid).first().to_mongo())
    del user_info['password']
    del user_info['_id']
    user_info_json = dumps(user_info)
    resp = make_response(user_info_json, 200)
    return resp
# --------------------我是分界线--------------------
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port= 5001)
# --------------------我是分界线--------------------