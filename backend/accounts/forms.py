from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import Note





class AddNote(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Title", "class":"form-control"}), label="")
    body = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Enter Notes...", "class":"form-control"}), label="")
    class Meta:
        model = Note
        exclude = ('user', 'archive', 'trash', 'pin', 'created_at', 'updated_at')