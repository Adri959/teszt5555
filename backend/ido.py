import datetime as dt

idopontok = []

kezdetidatum = dt.datetime.now().date()


for j in range(6):  #itt állítható, hogy hány napra (- a hétvégei napok)
    intervalday = dt.timedelta(days=j)
    idopont = dt.datetime(kezdetidatum.year,kezdetidatum.month,kezdetidatum.day,10,0)
    idopont = idopont + intervalday
    if idopont.weekday() == 5 or idopont.weekday() == 6:  #ha hétvége, ne generáljon  
        continue

    for i in range(0,10,4):   #itt állítható, hány óránként
        #print(idopont+ dt.timedelta(hours=i))
        idopontok.append(idopont + dt.timedelta(hours=i))

for i in range(len(idopontok)):
    #print(idopontok[i].time())
    continue

print(dt.datetime.now().date())
print(dt.datetime.now().date()+ dt.timedelta(days=1))


