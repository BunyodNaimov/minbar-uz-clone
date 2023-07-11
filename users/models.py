from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("Email"), unique=True, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, unique=True, null=True, )
    address = models.CharField(_("Address"), max_length=200, unique=True, null=True)
    birth_date = models.DateField(_("BirthDate"), null=True, blank=True)
    profile_picture = models.ImageField(_("ProfilePicture"), upload_to='profile_picture/', null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return self.get_full_name()


