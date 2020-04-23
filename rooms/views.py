from rest_framework.generics import ListAPIView
from .models import Room
from .serializers import RoomSerializer
from rest_framework.views import APIView


class ListRoomsView(ListAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer