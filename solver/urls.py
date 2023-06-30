from django.urls import path
from .views import SolverView

urlpatterns = [
    path('', SolverView.as_view(), name='solver'),
]