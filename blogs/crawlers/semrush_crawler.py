from requests_html import HTMLSession
from slugify import slugify

def crawl_one(url):
    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text
    content = response.html.xpath("//article[@data-test='article-body']/p")
    image = response.html.xpath(".//img/@data-fullsize-src")[0]
    author = response.html.xpath("//p[@data-test='author']")[0].text
    pub_date = response.html.xpath("//span[@data-test='date']")[0].text

    my_content = ''
    short_description = ''

    for element in content:
        breakpoint()
        my_content += element.raw_html
        if not short_description and len(short_description) < 200:
            short_description += element.text

    image_name = slugify(name)
    img_type = image.split['.'][-1]
    img_path = f'images/{image_name}.{img_type}'

    # 35 minute

    article = {
        'name': name,
        'content': content,
        'images': image,
        'author': author,
        'pub_date': pub_date,
        'short_description': short_description.strip(),
    }

    print(article)
