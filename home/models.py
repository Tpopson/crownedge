from django.db import models

# Create your models here.


class CompanyProfile(models.Model):
    name = models.CharField(max_length=50)
    keyword = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
    favicon = models.ImageField(upload_to='logo', blank=True, null=True, default='/favicon-96x96.png')
    carousel = models.ImageField(upload_to='carousel', blank=True, null=True)
    carousel2 = models.ImageField(upload_to='carousel', blank=True, null=True)
    carousel3 = models.ImageField(upload_to='carousel', blank=True, null=True)
    carousel4 = models.ImageField(upload_to='carousel', blank=True, null=True)
    banner = models.ImageField(upload_to='banner', blank=True, null=True)
    mobile = models.CharField(max_length=20)
    mobile2 = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()
    about = models.TextField()
    about2 = models.TextField()
    copyright_year = models.CharField(max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'companyprofile'
        managed = True
        verbose_name = 'CompanyProfile'
        verbose_name_plural = 'CompanyProfile'




STATUS = [
    ('New', 'New'),
    ('Processing', 'Processing'),
    ('Cleared', 'Cleared'),
]

class TalkToUs(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    message = models.TextField()
    email = models.EmailField()
    created = models.DateField(auto_now=True)
    cleared = models.DateField(auto_now=True)
    admin_note = models.TextField(default='a')
    status = models.CharField(max_length=50, choices=STATUS, default='New')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'talktous'
        managed = True 
        verbose_name = 'TalkToUs'
        verbose_name_plural = 'TalkToUs'
    
