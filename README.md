FakeHTTPServers
===========

A http server designed for faking responses to network connectivity tests (and wpad).
Cookied are saved into ./data/&lt;host&gt;.txt with the IP of the client who sent the cookie.
Note that these files should be read with "sort -u" to filter out the duplicates

Arguments:
-v		: debug level logging

Files are served in the following priority, falling to the next if the file does not exist:

1) overwrites in the ## directory: ./web/##/(.\*)\*/&lt;path&gt;

2) index.html in the directory defined by the path and host requested: ./web/&lt;host&gt;/&lt;path&gt;/index.html

3) #.html in the directory defined by the path and host requested: ./web/&lt;host&gt;/&lt;path&gt;/#.html

4) original path requeuested on host requested: ./web/&lt;host&gt;/&lt;path&gt;

5) #.html in the directory defined by the host: ./web/&lt;host&gt;/#.html

6) if there is no ./web/&lt;host&gt;/ folder, path requsted in # folder: ./web/#/&lt;path&gt;

7) notfound page: ./web/#/#.html



A .headers file defines custom headers for a response e.g.

Content-Type: text/html; charset=UTF-8

The first line of the .headers file can be a number, if so this is the status code of the response

.headers are read in the following priority:

./web/&lt;host&gt;/&lt;path&gt;/.headers

./web/&lt;host&gt;/.headers

e.g.

www.google.com/foo/bar.html

would first try

./web/www.google.com/foo/.headers

then

./web/www.google.com/.headers

This allows single pages on the same vhost to use different status codes by using a folder in place of the page and putting the content in a index.hmtl or #.html file inside this folder along with the custom .headers for this page




