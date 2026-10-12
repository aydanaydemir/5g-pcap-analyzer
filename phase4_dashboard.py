import streamlit as st
import plotly.express as px
from phase3_analyzer import NetworkAnalyzer

# Page configuration
st.set_page_config(
    page_title="5G PCAP Analyzer",
    page_icon="📶",
    layout="wide"
)

# Header
st.title("📶 5G & IP Packet Analyzer Dashboard")
st.markdown("""
This professional dashboard analyzes network traffic from a PCAP file using Scapy and Pandas.
It simulates real-time monitoring of Subscriber IP bandwidth, protocol distribution, and traffic spikes.
""")

# Load Data
@st.cache_data
def load_and_analyze_data():
    analyzer = NetworkAnalyzer("sample_traffic.pcap")
    success = analyzer.load_data()
    return analyzer if success else None

with st.spinner("Analyzing PCAP file..."):
    analyzer = load_and_analyze_data()

if not analyzer:
    st.error("Failed to load or parse the PCAP file. Please ensure 'sample_traffic.pcap' exists.")
else:
    st.success(f"Successfully loaded and parsed {len(analyzer.df)} packets.")
    
    # KPIs Row
    st.markdown("### 📊 Key Performance Indicators (KPIs)")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    total_bandwidth = analyzer.df['length'].sum() / 1024 # KB
    total_packets = len(analyzer.df)
    unique_ips = analyzer.df['src_ip'].nunique()
    
    kpi1.metric("Total Traffic Processed", f"{total_bandwidth:.2f} KB")
    kpi2.metric("Total Packets", f"{total_packets}")
    kpi3.metric("Unique Subscribers (UEs)", f"{unique_ips}")
    
    st.divider()

    # Visualizations Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bandwidth Usage by Subscriber (IP)")
        bw_df = analyzer.get_bandwidth_per_ip()
        fig_bw = px.bar(
            bw_df, x='Source IP', y='Total Bytes', 
            color='Total Bytes', color_continuous_scale='Blues',
            text_auto='.2s'
        )
        st.plotly_chart(fig_bw, use_container_width=True)
        
    with col2:
        st.subheader("Protocol Distribution")
        proto_df = analyzer.get_protocol_distribution()
        fig_proto = px.pie(
            proto_df, names='Protocol', values='Packet Count',
            hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_proto, use_container_width=True)
        
    st.divider()
    
    # Visualizations Row 2
    st.subheader("Network Traffic Over Time")
    time_df = analyzer.get_traffic_over_time()
    fig_time = px.line(
        time_df, x='Time', y='Total Bytes/s', 
        markers=True, line_shape="spline",
        title="Traffic Spikes (Bytes per Second)"
    )
    # Fill area under the line
    fig_time.update_traces(fill='tozeroy')
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Raw Data Expander
    with st.expander("Show Raw PCAP Data"):
        st.dataframe(analyzer.df, use_container_width=True)
