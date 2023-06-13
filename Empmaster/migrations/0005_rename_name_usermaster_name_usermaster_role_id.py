# Generated by Django 4.0.6 on 2022-10-28 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empmaster', '0004_usermaster'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermaster',
            old_name='name',
            new_name='Name',
        ),
        migrations.AddField(
            model_name='usermaster',
            name='role_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Empmaster.role'),
        ),
    ]