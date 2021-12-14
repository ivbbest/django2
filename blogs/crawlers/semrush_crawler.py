from requests_html import HTMLSession
from slugify import slugify
from datetime import datetime
import re


def crawl_one(url):
    with HTMLSession() as session:
        response = session.get(url)

    # парсим данные со страницы: название статьи, контент, 1 картинку, дату и т.д.

    name = response.html.xpath('//h1')[0].text
    content = response.html.xpath("//article[@data-test='article-body']/p")
    image_url = response.html.xpath(".//img/@data-fullsize-src")[0]
    pub_date = response.html.xpath("//span[@data-test='date']")[0].text
    categories = ['SEO', 'Python', 'Advanced SEO']      # задаем вручную т.к. в статье нет категорий

    # парсим информацию по автору согласно модели: имя, био, картинка

    author_name = response.html.xpath("//p[@data-test='author']")[0].text
    author_image_url = response.html.xpath("//svg[@data-test='author-photo']/image")
    bio_author = response.html.xpath("//span[@data-test='author-caption']")[0].text

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

    with open(f'media/images/{img_path}', 'wb') as f:
        response = session.get(image_url)
        f.write(response.content)

    # вытаскиваем через регулярку урл картинки

    pattern = r"https?://[\S][^']+"
    author_image_url = re.findall(pattern, str(author_image_url[0]))[0]

    # сохраняем картинку автора статьи

    author_image_name = slugify(author_name)
    author_img_type = author_image_url.split('.')[-1]
    author_img_path = f'images/{author_image_name}.{author_img_type}'

    with open(f'media/avatars/{author_img_path}', 'wb') as f:
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

    # подготавливаем словарь с данными по статье

    article = {
        'name': name,
        'slug': slugify(name),
        'content': my_content,
        'images': img_path,
        'pub_date': pub_date,
        'short_description': short_description.strip(),
        'categories': categories,
        'author': author,
    }

    print(author_image_url)
