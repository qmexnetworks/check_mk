#!/usr/bin/python2.7

import ConfigParser
import MySQLdb
import sys

CONFIG_FILE = "/etc/check_mk/bareos_jobs.cfg"

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
    print "/etc/check_mk/bareos_jobs.cfg not existing"
    sys.exit(1)

#connect to database
connection = MySQLdb.connect(host=config_map("MySQL")['server'], user=config_map("MySQL")['username'], passwd=config_map("MySQL")['password'], db=config_map("MySQL")['database'])
cursor = connection.cursor()

cursor.execute("SELECT ClientId, CONVERT(Name USING utf8) FROM `Client`;")
rows = cursor.fetchall()
for row in rows:
    print row[1]
    cursor.execute("SELECT CONVERT(Name USING utf8),CONVERT(JobStatus USING utf8),JobErrors FROM Job WHERE ClientId = %s AND CONVERT(Name USING utf8) != 'RestoreFiles' ORDER BY RealEndTime DESC LIMIT 1;", (row[0],))
    rowb = cursor.fetchone()
    print rowb
    