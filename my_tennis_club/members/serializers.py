from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "bigraphy"],

        def update(self, instance, validated_data):
            print("hello")
            password = validated_data.pop('password', None)
            if password:
                instance.set_password(password)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        print("hello 123")
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
