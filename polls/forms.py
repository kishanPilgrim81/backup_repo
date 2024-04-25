from django import forms
from .models import Profile


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('customer_id', 'profile_image')