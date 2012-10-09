
from twisted.web import server, resource
from twisted.internet import reactor
import os


root_path = "/index.html"
path_404 = "/#.html"

class CustomHTTPServer(resource.Resource):
    isLeaf = True
    
    def __init__(self, allhosts):
        self.allhosts = allhosts
    
    #args: twisted.web.server.Request
    def render_GET(self, request):
        host = request.getRequestHostname().split(' ', 1)[0]
        hostdir = os.path.abspath(os.curdir + "/web" + os.path.abspath("/" + host).replace("C:", ""))
               
        print "Requested " + os.path.abspath(hostdir + request.path).replace(os.path.abspath(os.curdir + "/web"), "")
        
        if not os.path.exists(hostdir):
            hostdir = os.path.abspath(os.curdir + "/web/#/")
        
        if 
        
        path = os.path.abspath(hostdir + request.path)
        if os.path.isdir(path):
            path = os.path.abspath(path + root_path)
        if not os.path.exists(path):
            path = os.path.abspath(os.path.dirname(hostdir + request.path) + path_404)
        if not os.path.exists(path):
            path = os.path.abspath(os.curdir + "/web/#" + path_404)
        print "Serving " + path.replace(os.path.abspath(os.curdir + "/web"), "")
        
        if os.path.exists(hostdir + "/.headers"):
            f = file(hostdir + "/.headers")
            for line in f.read().split("\n"):
                try:
                    request.setHeader(line.split(": ")[0], line.split(": ")[1])
                except IndexError:
                    pass
        
        f = file(path)
        return f.read()
        f.close()


allhosts = dict()

for dirname, dirnames, filenames in os.walk(os.curdir + "/web/##/"):
    for filename in filenames:
        allhosts[filename] = os.path.join(dirname, filename)
print allhosts
site = server.Site(CustomHTTPServer(allhosts))
reactor.listenTCP(80, site) #@UndefinedVariable
reactor.run() #@UndefinedVariable