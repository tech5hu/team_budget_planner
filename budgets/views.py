from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.db.models import Sum
from django.http import HttpResponseForbidden
from .models import BudgetAndCategory, Transaction, UserProfile
from .forms import (
    UserProfileCreationForm, BudgetForm, TransactionForm,
    ReportFilterForm, UserProfileForm, PasswordChangeForm
)
import logging

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
            form.save()  # Save the User instance (signals handle the UserProfile creation)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to your login URL
    else:
        form = UserProfileCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Handle user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('budgets:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'budgets/login.html')  # Fixed template reference

# Handle user logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('budgets:home')

# Home view for the main page after login
@login_required
def home(request):
    return render(request, 'budgets/home.html')

logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from budgets.models import UserProfile, BudgetAndCategory, Transaction

@login_required
def dashboard_view(request):
    # Fetch all user profiles to get team data
    user_profiles = UserProfile.objects.all()  # Retrieve all user profiles

    # Fetch budgets and transactions for all users in the team
    budgets = BudgetAndCategory.objects.filter(user_profile__in=user_profiles)
    transactions = Transaction.objects.filter(user_profile__in=user_profiles)

    # Calculate total income and total expenses for the entire team
    total_income = budgets.aggregate(Sum('income_amount'))['income_amount__sum'] or 0
    total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = total_income - total_expense

    # Create a summary of the budget
    budget_summary = {
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_budget': remaining_budget,
    }

    # Get recent transactions for display
    recent_transactions = transactions.order_by('-transaction_date')[:3]

    # Prepare data for the expense breakdown pie chart
    expense_breakdown = transactions.values('expense_category__name').annotate(total_amount=Sum('amount')).order_by('-total_amount')

    # Render the dashboard template with the aggregated team data
    return render(request, 'budgets/dashboard.html', {
        'budgets': budgets,
        'recent_transactions': recent_transactions,
        'budget_summary': budget_summary,  # Pass the summary data
        'expense_breakdown': expense_breakdown,  # Pass expense breakdown data
    })


# List all budgets
@login_required
def budgets_list(request):
    budgets = BudgetAndCategory.objects.all()  # Show all budgets
    budget_names = {
        1: 'Monthly Cloud Service Subscription',
        2: 'Annual Software License Fees',
        3: 'Budget for Development Tool Licenses',
        4: 'Employee Training and Development Budget',
        5: 'Quarterly Server Maintenance Costs',
        6: 'Annual Network Equipment Purchases',
        7: 'Budget for Performance Testing Services',
        8: 'Monthly Subscription for Project Management Tools',
        9: 'Yearly Budget for Team Collaboration Tools',
        10: 'Annual Database License Renewal Fees'
    }
    context = {
        'budgets': budgets,
        'budget_names': budget_names
    }

    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

@login_required
def budget_form_view(request, budget_id=None):
    if budget_id:
        budget = get_object_or_404(BudgetAndCategory, id=budget_id)
    else:
        budget = BudgetAndCategory(user_profile=request.user.userprofile)  # Set user_profile here

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)  # Create instance without saving yet
            budget.user_profile = request.user.userprofile  # Ensure user_profile is set
            budget.save()  # Now save the instance
            messages.success(request, 'Budget saved successfully.')
            return redirect('budgets:budgets_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'budgets/budget_form.html', {'form': form, 'budget': budget})

@login_required
def budget_info_view(request, budget_id):
    budget = get_object_or_404(BudgetAndCategory, id=budget_id)
    remaining_amount = budget.income_amount - budget.expense_amount
    return render(request, 'budgets/budget_info.html', {
        'budget': budget,
        'remaining_amount': remaining_amount
    })

@login_required
def budget_delete_view(request, budget_id):
    budget = get_object_or_404(BudgetAndCategory, id=budget_id)

    if is_admin(request.user):  # Only allow admins to delete budgets
        # Clear any existing messages
        storage = get_messages(request)
        for _ in storage:  # This will clear the message queue
            pass

        if request.method == 'POST':
            budget.delete()
            messages.success(request, 'Budget deleted successfully.')
            return redirect('budgets:budget_list')

        return render(request, 'budgets/delete_budget_confirmation.html', {'budget': budget})

    else:
        return HttpResponseForbidden("You do not have permission to delete this budget.")

@login_required
def transactions_list(request):
    # Get all transactions
    transactions = Transaction.objects.all()  # Show all transactions

    # Group transactions by expense category
    grouped_transactions = (
        transactions
        .values('expense_category__name')
        .annotate(total_amount=Sum('amount'))
        .order_by('expense_category__name')
    )

    # Prepare a dictionary to hold transactions grouped by category
    categorised_transactions = {category['expense_category__name']: [] for category in grouped_transactions}

    # Populate the dictionary with transactions
    for transaction in transactions:
        categorised_transactions[transaction.expense_category.name].append(transaction)

    context = {
        'grouped_transactions': grouped_transactions,
        'categorised_transactions': categorised_transactions,
    }

    return render(request, 'budgets/transaction_list.html', context)

@login_required
def transaction_form_view(request, transaction_id=None):
    if transaction_id:
        transaction = get_object_or_404(Transaction, id=transaction_id)
        is_editing = True
    else:
        transaction = Transaction()
        is_editing = False

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user_profile = get_object_or_404(UserProfile, user=request.user)
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
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'budgets/transaction_info.html', {'transaction': transaction})

def is_admin(user):
    return user.userprofile.role == 'admin'  # Adjust this according to your UserProfile model

@login_required
def transaction_delete_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if is_admin(request.user):  # Only allow admins to delete transactions
        # Clear any existing messages
        storage = get_messages(request)
        for _ in storage:  # Consume and clear the message queue
            pass

        if request.method == 'POST':
            transaction.delete()
            messages.success(request, 'Transaction deleted successfully.')
            return redirect('budgets:transactions_list')
        
        return render(request, 'budgets/delete_transaction_confirmation.html', {'transaction': transaction})
    else:
        return HttpResponseForbidden("You do not have permission to delete this transaction.")


@login_required
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)  
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('budgets:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'account_level': user_profile.role,
        'team': user_profile.team,
        'number': user_profile.work_phone,
        'read_only': is_regular_user(request.user),
    }
    
    return render(request, 'budgets/profile.html', context)

@login_required
def recent_budgets(request):
    recent_budgets = BudgetAndCategory.objects.order_by('-created_at')[:10]  # Show recent budgets for all users
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
def generate_report_view(request):
    transactions = Transaction.objects.all()  # Allow access to all transactions

    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data.get('category')

            if start_date:
                transactions = transactions.filter(transaction_date__gte=start_date)
            if end_date:
                transactions = transactions.filter(transaction_date__lte=end_date)
            if category:
                transactions = transactions.filter(expense_category=category)
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
        # Handle user profile form submission
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        # Handle change password form submission
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        # Handle notification settings
        email_notifications = 'email_notifications' in request.POST
        sms_notifications = 'sms_notifications' in request.POST
        request.user.userprofile.email_notifications = email_notifications
        request.user.userprofile.sms_notifications = sms_notifications

        # Check for password change
        if 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('budgets:settings')

        # Check for user profile form validity
        if form.is_valid():
            form.save()  # Save user profile changes
            request.user.userprofile.save()  # Save notification changes
            messages.success(request, 'Settings updated successfully.')
            return redirect('budgets:settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user.userprofile)  # Ensure you're using the user profile instance
        password_form = PasswordChangeForm(user=request.user)  # Initialize the password form

    return render(request, 'budgets/settings.html', {
        'form': form,
        'password_form': password_form,  # Pass the password form to the template
    })
