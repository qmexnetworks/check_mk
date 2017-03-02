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
    print("<<<<"+str(row[1])+">>>>")
    print("<<<bareos_jobs>>>")
    cursor.execute("SELECT CONVERT(t0.Job USING utf8), CONVERT(t0.Name USING utf8), t0.EndTime FROM Job AS t0 LEFT JOIN Job AS t1 ON t1.Name=t0.Name AND t1.JobId>t0.JobId WHERE t0.ClientId = %s AND CONVERT(t0.Name USING utf8) != 'RestoreFiles' AND CONVERT(t0.JobStatus USING utf8) != 'R' AND t1.JobId IS NULL", (row[0],))
    rowsb = cursor.fetchall()
    for rowb in rowsb:
        # Catch Jobs with Wrong name and Ignore them
        try:
            jobname = rowb[1].split("_")[1]
            error = False
        except:
            error = True
        if not error:
            print str(jobname)+" "+str(rowb[2])
    