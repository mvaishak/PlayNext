"""
Utility functions for the Streamlit app
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from scipy.sparse import load_npz
import re

# Cache data loading functions
@st.cache_data
def load_evaluation_results():
    """Load evaluation results from JSON"""
    try:
        with open("../model_outputs/final_evaluation_results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Evaluation results not found. Please run the complete_steam_recommender.ipynb first.")
        return None

@st.cache_data
def load_precomputed_recommendations():
    """Load pre-computed recommendations for all users"""
    try:
        with open("../model_outputs/all_user_recommendations.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("Pre-computed recommendations not found. Using sample data...")
        try:
            with open("../model_outputs/sample_recommendations.json", "r") as f:
                return json.load(f)
        except:
            return []

@st.cache_data
def load_game_metadata():
    """Load game popularity and metadata"""
    try:
        game_df = pd.read_csv("../features/game_popularity.csv")
        return game_df
    except FileNotFoundError:
        st.error("Game metadata not found.")
        return None

@st.cache_data
def load_game_names():
    """Load game ID to name mapping"""
    try:
        with open("game_names.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty dict if not found
        return {}

@st.cache_data
def load_mappings():
    """Load ID mappings"""
    try:
        with open("../features/mappings.pkl", "rb") as f:
            mappings = pickle.load(f)
        return mappings
    except FileNotFoundError:
        st.error("Mappings not found.")
        return None

@st.cache_data
def load_comprehensive_results():
    """Load comprehensive evaluation results with baselines"""
    try:
        with open("../model_outputs/comprehensive_results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_resource
def load_models():
    """Load trained models (cached for entire session)"""
    try:
        with open("../model_outputs/trained_models.pkl", "rb") as f:
            models = pickle.load(f)
        return models
    except FileNotFoundError:
        st.error("Trained models not found. Please run the complete_steam_recommender.ipynb first.")
        return None

def get_steam_image_url(game_id, size="header"):
    """
    Generate Steam CDN image URL for a game
    
    Args:
        game_id: Steam app ID (extracted from game name or ID)
        size: "header" (460x215), "capsule_231x87", "capsule_sm_120" 
    
    Returns:
        URL string for the game's image
    """
    # Try to extract app ID from game_id string if it contains numbers
    app_id = extract_app_id(game_id)
    
    if app_id:
        if size == "header":
            return f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
        elif size == "capsule":
            return f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_231x87.jpg"
        elif size == "capsule_sm":
            return f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_sm_120.jpg"
    
    # Fallback placeholder
    return "https://via.placeholder.com/460x215/1b2838/66c0f4?text=Game+Image"

def extract_app_id(game_id):
    """
    Extract Steam app ID from game identifier
    
    The game_id might be in formats like:
    - "123456" (pure app ID)
    - "game_123456"
    - "app123456"
    """
    if not game_id:
        return None
    
    # Convert to string
    game_id_str = str(game_id)
    
    # Try to find numbers in the string
    numbers = re.findall(r'\d+', game_id_str)
    
    if numbers:
        # Return the first (or longest) number sequence
        return max(numbers, key=len) if len(numbers) > 1 else numbers[0]
    
    return None

def format_game_card(game_info, rank=None, show_image=True):
    """
    Create a styled game card with Steam theme using Streamlit components
    
    Args:
        game_info: Dict with item_id, score/confidence, and optionally item_idx
        rank: Recommendation rank (1, 2, 3, ...)
        show_image: Whether to show the Steam game image
    """
    import streamlit as st
    
    item_id = game_info.get('item_id', 'Unknown')
    score = game_info.get('score', game_info.get('confidence', 0))
    
    # Load game names and get the actual name
    game_names = load_game_names()
    game_name = game_names.get(str(item_id), f"Unknown Game")
    
    # Format score
    score_pct = f"{score * 100:.1f}%" if score < 10 else f"{score:.2f}"
    
    # Create rank badge
    rank_badge = f"<span style='background: #66c0f4; color: #1b2838; padding: 2px 8px; border-radius: 3px; font-weight: bold; margin-right: 8px;'>#{rank}</span>" if rank else ""
    
    if show_image:
        img_url = get_steam_image_url(item_id)
        # Use st.image with fallback
        try:
            st.image(img_url, width='stretch')
        except:
            st.image("https://via.placeholder.com/460x215/1b2838/66c0f4?text=Game+Image", width='stretch')
        
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Small spacing
    
    # Display title and score with better formatting
    st.markdown(f"<div style='background: #16202d; padding: 12px; border-radius: 4px; margin-bottom: 10px;'>"
                f"<div style='margin-bottom: 8px;'>{rank_badge}</div>"
                f"<div style='color: #66c0f4; font-weight: bold; font-size: 1.1em; margin-bottom: 5px;'>{game_name}</div>"
                f"<div style='color: #8f98a0; font-size: 0.85em; margin-bottom: 3px;'>App ID: {item_id}</div>"
                f"<div style='color: #8f98a0; font-size: 0.85em;'>Score: {score_pct}</div>"
                f"</div>", unsafe_allow_html=True)

def format_bundle_info(bundle_info):
    """Format bundle ownership information"""
    owned_pct = bundle_info['ownership_ratio'] * 100
    total_games = bundle_info['owned_count'] + bundle_info['missing_count']
    
    color = "#5cb85c" if owned_pct >= 70 else "#66c0f4" if owned_pct >= 40 else "#ff6b2c"
    
    html = f"""
    <div class="info-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>Bundle #{bundle_info['bundle_idx']}</strong><br>
                <span class="game-meta">
                    Owned: {bundle_info['owned_count']}/{total_games} games
                </span>
            </div>
            <div style="text-align: right;">
                <span style="color: {color}; font-size: 1.5rem; font-weight: bold;">
                    {owned_pct:.0f}%
                </span><br>
                <span class="game-meta">Complete</span>
            </div>
        </div>
        <div style="margin-top: 10px; background: #171a21; border-radius: 4px; height: 8px;">
            <div style="background: {color}; width: {owned_pct}%; height: 100%; border-radius: 4px;"></div>
        </div>
    </div>
    """
    
    return html

def create_metric_card(title, value, subtitle=None, color="#66c0f4"):
    """Create a styled metric card"""
    subtitle_html = f"<p class='game-meta'>{subtitle}</p>" if subtitle else ""
    
    html = f"""
    <div class="stats-container" style="text-align: center;">
        <h3 style="color: {color} !important; margin-bottom: 10px;">{title}</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: {color};">
            {value}
        </div>
        {subtitle_html}
    </div>
    """
    
    return html

def get_user_list():
    """Get list of all users for selection"""
    mappings = load_mappings()
    if mappings:
        return list(mappings['user_to_idx'].keys())
    return []

def search_users(query, user_list, max_results=50):
    """Search users by ID"""
    if not query:
        return user_list[:max_results]
    
    query_lower = query.lower()
    matching = [u for u in user_list if query_lower in str(u).lower()]
    return matching[:max_results]
