from socket import socket,AF_INET,SOCK_STREAM
import select
import threading
import hotLaps_db
import produceReports
import xml.sax.handler
import sys
import client

class record(xml.sax.handler.ContentHandler):
    trackID = ""
    driver = ""
    classV = ""
    carName = ""
    s1 = ""
    s2 = ""
    s3 = ""
    lapTime = ""
    theDate = ""
    totalLapTime = ""

    def __init__(self):
        self.mapping = {}

    def startElement(self, name, attributes):
        if name == "result":
            self.buffer = ""
            self.trackID = attributes["trackID"].encode('ascii', 'ignore')
            self.driver = attributes["driver"].encode('ascii', 'ignore')
            self.classV = attributes["classV"].encode('ascii', 'ignore')
            self.carName = attributes["carName"].encode('ascii', 'ignore')
            self.s1 = attributes["s1"].encode('ascii', 'ignore')
            self.s2 = attributes["s2"].encode('ascii', 'ignore')
            self.s3 = attributes["s3"].encode('ascii', 'ignore')
            self.lapTime = attributes["lapTime"].encode('ascii', 'ignore')
            self.theDate = attributes["theDate"].encode('ascii', 'ignore')
            self.totalLapTime = attributes["totalLapTime"].encode('ascii', 'ignore')


    def fromXMLString(self):
        return [self.trackID, self.driver, self.classV, self.carName, self.s1, self.s2, self.s3, self.lapTime, self.theDate, self.totalLapTime]


    def toXMLString(self):
        self.xmlString = "<result trackID=\"" + self.trackID
        self.xmlString = self.xmlString + "\" driver=\"" + self.driver
        self.xmlString = self.xmlString + "\" classV=\"" + self.classV
        self.xmlString = self.xmlString + "\" carName=\"" + self.driver
        self.xmlString = self.xmlString + "\" s1=\"" + self.s1
        self.xmlString = self.xmlString + "\" s2=\"" + self.s2
        self.xmlString = self.xmlString + "\" s3=\"" + self.s3
        self.xmlString = self.xmlString + "\" lapTime=\"" + self.lapTime
        self.xmlString = self.xmlString + "\" theDate=\"" + self.theDate
        self.xmlString = self.xmlString + "\" totalLapTime=\"" + self.totalLapTime
        self.xmlString = self.xmlString + "\" />"
        return self.xmlString

class rfactorHotlapsServer(threading.Thread):

    HOST = ''    #we are the host
    PORT = 1234    #arbitrary port not currently in use
    ADDR = (HOST,PORT)    #we need a tuple for the address
    BUFSIZE = 4096    #reasonably sized buffer for data
    MAX_CONNS = 16
    serv=[]

    def __init__(self, addr, dataBaseFile, outputFilenames, postUrl):
        threading.Thread.__init__(self)
        self.ADDR = (addr[0], addr[1])
        self.dataBaseFile = dataBaseFile
        self.outputFilenames = outputFilenames
        self.postUrl = postUrl

    def stopRunning(self):
        self.continueRunning = False

    def run(self):

        self.createSocketandListen()
        input_src = [self.serv]
        self.db = hotLaps_db.hotLapsDataBase(self.dataBaseFile)
        xmlWriter = produceReports.xmlOutput(self.db, self.outputFilenames[0], self.outputFilenames[1])
        xmlWriter.run()

        self.continueRunning = True
        print "Waiting for connections"
        while (self.continueRunning):
            try:
                inputready,outputready,exceptready = select.select(input_src,[],[],5.0)
                for s in inputready:
                    if s == self.serv:
                        conn, addr = self.serv.accept()
                        input_src.append(conn)
                    else:
                        # handle all other sockets
                        data = s.recv(1024)
                        if data:
                            # Check to make sure it is a race result
                            if self.db:
                                self.dataHandler(data)
                            xmlWriter.run()
                        else:
                            s.close()
                            input_src.remove(s)

            except Exception, err:
                print "Exception received: " + str(err)
                self.continueRunning = False

        self.serv.close()

    def dataHandler(self, d):
        """
            Get an XML string d and extract data and insert it into the database
        """
        data = []
        rec_handler = record()
        start = d.find('<result', 0)
        while start != -1:
            end = d.find('/>', start)
            if end == -1:
                start = -1
            else:
                end = end + 2
                xml.sax.parseString(d[start:end], rec_handler)
                temp = rec_handler.fromXMLString()
                print >> sys.stdout, str(d[start:end])
                data.append(rec_handler.fromXMLString())
                start = d.find('<results', end)

        self.db.addLaps(data)
        for lap in data:
            post_dictionary = client.prepare_data(lap)
            client.post(self.postUrl, post_dictionary)

    def setConnectionHandler(self, func):
        self.callback = func

    def createSocketandListen(self):
        self.serv = socket( AF_INET,SOCK_STREAM)
        ##bind our socket to the address
        self.serv.bind((self.ADDR))
        return self.serv.listen(self.MAX_CONNS)

    def waitForConnections(self):
        return self.serv.accept()

    def closeConnection(self, conn):
        return conn.close()

    def read(self, conn):
        rc = conn.recv()
        return rc

    def close(self):
        return self.serv.close()
