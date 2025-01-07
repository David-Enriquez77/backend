
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

#Create Register serializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    #defining serializer fields 
    password = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'password2','first_name', 'last_name','area', 'email' ]
        
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({"Username already exists"})
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords did not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2') #popping field because it does not belong in the model
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
       
       
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'tokens']

    def get_tokens(self, obj):
        return obj.tokens()

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin.')

        return {
            'username': user.username,
            'tokens': user.tokens(),
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
          
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except Exception as e:
            raise ValidationError(f"Error al invalidar el token: {str(e)}")