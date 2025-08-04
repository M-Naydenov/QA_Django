from typing import cast

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm, UserChangeForm, AuthenticationForm
from django.db.models import QuerySet

from users.models import Agent, Team, Department, Role

UserModel = get_user_model()

class BaseUserForm(UserCreationForm):

    department = forms.ModelChoiceField(queryset=cast(QuerySet, Department.objects.all()))
    team = forms.ModelChoiceField(queryset=cast(QuerySet, Team.objects.all()))
    role = forms.ModelChoiceField(queryset=cast(QuerySet, Role.objects.all()))

    class Meta:
        model = UserModel
        exclude = ['password']


        labels = {
            'email': 'Company Email',
            'icepor': 'ICEPOR',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'department': 'Department',
            'team': 'Team',
            'tl': 'Team Lead',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your company email...'}),
            'icepor': forms.TextInput(attrs={'placeholder': 'Enter your icepor...'}),
            'first_name' : forms.TextInput(),
            'last_name': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tl'].queryset = cast(QuerySet, Agent.objects.filter(role__work_title='Team Leader'))

class CreateUserForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = UserModel
        exclude = ['icepor', 'first_name' , 'last_name', 'is_active', 'is_superuser','is_staff','groups','last_login','user_permissions','password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['role', 'team', 'tl', 'department']:
            self.fields[field_name].widget.attrs.update({'class': 'selector'})

        for field_name in ['password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'password-wrapper', 'id': field_name})
            self.fields[field_name].widget.attrs.update({'placeholder': 'Enter your chosen password'} if field_name == 'password1' else {'placeholder': 'Confirm you password...'})


class UpdateUserForm(UserChangeForm):
    class Meta(BaseUserForm.Meta):
        model = UserModel
        fields = '__all__'

class LoginForm(forms.Form):

    email = forms.EmailField(label = 'Company Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Enter your company email...', }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'password-wrapper',
        'placeholder': 'Enter your password...',
        'id': 'password',
    }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user=None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user = authenticate(username=email, password=password)

            if not self.user:
                raise forms.ValidationError('Invalid email or password')

            if not self.user.is_active:
                raise forms.ValidationError('Your account is inactive')

            return self.cleaned_data
        return None

    def get_user(self):
        return self.user


