from django.urls import path

from core.api import views

urlpatterns = [
    path('default', views.default_song),
    path('home', views.HomeViewAPI.as_view()),
    path('songs', views.SongListAPIView.as_view()),
    path('testimonials', views.TestimonialsAPIView.as_view()),
    path('sublimals', views.SublimalListAPIView.as_view()),
    path('sublimals/<int:pk>/songs', views.SublimalRetrieveAPIView.as_view()),
    path('categories', views.CategoryListAPIView.as_view()),
    path('categories/<int:pk>/songs', views.SongsByCategoryListAPIView.as_view()),
    path('songs/<int:pk>', views.SongRetrieveAPIView.as_view()),
    path('playlist', views.PlaylistCreateAPIView.as_view()),
    path('playlist/<slug:slug>', views.PlaylistListView.as_view())
]
