# Generated by Django 4.1.5 on 2023-07-30 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_employmenttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='employment_type_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.employmenttype'),
        ),
    ]
