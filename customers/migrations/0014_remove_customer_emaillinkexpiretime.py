# Generated by Django 4.0.4 on 2022-07-05 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_customer_emaillinkexpiretime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='emailLinkExpireTime',
        ),
    ]
