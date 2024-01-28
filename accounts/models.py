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

class CustomUser(AbstractUser):
    name = models.CharField(_('Name'), default='Dein Name', max_length=255)
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Telefon'), max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(_('Geburtsdatum'), blank=True, null=True)
    gender = models.CharField(_('Geschlecht'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(_('Adresse'), blank=True, null=True)
    password = models.CharField(
        _('Passwort'),
        max_length=128,
        validators=[
            MinimumLengthValidator,
            CommonPasswordValidator,
            NumericPasswordValidator,
            UserAttributeSimilarityValidator,
        ],
        help_text=_('Ihr Passwort muss mindestens 8 Zeichen lang sein und eine Mischung aus Buchstaben, Ziffern und Symbolen enthalten.'),
    )

    groups = models.ManyToManyField(
            'auth.Group',
            verbose_name=_('groups'),
            blank=True,
            related_name='custom_user_groups'
        )
    user_permissions = models.ManyToManyField(
            'auth.Permission',
            verbose_name=_('user permissions'),
            blank=True,
            related_name='custom_user_permissions'
    )
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_profile', on_delete=models.CASCADE, verbose_name=_('Benutzer'))
    barber = models.ForeignKey(Barber, related_name='barber_profile', on_delete=models.SET_NULL, verbose_name=_('Friseur'),  null=True, blank=True)
    profile_image = models.ImageField(_('Profile Foto'), upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"Profil von {self.user.username}"

class OwnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='owner_user_profile', on_delete=models.CASCADE, verbose_name=_('Benutzer'), default=1)
    owner = models.OneToOneField(Owner, related_name='owner_profile', on_delete=models.CASCADE, verbose_name=_('Eigentümer'), default=None)
    image = models.ImageField(_('Foto'), upload_to='profile_images/')

    def __str__(self):
        return f"Eigentümerprofil {self.owner.name}"
