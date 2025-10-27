from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP, ICMP

def packet_callback(pkt):
    if IP in pkt:
        ip_layer = pkt[IP]
        print(f"\nPacket: {ip_layer.src} -> {ip_layer.dst} | Protocol: {ip_layer.proto}",end="")

        if TCP in pkt:
            print(f" TCP Packet: {pkt[TCP].sport} -> {pkt[TCP].dport}")
        elif UDP in pkt:
            print(f" UDP Packet: {pkt[UDP].sport} -> {pkt[UDP].dport}")
        elif ICMP in pkt:
            print(" ICMP Packet")

def start_sniffing(interface=None, count=0):
    print(f"[*] Starting packet capture on interface: {interface or 'default'}")
    sniff(prn=packet_callback, iface=interface, count=count, store=0)


start_sniffing()