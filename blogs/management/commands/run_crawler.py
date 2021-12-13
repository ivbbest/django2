from django.core.management.base import BaseCommand
from blogs.crawlers.semrush_crawler import crawl_one


class Command(BaseCommand):
    help = 'Run Semrush crawler'

    def handle(self, *args, **options):
        url = 'https://www.semrush.com/blog/python-content-briefs-seo/'
        crawl_one(url)
