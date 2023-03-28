
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main,  name='main'),
    path('quotes/', views.quotes, name='quotes'),
    path('authors/', views.authors, name='authors'),
    path('about/<int:author_id>', views.about, name='about'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('t_quotes/<int:tag_id>', views.t_quotes, name='t_quotes'),
]
