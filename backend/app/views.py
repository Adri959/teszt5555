from django.shortcuts import render,redirect
from .models import Szolgaltatas, Idopont, Foglalas
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import IdopontSerializer

import re
import datetime
from django.db.models import Q

# Create your views here.

#######API#######
@api_view(["GET"])
def SzabadIdopontokApi(request):
    szabadidopontok = Idopont.objects.filter(foglalt=False)
    serializer = IdopontSerializer(szabadidopontok, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#################
def index(request):
    return render(request, "index.html")

@login_required
def foglalas(request):

    most = datetime.datetime.now()
    ketoramulva = most + datetime.timedelta(hours=2)
    mai_datum = most.date()

    szolgatatasok = Szolgaltatas.objects.all()
    idopontok = Idopont.objects.filter(
    foglalt=False
    ).filter(
        Q(datum=mai_datum, ido__gt=ketoramulva.time())  # ma, ido nagyobb mint most+2 óra
        | # vagy
        Q(datum__gt=mai_datum)  # minden olyan időpont, ami holnap vagy később van
    ).order_by('datum', 'ido')
    
    context= {
        'szolgaltatasok' : szolgatatasok,
        'idopontok' : idopontok,
    }

    return render(request,'foglalas.html',context=context)

def foglal(request):
    if request.method=='POST':
        
        szolgaltatasnev = request.POST.get('szolgaltatas')        
        idopont = request.POST.get('idopont')
        tapasztalat = request.POST.get('tapasztalat')
        most = datetime.datetime.now()
        ketoramulva = most + datetime.timedelta(hours=2)

        parts = idopont.split()
        datum, ido = parts[:2]
        idopont = Idopont.objects.get(datum=datum, ido=ido, foglalt=False)

        #print(datum)
        #print(ido)

        if idopont.datum == datetime.datetime.now().date():
            idopont_datetime = datetime.datetime.combine(idopont.datum, idopont.ido)
            if idopont_datetime < ketoramulva:
                uzenet="Sikertelen foglalás! Az időpont legalább 2 órával későbbi kell legyen!"
                context={
                    'uzenet': uzenet,
                }
                return render(request,'foglalas.html',context=context)

        userobj = User.objects.get(username=request.user.username)

        Szolgaltatasobj = Szolgaltatas.objects.get(nev=szolgaltatasnev)

        idopont.foglalt = True
        idopont.save()
    
        foglalas = Foglalas(idopont=idopont, szolgaltatas=Szolgaltatasobj, user=userobj, tapasztalat=tapasztalat)
        foglalas.save()
        
    return redirect('/app/sikeresfoglalas')

def regisztracio(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.error(request, "A felhasználónév már foglalt")
            return redirect('/app/regisztracio')
        
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Az email cím már foglalt")
            return redirect('/app/regisztracio')

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, "A jelszavak nem egyeznek!")
            return redirect('/app/regisztracio')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
            return redirect('/app/regisztracio')
        
        newuser = User.objects.create_user(username=username, email=email, password=password)
        newuser.save()
        return redirect('/app/foglalas')


    return render(request, 'regisztracio.html')

def belepes(request):
    if request.method =="POST":
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == "" or password == "":
            messages.error(request, "Hibás bejelentkezési adatok")
            return redirect('/app/belepes')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None
            messages.error(request, "Hibás bejelentkezési adatok")
            return redirect('/app/belepes')
        
        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/app/foglalas')
        else:
            messages.error(request, "Hibás bejelentkezési adatok")


    return render(request, 'belepes.html')

def sikeresreg(request):
    return render(request, 'sikeresreg.html')

def kilepes(request):
    logout(request)
    return redirect('/app')

@login_required
def profilepage(request):
    foglalasok = Foglalas.objects.filter(user=request.user.id)
    context= {'foglalasok':foglalasok}
    return render(request,'profilepage.html',context)

def foglalaslemondas(request):
    if request.method == 'POST':
        foglalasid = request.POST.get("foglalasid")
        torlendo = Foglalas.objects.get(id=foglalasid)
        torlendo.idopont.foglalt = False
        torlendo.idopont.save()
        torlendo.delete()
    return redirect('/app/profilepage')

def foglalaslemondasAdmin(request):
    if request.user.is_staff:
        if request.method == 'POST':
            foglalasid = request.POST.get("foglalasid")
            torlendo = Foglalas.objects.get(id=foglalasid)
            torlendo.idopont.foglalt = False
            torlendo.idopont.save()
            torlendo.delete()
        return redirect('/app/staffpage')
    else:
        return redirect('/')

def foglalastorlesAdmin(request):
    if request.user.is_staff:
        if request.method == 'POST':
            foglalasid = request.POST.get("foglalasid")
            torlendo = Foglalas.objects.get(id=foglalasid)
            torlendo.idopont.delete()
            torlendo.delete()
        return redirect('/app/staffpage')
    else:
        return redirect('/')
    
def idoponttorlesAdmin(request):
    if request.user.is_staff:
        if request.method == 'POST':
            idopontid = request.POST.get("idopontid")
            idopont = Idopont.objects.get(id=idopontid)
            idopont.delete()
        return redirect('/app/staffpage2')
    else:
        return redirect('/')

def idelete(request):
    if request.user.is_staff:
        idopontok = Idopont.objects.all()
        for idopont in idopontok:
            if not idopont.foglalt:
                idopont.delete()
        return redirect('/app/staffpage2')
    else:
        return redirect('/')

def createIdopont(request):
    if request.user.is_staff:
        if request.method == 'POST':
            datum = request.POST.get("datum")
            datum_pattern = r'^\d{4}-\d{2}-\d{2}$'
            ido = request.POST.get("ido")
            ido_pattern = r'^\d{2}:\d{2}$'
            
            if not re.match(datum_pattern, datum):
                messages.error(request, 'Hibás dátum formátum! Használj: ÉÉÉÉ-HH-NN (pl. 2025-05-05)')
                return redirect('/app/staffpage3')
            
            if not re.match(ido_pattern, ido):
                messages.error(request, 'Hibás idő formátum! Használj: ÓÓ:PP (pl. 21:00)')
                return redirect('/app/staffpage3')
            if Idopont.objects.filter(datum=datum, ido=ido).exists():
                messages.error(request, 'Ez az időpont már foglalt!')
                return redirect('/app/staffpage3')

            newidopont = Idopont.objects.create(datum=datum,ido=ido)
            newidopont.save()
            return redirect('/app/staffpage3')
    else:
        return redirect('/')

def igenerate(request):
    if request.user.is_staff:
        if request.method == "POST":
            kezdet_str = request.POST.get("kezdetidatum")
            if kezdet_str == "":
                kezdet_str = str(datetime.datetime.now().date())
            datum_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(datum_pattern, kezdet_str):
                    messages.error(request, 'Hibás dátum formátum! Használj: ÉÉÉÉ-HH-NN (pl. 2025-05-05)')
                    return redirect('/app/staffpage3')
            kezdetidatum = datetime.datetime.strptime(kezdet_str, "%Y-%m-%d").date()


            napok_szama = request.POST.get("nap")
            if napok_szama == "":
                napok_szama = "10"

            oras_lepes = request.POST.get("lepeskoz")
            if oras_lepes == "":
                oras_lepes = "3"
            
            nap_pattern = r'^[1-9]\d*$'


            if not re.match(nap_pattern, napok_szama):
                        messages.error(request, 'Csak pozitív egész szám adható meg a nap és lépésköz mezőkbe')
                        return redirect('/app/staffpage3')
            if not re.match(nap_pattern, oras_lepes):
                        messages.error(request, 'Csak pozitív egész szám adható meg a nap és lépésköz mezőkbe')
                        return redirect('/app/staffpage3')
            
        oras_lepes = int(oras_lepes)
        napok_szama = int(napok_szama)
        generaltnapok=0
        j=0
        while generaltnapok != napok_szama:
            
            intervalday = datetime.timedelta(days=j)
            j=j+1
            idopont = datetime.datetime(kezdetidatum.year,kezdetidatum.month,kezdetidatum.day,10,0)
            idopont = idopont + intervalday
            if idopont.weekday() == 5 or idopont.weekday() == 6:  #ha hétvége, ne generáljon  
                continue
                

            for i in range(0,10,oras_lepes):   #itt állítható, hány óránként
                    keszidopont = idopont + datetime.timedelta(hours=i)
                    Idopont.objects.get_or_create(datum=keszidopont.date(), ido=keszidopont.time())

            generaltnapok +=1
        return redirect('/app/staffpage3')
            
def sikeresfoglalas(request):
    return render(request,'sikeresfoglalas.html')

def staffpage(request):
    foglalasok = Foglalas.objects.all().order_by('idopont__datum', 'idopont__ido')
    context={'foglalasok':foglalasok,}
    return render(request, "staffpage.html",context=context)

def staffpage2(request):
    idopontok = Idopont.objects.all().order_by('datum', 'ido')
    context={'idopontok':idopontok}
    return render(request, "staffpage2.html",context=context)

def staffpage3(request):
    maidatum = str(datetime.datetime.now().date())
    context={'maidatum':maidatum}
    return render(request, "staffpage3.html",context=context)