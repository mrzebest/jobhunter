from rest_framework import serializers
from .models import Candidature

class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = '__all__'
        read_only_fields = ['user']
