import logging

from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models, transaction
from django.conf import settings

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    """
    Custom user manager is necessary for custom user with custom fields (notably email as username) to work.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            logger.warning("No mail entered for new user.")
            raise ValueError('User must have an email address.')
        with transaction.atomic():
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    """
    Custom user,
    Declared in settings.py
    """
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='email address',
        error_messages={'unique': 'A user with this email already exists.'})
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    date_joined = None
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    readonly_fields = ['date_created', 'date_updated']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Client(models.Model):
    """
    Client model.
    Gathering info about clients. Clients are not real users of the app.
    Foreign key to sales contact assigned by management user.
    """
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='email address',
        error_messages={'unique': 'A user with this email already exists.'})
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        client_name = f"{self.first_name} {self.last_name} - {self.email}"
        return client_name
