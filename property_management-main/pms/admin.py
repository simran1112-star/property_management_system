from django.contrib import admin
from pms.models import UserProfile, Blogs, Property, PropertyImages, \
    PropertyMembership, PropertyContacts, Contact,Location

admin.site.register(UserProfile)
admin.site.register(Blogs)
admin.site.register(Property)
admin.site.register(PropertyImages)
admin.site.register(PropertyMembership)
admin.site.register(PropertyContacts)
admin.site.register(Contact)
admin.site.register(Location)
