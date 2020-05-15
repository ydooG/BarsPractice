from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from chat.models import Chat


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'members']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'create'))
        self.helper.form_method = 'post'
