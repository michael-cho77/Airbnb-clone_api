from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner


class RoomViewSet(ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):

        #list는 get과 같은 즉 /rooms
        # retrieve는 /rooms 또는 /room/1 과 같음 
        if self.action =="list" or self.action == "retrieve":
            # AllowAny 누구나 요청가능함
            permission_classes = [permissions.AllowAny]
        #crete = "POST"
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
        '''
        called_perm = []
        for p in permission_classes:
            called_perm.append(p())
            를 한줄로 축약한것
        '''



@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    # print(filter_kwargs) 
            #{'price__lte':30, 'beds_gte':2 ...}
    # print(*filter_kwargs) 
            # price__lte beds_gte
    #print(**filter_kwargs)
            # price__lte='30', beds_gte='2', bathrooms__gte='2' filter()에서 사용가능하게 출력됨(Doble expansion or unpacking)
    paginator = OwnPagination()
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005  #왼쪽
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer  = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)