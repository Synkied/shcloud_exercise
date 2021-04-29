"""
Users models
"""
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils.translation import gettext_lazy as _

from timezone_field import TimeZoneField

import users.permissions.admin

PERMISSION_BACKENDS = [
    users.permissions.admin.AdminBackend(),
]


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission
    checking.

    Replaces django.contrib.auth.models._user_has_perm since we don't want
    to use the `django.contrib.auth.backends.ModelBackend` for the permissions
    but we still need it for authentication...
    """
    for backend in PERMISSION_BACKENDS:
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_perms(user, perms, obj):
    for backend in PERMISSION_BACKENDS:
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            fail = False
            for perm in perms:
                if not backend.has_perm(user, perm, obj):
                    fail = True
                    continue
            if fail:
                continue
            return True
        except PermissionDenied:
            return False
    return False


class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password
        """
        if not email:
            raise ValueError('Superuser must have an email address')
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User model
    """
    MAN = 'M'
    WOMAN = 'W'
    GENDERS = (
        (MAN, _('Mr')),
        (WOMAN, _('Mme')),
    )

    email = models.EmailField(
        _('email address'),
        max_length=255,
        db_index=True,
        unique=True
    )
    gender = models.CharField(
        _('gender'),
        max_length=1,
        default=MAN,
        choices=GENDERS,
    )
    timezone = TimeZoneField(default='Europe/London')
    name = models.CharField(
        _('fullname'),
        max_length=255,
        blank=False
    )
    private_key = models.UUIDField(
        _('private api key'),
        default=uuid.uuid4,
        editable=False,
    )
    user_uuid = models.UUIDField(
        _('private id'),
        default=None,
        editable=False,
        null=True,
        blank=True,
    )

    # User type flags
    is_admin = models.BooleanField(
        _('admin'),
        default=False
    )
    is_staff = models.BooleanField(
        _('staff'),
        default=False
    )
    is_active = models.BooleanField(_('Enabled'), default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perms, obj=None):
        """
        Works like has_perm but parameter 'perms' is tuple of permissions.
        """
        return _user_has_perms(self, perms, obj)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        pass
