from django.db import models
from contact.models import Owner

class Salon(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, related_name='salon')
    web_icon = models.ImageField(upload_to='owner_logos/', blank=True, null=True)
