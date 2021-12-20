from django.contrib import admin

from .crawlers import semrush_crawler
from .models import Article, Category, Comment, Author, Tag, Newsletter
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html
from threading import Thread
#from blogs.crawlers.semrush_crawler import run

def count_words(modeladmin, request, queryset):
    for object in queryset:
        text = object.content.replace('<p>', '').replace('</p>', '')
        words = text.split()
        object.content_words_count = len(words)
        object.save()


count_words.short_description = 'Count words in article'


def get_fresh_news(modeladmin, request, queryset):
    for object in queryset:
        if object.name == 'Brian Moseley':
            Thread(target=semrush_crawler.run, args=()).start()


get_fresh_news.short_description = 'Get fresh news'


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'short_description',)
    list_display = ('image_code', 'name', 'pub_date', 'author',
                    'content_words_count', 'count_unique_words')
    list_filter = ('name', 'author',)
    search_fields = ('name', 'author')
    actions = (count_words, )

    def image_code(self, object):
        return format_html(
            '<img src="{}" style="max-width: 100px" />',
            object.main_image.url
        )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_menu', 'order')
    list_filter = ('in_menu',)
    search_fields = ('slug',)
    list_editable = ('slug',)
    readonly_fields = ('name',)


class AuthorArticleInLine(admin.TabularInline):
    model = Article
    exclude = ('content', 'short_description')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('ava', 'name', 'bio', 'articles_count')
    inlines = (AuthorArticleInLine,)
    actions = (get_fresh_news, )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('article_set')

    def articles_count(self, object):
        return object.article_set.all().count()

    def ava(self, object):
        return format_html(
            '<img src="{}" style="max-width: 30px" />',
            object.avatar.url
        )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Newsletter)
