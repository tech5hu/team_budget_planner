from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from budgets.models import UserProfile  # Adjust this import if needed
from django.db.models.signals import post_save
from django.dispatch import receiver

class Command(BaseCommand):
    help = 'Set is_staff to True for all users and create UserProfile where needed.'

    def handle(self, *args, **kwargs):
        # Disconnect the post_save signal temporarily
        post_save.disconnect(receiver=save_user_profile, sender=User)

        users = User.objects.all()
        for user in users:
            user.is_staff = True
            user.save()

            # Ensure the UserProfile exists for the user
            UserProfile.objects.get_or_create(user=user)

        # Reconnect the post_save signal
        post_save.connect(receiver=save_user_profile, sender=User)

        self.stdout.write(self.style.SUCCESS('Successfully set is_staff to True for all users and created UserProfile where needed.'))

def save_user_profile(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Optionally handle updates here
        user_profile = getattr(instance, 'userprofile', None)
        if user_profile:
            user_profile.save()  # Only save if the profile exists
