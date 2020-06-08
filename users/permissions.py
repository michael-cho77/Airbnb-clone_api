from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):

    # 특정 대상(한개)를 찾기위한 has_object_permission
    def has_object_permission(self, request, view, user):
        return user == request.user