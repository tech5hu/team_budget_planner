from django.contrib import admin
from .models import TeamMember, Budget, ExpenseCategory, Transaction, Log, Settings, UserCategory, PaymentMethod

# User Admin configuration
class TeamMemberAdmin(admin.ModelAdmin):
    model = TeamMember
    list_display = ('get_email', 'role', 'team')  # Removed 'profile_picture'
    list_filter = ('role', 'team')
    fieldsets = (
        (None, {'fields': ('user', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'team')}),  # Removed 'profile_picture'
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'password1', 'password2', 'role', 'team'),
        }),
    )
    search_fields = ('user__email', 'role')  # Use related user email for search
    ordering = ('user__email',)  # Use related user email for ordering

    def get_email(self, obj):
        return obj.user.email  # Assuming TeamMember has a OneToOne or ForeignKey to User
    get_email.short_description = 'Email'  # Display name in the admin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'manager':
            return qs
        return qs.filter(role='developer')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'manager':
            return True
        if obj and obj.role == 'developer':
            return obj == request.user
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'manager':
            return True
        return False

# Registering the custom user admin
admin.site.register(TeamMember, TeamMemberAdmin)

# Register other models
admin.site.register(Budget)
admin.site.register(Log)
admin.site.register(Settings)

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def delete_selected_expense_categories(self, request, queryset):
        if request.user.is_superuser:
            queryset.delete()
        else:
            self.message_user(request, "You do not have permission to perform this action.", level='error')

    delete_selected_expense_categories.short_description = 'Delete selected expense categories'
    actions = [delete_selected_expense_categories]

@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    search_fields = ('user__email', 'category__name')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'expense_category', 'amount', 'description')
    search_fields = ('description', 'expense_category__name', 'amount')
