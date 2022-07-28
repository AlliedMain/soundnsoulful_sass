from django.urls import path

from core.api import views

urlpatterns = [
    path('default', views.default_song),
    path('home', views.HomeViewAPI.as_view()),
    path('songs', views.SongListAPIView.as_view()),
    path('testimonials', views.TestimonialsAPIView.as_view()),
    path('albums', views.AlbumListAPIView.as_view()),
    path('albums/<slug:slug>', views.AlbumRetrieveAPIView.as_view()),
    path('genres', views.GenreListAPIView.as_view()),
    path('genres/<int:pk>/songs', views.SongsByGenreListAPIView.as_view()),
    path('songs/<int:pk>', views.SongRetrieveAPIView.as_view()),
]
