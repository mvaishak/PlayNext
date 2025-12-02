"""
Home/Dashboard page - Overview of the recommendation system
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import (
    load_evaluation_results, 
    load_comprehensive_results,
    create_metric_card
)

def show():
    st.title("🎮 PlayNext: Steam Game Recommender System")
    
    st.markdown("""
    <div class="info-box">
        <h3>Welcome to PlayNext!</h3>
        <p>An intelligent game recommendation system powered by bundle relationships and collaborative filtering.</p>
        <p>Explore personalized recommendations, discover new games, and complete your game bundles!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load evaluation results
    eval_results = load_evaluation_results()
    
    if not eval_results:
        st.error("Could not load evaluation results. Please run the notebook first.")
        return
    
    # Key metrics
    st.markdown("## 🏆 Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    task1 = eval_results['task1_next_game_prediction']['10']
    
    with col1:
        st.markdown(
            create_metric_card(
                "Hit Rate@10",
                f"{task1['hit_rate']['mean']:.1%}",
                f"±{task1['hit_rate']['ci']:.2%}",
                "#5cb85c"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "Precision@10",
                f"{task1['precision']['mean']:.2%}",
                f"±{task1['precision']['ci']:.2%}",
                "#66c0f4"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_metric_card(
                "Recall@10",
                f"{task1['recall']['mean']:.2%}",
                f"±{task1['recall']['ci']:.2%}",
                "#ff6b2c"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            create_metric_card(
                "NDCG@10",
                f"{task1['ndcg']['mean']:.3f}",
                "Ranking Quality",
                "#c79c2e"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance across K values
    st.markdown("## 📊 Performance Across Different K Values")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hit Rate chart
        k_values = ['5', '10', '20']
        hit_rates = [
            eval_results['task1_next_game_prediction'][k]['hit_rate']['mean'] 
            for k in k_values
        ]
        hit_rate_cis = [
            eval_results['task1_next_game_prediction'][k]['hit_rate']['ci'] 
            for k in k_values
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=k_values,
            y=hit_rates,
            error_y=dict(type='data', array=hit_rate_cis),
            marker_color='#5cb85c',
            text=[f"{hr:.1%}" for hr in hit_rates],
            textposition='outside',
            hovertemplate='K=%{x}<br>Hit Rate: %{y:.2%}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Hit Rate@K",
            xaxis_title="K (Number of Recommendations)",
            yaxis_title="Hit Rate",
            yaxis_tickformat='.0%',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d5e0'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # NDCG chart
        ndcg_values = [
            eval_results['task1_next_game_prediction'][k]['ndcg']['mean'] 
            for k in k_values
        ]
        ndcg_cis = [
            eval_results['task1_next_game_prediction'][k]['ndcg']['ci'] 
            for k in k_values
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=k_values,
            y=ndcg_values,
            error_y=dict(type='data', array=ndcg_cis),
            marker_color='#c79c2e',
            text=[f"{ndcg:.3f}" for ndcg in ndcg_values],
            textposition='outside',
            hovertemplate='K=%{x}<br>NDCG: %{y:.4f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="NDCG@K",
            xaxis_title="K (Number of Recommendations)",
            yaxis_title="NDCG",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d5e0'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Dataset Information
    st.markdown("## 📚 Dataset Information")
    
    dataset_info = eval_results['dataset_info']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            create_metric_card(
                "Total Users",
                f"{dataset_info['n_users']:,}",
                "Steam Players",
                "#66c0f4"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "Total Games",
                f"{dataset_info['n_items']:,}",
                "Unique Titles",
                "#66c0f4"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_metric_card(
                "Total Bundles",
                f"{dataset_info['n_bundles']:,}",
                "Game Collections",
                "#66c0f4"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            create_metric_card(
                "Training Interactions",
                f"{dataset_info['train_interactions']:,}",
                "User-Game Pairs",
                "#5cb85c"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(
                "Test Interactions",
                f"{dataset_info['test_interactions']:,}",
                "Evaluation Set",
                "#ff6b2c"
            ),
            unsafe_allow_html=True
        )
    
    # Three Tasks Overview
    st.markdown("## 🎯 Three Recommendation Tasks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-container">
            <h3 style="color: #5cb85c !important;">Task 1: Next-Game Prediction</h3>
            <p class="game-meta">Predict which games users are likely to purchase next</p>
            <ul style="color: #c7d5e0; text-align: left;">
                <li>Collaborative Filtering</li>
                <li>Bundle-Enhanced Similarity</li>
                <li>Popularity Baseline</li>
                <li>GPU Accelerated</li>
            </ul>
            <div style="margin-top: 15px;">
                <span class="badge badge-blue">79.5% Hit Rate@10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        task2 = eval_results.get('task2_bundle_completion', {}).get('10', {})
        if task2:
            hr = task2.get('hit_rate', {}).get('mean', 0)
            bp = task2.get('bundle_precision', {}).get('mean', 0)
            
            st.markdown(f"""
            <div class="stats-container">
                <h3 style="color: #66c0f4 !important;">Task 2: Bundle Completion</h3>
                <p class="game-meta">Complete partially owned bundles</p>
                <ul style="color: #c7d5e0; text-align: left;">
                    <li>Partial Bundle Detection</li>
                    <li>Ownership Ratio Analysis</li>
                    <li>Confidence Scoring</li>
                    <li>Bundle-Aware</li>
                </ul>
                <div style="margin-top: 15px;">
                    <span class="badge badge-blue">{hr:.1%} Hit Rate</span>
                    <span class="badge badge-orange">{bp:.1%} Bundle Precision</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="stats-container">
                <h3 style="color: #66c0f4 !important;">Task 2: Bundle Completion</h3>
                <p class="game-meta">Complete partially owned bundles</p>
                <ul style="color: #c7d5e0; text-align: left;">
                    <li>Partial Bundle Detection</li>
                    <li>Ownership Ratio Analysis</li>
                    <li>Confidence Scoring</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-container">
            <h3 style="color: #ff6b2c !important;">Task 3: Cross-Bundle Discovery</h3>
            <p class="game-meta">Find similar bundles for cross-promotion</p>
            <ul style="color: #c7d5e0; text-align: left;">
                <li>Bundle-Bundle Similarity</li>
                <li>Content-Based Filtering</li>
                <li>User Overlap Analysis</li>
                <li>Theme Discovery</li>
            </ul>
            <div style="margin-top: 15px;">
                <span class="badge">Cross-Promotion</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start
    st.markdown("## 🚀 Quick Start")
    
    st.markdown("""
    <div class="info-box">
        <h4>Get Started:</h4>
        <ol style="color: #c7d5e0;">
            <li><strong>User Recommendations</strong> - Search for a user and get personalized game recommendations</li>
            <li><strong>Model Explorer</strong> - Compare different models and understand how they work</li>
            <li><strong>About</strong> - Learn more about the technical details and methodology</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
