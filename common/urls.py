from django.urls import path

from common.views import IndexView, StarEvalView, ContinueEvalView, LoginView, RegisterView, OverviewView, \
    ProcessKnowledgeView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('evaluation/', StarEvalView.as_view(), name='evaluation'),
    path('continue_eval/', ContinueEvalView.as_view(), name='continue_eval'),
    path('login/',LoginView.as_view(), name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('overview/', OverviewView.as_view(), name='overview'),
    path('pkt/', ProcessKnowledgeView.as_view(), name='process_knowledge_test'),
]