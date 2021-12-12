from django.shortcuts import render


def blog_handler(request):
    context = {}
    return render(request, 'news/blog.html', context)


def page_handler(request):
    context = {}
    return render(request, 'news/page.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'news/contact.html', context)


def index_handler(request):
    context = {}
    return render(request, 'news/index.html', context)


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
