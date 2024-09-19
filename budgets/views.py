from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Budget, Transaction, TeamMember, UserCategory, ExpenseCategory
from .forms import (
    TeamMemberCreationForm, BudgetForm, TransactionForm, ProfileUpdateForm,
    ReportFilterForm, UserProfileForm, CustomPasswordChangeForm
)
import uuid

# Handle user registration
def register_view(request):
    if request.method == 'POST':
        form = TeamMemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            TeamMember.objects.create(user=user)  # Create TeamMember profile
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('budgets:dashboard')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = TeamMemberCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard or another page
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


# Handle user logout
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('budgets:home')  # Redirect to the home page

# Home view for the main page after login
@login_required
def home(request):
    return render(request, 'budgets/home.html')  # Render the home page template

# Dashboard view
@login_required
def dashboard_view(request):
    # Get budgets for the current user
    budgets = Budget.objects.filter(user=request.user)
    
    # Get transactions related to the user's budgets
    transactions = Transaction.objects.filter(budget__in=budgets)

    # Data for Expense Breakdown (Pie Chart)
    expense_breakdown = transactions.filter(transaction_type='expense')\
        .values('expense_category__name').annotate(total_amount=Sum('amount'))

    # Data for Recent Transactions (Last 3 transactions for the current user)
    recent_transactions = transactions.order_by('-transaction_date')[:3]

    # Data for Budget Summary (Total income and total expenses for the current user's budgets)
    total_income = budgets.aggregate(Sum('income_amount'))['income_amount__sum'] or 0
    total_expense = budgets.aggregate(Sum('expense_amount'))['expense_amount__sum'] or 0
    remaining_budget = total_income - total_expense

    # Prepare data for the template
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
    budgets = Budget.objects.filter(user=request.user)  
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

@login_required
# View to manage the budget form
def budget_form_view(request, budget_id=None):
    if budget_id:
        # Edit an already existing budget
        budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    else:
        # Create a new budget
        budget = Budget(user=request.user)

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

    return render(request, 'budgets/budget_form.html', {'form': form, 'budget': budget})

@login_required
def budget_info_view(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    return render(request, 'budgets/budget_info.html', {'budget': budget})

@login_required
def budget_delete_view(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully.')
        return redirect('budgets:budgets_list')
    
    return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})

# List all transactions for the current user
@login_required
def transactions_list(request):
    # Fetch the TeamMember instance associated with the current user
    team_member = get_object_or_404(TeamMember, user=request.user)
    
    # Filter transactions based on the TeamMember instance
    transactions = Transaction.objects.filter(user_category__user=team_member)
    
    return render(request, 'budgets/transaction_list.html', {
    'transactions': transactions,
})

@login_required
def transaction_form_view(request, transaction_id=None):
    if transaction_id:
        # Edit an existing transaction
        transaction = get_object_or_404(Transaction, id=transaction_id)
        # Ensure the transaction belongs to the logged-in user
        if transaction.user_category.user != request.user:
            messages.error(request, "You do not have permission to edit this transaction.")
            return redirect('budgets:transactions_list')
        is_editing = True
    else:
        # Create a new transaction
        transaction = None
        is_editing = False

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            # Save the transaction with the current user
            transaction = form.save(commit=False)
            transaction.user_category = UserCategory.objects.filter(user=request.user).first()  # Adjust as needed
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
    transaction = get_object_or_404(Transaction, id=transaction_id, user_category__user=request.user)
    return render(request, 'budgets/transaction_info.html', {'transaction': transaction}) 

@login_required
def transaction_delete_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('budgets:transactions_list')
    
    return render(request, 'budgets/transaction_confirm_delete.html', {'transaction': transaction})    

# Display the profile of the current user
@login_required
def profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        if user.role == 'manager':
            form = UserProfileForm(request.POST, instance=user, user=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('budgets:profile')
        else:
            form = UserProfileForm(request.POST, instance=user, user=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('budgets:profile')
    else:
        form = UserProfileForm(instance=user, user=user)

    context = {
        'form': form,
        'account_level': user.account_level,
        'team': user.team,
        'number': user.work_phone,  # Directly get work_phone from user object
        'read_only': user.role != 'manager',
    }
    
    return render(request, 'budgets/profile.html', context)

@login_required
def recent_budgets(request):
    # Replace '-timestamp' with '-created_at'
    recent_budgets = Budget.objects.all().order_by('-created_at')[:10]
    return render(request, 'budgets/recent_budgets.html', {'recent_budgets': recent_budgets})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.team_member = request.user.teammember  # Assuming you have a one-to-one link
            transaction.save()
            return redirect('budgets:transactions_list')  # Redirect to transactions list or another page
    else:
        form = TransactionForm()
    return render(request, 'budgets/add_transaction.html', {'form': form})

@login_required
def manage_categories(request):
    categories = ExpenseCategory.objects.all()
    if request.method == 'POST':
        # Handle form submission to create/update/delete categories if needed
        # For simplicity, we'll assume you handle this part in the template or through another view
        pass
    return render(request, 'budgets/manage_categories.html', {'categories': categories})

@login_required
def generate_report_view(request):
    # Fetch the TeamMember instance associated with the current user
    team_member = get_object_or_404(TeamMember, user=request.user)

    transactions = Transaction.objects.filter(user_category__user=team_member)

    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data['category']

            # Apply filters
            if start_date:
                transactions = transactions.filter(transaction_date__gte=start_date)
            if end_date:
                transactions = transactions.filter(transaction_date__lte=end_date)
            if category:
                transactions = transactions.filter(expense_category=category)
    else:
        form = ReportFilterForm()

    # Calculate totals for the filtered transactions
    total_amount = transactions.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'budgets/generate_report.html', {
        'form': form,
        'transactions': transactions,
        'total_amount': total_amount,
    })

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Redirect to the settings page or any other page
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'budgets/settings.html', {'form': form})    

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('budgets:profile')  # Ensure this matches the URL name in urls.py
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'budgets/update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')  # Redirect to profile or another page
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def update_notifications(request):
    if request.method == 'POST':
        # Handle notification settings update
        pass
    return render(request, 'budgets/update_notifications.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Handle account deletion
        pass
    return render(request, 'budgets/delete_account.html')    

