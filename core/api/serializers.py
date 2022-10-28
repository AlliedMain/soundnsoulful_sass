from rest_framework import serializers

from core.models import Playlist, Song, Sublimal, Testimonials,Category


class SublimalSerializer(serializers.ModelSerializer):
    class Meta:
        model =     Sublimal
        fields = "__all__"


class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    sublimal = SublimalSerializer(many=True)
    category = Categoryserializer()
    url = serializers.SerializerMethodField('get_url')
    #album = serializers.SerializerMethodField('get_joined_album')

    class Meta:
        model = Song
        fields = "__all__"

    def get_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.song.url)

    # def get_joined_artist(self, obj):
    #     return ", ".join([a.name for a in obj.album.all()])


class SublimalSongsSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Sublimal
        fields = "__all__"

class CategorySongsSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)


    class Meta:
        model = Category
        fields ="__all__"

class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields ="__all__"
