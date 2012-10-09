FakeHTTPServers
===========

A http server designed for faking responses to network connectivity tests (and wpad).

Files are served in the following priority, falling to the next if the file does not exist:

./web/##/(.\*)\*&lt;path&gt;

./web/&lt;host&gt;/&lt;path&gt;

./web/&lt;host&gt;/#.html

./web/#/&lt;path&gt;

./web/#/#.html

