from django import forms

from .models import Images
from .models import ImageDecrypt


class ImageForm(forms.ModelForm):
	class Meta:
		model = Images
		fields = ('message', 'key', 'img')

class ImageDecForm(forms.ModelForm):
	class Meta:
		model = ImageDecrypt
		fields = ('EncImage', 'key')