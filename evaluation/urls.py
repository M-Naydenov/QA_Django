from django.urls import path

from evaluation import views
from evaluation.views import EvaluationListView, EvaluationCreateView, EditEvaluationView, EvaluationDetailsView, \
    DeleteEvaluationView, SearchEvaluationView

urlpatterns = [
    path('initialize_evaluation/', views.start_evaluation_view, name='start-evaluation'),
    path('finalize_evaluation/', EvaluationCreateView.as_view(), name='finalize-evaluation'),
    path('edit-evaluation/<uuid:uuid_field>/', EditEvaluationView.as_view(), name='edit-evaluation'),
    path('view-evaluation/<uuid:uuid_field>/', EvaluationDetailsView.as_view(), name='view-evaluation'),
    path('delete-evaluation/<uuid:uuid_field>/', DeleteEvaluationView.as_view(), name='delete-evaluation'),
    path('search-evaluation/', SearchEvaluationView.as_view(), name='search-evaluation'),
    path('overview/', EvaluationListView.as_view(), name='overview'),
]