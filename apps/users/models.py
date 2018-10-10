from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Permission, PermissionsMixin, Group
)
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserProfileManager(BaseUserManager):
    def create_user(self, username, nickname, email, password=None):
        """
        Creates and saves a User with the given username, nickname, email and password.
        """
        if not username:
            raise ValueError('Users must have a name')

        if not nickname:
            raise ValueError('Users must have a nickname')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            nickname=nickname,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, email, password):
        """
        Creates and saves a superuser with the given username, nickname, email, and password.
        """
        user = self.create_user(username=username,
                                nickname=nickname,
                                password=password,
                                email=email,
                                )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name=_('Username'), max_length=64, unique=True)
    nickname = models.CharField(verbose_name=_('Nickname'), max_length=64)
    email = models.EmailField(verbose_name=_('Email'), max_length=64, unique=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Superuser'))
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'email']

    class Meta:
        db_table = 'UserProfile'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profile')

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_user_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.nickname

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    @property
    def is_valid(self):
        if self.is_active:
            return True
        return False

    @property
    def is_staff(self):
        return self.is_superuser
