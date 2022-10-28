from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path('', home, name='home'),
    path('instructions', instructions, name="instructions"),
    path('contact', contact, name="contact"),  
    path('listeningtips',listeningtips, name="listeningtips"),   
    path('sublimals', SublimalListView.as_view(), name='sublimals'),
    path('sublimals/<slug:slug>', SublimalDetailView.as_view(), name='sublimals'),
    path('categories', CategoryListView.as_view(), name='category'),
    path('affirmations/<song_id>', affirmations, name='affirmations'),
    path('categories/<int:pk>', SongsByCategoryListView.as_view(), name='songs-by-category'),
    path('songs/', include([
        path('make-favorite', favoriteunfavorite, name='song-favorite'),
        path('upload', SongUploadView.as_view(), name='upload'),
        path('<slug:audio_id>', SongDetailsView.as_view(), name='upload-details'),

    ])),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
