from django.core.management.base import BaseCommand
from budgets.models import BudgetAndCategory, UserProfile, Transaction, TeamAndSetting, ExpenseCategory
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from budgets.signals import create_user_profile, create_team_setting
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating data...')

        # Temporarily disconnect the signals to prevent auto-creation of profiles
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(create_team_setting, sender=UserProfile)

        # Delete all existing records
        BudgetAndCategory.objects.all().delete()
        UserProfile.objects.all().delete()
        TeamAndSetting.objects.all().delete()
        Transaction.objects.all().delete()
        User.objects.all().delete()  # Clear users too if needed

        # Define your expense categories and other constants
        expense_categories = [
            'Cloud Services', 'Software Licenses', 
            'Development Tools', 'Training Programs',
            'Server Maintenance', 'Network Equipment', 
            'Performance Testing', 'Project Management Tools'
        ]
        payment_methods = [
            'Corporate Credit Card', 'Company Expense Report', 
            'Direct Bank Transfer', 'Reimbursement Request'
        ]
        communication_preferences = ['Email', 'Phone', 'Slack']

        # Create ExpenseCategory records
        for category_name in expense_categories:
            ExpenseCategory.objects.get_or_create(name=category_name)

        # Create or get groups for managers and developers
        manager_group, _ = Group.objects.get_or_create(name='Managers')
        developer_group, _ = Group.objects.get_or_create(name='Developers')

        # Create admin user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'password': make_password('123')  # Store hashed password
            }
        )

        # Manually create UserProfile for admin user
        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'email': 'admin@example.com',
                'username': 'admin',
                'password': make_password('123'),  # Store hashed password
                'role': 'admin',
                'is_manager': True,  # Admin is a manager
            }
        )

        # User data for additional users
        user_data = [
            ('man_alice', 'alice@example.com', True),
            ('man_bob', 'bob@example.com', True),
            ('man_charlie', 'charlie@example.com', True),
            ('dev_david', 'david@example.com', False),
            ('dev_eve', 'eve@example.com', False),
            ('dev_frank', 'frank@example.com', False),
            ('dev_grace', 'grace@example.com', False),
            ('dev_heidi', 'heidi@example.com', False),
            ('dev_ivan', 'ivan@example.com', False),
            ('dev_judy', 'judy@example.com', False),
        ]

        users = []
        for username, email, is_manager in user_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': make_password('password')
                }
            )

            # Manually create UserProfile without signal interference
            user_profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'email': email,
                    'username': username,
                    'password': make_password('password'),  # Store hashed password
                    'role': 'admin' if is_manager else 'developer',
                    'is_manager': is_manager,
                }
            )

            # Assign users to groups
            if is_manager:
                user.groups.add(manager_group)
            else:
                user.groups.add(developer_group)

            users.append(user_profile)

        # Create BudgetAndCategory records
        budget_names = [
            'Monthly Cloud Service Subscription',
            'Annual Software License Fees', 
            'Budget for Development Tool Licenses',
            'Employee Training and Development Budget',
            'Quarterly Server Maintenance Costs',
            'Annual Network Equipment Purchases',
            'Budget for Performance Testing Services',
            'Monthly Subscription for Project Management Tools',
            'Yearly Budget for Team Collaboration Tools',
            'Annual Database License Renewal Fees'
        ]
        
        for name in budget_names:
            income_amount = round(random.uniform(500.00, 1000.00), 2)
            expense_amount = round(random.uniform(100.00, income_amount - 1), 2)
            BudgetAndCategory.objects.create(
                budget_name=name,
                income_amount=income_amount,
                expense_amount=expense_amount,
                expense_category=random.choice(ExpenseCategory.objects.all()),
                payment_method=random.choice(payment_methods),
                user_profile=random.choice(users),
            )

        # Create TeamAndSetting records
        for user_profile in users:
            TeamAndSetting.objects.get_or_create(
                team_name='Default Team',
                user=user_profile.user,
                currency='GBP',
                communication_preference=random.choice(communication_preferences),
                role=user_profile.role,
                work_phone=f"+1-{random.randint(1000, 9999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            )
        
        # Create Transaction records
        budgets = BudgetAndCategory.objects.all()
        transaction_types = ['income', 'expense']

        for _ in range(10):
            expense_category = random.choice(ExpenseCategory.objects.all())
            transaction_date = make_aware(datetime.now() - timedelta(days=random.randint(1, 30)))
            payment_method = random.choice(payment_methods)
            transaction_type = random.choice(transaction_types)
            user_profile = random.choice(users)
            budget = random.choice(budgets)

            # Generate amount based on transaction type
            if transaction_type == 'income':
                amount = round(random.uniform(100.00, float(budget.income_amount)), 2)
                description = f"Received an income of £{amount} from project A."
            else:
                amount = round(random.uniform(100.00, float(budget.expense_amount)), 2)
                description = f"Paid £{amount} for {expense_category.name}: {self.generate_transaction_description(expense_category.name)}"

            Transaction.objects.create(
                budget=budget,
                user_profile=user_profile,
                expense_category=budget.expense_category,
                amount=amount,
                transaction_date=transaction_date.date(),
                payment_method=payment_method,
                description=description,
                transaction_type=transaction_type
            )

        # Reconnect signals after bulk operation
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(create_team_setting, sender=UserProfile)

        self.stdout.write(self.style.SUCCESS('Data populated successfully'))

    def generate_transaction_description(self, category):
        descriptions = {
            'Cloud Services': "Monthly cloud storage subscription.",
            'Software Licenses': "Renewed software licenses for the team.",
            'Development Tools': "Purchased development tool licenses.",
            'Training Programs': "Paid for training program on agile methodologies.",
            'Server Maintenance': "Quarterly server maintenance completed.",
            'Network Equipment': "Acquired new network routers.",
            'Performance Testing': "Engaged a service for performance testing.",
            'Project Management Tools': "Monthly subscription for project management tools.",
            'Team Collaboration Software': "Yearly subscription for team collaboration software.",
            'Database Licensing': "Renewed database licenses."
        }
        return descriptions.get(category, "General transaction for unspecified category.")
