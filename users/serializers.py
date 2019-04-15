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
        """Handles User Creation and Update Credits for that user uses optimistic locking a transactions"""
        with transaction.atomic():
            if validated_data.get('referee_code', None) is not None:  # if referee_code was used while signup
                # user who referred is fetched
                referee = User.objects.get(
                    referral_code=validated_data['referee_code'])
                # user who invited gets credits for signing up this user
                updated = referee.add_credits(settings.REFERRAL_CREDITS)
                if not updated:
                    raise RetryAgainException
            user = User.objects.create(**validated_data)  # creating a user
            user = user.generate_referral_code()
            if user.referee_code is not None:  # if user signed up using someone's referral code he is rewarded credits.
                user = user.add_credits(settings.REFERRAL_CREDITS)
            user.set_password(validated_data['password'])  # setting user password
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
