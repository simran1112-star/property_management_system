# Generated by Django 5.0.2 on 2024-04-15 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0002_rename_property_address_property_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=2)),
                ('postal_code', models.CharField(max_length=10)),
                ('city_name', models.CharField(max_length=100)),
                ('state_name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]
