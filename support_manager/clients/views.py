from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Ticket
from .forms import ClientForm, TicketForm

# =========================
# CRUD CLIENTES
# =========================

# SELECT (ORM)
def client_list(request):
    clients = Client.objects.all()  # Selección de registros
    return render(request, 'clients/client_list.html', {'clients': clients})


# CREATE (ORM)
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()  # Creación de registro
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})


# UPDATE (ORM)
def client_update(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()  # Modificación de registro
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form})


# DELETE (ORM)
def client_delete(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()  # Eliminación de registro
        return redirect('client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})


# =========================
# CRUD TICKETS
# =========================

def ticket_list(request):
    # select_related evita una consulta adicional por cada cliente mostrado.
    tickets = Ticket.objects.select_related('client').all()  # SELECT (ORM)
    return render(request, 'clients/ticket_list.html', {'tickets': tickets})


def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'clients/ticket_form.html', {'form': form})


def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'clients/ticket_form.html', {'form': form})


def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'clients/ticket_confirm_delete.html', {'ticket': ticket})
