from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "amount", "currency", "status", "plan",
            "payment_provider", "transaction_id", "receipt_url",
            "notes", "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]
