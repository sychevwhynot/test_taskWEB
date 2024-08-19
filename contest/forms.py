from django import forms

from .models import Participant


class ParticipantForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Participant
        fields = ['name', 'email', 'code']
