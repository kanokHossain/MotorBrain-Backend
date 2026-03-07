from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceCategoryViewSet, MaintenanceRecordViewSet, MaintenanceReminderViewSet

router = DefaultRouter()
router.register(r"categories", MaintenanceCategoryViewSet, basename="maintenance-category")
router.register(r"records", MaintenanceRecordViewSet, basename="maintenance-record")
router.register(r"reminders", MaintenanceReminderViewSet, basename="maintenance-reminder")

urlpatterns = [
    path("", include(router.urls)),
]
