#!/bin/bash

#insert zabbix values(temperature)
/usr/bin/mysql -uroot -pRkdqnrlte1q -h 172.21.27.208 --local-infile -e "LOAD DATA LOCAL INFILE '/root/scripts/database/zabbix/zabbix_values_lte.csv' INTO TABLE oneview.zabbix_values_lte character set utf8 FIELDS TERMINATED BY ',' IGNORE 1 ROWS";