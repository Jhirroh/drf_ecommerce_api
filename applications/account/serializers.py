from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile


class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Password and Confirm Password must be same')
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'first_name', 'last_name', 'dob', 'avatar')
