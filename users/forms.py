from typing import cast

from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm, UserChangeForm
from django.db.models import QuerySet

from users.models import Agent, Team, Department


class BaseUserForm(UserCreationForm):

    department = forms.ModelChoiceField(queryset=cast(QuerySet, Department.objects.all()))
    team = forms.ModelChoiceField(queryset=cast(QuerySet, Team.objects.all()))
    tl = forms.ModelChoiceField(queryset=cast(QuerySet, Agent.objects.filter(role__work_title='Team Leader')))

    class Meta:
        model = Agent
        fields = '__all__'


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

class CreateUserForm(UserCreationForm):
    class Meta(BaseUserForm.Meta):
        model = Agent
        exclude = ['icepor', 'first_name' , 'last_name', 'is_active', 'is_superuser']

class UpdateUserForm(UserChangeForm):
    class Meta(BaseUserForm.Meta):
        model = Agent
        fields = '__all__'