from .models import *
import random
from rest_framework import status
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
# ============== Views =========================
class RegisterUserAPIView(APIView):
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        if not email and password:
            return JsonResponse({
                'error':"Email and password required"
            },status=status.HTTP_400_BAD_REQUEST)
        if UserEx.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "error" : "email/username is already taken please try something new"
                },status=status.HTTP_400_BAD_REQUEST
            )
        username=email.split('@')[0]
        username+= str(random.randint(111,999))
        user=UserEx.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='registered'
        )
        refresh = RefreshToken.for_user(user)
        user.save()
        return JsonResponse(
            {
                'Success':'user has successfully added',
                'user_id':user.id,
                'username':user.username,
                "role":user.role,
                "email":user.email,
                "JWT_accessToken" :str(refresh.access_token),
                "JWT_refreshToken" :str(refresh),
            }
        )
        
# ================= Login User ===============
class LoginUserAPIView(APIView):
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        if not email and password:
            return JsonResponse(
                {
                    'error':"email/password required.."
                },status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = UserEx.objects.select_related().get(email=email)
            if not user.check_password(password):
                return JsonResponse(
                    {"error": "Invalid email or password."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "success": "Login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "email": user.email,
                    "JWT_accessToken": str(refresh.access_token),
                    "JWT_refreshToken": str(refresh),
                },
                status=status.HTTP_200_OK
            )
        except UserEx.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )