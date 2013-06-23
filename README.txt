Textile: Super-fast in-memory text finder
==========================================

(C) Copyright 2013 Takahiro Yoshimura <altakey@gmail.com>

For the keyword-seeking souls suffering in the world of braindead security software and mixed encodings (CP932/EUC-JP/UTF-8/UTF-16/ASCII.)

0. HOW TO USE
-------------

$ python ./textile.py
textile> update /path/to/project
updating /path/to/project ..
.. (107927491 bytes)
textile> find <html
/path/to/project/somewhere/text.html:2:<html>
/path/to/project/anywhere/text.html:2:<html onload="....">
/path/to/project/elsewhere/text.html:2:<html class="..." ....>
...
textile> find 今週のハイライト</p>
/path/to/project/somewhere/highlight.html: <p>今週のハイライト</p>
...

1. FEATURES
-----------

 * Searchs should be lighting-fast, even in the morasses of slow-and-braindead on-access malware scanners
 * Allows searching in UTF-8 over different encodings
 * Do not use sockets: doesn't provoke local security software
 * Allows searching with rather expressive RE flavor (Python 2.7 regex)
 * Allows multithreaded search

2. BUGS
--------

 * Databases are volatile
 * Huge memory consumption
 * Search shell is stupid -- no history, no readline, ...
 * Requires newer regex module
