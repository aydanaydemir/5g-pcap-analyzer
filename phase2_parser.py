import os
from scapy.all import rdpcap, IP, TCP, UDP

def parse_pcap(filename="sample_traffic.pcap"):
    """
    Reads a PCAP file and parses it to extract key network metrics.
    Returns a list of dictionaries containing parsed packet data.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Error: The file {filename} does not exist.")
        
    print(f"Reading and parsing {filename}... This might take a moment.")
    
    # Read the PCAP file
    packets = rdpcap(filename)
    parsed_data = []

    for pkt in packets:
        # We only care about IP packets for this analysis
        if IP in pkt:
            timestamp = float(pkt.time)
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            length = len(pkt)
            
            # Determine the protocol (TCP or UDP)
            protocol = "Other"
            src_port = None
            dst_port = None
            
            if TCP in pkt:
                protocol = "TCP"
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
            elif UDP in pkt:
                protocol = "UDP"
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
                
            # Append the parsed data as a dictionary
            parsed_data.append({
                "timestamp": timestamp,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": protocol,
                "src_port": src_port,
                "dst_port": dst_port,
                "length": length
            })
            
    print(f"Successfully parsed {len(parsed_data)} IP packets.")
    return parsed_data

if __name__ == "__main__":
    # Test the parser directly
    data = parse_pcap()
    if data:
        print("Sample of parsed data (first 3 packets):")
        for i in range(min(3, len(data))):
            print(data[i])
