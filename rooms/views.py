from rest_framework.decorators import api_view
from rest_framework.response import Response


# @api_view(['GET', 'POST']) 처럼 동시 허용도 가능
@api_view(['GET'])
def list_rooms(request):
    return Response()