# Generated by Django 5.1.2 on 2024-11-12 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customerprofile_department_sellerprofile_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_role',
            field=models.CharField(choices=[('customer', 'Customer'), ('seller', 'Seller'), ('both', 'Both')], default='seller', max_length=10),
        ),
    ]
