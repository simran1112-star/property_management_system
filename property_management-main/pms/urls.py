from django.urls import path, reverse_lazy
from pms import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),

    # About Us
    path('about/', views.about, name='about'),
    path('get_cities/', views.get_cities, name='get_cities'),
    path('get_zip_codes/', views.get_zip_codes, name='get_zip_codes'),


    # All Properties
    path('all-properties/', views.all_properties, name='all_properties'),

    # Particular Property Detail
    path('property-detail/<int:id>/',
         views.property_details, name='property_details'),

    # Contact Page
    path('contact/', views.contact_us, name='contact'),

    # Blogs (Home Page)
    path('blogs/', views.blog, name='blogs'),
    path('blog/<int:id>/', views.blog_description, name='blog_description'),

    # Login Page
    path('login/', views.auth_login, name='login'),

    # Logout
    path('logout/', views.user_logout, name='logout'),

    # Register Page
    path('register/', views.auth_register, name='register'),

    # Profile Page
    path('profile/', views.profile, name='profile'),

    # Forgot/Reset Password
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='reset/password_reset.html',
                                                                  email_template_name='reset/password_reset_email.html',
                                                                  success_url=reverse_lazy('password_reset_done')),
         name='forgot_password_url'),

    path('forgot-password/sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='reset/password_reset_done.html'),  name='password_reset_done'),

    path('forgot-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_form.html',
         success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),

    path('forgot-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset/password_reset_complete.html'), name='password_reset_complete'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view/user-image/<int:id>/',
         views.view_user_image, name='view_user_image'),

    # Blogs CRUD
    path('add-new-blog/', views.add_new_blog, name='new_blog'),
    path('blog-list/', views.view_blogs_list, name='blog_list'),
    path('update/blog/<int:id>/', views.update_blog, name='update_blog'),
    path('delete/blog/<int:id>/', views.delete_blog, name='delete_blog'),

    # Property Operations
    path('add-new-property/', views.add_new_property, name='new_property'),
    path('properties/', views.list_uploaded_properties, name='property_list'),
    path('update/property/<int:id>/',
         views.update_property, name='update_property'),
    path('delete/property/<int:id>/',
         views.delete_property, name='delete_property'),
    path('view/property-details/<int:id>/<view>/',
         views.update_property, name='view_property'),
    path('view/property-images/<int:id>/',
         views.view_property_images, name='view_property_images'),
    path('approve-property/<int:id>/',
         views.approve_property, name='approve_property'),
    path('listed-properties/', views.listed_properties_view,
         name='listed_properties'),
    path('unlisted-properties/', views.unlisted_properties_view,
         name='unlisted_properties'),
    path('unlisted-property/<int:id>/',
         views.unlist_property, name='unlist_property'),
    path('property-contact/<int:id>/',
         views.property_comments, name='property_comments'),
    path('pending-properties/', views.pending_properties_view,
         name='pending_properties'),
    path('property-responses/<int:id>/',
         views.list_property_contacts, name='list_property_contacts'),
    path('membership-payment-success/<int:id>/',
         views.payment_success_membership, name='payment_success_membership'),
    path('properties-list/user/', views.properties_uploaded_by_user,
         name='properties_uploaded_by_user'),

    # EMI Calculator
    path('emi-calculator/', views.calculate_emi, name='emi_calculator'),

    # Reports Section
    path('agents-list/', views.agents_list_view, name='agents_list'),
    path('customers-list/', views.customers_list_view, name='customers_list_view'),
    path('total-uploaded-properties/', views.total_uploaded_properties,
         name='total_uploaded_properties'),
    path('total-listed-properties/', views.total_listed_properties,
         name='total_listed_properties'),
    path('total-unlisted-properties/', views.total_unlisted_properties,
         name='total_unlisted_properties'),
    path('revenue-details/', views.revenue_details, name='revenue_details'),

]
