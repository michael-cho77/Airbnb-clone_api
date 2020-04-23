from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


# @api_view(['GET', 'POST']) 처럼 동시 허용도 가능
@api_view(['GET'])
def list_rooms(request):
    rooms = Room.objects.all()
    #many=True = 방 전체(리스트단위)를 직렬화가능하게함
    serialized_rooms = RoomSerializer(rooms, many=True)
    return Response(data=serialized_rooms.data)