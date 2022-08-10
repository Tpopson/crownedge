from django.db import models

# Create your models here.


class Category(models.Model):
    room_type = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    room_pix = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return self.room_type

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Room(models.Model):
    category = models.ForeignKey(Category,on_delete= models.CASCADE)
    tag = models.CharField(max_length=50)
    room_no = models.IntegerField()
    slug = models.SlugField(unique=True)
    room_img = models.ImageField(upload_to='room', blank=True, null=True)
    description = models.TextField()
    rate = models.IntegerField()
    amenity = models.CharField(max_length=100)
    standard_suite = models.BooleanField(default=False)
    luxury_suite = models.BooleanField(default=False)
    deluxe_suite = models.BooleanField(default=False)
    royal_suite = models.BooleanField(default=False)
    min_guest = models.IntegerField()
    max_guest = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.tag

    class Meta:
        db_table = 'room'
        managed = True
        verbose_name = 'Room'
        verbose_name_plural = 'Room'