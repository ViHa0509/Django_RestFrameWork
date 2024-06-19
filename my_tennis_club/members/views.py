from django.shortcuts import render
from django.template import loader
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, CustomUserSerializer, UserLoginSerializer
from .models import CustomUser
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

def GetCsrfToken(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]  # or SessionAuthentication
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return  CustomUser.objects.all()

    @action(detail=False, methods=['get'], url_path='all')
    def get_all_user(self, request):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='current-user')
    def get_current_user(self, request):
        queryset = request.user
        serializer = CustomUserSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=['put'], url_path='current-user')
    # def get_current_user(self, request):
    #     updated_data = request.data
    #     queryset = request.user
    #     serializer = CustomUserSerializer(queryset, many=False)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='<pk>')
    def get_user(self, request, pk):
        queryset = self.get_queryset()
        user = queryset.filter(pk=pk)
        serializer = CustomUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    @action(detail=False, methods=['post'], url_path="new")
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.filter(username=request.data['username']).first()
            if user:
                if check_password(request.data['password'], user.password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    return Response({'error':'wrong password'})
            else:
                return Response({'error':'user does not exist'})
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
