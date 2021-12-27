from django.db.models import Count

from .models import Category


def menu_categories(request):
    # плохой способ взять 3 первых категории и вывести их в меню
    # menu_categories = []
    #
    # for cat in Category.object.all().prefetch_related('article_set'):
    #     menu_categories.append((cat, cat.article_set.all().count()))
    #
    # menu_categories.sort(key=lambda x: x[1], reverse=True)
    #
    # menu_categories = [x[0] for x in menu_categories[:3]]

    cat_list = Category.objects.annotate(
        count=Count('article')).order_by('-count')[:3]

    return {'menu_categories': cat_list}
