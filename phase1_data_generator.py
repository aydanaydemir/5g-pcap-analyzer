import time
import random
from scapy.all import Ether, IP, TCP, UDP, Raw, wrpcap

def generate_synthetic_pcap(filename="sample_traffic.pcap", num_packets=500):
    """
    Generates a synthetic PCAP file simulating network traffic from multiple subscribers.
    This simulates standard IP traffic (TCP/UDP) as a baseline for our 5G Analyzer.
    """
    print(f"Generating {num_packets} synthetic packets...")
    packets = []
    
    # Simulate a few different UE (User Equipment) IP addresses
    ue_ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]
    # Simulate some external servers (e.g., Netflix, Google, Meta)
    server_ips = ["142.250.190.46", "3.211.23.1", "157.240.22.35"]

    start_time = time.time() - 3600 # Start generating traffic from an hour ago
    
    for i in range(num_packets):
        src_ip = random.choice(ue_ips)
        dst_ip = random.choice(server_ips)
        
        # 80% TCP (HTTP/Video), 20% UDP (DNS/Gaming/Voice)
        protocol = "TCP" if random.random() < 0.8 else "UDP"
        
        # Simulate different payload sizes (video stream = large, text = small)
        payload_size = random.randint(64, 1400)
        payload = Raw(b"X" * payload_size)

        if protocol == "TCP":
            # Simulate a standard TCP packet
            pkt = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=random.randint(1024, 65535), dport=random.choice([80, 443]))/payload
        else:
            # Simulate a standard UDP packet
            pkt = Ether()/IP(src=src_ip, dst=dst_ip)/UDP(sport=random.randint(1024, 65535), dport=random.choice([53, 5060]))/payload
        
        # Simulate a slight delay between packets to make timestamps realistic (0.001s to 0.05s)
        pkt.time = start_time + (i * random.uniform(0.001, 0.05))
        packets.append(pkt)
        
    # Write packets to PCAP file
    wrpcap(filename, packets)
    print(f"Successfully generated '{filename}' with {len(packets)} packets.")

if __name__ == "__main__":
    generate_synthetic_pcap()
