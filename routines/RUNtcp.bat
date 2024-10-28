#!/bin/bash
##python tcp_connect.py -host 172.24.32.1 -port 8267
##python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn 38 -dirname K:\\RUNDATA\\TCPdata
##python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn 38 -dirname K:\\RUNDATA\\TCPdata
##python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn 48 -dirname K:\\RUNDATA\\TCPdata
##python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn $1 -dirname K:\\RUNDATA\\TCPdata -alldata 1
##python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn $1 -dirname K:\\RUNDATA\\TCPdata
##python tcp_connect_TODISABLE.py -host 134.158.137.124 -port 8247 -vrefn $1 -dirname K:\\RUNDATA\\TCPdata
#################python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn $1 -dirname K:\\RUNDATA\\TCPdata
python tcp_connect.py -host 134.158.139.27 -port 8247  -vrefn $1 -dirname K:\\RUNDATA\\TCPdata
##python tcp_connect.py -host 134.158.137.124 -port 8247 -vrefn 35 -dirname K:\\RUNDATA\\TCPdata
##python tcp_connect.py -host 134.158.139.27 -port 8267 -vrefn 150 -dir_name "K:\\RUNDATA\\TCP_IP7"
##for VREFN in {40..41}; do python tcp_connect.py -host 134.158.139.27 -port 8267 -vrefn $VREFN ; done
