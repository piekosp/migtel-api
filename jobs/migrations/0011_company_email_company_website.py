# Generated by Django 4.1.5 on 2023-08-14 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_alter_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
