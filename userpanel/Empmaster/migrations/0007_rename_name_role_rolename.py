# Generated by Django 4.0.6 on 2022-11-01 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empmaster', '0006_usermaster_groups_usermaster_is_superuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='name',
            new_name='rolename',
        ),
    ]
