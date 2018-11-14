#!/usr/bin/python

import pymssql
import datetime

server = "127.0.0.1"
user = "user"
password = "secret"


conn = pymssql.connect(server, user, password, "WebCC")
cursor = conn.cursor()

cursor.execute('SELECT Job.JobId,Result,DateTime,Errors,Warnings,computerName,Name,Agent.description,Agent.type FROM [WebCC].[dbo].[JobStatus] INNER JOIN WebCC.dbo.Job ON (WebCC.dbo.JobStatus.JobId = WebCC.dbo.Job.JobId) INNER JOIN WebCC.dbo.Agent ON (WebCC.dbo.JobStatus.AgentId = WebCC.dbo.Agent.agentID) WHERE WebCC.dbo.JobStatus.Type = %s;',"BACKUP")
rows = cursor.fetchall()

cmk_dict = {}
database = []

print '<<<evault_jobs>>>'

for row in rows:
    if not row[7]:
        pass
    elif row[7].startswith('NO-'):
        pass
    elif row[7].startswith('CMK-'):
        # CheckMK Piggyback add to array for later use
        hostname = row[7][4:]
        try:
            cmk_dict[hostname]
        except:
            cmk_dict[hostname] = {}
            database.append(hostname)
        cmk_dict[hostname][row[0]] = {}
        cmk_dict[hostname][row[0]]['Result'] = row[1]
        cmk_dict[hostname][row[0]]['DateTime'] = row[2]
        cmk_dict[hostname][row[0]]['computerName'] = row[5]
        cmk_dict[hostname][row[0]]['Name'] = row[6]
        cmk_dict[hostname][row[0]]['hostname'] = row[7][4:]
        cmk_dict[hostname][row[0]]['AgentType'] = row[8]
    else:
        print str(row[7])+"_"+str(row[5])+ "_"+str(row[6])+" "+str(row[8])+" "+str(row[1])+" "+str(datetime.datetime.strftime(row[2],'%Y-%m-%d %H:%M:%S'))

for row in database:
    print "<<<<"+str(row)+">>>>"
    print '<<<evault_jobs>>>'
    for key in cmk_dict[row]:
        print cmk_dict[row][key]['Name']+" "+cmk_dict[row][key]['AgentType']+" "+cmk_dict[row][key]['Result']+" "+str(datetime.datetime.strftime(cmk_dict[row][key]['DateTime'],'%Y-%m-%d %H:%M:%S'))

