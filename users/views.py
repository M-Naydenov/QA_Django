from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreateUserForm, LoginForm

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


class ProfileView:
    pass

class MyTeamView:
    pass