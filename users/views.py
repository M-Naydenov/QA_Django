from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import CreateUserForm, LoginForm, UpdateUserForm, UpdateProfileForm

UserModel = get_user_model()

# Create your views here.
class RegisterView(CreateView):
    model = UserModel
    form_class = CreateUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')

class AgentLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True


class ProfileView(UpdateView):
    model = UserModel
    form_class = UpdateProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('profile')
    success_message = 'Profile updated successfully'


    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        if form.cleaned_data.get('new_password'):
            update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class MyTeamView:
    pass