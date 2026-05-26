from django.urls import path
from consulta.views import buscar_cadeado


urlpatterns = [
    path('', buscar_cadeado, name='buscar_cadeado'),
]