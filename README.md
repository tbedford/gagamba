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

- [x] Use HTML parser or something to process links (my regex is probably not robust)
