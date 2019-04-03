from django.db import transaction
from rest_framework import serializers
from users.models import User
REFERRAL_CREDITS = 100


class UserSignUpSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        referee_code = attrs.get('referee_code', None)
        if referee_code is not None and not User.objects.filter(referral_code=referee_code).exists():
            raise serializers.ValidationError("Invalid referral code.")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            if validated_data.get('referee_code', None) is not None:
                re
                referee = User.objects.get(referral_code=validated_data['referee_code'])
                referee.add_credits(REFERRAL_CREDITS)
                validated_data['credits'] = REFERRAL_CREDITS
            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.set_referral_code()
            user.save()
            return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'referee_code',)


class InviteEmailSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ('email',)
