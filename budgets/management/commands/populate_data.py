from django.core.management.base import BaseCommand
from budgets.models import BudgetAndCategory, UserProfile, Transaction, TeamAndSetting
from django.contrib.auth.models import Group
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating data...')

        # Delete all existing records
        BudgetAndCategory.objects.all().delete()
        UserProfile.objects.all().delete()
        TeamAndSetting.objects.all().delete()
        Transaction.objects.all().delete()

        # Define your data
        expense_categories = [
            'Cloud Services', 'Software Licenses', 
            'Development Tools', 'Training Programs'
        ]
        payment_methods = [
            'Corporate Credit Card', 'Company Expense Report', 
            'Direct Bank Transfer', 'Reimbursement Request'
        ]
        communication_preferences = ['Email', 'Phone', 'Slack']

        # Create 10 BudgetAndCategory records
        budget_names = [
            'Cloud Infrastructure', 'Software Development Tools', 
            'Employee Training', 'Team Collaboration Software',
            'Network Equipment', 'Server Maintenance', 
            'Database Licensing', 'Performance Testing', 
            'Development Frameworks', 'Project Management Tools'
        ]
        
        for name in budget_names:
            income_amount = round(random.uniform(500.00, 1000.00), 2)
            expense_amount = round(random.uniform(100.00, income_amount - 1), 2)  # Ensure expense is less than income
            BudgetAndCategory.objects.create(
                budget_name=name,
                income_amount=income_amount,
                expense_amount=expense_amount,
                expense_category=random.choice(expense_categories),
                payment_method=random.choice(payment_methods),
            )
        
        # Create or get groups for managers and developers
        manager_group, created = Group.objects.get_or_create(name='Managers')
        developer_group, created = Group.objects.get_or_create(name='Developers')

        # Create UserProfile records (3 managers and 7 developers)
        user_data = [
            ('man_alice', 'alice@example.com', 'admin'),
            ('man_bob', 'bob@example.com', 'admin'),
            ('man_charlie', 'charlie@example.com', 'admin'),
            ('dev_david', 'david@example.com', 'regular'),
            ('dev_eve', 'eve@example.com', 'regular'),
            ('dev_frank', 'frank@example.com', 'regular'),
            ('dev_grace', 'grace@example.com', 'regular'),
            ('dev_heidi', 'heidi@example.com', 'regular'),
            ('dev_ivan', 'ivan@example.com', 'regular'),
            ('dev_judy', 'judy@example.com', 'regular'),
        ]

        for username, email, account_level in user_data:
            user, created = UserProfile.objects.get_or_create(
                username=username,
                email=email,
                defaults={
                    'password': make_password('password'),  # Use hashed password
                    'role': 'manager' if account_level == 'admin' else 'developer'
                }
            )
            # Assign users to groups
            if account_level == 'admin':
                user.groups.add(manager_group)
            else:
                user.groups.add(developer_group)
        
        # Create TeamAndSetting records
        users = UserProfile.objects.all()
        for user in users:
            TeamAndSetting.objects.get_or_create(
                team_name='Video Game Consoles SDE Team',
                user=user,
                currency=random.choice(['GBP', 'USD']),
                communication_preference=random.choice(communication_preferences),
                role=user.role,
                work_phone=f"+1-{random.randint(1000, 9999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            )
        
        # Create Transaction records
        budgets = BudgetAndCategory.objects.all()
        transaction_types = ['income', 'expense']

        for _ in range(10):
            description = f"Transaction related to {random.choice(expense_categories)}"
            transaction_date = make_aware(datetime.now() - timedelta(days=random.randint(1, 30)))
            payment_method = random.choice(payment_methods)
            transaction_type = random.choice(transaction_types)
            
            user_profile = random.choice(users)
            budget = random.choice(budgets)  # Choose a budget for the transaction

            # Set amounts based on transaction type
            if transaction_type == 'income':
                amount = round(random.uniform(100.00, float(budget.income_amount)), 2)
            else:  # expense
                amount = round(random.uniform(100.00, float(budget.expense_amount)), 2)

            # Create the transaction
            Transaction.objects.create(
                budget=budget,
                user_category=user_profile,  # This will show the username
                expense_category=budget,  # Use the budget instance instead
                amount=amount,
                transaction_date=transaction_date.date(),
                payment_method=payment_method,
                description=description,
                transaction_type=transaction_type
            )

        self.stdout.write(self.style.SUCCESS('Data populated successfully'))
