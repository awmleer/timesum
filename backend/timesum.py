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
    time_inputed=BooleanField(required=True, default=False)

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
    time = IntField(required=True, default=int(time.time() * 1000))
    text = StringField(required=True)

class activity(Document):
    aid = IntField(requird=True)
    publisher = IntField(requird=True)
    title = StringField(required=True)
    description = StringField(required=True)
    place = StringField(required=True)
    organizer = StringField(required=True)
    opening = BooleanField(required=True, default=True)
    history = BooleanField(required=True, default=False)
    participators = ListField(EmbeddedDocumentField(participators_in), required=True, default=[])
    time_collection = ListField(EmbeddedDocumentField(time_collection_in), required=True, default=[])
    expected_number = IntField(required=True)
    duration = IntField(required=True)
    published_time = IntField(required=True, default=int(time.time() * 1000))
    time_determined = IntField(required=True, default=123)
    date_range = ListField(EmbeddedDocumentField(date_in), required=True)
    comments = ListField(EmbeddedDocumentField(comments_in), required=True, default=[])
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

# ccc = activity.objects(aid=1).first()
# ccc['comments'].append(comments_in(uid=164,time=64546546,text='65464'))
# ccc.save()


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

def sendsms4(operate, code, person, mobile):
    d = {'#operate#': operate, '#code#': code}
    tpl_value = urllib.urlencode(d)
    finalstr = ''
    getdata = urllib.urlencode({'mobile':mobile,'tpl_id':14665,'tpl_value':tpl_value,'key': 'b32c625ffb38e4ad07f86bb1101548e1'})
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
    # text['phone'] = str(text['phone'])
    # text['password'] = str(text['password'])
    # text['code'] = str(text['code'])
    # text['name'] = str(text['name'])
    if (text['phone'] == '' or text['name'] == '' or text['password'] == '' or text['code'] == ''):
        resp = make_response('信息不完整', 200)
        return resp

    if (users.objects(phone=text['phone']).first() != None):
        resp = make_response('(´・ω・`)该手机号已经注册过啦', 200)
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
    text['password'] =hashlib.md5(text['password'] + salt).hexdigest()
    text_save = users(uid=sum, name=text['name'], phone=text['phone'], password=text['password'], last_login=int(time.time() * 1000), login_count=1)
    text_save.save()
    resp = make_response('success', 200)
    resp.set_cookie('All_Hail_Fqs', base64.b64encode(salt + str(sum)), max_age=2592000)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/is_signed')
def is_signed():
    phone = request.args.get('phone')
    if (users.objects(phone=phone).first() == None):
        resp = make_response('false', 200)
    else:
        resp = make_response('true', 200)
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
    operate = '注册用户'
    person = '用户'+ phone
    print sendsms4(operate.encode('utf-8'), code, person.encode('utf-8'), int(phone))
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
@app.route('/api/changepwd', methods=['POST'])
def changepwd():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('cookies error', 401)
        return resp
    uid = flag[1]

    text = request.json
    text['pwd_old'] = str(text['pwd_old'])
    text['pwd_new'] = str(text['pwd_new'])
    user_info = users.objects(uid=uid).first()
    old_password_hash = hashlib.md5(text['pwd_old'] + salt).hexdigest()
    new_password_hash = hashlib.md5(text['new_old'] + salt).hexdigest()
    if (user_info['password'] != old_password_hash):
        resp = make_response('(￢_￢)旧密码输错啦', 200)
        return resp
    user_info['password'] = new_password_hash
    user_info.save()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
# @app.route('/api/activities')
# def activities():
#     flag = islogin()
#     if (not flag[0]):
#         resp = make_response('cookies error', 401)
#         return resp
#     uid = flag[1]
# --------------------我是分界线--------------------
@app.route('/api/ac_join')
def ac_join():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    ac_info = activity.objects(aid=aid).first()
    for person in ac_info['participators']:
        if (uid == person['uid']):
            resp = make_response('(´・ω・`)您已经加入该活动了哦', 200)
            return resp
    ac_info['participators'].append(participators_in(uid=uid))
    ac_info.save()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/submit_comment')
def submit_comment():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    comment = request.args.get('comment')
    ac_info = activity.objects(aid=aid).first()
    flag = False
    for person in ac_info['participators']:
        if (uid == person['uid']):
            flag = True
            break
    if (not flag):
        resp = make_response('（¯﹃¯）您还未加入该活动呢', 200)
        return resp
    ac_info['comments'].append(comments_in(uid=uid, text=comment))
    ac_info.save()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/time_input', methods=['POST'])
def time_input():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    text = request.json
    text['aid'] = int(text['aid'])
    ac_info = activity.objects(aid=text['aid']).first()
    flag = False
    for person in ac_info['participators']:
        if (uid == person['uid']):
            flag = True
            break
    if (not flag):
        resp = make_response('（¯﹃¯）您还未加入该活动呢', 200)
        return resp
    for user_time in ac_info['time_collection']:
        if (user_time['uid'] == uid):
            user_time['data'] = text['data']
            ac_info.save()
            resp = make_response('success', 200)
            return resp
    ac_info['time_collection'].append(time_collection_in(uid=uid, data=text['data']))
    ac_info.save()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/new_ac', methods=['POST'])
def new_ac():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    text = request.json
    resp_json = json.dumps({'result': 'fail', 'message': '信息不完整'})
    if (text['title'] == '' or text['description'] == '' or text['place'] == '' or text['organizer'] == ''):
        resp = make_response(resp_json, 200)
        return resp
    if (text['expected_number'] == '' or text['duration'] == '' or text['date_range'] == []):
        resp = make_response(resp_json, 200)
        return resp

    sum = me_ta.objects(me_ta='auto_increase').first()['aid']
    sum = sum + 1
    me_ta.objects(me_ta='auto_increase').update_one(set__aid=sum)
    text_save = activity(aid=sum, publisher=uid)
    text_save['title'] = str(text['title'])
    text_save['description'] = str(text['description'])
    text_save['place'] = str(text['place'])
    text_save['organizer'] = str(text['organizer'])
    text_save['expected_number'] = int(text['expected_number'])
    text_save['duration'] = int(text['duration'])
    text_save['date_range'] = text['date_range']
    text_save.save()
    resp_json = json.dumps({'result': 'success', 'aid': sum})
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port= 5001)
# --------------------我是分界线--------------------