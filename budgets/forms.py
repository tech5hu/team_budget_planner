from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import UserProfile, BudgetAndCategory, TeamAndSetting, Transaction, ExpenseCategory, User
from django.core.exceptions import ValidationError
import re

# User profile creation form with role and account level choices
class UserProfileCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
        ('admin', 'Admin'),
        ('regular', 'Regular User'),
    ], required=True)

    account_level = forms.ChoiceField(choices=[
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    ], required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'account_level', 'password1', 'password2')

    # Validate email uniqueness and format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Enter a valid email address.")
        return email

    # Validate username uniqueness and format
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
            raise ValidationError("Username can only contain letters, numbers, dots, and underscores.")
        if len(username) < 3 or len(username) > 150:
            raise ValidationError("Username must be between 3 and 150 characters.")
        return username

    # Save the user and set is_staff attribute
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        user.is_staff = True

        if commit:
            user.email = email
            user.save()

        return user

# Form for creating or updating budgets
class BudgetForm(forms.ModelForm):
    class Meta:
        model = BudgetAndCategory
        fields = ['budget_name', 'income_amount', 'expense_amount', 'expense_category']

    expense_category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        empty_label="Select an Expense Category",
        label="Expense Category"
    )

    budget_name = forms.ModelChoiceField(
        queryset=BudgetAndCategory.objects.all(),
        empty_label="Select Budget",
        required=True,
        label="Budget"
    )

# Form for creating transactions
class TransactionForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('', 'Choose a Payment Method'),  # Empty choice for the dropdown
        ('Corporate Credit Card', 'Corporate Credit Card'),
        ('Company Expense Report', 'Company Expense Report'),
        ('Direct Bank Transfer', 'Direct Bank Transfer'),
        ('Reimbursement Request', 'Reimbursement Request'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('', 'Choose an Option'),  # Empty choice for the dropdown
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    # Define fields for the transaction form
    expense_category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        empty_label="Choose an Expense Category",
        required=True,
    )

    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Transaction Date"
    )

    class Meta:
        model = Transaction
        fields = ['budget', 'amount', 'expense_category', 'transaction_date', 'payment_method', 'description', 'transaction_type']

    budget = forms.ModelChoiceField(
        queryset=BudgetAndCategory.objects.all(),
        empty_label="Select Budget",
        required=True,
        label="Budget"
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        required=True,
        label="Payment Method"
    )

    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        required=True,
        label="Transaction Type"
    )

# Form for filtering reports based on date and category
class ReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        empty_label="Select an Expense Category",
        required=False
    )

# Form for updating user profile information
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'team', 'work_phone']

# Custom password change form with additional validation
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        
        if self.user.check_password(new_password1):
            raise ValidationError("The new password cannot be the same as the old password.")
        
        if len(new_password1) < 8:
            raise ValidationError("The new password must be at least 8 characters long.")

        return new_password1

    def clean(self):
        super().clean()
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("The two password fields must match.")

# Form for user profile management
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'team', 'work_phone']
        widgets = {
            'team': forms.TextInput(attrs={'readonly': 'readonly'}),
            'work_phone': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Make fields readonly for non-managers
        if user:
            if user.role != 'manager':
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

# Form for team settings management
class TeamSettingsForm(forms.ModelForm):
    class Meta:
        model = TeamAndSetting
        fields = ['team_name', 'currency', 'communication_preference', 'role', 'work_phone']

    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    account_level = forms.ChoiceField(choices=[
        ('developer', 'Developer'),
        ('manager', 'Manager'),
    ], required=True)

    # Validate email uniqueness and format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Enter a valid email address.")
        return email

    # Validate username uniqueness and format
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
            raise ValidationError("Username can only contain letters, numbers, dots, and underscores.")
        if len(username) < 3 or len(username) > 150:
            raise ValidationError("Username must be between 3 and 150 characters.")
        return username

    # Validate that passwords match
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

    # Save user and profile information
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username'],
                role=self.cleaned_data['role']
            )
        return user
