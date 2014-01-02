import time
import hotLaps_db

class  xmlOutput:
    
    def __init__(self, dbase, outputFilename1, outputFilename2):
        self.db = dbase
        self.outputXMLfile = outputFilename1
        self.outputXMLfile2 = outputFilename2
            
    def run(self):
        if  self.db and self.outputXMLfile:
            self.WriteOutChanges()
        if self.db and self.outputXMLfile2:
            self.WriteOutChanges2()

    def formatLapData(self, l):
        params = {'tId': l[1], 'drv': l[2], 'cCls': l[3], 'cName' : l[4], 's1' : l[5], 's2' : l[6], 's3' : l[7], 'lt' : l[8], 'date' : l[9], 'time' : l[10]}
        return '<result trackID="%(tId)s" driver="%(drv)s" classV="%(cCls)s" carName="%(cName)s" s1="%(s1)s" s2="%(s2)s" s3="%(s3)s" lapTime="%(lt)s" theDate="%(date)s" totalLapTime="%(time)3F"/>' % params
 
    def WriteOutChanges(self):
        FILE = open(self.outputXMLfile,"w")
        FILE.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
        FILE.write("<results>\n")
        
        laps = self.db.getLaps()
        
        for l in laps:
            FILE.write("\t" + self.formatLapData(l) + "\n")
            
        FILE.write("</results>\n")
        FILE.close()
        
    def WriteOutChanges2(self):
        FILE = open(self.outputXMLfile2,"w")
        FILE.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
        FILE.write("<results>\n")
        
        laps = self.db.getUniqueLaps()
        
        for l in laps:
            FILE.write("\t" + self.formatLapData(l) + "\n")
            
        FILE.write("</results>\n")
        FILE.close()