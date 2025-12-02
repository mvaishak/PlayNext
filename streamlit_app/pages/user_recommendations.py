"""
User Recommendations page - Search users and view personalized recommendations
"""

import streamlit as st
from utils import (
    load_precomputed_recommendations,
    load_mappings,
    get_user_list,
    search_users,
    format_game_card,
    format_bundle_info
)

def show():
    st.title("👤 User Recommendations")
    
    st.markdown("""
    <div class="info-box">
        <p>Search for a user to see personalized game recommendations across all three tasks.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    recommendations = load_precomputed_recommendations()
    mappings = load_mappings()
    
    if not recommendations or not mappings:
        st.error("Could not load recommendations. Please run the pre-computation script first.")
        return
    
    # Create user lookup dictionary
    user_recs_dict = {rec['user_id']: rec for rec in recommendations}
    
    # User selection
    st.markdown("## 🔍 Select a User")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Get user list
        user_list = list(user_recs_dict.keys())
        
        # Search box
        search_query = st.text_input(
            "Search by User ID",
            placeholder="Enter user ID...",
            help="Search for a specific user"
        )
        
        if search_query:
            matching_users = search_users(search_query, user_list)
            if matching_users:
                selected_user = st.selectbox(
                    "Select from matching users",
                    matching_users,
                    format_func=lambda x: f"User: {x}"
                )
            else:
                st.warning("No matching users found")
                selected_user = None
        else:
            # Show first 100 users
            selected_user = st.selectbox(
                "Or select from list (first 100 users)",
                user_list[:100],
                format_func=lambda x: f"User: {x}"
            )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        total_users = len(user_list)
        st.metric("Total Users", f"{total_users:,}")
    
    if not selected_user or selected_user not in user_recs_dict:
        st.info("Please select a user to see recommendations")
        return
    
    # Get user recommendations
    user_data = user_recs_dict[selected_user]
    
    st.markdown("---")
    
    # User Info
    st.markdown(f"## 🎮 Recommendations for User: `{selected_user}`")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Games Owned", f"{user_data['owned_games_count']:,}")
    
    with col2:
        st.metric("Partial Bundles", f"{user_data.get('partial_bundles_count', 0)}")
    
    with col3:
        st.metric("Recommendations", f"{len(user_data['next_game_recommendations'])}")
    
    # Show owned games sample
    with st.expander("📚 View Owned Games (Sample)"):
        owned_games = user_data.get('owned_games_sample', [])
        if owned_games:
            st.markdown(", ".join([f"`{game}`" for game in owned_games[:20]]))
        else:
            st.info("No owned games data available")
    
    st.markdown("---")
    
    # Task 1: Next-Game Recommendations
    st.markdown("### 🎯 Task 1: Next-Game Purchase Predictions")
    
    st.markdown("""
    <div class="info-box">
        <p>These are the top games the user is likely to purchase next, based on:</p>
        <ul>
            <li>Similar users' purchase patterns</li>
            <li>Bundle relationships</li>
            <li>Game popularity</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Number of recommendations to show
    col1, col2 = st.columns([3, 1])
    
    with col1:
        show_images = st.checkbox("Show game images", value=True, help="Display Steam store images for games")
    
    with col2:
        num_recs = st.select_slider(
            "Number of recommendations",
            options=[5, 10, 15, 20],
            value=10
        )
    
    next_game_recs = user_data.get('next_game_recommendations', [])[:num_recs]
    
    if next_game_recs:
        # Display in columns
        cols_per_row = 2 if show_images else 3
        
        for i in range(0, len(next_game_recs), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(next_game_recs):
                    rec = next_game_recs[idx]
                    with col:
                        format_game_card(rec, rank=idx+1, show_image=show_images)
    else:
        st.info("No next-game recommendations available for this user")
    
    st.markdown("---")
    
    # Task 2: Bundle Completion
    st.markdown("### 📦 Task 2: Bundle Completion Recommendations")
    
    st.markdown("""
    <div class="info-box">
        <p>Complete your partially owned bundles! These games are from bundles you've already started collecting.</p>
    </div>
    """, unsafe_allow_html=True)
    
    bundle_recs = user_data.get('bundle_completion_recommendations', [])
    partial_bundles = user_data.get('top_partial_bundles', [])
    
    if bundle_recs:
        # Show partial bundles info
        if partial_bundles:
            st.markdown("#### 📊 Your Partial Bundles")
            
            for bundle in partial_bundles[:5]:
                st.markdown(format_bundle_info(bundle), unsafe_allow_html=True)
        
        st.markdown("#### 🎁 Recommended Games to Complete Bundles")
        
        # Show bundle completion recommendations
        for i in range(0, min(10, len(bundle_recs)), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(bundle_recs):
                    rec = bundle_recs[idx]
                    with col:
                        format_game_card(rec, rank=idx+1, show_image=show_images)
    else:
        st.info("No partial bundles found for this user. They may own complete bundles or no bundles at all.")
    
    st.markdown("---")
    
    # Download recommendations
    st.markdown("### 💾 Export Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download as JSON", use_container_width=True):
            import json
            json_str = json.dumps(user_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"recommendations_{selected_user}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📋 Copy User ID", use_container_width=True):
            st.code(selected_user, language=None)
