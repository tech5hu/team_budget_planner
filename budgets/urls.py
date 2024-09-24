from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import generate_report_view, settings_view

app_name = 'budgets'

urlpatterns = [
    # Home and user authentication
    path('', views.home, name='home'),  # Home page
    path('register/', views.register_view, name='register'),  # User registration page
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # User login page
    path('logout/', views.logout_view, name='logout'),  # User logout action
    
    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # Password reset request page
    path('password_reset/sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_sent'),  # Password reset email sent confirmation
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Password reset confirmation page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Password reset complete confirmation

    # User profile and dashboard
    path('profile/', views.profile_view, name='profile'),  # User profile page
    path('dashboard/', views.dashboard_view, name='dashboard'),  # User dashboard

    # Budget management
    path('budgets/', views.budgets_list, name='budgets_list'),  # List of budgets
    path('budgets/new/', views.budget_form_view, name='budget_form'),  # Create new budget form
    path('budgets/edit/<int:budget_id>/', views.budget_form_view, name='budget_edit'),  # Edit existing budget form
    path('budgets/<int:budget_id>/', views.budget_info_view, name='budget_info'),  # View budget details
    path('budgets/delete/<int:budget_id>/', views.budget_delete_view, name='budget_delete'),  # Delete budget action
    path('recent-budgets/', views.recent_budgets, name='recent_budgets'),  # View recent budgets

    # Transaction management
    path('transactions/', views.transactions_list, name='transactions_list'),  # List of transactions
    path('transactions/new/', views.transaction_form_view, name='transaction_form'),  # Create new transaction form
    path('transactions/edit/<int:transaction_id>/', views.transaction_form_view, name='transaction_edit'),  # Edit existing transaction form
    path('transactions/<int:transaction_id>/', views.transaction_info_view, name='transaction_info'),  # View transaction details
    path('transactions/delete/<int:transaction_id>/', views.transaction_delete_view, name='transaction_delete'),  # Delete transaction action

    # Other features
    path('add-transaction/', views.add_transaction, name='add_transaction'),  # Add transaction action
    path('settings/', settings_view, name='settings'),  # User settings page
    path('generate-report/', generate_report_view, name='generate_report'),  # Generate financial report
]
