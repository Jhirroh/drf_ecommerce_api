from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Profile
from .serializers import ProfileSerializer, UserSerializer, SignUpSerializer, LoginSerializer


class ProfileViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    lookup_field = 'user__username'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(username=serializer.data['username'], email=serializer.data['email'])
            user.set_password(serializer.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            response = {
                'status': status.HTTP_201_CREATED,
                'token': token.key,
                'user': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, is_created = Token.objects.get_or_create(user=user)
        serializer = LoginSerializer(user)
        response = {
            'token': token.key,
            'user': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = IsAuthenticated
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
