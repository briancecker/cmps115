from django import forms
from django.contrib.auth.models import User

"""""""""""""""""""""

	Video Upload Form

"""""""""""""""""""""
class VideoUploadForm(forms.Form):
	video = forms.FileField()
	title = forms.CharField(max_length = 50)
	description = forms.CharField()
	public_access = forms.BooleanField(widget=forms.RadioSelect())