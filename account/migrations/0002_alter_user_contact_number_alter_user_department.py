# Generated by Django 5.1.2 on 2024-11-06 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(choices=[('', 'Select'), ('bca', 'BCA'), ('bit', 'BIT')], default='bca', max_length=10),
        ),
    ]