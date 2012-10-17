FakeHTTPServers
===========

A http server designed for faking responses to network connectivity tests (and wpad).

Files are served in the following priority, falling to the next if the file does not exist:

./web/##/(.\*)\*/&lt;path&gt;
./web/&lt;host&gt;/&lt;path&gt;
./web/&lt;host&gt;/#.html
./web/#/&lt;path&gt;
./web/#/#.html


A .headers file defines custom headers for a response e.g.
Content-Type: text/html; charset=UTF-8

The first line of the .headers file can be a number, if so this is the status code of the response

.headers are read in the following priority:
./web/<host>/<directories>/.headers
./web/<host>/.headers

e.g.
www.google.com/foo/bar.html
would first try
./web/www.google.com/foo/.headers
then
./web/www.google.com/.headers

This allows single pages on the same vhost to use different status codes by using a folder in place of the page and putting the content in a #.html file inside this folder along with the custom .headers for this page


