# budgets/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User, Group, Permission  # Import necessary user models
from django.db import models  # Import Django models
from django.db.models.signals import post_save  # Import signal for post-save
from django.dispatch import receiver  # Import receiver decorator
import random  # Import random for generating random phone numbers

# User Profile Manager for creating User and Superuser
class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:  # Ensure email is provided
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize email
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Set is_staff to True for superuser
        extra_fields.setdefault('is_superuser', True)  # Set is_superuser to True
        return self.create_user(username, email, password, **extra_fields)  # Create user

# User Profile model extending AbstractBaseUser and PermissionsMixin
class UserProfile(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('regular', 'Regular'),
    ]
    ACCOUNT_LEVEL_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    ]

    # Fields for UserProfile
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    email = models.EmailField(unique=True)  # Unique email field
    username = models.CharField(max_length=150, unique=True)  # Unique username field
    account_level = models.CharField(max_length=20, choices=ACCOUNT_LEVEL_CHOICES, default='developer')  # Account level
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='regular')  # User role
    is_manager = models.BooleanField(default=False)  # Boolean flag for manager status
    work_phone = models.CharField(max_length=15, blank=True, null=True)  # Optional work phone field
    team = models.CharField(max_length=100, blank=True, null=True)  # Optional team field

    USERNAME_FIELD = 'username'  # Specify username field as the unique identifier
    REQUIRED_FIELDS = ['email']  # Specify required fields for creating user

    # Many-to-many relationships for groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name='user_profiles',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',
        blank=True,
    )

    def generate_random_phone_number(self):
        """Generates a random phone number."""
        return f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.work_phone:  # Assign phone number if not set
            self.work_phone = self.generate_random_phone_number()
        # Set account level and manager status based on role
        if self.role == 'admin':
            self.account_level = 'manager'
            self.is_manager = True
        elif self.role == 'regular':
            self.account_level = 'developer'
            self.is_manager = False
        super().save(*args, **kwargs)  # Call the parent save method

# Signal to create or update UserProfile when User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    user_profile, _ = UserProfile.objects.get_or_create(user=instance)  # Get or create UserProfile

    if created:  # If the User was just created
        # Assign default permissions based on role
        if user_profile.role == 'admin':
            instance.is_staff = True  # Set staff status
            instance.save()  # Save User instance
            instance.user_permissions.set(Permission.objects.all())  # Assign all permissions
        else:
            user_permissions = Permission.objects.filter(
                codename__in=[
                    'add_budgetandcategory', 'change_budgetandcategory', 'view_budgetandcategory',
                    'add_transaction', 'change_transaction', 'view_transaction',
                ]
            )
            instance.user_permissions.set(user_permissions)  # Assign specific user permissions

        # Assign default team if not set
        if not user_profile.team:
            user_profile.team = "Video Game Consoles SDE Team"  # Default team

    # Update profile fields based on User instance
    user_profile.username = instance.username
    user_profile.email = instance.email
    
    # Assign role based on account level
    if user_profile.account_level == 'manager':
        user_profile.role = 'admin'
    else:  # Only other option is 'developer'
        user_profile.role = 'regular'

    user_profile.save()  # Save UserProfile instance

# Team and Setting model for managing team settings
class TeamAndSetting(models.Model):
    TEAM_CHOICES = [
        ('Video Game Consoles SDE Team', 'Video Game Consoles SDE Team'),
    ]
    CURRENCY_CHOICES = [
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
    ]
    
    # Fields for TeamAndSetting
    team_name = models.CharField(max_length=100, choices=TEAM_CHOICES, default='Video Game Consoles SDE Team')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USD')  # Currency field
    communication_preference = models.CharField(max_length=50, default='email')  # Communication preference
    role = models.CharField(max_length=50, choices=[('manager', 'Manager'), ('developer', 'Developer')])  # Role field
    work_phone = models.CharField(max_length=25, blank=True, null=True)  # Optional work phone field
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    def __str__(self):
        return self.team_name  # String representation

# Expense Category model for managing expense categories
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique category name

    def __str__(self):
        return self.name  # String representation

# Budget and Category model for managing budgets
class BudgetAndCategory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Foreign key to UserProfile
    budget_name = models.CharField(max_length=100)  # Budget name
    income_amount = models.DecimalField(decimal_places=2, max_digits=10)  # Income amount
    expense_amount = models.DecimalField(decimal_places=2, max_digits=10)  # Expense amount
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)  # Foreign key to ExpenseCategory
    payment_method = models.CharField(max_length=100)  # Payment method
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    @property
    def remaining_amount(self):
        return self.income_amount - self.expense_amount  # Calculate remaining amount

    # Method to calculate total amount (example logic)
    def total_amount(self):
        return sum(transaction.amount for transaction in self.transactions.all())  # Calculate total transaction amount

    def __str__(self):
        return self.budget_name  # String representation

    class Meta:
        permissions = [
            ("can_create_budget", "Can create budgets"),
            ("can_read_budget", "Can read budgets"),
            ("can_update_budget", "Can update budgets"),
        ]    

# Transaction model for managing transactions
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    budget = models.ForeignKey(BudgetAndCategory, on_delete=models.CASCADE, related_name='transactions')  # Foreign key to BudgetAndCategory
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)  # Foreign key to UserProfile
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)  # Foreign key to ExpenseCategory
    transaction_date = models.DateField()  # Transaction date
    payment_method = models.CharField(max_length=100)  # Payment method
    description = models.TextField(blank=True, null=True)  # Optional description
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)  # Transaction type

    class Meta:
        permissions = [
            ("can_create_transaction", "Can create transactions"),
            ("can_read_transaction", "Can read transactions"),
            ("can_update_transaction", "Can update transactions"),
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"  # String representation

# Example data for ExpenseCategory
expense_categories_data = [
    'Cloud Services',
    'Software Licenses',
    'Development Tools',
    'Training Programs',
]

# Example function to populate initial data
def populate_initial_data():
    for category_name in expense_categories_data:
        ExpenseCategory.objects.get_or_create(name=category_name)  # Create expense categories if not exist