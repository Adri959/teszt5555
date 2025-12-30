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
    path('foglalastorles/', views.foglalastorles, name="foglalastorles"),

    path('sikeresreg/', views.sikeresreg, name="sikeresreg"),
    path('sikeresfoglalas/', views.sikeresfoglalas, name="sikeresfoglalas"),

    path('api/', views.SzabadIdopontokApi, name="SzabadIdopontokApi"),

]
