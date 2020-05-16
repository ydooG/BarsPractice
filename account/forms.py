from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db.models import Q
from django_select2 import forms as s2forms

from account.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(required=True, choices=CustomUser.ROLE_CHOICES)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'role')


class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(required=True, choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('role',)


class UserRegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(required=True, choices=CustomUser.ROLE_CHOICES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'role')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RoomForm(forms.Form):
    title = forms.CharField()
    staff = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter((~Q(role=CustomUser.MANAGER)) & Q(room=None) & (~Q(role=None))),
        widget=s2forms.Select2MultipleWidget)

    # def clean(self):
    #     raise forms.ValidationError('Something went wrong')


class AddStaffToRoomForm(forms.Form):
    staff = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter((~Q(role=CustomUser.MANAGER)) & Q(room=None) & (~Q(role=None))),
        widget=s2forms.Select2MultipleWidget)
