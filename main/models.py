from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

        def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
                now = timezone.now()

                if not email:
                        raise ValueError('Email Must Be Set')

                email = self.normalize_email(email)
                user = self.model(email=email,
                                   is_staff=is_staff,
                                   is_active=True,
                                   is_superuser=is_superuser,
                                   last_login=now,
                                   date_joined=now,
                                   **extra_fields
                                    )

                user.set_password(password)
                user.save(using=self._db)

                return user

        def create_user(self, email, password=None, **extra_fields):
                return self._create_user(email, password, False, False, **extra_fields)

        def create_superuser(self, email, password, **extra_fields):
                return self._create_user(email, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(_('email address'), max_length=254, unique=True)
        first_name = models.CharField(_('first name'), max_length=30, blank=True)
        last_name = models.CharField(_('last name'), max_length=30, blank=True)
        is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Lets the user login to Django admin dashboard'))
        is_active = models.BooleanField(_('active'), default=True, help_text=_('Marks the account as usable'))
        date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

        objects = CustomUserManager()


        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        class Meta:
                verbose_name= _('user')
                verbose_name= _('users')

        def get_absolute_url(self):
                full_name = '%s %s' % (self.first_name, self.last_name)
                return full_name.strip()

        def get_short_name(self):
                return self.first_name

        def email_user(self, subject, message, from_email=None):
                send_mail(subject, message, from_email, [self.email])


class SpeedModel(models.Model):
        #pk = models.IntegerField(auto_increment=True)
        title = models.CharField(max_length=255)
        info = models.TextField()
        image = models.ImageField(upload_to='image', null=True, blank=True)
        user = models.ForeignKey(CustomUser)
        up_votes = models.ManyToManyField(CustomUser, blank=True, related_name='up_votes')
        down_votes = models.ManyToManyField(CustomUser, blank=True, related_name='down_votes')

        def __unicode__(self):
                return self.title