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
    
        foglalas = Foglalas(idopont=idopont, szolgaltatas=Szolgaltatasobj, user=userobj)
        foglalas.save()
        
    return redirect('/app')

def szolgaltatasok(request):
    return render(request, 'szolgaltatasok.html')

def rolunk(request):
    return render(request, 'rolunk.html')

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
        return redirect('/app/sikeresreg')


    return render(request, 'regisztracio.html')

def belepes(request):
    if request.method =="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password,email=email)
        if user is not None:
            login(request,user)
            return redirect('/app')
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

def foglalastorles(request):
    if request.method == 'POST':
        foglalasid = request.POST.get("foglalasid")
        torlendo = Foglalas.objects.get(id=foglalasid)
        torlendo.idopont.foglalt = False
        torlendo.idopont.save()
        torlendo.delete()
        
    return redirect('/app/profilepage')