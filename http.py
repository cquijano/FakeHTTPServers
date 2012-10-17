
from twisted.web import server, resource
from twisted.internet import reactor
import os


root_path = "/index.html"
path_404 = "/#.html"

class CustomHTTPServer(resource.Resource):
    isLeaf = True
    
    def __init__(self, allhosts):
        self.allhosts = allhosts

    def getResponsePage(self, request):
        host = request.getRequestHostname().split(' ', 1)[0]
        hostdir = os.path.abspath(os.curdir + "/web" + os.path.abspath("/" + host).replace("C:", ""))
	urlPath = request.path.replace("http://", "").split("/", 1)[1]               

        print "Requested " + os.path.abspath(hostdir + "/" + urlPath).replace(os.path.abspath(os.curdir + "/web"), "")
        
        for overpath in allhosts.keys():
            if request.path.split("/")[-1] == overpath:
		print "Vhosts overwrite: " + allhosts[overpath]
                return os.path.abspath(os.curdir + "/web/##/"), allhosts[overpath]

        if not os.path.exists(hostdir):
            hostdir = os.path.abspath(os.curdir + "/web/#/")
        
        path = os.path.abspath(hostdir + "/" + urlPath)
	print urlPath
	print path
        if os.path.isdir(path):
	    print path + " is a directory"
            path = os.path.abspath(path + "/" + root_path)
	    print "Falling to : " + path
        if not os.path.exists(path):
	    print path + " does not exist"
            path = os.path.abspath(hostdir + "/" + urlPath + "/" + path_404)
	    print "Falling to: " + path
        if not os.path.exists(path):
	    print path + " does not exist"
            path = os.path.abspath(os.curdir + "/web/#" + path_404)
	    print "Falling to: " + path
            
            
        print "Serving " + path.replace(os.path.abspath(os.curdir + "/web"), "")
	return hostdir, path

    def getHeadersFile(self, hostdir, page):
	path = os.path.split(page)[0] + "/.headers"
	print "Headers: " + path
	if os.path.exists(path):
	    return path
	
	path = hostdir + "/.headers"
	print "Does not exist, falling to: " + path
	if os.path.exists(path):
	    return path
	
	print "Does not exist, not using custom headers"
	return None

    
    #args: twisted.web.server.Request
    def render_GET(self, request):

	hostdir, page = self.getResponsePage(request)
        
	headersFile = self.getHeadersFile(hostdir, page)

        if headersFile:
	    print "Overwriting headers with: " + headersFile
            f = file(headersFile)
	    fileData = f.read()
	    fileLines = fileData.split("\n")
	    if fileLines[0].isdigit() == True:
		request.setResponseCode(int(fileLines[0]))
	    else:
		fileLines = fileLines[1:]
            for line in fileLines:
                try:
                    request.setHeader(line.split(": ")[0], line.split(": ")[1])
                except IndexError:
                    pass
        
        f = file(page)
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
