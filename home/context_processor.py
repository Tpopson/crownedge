from room.models import Category
from . models import CompanyProfile
from booking.models import Booking


def dropdown(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return context 

def company(request):
    cprofile = CompanyProfile.objects.get(pk=1)

    context = {
        'cprofile':cprofile
    }

    return context 


def cartcount(request):
    count = Booking.objects.filter(user__username = request.user.username, paid=False)

    itemcount = 0
    for item in count:
        itemcount += item.no_days

    context = {
        'itemcount':itemcount
    }

    return context 

