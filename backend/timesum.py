# coding:utf-8

from wo_jiu_wen_ni_pa_bu_pa import *
# --------------------我是分界线--------------------
app = Flask(__name__)
CORS(app)   #跨域访问
# --------------------我是分界线--------------------
salt = '5aWZak2n35Wk fqsws'
ac_preview_item = ['_id', 'history', 'participators', 'time_collection', 'time_determined', 'comments']
timeblocks_default = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
edit_ac_item = ['title', 'organizer', 'place', 'description', 'expected_number', 'duration']

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
# --------------------我是分界线--------------------
class suggest():
    start=0
    end=0
    list0=[]
    list1=[]
    list2=[]
    list0_name=[]
    list1_name=[]
    list2_name=[]
#添加可行的推荐时间点
def res(k,t):
    global answer, s,sjc1, time_coll,aid
    re=suggest()
    re.start=sjc1[k]+t*600
    re.end=re.start+duration*600
    for i in range(num):
        if s[i][k][t]==2:
            re.list2.append(time_coll[i]['uid'])
        elif s[i][k][t]==1:
            re.list1.append(time_coll[i]['uid'])
    answer.append(re)
    return
def del_repeat():
    global answer
    p=suggest()
    for i in range(len(answer)):
        for j in range(len(answer)):
            if answer[i].start>answer[j].start:
                p=answer[i]
                answer[i]=answer[j]
                answer[j]=p
    i=0
    while i<len(answer)-1:
        if answer[i].start==answer[i+1].start:
            del answer[i]
        else: i+=1
    return
#s存储时间状态，当前活动持续时间块长度为l。返回成块时间状态
def foo(s,l):
    s2=''
    for j in range(0,len(s)-l+1):
        flag=2
        for t in range(j,j+l):
            if s[t]=='0':
                flag=0
                break
            elif s[t]=='1':
                flag=1
        s2=s2+chr(flag+48)
    return s2
#能来和不能来都算上，总人数最多
def plan_1():
    global sum,num
    max=0
    ans = [[0 for col in len(s[0][row])] for row in range(sum)]
    for k in range(sum):
        for i in range(len(s[0][k])):
            for j in range(num):
                if s[j][k][i]!='0':
                    ans[k][i]+=1
            if ans[k][i]>max:
                max=ans[k][i]
    for k in range(sum):
        for i in range(len(s[0][k])):
            if ans[k][i]==max:
                res(k,i)
    return
#能来的人最多情况下，可能来的人最多
def plan_2():
    global sum,num
    max=0
    max2=0
    ans = [[0 for col in len(s[0][row])] for row in range(sum)]
    for k in range(sum):
        for i in range(len(s[0][k])):
            for j in range(num):
                if s[j][k][i] == '2':
                    ans[k][i] += 1
            if ans[k][i] > max:
                max = ans[k][i]
    for k in range(sum):
        for i in range(len(s[0][k])):
            if ans[k][i]==max:
                pp = 0
                for j in range(num):
                    if s[j][k][i] == '1': pp+=1
                if pp > max2:
                    max2=pp
    for k in range(sum):
        for i in range(len(s[0][k])):
            if ans[k][i] == max:
                pp = 0
                for j in range(num):
                    if s[j][k][i] == '1': pp += 1
                if pp == max2:
                    res(k,i)
    return
#能来的人算1，可能来的人算0.5
def plan_3():
    global num,sum
    max=0
    ans = [[0 for col in len(s[0][row])] for row in range(sum)]
    for k in range(sum):
        for i in range(len(s[0][k])):
            for j in range(num):
                ans[k][i]+=float(s[j][k][i])/2
            if ans[k][i]>max:
                max=ans[k][i]
    for k in range(sum):
        for i in range(len(s[0][k])):
            if ans[k][i] == max:
                res(k,i)
    return
# --------------------我是分界线--------------------
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

def date_to_day(year, month, day):
    day1 = datetime.datetime(2015, 12, 31)
    day2 = datetime.datetime(year, month, day)
    return (day2 - day1).days

# def day_to_date(day):
#     day1 = datetime.datetime(2015, 12, 31)
#     return (day1 + datetime.timedelta(days=day)).strftime('%Y%m%d')

def week_day(year, month, day):
    weekday = datetime.datetime(int(year), int(month), int(day)).strftime("%w")
    if (weekday == '1'): return '周一'
    if (weekday == '2'): return '周二'
    if (weekday == '3'): return '周三'
    if (weekday == '4'): return '周四'
    if (weekday == '5'): return '周五'
    if (weekday == '6'): return '周六'
    if (weekday == '0'): return '周日'

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
@app.route('/api/change_name')
def change_name():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('cookies error', 401)
        return resp
    uid = flag[1]

    name = request.args.get('name')
    if (name == '' or name == None):
        resp = make_response('(｡・`ω´･)所以说姓名怎么能是空呢？', 200)
        return resp
    user_info = users.objects(uid=uid).first()
    user_info['name'] = name
    user_info.save()
    resp = make_response('success', 200)
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
        info = verification.objects(phone=phone).first()
        flag = False
    if (flag and (int(time.time() * 1000) - info['last_verify'] < 120000)):
        resp = make_response('两分钟之内只能发送一次验证码！', 200)
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
    new_password_hash = hashlib.md5(text['pwd_new'] + salt).hexdigest()
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
        if (one_ac['time_determined'] != []):
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
        if (one_ac['time_determined'] != []):
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
        if (one_ac['time_determined'] != []):
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
    for i in ac_info['date_range']:
        i.update({'day_in_week': week_day(i['year'], i['month'], i['day'])})
    for person in ac_info['participators']:
        person.update({'name': users.objects(uid=person['uid']).first()['name']})
    for person in ac_info['comments']:
        person.update({'name': users.objects(uid=person['uid']).first()['name']})
    if (ac_info['time_determined'] != []):
        day_start = date_to_day(int(ac_info['time_determined'][0]['year']), int(ac_info['time_determined'][0]['month']), int(ac_info['time_determined'][0]['day']))
        time_start = int(ac_info['time_determined'][0]['time'])
        time_end = int(ac_info['time_determined'][1]['time'])
        day_end = date_to_day(int(ac_info['time_determined'][1]['year']), int(ac_info['time_determined'][1]['month']), int(ac_info['time_determined'][1]['day']))
        if (time_end == 0):
            day_end -= 1
            time_end = 144
        if (day_start == day_end):
            for person in ac_info['participators']:
                if (person['time_inputed'] == False):
                    person.update({'attendable': 0})
                    continue
                for time in ac_info['time_collection']:
                    if (time['uid'] == person['uid']):
                        flag = 2
                        for days in time['data']:
                            if (flag == 0): break
                            day = date_to_day(int(days['date']['year']), int(days['date']['month']), int(days['date']['day']))
                            if (day == day_start):
                                for i in range(time_start, time_end):
                                    if (days['timeblocks'][i] == '0'):
                                        flag = 0
                                        break
                                    if (days['timeblocks'][i] == '1'):
                                        flag = 1
                        person.update({'attendable': flag})
                        break
        else:
            for person in ac_info['participators']:
                if (person['time_inputed'] == False):
                    person.update({'attendable': 0})
                    continue
                for time in ac_info['time_collection']:
                    if (time['uid'] == person['uid']):
                        flag = 2
                        for days in time['data']:
                            if (flag == 0): break
                            day = date_to_day(int(days['date']['year']), int(days['date']['month']), int(days['date']['day']))
                            if (day == day_start):
                                for i in range(time_start, 144):
                                    if (days['timeblocks'][i] == '0'):
                                        flag = 0
                                        break
                                    if (days['timeblocks'][i] == '1'):
                                        flag = 1
                            if (day == day_end):
                                for i in range(0, time_end):
                                    if (days['timeblocks'][i] == '0'):
                                        flag = 0
                                        break
                                    if (days['timeblocks'][i] == '1'):
                                        flag = 1
                            if (day>day_start and day<day_end):
                                for i in range(0, 144):
                                    if (days['timeblocks'][i] == '0'):
                                        flag = 0
                                        break
                                    if (days['timeblocks'][i] == '1'):
                                        flag = 1
                        person.update({'attendable': flag})
                        break
    del ac_info['_id']
    del ac_info['time_collection']
    resp_json.update(ac_info)
    resp_json = dumps(resp_json)
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/time_collection')
def time_collection():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    ac_info = dict(activity.objects(aid=aid).first().to_mongo())
    flag = False
    for person in ac_info['participators']:
        if (uid == person['uid']):
            flag = True
            break
    if (not flag):
        resp = make_response('（¯﹃¯）您还未加入该活动呢', 200)
        return resp

    for person in ac_info['time_collection']:
        person.update({'name': users.objects(uid=person['uid']).first()['name']})
        for i in person['data']:
            i['date'].update({'day_in_week': week_day(i['date']['year'], i['date']['month'], i['date']['day'])})
    resp_json = dumps({'aid': aid, 'time_collection': ac_info['time_collection']})
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/ac_preview')
def ac_preview():
    aid = int(request.args.get('aid'))
    ac_info = dict(activity.objects(aid=aid).first().to_mongo())
    ac_info['publisher'] = {'uid': ac_info['publisher'], 'name': users.objects(uid=ac_info['publisher']).first()['name']}
    for i in ac_info['date_range']:
        i.update({'day_in_week': week_day(i['year'], i['month'], i['day'])})
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
    ac_info['comments'].append(comments_in(uid=uid, time=int(time.time() * 1000), text=comment))
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
@app.route('/api/timeblocks')
def timeblocks():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    ac_info = dict(activity.objects(aid=aid).first().to_mongo())
    flag = False
    for person in ac_info['participators']:
        if (uid == person['uid']):
            flag = True
            if_inputed = person['time_inputed']
            break
    if (not flag):
        resp = make_response('（¯﹃¯）您还未加入该活动呢', 200)
        return resp

    ac_info['publisher'] = {'uid': ac_info['publisher'], 'name': users.objects(uid=ac_info['publisher']).first()['name']}
    resp_json = {'aid': aid, 'title': ac_info['title'], 'publisher': ac_info['publisher'], 'organizer': ac_info['organizer'], 'place': ac_info['place'], 'opening': ac_info['opening']}
    if (if_inputed):
        for person in ac_info['time_collection']:
            if (uid == person['uid']):
                temp = {'date_range': person['data'], 'time_inputed': True}
                for i in temp['date_range']:
                    i['date'].update({'day_in_week': week_day(i['date']['year'], i['date']['month'], i['date']['day'])})
                break
    else:
        temp = {'date_range': [], 'time_inputed': False}
        for i in ac_info['date_range']:
            i.update({'day_in_week': week_day(i['year'], i['month'], i['day'])})
            temp['date_range'].append({'date': i, 'timeblocks': timeblocks_default})
    resp_json.update(temp)
    resp_json = dumps(resp_json)
    resp = make_response(resp_json, 200)
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
    text.update({'aid': sum, 'publisher': uid, 'participators': [{'uid': uid, 'time_inputed': False}], 'published_time': int(time.time() * 1000)})
    text_save = activity.from_json(dumps(text))
    text_save.save()
    resp_json = json.dumps({'result': 'success', 'aid': sum})
    resp = make_response(resp_json, 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/edit_ac', methods=['POST'])
def edit_ac():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    text = request.json
    text['aid'] = int(text['aid'])
    ac_info = activity.objects(aid=text['aid']).first()
    if (ac_info['publisher'] != uid):
        resp = make_response('您没有权限', 200)
        return resp
    if (text['expected_number'] == '' or text['duration'] == '' or text['title'] == ''):
        resp = make_response('信息不完整', 200)
        return resp

    for item in edit_ac_item:
        ac_info[item] = text[item]
    ac_info.save()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/delete_ac')
def delete_ac():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    aid = int(request.args.get('aid'))
    ac_info = dict(activity.objects(aid=aid).first().to_mongo())
    if (ac_info['publisher'] != uid):
        resp = make_response('您没有权限', 200)
        return resp

    del ac_info['_id']
    ac_deleted_save = ac_deleted.from_json(dumps(ac_info))
    ac_deleted_save.save()
    ac_info = activity.objects(aid=aid).first()
    ac_info.delete()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/determine_time', methods=['POST'])
def determine_time():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]

    text = request.json
    text['aid'] = int(text['aid'])
    ac_info = activity.objects(aid=text['aid']).first()
    if (ac_info['publisher'] != uid):
        resp = make_response('您没有权限', 200)
        return resp

    temp = []
    for time_form in text['time_determined']:
        temp.append(time_format.from_json(dumps(time_form)))
    ac_info['time_determined'] = temp
    ac_info.save()
    resp = make_response('success', 200)
    return resp
# --------------------我是分界线--------------------
@app.route('/api/time_recommend')
def time_recommend():
    flag = islogin()
    if (not flag[0]):
        resp = make_response('', 200)
        return resp
    uid = flag[1]
    aid = int(request.args.get('aid'))
    acinfo = dict(activity.objects(aid=aid).first().to_mongo())
    if (acinfo['publisher'] != uid):
        resp = make_response('您没有权限', 200)
        return resp
# 添加可行的推荐时间点
    def res(k, t):
        re = suggest()
        re.list0 = []
        re.list1 = []
        re.list2 = []
        re.list0_name = []
        re.list1_name = []
        re.list2_name = []
        re.start = sjc1[k] + t * 600
        re.end = re.start + duration * 600
        for i in range(num):
            if s[i][k][t] == '2':
                re.list2.append(time_coll[i]['uid'])
            elif s[i][k][t] == '1':
                re.list1.append(time_coll[i]['uid'])
            elif s[i][k][t] == '0':
                re.list0.append(time_coll[i]['uid'])
        answer.append(re)
        return
    def del_repeat():
        for i in range(len(answer)):
            for j in range(len(answer)):
                if answer[i].start > answer[j].start:
                    p = answer[i]
                    answer[i] = answer[j]
                    answer[j] = p
        i = 0
        while i < len(answer) - 1:
            if answer[i].start == answer[i + 1].start:
                del answer[i]
            else:
                i += 1
        return

    # s存储时间状态，当前活动持续时间块长度为l。返回成块时间状态
    def foo(s, l):
        s2 = ''
        for j in range(len(s) - l+1):
            flag = 2
            for t in range(j, j + l):
                if s[t] == '0':
                    flag = 0
                    break
                elif s[t] == '1':
                    flag = 1
            s2 = s2 + chr(flag + 48)
        return s2
    # 能来和不能来都算上，总人数最多
    def plan_1():
        max = 0
        ans = [[0 for col in range(len(s[0][row]))] for row in range(sum)]
        for k in range(sum):
            for i in range(len(s[0][k])):
                for j in range(num):
                    if s[j][k][i] != '0':
                        ans[k][i] += 1
                if ans[k][i] > max:
                    max = ans[k][i]
        for k in range(sum):
            for i in range(len(s[0][k])):
                if ans[k][i] == max:
                    res(k, i)
        return
    # 能来的人最多情况下，可能来的人最多
    def plan_2():
        max = 0
        max2 = 0
        ans = [[0 for col in range(len(s[0][row]))] for row in range(sum)]
        for k in range(sum):
            for i in range(len(s[0][k])):
                for j in range(num):
                    if s[j][k][i] == '2':
                        ans[k][i] += 1
                if ans[k][i] > max:
                    max = ans[k][i]
        for k in range(sum):
            for i in range(len(s[0][k])):
                if ans[k][i] == max:
                    pp = 0
                    for j in range(num):
                        if s[j][k][i] == '1': pp += 1
                    if pp > max2:
                        max2 = pp
        for k in range(sum):
            for i in range(len(s[0][k])):
                if ans[k][i] == max:
                    pp = 0
                    for j in range(num):
                        if s[j][k][i] == '1': pp += 1
                    if pp == max2:
                        res(k, i)
        return

    # 能来的人算1，可能来的人算0.5
    def plan_3():
        max = 0
        ans = [[0 for col in range(len(s[0][row]))] for row in range(sum)]
        for k in range(sum):
            for i in range(len(s[0][k])):
                for j in range(num):
                    ans[k][i] += float(s[j][k][i]) / 2
                if ans[k][i] > max:
                    max = ans[k][i]
        for k in range(sum):
            for i in range(len(s[0][k])):
                if ans[k][i] == max:
                    res(k, i)
        return
    acinfo = dict(activity.objects(aid=aid).first().to_mongo())
    date_range = acinfo['date_range']
    time_coll = acinfo['time_collection']
    duration = acinfo['duration']
    sum = 0
    num = len(time_coll)
    answer=[]
    s = [['' for col in range(len(date_range))] for row in range(num)]
    sjc1 = []
    sjc2 = []
    sjc1.append(time.mktime(datetime.datetime(int(date_range[0]['year']), int(date_range[0]['month']), int(date_range[0]['day']), 0, 0,0).timetuple()))
    pp = [['' for col in range(len(date_range))] for row in range(num)]
    for i in range(len(date_range)):
        if i != 0:
            if time.mktime(datetime.datetime(int(date_range[i]['year']), int(date_range[i]['month']),int(date_range[i]['day']), 0, 0, 0).timetuple()) - time.mktime(datetime.datetime(int(date_range[i - 1]['year']), int(date_range[i - 1]['month']),int(date_range[i - 1]['day']), 0, 0, 0).timetuple()) != 86400:
                sjc2.append(time.mktime(datetime.datetime(int(date_range[i - 1]['year']), int(date_range[i - 1]['month']),int(date_range[i - 1]['day']), 0, 0, 0).timetuple()) + 86400)
                sum += 1
                sjc1.append(time.mktime(datetime.datetime(int(date_range[i]['year']), int(date_range[i]['month']),int(date_range[i]['day']), 0, 0, 0).timetuple()))
        for j in range(num):
            pp[j][sum]=pp[j][sum]+time_coll[j]['data'][i]['timeblocks']
    for j in range(num):
        s[j][sum] = foo(pp[j][sum], duration)
    i = len(date_range) - 1
    sjc2.append(time.mktime(datetime.datetime(int(date_range[i]['year']), int(date_range[i]['month']), int(date_range[i]['day']), 0, 0,0).timetuple()) + 86400)
    sum += 1
    plan_1()
    plan_2()
    plan_3()
    del_repeat()
    resp_json = []
    for i in answer:
        resp_json.append({'start': i.start, 'end': i.end, 'list2': i.list2, 'list1': i.list1})
    resp_json = dumps(resp_json)
    resp = make_response(resp_json, 200)
    return resp_json
# --------------------我是分界线--------------------
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port= 5001)
# --------------------我是分界线--------------------