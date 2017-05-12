from django import forms

class ImageForm(forms.Form):
    image = forms.ImageField()

class FileForm(forms.Form):
    file = forms.FileField()
