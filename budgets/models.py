from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
import random

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('regular', 'Regular'),
    ]
    ACCOUNT_LEVEL_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Correct way to refer to the custom user model
        on_delete=models.CASCADE,
        null=True,
    )

    USERNAME_FIELD = 'username'
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    account_level = models.CharField(max_length=20, choices=ACCOUNT_LEVEL_CHOICES, default='developer')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='regular')
    team = models.CharField(max_length=50, default='Video Game Consoles SDE Team')
    work_phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)  # New field to check if user is a manager
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def generate_random_phone_number(self):
        while True:
            phone_number = f'{random.randint(1000000000, 9999999999)}'
            if not UserProfile.objects.filter(work_phone=phone_number).exists():
                return phone_number

    def save(self, *args, **kwargs):
        if not self.pk and not self.work_phone:
            self.work_phone = self.generate_random_phone_number()
        super().save(*args, **kwargs)

class TeamAndSetting(models.Model):
    TEAM_CHOICES = [
        ('Video Game Consoles SDE Team', 'Video Game Consoles SDE Team'),
    ]
    CURRENCY_CHOICES = [
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
    ]
    
    team_name = models.CharField(max_length=100, choices=TEAM_CHOICES, default='Video Game Consoles SDE Team')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='USD')
    communication_preference = models.CharField(max_length=50, default='email')
    role = models.CharField(max_length=50, choices=[('manager', 'Manager'), ('developer', 'Developer')])
    work_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BudgetAndCategory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    budget_name = models.CharField(max_length=100)
    income_amount = models.DecimalField(decimal_places=2, max_digits=10)
    expense_amount = models.DecimalField(decimal_places=2, max_digits=10)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.budget_name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    budget = models.ForeignKey(BudgetAndCategory, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    payment_method = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.amount} on {self.transaction_date}"