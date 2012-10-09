FakeHTTPServers
===========

A http server designed for faking responses to network connectivity tests (and wpad).

Files are served in the following priority, falling to the next if the file does not exist:

./web/##/(.*)*<path>
./web/<host>/<path>
./web/<host>/#.html
./web/#/<path>
./web/#/#.html
