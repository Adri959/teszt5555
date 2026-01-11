from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.index, name="index"),
    path('foglalas/', views.foglalas, name="foglalas"),
    path('foglal/', views.foglal, name="foglal"),


    path('belepes/', views.belepes, name="belepes"),
    path('regisztracio/', views.regisztracio, name="regisztracio"),
    path('kilepes/', views.kilepes, name="kilepes"),
    path('profilepage/', views.profilepage, name="profilepage"),
    
    path('foglalaslemondas/', views.foglalaslemondas, name="foglalaslemondas"),
    path('foglalaslemondasAdmin/', views.foglalaslemondasAdmin, name="foglalaslemondasAdmin"),
    path('foglalastorlesAdmin/', views.foglalastorlesAdmin, name="foglalastorlesAdmin"),
    path('idoponttorlesAdmin/', views.idoponttorlesAdmin, name="idoponttorlesAdmin"),
    path('idelete/', views.idelete, name="idelete"),
    path('createIdopont/', views.createIdopont, name="createIdopont"),
    path('igenerate/', views.igenerate, name="igenerate"),


    path('sikeresreg/', views.sikeresreg, name="sikeresreg"),
    path('sikeresfoglalas/', views.sikeresfoglalas, name="sikeresfoglalas"),

    path('staffpage/', views.staffpage, name="staffpage"),
    path('staffpage2/', views.staffpage2, name="staffpage2"),
    path('staffpage3/', views.staffpage3, name="staffpage3"),

    path('api/', views.SzabadIdopontokApi, name="SzabadIdopontokApi"),

]
