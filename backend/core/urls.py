from django.urls import path
from .views import CSVUploadView, DashboardStatsView, PDFReportView, EquipmentListView

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('report/pdf/', PDFReportView.as_view(), name='pdf-report'),
    path('equipment/', EquipmentListView.as_view(), name='equipment-list'),
]
