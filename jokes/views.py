from django.views.generic import TemplateView, DetailView, View
import requests
from django.shortcuts import render
from django.http import JsonResponse

class JokesView(View):
    def get(self, request):
        url = "https://joke110.p.rapidapi.com/random_joke"
        headers = {
            "X-RapidAPI-Key": "97f9f098c5mshd6807dd11fd6f33p1d5cddjsn134c81f9a126",
            "X-RapidAPI-Host": "joke110.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        context= {
            'results':response.json()
        }
        return render(request, 'jokes/home.html', context)
    
    def post(self, request):
        url = "https://joke110.p.rapidapi.com/random_joke"
        headers = {
            "X-RapidAPI-Key": "97f9f098c5mshd6807dd11fd6f33p1d5cddjsn134c81f9a126",
            "X-RapidAPI-Host": "joke110.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        
        return JsonResponse({
            'setup': response.json()['setup'],
            'punchline':response.json()['punchline'],
            })