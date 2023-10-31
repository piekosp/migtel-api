# Generated by Django 4.1.5 on 2023-08-14 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_polishclassificationofactivities_industry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='krs',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='phone'),
        ),
    ]