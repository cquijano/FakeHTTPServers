
from twisted.web import server, resource
from twisted.internet import reactor
import os
import logging
import sys

loglevel = logging.INFO
if (len(sys.argv) > 1 and sys.argv[1] == "-v"):
    loglevel = logging.DEBUG
logging.basicConfig(format="%(levelname)s\t\t%(message)s")

root_path = "/index.html"
path_404 = "/#.html"

class CustomHTTPServer(resource.Resource):
    isLeaf = True
    
    def __init__(self, allhosts):
        self.allhosts = allhosts
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(loglevel)

    def getResponsePage(self, request):        
        host = request.getRequestHostname().split(' ', 1)[0]
        hostdir = os.path.abspath(os.curdir + "/web" + os.path.abspath("/" + host).replace("C:", "")[1:])
        urlPath = request.path.replace("http://", "").split("/", 1)[1]               

        path = os.path.abspath(hostdir + "/" + urlPath)
        
        url = path.replace(os.path.abspath(os.curdir + "/web"), "")
        self.log.warning("%s: requested %s" % (request.getClientIP(), url))
        
        for overpath in allhosts.keys():
            if request.path.split("/")[-1] == overpath:
                self.log.debug("Forced overwrite response: %s" % allhosts[overpath].replace(os.path.abspath(os.curdir + "/web"), ""))
                return os.path.abspath(os.curdir + "/web/##/"), allhosts[overpath]

        if not os.path.exists(hostdir):
            hostdir = os.path.abspath(os.curdir + "/web/#/")
            path = os.path.abspath(hostdir + "/" + urlPath)
            self.log.debug("vhost directory does not exist, falling to %s" % path.replace(os.path.abspath(os.curdir + "/web"), ""))

        if os.path.isdir(path):
            pathdir = path
            path = os.path.abspath(pathdir + "/" + root_path)
            self.log.debug("path is a directory, falling to %s" % path.replace(os.path.abspath(os.curdir + "/web"), ""))
            if not os.path.exists(path):
                path = os.path.abspath(pathdir + "/" + path_404)
                self.log.debug("path does not exist, falling to %s" % path.replace(os.path.abspath(os.curdir + "/web"), ""))
        if not os.path.exists(path):
            path = os.path.abspath(hostdir + "/" + path_404)
            self.log.debug("path does not exist, falling to %s" % path.replace(os.path.abspath(os.curdir + "/web"), ""))
        if not os.path.exists(path):
            path = os.path.abspath(os.curdir + "/web/#" + path_404)
            self.log.debug("path does not exist, falling to %s" % path.replace(os.path.abspath(os.curdir + "/web"), ""))
            
        return url, hostdir, path

    def getHeadersFile(self, hostdir, page):
        path = os.path.split(page)[0] + "/.headers"
        if os.path.exists(path):
            self.log.debug("Using %s for headers" % path.replace(os.path.abspath(os.curdir + "/web"), ""))
            return path
    
        oldpath = path
        path = hostdir + "/.headers"
        if os.path.exists(path):
            self.log.debug("using %s for headers" % oldpath)
            self.log.debug("path does not exist, falling to %s" % path.replace(os.path.abspath(os.curdir + "/web"), ""))
            return path
    
        return None

    
    #args: twisted.web.server.Request
    def render_GET(self, request):
        url, hostdir, path = self.getResponsePage(request)
        self.log.warning("%s: serving: %s" % (request.getClientIP(), path.replace(os.path.abspath(os.curdir + "/web"), "")))
                
        headersFile = self.getHeadersFile(hostdir, path)

        if headersFile:
            f = file(headersFile)
        fileData = f.read()
        fileLines = fileData.split("\n")
        if fileLines[0].rstrip().isdigit() == True:
            self.log.debug("using %s status code" % fileLines[0])
            request.setResponseCode(int(fileLines[0].rstrip()))
        else:
            fileLines = fileLines[1:]
        for line in fileLines:
            try:
                rsline = line.rstrip()
                request.setHeader(rsline.split(": ")[0], rsline.split(": ")[1])
            except IndexError:
                pass
        
        if len(request.received_cookies) > 0:
            cookieLog = file("./data/" + url.split(os.sep)[0] + ".txt", "a")
            for key in request.received_cookies.keys():
                cookieLog.write("%s\t%s=%s\n" % (request.getClientIP(), key, request.received_cookies[key]))
            
            self.log.info("Received %d cookies from %s for %s. Saving to ./data/%s.txt" % (len(request.received_cookies), request.getClientIP(), url,  url.split(os.sep)[0]))
            cookieLog.close()

                                                   
        f = file(path)
        content = f.read()
        f.close()
        return content


allhosts = dict()
for dirname, dirnames, filenames in os.walk(os.curdir + "/web/##/"):
    for filename in filenames:
        allhosts[filename] = os.path.join(dirname, filename)
if not os.path.exists("data/"):
    os.mkdir("data")   
site = server.Site(CustomHTTPServer(allhosts))
reactor.listenTCP(80, site) #@UndefinedVariable
print "Starting"
reactor.run() #@UndefinedVariable
