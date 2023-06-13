# Generated by Django 4.0.6 on 2022-11-08 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empmaster', '0008_menuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkbox', models.CharField(max_length=250, null=True)),
                ('Role_Id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Empmaster.role')),
            ],
        ),
    ]