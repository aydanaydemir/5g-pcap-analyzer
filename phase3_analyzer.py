import pandas as pd
from phase2_parser import parse_pcap

class NetworkAnalyzer:
    def __init__(self, pcap_file="sample_traffic.pcap"):
        self.pcap_file = pcap_file
        self.df = None
        
    def load_data(self):
        """
        Loads the parsed PCAP data into a Pandas DataFrame for analysis.
        """
        parsed_data = parse_pcap(self.pcap_file)
        if not parsed_data:
            print("No data found to analyze.")
            return False
            
        self.df = pd.DataFrame(parsed_data)
        
        # Convert timestamp to datetime for time-series analysis
        self.df['datetime'] = pd.to_datetime(self.df['timestamp'], unit='s')
        return True

    def get_bandwidth_per_ip(self):
        """
        Calculates total bytes (bandwidth) consumed by each Source IP.
        """
        if self.df is None:
            return None
        
        # Group by Source IP and sum the length of packets
        bw_df = self.df.groupby('src_ip')['length'].sum().reset_index()
        bw_df.columns = ['Source IP', 'Total Bytes']
        bw_df = bw_df.sort_values(by='Total Bytes', ascending=False)
        return bw_df

    def get_protocol_distribution(self):
        """
        Counts the number of packets per protocol.
        """
        if self.df is None:
            return None
            
        proto_df = self.df['protocol'].value_counts().reset_index()
        proto_df.columns = ['Protocol', 'Packet Count']
        return proto_df

    def get_traffic_over_time(self):
        """
        Groups traffic by seconds to show a time-series graph of network activity.
        """
        if self.df is None:
            return None
            
        # Set datetime as index and resample by 1 second ('1s' -> '1S' or similar, here we'll just group by rounded timestamp)
        # We can create a 'time_rounded' column
        time_df = self.df.copy()
        time_df['Time (s)'] = time_df['datetime'].dt.floor('s') # Floor to nearest second
        
        time_grouped = time_df.groupby('Time (s)')['length'].sum().reset_index()
        time_grouped.columns = ['Time', 'Total Bytes/s']
        return time_grouped

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    if analyzer.load_data():
        print("\n--- Network Analysis Results ---")
        
        print("\n1. Bandwidth per IP:")
        print(analyzer.get_bandwidth_per_ip())
        
        print("\n2. Protocol Distribution:")
        print(analyzer.get_protocol_distribution())
        
        print("\n3. Traffic over Time (First 5 seconds):")
        print(analyzer.get_traffic_over_time().head(5))
