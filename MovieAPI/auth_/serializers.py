from rest_framework import serializers
from auth_.models import MainUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=MainUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MainUser
        fields = ('user_name', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = MainUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_name=validated_data['user_name']
        )
        return user
