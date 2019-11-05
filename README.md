# gagumba

Simple spider to check for bad links (404s etc.)

## Rough notes kept during development

``` python
debug_print("Links found --> ")
for link in links:
    debug_print("-- DEBUG --> {link}".format(link=link))
debug_print("--------")
```

``` python
regex = r'<a[\s\S]*?href=["\'](\S*?)["\']>'
m = re.findall(regex, r.text, re.MULTILINE)
```

## TODO

- [ ] Stack overflow due to too many levels of recursion when spidering NDP
- [ ] Try to make it work locally - this would be a lot faster https://localhost:3000
- [x] Use HTML parser or something to process links (my regex is probably not robust)
- [x] Add checks for links that point offsite but do not crawl them
- [x] Add exception handling because some sites cause an exception rather than returning an error code. For example if the site doesn;t          exist.
