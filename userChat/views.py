from .models import *
import random
from rest_framework import status
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
        user=UserEx.objects.create(
            username=username,
            email=email,
            password=password
        )
        refresh = RefreshToken.for_user(user)
        user.save()
        return JsonResponse(
            {
                'Success':'user has successfully added',
                'user_id':user.id,
                'username':user.username,
                "email":user.email,
                "JWT_accessToken" :str(refresh.access_token),
                "JWT_refreshToken" :str(refresh),
            }
        )
        
        