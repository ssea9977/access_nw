import requests
import json
import pandas as pd
from sqlalchemy import create_engine

ZABBIX_API_URL = "http://172.21.245.195/zabbix/api_jsonrpc.php"
UNAME = "gangbukkt1"
PWORD = "gangbuk1@#$"

# get authtoken
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "user": UNAME,
                          "password": PWORD},
                      "id": 1
                  })
AUTHTOKEN = r.json()["result"]

# get group and host
r2 = requests.post(ZABBIX_API_URL, 
json = {  
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": "extend",
        "selectGroups": "extend"
    },
    "id": 1,
    "auth": AUTHTOKEN
})
data2 = json.dumps(r2.json(), sort_keys=True)
js2 = json.loads(data2)

groupid_list = []
group_list = []
hostid_list = []
host_list = []
name_list = []
for i in js2['result']:
    groupid_list.append(i['groups'][0]['groupid'])
    group_list.append(i['groups'][0]['name'])
    hostid_list.append(i['hostid'])
    host_list.append(i['host'])
    name_list.append(i['name'])
host = pd.DataFrame({'group_id' : groupid_list, 'group' : group_list, 'host_id' : hostid_list, 'host' : host_list, 'host_name' : name_list})
print(host)

db_connection_str = 'mysql+pymysql://root:Rkdqnrlte1q@172.21.27.208/oneview'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()
host.to_sql(name='zabbix_host_info_lte', con=db_connection, if_exists='append',index=False)  