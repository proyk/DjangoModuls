# Generated by Django 4.0.4 on 2022-06-24 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_alter_customerinformation_customergroup_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='city',
            fields=[
                ('cityId', models.AutoField(primary_key=True, serialize=False)),
                ('cityName', models.CharField(max_length=24, unique=True, verbose_name='City Name')),
            ],
        ),
        migrations.CreateModel(
            name='customerAddress',
            fields=[
                ('customerAddressId', models.AutoField(primary_key=True, serialize=False)),
                ('addressName', models.CharField(max_length=100, verbose_name='Name')),
                ('building', models.CharField(max_length=200, verbose_name='Building / House No.')),
                ('street', models.CharField(max_length=200, verbose_name='Street')),
                ('postalCode', models.IntegerField(verbose_name='Postal Code')),
                ('landMark', models.CharField(max_length=200, verbose_name='Landmark')),
                ('isDefault', models.BooleanField(default=False, verbose_name='Is Default')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.city')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='state',
            fields=[
                ('stateId', models.AutoField(primary_key=True, serialize=False)),
                ('stateName', models.CharField(max_length=24, unique=True, verbose_name='State Name')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomerInformation',
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.state'),
        ),
        migrations.AddField(
            model_name='city',
            name='stateName',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.state'),
        ),
    ]
