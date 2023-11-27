from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_incidentes, name="lista_incidentes"),
    path("/<int:id>/", views.incidente, name="incidente"),
    path("/cerrar_incidente/<int:id>/", views.cerrar_incidente, name="cerrar_incidente"),
]
