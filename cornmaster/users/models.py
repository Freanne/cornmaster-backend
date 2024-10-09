from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('agriculteur', 'Agriculteur'),
        ('expert', 'Expert Agricole'),
        ('admin', 'Administrateur'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    numero_phone = models.CharField(max_length=20, blank=True, null=True)
    numero_ifu = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default='agriculteur')


class Agriculteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agriculteur')
    type_ferme = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255)


class ExpertAgricole(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='expert')
    specialisation = models.CharField(max_length=100)
    disponibilite = models.BooleanField(default=True)


class Administrateur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin')
