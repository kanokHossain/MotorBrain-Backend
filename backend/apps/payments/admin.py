from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "currency", "status", "plan", "created_at"]
    list_filter = ["status", "currency", "plan"]
    search_fields = ["user__email", "transaction_id"]
    raw_id_fields = ["user"]
