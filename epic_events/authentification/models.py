from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models, transaction
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom user manager is necessary for custom user with custom fields (notably email as username) to work.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        with transaction.atomic():
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user,
    Declared in settings.py
    """
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='email address',
        error_messages={'unique': 'A user with this email already exists.'})
    phone = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_superuser

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Client(models.Model):
    """
    Client model.
    Gathering info about clients. clients are not users of the app.
    Foreign key to sales user assigned by management user.
    """
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='email address',
        error_messages={'unique': 'A user with this email already exists.'})
    phone = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
