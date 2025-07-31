import datetime as dt

idopontok = []

kezdetidatum = dt.datetime.now().date()


for j in range(6):
    intervalday = dt.timedelta(days=j)
    idopont = dt.datetime(kezdetidatum.year,kezdetidatum.month,kezdetidatum.day,10,0)
    idopont = idopont + intervalday
    if idopont.weekday() == 5 or idopont.weekday() == 6:  #ha hétvége, ne generáljon       
        continue

    for i in range(11):
        print(idopont+ dt.timedelta(hours=i))


for i in range(len(idopontok)):
    print(idopontok[i])

