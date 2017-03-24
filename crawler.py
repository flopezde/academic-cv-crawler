#!/usr/bin/env python3

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import urllib
import time
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
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
            self.feed(html_string)
            return html_string, self.links
        else:
            return "", []


def spider(url, words, out_dir, max_levels=4):
    pages_to_visit = [(url, 0)]
    number_visited = 0
    visited_links = set()
    visited_pdfs = set()
    while pages_to_visit:
        number_visited += 1
        (url, level) = pages_to_visit[0]
        pages_to_visit = pages_to_visit[1:]
        visited_links.add(url)
        try:
            print("C", level, number_visited,  "Visiting:", url)
            parser = LinkParser()
            data, links = parser.get_links(url)
            soup = BeautifulSoup(data, 'html.parser')
            found_cv = False

            if level > 0:
                for a_tag in soup.find_all('a', href=True):
                    if any(word in a_tag.text.lower() for word in words) and a_tag['href'][-4:] == '.pdf':
                        pdf_url = parse.urljoin(url, a_tag['href'])
                        if pdf_url not in visited_pdfs:
                            found_cv = True
                            visited_pdfs.add(pdf_url)
                            millis = int(round(time.time() * 1000))
                            urllib.request.urlretrieve(pdf_url, out_dir + str(millis) + '.pdf')
                            print("D Downloaded", pdf_url)
                            break

            if not found_cv and level < max_levels:
                for link in links:
                    if link not in visited_links:  # and url in link
                        pages_to_visit.append((link, level + 1))
                        visited_links.add(link)
        except Exception as e:
            print("E", e)


def run_crawler(urls, out_dir):
    words = ['cv', 'resume', 'curriculum vitae', 'curriculum', 'vitae']
    for url in urls:
        spider(url, words, out_dir)

if __name__ == '__main__':
    import sys
    import os

    urls_file = 'urls'
    out_dir = 'CVs'

    if len(sys.argv) > 1:
        urls_file = sys.argv[1]
    urls = list()
    for line in open(urls_file, 'r').readlines():
        urls.append(line)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_dir += '/'

    run_crawler(urls, out_dir)
