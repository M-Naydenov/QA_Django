from django.urls import path

from common.views import IndexView, StarEvalView, ContinueEvalView, OverviewView, ProcessKnowledgeView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('pkt/', ProcessKnowledgeView.as_view(), name='process_knowledge_test'),
]