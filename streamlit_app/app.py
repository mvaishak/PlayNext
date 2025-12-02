"""
Steam Game Recommender System - Streamlit Web App
A comprehensive web interface to explore game recommendations with Steam-inspired design
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path
import sys

# Add parent directory to path to import utilities
sys.path.append(str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="PlayNext - Steam Game Recommender",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Steam theme
st.markdown("""
<style>
    /* Steam Dark Theme */
    :root {
        --steam-dark: #1b2838;
        --steam-darker: #171a21;
        --steam-light: #2a475e;
        --steam-blue: #66c0f4;
        --steam-green: #5cb85c;
    }
    
    /* Hide default Streamlit navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Main background */
    .stApp {
        background-color: #1b2838;
        color: #c7d5e0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #171a21;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #66c0f4 !important;
        font-family: 'Motiva Sans', Arial, sans-serif;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #66c0f4;
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #c7d5e0;
    }
    
    /* Game cards */
    .game-card {
        background: linear-gradient(135deg, #1e3a52 0%, #2a475e 100%);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #3d5a73;
        transition: all 0.3s ease;
    }
    
    .game-card:hover {
        border-color: #66c0f4;
        box-shadow: 0 0 20px rgba(102, 192, 244, 0.3);
        transform: translateY(-2px);
    }
    
    .game-title {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    
    .game-score {
        color: #66c0f4;
        font-size: 1rem;
        font-weight: bold;
    }
    
    .game-meta {
        color: #8f98a0;
        font-size: 0.9rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3d5a73 0%, #2a475e 100%);
        color: #ffffff;
        border: 1px solid #66c0f4;
        border-radius: 3px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #66c0f4 0%, #4a9cd4 100%);
        border-color: #ffffff;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #2a475e;
        color: #c7d5e0;
        border-color: #3d5a73;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1e3a52 0%, #2a475e 100%);
        border-left: 4px solid #66c0f4;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, #171a21 0%, #1b2838 100%);
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #3d5a73;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        background: #5cb85c;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
        margin: 2px;
    }
    
    .badge-blue {
        background: #66c0f4;
    }
    
    .badge-orange {
        background: #ff6b2c;
    }
</style>
""", unsafe_allow_html=True)

# Import page modules
from pages import home, user_recommendations, model_explorer, about

# Sidebar navigation
st.sidebar.title("🎮 PlayNext")
st.sidebar.markdown("### Steam Game Recommender")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "👤 User Recommendations", "🔬 Model Explorer", "📊 About"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Load data info for sidebar
try:
    with open("../model_outputs/final_evaluation_results.json", "r") as f:
        eval_results = json.load(f)
    
    st.sidebar.markdown("### 📈 Quick Stats")
    st.sidebar.metric("Hit Rate@10", f"{eval_results['task1_next_game_prediction']['10']['hit_rate']['mean']:.1%}")
    st.sidebar.metric("NDCG@10", f"{eval_results['task1_next_game_prediction']['10']['ndcg']['mean']:.3f}")
    st.sidebar.metric("Total Users", f"{eval_results['dataset_info']['n_users']:,}")
    st.sidebar.metric("Total Games", f"{eval_results['dataset_info']['n_items']:,}")
except:
    pass

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #8f98a0; font-size: 0.85rem;'>
    <p>Built with Streamlit</p>
    <p>CSE258R - Fall 2024</p>
</div>
""", unsafe_allow_html=True)

# Route to appropriate page
if page == "🏠 Home":
    home.show()
elif page == "👤 User Recommendations":
    user_recommendations.show()
elif page == "🔬 Model Explorer":
    model_explorer.show()
elif page == "📊 About":
    about.show()
