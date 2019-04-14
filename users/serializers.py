from django.conf import settings
from django.db import transaction
from rest_framework import serializers

from users.exceptions import RetryAgainException
from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    """Handles Signup creates a user and adds credits based on referral code"""
    def validate(self, attrs):
        """Does serializer validation and validates if the referee code entered by user is valid or not"""
        referee_code = attrs.get('referee_code', None)  # referee_code is entered by user while sign up.
        if referee_code is not None and not User.objects.filter(
                referral_code=referee_code).exists():
            raise serializers.ValidationError("Invalid referral code.")
        return attrs

    def create(self, validated_data):
        """Handles User Creation and Update Credits for that user uses optimistic  locking a transactions"""
        with transaction.atomic():
            if validated_data.get('referee_code', None) is not None:  # if referee_code was used while signup
                referee = User.objects.get(
                    referral_code=validated_data['referee_code'])
                updated = referee.add_credits(settings.REFERRAL_CREDITS)
                if not updated:
                    raise RetryAgainException
                validated_data['credits'] = settings.REFERRAL_CREDITS  # adding credits to current signing up user.
            user = User.objects.create(**validated_data)  # creating a user
            user.set_password(validated_data['password'])  # setting user password
            user.set_referral_code()  # generating referral code for new user.
            user.save()
            return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',
                  'referee_code',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'referee_code', 'referral_code', 'credits',)


class InviteEmailSerializer(serializers.ModelSerializer):
    emails = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = User
        fields = ('emails',)
