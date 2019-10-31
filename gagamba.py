# TODO:
# Exception handling for bad links (instead of timeout and crash, should go to next link)
# Improve normalization code
# Handle other links e.g. mailto:
# Use HTML parser or something to process links
# Use urlparse to parse or process links
# Put page fetching in function with exception handling
# Better logging write(f, msg) - where f could be stdout, file, stderr

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
    debug_print("Link: --> {link}".format(link=link))
    link = urljoin(base, link)
    debug_print("Normalized link: --> {link}".format(link=link))
    return link

def get_page(link):
    try:
        r = requests.get(link)  
        return r
    except Exception as e:
        print(e)
        return None

def get_links(link):
    msg = "Getting links on page --> {link}".format(link=link)
    print(msg)
    links = []
    r = get_page(link)
    if r:
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
        debug_print("Links found --> ")
        for link in links:
            debug_print("-- DEBUG --> {link}".format(link=link))
        debug_print("--------")
    return links

def crawl (link):
    links = get_links(link)
    for link in links:
        if link in visited:
            if debug_mode:
                print('Already visited --> ', link)
            continue
        visited.append(link)
        crawl(link)

fout = open(filename, "w")
crawl(base)
print("Number of pages visited: --> ", len(visited))
fout.close()
