# Generated by Django 4.0.4 on 2022-07-04 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_alter_customeraddress_isdefault'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=250, verbose_name='Password'),
        ),
    ]
