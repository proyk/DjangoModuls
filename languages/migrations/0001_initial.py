# Generated by Django 4.0.4 on 2022-05-27 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='language',
            fields=[
                ('title', models.CharField(max_length=50)),
                ('locale', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('isDefault', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=10)),
            ],
        ),
    ]
