from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.http  import HttpResponse

from utils.song_utils import generate_key
from .forms import *
from tinytag import TinyTag


def home(request):
    context = {
        'sublimal': Sublimal.objects.all()[:6],
        'categories': Category.objects.all()[:6],
        'latest_songs': Song.objects.all()[:6]
    }
    return render(request, "home.html", context)

def instructions(request):
    return render(request, "songs/instructions.html")

def contact(request):
    return render(request, "contact/index.html")
def listeningtips(request):
    return render(request, "contact/listeningtips.html")


class SongUploadView(CreateView):
    form_class = SongUploadForm
    template_name = "songs/create.html"

    @method_decorator(login_required(login_url=reverse_lazy('core:home')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context['sublimal'] = Sublimal.objects.all()
        context['category'] = Category.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(SongUploadView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        song = TinyTag.get(self.request.FILES['song'].file.name)
        form.instance.audio_id = generate_key(15, 15)
        form.instance.user = self.request.user
        form.instance.playtime = song.duration
        form.instance.size = song.filesize
        sublimal = []
        for a in self.request.POST.getlist('sublimal[]'):
            try:
                sublimal.append(int(a))
            except:
                sublimal = sublimal.objects.create(name=a)
                sublimal.append(sublimal)
        form.save()
        form.instance.artists.set(sublimal)
        form.save()
        data = {
            'status': True,
            'message': "Successfully submitted form data.",
            'redirect': reverse_lazy('core:upload-details', kwargs={'audio_id': form.instance.audio_id})
        }
        return JsonResponse(data)


class SongDetailsView(DetailView):
    model = Song
    template_name = 'songs/show.html'
    context_object_name = 'song'
    slug_field = 'audio_id'
    slug_url_kwarg = 'audio_id'



def affirmations(request, song_id):
    aff = Song.objects.get(audio_id=song_id).affirmations
    return HttpResponse(aff)



class CategoryListView(ListView):
    model = Category
    template_name = 'Categorys/index.html'
    context_object_name = 'Categorys'

# class AffirmationsListView(ListView):
#     model = Song
#     template_name = 'Categorys/index.html'
#     context_object_name = 'Categorys'


class SongsByCategoryListView(DetailView):
    model = Category
    template_name = 'Categorys/songs-by-Category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(SongsByCategoryListView, self).get_context_data(**kwargs)
        context['songs'] = self.get_object().song_set.all
        return context

class SongsBySublimalListView(DetailView):
    model = Sublimal
    template_name = 'sublimal/songs-by-Category.html'
    context_object_name = 'sublimal'

    def get_context_data(self, **kwargs):
        context = super(SongsBySublimalListView, self).get_context_data(**kwargs)
        context['songs'] = self.get_object().song_set.all
        return context



class SublimalListView(ListView):
     model = Sublimal
     template_name = 'sublimal/index.html'
     context_object_name = 'sublimal'


class SublimalDetailView(DetailView):
    model = Sublimal
    template_name = 'sublimal/show.html'
    context_object_name = 'sublimal'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(SublimalDetailView, self).get_context_data(**kwargs)
        context['sublimal'] = self.get_object().songs.all()
        return context

class TestimonialsDetailView(DetailView):
    model = Testimonials
    template_name = 'testimonials/show.html'
    context_object_name = 'testimonials'

    def get_context_data(self, **kwargs):
        context = super(TestimonialsDetailView, self).get_context_data(**kwargs)
        context['testimonials'] = self.get_object().testimonials.all()
        return context


class PlaylistCreateView(CreateView):
    form_class = PlaylistForm
    http_method_names = ['post']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlaylistCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                'status': True,
                'message': "Please login first",
                'redirect': None
            }
            return JsonResponse(data=data)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def favoriteunfavorite(request):
    if request.method == "POST":
        if request.POST.get('decision') == 'make':
            song = Song.objects.get(id=request.POST.get('song_id'))
            if not Playlist.objects.filter(user=request.user, song=song).exists():
                Playlist.objects.create(user=request.user, song=song)
                data = {
                    'status': True,
                    'message': "Song marked in Favourite",
                    'redirect': None
                }
                return JsonResponse(data)
            else:
                data = {
                    'status': True,
                    'message': "Already favorite",
                    'redirect': None
                }

                return JsonResponse(data)
        else:
            song = Song.objects.get(id=request.POST.get('song_id'))
            Playlist.objects.filter(user=request.user, song=song).delete()
            data = {
                'status': True,
                'message': "Song unfavorited",
                'redirect': None
            }
            return JsonResponse(data)
    else:
        data = {
            'status': False,
            'message': "Method not allowed",
            'redirect': None
        }

        return JsonResponse(data)


class UnFavoriteView(DeleteView):
    model = Playlist;

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        data = {
            'status': True,
            'message': "Song unfavorited.",
            'redirect': None
        }

        return JsonResponse(data)
