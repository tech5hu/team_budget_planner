# Generated by Django 5.1 on 2024-09-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('budgets', '0005_alter_userprofile_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='auth.permission'),
        ),
    ]
