from django import forms
from .models import *

class NotesForm(forms.ModelForm):
    
    class Meta:
        model = Notes
        fields = ['title','description']


class HomeworkForm(forms.ModelForm):
    
    class Meta:
        model = Homework
        fields = ['subject','title','description','is_finish']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Search")


class TodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ['title','is_finish']

Language =(
        ('da', 'Danish'),
        ("en", "English"),
        ('fr', 'French'),
        ('de', 'German'),
        ('el', 'Greek'),
        ("gu", "Gujarati"),
        ("hi", "Hindi"),
        ('id', 'Indonesian'),
        ('it', 'Italian'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('ml', 'Malayalam'),
        ('ne', 'Nepali'),
        ('pa', 'Punjabi'),
        ('ro', 'Romanian'),
        ('ru', 'Russian'),
        ('sd', 'Sindhi'),
        ('es', 'Spanish'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('th', 'Thai'),
        ('tr', 'Turkish'),
        ('ur', 'Urdu'),
        ('yo', 'Yoruba'),
        ('zu', 'Zulu')
    )

class TranslateForm(forms.Form):

        text = forms.CharField(widget=forms.Textarea)
        lang = forms.ChoiceField(choices = Language)

