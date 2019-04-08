from django.conf import settings
from django.db import transaction
from rest_framework import serializers

from users.exceptions import RetryAgainException
from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        referee_code = attrs.get('referee_code', None)
        if referee_code is not None and not User.objects.filter(
                referral_code=referee_code).exists():
            raise serializers.ValidationError("Invalid referral code.")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            if validated_data.get('referee_code', None) is not None:
                referee = User.objects.get(
                    referral_code=validated_data['referee_code'])
                updated = referee.add_credits(settings.REFERRAL_CREDITS)
                if not updated:
                    raise RetryAgainException
                validated_data['credits'] = settings.REFERRAL_CREDITS
            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.set_referral_code()
            user.save()
            return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',
                  'referee_code',)


class InviteEmailSerializer(serializers.ModelSerializer):
    emails = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = User
        fields = ('emails',)
