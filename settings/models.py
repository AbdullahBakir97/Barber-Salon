from django.db import models
from contact.models import Owner

class Salon(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, related_name='salon')
