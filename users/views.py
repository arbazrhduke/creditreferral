from rest_framework.views import APIView
from users.serializers import (UserSignUpSerializer, InviteEmailSerializer,)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class SignUpView(APIView):

    def post(self, request, *args, **kwargs):
        print("REQUEST DATA")
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "You have signed up successfully"}, status=status.HTTP_200_OK)


class InviteUserView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = InviteEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pass
        return Response({}, status=status.HTTP_200_OK)



