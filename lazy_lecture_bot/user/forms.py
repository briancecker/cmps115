from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

"""""""""""""""""""""
 
  Login Form

"""""""""""""""""""""
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError("Sorry, that login was invalid. Try again.")
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user

"""""""""""""""""""""		

  Registration Form

"""""""""""""""""""""
class RegistrationForm(forms.Form):
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)

	def clean_username(self): # Checks to see if user already exists	
		try:
			user = User.objects.get(username__iexact = self.cleaned_data.get('username'))
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError('That username already exists, try another one.')

	def clean(self): # Validates the Password
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if(password != confirm_password):
			raise forms.ValidationError("Passwords do not match!")
		return self.cleaned_data