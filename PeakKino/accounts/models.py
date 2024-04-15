from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, user_name, password, **extra_fields):
        
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  

        return user
    
    def create_user(self, user_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_approved', False)

        return self._create_user(user_name, password, **extra_fields)
    
    def create_superuser(self, user_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)

        return self._create_user(user_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=20, unique=True)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()
