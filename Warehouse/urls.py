from django.urls import path
from .views import MaterialReportView

urlpatterns = [
    path('materials/', MaterialReportView.as_view(), name='material-report'),
]
