from django.shortcuts import render
from .models import Article, Category
from django.db.models import Count


def index_handler(request):
    last_articles = Article.object.all().order_by('-pub_date')[:5].prefetch_related('categories')
    first_articles = Article.object.all().order_by('pub_date')[:5].prefetch_related('categories')

    # плохой способ взять 3 первых категории и вывести их в меню
    # menu_categories = []
    #
    # for cat in Category.object.all().prefetch_related('article_set'):
    #     menu_categories.append((cat, cat.article_set.all().count()))
    #
    # menu_categories.sort(key=lambda x: x[1], reverse=True)
    #
    # menu_categories = [x[0] for x in menu_categories[:3]]

    menu_categories = Category.objects.annotate(
        count=Count('article')).order_by('count')[:3]

    context = {'last_articles': last_articles,
               'first_articles': first_articles,
               'menu_categories': menu_categories
               }

    return render(request, 'news/index.html', context)


def blog_handler(request):
    last_articles = Article.object.all().order_by('pub_date')[:10].prefetch_related('categories')
    context = {'last_articles': last_articles}

    return render(request, 'news/blog.html', context)


def category_handler(request, slug):
    context = {}
    return render(request, 'news/blog.html', context)


def page_handler(request, slug):
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
