from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class StarEvalView(TemplateView):
    template_name = 'evaluation/start-evaluation.html'

class ContinueEvalView(TemplateView):
    template_name = 'evaluation/continue-evaluation.html'

class RegisterView(TemplateView):
    template_name = 'user/register.html'

class OverviewView(TemplateView):
    template_name = 'evaluation/overview.html'

class ProcessKnowledgeView(TemplateView):
    template_name = 'pkt/process-knowledge-test.html'