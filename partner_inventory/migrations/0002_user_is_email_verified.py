# Generated by Django 4.0.4 on 2022-06-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False, verbose_name='email verification status'),
        ),
    ]
