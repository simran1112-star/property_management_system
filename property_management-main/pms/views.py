import re
import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.db.models import Q
from operator import itemgetter
from django.core.paginator import Paginator
import datetime
from property_management_system.settings import razorpay_api_key, razorpay_api_secret_key
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum, Func, Count
from django.contrib.auth import login, logout, authenticate
from pms.send_mail import send_customise_mail
from django.db import models
from django.http import JsonResponse


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import Property, PropertyMembership, PropertyContacts
from django.db.models.functions import ExtractMonth
import datetime
from pms.models import Blogs, Contact, Property, PropertyContacts, PropertyImages, PropertyMembership, UserProfile,Location

months_mapping = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def index(request):

    try:
        property_list = list(Property.objects.filter(
            is_listed=True).order_by('-membership_purchased'))

        if len(property_list) > 6:
            random_properties = random.sample(property_list, 6)
        else:
            random_properties = (Property.objects.filter(
                is_listed=True).order_by('-membership_purchased'))

    except Exception as e:
        print(e)

    try:
        agents_list = list(UserProfile.objects.filter(
            user_type="Agent").order_by('-created_at'))

        if len(agents_list) > 3:
            random_agents = random.sample(agents_list, 3)
        else:
            random_agents = UserProfile.objects.filter(
                user_type="Agent").order_by('-created_at')

    except Exception as e:
        print(e)

    all_properties = Property.objects.filter(is_listed=True)

    blogs = Blogs.objects.all().order_by('-created_at')

    index_page_blogs = None
    if len(blogs) > 6:
        index_page_blogs = blogs[:6]
    else:
        index_page_blogs = blogs
    buyer=False
    seller=False
    for agent in agents_list:
        if str(request.user) == str(agent):
            seller=True
            buyer=False
            break
        else:
            seller=False
            buyer=True
    print(request.user not in random_agents)
    context = {
        'random_properties': random_properties,
        'all_properties': all_properties,
        'random_agents': random_agents,
        'index_page_blogs': index_page_blogs,
        'buyer':buyer,
        'seller':seller,
    }
    return render(request, 'ui_templates/index.html', context)


def error_404_view(request, exception):
    return render(request, 'ui_templates/404.html')


def about(request):
    registered_users = UserProfile.objects.filter(user_type='Buyer').count()
    agents = UserProfile.objects.filter(user_type='Agent').count()
    total_properties = Property.objects.all().count()
    print(agents)
    context = {
        'registered_users': registered_users,
        'agents': agents,
        'total_properties': total_properties
    }
    return render(request, 'ui_templates/about.html', context)


def all_properties(request):
    filtered_properties = Property.objects.filter(
        is_listed=True).order_by('-membership_purchased')

    if request.method == 'GET':
        search_filter = request.GET.get('searching_filters')
        sorting_properties = request.GET.get('sort')
        property_size = request.GET.get('property_size')
        nearbuy_location = request.GET.get('nearbuy_location')

        if search_filter:
            filtered_properties = Property.objects.filter(
                Q(city__icontains=search_filter) |
                Q(state__icontains=search_filter) |
                Q(address__icontains=search_filter) |
                Q(type__icontains=search_filter) |
                Q(zip_code__icontains=search_filter) |
                Q(furnishing__icontains=search_filter) |
                Q(availability__icontains=search_filter) |
                Q(ownership__icontains=search_filter) |
                Q(expected_price__icontains=search_filter) |
                Q(details__icontains=search_filter)
            ).order_by('-membership_purchased')

        if sorting_properties and sorting_properties == 'lth':
            filtered_properties = filtered_properties.order_by(
                'expected_price')

        if sorting_properties and sorting_properties == 'htl':
            filtered_properties = filtered_properties.order_by(
                '-expected_price')

        if property_size:
            filtered_properties = filtered_properties.filter(
                area__gte=property_size)

        if nearbuy_location:
            filtered_properties = filtered_properties.filter(
                Q(city__icontains=nearbuy_location) |
                Q(state__icontains=nearbuy_location) |
                Q(address__icontains=nearbuy_location))

        paginator = Paginator(filtered_properties, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'active_properties': filtered_properties,
            'page_obj': page_obj,
        }

        return render(request, 'ui_templates/properties.html', context)

    else:
        active_properties = Property.objects.filter(
            is_listed=True).order_by('-membership_purchased')

        paginator = Paginator(active_properties, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'active_properties': active_properties,
            'page_obj': page_obj,
        }

        return render(request, 'ui_templates/properties.html', context)


def property_details(request, id):

    property = Property.objects.get(id=id)

    property_images = PropertyImages.objects.filter(property=property)
    amenities = []
    if property.amenities:
        amenities = [amenity.strip()
                     for amenity in property.amenities.split(',')]

    context = {
        'property': property,
        'amenities': amenities,
        'property_images': property_images,
    }
    return render(request, 'ui_templates/property_detail.html', context)


def blog(request):
    recent_blogs = Blogs.objects.all().order_by('-created_at')

    paginator = Paginator(recent_blogs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recent_blogs': recent_blogs,
        'page_obj': page_obj,
    }
    return render(request, 'ui_templates/blog.html', context)


def blog_description(request, id):
    requested_blog = Blogs.objects.filter(id=id)
    context = {'requested_blog': requested_blog}
    return render(request, 'ui_templates/blog_description.html', context)


@login_required(login_url='login')
def add_new_blog(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        if request.method == 'POST':
            blog_image = None
            title = request.POST.get('title')
            body = request.POST.get('body')

            try:
                blog_image = request.FILES.get('blog_image')
            except Exception as e:
                print(e)

            if blog_image:
                create_new_blog = Blogs(
                    blog_title=title, blog_body=body, blog_image=blog_image,
                    uploaded_by=user)
                create_new_blog.save()

                messages.add_message(request, messages.WARNING,
                                     "New Blog Created Successfully.")

            else:
                messages.add_message(request, messages.WARNING,
                                     "Blog Image is Required")

    return render(request, 'dashboard_templates/blog/add_new_blog.html')


@login_required(login_url='login')
def view_blogs_list(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        all_blogs = Blogs.objects.all()
        context = {'all_blogs': all_blogs}
        return render(request, 'dashboard_templates/blog/blogs_view.html', context)


@login_required(login_url='login')
def update_blog(request, id):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        requested_blog = Blogs.objects.filter(id=id)

        if request.method == 'POST':
            blog_update = Blogs.objects.filter(id=id).first()

            updated_title = request.POST.get('title')
            updated_body = request.POST.get('body')

            blog_update.blog_title = updated_title
            blog_update.blog_body = updated_body

            try:
                updated_blog_image = request.FILES['blog_image']
                blog_update.blog_image = updated_blog_image
            except Exception as e:
                print(e)

            blog_update.save()

            messages.add_message(request, messages.WARNING,
                                 "Blog Updated Successfully.")

        context = {
            'requested_blog': requested_blog
        }
        return render(request, 'dashboard_templates/blog/update_blog.html', context)


@login_required(login_url='login')
def delete_blog(request, id):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        requested_blog = Blogs.objects.filter(id=id)
        requested_blog.delete()
        return redirect('blog_list')


def auth_login(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING,
                             "You already logged in.")
        return redirect('index')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                messages.add_message(
                    request, messages.WARNING, f"Welcome, {request.user.first_name} {request.user.last_name} you logged in successfully.")
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.WARNING, "Sorry, check again your email or password.")

    return render(request, 'ui_templates/login_page.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         "Success, You Logged Out Successfully.")
    return redirect('index')


@login_required(login_url='login')
def profile(request):
    requested_user = request.user
    user_profile = UserProfile.objects.get(user=requested_user)
    context = {
        'profile_details': user_profile
    }
    return render(request, 'dashboard_templates/profile/user_profile.html', context)


def contact_us(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and contact_no and subject and message:

            new_contact = Contact(name=name, email=email, contact_no=contact_no,
                                  subject=subject, message=message)
            new_contact.save()

            messages.add_message(
                request, messages.SUCCESS, "Thanks for Contacting us. We will contact you shortly.")

            return redirect('index')

        else:
            messages.add_message(request, messages.WARNING,
                                 "Please fill all the required details.")

            return render(request, 'ui_templates/contact.html')

    return render(request, 'ui_templates/contact.html')


def auth_register(request):
    password_validation = False
    if request.method == 'POST':
        profile_image = None
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        try:
            profile_image = request.FILES.get('profile_image')
        except Exception as e:
            print(e)

        user_exists = User.objects.filter(username=email)

        # Minimum six characters, Maximum 20 Characters, at least one Uppercase and Lowecase letter and one number:
        password_regex = (
            "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")

        password_regex_compile = re.compile(password_regex)

        if (re.search(password_regex_compile, password)):
            password_validation = True

        if password_validation:
            if profile_image:
                if not user_exists:
                    if user_type == "Agent":
                        new_user = User.objects.create_user(
                            first_name=fname, last_name=lname, username=email, email=email, password=password, is_active=True, is_staff=True)

                        new_user.save()

                        subject = "Dream Homes: Registration Successfully"
                        body = (
                            "Hi "+fname+". Thanks for Registering with Dream Homes as a " + user_type+".")

                        send_customise_mail(
                            subject=subject,
                            body=body,
                            email_id=email)

                    else:
                        new_user = User.objects.create_user(
                            first_name=fname, last_name=lname, username=email, email=email, password=password, is_active=True)

                        new_user.save()

                        subject = "Dream Homes: Registration Successfully"
                        body = (
                            "Hi "+fname+". Thanks for Registering with Dream Homes as a " + user_type+".")

                        send_customise_mail(
                            subject=subject,
                            body=body,
                            email_id=email)

                    user_profile = UserProfile(
                        contact=contact, user=new_user, user_type=user_type, user_image=profile_image)
                    user_profile.save()

                    messages.add_message(
                        request, messages.SUCCESS, "Thanks for Registering with us.Please Login")
                    return redirect('login')

                else:
                    messages.add_message(
                        request, messages.WARNING, "You Already have an Account. Please Login")

            else:
                messages.add_message(
                    request, messages.SUCCESS, "Profile Image is Required")

        else:
            messages.add_message(
                request, messages.WARNING, "Please Create Strong Password as mentioned criteria.")

    return render(request, 'ui_templates/register_page.html')


class Month(Func):
    function = 'EXTRACT'
    template = "%(function)s(MONTH from %(expressions)s)"
    output_field = models.IntegerField()


@login_required(login_url='login')
def dashboard(request):
    logged_in_user = request.user
    current_time = datetime.datetime.now()
    properties_uploaded_by_user = Property.objects.filter(uploaded_by=logged_in_user)

    if logged_in_user.is_superuser:
        total_membership_amount = PropertyMembership.objects.aggregate(Sum('property_membership_amount'))['property_membership_amount__sum']
        total_membership_taken = PropertyMembership.objects.count()
        approved_properties = Property.objects.filter(approved=True).count()
        pending_properties = Property.objects.filter(approved=False).count()
        listed_properties = Property.objects.filter(is_listed=True).count()
        unlisted_properties = Property.objects.filter(is_listed=False).count()

        response_summary = (PropertyContacts.objects
                            .filter(property_id__in=properties_uploaded_by_user, created_at__year=current_time.year)
                            .annotate(response_by_month=ExtractMonth('created_at'))
                            .values('response_by_month')
                            .annotate(total=Count('id')))
    else:
        approved_properties = Property.objects.filter(uploaded_by=logged_in_user, approved=True).count()
        pending_properties = Property.objects.filter(uploaded_by=logged_in_user, approved=False).count()
        listed_properties = Property.objects.filter(uploaded_by=logged_in_user, is_listed=True).count()
        unlisted_properties = Property.objects.filter(uploaded_by=logged_in_user, is_listed=False).count()

        response_summary = (PropertyContacts.objects
                            .filter(property_id__in=properties_uploaded_by_user, created_at__year=current_time.year)
                            .annotate(response_by_month=ExtractMonth('created_at'))
                            .values('response_by_month')
                            .annotate(total=Count('id')))

    response_data = []
    for data in response_summary:
        response_data.append({
            "month": datetime.date(1900, data['response_by_month'], 1).strftime("%B"),
            "total_responses": data['total']
        })

    for month in range(1, 13):
        if not any(data['month'] == datetime.date(1900, month, 1).strftime("%B") for data in response_data):
            response_data.append({"month": datetime.date(1900, month, 1).strftime("%B"), "total_responses": 0})

    sorted_response_data = sorted(response_data, key=lambda d: datetime.datetime.strptime(d['month'], "%B"))
    random_agents = UserProfile.objects.filter(
                user_type="Agent")
    buyer=False
    seller=False
    for agent in random_agents:
        if str(request.user) == str(agent):
            seller=True
            buyer=False
            print("seller")
            break
        else:
            seller=False
            buyer=True
            print("buyer")
    context = {
        'approved_properties': approved_properties,
        'listed_properties': listed_properties,
        'unlisted_properties': unlisted_properties,
        'pending_properties': pending_properties,
        'total_membership_amount': total_membership_amount if logged_in_user.is_superuser else None,
        'total_membership_taken': total_membership_taken if logged_in_user.is_superuser else None,
        'response_data': sorted_response_data,
        'current_year': current_time.year,
        'buyer':buyer,
        'seller':seller,
    }
    

    return render(request, 'dashboard_templates/dashboard.html', context)

@login_required(login_url='login')
def add_new_property(request):
    user = request.user
    states = Location.objects.values_list('state_name', flat=True).distinct()

    last_property_id = Property.objects.all().order_by('id').last()
    if not last_property_id:
        prop_id = 'WHPR' + '000001'
    else:
        last_prop_id = last_property_id.property_id
        prop_no_int = int(last_prop_id[4:10])
        new_property_id = prop_no_int + 1
        prop_id = 'WHPR' + str(new_property_id).zfill(6)

    if request.method == 'POST':
        property_sr = request.POST.get('property_sr')
        property_type = request.POST.get('property_type')
        property_address = request.POST.get('property_address')
        property_city = request.POST.get('property_city')
        property_state = request.POST.get('property_state')
        no_bedrooms = request.POST.get('no_bedrooms')
        no_bathrooms = request.POST.get('no_bathrooms')
        no_balconies = request.POST.get('no_balconies')
        area_details = request.POST.get('area_details')
        furnishing_type = request.POST.get('furnishing_type')
        open_parking = request.POST.get('open_parking')
        covered_parking = request.POST.get('covered_parking')
        availability_status = request.POST.get('availability_status')
        property_age = request.POST.get('property_age')
        property_ownership = request.POST.get('property_ownership')
        expected_price = request.POST.get('expected_price')
        price_sq_ft = request.POST.get('price_sq_ft')
        property_unique_details = request.POST.get('property_unique_details')
        zip_code = request.POST.get('zip_code')
        amenities = request.POST.get('amenities')

        create_new_property = Property(
            property_id=prop_id,
            sell_rent=property_sr,
            type=property_type,
            address=property_address,
            city=property_city,
            state=property_state,
            zip_code=zip_code,
            bedrooms=no_bedrooms,
            bathrooms=no_bathrooms,
            balconies=no_balconies,
            area=area_details,
            furnishing=furnishing_type,
            open_parking=open_parking,
            covered_parking=covered_parking,
            availability=availability_status,
            age=property_age,
            ownership=property_ownership,
            expected_price=expected_price,
            area_price=price_sq_ft,
            details=property_unique_details,
            approved=False,
            uploaded_by=request.user,
            amenities=amenities
        )
        create_new_property.save()

        try:
            property_images = request.FILES.getlist('property_images')
            for img in property_images:
                new_img = PropertyImages(
                    property=create_new_property,
                    images=img
                )
                new_img.save()
        except Exception as e:
            print(e)

        subject = "Dream Homes: Property Added Successfully"
        body = ("Hi "+user.first_name+". New Property Added Successfully. Your Property ID: " +
                prop_id+". It will be listed once all details are verified.")

        send_customise_mail(
            subject=subject,
            body=body,
            email_id=user.email)

        messages.add_message(request, messages.WARNING,
                             "New Property Created Successfully.")
    print(len(states))
    agents_list = list(UserProfile.objects.filter(
            user_type="Agent"))
    buyer=False
    seller=False
    for agent in agents_list:
        if str(request.user) == str(agent):
            seller=True
            buyer=False
            break
        else:
            seller=False
            buyer=True
    if seller:
        return render(request, 'dashboard_templates/property/add_new_property.html',{'states': states})
    else:
        return redirect('property_list')

def get_zip_codes(request):
    if request.method == 'GET' and 'city_name' in request.GET:
        city_name = request.GET['city_name']
        zip_codes = Location.objects.filter(city_name=city_name).values_list('postal_code', flat=True).distinct()
        print(list(zip_codes))
        return JsonResponse(list(zip_codes), safe=False)
    
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def get_cities(request):
    if request.method == 'GET' and 'state_name' in request.GET:
        state_name = request.GET.get('state_name')
        cities = Location.objects.filter(state_name=state_name).values_list('city_name', flat=True)
        print(cities)
        return JsonResponse(list(cities), safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='login')
def list_uploaded_properties(request):
    properties_list_by_user = Property.objects.all#(uploaded_by=request.user)

    membership_amount = 5000000  # In Paisa = Rs 500
    membership_currency = 'INR'

    client = razorpay.Client(auth=(razorpay_api_key, razorpay_api_secret_key))

    payment_data = {"amount": membership_amount,
                    "currency": membership_currency, 'payment_capture': '1'}

    payment_order = client.order.create(data=payment_data)
    payment_order_id = payment_order['id']
    agents_list = list(UserProfile.objects.filter(
            user_type="Agent"))
    buyer=False
    seller=False
    for agent in agents_list:
        if str(request.user) == str(agent):
            seller=True
            buyer=False
            break
        else:
            seller=False
            buyer=True
    
    context = {
        'amount': membership_amount,
        'api_key': razorpay_api_key,
        'order_id': payment_order_id,
        'property_list': properties_list_by_user,
        'buyer':buyer,
        'seller':seller,

    }
    return render(request, 'dashboard_templates/property/list_uploaded_properties.html', context)


@login_required(login_url='login')
def list_property_contacts(request, id):

    property_contacts = PropertyContacts.objects.filter(property=id,
                                                        property__membership_purchased=True)

    context = {
        'property_contacts': property_contacts
    }

    return render(request, 'dashboard_templates/property/property_contacts.html', context)


@login_required(login_url='login')
def delete_property(request, id):
    requested_property = Property.objects.get(id=id)
    requested_property.delete()
    return redirect('property_list')


@login_required(login_url='login')
def update_property(request, id, view=None):
    user = request.user

    requested_property = Property.objects.filter(id=id)

    if request.method == 'POST':
        property_update = Property.objects.filter(id=id).first()

        property_sr = request.POST.get('property_sr')
        property_type = request.POST.get('property_type')
        property_address = request.POST.get('property_address')
        property_city = request.POST.get('property_city')
        property_state = request.POST.get('property_state')
        no_bedrooms = request.POST.get('no_bedrooms')
        no_bathrooms = request.POST.get('no_bathrooms')
        no_balconies = request.POST.get('no_balconies')
        area_details = request.POST.get('area_details')
        furnishing_type = request.POST.get('furnishing_type')
        open_parking = request.POST.get('open_parking')
        covered_parking = request.POST.get('covered_parking')
        availability_status = request.POST.get('availability_status')
        property_age = request.POST.get('property_age')
        property_ownership = request.POST.get('property_ownership')
        expected_price = request.POST.get('expected_price')
        price_sq_ft = request.POST.get('price_sq_ft')
        property_unique_details = request.POST.get('property_unique_details')
        zip_code = request.POST.get('zip_code')
        amenities = request.POST.get('amenities')

        property_update.sell_rent = property_sr
        property_update.type = property_type
        property_update.address = property_address
        property_update.city = property_city
        property_update.state = property_state
        property_update.bedrooms = no_bedrooms
        property_update.bathrooms = no_bathrooms
        property_update.balconies = no_balconies
        property_update.area = area_details
        property_update.furnishing = furnishing_type
        property_update.open_parking = open_parking
        property_update.covered_parking = covered_parking
        property_update.availability = availability_status
        property_update.age = property_age
        property_update.ownership = property_ownership
        property_update.expected_price = expected_price
        property_update.area_price = price_sq_ft
        property_update.zip_code = zip_code
        property_update.details = property_unique_details
        property_update.amenities = amenities
        try:
            updated_blog_image = request.FILES['blog_image']
            property_update.blog_image = updated_blog_image
        except Exception as e:
            print(e)

        requested_property_images = PropertyImages.objects.filter(
            property=property_update)
        try:
            property_images = request.FILES.getlist('property_images')
            if property_images:
                for old_img in requested_property_images:
                    old_img.delete()

            for img in property_images:
                new_images = PropertyImages(
                    property=property_update,
                    images=img
                )
                new_images.save()
        except Exception as e:
            print(e)

        property_update.save()

        subject = "Dream Homes: Property Updated Successfully"
        body = ("Hi "+user.first_name+". Your Property " +
                property_update.property_id+" Updated Successfully.")

        send_customise_mail(
            subject=subject,
            body=body,
            email_id=user.email)

        messages.add_message(request, messages.WARNING,
                             "Property Details Updated Successfully.")

    if view:
        context = {'requested_property': requested_property,
                   'view_property': True}
    else:
        context = {'requested_property': requested_property}
    return render(request, 'dashboard_templates/property/update_property.html', context)


@login_required(login_url='login')
def view_property_images(request, id):
    property_images = PropertyImages.objects.filter(property=id)

    context = {
        'property_images': property_images
    }
    return render(request, 'dashboard_templates/property/property_images.html', context)


@csrf_exempt
def payment_success_membership(request, id):
    user = request.user
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id', '')

    property = Property.objects.get(id=id)
    property.membership_purchased = True
    amount = 500

    create_property_membership = PropertyMembership(
        property=property,
        user=request.user,
        property_membership_plan=True,
        payment_order_id=payment_id,
        property_membership_amount=amount
    )

    create_property_membership.save()
    property.save()

    subject = "Dream Homes: Property Membership"
    body = ("Hi "+user.first_name+". Thanks for Purchasing Property " +
            property.property_id+" Membership.")

    send_customise_mail(
        subject=subject,
        body=body,
        email_id=user.email)

    return redirect('property_list')


@login_required(login_url='login')
def pending_properties_view(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        pending_properties_list = Property.objects.filter(
            approved=False)
        context = {
            'pending_properties_data': pending_properties_list
        }
        return render(request, 'dashboard_templates/property/pending_properties.html', context)


@login_required(login_url='login')
def approve_property(request, id):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        property = Property.objects.get(id=id)
        property.approved = True
        property.approved_on = datetime.datetime.now()
        property.is_listed = True
        property.save()
        return redirect('pending_properties')


@login_required(login_url='login')
def unlist_property(request, id):
    property = Property.objects.get(id=id)
    property.is_listed = False
    property.unlisted_date = datetime.datetime.now()
    property.save()
    return redirect('unlisted_properties')


@login_required(login_url='login')
def listed_properties_view(request):
    listed_properties_list = Property.objects.filter(
        approved=True, is_listed=True)

    context = {
        'listed_properties_data': listed_properties_list
    }

    return render(request, 'dashboard_templates/property/listed_properties.html', context)


@login_required(login_url='login')
def unlisted_properties_view(request):
    unlisted_properties_list = Property.objects.filter(
        approved=True, is_listed=False, uploaded_by=request.user)

    context = {
        'unlisted_properties_data': unlisted_properties_list
    }

    return render(request, 'dashboard_templates/property/unlisted_properties.html', context)


@login_required(login_url='login')
def calculate_emi(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        interest = request.POST.get('interest')
        tenure = request.POST.get('tenure')

        if not amount or not interest or not tenure:
            messages.add_message(request, messages.WARNING,
                                 "Fill All the Details Properly")
            return render(request, 'emi_calculate.html')
        else:
            rate_of_interest_per_month = float(interest)/(12*100)

            monthly_emi = float(amount) * float(rate_of_interest_per_month) * ((1+float(rate_of_interest_per_month))
                                                                               ** float(tenure))/((1+float(rate_of_interest_per_month)) ** float(tenure) - 1)

            total_interest_amount = (
                float(monthly_emi)*float(tenure)) - float(amount)

            context = {
                'amount': amount,
                'rate_of_interest_per_month': rate_of_interest_per_month,
                'tenure': tenure,
                'monthly_emi': monthly_emi,
                'total_interest_amount': total_interest_amount,
                'interest': interest,
                'total_amount': round((float(amount)+float(total_interest_amount)), 2),
            }

            return render(request, 'dashboard_templates/emi_calculate.html', context)
    else:
        return render(request, 'dashboard_templates/emi_calculate.html')


@login_required(login_url='login')
def agents_list_view(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        agents_data = UserProfile.objects.filter(user_type='Agent').all()
        context = {
            'agents_list': agents_data
        }
        return render(request, 'dashboard_templates/reports/agents_list.html', context)


@login_required(login_url='login')
def properties_uploaded_by_user(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        properties = Property.objects.all()

        context = {
            'properties': properties
        }
        return render(request, 'dashboard_templates/reports/user_uploaded_properties.html', context)


@login_required(login_url='login')
def customers_list_view(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        customers_data = UserProfile.objects.filter(user_type='Buyer').all()
        context = {
            'customers_data': customers_data
        }
        return render(request, 'dashboard_templates/reports/customers_list.html', context)


@login_required(login_url='login')
def total_uploaded_properties(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        all_uploaded_properties = Property.objects.all()
        context = {
            'all_uploaded_properties': all_uploaded_properties
        }
        return render(request, 'dashboard_templates/reports/total_uploaded_properties.html', context)


@login_required(login_url='login')
def total_listed_properties(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        all_listed_properties = Property.objects.filter(is_listed=True)
        context = {
            'all_listed_properties': all_listed_properties
        }
        return render(request, 'dashboard_templates/reports/total_listed_properties.html', context)


@login_required(login_url='login')
def total_unlisted_properties(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        all_unlisted_properties = Property.objects.filter(
            is_listed=False, unlisted_date__isnull=False)
        context = {
            'all_unlisted_properties': all_unlisted_properties
        }
        return render(request, 'dashboard_templates/reports/total_unlisted_properties.html', context)


@login_required(login_url='login')
def revenue_details(request):
    user = request.user
    if not user.is_superuser:
        return redirect('index')
    else:
        if request.method == 'POST':
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')

            if from_date and to_date:
                from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
                to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

                to_date = datetime.datetime(
                    to_date.year, to_date.month, to_date.day, 23, 59, 59)

                revenue_details = PropertyMembership.objects.filter(
                    payment_date__gte=from_date, payment_date__lte=to_date)

                context = {
                    'revenue_details': revenue_details
                }

                if revenue_details:
                    messages.add_message(request, messages.SUCCESS,
                                         "Revenue Details From: "+str(from_date)+" To: "+str(to_date))
                else:
                    messages.add_message(request, messages.WARNING,
                                         "No Revenue Details Found !!")

                return render(request, 'dashboard_templates/reports/revenue_details.html', context)

            else:
                return render(request, 'dashboard_templates/reports/revenue_details.html')

        else:
            return render(request, 'dashboard_templates/reports/revenue_details.html')


def property_comments(request, id):
    if request.method == 'POST':
        property = Property.objects.get(id=id)

        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        comment = request.POST.get('comment')

        new_property_contact = PropertyContacts(
            name=name, email=email, contact=contact, comments=comment, property=property)

        new_property_contact.save()

        subject = "Dream Homes: Property Response"
        body = ("Hi "+property.uploaded_by.first_name +
                ". Someone Shows Interest in your Property. Property ID: "+property.property_id+".")

        send_customise_mail(
            subject=subject,
            body=body,
            email_id=property.uploaded_by.email)

        messages.add_message(request, messages.WARNING,
                             "Query Submitted Successfully...")

        return redirect("property_details", id=id)
    else:
        return redirect("index")


@login_required(login_url='login')
def view_user_image(request, id):
    user_profile_image = UserProfile.objects.filter(user=id)
    context = {
        'user_profile_image': user_profile_image
    }
    return render(request, 'dashboard_templates/reports/user_images.html', context)
