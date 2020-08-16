from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rooms.serializers import RoomSerializer
from rooms.models import Room
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf

import jwt
from django.conf import settings
from django.contrib.auth import authenticate




class UsersViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (self.action == "create" or self.action == "retrieve" or self.action == "favs"):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]

    #데코레이터에서 method를 지정해줄 수 있음
    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        #setting의 secret_key를 통해 토큰의 진위여부를 가림 
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )  # user.pk도 추가로 받아 어떤 유저인지 식별함
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    #detail=True는 users/1과 같이 user와 id가 같이 있을때만 작동함
    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    #확장된 것이기 때문에 (detail=True같은 문법 사용불가), 또한 action에 선언된 detail등의 값을 그대로 따라감
    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()  #self.user인걸 인식하기때문에 object으로 가도 됨
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)



