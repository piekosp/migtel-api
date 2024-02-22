# Generated by Django 4.1.5 on 2024-02-22 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0005_remove_phone_company_company_email1_company_email2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('criteria', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyStatus',
            fields=[
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='status', serialize=False, to='companies.company')),
                ('completed', models.BooleanField(default=False)),
                ('completed_on', models.DateField(null=True)),
                ('assigned_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]