from datetime import date
import datetime

def Overduedays(a, b, c):
    dt = date(a, b, c)
    now = datetime.datetime.now()
    nowdt = now.date()
    print(nowdt)
    print(dt)
    if dt>nowdt:
        return 0
    else:
        return (nowdt-dt).days

print(Overduedays(2021, 11, 1))
