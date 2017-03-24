from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup



class LinkParser(HTMLParser):

    def __init__(self):
        super(LinkParser, self).__init__()
        self.links = []
        self.baseUrl = ''

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    new_url = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [new_url]

    def get_links(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "", []


def spider(url, words, max_pages):
    pages_to_visit = [url]
    number_visited = 0
    visited_links = set()
    while number_visited < max_pages and pages_to_visit != []:
        number_visited += 1
        url = pages_to_visit[0]
        pages_to_visit = pages_to_visit[1:]
        visited_links.add(url)
        try:
            print(number_visited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.get_links(url)
            soup = BeautifulSoup(data, 'html.parser')
            if number_visited > 1 and any(len(x) > 0 for x in [soup(text=y) for y in words]):
                for link in links:
                    if '.pdf' in link:
                        print(link)
            else:
                for link in links:
                    if link not in visited_links:  # and url in link
                        pages_to_visit.append(link)
                        visited_links.add(link)
        except Exception as e:
            print(e)
            print(" **Failed!**")

words = ['CV', 'cv', 'Resume', 'RESUME', 'resume']
spider("https://mattbrehmer.github.io/", words, 10000)
