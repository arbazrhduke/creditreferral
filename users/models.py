import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=255
    )
    # notice the absence of a 'Password field' , that's built in.
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    credits = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=6, unique=True, null=True)
    referee_code = models.CharField(max_length=6, null=True)
    version = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password are required by default

    def add_credits(self, new_credits):
        user = User.objects.filter(
            referral_code=self.referral_code,
            version=self.version,
        ).update(
            credits=self.credits + new_credits,
            version=self.version + 1,
        )
        return user > 0

    def set_referral_code(self):
        self.referral_code = uuid.uuid4().hex[:6].upper()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def staff(self):
        """Is the user a member of staff?"""
        return self.is_staff

    @property
    def superuser(self):
        """Is the user a admin member?"""
        return self.is_superuser

    @property
    def active(self):
        """Is the user active?"""
        return self.is_active

    objects = UserManager()
