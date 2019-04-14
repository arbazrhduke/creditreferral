from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import SuperUserPermission
from users.serializers import (UserSignUpSerializer, InviteEmailSerializer, UserSerializer, )
from users.tasks import invite_email
from users.models import User


class SignUpView(APIView):
    """Signup View handles signup process for the application"""

    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "You have signed up successfully"},
                        status=status.HTTP_201_CREATED)


class ListUserView(APIView):
    """ Lists Users for Admin/Superuser"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (SuperUserPermission,)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InviteUserView(APIView):
    """ Used to Invite a user to signup using referral code."""
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
        return Response({"message": "Invites sent successfully"},
                        status=status.HTTP_200_OK)
