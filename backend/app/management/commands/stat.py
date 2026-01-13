from django.core.management.base import BaseCommand  
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # plt.plot([1,2,3],['egy','kettő','három'])
        # plt.show()
        #print(os.getcwd())
        os.chdir("./Excelek")
        excelekmappa = os.getcwd()
        excelek = os.listdir()
        if not excelek:
            print("Üres az excelek mappa")
            return
        #print(excelek)
        y=[]
        x=[]
        for excel in excelek:
            #print(f"{excelekmappa}\{excel}")
             nyitott = pd.read_excel(f"{excelekmappa}\\{excel}")
             df = pd.DataFrame(nyitott)
             if df["Ár"].isna().all():
                 y.append(0)
             else:
                 y.append(int(df.get("Ár").cumsum().max()))
             x.append(f"{excel.split('.')[0]}")
        print(x)
        print(y)
        plt.plot(x,y,"-*")
        plt.grid()
        plt.show()        

                
            
