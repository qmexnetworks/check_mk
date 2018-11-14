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

print '<<<evault_jobs>>>'

for row in rows:
    if row[6].startswith('NO-'):
        pass
    elif row[6].startswith('CMK-'):
        # CheckMK Piggyback add to array for later use
        cmk_dict[row[0]] = {}
        cmk_dict[row[0]]['Result'] = row[1]
        cmk_dict[row[0]]['DateTime'] = row[2]
        cmk_dict[row[0]]['Errors'] = row[3]
        cmk_dict[row[0]]['Warnings'] = row[4]
        cmk_dict[row[0]]['computerName'] = row[5]
        cmk_dict[row[0]]['Name'] = row[6]
        cmk_dict[row[0]]['hostname'] = row[7][4:]
        cmk_dict[row[0]]['AgentType'] = row[8]
    else:
        print str(row[8])+" "+str(row[7])+" "+str(row[5])+ " "+str(row[6])+" "+str(row[1])+" "+str(row[4])+" "+str(row[3])+" "+str(datetime.datetime.strftime(row[2],'%Y-%m-%d %H:%M:%S'))

