from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm) :
	name = forms.CharField(max_length=128,
			help_text="Please enter category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(),
			initial = 0)
	likes = forms.IntegerField(widget=forms.HiddenInput(),
			initial = 0)

	# Inline class to provide additional information on the form.
	class Meta:
		#Associate it to the model
		model = Category

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128,
			help_text = "Please enter the title name.")
	url = forms.URLField(max_length=200,
			help_text = "Please enter a valid URL.")
	views = forms.IntegerField(widget=forms.HiddenInput(),
			initial = 0)

	class Meta:
		model = Page

		#Manual specify the fields to be shown in the form
		fields = ('title', 'url', 'views')

from rango.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    username = forms.CharField(
                    help_text="Username"
                    )
                    
    email = forms.CharField(
                    help_text="Email"
                    )
                    
    password = forms.CharField(
                    widget=forms.PasswordInput(),
                    help_text="Password"
                    )
    
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(
                    help_text="Website",
                    required=False
                    )
    
    picture = forms.ImageField(
                    help_text="Profile Image",
                    required=False
                    )
    
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        