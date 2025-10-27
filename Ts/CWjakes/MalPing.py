from scapy.all import *

for x in range(20):
  send(IP(dst="www.google.com", src="192.168.43.31")/ICMP()/"AleJaja")

