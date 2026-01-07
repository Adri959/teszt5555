from django.core.management.base import BaseCommand
from app.models import Szolgaltatas, Idopont, Foglalas  
import datetime as dt

# Időpontokat generál. (Alapból 10 napra előre, 10 és 20 óra közt, 3 óránként. Állítható a --napok és --lepeskoz opciókkal)

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
        '--napok',
        type=int,
        default=10,
        help='Hány napra generáljon időpontot'
    )
        parser.add_argument(
        '--lepeskoz',
        type=int,
        default=3,
        help='Hány óránként generáljon időpontot'
    )
        parser.add_argument(
            '--kezdet',
            type=str,
            default=None,
            help='Kezdő dátum (YYYY-MM-DD)'
    )
    def handle(self, *args, **options):
        napok_szama = options['napok']
        oras_lepes = options['lepeskoz']
        kezdet_str = options.get('kezdet')

        if kezdet_str:
            # pl. --kezdet 2025-02-01
            kezdetidatum = dt.datetime.strptime(kezdet_str, "%Y-%m-%d").date()
        else:
            # ha nincs megadva, marad az aktuális dátum
            kezdetidatum = dt.datetime.now().date()



        generaltnapok=0
        j=0
        while generaltnapok != napok_szama:
            
            intervalday = dt.timedelta(days=j)
            j=j+1
            idopont = dt.datetime(kezdetidatum.year,kezdetidatum.month,kezdetidatum.day,10,0)
            idopont = idopont + intervalday
            if idopont.weekday() == 5 or idopont.weekday() == 6:  #ha hétvége, ne generáljon  
                continue
                

            for i in range(0,10,oras_lepes):   #itt állítható, hány óránként
                    keszidopont = idopont + dt.timedelta(hours=i)
                    Idopont.objects.get_or_create(datum=keszidopont.date(), ido=keszidopont.time())

            generaltnapok +=1
                #print(idopont+ dt.timedelta(hours=i))
                #idopontok.append(idopont + dt.timedelta(hours=i))

        # for i in range(len(idopontok)):
        #     print(idopontok[i])


            