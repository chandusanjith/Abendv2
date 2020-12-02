from django import forms
from .models import Tutorials
from ckeditor.widgets import CKEditorWidget

class BlogForm(forms.ModelForm):

    class Meta:
        model = Tutorials
        fields = ['body']