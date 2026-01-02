from django.core.management.base import BaseCommand
from app.models import  Idopont  
import datetime as dt

# A mai dátumtól kezdve kitörli a még nem foglalt időpontokat.
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        idopontok = Idopont.objects.all()
        maidatum = dt.datetime.now().date()
        for idopont in idopontok:
            if(idopont.datum >= maidatum) and not idopont.foglalt:
                idopont.delete()
                
                    