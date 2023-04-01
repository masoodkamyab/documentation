from django.urls import path
from .views import InspectionDocumentView

urlpatterns = [
    path(
        'inspections/',
        InspectionDocumentView.as_view(),
        name='inspection-document-list',
    ),
    path(
        'inspections/<int:inspection_id>/',
        InspectionDocumentView.as_view(),
        name='inspection-document-detail',
    ),
]
