from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (UserSignUpSerializer, InviteEmailSerializer, )
from users.tasks import invite_email


# Create your views here.


class SignUpView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "You have signed up successfully"},
                        status=status.HTTP_200_OK)


class InviteUserView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = InviteEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.is_secure():
                protocol = "https://"
            else:
                protocol = "http://"
            host = "{}{}".format(protocol, request.get_host())
            invite_email.delay(serializer.data['emails'], request.user.id, host)
        return Response({}, status=status.HTTP_200_OK)
