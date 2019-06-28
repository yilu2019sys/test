import time
import datetime


def caltime(date1, date2):
    date1=time.strptime(date1,'%Y%m%d')
    date2=time.strptime(date2,'%Y%m%d')
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
#
    return((date1-date2).days)


if __name__ == 'main':
    caltime(a,b)
    print(caltime(a,b))


## method 2
#aa=['20180501']
#bb=['20180701']
#aa=int(time.mktime(time.strptime(aa[0],'%Y%m%d')))
#bb=int(time.mktime(time.strptime(bb[0],'%Y%m%d')))
#t= datetime.datetime.fromtimestamp(aa)- datetime.datetime.fromtimestamp(bb)
#d=t.days
    