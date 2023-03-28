from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.conf import settings

from .forms import AuthorForm, QuoteForm
from .models import Author, Note, Tag


# Create your views here.

def main(request):
    return render(request, 'quotes/base.html', context={"title": "MY_site"})


def quotes(request):
    quotes = Note.objects.all()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top = Note.objects.all().values('tags').annotate(total=Count('text')).order_by('-total')[:10]
    top_tags = {}
    for tg in top:
        tag = Tag.objects.filter(pk=tg['tags']).get()
        top_tags[tag] = tg['total']
    # print(top_tags)
    return render(request, 'quotes/quotes.html',
                  context={"title": "MY_site/Q", "quotes": quotes, "top_tags": top_tags, 'page_obj': page_obj})


def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes/authors.html',
                  context={"title": "MY_site/A", "authors": authors, 'page_obj': page_obj})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            pic = form.save()
            pic.save()
            return redirect(to="quotes:authors")
    return render(request, 'quotes/add_author.html', context={"form": form})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    form = QuoteForm(instance=Note())

    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Note())
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.get(fullname=request.POST.get('author'))
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes:quotes")
        else:
            return render(request, 'quotes/add_quote.html', {"tags": tags, "authors": authors, 'form': form})
    return render(request, 'quotes/add_quote.html', context={"tags": tags, "authors": authors, 'form': form})


def about(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/about.html', context={'author': author})


def t_quotes(request, tag_id):
    t_quotes = Note.objects.filter(tags=tag_id)
    tg = Tag.objects.filter(pk=tag_id).get()

    return render(request, 'quotes/t_quotes.html', context={'t_quotes': t_quotes, 'tg': tg})
