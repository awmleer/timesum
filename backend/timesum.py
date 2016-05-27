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
app = Flask(__name__)
CORS(app)   #跨域访问
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
    time = IntField(required=True, default=int(time.time() * 1000))
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
    published_time = IntField(required=True, default=int(time.time() * 1000))
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
salt = '5aWZak2n35Wk fqsws'
ac_preview_item = ['_id', 'history', 'participators', 'time_collection', 'expected_number', 'duration', 'time_determined', 'comments']

# aaaa = dict(users.objects(uid=6).first().to_mongo())
# print aaaa
# aaa = {'phone':'65466','last_verify':312351,'verify_code': '6546'}
# bbbb = dumps(aaa)
# cc = verification.from_json(bbbb)
# cc.save()

# ccc = activity.objects(aid=1).first()
# ccc['comments'].append(comments_in(uid=164,time=64546546,text='65464'))
# ccc.save()

# anyday=datetime.datetime(2012,2,15).strftime("%w")
# print anyday


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

def week_day(year, month, day):
    weekday=datetime.datetime(int(year),int(month),int(day)).strftime("%w")
    if (weekday == '1'): return '周一'
    if (weekday == '2'): return '周二'
    if (weekday == '3'): return '周三'
    if (weekday == '4'): return '周四'
    if (weekday == '5'): return '周五'
    if (weekday == '6'): return '周六'
    if (weekday == '7'): return '周日'

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
@app.route('/api/login', methods=['POST'])
def login():
    text = request.json
    phone = str(text['phone'])
    password = str(text['password'])
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
    if (users.objects(phone=phone).first() != None):
        resp = make_response('(´・ω・`)该手机号已经注册过啦', 200)
        return resp
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
    operate = u'注册用户'
    person = u'新用户' + phone
    print sendsms4(operate.encode('utf-8'), code, person.encode('utf-8'), int(phone))
    info['last_verify'] = int(time.time() * 1000)
    info['verify_code'] = code
    info.save()
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
        resp = make_response('', 200)
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
@app.route('/api/activities')
def activities():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    resp_json = {'ac_published': [], 'ac_participated': [], 'ac_published_history': [], 'ac_participated_history': []}
    for one_activity in activity.objects(publisher=uid):
        one_ac = dict(one_activity.to_mongo())
        one_ac['time_determined'][0].update({'day_in_week': week_day(one_ac['time_determined'][0]['year'], one_ac['time_determined'][0]['month'], one_ac['time_determined'][0]['day'])})
        one_ac['time_determined'][1].update({'day_in_week': week_day(one_ac['time_determined'][1]['year'], one_ac['time_determined'][1]['month'], one_ac['time_determined'][1]['day'])})
        if (one_ac['history'] == False):
            temp = {}
            temp.update({'aid': one_ac['aid'], 'title': one_ac['title'], 'opening': one_ac['opening'], 'participators': one_ac['participators']})
            temp.update({'expected_number': one_ac['expected_number'], 'published_time': one_ac['published_time'], 'time_determined': one_ac['time_determined']})
            resp_json['ac_published'].append(temp)
        else:
            temp = {}
            temp.update({'aid': one_ac['aid'], 'title': one_ac['title'], 'time_determined': one_ac['time_determined']})
            resp_json['ac_published_history'].append(temp)
    for one_activity in activity.objects(participators__all=[participators_in(uid=uid, time_inputed=True)]):
        one_ac = dict(one_activity.to_mongo())
        one_ac['time_determined'][0].update({'day_in_week': week_day(one_ac['time_determined'][0]['year'], one_ac['time_determined'][0]['month'], one_ac['time_determined'][0]['day'])})
        one_ac['time_determined'][1].update({'day_in_week': week_day(one_ac['time_determined'][1]['year'], one_ac['time_determined'][1]['month'], one_ac['time_determined'][1]['day'])})
        if (one_ac['history'] == False):
            temp = {}
            temp.update({'aid': one_ac['aid'], 'title': one_ac['title'], 'opening': one_ac['opening'], 'participators': one_ac['participators']})
            temp.update({'expected_number': one_ac['expected_number'], 'published_time': one_ac['published_time'], 'time_determined': one_ac['time_determined']})
            resp_json['ac_participated'].append(temp)
        else:
            temp = {}
            temp.update({'aid': one_ac['aid'], 'title': one_ac['title'], 'time_determined': one_ac['time_determined']})
            resp_json['ac_participated_history'].append(temp)
    for one_activity in activity.objects(participators__all=[participators_in(uid=uid, time_inputed=False)]):
        one_ac = dict(one_activity.to_mongo())
        one_ac['time_determined'][0].update({'day_in_week': week_day(one_ac['time_determined'][0]['year'], one_ac['time_determined'][0]['month'], one_ac['time_determined'][0]['day'])})
        one_ac['time_determined'][1].update({'day_in_week': week_day(one_ac['time_determined'][1]['year'], one_ac['time_determined'][1]['month'], one_ac['time_determined'][1]['day'])})
        if (one_ac['history'] == False):
            temp = {}
            temp.update({'aid': one_ac['aid'], 'title': one_ac['title'], 'opening': one_ac['opening'], 'participators': one_ac['participators']})
            temp.update({'expected_number': one_ac['expected_number'], 'published_time': one_ac['published_time'], 'time_determined': one_ac['time_determined']})
            resp_json['ac_participated'].append(temp)
        else:
            temp = {}
            temp.update({'aid': one_ac['aid'], 'title': one_ac['title'], 'time_determined': one_ac['time_determined']})
            resp_json['ac_participated_history'].append(temp)
    resp_json = dumps(resp_json)
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/ac_detail')
def ac_detail():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    ac_info = dict(activity.objects(aid=aid).first().to_mongo())
    resp_json = {'me': {}}
    flag = False
    for person in ac_info['participators']:
        if (uid == person['uid']):
            flag = True
            resp_json['me'].update({'relation': 'participated', 'time_inputed': person['time_inputed']})
            break
    if (uid == ac_info['publisher']):
        resp_json['me']['relation'] = 'published'
    if (not flag):
        resp = make_response('（¯﹃¯）您还未加入该活动呢', 200)
        return resp

    ac_info['publisher'] = {'uid': ac_info['publisher'], 'name': users.objects(uid=ac_info['publisher']).first()['name']}
    ac_info['date_range'][0].update({'day_in_week': week_day(ac_info['date_range'][0]['year'], ac_info['date_range'][0]['month'], ac_info['date_range'][0]['day'])})
    ac_info['date_range'][1].update({'day_in_week': week_day(ac_info['date_range'][1]['year'], ac_info['date_range'][1]['month'], ac_info['date_range'][1]['day'])})
    for person in ac_info['participators']:
        person.update({'name': users.objects(uid=person['uid']).first()['name']})
    del ac_info['_id']
    del ac_info['time_collection']
    resp_json.update(ac_info)
    resp_json = dumps(resp_json)
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/ac_preview')
def ac_preview():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    ac_info = dict(activity.objects(aid=aid).first().to_mongo())
    ac_info['publisher'] = {'uid': ac_info['publisher'], 'name': users.objects(uid=ac_info['publisher']).first()['name']}
    ac_info['date_range'][0].update({'day_in_week': week_day(ac_info['date_range'][0]['year'], ac_info['date_range'][0]['month'], ac_info['date_range'][0]['day'])})
    ac_info['date_range'][1].update({'day_in_week': week_day(ac_info['date_range'][1]['year'], ac_info['date_range'][1]['month'], ac_info['date_range'][1]['day'])})
    for item in ac_preview_item:
        del ac_info[item]
    resp_json = dumps(ac_info)
    resp = make_response(resp_json, 200)
    return resp
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
            if_modify = True
            if (not person['time_inputed']):
                person['time_inputed'] = True
                if_modify = False
            break
    if (not flag):
        resp = make_response('（¯﹃¯）您还未加入该活动呢', 200)
        return resp

    if (if_modify):
        location = -1
        for user_time in ac_info['time_collection']:
            location += 1
            if (user_time['uid'] == uid):
                time_collect_in = dumps({'uid': uid, 'data': text['data']})
                ac_info['time_collection'][location] = time_collection_in.from_json(time_collect_in)
                ac_info.save()
                resp = make_response('success', 200)
                return resp
    time_collect_in = dumps({'uid': uid, 'data': text['data']})
    ac_info['time_collection'].append(time_collection_in.from_json(time_collect_in))
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
    if (text['expected_number'] == '' or text['duration'] == '' or text['date_range'] == [] or text['title'] == ''):
        resp = make_response(resp_json, 200)
        return resp

    sum = me_ta.objects(me_ta='auto_increase').first()['aid']
    sum = sum + 1
    me_ta.objects(me_ta='auto_increase').update_one(set__aid=sum)
    text.update({'aid': sum, 'publisher': uid, 'participators': [{'uid': uid, 'time_inputed': False}]})
    text_save = activity.from_json(dumps(text))
    text_save.save()
    resp_json = json.dumps({'result': 'success', 'aid': sum})
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port= 5001)
# --------------------我是分界线--------------------