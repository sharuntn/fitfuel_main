# accounts/forms.py
from django import forms
from base.models import Image
 
 
class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)

