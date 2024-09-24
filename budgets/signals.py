# budgets/signals.py

from django.db.models.signals import post_save  # Import post_save signal
from django.dispatch import receiver  # Import receiver decorator
from django.contrib.auth.models import User  # Import User model
from .models import TeamAndSetting, UserProfile  # Import related models

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only create profile if the user is newly created
        UserProfile.objects.get_or_create(user=instance)
        
# Signal to create TeamAndSetting whenever a UserProfile is created
@receiver(post_save, sender=UserProfile)
def create_team_setting(sender, instance, created, **kwargs):
    if created:  # Check if the UserProfile instance was created
        TeamAndSetting.objects.create(
            user=instance.user,  # Correctly associate with the User instance
            team_name='Video Game Consoles SDE Team',  # Default team name
            currency='USD',  # Default currency
            communication_preference='Email',  # Default communication preference
            role=instance.role,  # Role from UserProfile
            work_phone=instance.generate_random_phone_number()  # Generate random phone number
        )
