# Generated by Django 4.1.5 on 2023-08-24 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_alter_joboffer_created_alter_joboffer_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
