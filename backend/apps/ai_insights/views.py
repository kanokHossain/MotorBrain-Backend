from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AIInsight, VehicleHealthScore
from .serializers import AIInsightSerializer, VehicleHealthScoreSerializer


class AIInsightListView(generics.ListAPIView):
    serializer_class = AIInsightSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = AIInsight.objects.filter(vehicle__owner=self.request.user, is_dismissed=False)
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs


class DismissInsightView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            insight = AIInsight.objects.get(pk=pk, vehicle__owner=request.user)
        except AIInsight.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        insight.is_dismissed = True
        insight.save(update_fields=["is_dismissed"])
        return Response({"detail": "Insight dismissed."})


class VehicleHealthScoreView(generics.ListAPIView):
    serializer_class = VehicleHealthScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = VehicleHealthScore.objects.filter(
            vehicle__owner=self.request.user
        ).order_by("-computed_at")
        vehicle_id = self.request.query_params.get("vehicle")
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs
