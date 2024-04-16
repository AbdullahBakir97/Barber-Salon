from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import validators
from django.contrib.auth.password_validation import CommonPasswordValidator, MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator
from django.contrib.auth.models import User
from contact.models import Barber , Owner
#from phonenumber_field.modelfields import PhoneNumberField
 


GENDER_CHOICES = [
    ('male', _('Männlich')),
    ('female', _('Weiblich')),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.SET_NULL, verbose_name=_('Benutzer'),null=True, blank=True)
    barber = models.ForeignKey(Barber, related_name='barber_profile', on_delete=models.SET_NULL, verbose_name=_('Friseur'),  null=True, blank=True)
    phone = models.CharField(_('Telefon'), max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(_('Geburtsdatum'), blank=True, null=True)
    gender = models.CharField(_('Geschlecht'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(_('Adresse'), blank=True, null=True)
    profile_image = models.ImageField(_('Profile Foto'), upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"Profil von {self.user}"

class OwnerProfile(models.Model):
    user = models.OneToOneField(User, related_name='owner_user_profile', on_delete=models.SET_NULL, verbose_name=_('Benutzer'), default=1,null=True, blank=True)
    owner = models.OneToOneField(Owner, related_name='owner_profile', on_delete=models.SET_NULL, verbose_name=_('Eigentümer'), default=None, null=True, blank=True)
    phone = models.CharField(_('Telefon'), max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(_('Geburtsdatum'), blank=True, null=True)
    gender = models.CharField(_('Geschlecht'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(_('Adresse'), blank=True, null=True)
    image = models.ImageField(_('Foto'), upload_to='profile_images/')

    def __str__(self):
        return f"Eigentümerprofil {self.owner.name}"
