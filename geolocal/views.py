import traceback

from django.shortcuts import render
import adrf.viewsets as viewsets
from django.utils import timezone
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from geolocal.serializer import GeolocalSerializer

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import AllowAny

from geolocal.models import Location 

# Create your views here.

class GeolocalViewSet(viewsets.ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = GeolocalSerializer


    # ----------- STORE METHOD
    # -------------------------------------
    @action(detail=False, methods=['post'])
    async def store(self, request):
        try: 
            serializer = GeolocalSerializer(data=request.data)

            if serializer.is_valid():
                
                latitude = serializer.validated_data.get('latitude')
                longitude = serializer.validated_data.get('longitude')
                
                if not latitude or not longitude:
                    return Response(
                            {
                                "status": 400,
                                "msg": "Ingrese latitud y/o longitud",
                                "error": "Campos nulos"
                            }, status=status.HTTP_400_BAD_REQUEST
                    ) 
                
                # Creation of object 
                current_time = timezone.now()

                await Location.objects.acreate(
                    latitude = latitude,
                    longitude = longitude,
                    date = current_time
                )

                # Broadcast the new location to all connected WebSocket clients
                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    "location_updates",
                    {
                        "type": "location_update",
                        "latitude": latitude,
                        "longitude": longitude,
                    }
                )

                return Response({
                    "status": 200,
                    "msg": "Geolocalización guardada exitosamente"
                    },
                    status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback.print_exc()
            return Response({"Error respondiendo": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                

    # ------------ SHOW METHOD
    # ---------------------------------
    @action(detail=False, methods=['get'])
    def show(self, request):
        # Get all locations and find the latest one
        all_locations = list(Location.objects.all().order_by('-date'))
        
        # Prepare context for template
        latest_location = None
        if all_locations:
            latest = all_locations[0]
            latest_location = {
                "latitude": latest.latitude,
                "longitude": latest.longitude,
                "date": latest.date
            }

        return render(request, 'location_map.html', {
            'latest_location': latest_location
        })
