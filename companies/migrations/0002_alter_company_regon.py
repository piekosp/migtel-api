# Generated by Django 4.1.5 on 2023-07-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='regon',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
