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
