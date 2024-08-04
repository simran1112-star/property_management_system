# Generated by Django 4.1 on 2023-03-04 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('contact_no', models.CharField(max_length=10, null=True)),
                ('subject', models.TextField(default='')),
                ('message', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_id', models.CharField(blank=True, max_length=60, null=True)),
                ('property_sr', models.CharField(blank=True, max_length=60, null=True)),
                ('property_type', models.CharField(blank=True, max_length=60, null=True)),
                ('property_address', models.CharField(blank=True, max_length=400, null=True)),
                ('property_city', models.CharField(blank=True, max_length=60, null=True)),
                ('property_state', models.CharField(blank=True, max_length=60, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('total_bedrooms', models.CharField(blank=True, max_length=60, null=True)),
                ('total_bathrooms', models.CharField(blank=True, max_length=60, null=True)),
                ('total_balconies', models.CharField(blank=True, max_length=60, null=True)),
                ('area_details', models.CharField(blank=True, max_length=60, null=True)),
                ('furnishing_type', models.CharField(blank=True, max_length=60, null=True)),
                ('open_parking', models.IntegerField(blank=True, null=True)),
                ('covered_parking', models.IntegerField(blank=True, null=True)),
                ('availability_status', models.CharField(blank=True, max_length=60, null=True)),
                ('property_age', models.CharField(blank=True, max_length=60, null=True)),
                ('property_ownership', models.CharField(blank=True, max_length=60, null=True)),
                ('property_expected_price', models.FloatField(default=0.0)),
                ('property_area_price', models.FloatField(default=0.0)),
                ('property_amenities', models.TextField(blank=True, null=True)),
                ('property_unique_details', models.TextField(blank=True, null=True)),
                ('approval_status', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(blank=True, null=True)),
                ('property_listed', models.BooleanField(default=False)),
                ('property_unlisted_date', models.DateTimeField(blank=True, null=True)),
                ('membership_required_for_listening', models.BooleanField(default=False)),
                ('property_membership_purchased', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image', models.ImageField(upload_to='registed_user_images/')),
                ('contact', models.CharField(max_length=10)),
                ('user_type', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_membership_plan', models.BooleanField(default=False)),
                ('property_membership_amount', models.FloatField(blank=True, default=0.0, null=True)),
                ('payment_order_id', models.CharField(blank=True, max_length=60, null=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_membership', to='pms.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_membership_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='property_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_images', to='pms.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('email', models.CharField(blank=True, max_length=60, null=True)),
                ('contact', models.CharField(blank=True, max_length=10, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_contacts', to='pms.property')),
            ],
        ),
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(blank=True, max_length=255, null=True)),
                ('blog_body', models.TextField(blank=True, max_length=10000, null=True)),
                ('blog_image', models.ImageField(upload_to='blog_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
