from django import forms
from django_select2 import forms as s2forms
from account.models import Room
from vcs.models import Repository


class RepositoryCreateForm(forms.ModelForm):
    room = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Repository
        fields = ('name', 'url')
