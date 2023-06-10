from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from members.models import ChurchMember

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    baptism_date = models.DateField(blank=True, null=True)
    is_first_login = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Import ChurchMember if it's not in the same file
# from .models import ChurchMember

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='img/default.png')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class ChurchMemberProfile(models.Model):
    church_member = models.OneToOneField(ChurchMember, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='img/default.png')

    def __str__(self):
        return self.church_member.first_name + ' ' + self.church_member.last_name

@receiver(post_save, sender=ChurchMember)
def create_church_member_profile(sender, instance, created, **kwargs):
    if created:
        ChurchMemberProfile.objects.create(church_member=instance)

