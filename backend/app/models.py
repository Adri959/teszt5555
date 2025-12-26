from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Szolgaltatas(models.Model):
    nev = models.CharField(max_length=126,null=False, blank=False)
    ar = models.DecimalField(max_digits=12, decimal_places=2,null=False, blank=False)
    leiras = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nev

class Idopont(models.Model):
    datum = models.DateField(null=False, blank=False)
    ido = models.TimeField(null=False, blank=False)
    foglalt = models.BooleanField(default=False)

    def __str__(self):
        return str(self.datum) + " " + str(self.ido) + (" Foglalt" if self.foglalt else " Szabad")
    

    class Meta:
        unique_together = ('datum','ido')


class Foglalas(models.Model):
    idopont = models.OneToOneField(Idopont, on_delete=models.CASCADE)  # Egy időpontra csak egy foglalás lehet
    szolgaltatas = models.ForeignKey(Szolgaltatas, on_delete=models.CASCADE)
    tapasztalat = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user} - {self.szolgaltatas} - {self.idopont.datum} - {self.idopont.ido}"
