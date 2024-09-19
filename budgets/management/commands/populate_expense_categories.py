# budgets/management/commands/populate_expense_categories.py
from django.core.management.base import BaseCommand
from budgets.models import ExpenseCategory

class Command(BaseCommand):
    help = 'Populate the ExpenseCategory model with predefined categories'

    def handle(self, *args, **options):
        categories = ['Food', 'Office Equipment', 'Software', 'IT repairs', 'Business Trips', 'Travel']
        
        for category_name in categories:
            ExpenseCategory.objects.get_or_create(name=category_name)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated ExpenseCategory table'))
