import requests
import json
import uuid

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings

from . models import *
from room.models import *
from userprofile.models import *
from booking.models import *
from .forms import TalkToUsForm
from userprofile.forms import SignupForm, ProfileForm

# Create your views here.
def home(request):
    standard_suite = Room.objects.filter(standard_suite=True).order_by('-updated_at')[:1]
    luxury_suite = Room.objects.filter(luxury_suite=True).order_by('-updated_at')[:1]
    deluxe_suite = Room.objects.filter(deluxe_suite=True).order_by('-updated_at')[:1]
    royal_suite = Room.objects.filter(royal_suite=True).order_by('-updated_at')[:1]

    context = {
        'standard_suite': standard_suite,
        'luxury_suite': luxury_suite,
        'deluxe_suite': deluxe_suite,
        'royal_suite': royal_suite,
    }
    return render(request, 'index.html', context)

    #display all the available rooms

def rooms(request):
    rooms = Room.objects.all().order_by('-created_at')
    p = Paginator(rooms, 8)
    page = request.GET.get('page')
    paginate = p.get_page(page)
    
    context = {
        'paginate':paginate
    }

    return render(request, 'rooms.html', context)


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'categories.html', context)


def category(request,id,slug):
    category = Room.objects.filter(category_id = id)
    specific_category = Category.objects.get(pk = id)

    context = {
        'category': category,
        'specific_category': specific_category,
    }

    return render(request, 'category.html', context)


def details(request, id, slug):
    detail = Room.objects.get(pk = id)

    context = {
        'detail':detail,
    }

    return render(request, 'details.html', context)


def talktous(request):
    talkform = TalkToUsForm() #instantiate the form for a Get request
    if request.method == 'POST': # method POST is used to collect data from users so as to persist the data to the Database 
        talkform = TalkToUsForm(request.POST) #instantiate the form for a POST request
        if talkform.is_valid(): # form validations holds at this point
            talkform.save() # form is saved if it passes the validation check
            messages.success(request, 'Your messages has been sent successfully! We will contact you shortly, Thank you.') # alert pop us message will be sent automatically
            return redirect('home')

    return render(request, 'index.html')

def search(request):
    if request.method == 'POST':
        items = request.POST['search']
        searched = Q(Q(tag__icontains=items)| Q(rate__icontains=items)| Q(room_no__icontains=items))
        searched_item = Room.objects.filter(searched)
        context = {
            'items':items,
            'searched_item':searched_item
        }

        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')

# authentication 
def signout(request):
    logout(request)
    messages.success(request, 'You have signed out!')
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # new = user.username.title()
        if user:
            login(request, user)
            messages.success(request, f'{username} Welcome, signin successful!')
            return redirect('home')
        else:
            messages.info(request, 'Username/Password is incorrect, please try again.')
            return redirect('signin')

    return render(request, 'signin.html')



def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            newuser = Profile(user = user)
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.phone = phone
            newuser.pix = pix
            newuser.save()
            login(request, user)
            client = user.username.title()
            messages.success(request, f'Congratulations {client} your registration is successful!')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('signup')

    return render(request, 'signup.html')
# authentication done

# user profile 
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile':profile
    }    

    return render(request, 'profile.html', context)



@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username= request.user.username)
    form = ProfileForm(instance=request.user.profile) #instatiate the form for a GET request
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)#instatiate the form for a POST request
        if form.is_valid():
            user = form.save()
            new = user.first_name.title()
            messages.success(request, f'Dear {new}, your profile update is successful!')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {new}, your update generated the following errors: {form.errors}')
            return redirect('update')
            
    context = {
        'form': form,
        'profile':profile
    }
    return render(request, 'update.html', context)


@login_required(login_url='signin')
def password_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            new = user.username.title()
            update_session_auth_hash(request, user)
            messages.success(request, f'Dear {new} your password update is successful!')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {new} your password update is unsuccessful, {form.errors}')
            return redirect('password')

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'password.html', context)
# user profile done

# booking 
@login_required(login_url='signin')
def booking(request):
    profile = Profile.objects.get(user__username = request.user.username)
    code = profile.id
    if request.method == 'POST':
        datein = request.POST['checkin']
        dateout = request.POST['checkout']
        droom = request.POST['roomid']
        specific = Room.objects.get(pk=droom)
        booking = Booking.objects.filter(user__username = request.user.username, paid=False)
        if booking:
            reserve = Booking.objects.filter(room = specific.id, checkin=datein, checkout=dateout,user__username = request.user.username, paid=False)
            if reserve:
                reserve.checkin = datein
                reserve.checkout = dateout 
                if reserve.checkin > dateout or reserve.checkout < datein:
                    reserve.save()
                    messages.success(request, 'Your booking is confirmed!.Kindly make payment within 30mins')
                    return redirect('booked')
                else:
                    messages.info(request, 'The room you requested is already booked.')
                    return redirect('rooms')
            else:
                newroom = Booking()
                newroom.user = request.user
                newroom.room = specific
                newroom.room_num = specific.room_no
                newroom.booking_code = code
                newroom.checkin = datein
                newroom.checkout = dateout
                newroom.price = specific.rate
                newroom.paid = False
                newroom.available = False
                newroom.save()
                messages.success(request, 'Your booking is confirmed!.Kindly make payment within 30mins')
                return redirect('booked')

        else:#capture  a user's first booking attempt
            new = Booking()
            new.user = request.user
            new.room = specific
            new.room_num = specific.room_no
            new.booking_code = code
            new.checkin = datein
            new.checkout = dateout
            new.price = specific.rate
            new.paid = False
            new.available = False
            new.save()
            messages.success(request, 'Your booking is confirmed!.Kindly make payment within 30mins')
    return redirect('booked')



@login_required(login_url='signin')
def booked(request):
    Booking.objects.filter(del_booking__lte = timezone.now() - timezone.timedelta(minutes=3)).filter(paid=False).delete()
    booking = Booking.objects.filter(user__username= request.user.username, paid=False)
    
    for item in booking:
        item.no_days = (item.checkout - item.checkin).days
        item.amount = item.price * item.no_days
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    # total amount of all bookings if more than one 
    for item in booking:
        subtotal += item.price * item.no_days

    # vat at 7.5%
    vat = 0.075 * subtotal 

    # total amount to be charged 
    total = subtotal + vat
   
    context = {
        'booking': booking, 
        'subtotal': subtotal, 
        'vat': vat, 
        'total': total, 
    }

    return render(request, 'booked.html', context)


#users delete room from booking table
@login_required(login_url='signin')
def delete_room(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        del_room = request.POST['room_id']
        Booking.objects.filter(pk=del_room).delete()
        messages.success(request, 'Room delete successful!')
        return redirect(url)


@login_required(login_url='signin')
def checkout(request):
    profile = Profile.objects.get(user__username= request.user.username)
    booking = Booking.objects.filter(user__username= request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    # total amount of all bookings if more than one 
    for item in booking:
        subtotal += item.price * item.no_days

    # vat at 7.5%
    vat = 0.075 * subtotal 

    # total amount to be charged 
    total = subtotal + vat
   
    context = {
        'profile': profile, 
        'booking': booking, 
        'total': total, 
    }

    return render(request, 'checkout.html', context)


@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
        curl = 'https://api.paystack.co/transaction/initialize'
        # cburl = 'http://54.172.50.9/booking_confirmed'    
        cburl = 'http://54.91.97.254/booking_confirmed'    
        # cburl = 'http://localhost:8000/booking_confirmed'    
        ref = str(uuid.uuid4()) 
        profile = Profile.objects.get(user__username = request.user.username)
        booking_code = profile.id  
        total = float(request.POST['total']) * 100  
        user = User.objects.get(username = request.user.username)   
        email = user.email  
        first_name = request.POST['first_name']     
        last_name = request.POST['last_name']   
        phone = request.POST['phone']   
        # address = request.POST['address']
        # state = request.POST['state']


        #collect data to send to paystack via call
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'amount': int(total), 'email': email, 'callback_url': cburl, 'order_number': booking_code, 'currency': 'NGN'}

        #make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data) #pip install requests
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.first_name = first_name
            account.last_name = last_name
            account.amount = total/100
            account.paid = True
            account.phone = phone
            account.pay_code = ref
            account.booking_code = booking_code
            account.save()

            email = EmailMessage(
                'Transaction successful',#subject
                f'Dear {first_name }! your reservation is successful. \n \n We look forward to your arrival. Thank you for choosing us to serve you.',#message
                settings.EMAIL_HOST_USER,#host email
                [email] #sender
                )

            email.fail_silently = True
            email.send()

            return redirect(rdurl)
        return redirect('checkout')
    


def callback(request):
    profile = Profile.objects.get(user__username = request.user.username)
    reserved  = Booking.objects.filter(user__username = request.user.username, paid=True)
    booking = Booking.objects.filter(user__username = request.user.username, paid=False)

    for item in booking:
        item.paid = True
        item.available = False
        item.future = True
        item.display = True
        item.save()

        room = Room.objects.get(pk=item.room.id)
        room.available = False
        room.save()


    subtotal = 0
    vat = 0
    total = 0

    # total amount of all bookings if more than one 
    for item in reserved:
        subtotal += item.price * item.no_days

    # vat at 7.5%
    vat = 0.075 * subtotal 

    # total amount to be charged 
    total = subtotal + vat

    context = {
        'profile':profile,
        'reserved':reserved,
        'total':total,
    }

    return render(request, 'callback.html', context)


@login_required(login_url='signin')
def booking_details(request):
    profile = Profile.objects.get(user__username = request.user.username)
    reserved  = Booking.objects.filter(user__username = request.user.username, paid=True, future=True)
    
    subtotal = 0
    vat = 0
    total = 0

    # total amount of all bookings if more than one 
    for item in reserved:
        subtotal += item.price * item.no_days

    # vat at 7.5%
    vat = 0.075 * subtotal 

    # total amount to be charged 
    total = subtotal + vat

    context = {
        'profile':profile,
        'reserved':reserved,
        'total':total,
    }

    return render(request, 'booking_details.html', context)



#booking history
@login_required(login_url='signin')
def history(request):
    profile = Profile.objects.get(user__username = request.user.username)
    reserved  = Booking.objects.filter(user__username = request.user.username, paid=True,  future=False, display=True)
   
    subtotal = 0
    vat = 0
    total = 0

    # total amount of all bookings if more than one 
    for item in reserved:
        subtotal += item.price * item.no_days

    # vat at 7.5%
    vat = 0.075 * subtotal 

    # total amount to be charged 
    total = subtotal + vat

    context = {
        'profile':profile,
        'reserved':reserved,
        'total':total,
    }

    return render(request, 'history.html', context)


#booking history deletion
@login_required(login_url='signin')
def del_history(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        history_id = request.POST['history_id']
        del_detail = Booking.objects.filter(pk = history_id)
        for item in del_detail:
            item.display = False 
            item.save()
            messages.success(request, 'Booking history deleted successfully!')
        return redirect(url)

# booking completely trashed