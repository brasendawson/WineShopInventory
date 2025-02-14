# Generated by Django 5.1.2 on 2025-02-13 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0002_rename_employee_drink_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='date_published'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='category',
            field=models.CharField(choices=[('Champagne', 'Champagne'), ('Rose', 'Rose'), ('Wine', 'Wine'), ('Vodka', 'Vodka'), ('Whiskey', 'Whiskey'), ('Cognac', 'Cognac')], max_length=50),
        ),
    ]
