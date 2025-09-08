# customizacoes/urls.py

# Este arquivo define as URLs (endereços) para o seu app 'customizacoes'.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views # Importa o arquivo views.py

# DefaultRouter cria automaticamente as URLs para um ViewSet.
router = DefaultRouter()

# Registra um ViewSet com o router, associando-o a um prefixo de URL.
router.register(r'tipos-customizacao', views.TipoCustomizacaoViewSet)
router.register(r'customizacoes', views.CustomizacaoViewSet)
router.register(r'historico-alteracoes', views.HistoricoAlteracaoViewSet)
router.register(r'dependencias', views.DependenciaViewSet)
router.register(r'documentacao-tecnica', views.DocumentacaoTecnicaViewSet)

# urlpatterns é a lista de padrões de URL que o Django usará.
urlpatterns = [
    # Inclui todas as URLs geradas pelo router.
    path('', include(router.urls)),
]
