from django.contrib import admin
from .models import Transaction, BudgetAndCategory, UserProfile, TeamAndSetting

class CustomAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion if the user is an admin
        return request.user.is_superuser or (request.user.userprofile.role == 'admin')

@admin.register(Transaction)
class TransactionAdmin(CustomAdmin):
    list_display = ('budget', 'user_profile', 'expense_category', 'amount', 'transaction_date', 'payment_method', 'description', 'transaction_type')

@admin.register(BudgetAndCategory)
class BudgetAndCategoryAdmin(CustomAdmin):
    list_display = ['id', 'budget_name', 'income_amount', 'expense_amount', 'expense_category', 'payment_method', 'created_at', 'updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(CustomAdmin):
    list_display = ['id', 'username', 'email', 'created_at', 'updated_at']

@admin.register(TeamAndSetting)
class TeamAndSettingAdmin(CustomAdmin):
    list_display = ['id', 'team_name', 'user', 'currency', 'communication_preference', 'role', 'work_phone', 'created_at', 'updated_at']
