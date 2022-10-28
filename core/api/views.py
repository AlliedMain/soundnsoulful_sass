from unicodedata import name
from rest_framework import status
from accounts.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.edit import CreateView
from core.models import Playlist, Song, Sublimal, Category
from .serializers import CategorySongsSerializer, SongSerializer, SublimalSerializer, Categoryserializer, SublimalSongsSerializer, TestimonialsSerializer, PlaylistSerializer
from core.api import serializers


@api_view(['GET'])
def default_song(request):
    song = Song.objects.filter(type='free')[1]
    serializer = SongSerializer(song, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


class HomeViewAPI(APIView):
    """
        Get various type of data for home
    """

    def get(self, request, format=None):
        song_queryset = Song.objects.all()
        serializer = SongSerializer(data=song_queryset, many=True, context={'request': request})
        serializer.is_valid()

        return Response({'songs': serializer.data})


class SongListAPIView(ListAPIView):
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SongsByCategoryListAPIView(ListAPIView):
    """
        List of songs by Category
    """
    serializer_class = SongSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        try:
            Category_id = self.kwargs
            return self.model.objects.filter(Category_id=Category_id).order_by('-created_at')
        except:
            return self.model.objects.all().order_by('-created_at')


class SublimalListAPIView(ListAPIView):
    """
        List of Sublimals
    """
    serializer_class = SublimalSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SublimalRetrieveAPIView(RetrieveAPIView):
    """
        Sublimals details view with songs
    """
    serializer_class = SublimalSongsSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class CategoryListAPIView(ListAPIView):
    """
        List of Categorys
    """
    serializer_class = Categoryserializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SongRetrieveAPIView(RetrieveAPIView):
    """
        Get song details
    """
    serializer_class = SongSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SongsByCategoryListView(RetrieveAPIView):
    serializer_class = CategorySongsSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()




class TestimonialsAPIView(ListAPIView):
    serializer_class = TestimonialsSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    


class PlaylistCreateAPIView(CreateAPIView):
    
    """   
        Create Playlist details 
    """
    serializer_class = PlaylistSerializer
    fields = "__all__"
    model = serializer_class.Meta.model



class PlaylistListView(ListAPIView):
    serializer_class = PlaylistSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


    def get_queryset(self):
        user = get_object_or_404(User, name=self.kwargs.get('playlist'))
        
        return Playlist.objects.filter(creator=user).order_by('-date_created')

    












