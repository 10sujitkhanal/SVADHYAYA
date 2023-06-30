from django.views.generic import TemplateView, DetailView, View
import requests
from django.http import JsonResponse
from Bard import Chatbot
from django.views.decorators.csrf import csrf_exempt
import multiprocessing
from django.shortcuts import render
from django.core.paginator import Paginator



class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queries = {'q': 'django','key': 'AIzaSyC8asuRKYeXBqbobCA2q60R-_3SIiIT3S4', 'maxResults':20}
        api_url = 'https://www.googleapis.com/books/v1/volumes'
        r = requests.get(api_url, params=queries)
        data = r.json()
        context['books'] = data['items']
        return context

class BookDetailView(DetailView):
    template_name = 'core/detail_view.html'
    context_object_name = 'books'

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        queries = {'key': 'AIzaSyC8asuRKYeXBqbobCA2q60R-_3SIiIT3S4'}
        api_url = 'https://www.googleapis.com/books/v1/volumes/'+id
        r = requests.get(api_url, params=queries)
        data = r.json()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        queries = {'key': 'AIzaSyC8asuRKYeXBqbobCA2q60R-_3SIiIT3S4'}
        r1 = requests.get('https://www.googleapis.com/books/v1/volumes/'+id, params=queries)
        books = r1.json()
        api_url = "https://www.googleapis.com/books/v1/volumes?q="+books['volumeInfo']['title']+"&maxResults=10"
        r2 = requests.get(api_url, params=queries)
        similar_books = r2.json()
        # Add custom context data
        context['books'] = books
        context['similar_books'] = similar_books
        return context
    

class ReadOnlineView(DetailView):
    template_name = 'core/read_view.html'
    context_object_name = 'books'

    def get_object(self, queryset=None):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        queries = {'key': 'AIzaSyC8asuRKYeXBqbobCA2q60R-_3SIiIT3S4'}
        api_url = 'https://www.googleapis.com/books/v1/volumes/' + id
        r = requests.get(api_url, params=queries)
        data = r.json()
        
        context['books'] = data
        
        volume_info = data.get('volumeInfo', {})
        context['ISBN'] = volume_info.get('industryIdentifiers', [{}])[0].get('identifier', '')
        
        return context

def process_bard_ai(message):

    api_token = "YAjBxpqmz1Uy3svonTiNxWyAnd0kW45JypomS6bp9obeYIi-ZUnEU-FfmcDbMVgwRG1kyA."

    def run_bard_ai(message, result_queue):
            chatbot = Chatbot(api_token)
            response = chatbot.ask(message)
            print(response)
            answer = response['content']
            result_queue.put(answer)
            
        
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_bard_ai, args=(message, result_queue))
    process.start()
    process.join()

    if process.exitcode == 0:
        answer = result_queue.get()
        return answer
    else:
        return 'Failed to process the request'


@csrf_exempt
def bard_ai(request):
    message = request.GET.get('message')
    answer = process_bard_ai(message)
    return JsonResponse({'answer': answer})
    
class SearchView(View):
    def get(self, request):
        search_keywords = request.GET.get('q')
        queries_book = {'q': search_keywords,'key': 'AIzaSyC8asuRKYeXBqbobCA2q60R-_3SIiIT3S4', 'maxResults':8}
        api_url_book = 'https://www.googleapis.com/books/v1/volumes'
        r_book = requests.get(api_url_book, params=queries_book)
        data_book = r_book.json()
        
        
        api_url_video = "https://simple-youtube-search.p.rapidapi.com/search"

        queries_video = {"query":search_keywords,"type":"video","safesearch":"true"}

        headers = {
            "X-RapidAPI-Key": "97f9f098c5mshd6807dd11fd6f33p1d5cddjsn134c81f9a126",
            "X-RapidAPI-Host": "simple-youtube-search.p.rapidapi.com"
        }
        
        r = requests.get(api_url_video, headers=headers, params=queries_video)
        data_video = r.json()

        context = {
            'search_keywords': search_keywords,
            'books':data_book['items'],
            'videos': data_video['results']
        }
        return render(request, 'search/search.html', context)
    

class BookListView(View):
    def get(self, request):
        search_keywords = request.GET.get('q', 'ramayan')
        max_results = 20
        total_books = 200
        page_number = request.GET.get('page', 1)
        total_requests = (total_books + max_results - 1) // max_results

        api_url = 'https://www.googleapis.com/books/v1/volumes'
        all_books = []
        
        for i in range(total_requests):
            start_index = i * max_results
            params = {
                'q': search_keywords,
                'key': 'AIzaSyC8asuRKYeXBqbobCA2q60R-_3SIiIT3S4',
                'maxResults': max_results,
                'startIndex': start_index
            }
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                books = data.get('items', [])
                all_books.extend(books)

        paginator = Paginator(all_books, max_results)
        page_obj = paginator.get_page(page_number)

        context = {
            'search_keywords': search_keywords,
            'total_items': total_books,
            'books': page_obj,
        }
        return render(request, 'core/book_list.html', context)
    
    
# class PresentationPageView(TemplateView):
#     template_name = 'presentation/presentation.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         answer = process_bard_ai("")
#         context['books'] = data['items']
#         return context