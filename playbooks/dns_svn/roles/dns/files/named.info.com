$TTL 600
@                       IN SOA   dns1.info.com. dns2.info.com. (2016090201 3H 15M 1W 1D)
@                       IN NS    dns1.info.com.
@                       IN NS    dns2.info.com.
dns1.info.com.    	IN A     192.168.100.1
dns2.info.com.    	IN A     192.168.100.1

tg		        IN A     120.76.239.84
