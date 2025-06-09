from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JugadorViewSet, PagoViewSet, CategoriaViewSet, YoView, JugadorFiltradoViewSet

router = DefaultRouter()
router.register(r'jugadores', JugadorViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'categorias', CategoriaViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('yo/', YoView.as_view(), name='yo'),
    path('jugadores/mis_jugadores/', JugadorFiltradoViewSet.as_view({'get': 'mis_jugadores'})),
]