from django.core.management.base import BaseCommand
from app.models import Szolgaltatas, Idopont, Foglalas  
import datetime as dt

# Időpontokat generál. (Alapból 10 napra előre, 10 és 20 óra közt, 3 óránként)

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        Idopont.objects.get_or_create(datum="2025-12-31", ido="14:00:00")

        kezdetidatum = dt.datetime.now().date()


        for j in range(10):  #itt állítható, hogy hány napra (- a hétvégei napok)
            intervalday = dt.timedelta(days=j)
            idopont = dt.datetime(kezdetidatum.year,kezdetidatum.month,kezdetidatum.day,10,0)
            idopont = idopont + intervalday
            if idopont.weekday() == 5 or idopont.weekday() == 6:  #ha hétvége, ne generáljon  
                continue

            for i in range(0,10,3):   #itt állítható, hány óránként
                    keszidopont = idopont + dt.timedelta(hours=i)
                    Idopont.objects.get_or_create(datum=keszidopont.date(), ido=keszidopont.time())

                #print(idopont+ dt.timedelta(hours=i))
                #idopontok.append(idopont + dt.timedelta(hours=i))

        # for i in range(len(idopontok)):
        #     print(idopontok[i])


            