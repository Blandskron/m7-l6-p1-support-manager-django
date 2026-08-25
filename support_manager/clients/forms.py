from django import forms
from .models import Client, Ticket

# Formularios basados en ORM (MVC - capa vista/modelo)
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del cliente'}),
            'phone': forms.TextInput(attrs={'placeholder': '+56 9 1234 5678'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['client', 'title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Resumen del requerimiento'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
