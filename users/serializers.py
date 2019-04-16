from django.conf import settings
from django.db import transaction
from rest_framework import serializers

from users.exceptions import RetryAgainException
from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    """Handles Signup creates a user and adds credits based on referral code and generates referral code for new user"""

    def validate_referee_code(self, referee_code):
        """Validates a referee code if used while signup is valid or not"""
        if referee_code is not None and not User.objects.filter(referral_code=referee_code).exists():
            raise serializers.ValidationError("Invalid referral code.")
        return referee_code

    def set_password(self, user):
        """Used to set password for new user using django user set_password method"""
        user.set_password(user.password)
        user.save()
        return user

    def generate_referral_code(self, user):
        """Used to generate referral code for new user"""
        return user.generate_referral_code()

    def add_credits_to_referee_and_user(self, user):
        """Checks if user signed up using referee code and add credits to referee and user"""
        if user.referee_code is not None:
            referee = User.objects.get(
                referral_code=user.referee_code)
            # user who invited gets credits for signing up this user
            updated = referee.add_credits(settings.REFERRAL_CREDITS)  # adding credits to referee using optimistic lock.
            if not updated:
                raise RetryAgainException
            user.credits += settings.REFERRAL_CREDITS  # adding credits to new user
            user.save()
            return user
        return user

    def post_create_user(self, user):
        """Called after user is created to perform set_password, generate referral code for new user, Add credits
        to new user and referee if user signed up using referee code"""
        user = self.set_password(user)
        user = self.generate_referral_code(user)
        user = self.add_credits_to_referee_and_user(user)
        return user

    @transaction.atomic  # Adding block under transaction to avoid incomplete database updates.
    def create(self, validated_data):
        """Overriding serializer create method to perform required operations after create user"""
        user = User.objects.create(**validated_data)  # creating a user
        user = self.post_create_user(user)
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
