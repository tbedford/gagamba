# gagumba

Simple spider to check for bad links (404s etc.)

``` python
debug_print("Links found --> ")
for link in links:
    debug_print("-- DEBUG --> {link}".format(link=link))
debug_print("--------")
```

## TODO

- [ ] Use HTML parser or something to process links (my regex is probably not robust)

