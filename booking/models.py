from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from room.models import Room
# Create your models here.



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_num = models.IntegerField()
    booking_code = models.CharField(max_length=50)
    checkin = models.DateField()
    checkout = models.DateField()
    no_days = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    paid = models.BooleanField(default= False)
    available = models.BooleanField(default=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    del_booking = models.DateTimeField(default=timezone.now)
    checkout_update = models.DateTimeField(auto_now=True)
    future = models.BooleanField(default=False)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField(default= False)
    phone = models.CharField(max_length=20)
    pay_code = models.CharField(max_length=36)
    booking_code = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.user.username
    
   
   
    
    
    
    
    