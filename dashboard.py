import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Satellite Intelligence Dashboard", layout="wide")

st.title("🌍 Satellite Image Intelligence Platform")
st.markdown("### AI-Powered Environmental Monitoring and Disaster Analysis")

# Sidebar
st.sidebar.header("Upload Satellite Imagery")
uploaded_file = st.sidebar.file_uploader("Choose a satellite TIFF/JPG...", type=["tif", "tiff", "jpg", "jpeg", "png"])

analysis_type = st.sidebar.selectbox("Analysis Type", ["Flood Detection", "Wildfire Spread", "Urban Growth", "Land Use Change"])

if st.sidebar.button("Run Intelligence Analysis"):
    if uploaded_file:
        with st.spinner("Processing geospatial data..."):
            # Mocking the API call for demonstration
            # In a real app, you'd send the file to the API
            # response = requests.post(f"{API_URL}/upload_image", files={"file": uploaded_file})
            # file_id = response.json()["file_id"]
            # analysis_response = requests.post(f"{API_URL}/analyze", json={"file_id": file_id})
            
            # Mock Results
            results = {
                "flood_area": 12.4,
                "urban_growth": 25,
                "veg_loss": 11,
                "wildfire": True,
                "summary": "The region shows significant urban expansion and declining vegetation coverage over the past three years, with flood-prone areas increasing near river boundaries."
            }
            st.session_state['results'] = results
            st.success("Analysis Complete!")
    else:
        st.sidebar.error("Please upload an image first.")

# Main Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Interactive Geospatial Map")
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5) # Default India location
    
    # Example overlay (mock)
    if 'results' in st.session_state:
        folium.Marker(
            [22.5726, 88.3639], # Example Kolkata area
            popup="Flood Zone Detected",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        folium.Circle(
            location=[23.5726, 89.3639],
            radius=5000,
            color='red',
            fill=True,
            fill_color='red',
            popup="Active Wildfire Area"
        ).add_to(m)

    st_folium(m, width=700, height=500)

with col2:
    st.subheader("Intelligence Insights")
    if 'results' in st.session_state:
        res = st.session_state['results']
        st.info(res['summary'])
        
        st.write("#### Key Metrics")
        metrics_df = pd.DataFrame({
            "Metric": ["Flood Area", "Urban Growth", "Veg Loss"],
            "Value": [f"{res['flood_area']} sq km", f"{res['urban_growth']}%", f"{res['veg_loss']}%"]
        })
        st.table(metrics_df)
        
        # Mini Chart
        fig, ax = plt.subplots()
        ax.bar(["Flood", "Urban", "Veg Loss"], [res['flood_area'], res['urban_growth'], res['veg_loss']])
        st.pyplot(fig)
        
        if st.button("Generate Detailed PDF Report"):
            st.write("Generating report... [Link to Download]")
    else:
        st.write("Upload and analyze an image to see insights.")

st.divider()
st.markdown("Developed by Antigravity AI - Advanced Geospatial Intelligence")
