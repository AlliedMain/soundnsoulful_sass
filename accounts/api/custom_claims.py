from curses.ascii import US
from operator import mod
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from accounts.api.views import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



from .serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)



        # Add custom claims
        token["user"] = UserSerializer(user, many=False).data

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class UserProjects(ListAPIView):
     serializer_class = UserSerializer
     model = serializer_class.Meta.model
     queryset = model.queryset = model.objects.all()  

