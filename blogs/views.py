from django.shortcuts import render
from .models import Article, Category


def index_handler(request):
    last_articles = Article.objects.all().order_by('-pub_date')[:5].prefetch_related('categories')
    first_articles = Article.objects.all().order_by('pub_date')[:5].prefetch_related('categories')

    context = {'last_articles': last_articles,
               'first_articles': first_articles,
               }

    return render(request, 'news/index.html', context)


def blog_handler(request, **kwargs):
    cat_slug = kwargs.get('cat_slug')

    if cat_slug:
        category = Category.objects.get(slug=cat_slug)
        last_articles = Article.objects.all().filter(
            categories__slug=cat_slug).order_by(
            '-pub_date')[:5].prefetch_related('categories')

    else:
        last_articles = Article.objects.all().order_by(
            '-pub_date')[:5].prefetch_related('categories')
        category = None

    context = {
        'last_articles': last_articles,
        'category': category
    }
    return render(request, 'news/blog.html', context)


# def category_handler(request, slug):
#     category = Category.objects.get(slug=slug)
#     last_articles = Article.objects.all().filter(
#         categories__slug=slug).order_by(
#         '-pub_date')[:5].prefetch_related('categories')
#
#     context = {
#         'last_articles': last_articles,
#         'category': category
#     }
#     return render(request, 'news/blog.html', context)


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
