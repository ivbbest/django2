from django.contrib import admin
from .models import Article, Category, Comment, Author, Tag, Newsletter
from django_summernote.admin import SummernoteModelAdmin


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'short_description',)


admin.site.register(Author)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Newsletter)
