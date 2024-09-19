# budgets/management/commands/populate_user_categories.py
from django.core.management.base import BaseCommand
from budgets.models import ExpenseCategory, UserCategory, TeamMember

class Command(BaseCommand):
    help = 'Populate the UserCategory model with predefined categories for users'

    def handle(self, *args, **options):
        # Define some example expense categories
        categories = ['Food', 'Office Equipment', 'Software', 'IT repairs', 'Business Trips', 'Travel']
        
        # Create ExpenseCategory instances if they don't exist
        for category_name in categories:
            ExpenseCategory.objects.get_or_create(name=category_name)
        
        # Create UserCategory instances for all users and categories
        for user in TeamMember.objects.all():
            for category in ExpenseCategory.objects.all():
                UserCategory.objects.get_or_create(user=user, category=category)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated UserCategory and ExpenseCategory tables'))
