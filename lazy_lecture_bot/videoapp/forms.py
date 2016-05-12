from mimetypes import MimeTypes # Useful for guessing the filetype
import uuid

from django import forms
from django.contrib.auth.models import User

from s3direct.widgets import S3DirectWidget

"""""""""""""""""""""

	Video Upload Form

"""""""""""""""""""""
class VideoUploadForm(forms.Form):
	
	"""video_file = forms.FileField(
		label='Upload Video',
		help_text='max is 1GB',
		)
	"""
	video_file = forms.URLField(widget=S3DirectWidget(
		dest='vids', 
		html=(
			'<div class="s3direct" data-policy-url="{policy_url}">'
            '  <a class="file-link" target="_blank" href="{file_url}">{file_name}</a>'
            '  <a class="file-remove" href="#remove" type="hidden">Remove</a>'
            '  <input class="file-url" type="hidden" value="{file_url}" id="{element_id}" name="{name}" />'
            '  <input class="file-dest" type="hidden" value="{dest}">'
            '  <input class="file-input" type="file" />'
            '  <div class="progress progress-striped active">'
            '    <div class="bar"></div>'
            '  </div>'
            '</div>'
            )
        ))
	title = forms.CharField(max_length = 50)
	description = forms.CharField(widget=forms.Textarea)
	public_access = forms.TypedChoiceField(
						widget=forms.RadioSelect, 
						choices=((True, 'Public'),
								 (False, 'Private')),
					)