from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    ]
    account_level = models.CharField(max_length=20, default='Developer')
    team = models.CharField(max_length=50, default='Video Game Consoles')
    work_phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def generate_random_phone_number(self):
        return f'{random.randint(1000000000, 9999999999)}'

    def save(self, *args, **kwargs):
        if not self.pk and not self.work_phone:  # If creating a new user and no phone number set
            self.work_phone = self.generate_random_phone_number()
            print(f'Generated phone number in save: {self.work_phone}')  # Debug print
        super().save(*args, **kwargs)

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.names

class TeamMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)  # User role (e.g., 'manager' or 'developer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    work_phone = models.CharField(max_length=15, blank=True, null=True, unique=True)

    class Meta:
        permissions = [
            ("manage_developers", "Can manage developer accounts"),
        ]
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return self.user.username

# Budget Model
class Budget(models.Model):
    name = models.CharField(max_length=100)
    income_amount = models.DecimalField(decimal_places=2, max_digits=10)
    expense_amount = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_amount(self):
        return self.income_amount - self.expense_amount

# Expense Category Model
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Payment Method Model
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Log Model
class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    action_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    related_id = models.PositiveIntegerField()

    def __str__(self):
        return f"Log {self.id} by {self.user.username} at {self.timestamp}"

# Settings Model
class Settings(models.Model):
    user = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, default='USD')
    default_view = models.CharField(max_length=50, default='list')
    notification_preference = models.CharField(max_length=50, default='email')

    def __str__(self):
        return f"Settings for {self.user.user.username}"

# User Category Model
class UserCategory(models.Model):
    user = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.username} - {self.category.name}"

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    user_category = models.ForeignKey(UserCategory, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.amount} on {self.transaction_date}"