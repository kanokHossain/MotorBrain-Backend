from django.urls import path
from .views import AIInsightListView, DismissInsightView, VehicleHealthScoreView

urlpatterns = [
    path("", AIInsightListView.as_view(), name="ai-insight-list"),
    path("<int:pk>/dismiss/", DismissInsightView.as_view(), name="ai-insight-dismiss"),
    path("health-scores/", VehicleHealthScoreView.as_view(), name="vehicle-health-scores"),
]
