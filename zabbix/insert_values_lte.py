import requests
import json
import pandas as pd
import datetime
import time
import os

ZABBIX_API_URL = "http://172.21.245.195/zabbix/api_jsonrpc.php"
UNAME = "gangbukkt1"
PWORD = "gangbuk1@#$"

def get_zabbix_values():
    now = datetime.datetime.now()
    print(now)         

    nowDate = now.strftime('%Y-%m-%d')
    print(nowDate)      
    
    nowTime = now.strftime('%H') + '00'
    print(nowTime)      

    #get authtoken
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
    print(AUTHTOKEN)

    #get items(include temperature)
    r3 = requests.post(ZABBIX_API_URL, 
    json = {  
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "search": {
                "key_": "temp"
            },
        },
        "id": 1,
        "auth": AUTHTOKEN
    })
    data3 = json.dumps(r3.json(), sort_keys=True)
    js3 = json.loads(data3)

    #logout user
    print("\nLogout user")
    r = requests.post(ZABBIX_API_URL,
                      json={
                          "jsonrpc": "2.0",
                          "method": "user.logout",
                          "params": {},
                          "id": 2,
                          "auth": AUTHTOKEN
                      })

    print(json.dumps(r.json(), indent=4, sort_keys=True))

    hostid_list2 = []
    value_list = []
    for i in js3['result']:
        hostid_list2.append(i['hostid'])
        value_list.append(i['lastvalue'])
    value = pd.DataFrame({'date' : nowDate, 'time' : nowTime, 'host_id' : hostid_list2, 'temperature' : value_list})
    print(value)

    return value

if __name__ == "__main__":
    value = get_zabbix_values()
    print(value)
    #scripts/database/zabbix
    value.to_csv('/root/scripts/database/zabbix/zabbix_values_lte.csv', header=True, index=False, columns=['date', 'time', 'host_id', 'temperature'])
    os.system('/root/scripts/database/zabbix/insert_values_lte.sh')