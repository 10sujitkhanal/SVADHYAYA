from django.urls import path
from .views import HomePageView, BookDetailView, ReadOnlineView, bard_ai, SearchView, BookListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('book/<str:pk>/', BookDetailView.as_view(), name='detail_view'),
    path('book/read/<str:pk>/', ReadOnlineView.as_view(), name='detail_online_view'),
    path('bardai/response/', bard_ai, name='chat'),
    path('search/', SearchView.as_view(), name='search'),
    path('books/list/', BookListView.as_view(), name='book_list'),
]