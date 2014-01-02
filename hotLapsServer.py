#!/usr/bin/env python

import ConfigParser
import sys
from socketHandler import rfactorHotlapsServer

threads = []

def ReadConfigFileSection( config, section ):
    """
    Reads the config file 1 section per run
    """
    dict1 = {}
    dict1['config'] = section
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            print >> sys.stderr, ("Exception on %s!" % option)
            dict1[option] = None
    return dict1

def parseCommand( cmd ):

    cmd = cmd.rstrip()
    
    command = {}
    
    if cmd[0:4].lower() == ("quit"):
        command['quit'] = True
    
    elif cmd[0:5].lower() == "query":
        command['query'] = command[5:].rstrip()

    else:
        print "unknown command"
    
    return command 



if __name__ == '__main__':

    print "Python HotLaps Server"

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


    ADDR = (config['server'], int(config['port']) )
    sh = rfactorHotlapsServer( ADDR, config['recordsstore'], [config['hotlapsxml'], config['uniquelapsxml']], config['postUrl'] )
    sh.start()
    
    continueRunning = True
    while (continueRunning):
    
        cmd = sys.stdin.readline()
        message = parseCommand(cmd)
        
        if ('quit' in message) :
            if  message['quit'] == True:
                print "quiting..."
                continueRunning = False
                # kill the socket handling thread

    sh.stopRunning()
