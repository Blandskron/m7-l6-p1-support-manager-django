from django.test import TestCase
from django.urls import reverse

from .models import Client, Ticket


class ClientCrudTests(TestCase):
    def setUp(self):
        self.client_record = Client.objects.create(
            name='Ada Lovelace', email='ada@example.com', phone='+56 9 1111 2222'
        )

    def test_list_uses_orm_and_displays_clients(self):
        response = self.client.get(reverse('client_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.client_record.name)

    def test_create_client_requires_csrf_and_persists_data(self):
        csrf_client = self.client_class(enforce_csrf_checks=True)
        url = reverse('client_create')
        response = csrf_client.post(url, {
            'name': 'Grace Hopper', 'email': 'grace@example.com', 'phone': '+56 9 3333 4444'
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.post(url, {
            'name': 'Grace Hopper', 'email': 'grace@example.com', 'phone': '+56 9 3333 4444'
        })
        self.assertRedirects(response, reverse('client_list'))
        self.assertTrue(Client.objects.filter(email='grace@example.com').exists())

    def test_update_and_delete_client_use_parameterized_routes(self):
        update_url = reverse('client_update', args=[self.client_record.id])
        response = self.client.post(update_url, {
            'name': 'Ada Byron', 'email': 'ada@example.com', 'phone': '+56 9 9999 0000'
        })
        self.assertRedirects(response, reverse('client_list'))
        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.name, 'Ada Byron')

        response = self.client.post(reverse('client_delete', args=[self.client_record.id]))
        self.assertRedirects(response, reverse('client_list'))
        self.assertFalse(Client.objects.filter(id=self.client_record.id).exists())


class TicketCrudTests(TestCase):
    def setUp(self):
        self.client_record = Client.objects.create(
            name='Linus Torvalds', email='linus@example.com', phone='+56 9 5555 6666'
        )
        self.ticket = Ticket.objects.create(
            client=self.client_record, title='No puedo acceder', description='El acceso falla.'
        )

    def test_ticket_crud(self):
        response = self.client.post(reverse('ticket_create'), {
            'client': self.client_record.id,
            'title': 'Restablecer contraseña',
            'description': 'Solicito ayuda para ingresar.',
            'status': 'OPEN',
        })
        self.assertRedirects(response, reverse('ticket_list'))
        new_ticket = Ticket.objects.get(title='Restablecer contraseña')

        response = self.client.post(reverse('ticket_update', args=[new_ticket.id]), {
            'client': self.client_record.id,
            'title': new_ticket.title,
            'description': new_ticket.description,
            'status': 'CLOSED',
        })
        self.assertRedirects(response, reverse('ticket_list'))
        new_ticket.refresh_from_db()
        self.assertEqual(new_ticket.status, 'CLOSED')

        response = self.client.post(reverse('ticket_delete', args=[new_ticket.id]))
        self.assertRedirects(response, reverse('ticket_list'))
        self.assertFalse(Ticket.objects.filter(id=new_ticket.id).exists())

# Create your tests here.
