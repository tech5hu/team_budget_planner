from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import generate_report_view, settings_view
app_name = 'budgets'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('budgets/', views.budgets_list, name='budgets_list'),
    path('budgets/new/', views.budget_form_view, name='budget_form'),
    path('budgets/edit/<int:budget_id>/', views.budget_form_view, name='budget_edit'),
    path('budgets/<int:budget_id>/', views.budget_info_view, name='budget_info'),
    path('budgets/delete/<int:budget_id>/', views.budget_delete_view, name='budget_delete'),
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/new/', views.transaction_form_view, name='transaction_form'),
    path('transactions/edit/<int:transaction_id>/', views.transaction_form_view, name='transaction_edit'),
    path('transactions/<int:transaction_id>/', views.transaction_info_view, name='transaction_info'),
    path('transactions/delete/<int:transaction_id>/', views.transaction_delete_view, name='transaction_delete'),
    path('recent-budgets/', views.recent_budgets, name='recent_budgets'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('settings/', settings_view, name='settings'),
    path('generate-report/', generate_report_view, name='generate_report'),
    path('update-profile/', views.update_profile_view, name='update_profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('update-notifications/', views.update_notifications, name='update_notifications'),  # Add this line
    path('delete-account/', views.delete_account, name='delete_account'),  # Add this line
    path('logout/', views.logout_view, name='logout'),
]
