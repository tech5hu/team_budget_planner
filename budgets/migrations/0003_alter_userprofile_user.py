import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def set_user_id_to_null(apps, schema_editor):
    UserProfile = apps.get_model('budgets', 'UserProfile')
    UserProfile.objects.filter(user__isnull=False).update(user=None)

class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_userprofile_user'),
    ]

    operations = [
        migrations.RunPython(set_user_id_to_null),  # Add this line
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
