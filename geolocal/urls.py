from django.urls import path
from geolocal.views import GeolocalViewSet

urlpatterns = [
    path('api/store/', GeolocalViewSet.as_view({'post': 'store'}), name='geolocal_store'),
    path('api/storee/', GeolocalViewSet.as_view({'post': 'store2'}), name='geolocal_store2'),
    path('api/show/', GeolocalViewSet.as_view({'get': 'show'}), name='geolocal_show'),
    path('api/table/', GeolocalViewSet.as_view({'get': 'table'}), name='geolocal_table'),
    ]

