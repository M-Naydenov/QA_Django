from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import RegisterView, AgentLoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AgentLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]