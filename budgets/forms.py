from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import UserProfile, BudgetAndCategory, TeamAndSetting, Transaction

class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

# Budget Form
class BudgetForm(forms.ModelForm):
    class Meta:
        model = BudgetAndCategory
        fields = ['budget_name', 'income_amount', 'expense_amount', 'expense_category']

# Transaction Form
class TransactionForm(forms.ModelForm):
    user_category = forms.ModelChoiceField(
        queryset=UserProfile.objects.all(), 
        empty_label="Select User Category", 
        required=True
    )
    
    expense_category = forms.ModelChoiceField(
        queryset=BudgetAndCategory.objects.all(), 
        empty_label="Select Expense Category", 
        required=True
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('personal_debit_card', 'Personal Debit Card'),
            ('cash', 'Cash'),
            ('company_voucher', 'Company Voucher'),
            ('company_credit_card', 'Company Credit Card'),
        ],
        required=True
    )

    class Meta:
        model = Transaction
        fields = ['budget', 'user_category', 'expense_category', 'amount', 'transaction_date', 'payment_method', 'description']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Report Filter Form
class ReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'team', 'work_phone']

# Custom Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    pass  # No need for a Meta class here

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'team', 'work_phone']
        widgets = {
            'team': forms.TextInput(attrs={'readonly': 'readonly'}),
            'work_phone': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        if user:
            if user.role != 'manager':
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'
            if not self.instance.work_phone:
                self.instance.work_phone = self.generate_random_phone_number()

    def generate_random_phone_number(self):
        import random
        return f'{random.randint(1000000000, 9999999999)}'

class TeamSettingsForm(forms.ModelForm):
    class Meta:
        model = TeamAndSetting
        fields = ['team_name', 'currency', 'communication_preference', 'role', 'work_phone']
