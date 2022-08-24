from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.auth import get_user_model
import authApp.models as models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, msisdn, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not msisdn:
            raise ValueError(_('The Phone Number must be set'))
        email = self.normalize_email(msisdn)
        user = self.model(msisdn=msisdn, is_active=False, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, msisdn, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(msisdn, password, **extra_fields)
    


class UsernameOrEmailBackend(object):
    def authenticate(self, msisdn=None, password=None, **kwargs):
        try:
            # Try to fetch the user by searching the username or email field
            user = User.objects.get(Q(username=msisdn)|Q(msisdn=msisdn))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)