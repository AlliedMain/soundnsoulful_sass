from rest_framework import serializers

from core.models import Song, Album, Genre, Testimonials


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(many=True)
    genre = GenreSerializer()
    url = serializers.SerializerMethodField('get_url')
    #album = serializers.SerializerMethodField('get_joined_album')

    class Meta:
        model = Song
        fields = "__all__"

    def get_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.song.url)

    # def get_joined_artist(self, obj):
    #     return ", ".join([a.name for a in obj.album.all()])


class AlbumSongsSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = "__all__"

class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = "__all__"
