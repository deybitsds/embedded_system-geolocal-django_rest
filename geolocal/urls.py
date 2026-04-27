from django.urls import path
from geolocal.views import GeolocalViewSet

urlpatterns = [
    path('api/store/', GeolocalViewSet.as_view({'post': 'store'}), name='geolocal_store'),
    path('api/show/', GeolocalViewSet.as_view({'get': 'show'}), name='geolocal_show'),
    ]

