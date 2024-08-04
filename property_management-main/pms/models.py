from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user_image = models.ImageField(upload_to='registed_user_images/')
    contact = models.CharField(max_length=10, null=False, blank=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile")
    user_type = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.user.username)


class Blogs(models.Model):
    blog_title = models.CharField(max_length=255, null=True, blank=True)
    blog_body = models.TextField(max_length=10000, null=True, blank=True)
    blog_image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogs_user')

    def __str__(self):
        return (self.blog_title)


class Property(models.Model):
    property_id = models.CharField(max_length=60, null=True, blank=True)
    sell_rent = models.CharField(max_length=60, null=True, blank=True)
    type = models.CharField(max_length=60, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=60, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    bedrooms = models.CharField(max_length=60, null=True, blank=True)
    bathrooms = models.CharField(max_length=60, null=True, blank=True)
    balconies = models.CharField(max_length=60, null=True, blank=True)
    area = models.CharField(max_length=60, null=True, blank=True)
    furnishing = models.CharField(max_length=60, null=True, blank=True)
    open_parking = models.IntegerField(null=True, blank=True)
    covered_parking = models.IntegerField(null=True, blank=True)
    availability = models.CharField(
        max_length=60, null=True, blank=True)
    age = models.CharField(max_length=60, null=True, blank=True)
    ownership = models.CharField(max_length=60, null=True, blank=True)
    expected_price = models.FloatField(default=0.0)
    area_price = models.FloatField(default=0.0)
    amenities = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    approved_on = models.DateTimeField(null=True, blank=True)
    is_listed = models.BooleanField(default=False)
    unlisted_date = models.DateTimeField(null=True, blank=True)
    membership_required = models.BooleanField(default=False)
    membership_purchased = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='property_user')

    def __str__(self):
        return f"{self.property_id}: {self.type}"


class PropertyContacts(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='property_contacts')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.property_id}:  {self.email}"


class PropertyImages(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='property_images')
    images = models.ImageField(upload_to='property_images/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property.property_id


class PropertyMembership(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='property_membership')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='property_membership_user')
    property_membership_plan = models.BooleanField(default=False)
    property_membership_amount = models.FloatField(
        null=True, blank=True, default=0.0)
    payment_order_id = models.CharField(max_length=60, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.property_id


class Contact(models.Model):
    name = models.CharField(max_length=80, null=True)
    email = models.EmailField()
    contact_no = models.CharField(max_length=10, null=True)
    subject = models.TextField(default='')
    message = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email+" / "+(self.name)
    

from django.db import models

class Location(models.Model):
    country_code = models.CharField(max_length=2)  # Renamed from state_code
    postal_code = models.CharField(max_length=10)  # Renamed from dist_code
    city_name = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)  # Provide a default value for latitude
    longitude = models.FloatField(default=0.0)  # Provide a default value for longitude
    # Add other fields as needed


