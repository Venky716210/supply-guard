import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime
import random
import os

# ===================== BEAUTIFUL STYLING =====================
st.set_page_config(page_title="supply chain disruption early warning system", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main {background: linear-gradient(135deg, #0f172a 0%, #1e2937 100%);}
    .metric-card {background: rgba(30, 41, 59, 0.9); border-radius: 12px; padding: 15px; border: 1px solid #475569;}
    h1, h2 {color: #60a5fa;}
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ supply chain disruption early warning system")
st.markdown("### AI-Powered Supply Chain Disruption Early Warning System")

# ===================== DATA FOLDER & GENERATION =====================
if not os.path.exists("data"):
    os.makedirs("data")

@st.cache_data
def load_or_generate_data():
    data_path = "data/suppliers_data.csv"
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        np.random.seed(42)
        suppliers = ['Foxconn (India)', 'Samsung (Vietnam)', 'Bosch (Germany)', 'Pfizer (USA)', 
                     'Nestle (Switzerland)', 'Intel (Malaysia)', 'Maersk Logistics', 'Tata Steel (India)']
        
        df = pd.DataFrame({
            'Supplier': suppliers,
            'Country': ['India', 'Vietnam', 'Germany', 'USA', 'Switzerland', 'Malaysia', 'Global', 'India'],
            'Geopolitical_Risk': np.round(np.random.uniform(0.20, 0.95, 8), 2),
            'Climate_Anomaly': np.round(np.random.uniform(0.15, 0.92, 8), 2),
            'Weather_Condition': np.random.choice(['Normal', 'Storm', 'Flood', 'Extreme Heat', 'Heavy Rain'], 8),
            'Transport_Risk': np.round(np.random.uniform(0.25, 0.90, 8), 2),
            'Demand_Fluctuation': np.random.randint(15, 85, 8)
        })
        
        # Risk Score with good weight to Climate and Geopolitical
        df['Risk_Score'] = (
            df['Geopolitical_Risk'] * 0.35 +
            df['Climate_Anomaly'] * 0.30 +
            df['Transport_Risk'] * 0.20 +
            df['Demand_Fluctuation']/100 * 0.15
        ) * 100
        
        df['Risk_Score'] = df['Risk_Score'].round(1)
        df['Risk_Level'] = pd.cut(df['Risk_Score'], bins=[0,40,65,100], labels=['Low 🟢', 'Medium 🟠', 'High 🔴'])
        df.to_csv(data_path, index=False)
    
    return df

data = load_or_generate_data()

# ===================== SIDEBAR =====================
st.sidebar.markdown("### 🛠️ Controls")
risk_threshold = st.sidebar.slider("🚨 Risk Alert Threshold (%)", 30, 90, 65)

if st.sidebar.button("🔄 Refresh All Signals", use_container_width=True):
    st.rerun()

# ===================== HEADER =====================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall Risk", "HIGH 🔴", "↑ 28%")
c2.metric("High Risk Suppliers", str(len(data[data['Risk_Level']=='High'])))
c3.metric("Active Climate Alerts", "5")
c4.metric("Last Updated", datetime.now().strftime("%d %b %H:%M"))

st.divider()

# ===================== TABS =====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Risk Overview", 
    "🌡️ Climate & Geopolitical Signals", 
    "📰 Live News", 
    "🗺️ World Risk Map", 
    "🤖 AI Copilot", 
    "⚔️ Crisis Comparison"
])

with tab1:
    st.subheader("Supplier Risk Scoring")
    fig = px.bar(data.sort_values('Risk_Score', ascending=False), 
                 x='Supplier', y='Risk_Score', color='Risk_Level',
                 color_discrete_map={'Low':'#22c55e', 'Medium':'#eab308', 'High':'#ef4444'})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(data, use_container_width=True)

with tab2:
    st.subheader("🌡️ Climate Conditions & Geopolitical Events")

    st.markdown("### **Overall Status Cards**")
    col1, col2, col3 = st.columns(3)

    avg_geo = data['Geopolitical_Risk'].mean()
    avg_climate = data['Climate_Anomaly'].mean()

    with col1:
        geo_status = "🔴 High" if avg_geo > 0.65 else "🟠 Medium" if avg_geo > 0.4 else "🟢 Safe"
        st.metric("Geopolitical Risk", f"{avg_geo:.2f}", geo_status)

    with col2:
        climate_status = "🔴 High" if avg_climate > 0.65 else "🟠 Medium" if avg_climate > 0.4 else "🟢 Safe"
        st.metric("Climate / Weather Risk", f"{avg_climate:.2f}", climate_status)

    with col3:
        st.metric("Average Risk Score", f"{data['Risk_Score'].mean():.1f}")

    st.markdown("---")

    # Supplier-wise detailed cards
    st.markdown("### **Supplier-wise Status**")
    for _, row in data.iterrows():
        geo_color = "🔴" if row['Geopolitical_Risk'] > 0.65 else "🟠" if row['Geopolitical_Risk'] > 0.4 else "🟢"
        climate_color = "🔴" if row['Climate_Anomaly'] > 0.65 else "🟠" if row['Climate_Anomaly'] > 0.4 else "🟢"
        
        with st.container(border=True):
            st.markdown(f"**{row['Supplier']}**  ({row['Country']})")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Geopolitical Events", f"{row['Geopolitical_Risk']:.2f}", geo_color)
            with col_b:
                st.metric("Climate / Weather", f"{row['Climate_Anomaly']:.2f} | {row['Weather_Condition']}", climate_color)
            with col_c:
                st.metric("Overall Risk", f"{row['Risk_Score']:.1f}", row['Risk_Level'])

with tab3:
    st.subheader("📰 Live News Monitor")
    for item in ["🌪️ Severe Cyclone alert near Indian ports", 
                 "🌧️ Heavy flooding in Southeast Asia", 
                 "⚠️ Strait of Hormuz tensions rising", 
                 "🔥 Extreme heatwave affecting supply routes"]:
        st.warning(item)

with tab4:
    st.subheader("🗺️ Live World Risk Map")
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    for _, row in data.iterrows():
        color = "red" if row['Risk_Score'] > 65 else "orange" if row['Risk_Score'] > 40 else "green"
        folium.Marker(location=[random.uniform(8, 55), random.uniform(-100, 120)],
                      popup=f"{row['Supplier']}<br>Risk: {row['Risk_Score']}",
                      icon=folium.Icon(color=color)).add_to(m)
    st_folium(m, width=1300, height=600)

with tab5:
    st.subheader("🤖 AI Copilot")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me about climate, weather or geopolitical risks."}]
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        st.session_state.messages.append({"role": "assistant", "content": "Current high risks are driven by **Climate Anomaly** and **Geopolitical Events**."})
        with st.chat_message("assistant"): st.write("Current high risks are driven by **Climate Anomaly** and **Geopolitical Events**.")

with tab6:
    st.subheader("⚔️ Crisis Comparison")
    st.info("Iran Conflict 2026 is causing higher **Geopolitical** and indirect **Climate-related** disruptions compared to 2022 Russia-Ukraine war.")

