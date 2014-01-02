#!/usr/bin/env python

import clientSocket
import time

testData = [['<result trackID="Mount Pleasant" driver="40pints" classV="Mini" carName="Cooper" s1="12.5" s2="14.6" s3="56.8" lapTime="1:40.673" theDate="28-02-2010" totalLapTime="100.673"/>'],
            ['<result trackID="Mount Pleasant" driver="40pints" classV="AE86" carName="Red One" s1="12.5" s2="14.6" s3="56.8" lapTime="1:43.673" theDate="28-02-2010" totalLapTime="103.673"/>'],
            ['<result trackID="Mount Pleasant" driver="R1K" classV="AE86" carName="Blue One" s1="12.5" s2="14.6" s3="56.8" lapTime="1:44.673" theDate="28-02-2010" totalLapTime="106.673"/>'],
            ['<result trackID="Mount Pleasant" driver="R1K" classV="Mini" carName="Cooper" s1="12.5" s2="14.6" s3="56.8" lapTime="1:47.673" theDate="28-02-2010" totalLapTime="107.673"/>'],
            ['<result trackID="Mount Pleasant" driver="R1K" classV="AE86" carName="Blue One" s1="12.5" s2="14.6" s3="56.8" lapTime="1:42.673" theDate="28-02-2010" totalLapTime="102.673"/>'],
            ['<result trackID="SilverStone" driver="R1K" classV="AE86" carName="Blue one" s1="12.5" s2="14.6" s3="56.8" lapTime="1:44.673" theDate="28-02-2010" totalLapTime="104.673"/>'],
            ['<result trackID="SilverStone" driver="40pints" classV="AE86" carName="Red One" s1="12.5" s2="14.6" s3="56.8" lapTime="1:45.673" theDate="28-02-2010" totalLapTime="105.673"/>'],
            ['<result trackID="Mount Pleasant" driver="40pints" classV="AE86" carName="Red One" s1="12.5" s2="14.6" s3="56.8" lapTime="1:49.673" theDate="28-02-2010" totalLapTime="109.673"/>'],
            ['<result trackID="Mount Pleasant" driver="40pints" classV="Mini" carName="Cooper" s1="12.5" s2="14.6" s3="56.8" lapTime="1:41.673" theDate="28-02-2010" totalLapTime="101.673"/>'],
            ['<result trackID="SilverStone" driver="40pints" classV="AE86" carName="Red One" s1="12.5" s2="14.6" s3="56.8" lapTime="1:43.673" theDate="28-02-2010" totalLapTime="103.673"/>'],
            ['<result trackID="Brandshatch" driver="R1K" classV="Buses" carName="DoubleDecker" s1="12.5" s2="14.6" s3="56.8" lapTime="1:44.673" theDate="28-02-2010" totalLapTime="106.673"/>'],
            ['<result trackID="Brandshatch" driver="40pints" classV="Buses" carName="DoubleDecker" s1="12.5" s2="14.6" s3="56.8" lapTime="1:47.673" theDate="28-02-2010" totalLapTime="107.673"/>'],
            ['<result trackID="Brandshatch" driver="R1k" classV="Buses" carName="DoubleDecker" s1="12.5" s2="14.6" s3="56.8" lapTime="1:42.673" theDate="28-02-2010" totalLapTime="102.673"/>'],
            ['<result trackID="SilverStone" driver="40pints" classV="LMS GT1" carName="Aston Martin V8" s1="12.5" s2="14.6" s3="56.8" lapTime="1:44.673" theDate="28-02-2010" totalLapTime="104.673"/>'],
            ['<result trackID="SilverStone" driver="40pints" classV="LMS GT1" carName="Aston Martin V8" s1="12.5" s2="14.6" s3="56.8" lapTime="1:45.673" theDate="28-02-2010" totalLapTime="105.673"/>'],
            ['<result trackID="SilverStone" driver="R1K" classV="LMS GT1" carName="Corvette" s1="12.5" s2="14.6" s3="56.8" lapTime="1:49.673" theDate="28-02-2010" totalLapTime="109.673"/>'],
            ['<result trackID="SilverStone" driver="40pints" classV="LMS GT1" carName="Aston Martin V8" s1="12.5" s2="14.6" s3="56.8" lapTime="1:41.673" theDate="28-02-2010" totalLapTime="101.673"/>'],
            ['<result trackID="Monaco" driver="R1K" classV="F1 2008" carName="Ferrari" s1="12.5" s2="14.6" s3="56.8" lapTime="1:24.673" theDate="28-02-2010" totalLapTime="84.673"/>'],
            ['<result trackID="Monaco" driver="40pints" classV="F1 2008" carName="Williams" s1="12.5" s2="14.6" s3="56.8" lapTime="1:23.673" theDate="28-02-2010" totalLapTime="83.673"/>']
            ]

if __name__ == '__main2__':

    print "Python HotLaps test client"

    host = "127.0.0.1"
    port = 1234
    
    cs = clientSocket.clientSckt()
    
    for i in testData:
        data = raw_input ( "Press a key to send the next result:" )
        if (data <> 'Q' and data <> 'q'):
            cs.createConnection(host, port)
            cs.send(i[0])
            cs.close()
        else:
            break
    
import sys
import ConfigParser
from hotLapsServer import ReadConfigFileSection
import hotLaps_db
import produceReports
    
if __name__ == '__main__':

    print "Python HotLaps test XML"

    configFile = ConfigParser.RawConfigParser()
    if len(sys.argv) >= 2:
        #read config and overwrite the conf structure
        try:
            configFile.read(sys.argv[1]) 
            conf = []
            for cfg in configFile.sections():
                row = ReadConfigFileSection(configFile, cfg)  
                conf.append(row)
        except:
            print >> sys.stderr, "Problem reading config file - exiting!"
            exit()
    else:
        print >> sys.stderr, "Need to pass the config file on the command line as an option"
        exit()
    config = conf[0]

    if not 'recordsstore' in config: 
        print >> sys.stderr, "No database file specified"        
        exit()
        
        
    db = hotLaps_db.hotLapsDataBase(config['recordsstore'])
    op = produceReports.xmlOutput(db,config['hotlapsxml'], config['uniquelapsxml'])
    
    op.run()
