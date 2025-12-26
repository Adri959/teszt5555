from django.core.management.base import BaseCommand
from app.models import Szolgaltatas, Idopont, Foglalas  
import datetime
import pandas as pd
import os

#Lementi a múltbéli foglalásokat excelbe, majd törli azokat.

# Windows feladatütemezőből futtatni majd .bat fájlal minden nap.
# Az utolsó időpont után ajánlott lefuttatni.

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        maidatum = datetime.date.today()
        tegnapidatum = maidatum - datetime.timedelta(days=1)

        # Kitörli az időpontokat amik régebbiek a mai dátumnál
        idopontok = Idopont.objects.all()
        foglalasok = Foglalas.objects.all()

        # Kimenteni excelbe, hogy ki és mikor ment mire, aztán kitörli
        data = {
            "Email":[],
            "Dátum":[],
            "Időpont":[],
            "Szolgáltatás":[],
            "Ár":[],
        }
        
        for foglalas in foglalasok:
            if foglalas.idopont.datum < maidatum:
                data["Email"].append(foglalas.user.email)
                data["Dátum"].append(foglalas.idopont.datum)
                data["Időpont"].append(foglalas.idopont.ido)
                data["Szolgáltatás"].append(foglalas.szolgaltatas.nev)
                data["Ár"].append(foglalas.szolgaltatas.ar)

        df = pd.DataFrame(data)
        print(df)
        #print(os.getcwd())
        df.to_excel(f"{os.getcwd()}\excelek\{tegnapidatum}.xlsx",index=False)

        for idopont in idopontok:
            if(idopont.datum < maidatum):
                idopont.delete()
