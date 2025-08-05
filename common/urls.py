from django.urls import path

from common.views import IndexView, access_denied_view

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('access-denied/', access_denied_view, name='access-denied')
]