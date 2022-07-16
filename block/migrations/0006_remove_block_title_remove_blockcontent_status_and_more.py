# Generated by Django 4.0.4 on 2022-07-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0005_remove_block_content_remove_block_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='title',
        ),
        migrations.RemoveField(
            model_name='blockcontent',
            name='status',
        ),
        migrations.AddField(
            model_name='block',
            name='status',
            field=models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=10),
        ),
        migrations.AddField(
            model_name='blockcontent',
            name='title',
            field=models.CharField(default=None, max_length=100),
        ),
    ]