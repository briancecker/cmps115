from mimetypes import MimeTypes # Useful for guessing the filetype
import uuid

from django import forms
from django.contrib.auth.models import User

"""""""""""""""""""""

	Video Upload Form

"""""""""""""""""""""
class VideoUploadForm(forms.Form):
	
	video_file = forms.FileField(
		label='Upload Video',
		help_text='max is 1GB'
		)
	title = forms.CharField(max_length = 50)
	description = forms.CharField(widget=forms.Textarea)
	public_access = forms.TypedChoiceField(
						widget=forms.RadioSelect, 
						choices=((True, 'Public'),
								 (False, 'Private')),
					)