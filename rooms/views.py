from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer



class OwnPagination(PageNumberPagination):
    page_size = 20


class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        '''
        페이징처리하는 뷰가 많다면 아예 클래스로 선언해도되고 그렇지 않다면 아래처럼 선언해주어야함
        paginator = PageNumberPagination()
        paginator.page_size = 20
        '''
        rooms = Room.objects.all()
        # request를 파싱하는것으로 paginator가 page_queryset을 찾게됨
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        # return Response()에서 아래로 바꾸는것으로 이전 이후 페이지등도 사용가능해짐
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        #print(dir(serializer))
        if serializer.is_valid():
            # save()안에 들어가는 인자는 validated data안에도 들어간다. 
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # (partial=True)는 모든 데이터가 아닌 내가 원하는 데이터만 수정할 수 있다는 의미.
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def room_search(request):
    paginator = OwnPagination()
    rooms = Room.objects.filter()
    results = paginator.paginate_queryset(rooms, request)
    serializers = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)