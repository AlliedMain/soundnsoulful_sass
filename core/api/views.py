from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.edit import CreateView
from core.models import Playlist, Song
from .serializers import SongSerializer, AlbumSerializer, GenreSerializer, AlbumSongsSerializer, TestimonialsSerializer, PlaylistSerializer


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


class SongsByGenreListAPIView(ListAPIView):
    """
        List of songs by genre
    """
    serializer_class = SongSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        try:
            genre_id = self.kwargs
            return self.model.objects.filter(genre_id=genre_id).order_by('-created_at')
        except:
            return self.model.objects.all().order_by('-created_at')


class AlbumListAPIView(ListAPIView):
    """
        List of albums
    """
    serializer_class = AlbumSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class AlbumRetrieveAPIView(RetrieveAPIView):
    """
        Albums details view with songs
    """
    serializer_class = AlbumSongsSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class GenreListAPIView(ListAPIView):
    """
        List of genres
    """
    serializer_class = GenreSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class SongRetrieveAPIView(RetrieveAPIView):
    """
        Get song details
    """
    serializer_class = SongSerializer
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
        try:
            playlist_id = self.kwargs
            return self.model.objects.filter(playlist_id=playlist_id).order_by('-user')
        except:
            return self.model.objects.all().order_by('-user')



