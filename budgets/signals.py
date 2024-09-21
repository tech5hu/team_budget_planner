# budgets/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TeamAndSetting, UserProfile
import random

@receiver(post_save, sender=UserProfile)
def create_team_setting(sender, instance, created, **kwargs):
    if created:
        TeamAndSetting.objects.create(
            user=instance,
            team_name='Default Team',
            currency='USD',
            communication_preference='Email',
            role=instance.role,
            work_phone=f"+1-{random.randint(1000, 9999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)