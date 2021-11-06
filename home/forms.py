from django import forms
from django.forms import fields, models
from .models import *
class AddMarkForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=User.objects.filter(user_type=2))
    class Meta:
        model = Marks
        fields = '__all__'