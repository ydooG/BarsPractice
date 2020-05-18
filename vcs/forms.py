from django import forms

from vcs.models import Repository


class RepositoryCreateForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = '__all__'
