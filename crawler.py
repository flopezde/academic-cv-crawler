from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


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


def spider(url, word, max_pages):
    pages_to_visit = [url]
    number_visited = 0
    found_word = False
    while number_visited < max_pages and pages_to_visit != [] and not found_word:
        number_visited += 1
        url = pages_to_visit[0]
        pages_to_visit = pages_to_visit[1:]
        try:
            print(number_visited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.get_links(url)
            if data.find(word) > -1:
                found_word = True
                pages_to_visit = pages_to_visit + links
                print(" **Success!**")
        except Exception as e:
            print(e)
            print(" **Failed!**")
    if found_word:
        print("The word", word, "was found at", url)
    else:
        print("Word never found")

spider("https://www.ualberta.ca/computing-science/", "his", 100)
