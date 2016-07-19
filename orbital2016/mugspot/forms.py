from django import forms
from .models import Person

class UserRegisterForm(forms.Form):
	username = forms.CharField(label='User name', max_length=200)
	user_email = forms.EmailField(label='Email', max_length=254)
	user_faculty = forms.CharField(label='Faculty', max_length=200)
	user_password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=200)
	user_password_re = forms.CharField(label='Retype Password', widget=forms.PasswordInput(), max_length=200)

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
	user_name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'size':'40'}), max_length=200)
	user_password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=200)
