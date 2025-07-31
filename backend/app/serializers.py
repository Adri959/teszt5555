from rest_framework import serializers
from .models import Idopont

class IdopontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idopont
        fields = '__all__'