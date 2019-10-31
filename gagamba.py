import requests
import re
import sys
from urllib.parse import urljoin
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    links = []

    # 'attrs' is list of tuples
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for a in attrs:
                if a[0] == 'href':
                    self.links.append(a[1])

def write_log(f, link, status):
    msg = "{link} -- {status}\n".format(link=link, status=status)
    f.write(msg)
    f.flush()

def debug_print(msg):
    if debug_mode:
        print(msg)

def normalize_link(link):
    return urljoin(base, link)

def get_links(link):
    links = []
    try:
        headers = {'user-agent': 'gagamba/0.0.1'}
        r = requests.get(link, headers=headers)
        print(r.status_code)
        if r.status_code == 200:
            if link.startswith(base): # We do want to check offsite links, but we don't want to crawl them
                parser.feed(r.text)
                m = parser.links
                for link in m:
                    link = normalize_link(link)
                    links.append(link)
                links = list(set(links))  # Remove duplicates
        else:
            write_log(fout, link, r.status_code)
    except Exception as e:
        print("FATAL")
        write_log(fout, link, "FATAL EXCEPTION")
    return links

def crawl (link):
    msg = "Checking page --> {link} -- ".format(link=link)
    print(msg, end='')
    links = get_links(link)
    for link in links:
        if link in visited:
            debug_print("Already visited --> {link}".format(link=link))
            continue
        visited.append(link)
        crawl(link)

#######    MAIN    ########

debug_mode = False
parser = MyHTMLParser()

if len(sys.argv) < 2:
    print("Usage: gagamba.py base")
    sys.exit()

base = sys.argv[1]
print("Crawling from base --> ", base)
visited = []
filename = "errors.log"

fout = open(filename, "w")
crawl(base)
print("Number of pages checked: --> ", len(visited))
fout.close()
