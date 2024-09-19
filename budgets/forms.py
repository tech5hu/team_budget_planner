from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import CustomUserModel, TeamMember, Budget, Transaction, UserCategory, ExpenseCategory, PaymentMethod, Team

class TeamMemberCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)  # Keep username required
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = CustomUserModel
        fields = ('username', 'email', 'password1', 'password2')  # Username included
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

# Budget Form
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'income_amount', 'expense_amount']

# Transaction Form
class TransactionForm(forms.ModelForm):
    user_category = forms.ModelChoiceField(
        queryset=UserCategory.objects.all(), 
        empty_label="Select User Category", 
        required=True
    )
    
    expense_category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(), 
        empty_label="Select Expense Category", 
        required=True
    )
    
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(), 
        empty_label="Select Payment Method", 
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
    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all(), required=False)

# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['role', 'team', 'work_phone']

# Custom Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'account_level', 'team', 'work_phone']
        widgets = {
            'account_level': forms.TextInput(attrs={'readonly': 'readonly'}),
            'team': forms.TextInput(attrs={'readonly': 'readonly'}),
            'work_phone': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Apply read-only settings based on user role
        if user:
            if user.role != 'manager':
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'
            # Generate a random phone number if not set
            if not self.instance.work_phone:
                self.instance.work_phone = self.generate_random_phone_number()

    def generate_random_phone_number(self):
        import random
        return f'{random.randint(1000000000, 9999999999)}'