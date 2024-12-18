from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, BadHeaderError, HttpResponseRedirect
from django.contrib import messages
from PIL import Image
from .models import Restaurant, Reservation, Menu, home, Photo, Basket, Comment
from .utils import average_rating
from .forms import NewUserForm
from django.conf import settings
import stripe
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse

from io import BytesIO
from django.core.files.images import ImageFile
import os


def index(request):
    homes = home.objects.filter()
    home_list = []
    for homess in homes:
        home_list.append({'homess' : homess})
    return render(request, "home.html", {'home' : home_list})


@login_required
def change(request):
    username = request.user.username

    # Retrieve reservations for the user
    reservations = Reservation.objects.filter(Username=username)
    basket = Basket.objects.filter(Username=username).first()
    reservation_list = []
    for reservation in reservations:
        title = get_object_or_404(Restaurant, title=reservation.Res_name)
        logo = title.logo.url
        reservation_list.append({'logo': logo, 'reservation': reservation})

    # Fetch or create user's photo instance
    photo_instance, created = Photo.objects.get_or_create(username=username)
    basket_items = basket.items if basket else {}
    menu_items = []
    if basket_items:
        for item_id, quantity in basket_items.items():
            menu_item = get_object_or_404(Menu, id=item_id)  # Get the menu item by ID
            menu_items.append({
                'name': menu_item.name,
                'price': menu_item.price,
                'img_url': menu_item.img.url,  # Get the image URL
                'quantity': quantity,
                'id': item_id,
            })
    if request.method == 'POST':
        if 'photo' in request.FILES:  # Ensure a file has been uploaded
            photo_instance.avatar = request.FILES['photo']
            photo_instance.save()
            return redirect('profile')  # Redirect to the same page to display updated image

    return render(request, 'profile.html', {
        'reservation_list': reservation_list,
        "photo": photo_instance.avatar,
        'menu_items': menu_items,
        "change": "change" if request.method != "POST" else "",
    })

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def profile(request):
    username = request.user.username
    reservations = Reservation.objects.filter(Username=username)
    basket = Basket.objects.filter(Username=username).first()
    reservation_list = []

    # Fetch reservation details
    for reservation in reservations:
        title = get_object_or_404(Restaurant, title=reservation.Res_name)
        logo = title.logo.url
        reservation_list.append({'logo': logo, 'reservation': reservation})

    # Fetch profile photo
    ava = get_object_or_404(Photo, username=username)
    photo = ava.avatar
    if not photo:
        photo = ''

    # Process basket items
    basket_items = basket.items if basket else {}
    menu_items = []
    total_price = 0  # Initialize total price
    if basket_items:
        for item_id, quantity in basket_items.items():
            menu_item = get_object_or_404(Menu, id=item_id)
            item_price = menu_item.price * quantity
            total_price += item_price
            menu_items.append({
                'name': menu_item.name,
                'price': menu_item.price,
                'img_url': menu_item.img.url,
                'quantity': quantity,
                'id': item_id,
            })

    return render(request, 'profile.html', {
        'reservation_list': reservation_list,
        'photo': photo,
        'menu_items': menu_items,
        'total_price': total_price,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def create_checkout_session(request):
    username = request.user.username
    basket = Basket.objects.filter(Username=username, is_paid=False).first()
    if not basket:
        return JsonResponse({'error': 'Basket is empty or already paid'}, status=400)

    # Prepare line items for Stripe checkout
    line_items = []
    for item_id, quantity in basket.items.items():
        menu_item = get_object_or_404(Menu, id=item_id)
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': menu_item.name,
                },
                'unit_amount': menu_item.price * 100,  # Amount in cents
            },
            'quantity': quantity,
        })

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/profile/success'),
        cancel_url=request.build_absolute_uri('/profile'),
    )

    return JsonResponse({'id': session.id})

@login_required
def payment_success(request):
    username = request.user.username
    basket = Basket.objects.filter(Username=username, is_paid=False).first()
    if basket:
        basket.is_paid = True
        basket.save()

    return render(request, 'payment_success.html')


def delete(request, res_id: int):
    Reservation.objects.filter(id=res_id).delete()
    return redirect('profile')


def delete_item(request, item_id: int):
    username = request.user.username
    basket = Basket.objects.filter(Username=username).first()

    items = basket.items
    print(items)
    del items[str(item_id)]
    print(items)

    basket.items = items
    basket.save()

    return redirect('profile')


@login_required
def reservation(request):
    restaurants = Restaurant.objects.all()
    if request.method == 'POST':
        Username = request.user.username
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Phone_num = request.POST.get('phone')
        Date = request.POST.get('date')
        Number = request.POST.get('number')
        Time = request.POST.get('time')
        Res_name = request.POST.get('res_name')
        Message = request.POST.get('message')

        reservations = Reservation.objects.filter(Date=Date)
        reservation_list = []
        for reservation in reservations:
            reservation_list.append({'reservation': reservation})

        reservationss = Reservation.objects.filter(Username=Username)
        reservation_list2 = []
        for reservation in reservationss:
            reservation_list2.append({'reservation': reservation})
        if len(reservation_list) > 10:
            messages.error(request, "There are more than 10 reservations on this day. Please choose another day")
            return redirect('profile')

        if len(reservation_list2) > 8:
            messages.error(request, "There are more than 8 reservations on this user")
            return redirect('profile')
        reservation = Reservation.objects.create(Username=Username, Name=Name, Email=Email, Phone_num=Phone_num,
                                                 Date=Date, Number=Number, Time=Time, Res_name=Res_name,
                                                 Message=Message)

        reservation.save()

        subject = "RESERVATION"
        message = "Name: {name},\n" \
                  "Phone number: {phone}\n" \
                  "Date: {date}\n" \
                  "Time: {time}\n" \
                  "Number of guests: {num}\n" \
                  "Comment: {comment}\n" \
                  "from Klassy reservation system".format(name=Name, phone=Phone_num, date=Date, time=Time, num=Number,
                                                          comment=Message)

        if subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [Email],
                          fail_silently=False)
                message = "Your reservation was sent successfully\n" + message
                send_mail(subject, message, settings.EMAIL_HOST_USER, [Email],
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Your table  was successfully reserved.")
            return HttpResponseRedirect("/reservation")

    return render(request, 'reservation.html', {"restaurants": restaurants})


def login(request):
    return render(request, 'registration/login.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            user = form.save()
            new = Photo.objects.create(avatar='ava/profile-icon-design-free-vector_1.png',username=username)
            new.save()
            messages.success(request, "Registration successful.")
            return redirect("/accounts/profile/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'registration/register.html', context={"form": form})


def ItemSearchView(request, id):
    if request.method == 'GET':
        search = request.GET.get('search_item')
        restaurant = get_object_or_404(Restaurant, id=id)
        menu = Menu.objects.filter(restaurant_id=id).filter(name__contains=search)
        return render(request, "restaurant_detail.html", {"restaurant": restaurant,
                                                          "menus": menu, 'id': id, 'search': search})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

# views.py
def restaurant_detail(request, restaurant_id, menu_id=None):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu = Menu.objects.filter(restaurant_id=restaurant_id)
    comments = restaurant.comments.all().order_by('-timestamp')  # Fetch comments for this restaurant

    if request.method == "POST":
        if "content" in request.POST:  # Check if a comment is being submitted
            content = request.POST.get("content")
            if content.strip():
                Comment.objects.create(restaurant=restaurant, user=request.user, content=content)
        else:  # Handle adding items to the basket
            item_id = menu_id
            quantity = int(request.POST.get('quantity', 1))
            user = request.user
            basket, created = Basket.objects.get_or_create(Username=user.username)
            items = basket.items if basket.items else {}
            if item_id in items:
                items[item_id] += quantity
            else:
                items[item_id] = quantity
            basket.items = items
            basket.save()

    return render(request, "restaurant_detail.html", {
        "restaurant": restaurant,
        "menus": menu,
        "comments": comments,
        "id": restaurant_id,
        "menu_id": menu_id,
    })
