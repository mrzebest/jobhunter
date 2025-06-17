from django.db import models
from django.contrib.auth.models import User

class Candidature(models.Model):
    CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('ALTERNANCE', 'Alternance'),
        ('STAGE', 'Stage'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entreprise = models.CharField(max_length=255)
    titre = models.CharField(max_length=255)
    lien = models.URLField(max_length=500) 
    ville = models.CharField(max_length=255, default="")  
    type_contrat = models.CharField(max_length=20, choices=CONTRAT_CHOICES, default='CDI')
    statut = models.CharField(max_length=50, default="en attente")
    date_postulation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entreprise} - {self.titre}"
