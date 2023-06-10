from django.apps import AppConfig



from django.apps import AppConfig
from django.db.models.signals import post_save

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .models import create_church_member_profile
        from .models import ChurchMember
        post_save.connect(create_church_member_profile, sender=ChurchMember)
