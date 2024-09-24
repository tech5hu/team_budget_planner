from django.apps import AppConfig  # Importing AppConfig to configure the application

class BudgetsConfig(AppConfig):
    # Configuration for the Budgets application
    default_auto_field = 'django.db.models.BigAutoField'  # Default field type for auto-generated primary keys
    name = 'budgets'  # Name of the application

    def ready(self):
        # Method called when the application is ready
        import budgets.signals  # Importing signals to ensure they are registered
