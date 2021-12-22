from django.shortcuts import render
from .models import Article


def index_handler(request):
    last_articles = Article.object.all().order_by('-pub_date')[:5]
    first_articles = Article.object.all().order_by('pub_date')[:5]
    context = {'last_articles': last_articles,
               'first_articles': first_articles,
               }
    return render(request, 'news/index.html', context)


def blog_handler(request):
    context = {}
    return render(request, 'news/blog.html', context)


def page_handler(request):
    context = {}
    return render(request, 'news/page.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'news/contact.html', context)





def about_handler(request):
    context = {}
    return render(request, 'news/about.html', context)


def category_handler(request):
    context = {}
    return render(request, 'news/category.html', context)


def latest_news(request):
    context = {}
    return render(request, 'news/latest_news.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context, content_type='text/plain')
