import requests
import re
import sys
from urllib.parse import urljoin

debug_mode = False

if len(sys.argv) < 2:
    print("Usage: gagamba.py base")
    sys.exit()

base = sys.argv[1]
print("Crawling from base --> ", base)
visited = []
filename = "404.log"

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
    msg = "Getting links on page --> {link}".format(link=link)
    print(msg)
    links = []
    r = requests.get(link)
    if r.status_code == 200:
        regex = r'<a[\s\S]*?href=["\'](\S*?)["\']>'
        m = re.findall(regex, r.text, re.MULTILINE)
        # Normalize links and add to array
        for link in m:
            link = normalize_link(link)
            if not link.startswith(base):
                debug_print("Not our domain --> {link}".format(link=link))
                continue
            links.append(link)
        # Remove duplicates
        links = list(set(links))   
    else:
        print(r.status_code)
        write_log(fout, link, r.status_code)
    return links

def crawl (link):
    links = get_links(link)
    for link in links:
        if link in visited:
            debug_print("Already visited --> {link}".format(link=link))
            continue
        visited.append(link)
        crawl(link)

fout = open(filename, "w")
crawl(base)
print("Number of pages visited: --> ", len(visited))
fout.close()
