from django.db import models
import datetime
from django.contrib.auth.models import User



class Book(models.Model):
        name = models.CharField(max_length = 50)
        amount = models.CharField(max_length = 50)
        date = models.DateField(default=datetime.date.today)
        unit = models.IntegerField(default=0)


        def __str__(self):
            return self.name

class Received(models.Model):
        name = models.CharField(max_length = 50)
        amount = models.CharField(max_length = 50)
        date = models.DateField(default=datetime.date.today)
        unit = models.IntegerField(default=0)
        author = models.ForeignKey(User, on_delete=models.CASCADE)

        def __str__(self):
            return self.name


# Create your models here.

class Spent(models.Model):
        name = models.CharField(max_length = 50)
        amount = models.CharField(max_length = 50)
        date = models.DateField(default=datetime.date.today)
        unit = models.IntegerField(default=0)
        author = models.ForeignKey(User, on_delete=models.CASCADE)

        def __str__(self):
            return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   # image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class worktrack(models.Model):
        Sno = models.AutoField(primary_key=True)
        Owner = models.ForeignKey(User, on_delete=models.CASCADE)
        Cust_Name = models.CharField(max_length = 50, blank=True, null=True)
        Work_details = models.CharField(max_length = 200 , blank=True, null=True)
        Total_Amount = models.IntegerField(blank=True, null=True)
        Amount_Paid = models.IntegerField(blank=True, null=True)
        Work_Status = models.CharField(max_length = 50, default="Working")
        Payment_Status = models.CharField(max_length = 50, blank=True, null=True)
        Target_Date = models.DateField(default=datetime.date.today)
        Comments = models.CharField(max_length = 100, blank=True, null=True)
        last_update_date = models.DateTimeField(auto_now_add=True)
        Mobile = models.IntegerField(blank=True, null=True)

        def __str__(self):
            return self.Cust_Name

class marriage(models.Model):
        Sno = models.AutoField(primary_key=True)
        Owner = models.ForeignKey(User, on_delete=models.CASCADE)
        First_name = models.CharField(max_length = 100, blank=True, null=True)
        Surname = models.CharField(max_length = 100, blank=True, null=True)
        DOB = models.DateField(blank=True, null=True)
        Father_name = models.CharField(max_length = 100, blank=True, null=True)
        Father_Occupation = models.CharField(max_length = 100, blank=True, null=True)
        Mother_name = models.CharField(max_length = 100, blank=True, null=True)
        Mother_Occupation = models.CharField(max_length = 100, blank=True, null=True)
        Siblings = models.CharField(max_length = 50, blank=True, null=True)
        Skin_tone = models.CharField(max_length = 20, blank=True, null=True)
        Study = models.CharField(max_length = 100, blank=True, null=True)
        Occupation = models.CharField(max_length = 100, blank=True, null=True)
        Address = models.CharField(max_length = 300, blank=True, null=True)
        Contact_number = models.IntegerField(blank=True, null=True)
        last_update_date = models.DateTimeField(auto_now_add=True)
        Gender = models.CharField(max_length = 10, blank=True, null=True)
        Age = models.IntegerField(blank=True, null=True)
        Height = models.FloatField(max_length = 3, blank=True, null=True)
        Religion = models.CharField(max_length = 20, blank=True, null=True)
        Sub_cast = models.CharField(max_length = 20, blank=True, null=True)
        Denomination = models.CharField(max_length = 50, blank=True, null=True)
        Mother_tongue = models.CharField(max_length = 15, blank=True, null=True)
        Image_profile = models.ImageField(upload_to='images/', blank=True, null=True)




        def __str__(self):
                return self.First_name

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')
