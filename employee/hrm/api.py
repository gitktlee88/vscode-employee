from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class UserAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(token.key)


class UserList(APIView):
    def get(self, request):
        model = Users.objects.all()
        serializer = UsersSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        model = Users.objects.all()
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_user(self, employee_id):
        try:
            model = Users.objects.get(id=employee_id)
            return model
        except Users.DoesNotExist:
            return

    def get(self, request, employee_id):
        if not self.get_user(employee_id):
            return Response(f'User with ID {employee_id}  is Not Found',
                        status=status.HTTP_404_NOT_FOUND)

        serializer = UsersSerializer(self.get_user(employee_id))
        return Response(serializer.data)

    def put(self, request, employee_id):
        if not self.get_user(employee_id):
            return Response(f'User with ID {employee_id}  is Not Found',
                        status=status.HTTP_404_NOT_FOUND)

        serializer = UsersSerializer(self.get_user(employee_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id):
        if not self.get_user(employee_id):
            return Response(f'User with ID {employee_id}  is Not Found',
                        status=status.HTTP_404_NOT_FOUND)
        model = self.get_user(employee_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
