import requests
import re
import sys
from urllib.parse import urljoin
from html.parser import HTMLParser

# run as sudo if you want unlimited stack (but I think is limited by hard limits)
# See also: Mac OS X ulimit -s 65532 (sets stack size in Bash)
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

class MyHTMLParser(HTMLParser):

    links = []

    # 'attrs' is list of tuples
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for a in attrs:
                if a[0] == 'href':
                    self.links.append(a[1])
        return
    
def write_log(f, link, status):
    msg = "{link} -- {status}\n".format(link=link, status=status)
    f.write(msg)
    f.flush()
    return

def debug_print(msg):
    if debug_mode:
        print(msg)
    return

def debug_print_file(f, msg):
    if debug_mode:
        f.write(msg)
        f.flush()
    return
        
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
                    link = urljoin(base, link)
                    links.append(link)
                    debug_print(link)
                links = list(set(links))  # Remove duplicates
        else:
            write_log(fout, link, r.status_code)
    except Exception as e:
        print("FATAL")
        write_log(fout, link, "FATAL EXCEPTION") # Only log errors
    return links

def crawl (link):
    msg = "Checking page --> {link} -- ".format(link=link)
    print(msg, end='')
    links = get_links(link)
    for link in links:
        if link in visited:
            continue
        visited.append(link)
        crawl(link)
    return
        
#######    MAIN    ########

debug_mode = False
parser = MyHTMLParser()

if len(sys.argv) < 2:
    print("Usage: gagamba.py base")
    sys.exit()

base = sys.argv[1]
print("Crawling from base --> ", base)
visited = []
error_file = "errors.log"
with open(error_file, "w") as fout:
    crawl(base)
    print("Number of links checked: --> ", len(visited))
