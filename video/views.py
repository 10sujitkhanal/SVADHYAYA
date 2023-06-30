from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
import requests
from django.core.paginator import Paginator


# Create your views here.
class VideoPageView(TemplateView):
    template_name = 'video/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = "https://simple-youtube-search.p.rapidapi.com/search"

        querystring = {"query":"react js book","type":"video","safesearch":"true"}

        headers = {
            "X-RapidAPI-Key": "97f9f098c5mshd6807dd11fd6f33p1d5cddjsn134c81f9a126",
            "X-RapidAPI-Host": "simple-youtube-search.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        context['videos'] = response.json()['results']
        return context
    
class VideoDetailView(DetailView):
    template_name = 'video/read_view.html'
    context_object_name = 'video'

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        url = "https://simple-youtube-search.p.rapidapi.com/video"

        querystring = {"search":"https://www.youtube.com/watch?v="+id}

        headers = {
            "X-RapidAPI-Key": "97f9f098c5mshd6807dd11fd6f33p1d5cddjsn134c81f9a126",
            "X-RapidAPI-Host": "simple-youtube-search.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()['result']
        return data


class VideoListView(View):
    def get(self, request):
        search_keywords = request.GET.get('q', 'rayaman')
        max_results = 12
        page_number = request.GET.get('page', 1)
        url = "https://simple-youtube-search.p.rapidapi.com/search"

        querystring = {"query":search_keywords,"type":"video","safesearch":"true"}

        headers = {
            "X-RapidAPI-Key": "97f9f098c5mshd6807dd11fd6f33p1d5cddjsn134c81f9a126",
            "X-RapidAPI-Host": "simple-youtube-search.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)

        paginator = Paginator(response.json()['results'], max_results)
        page_obj = paginator.get_page(page_number)

        context = {
            'search_keywords': search_keywords,
            'videos': page_obj,
        }
        return render(request, 'video/video_list.html', context)