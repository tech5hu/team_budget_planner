from django.contrib import admin  # Importing the Django admin module
from .models import Transaction, BudgetAndCategory, UserProfile, TeamAndSetting  # Importing models to be registered in admin

class CustomAdmin(admin.ModelAdmin):
    # Custom admin class to define common admin behaviors
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion if the user is an admin
        return request.user.is_superuser or (request.user.userprofile.role == 'admin')

# Registering Transaction model with the admin site
@admin.register(Transaction)
class TransactionAdmin(CustomAdmin):
    # Configuration for the Transaction admin interface
    search_fields = ['user_profile__username', 'description']  # Fields to search in the admin
    list_filter = ['expense_category', 'payment_method']  # Filters available on the right side
    list_display = (
        'budget', 
        'user_profile', 
        'expense_category', 
        'amount', 
        'transaction_date', 
        'payment_method', 
        'description', 
        'transaction_type'
    )  # Columns to display in the list view

# Registering BudgetAndCategory model with the admin site
@admin.register(BudgetAndCategory)
class BudgetAndCategoryAdmin(CustomAdmin):
    # Configuration for the BudgetAndCategory admin interface
    list_display = [
        'id', 
        'budget_name', 
        'income_amount', 
        'expense_amount', 
        'expense_category', 
        'payment_method', 
        'created_at', 
        'updated_at'
    ]  # Columns to display in the list view
    search_fields = ['budget_name', 'expense_category']  # Fields to search in the admin
    list_filter = ['expense_category']  # Filters available on the right side

# Registering UserProfile model with the admin site
@admin.register(UserProfile)
class UserProfileAdmin(CustomAdmin):
    # Configuration for the UserProfile admin interface
    list_display = ['user', 'account_level', 'role']  # Columns to display in the list view

# Registering TeamAndSetting model with the admin site
@admin.register(TeamAndSetting)
class TeamAndSettingAdmin(CustomAdmin):
    # Configuration for the TeamAndSetting admin interface
    list_display = [
        'id', 
        'team_name', 
        'user', 
        'currency', 
        'communication_preference', 
        'get_role', 
        'work_phone', 
        'created_at', 
        'updated_at'
    ]  # Columns to display in the list view
    search_fields = ['team_name', 'user__username', 'currency']  # Fields to search in the admin
    list_filter = ['currency']  # Filters available on the right side
    fields = ['team_name', 'user', 'currency', 'communication_preference', 'work_phone']  # Fields to be displayed in the edit form

    def get_role(self, obj):
        # Method to get the role of the user in a capitalized format
        return obj.user.userprofile.role.capitalize()  # Capitalize the role
    
    get_role.short_description = 'Role'  # Set a short description for the column
