import urllib3
from lxml import etree

http = urllib3.PoolManager()


def filter(str):
    if '请点击下一章继续阅读' in str:
        return True
    if ')' == str:
        return True
    if '艾米小说网' in str:
        return True
    if '精彩小说无弹窗' in str:
        return True
    if '(m.amxs.cc = ' in str:
        return True
    return False


def parse(uri, title, file):
    file.write(title.strip() + "\n\n")
    art_page = 1
    while art_page <= 4:
        art_query = uri if art_page == 1 else uri[:-5] + '_' + str(art_page) + ".html"
        content = http.request('GET', host + art_query, retries=10).data
        html_dom = etree.HTML(content, etree.HTMLParser())
        sections = html_dom.xpath('//div[@id="novelcontent"]//text()')
        print(art_query, title)

        for section in sections:
            if not filter(section):
                file.write(section.strip() + "\n")
        art_page += 1
    file.write("\n")


host = 'https://m.amxs.cc'
home = '/book/104795'
page = 1
chapterMap = {}

while page <= 35:
    query = home if page == 1 else home + '_' + str(page)
    homePageContent = http.request('GET', host + query, retries=10).data
    homePageDom = etree.HTML(homePageContent, etree.HTMLParser())
    chapters = homePageDom.xpath('//div[@class="list_xm"]/ul/li/a')
    for chapter in chapters:
        chapterMap[chapter.attrib['href']] = chapter.text
    page += 1

with open('book.txt', 'a', encoding='utf-8') as f:
    for chapterUri in sorted(chapterMap.keys()):
        parse(chapterUri, chapterMap[chapterUri], f)
    f.close()
