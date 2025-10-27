from scapy.all import IP, ICMP, sr1
import time

def my_traceroute(destination, max_hops=30, timeout=2):
    print(f"Traceroute to {destination}, max hops = {max_hops}\n")
    for ttl in range(1, max_hops + 1):
        pkt = IP(dst=destination, ttl=ttl) / ICMP()
        start = time.time()
        reply = sr1(pkt, verbose=0, timeout=timeout)
        end = time.time()

        if reply is None:
            print(f"{ttl}: Request timed out.")
        else:
            rtt = round((end - start) * 1000, 2)
            print(f"{ttl}: {reply.src} - {rtt} ms")
            if reply.type == 0:  # ICMP Echo Reply
                print("Destination reached.")
                break

my_traceroute(input("Podaj ip: "))
