from django.contrib import admin
from .models import Client, Ticket


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Administración complementaria al CRUD público."""

    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    ordering = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Facilita revisar y gestionar los tickets desde /admin/."""

    list_display = ("title", "client", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "client__name")
    list_select_related = ("client",)
