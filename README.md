# Aula de soporte: CRUD MVC con Django

Aplicación web educativa para administrar **clientes** y sus **tickets de soporte**. El proyecto ilustra una solución completa de persistencia de datos con Django: un cliente puede registrar requerimientos, consultarlos, actualizarlos y eliminarlos desde una interfaz web.

## Cobertura de resultados de aprendizaje

| Tema solicitado | Evidencia en el proyecto |
| --- | --- |
| Aplicación web MVC conectada a datos (6, 6.1) | `clients/models.py` define la capa de datos; `views.py` recibe peticiones y entrega templates, que representan la vista. Django coordina el controlador mediante URLconf y vistas. |
| CRUD sobre modelos (6.2) | Clientes y tickets tienen listar, crear, editar y eliminar. |
| ORM para CRUD (6.3) | `Client.objects.all()`, `form.save()`, `get_object_or_404(...)+form.save()` y `instance.delete()` se encuentran comentados en `clients/views.py`. |
| Interacción app, modelos y vistas | La app `clients` está registrada en `INSTALLED_APPS`; sus URLs se incluyen desde `support_manager/urls.py`; `Ticket` tiene una `ForeignKey` hacia `Client`. |
| CSRF | Todos los formularios que modifican datos incluyen `{% csrf_token %}`. La prueba de clientes comprueba que Django rechaza un POST sin token. |
| Enrutamiento y parámetros | `clients/urls.py` define rutas nombradas y rutas con `<int:id>` para editar y eliminar registros. |
| Calidad verificable | Las pruebas automatizadas validan listado, creación, modificación, eliminación, redirecciones, relación y protección CSRF. |

## Arquitectura MVC en Django

```text
Navegador → urls.py → views.py → ModelForm / ORM → SQLite
                         ↓
                  templates/clients/*.html → HTML
```

En la terminología de Django, la capa de templates es la vista y las funciones en `views.py` desempeñan la coordinación de solicitudes que normalmente se asocia al controlador MVC.

## Modelos y relación

- `Client`: nombre, correo único, teléfono y fecha de creación.
- `Ticket`: cliente asociado, título, descripción, estado y fecha de creación.
- La relación `Ticket.client` es uno-a-muchos: al borrar un cliente se borran sus tickets mediante `CASCADE`.

## Ejecución local

Se requiere Python 3.13 o compatible.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd support_manager
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abra `http://127.0.0.1:8000/clients/`, `http://127.0.0.1:8000/tickets/` o el panel `http://127.0.0.1:8000/admin/`.

## Docker

El repositorio incluye los cuatro elementos solicitados:

- `Dockerfile`: imagen Python ligera con Django.
- `docker-compose.yml`: expone el aula en el puerto 8000 y mantiene SQLite en un volumen.
- `.dockerignore`: excluye secretos, Git, entornos virtuales y artefactos locales de la imagen.
- `docker/entrypoint.sh`: aplica migraciones y crea el superusuario sin interacción si se configuran sus variables.

1. Copie `.env.example` como `.env` y reemplace la contraseña de ejemplo.
2. Inicie el servicio:

```bash
docker compose up --build
```

Con las variables `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` y `DJANGO_SUPERUSER_PASSWORD` presentes, el *entrypoint* crea el administrador en el primer arranque. Si se omiten, el sitio arranca normalmente sin crear usuarios. La base queda en el volumen `sqlite_data`.

Para detenerlo:

```bash
docker compose down
```

## Pruebas

```bash
cd support_manager
python manage.py test
python manage.py check
```

## Mapa de rutas

| Recurso | Listar | Crear | Editar | Eliminar |
| --- | --- | --- | --- | --- |
| Clientes | `/clients/` | `/clients/create/` | `/clients/edit/<id>/` | `/clients/delete/<id>/` |
| Tickets | `/tickets/` | `/tickets/create/` | `/tickets/edit/<id>/` | `/tickets/delete/<id>/` |
