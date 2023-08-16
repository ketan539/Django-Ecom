from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import *



class SignupForm(UserCreationForm):
    contact=forms.CharField(max_length=10,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile Number','type':'number'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'At least 8 characters'}))
    password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Re-Enter your Password'}))


    class Meta:
        model= User
        fields= ('username', 'email','first_name','last_name','password1', 'password2',)
  
    def __init__(self, *args, **kwargs):
        super(SignupForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

  

class ProductReviewForm(forms.ModelForm):
      class Meta:
        model= Review
        fields=('review', 'review_rating')
        widgets={
            'review':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your review'}),
            'review_rating':forms.Select(attrs={'class':'form-control'}),
          
           }
        labels ={
            'review':'Review',
            'review_rating':'Rating'
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=('address','contact','address_status')
        widgets={
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your address'}),
            'contact':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your contact','maxlength':'10'}),
            'address_status':forms.CheckboxInput(attrs={'class':'form-check-input',})
          
           }
        
class ProfileEdit(UserChangeForm):
    class Meta:
        model =User
        fields=('username', 'email','first_name','last_name')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your First name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Last name'}),
          
           }

class PasswordChangingForm(PasswordChangeForm):


    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your old password','type':'password'}))
    new_password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your new password','type':'password','label':'New Password'}))
    new_password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Re-Enter you new password','type':'password'}))

    class Meta:
        model= User
        fields='__all__'

    