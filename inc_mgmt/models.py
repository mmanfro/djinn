import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_upload_path(instance, filename):
    path = ""
    folder = ""
    if isinstance(instance, Ticket):
        folder = instance.id
        path = "ticket/"
    elif isinstance(instance, TicketUpdate):
        folder = instance.ticket.id
        path = "ticket/"
    
    return os.path.join(path + str(folder) + "/" + filename)


class Area(models.Model):
    name = models.CharField(_('area name'), max_length=30, unique=True)
    email = models.EmailField(_('area email address'), max_length=255, unique=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    
    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def _create_user(self, email, name, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError(_('The given email must be set' ))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=None, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, name, password=None, **extra_fields):
        return self._create_user(email, name, password, False, False, **extra_fields)
    
    def create_superuser(self, email, name, password, **extra_fields):
        user=self._create_user(email, name, password, True, True, **extra_fields)
        user.is_active=True
        user.is_trusty=True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=30)
    knoxid = models.CharField(_('knox ID'), max_length=20, blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=14, blank=True, null=True, help_text=_('Only numbers.'))
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))
    areas = models.ManyToManyField(Area)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name.split()[0]
    
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Priority(models.Model):
    priority = models.CharField(_('priority'), max_length=30, unique=True)
    
    class Meta:
        verbose_name_plural = 'Priorities'
        
    def __str__(self):
        return self.priority
    
    
class Status(models.Model):
    status = models.CharField(_('status'), max_length=20, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        verbose_name_plural = 'Status'
    
    def __str__(self):
        return self.status
    
        
class Ticket(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), max_length=500)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)   
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='created_by')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='assigned_to')
    time_created = models.DateTimeField(_('creation time'), default=timezone.now, editable=False)
    time_started = models.DateTimeField(_('starting working time'), default=timezone.now, null=True, editable=False)
    time_ended = models.DateTimeField(_('ending time'), default=timezone.now, null=True, editable=False)


class TicketUpdate(models.Model):
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    comment = models.TextField(_('comment'), max_length=500)
    time_posted = models.DateTimeField(_('posting time'), default=timezone.now)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE) 
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)
