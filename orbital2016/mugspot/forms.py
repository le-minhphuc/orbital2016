from django import forms
from .models import Person
from django.contrib.auth.models import User

class UserRegisterForm(forms.Form):
	username = forms.CharField(label='User name',widget=forms.TextInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;'}), max_length=200)
	user_email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;'}), max_length=254)
	user_faculty = forms.CharField(label='Faculty',widget=forms.TextInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;'}), max_length=200)
	user_password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;border:0px;'}), max_length=200)
	user_password_re = forms.CharField(label='Retype Password', widget=forms.PasswordInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;border:0px;'}), max_length=200)

	def clean(self):
		super(UserRegisterForm, self).clean()
		password = self.cleaned_data.get("user_password")
		password_re = self.cleaned_data.get("user_password_re")

		if password and password_re:
			# Only do something if both fields are valid so far
			if password != password_re:
				raise forms.ValidationError(
					"Your passwords do not match."
					)
		return self.cleaned_data # Why does this work????

class UserLoginForm(forms.Form):
	user_name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;'}), max_length=200)
	user_password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'style': 'width:100%;height:20px;border-radius:30px;border:0px;'}), max_length=200)

class AccountDetailForm(forms.Form):
	user_name = forms.CharField(label='Username', max_length=200)
	user_email = forms.EmailField(label='Email', max_length=254)
	user_faculty = forms.CharField(label='Faculty', max_length=200)
	class Meta:
		model = User # Specify the model that this form is related to? 
		fields = ['user_name', 'user_email', 'user_faculty']
		widgets = {
			'user_name': forms.TextInput(
					attrs={'id':'User-username', 'required':False, 'style': 'width:100%;height:20px;border-radius:30px;border:0px;',}
				),
			'user_email': forms.EmailInput(
					attrs={'id':'User-useremail', 'required':False, 'style': 'width:100%;height:20px;border-radius:30px;border:0px;',}
				),
			'user_faculty': forms.TextInput(
					attrs={'id':'User-userfaculty', 'required':False, 'style': 'width:100%;height:20px;border-radius:30px;border:0px;',}
				),
		}


class LocationForm(forms.Form):
	user_location = forms.CharField(label='Location', max_length=200)
