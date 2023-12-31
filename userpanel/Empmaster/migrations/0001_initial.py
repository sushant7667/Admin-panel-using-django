# Generated by Django 4.0.6 on 2022-10-28 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='countrymodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='statemodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=50, null=True)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empmaster.countrymodel')),
            ],
        ),
        migrations.CreateModel(
            name='useremp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=255, null=True)),
                ('Lastname', models.CharField(max_length=255, null=True)),
                ('mobile_no', models.CharField(max_length=255, null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=50)),
                ('email', models.CharField(max_length=255, null=True, unique=True)),
                ('isactive', models.BooleanField(default=True)),
                ('countryId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Empmaster.countrymodel')),
                ('stateId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Empmaster.statemodel')),
            ],
        ),
    ]
