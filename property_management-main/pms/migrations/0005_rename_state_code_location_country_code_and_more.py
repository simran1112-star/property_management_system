# Generated by Django 5.0.2 on 2024-04-15 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0004_rename_postal_code_location_dist_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='state_code',
            new_name='country_code',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='dist_code',
            new_name='postal_code',
        ),
        migrations.RemoveField(
            model_name='location',
            name='location',
        ),
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]