# Generated by Django 4.0.4 on 2022-07-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_alter_customer_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='emailLinkExpireTime',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
