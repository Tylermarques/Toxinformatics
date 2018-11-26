from django import forms


class UploadFileForm(forms.Form):
    """ Was used for uploading .hmm file, but proved too complicated for MVP model"""
    title = forms.CharField(max_length=50)
    file = forms.FileField()
