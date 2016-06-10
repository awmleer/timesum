#coding uft-8
from wo_jiu_wen_ni_pa_bu_pa import *
for i in activity.objects:
    pp=0
    for j in i.date_range:
        if time.mktime(datetime.datetime(int(j['year']), int(j['month']),int(j['day']), 0, 0, 0).timetuple())+86400>time.time():
            pp=1
            break
    if pp==0:
        i.history=True
        i.save()
