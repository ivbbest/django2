from requests_html import HTMLSession
from slugify import slugify
from datetime import datetime
import re
from blogs.models import Article, Author, Category
from concurrent.futures import ThreadPoolExecutor
from django.utils.timezone import make_aware

#author = Author.object.get(id=3)


def crawl_one(url):
    with HTMLSession() as session:
        response = session.get(url)

    # парсим данные со страницы: название статьи, контент, 1 картинку, дату и т.д.
    try:
        name = response.html.xpath('//h1')[0].text
        content = response.html.xpath("//article[@data-test='article-body']/p")
        image_url = response.html.xpath("//picture/source/@srcset")[0]
        pub_date = response.html.xpath("//span[@data-test='date']")[0].text
        cats = ['SEO', 'Python', 'Advanced SEO']      # задаем вручную т.к. в статье нет категорий

    except Exception:
        print('Truuble')

    # парсим информацию по автору согласно модели: имя, био, картинка

    author_name = response.html.xpath("//p[@data-test='author']")[0].text
    author_image_url = response.html.xpath("//svg[@data-test='author-photo']/image")
    bio_author = response.html.xpath("//span[@data-test='author-caption']")[0].text

    # заносим категории в словарь
    categories = []

    for cat in cats:
        categories.append(
            {
            'name': cat,
            'slug': slugify(cat),
        }
        )


    # подготавливаем описание статьи и само содержимое статьи
    my_content = ''
    short_description = ''

    for element in content:
        my_content += f'<{element.tag}>' + element.text + f'</{element.tag}>'
        if not short_description and len(short_description) < 200:
            short_description += element.text

    # составление название картинок, сохранение картинки статьи
    image_name = slugify(name)
    img_type = image_url.split('.')[-1]
    img_path = f'images/{image_name}.{img_type}'

    with open(f'media/{img_path}', 'wb') as f:
        response = session.get(image_url)
        f.write(response.content)

    # вытаскиваем через регулярку урл картинки

    pattern = r"https?://[\S][^']+"
    author_image_url = re.findall(pattern, str(author_image_url[0]))[0]

    # сохраняем картинку автора статьи

    author_image_name = slugify(author_name)
    author_img_type = author_image_url.split('.')[-1]
    author_img_path = f'avatars/{author_image_name}.{author_img_type}'

    with open(f'media/{author_img_path}', 'wb') as f:
        response = session.get(author_image_url)
        f.write(response.content)

    # дату сохраняем в корректном варианте для занесения в базу данных
    pub_date = datetime.strptime(pub_date, '%b %d, %Y')

    # подготавливаем словарь с данными по автору

    author = {
        'name': author_name,
        'avatar': author_img_path,
        'bio': bio_author,
    }

    # добавляем автора в базу если его нет

    author, created = Author.object.get_or_create(**author)

    # подготавливаем словарь с данными по статье

    article = {
        'name': name,
        'slug': slugify(name),
        'content': my_content,
        'main_image': img_path,
        'pub_date': make_aware(pub_date),
        'short_description': short_description.strip(),
        'author': author
    }

    # добавляем статью в базу если ее нет
    article, created = Article.object.get_or_create(**article)

    # добавляем категории для статей
    for category in categories:
        cat, created = Category.object.get_or_create(**category)
        article.categories.add(cat)


# реализовал парсинг всех страниц с учетом пагинации
# так как у сайта есть проблемы с кодом ответа 404, то вручную задал количество страниц

def get_fresh_news():
    base_url = 'https://www.semrush.com/blog/category/advanced-seo/'
    links = list()

    for i in range(1, 5):
        with HTMLSession() as session:
            params = {'page': i}
            response = session.get(base_url, params=params)
            links = set(links) | response.html.absolute_links

    fresh_news = [lnk for lnk in list(links) if ('/blog/' in lnk) and ('/category/' not in lnk)]

    return fresh_news


def run():
    fresh_news = get_fresh_news()

    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(crawl_one, fresh_news)
