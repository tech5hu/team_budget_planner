from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse
from .models import BudgetAndCategory, Transaction, TeamAndSetting, UserProfile
from .forms import (
    UserProfileCreationForm, BudgetForm, TransactionForm,
    ReportFilterForm, UserProfileForm, CustomPasswordChangeForm, TeamSettingsForm
)

# Helper functions to check user roles
def is_admin(user):
    return user.is_superuser

def is_regular_user(user):
    return not is_admin(user)

# Handle user registration
def register_view(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='regular')  # Default to 'regular'
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('budgets:dashboard')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = UserProfileCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Handle user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']  # This field collects only the username
        password = request.POST['password']
        
        # Authenticate by username
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('budgets:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            print("Authentication failed")  # Debug line for troubleshooting
            
    return render(request, 'login.html')
    
# Handle user logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('budgets:home')

# Home view for the main page after login
@login_required
def home(request):
    return render(request, 'budgets/home.html')

# Dashboard view
@login_required
def dashboard_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    budgets = BudgetAndCategory.objects.filter(user_profile=user_profile)
    transactions = Transaction.objects.filter(user_profile=user_profile)
    
    expense_breakdown = transactions.filter(transaction_type='expense')\
        .values('expense_category__expense_category').annotate(total_amount=Sum('amount'))

    recent_transactions = transactions.order_by('-transaction_date')[:3]

    total_income = budgets.aggregate(Sum('income_amount'))['income_amount__sum'] or 0
    total_expense = budgets.aggregate(Sum('expense_amount'))['expense_amount__sum'] or 0
    remaining_budget = total_income - total_expense

    budget_summary = {
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_budget': remaining_budget,
    }

    return render(request, 'budgets/dashboard.html', {
        'budgets': budgets,
        'expense_breakdown': expense_breakdown,
        'recent_transactions': recent_transactions,
        'budget_summary': budget_summary,
    })

# List all budgets for the current user
@login_required
def budgets_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    budgets = BudgetAndCategory.objects.filter(user_profile=user_profile)
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

# View to manage the budget form
@login_required
def budget_form_view(request, budget_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if budget_id:
        budget = get_object_or_404(BudgetAndCategory, id=budget_id, user_profile=user_profile)
    else:
        budget = BudgetAndCategory(user_profile=user_profile)

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget saved successfully.')
            return redirect('budgets:budgets_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BudgetForm(instance=budget)

    if is_admin(request.user) or budget.user_profile == user_profile:
        return render(request, 'budgets/budget_form.html', {'form': form, 'budget': budget})
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
def budget_info_view(request, budget_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    budget = get_object_or_404(BudgetAndCategory, id=budget_id, user_profile=user_profile)
    return render(request, 'budgets/budget_info.html', {'budget': budget})

@login_required
def budget_delete_view(request, budget_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    budget = get_object_or_404(BudgetAndCategory, id=budget_id, user_profile=user_profile)
    
    if is_admin(request.user):
        if request.method == 'POST':
            budget.delete()
            messages.success(request, 'Budget deleted successfully.')
            return redirect('budgets:budgets_list')
        return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})
    else:
        return HttpResponseForbidden("You do not have permission to delete this budget.")

# List all transactions for the current user
@login_required
def transactions_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    transactions = Transaction.objects.filter(user_profile=user_profile)
    return render(request, 'budgets/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_form_view(request, transaction_id=None):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if transaction_id:
        transaction = get_object_or_404(Transaction, id=transaction_id, user_profile=user_profile)
        is_editing = True
    else:
        transaction = None
        is_editing = False

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user_profile = user_profile
            transaction.save()
            messages.success(request, 'Transaction saved successfully.')
            return redirect('budgets:transactions_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'budgets/transaction_form.html', {
        'form': form, 
        'transaction': transaction, 
        'is_editing': is_editing
    })

@login_required
def transaction_info_view(request, transaction_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    transaction = get_object_or_404(Transaction, id=transaction_id, user_profile=user_profile)
    return render(request, 'budgets/transaction_info.html', {'transaction': transaction})

@login_required
def transaction_delete_view(request, transaction_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    transaction = get_object_or_404(Transaction, id=transaction_id, user_profile=user_profile)
    if is_admin(request.user) or transaction.user_profile == user_profile:
        if request.method == 'POST':
            transaction.delete()
            messages.success(request, 'Transaction deleted successfully.')
            return redirect('budgets:transactions_list')
        return render(request, 'budgets/transaction_confirm_delete.html', {'transaction': transaction})
    else:
        return HttpResponseForbidden("You do not have permission to delete this transaction.")

# Display the profile of the current user
@login_required
def profile_view(request):
    user = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('budgets:profile')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'account_level': user.role,
        'team': user.team,
        'number': user.work_phone,
        'read_only': is_regular_user(request.user),
    }
    
    return render(request, 'budgets/profile.html', context)

@login_required
def recent_budgets(request):
    recent_budgets = BudgetAndCategory.objects.filter(user_profile=request.user.userprofile).order_by('-created_at')[:10]
    return render(request, 'budgets/recent_budgets.html', {'recent_budgets': recent_budgets})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user_profile = get_object_or_404(UserProfile, user=request.user)
            transaction.save()
            messages.success(request, 'Transaction added successfully.')
            return redirect('budgets:transactions_list')
    else:
        form = TransactionForm()
    return render(request, 'budgets/add_transaction.html', {'form': form})

@login_required
def manage_team_and_settings(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Admins can manage team settings
    if is_admin(request.user):
        team_settings = get_object_or_404(TeamAndSetting, team=user_profile.team)
        if request.method == 'POST':
            form = TeamSettingsForm(request.POST, instance=team_settings)
            if form.is_valid():
                form.save()
                messages.success(request, 'Team settings updated successfully.')
                return redirect('budgets:manage_team_and_settings')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = TeamSettingsForm(instance=team_settings)
        
        return render(request, 'budgets/manage_team_and_settings.html', {'form': form, 'team_settings': team_settings})
    else:
        return HttpResponseForbidden("You do not have permission to manage team settings.")

@login_required
def generate_report_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    transactions = Transaction.objects.filter(user_profile=user_profile)

    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data['category']

            if start_date:
                transactions = transactions.filter(transaction_date__gte=start_date)
            if end_date:
                transactions = transactions.filter(transaction_date__lte=end_date)
            if category:
                transactions = transactions.filter(expense_category__expense_category=category)
    else:
        form = ReportFilterForm()

    total_amount = transactions.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'budgets/generate_report.html', {
        'form': form,
        'transactions': transactions,
        'total_amount': total_amount,
    })

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('budgets:settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'budgets/settings.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('budgets:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('budgets:home')
    return HttpResponseForbidden()  # Prevent GET requests

@login_required
def update_notifications(request):
    if request.method == 'POST':
        # Logic to update notification settings
        email_notifications = 'email_notifications' in request.POST
        sms_notifications = 'sms_notifications' in request.POST
        request.user.userprofile.email_notifications = email_notifications
        request.user.userprofile.sms_notifications = sms_notifications
        request.user.userprofile.save()
        messages.success(request, 'Notification settings updated successfully.')
        return redirect('budgets:settings')
    return HttpResponse(status=405)  # Method not allowed for non-POST requests

@login_required
def team_settings_view(request):
    try:
        user_profile = request.user.userprofile
        team_settings = TeamAndSetting.objects.filter(user=user_profile)
    except UserProfile.DoesNotExist:
        team_settings = []  # or handle it in another way, e.g., redirect or create a profile
        # You could also create a new profile here if needed
    
    return render(request, 'budgets/team_settings.html', {'team_settings': team_settings})

@login_required
def add_team_setting(request):
    if request.method == 'POST':
        form = TeamSettingsForm(request.POST)
        if form.is_valid():
            team_setting = form.save(commit=False)
            team_setting.user = request.user
            team_setting.save()
            messages.success(request, 'Team setting added successfully.')
            return redirect('budgets:team_settings')
    else:
        form = TeamSettingsForm()
    
    return render(request, 'budgets/add_team_setting.html', {'form': form})

@login_required
def user_list_view(request):
    users = UserProfile.objects.all()
    return render(request, 'budgets/user_list.html', {'users': users})

@login_required
def promote_user_view(request, user_id):
    user_to_promote = get_object_or_404(UserProfile, id=user_id)
    
    if is_admin(request.user):
        user_to_promote.role = 'admin'  # Or whatever designation you want
        user_to_promote.save()
        messages.success(request, f'User {user_to_promote.user.username} promoted to manager.')
        return redirect('budgets:user_list')  # Redirect to the user list
    else:
        return HttpResponseForbidden("You do not have permission to promote users.")        
