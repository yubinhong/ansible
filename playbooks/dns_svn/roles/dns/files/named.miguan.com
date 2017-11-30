$TTL 600
@                       IN SOA   dns1.miguan.com. dns2.miguan.com. (2016090201 3H 15M 1W 1D)
@                       IN NS    dns1.miguan.com.
@                       IN NS    dns2.miguan.com.
dns1.miguan.com.    	IN A     192.168.100.1
dns2.miguan.com.    	IN A     192.168.100.1

baobiao		        IN A     192.168.100.1
zabbix		        IN A     192.168.100.1
kibana		        IN A     192.168.100.3
svnadmin	        IN A     192.168.100.1
svn		        IN A     192.168.100.1
download	        IN A     192.168.100.1
oa		        IN A     192.168.100.1
grafana		        IN A     192.168.100.1
design		        IN A     192.168.100.1
pha		        IN A     192.168.100.1
gitlab		        IN A     192.168.100.4
git		        IN A     192.168.100.4
jenkins		        IN A     192.168.100.4
doexcel		        IN A     192.168.100.4
cmdb			IN A 	 192.168.100.5
bearychat		IN A 	 192.168.100.5
sonar      		IN A 	 192.168.100.5
monitor      		IN A 	 192.168.100.5
sql			IN A	 192.168.100.5
cms      		IN A 	 192.168.100.6
