from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




#DataFlair
class BookCreate(forms.ModelForm):
        class Meta:
            model = Book
            fields = '__all__'

class ReceivedCreate(forms.ModelForm):
        class Meta:
            model = Received
            fields = ['name', 'amount', 'unit']




class SpentCreate(forms.ModelForm):
        class Meta:
            model = Spent
            fields = ['name', 'amount', 'unit']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class worktrackCreate(forms.ModelForm):

    class Meta:
        model = worktrack
        fields = ['Sno', 'Cust_Name', 'Work_details', 'Total_Amount', 'Amount_Paid', 'Work_Status', 'Payment_Status', 'Target_Date','Mobile']



class mrgtrackCreate(forms.ModelForm):

    class Meta:
        model = marriage
        fields = ['Sno', 'First_name', 'Surname', 'DOB', 'Father_name', 'Father_Occupation', 'Mother_name', 'Mother_Occupation', 'Siblings', 'Skin_tone', 'Study', 'Occupation','Address', 'Contact_number',  'Gender', 'Age', 'Height', 'Religion', 'Sub_cast',  'Denomination', 'Mother_tongue','Image_profile']




