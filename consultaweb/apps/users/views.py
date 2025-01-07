from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, LoginSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from ...logs.loggers import info_logger, warning_logger, error_logger
from rest_framework_simplejwt.views import TokenRefreshView

class RegisterView(APIView):
    permission_classes = [AllowAny] #allow any user to have access w/o authentication 
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            #logs
            info_logger.info(f"[RegisterView] User registered successfully: {serializer.data.get('username', 'Unknown')}")
            return Response({'status':'Success',"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        #logs
        warning_logger.warning(f"[RegisterView] Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]  #allow any user to have access w/o authentication 
      
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            info_logger.info(f"[LoginView] User logged in: {serializer.validated_data.get('username', 'Unknown')}")
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
       #logs
        warning_logger.warning(f"[LoginView] Login failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        # Obtain refresh token
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
             warning_logger.warning("[LogoutView] Logout failed: Refresh token not provided.")
             return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # invalidate refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidates refresh token to prevent access
            
            info_logger.info(f"[LogoutView] User '{request.user}' logged out successfully.")
            return Response({'status':'Success',"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            error_logger.error(f"[LogoutView] Logout error: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RefreshTokenView(TokenRefreshView):
    pass

# Endpoint view
class ProtectedEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access to this protected resource!"}, status=200)