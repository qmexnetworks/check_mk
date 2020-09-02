#!/usr/bin/python2.7

import ConfigParser
import MySQLdb
import os


if os.path.isfile("/etc/check_mk/database.cfg"):
    CONFIG_FILE = "/etc/check_mk/database.cfg"
    CONFIG = ConfigParser.ConfigParser()

    def config_map(section):
        """ Function for CONFIG_FILE """
        dict1 = {}
        options = CONFIG.options(section)
        for option in options:
            try:
                dict1[option] = CONFIG.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print "exception on %s!" % option
                dict1[option] = None
        return dict1
    try:
        CONFIG.read(CONFIG_FILE)
    except:
        print "/etc/check_mk/database.cfg not existing"
        sys.exit(1)
    
    #connect to database
    connection = MySQLdb.connect(host=config_map("MySQL")['server'], user=config_map("MySQL")['username'], passwd=config_map("MySQL")['password'], db=config_map("MySQL")['database'])
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM (SELECT cdr_id FROM cdrs WHERE calltype = 'outbound' AND DATE(call_start_time) = CURDATE() GROUP BY sip_call_id) t")
    row = cursor.fetchone()
    outbound = int(row[0])

    cursor.execute("SELECT COUNT(*) FROM (SELECT cdr_id FROM cdrs WHERE calltype = 'inbound' AND DATE(call_start_time) = CURDATE() GROUP BY sip_call_id) t")
    row = cursor.fetchone()
    inbound = int(row[0])

    print "0 QTelecom-CallStats outbound="+str(outbound)+"|inbound="+str(inbound)+" OK - No output, only perfdata"
