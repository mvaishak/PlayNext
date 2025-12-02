"""
Model Explorer page - Compare models and understand methodology
"""

import streamlit as st
import plotly.graph_objects as go
from utils import load_comprehensive_results, load_evaluation_results

def show():
    st.title("🔬 Model Explorer")
    
    st.markdown("""
    <div class="info-box">
        <p>Explore the three recommendation models, compare their performance, and understand how they work.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection tabs
    tab1, tab2, tab3 = st.tabs([
        "🎯 Task 1: Next-Game Prediction",
        "📦 Task 2: Bundle Completion",
        "🔍 Task 3: Cross-Bundle Discovery"
    ])
    
    # Load evaluation results
    eval_results = load_evaluation_results()
    comprehensive_results = load_comprehensive_results()
    
    if not eval_results:
        st.error("Could not load evaluation results")
        return
    
    # Task 1
    with tab1:
        st.markdown("### Next-Game Purchase Prediction")
        
        st.markdown("""
        <div class="stats-container">
            <h4>How it works:</h4>
            <ol style="color: #c7d5e0;">
                <li><strong>Collaborative Filtering</strong>: Find users with similar game libraries</li>
                <li><strong>Bundle-Enhanced Similarity</strong>: Games from the same bundle are more similar</li>
                <li><strong>Co-Purchase Patterns</strong>: Games frequently bought together</li>
                <li><strong>Popularity Baseline</strong>: Cold-start handling with popular games</li>
                <li><strong>Hybrid Scoring</strong>: α * similarity + (1-α) * popularity</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Performance Metrics")
        
        task1 = eval_results['task1_next_game_prediction']
        
        # Create comparison table
        import pandas as pd
        
        metrics_data = []
        for k in ['5', '10', '20']:
            metrics_data.append({
                'K': k,
                'Precision': f"{task1[k]['precision']['mean']:.2%} ± {task1[k]['precision']['ci']:.2%}",
                'Recall': f"{task1[k]['recall']['mean']:.2%} ± {task1[k]['recall']['ci']:.2%}",
                'Hit Rate': f"{task1[k]['hit_rate']['mean']:.2%} ± {task1[k]['hit_rate']['ci']:.2%}",
                'NDCG': f"{task1[k]['ndcg']['mean']:.4f} ± {task1[k]['ndcg']['ci']:.4f}"
            })
        
        df = pd.DataFrame(metrics_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Model parameters
        st.markdown("#### ⚙️ Model Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <strong>Alpha Parameter</strong><br>
                <span style="color: #66c0f4; font-size: 1.5rem;">0.7</span><br>
                <span class="game-meta">70% similarity, 30% popularity</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <strong>Similarity Matrix</strong><br>
                <span style="color: #66c0f4;">Combined</span><br>
                <span class="game-meta">60% bundle + 40% co-purchase</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
                <strong>GPU Accelerated</strong><br>
                <span style="color: #5cb85c;">✓ Yes</span><br>
                <span class="game-meta">PyTorch MPS/CUDA</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Baseline comparison
        if comprehensive_results and 'task1_results' in comprehensive_results:
            st.markdown("#### 📈 Baseline Comparison")
            
            task1_results = comprehensive_results['task1_results']
            
            # Create comparison chart
            models = []
            hr_at_10 = []
            
            for model_name, results in task1_results.items():
                if '10' in results:
                    models.append(model_name)
                    hr_at_10.append(results['10']['hit_rate']['mean'])
            
            fig = go.Figure()
            colors = ['#ff6b2c', '#66c0f4', '#5cb85c']
            
            for i, (model, hr) in enumerate(zip(models, hr_at_10)):
                fig.add_trace(go.Bar(
                    x=[model],
                    y=[hr],
                    name=model,
                    marker_color=colors[i % len(colors)],
                    text=[f"{hr:.1%}"],
                    textposition='outside',
                    showlegend=False
                ))
            
            fig.update_layout(
                title="Hit Rate@10 Comparison",
                yaxis_title="Hit Rate",
                yaxis_tickformat='.0%',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#c7d5e0'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Task 2
    with tab2:
        st.markdown("### Bundle Completion")
        
        st.markdown("""
        <div class="stats-container">
            <h4>How it works:</h4>
            <ol style="color: #c7d5e0;">
                <li><strong>Detect Partial Bundles</strong>: Find bundles where user owns some but not all games</li>
                <li><strong>Calculate Ownership Ratio</strong>: owned_games / total_bundle_games</li>
                <li><strong>Prioritize High Ownership</strong>: Bundles with >50% ownership get higher scores</li>
                <li><strong>Recommend Missing Games</strong>: Suggest games from high-ownership bundles</li>
                <li><strong>Confidence Scoring</strong>: Score = ownership_ratio</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Performance Metrics")
        
        if 'task2_bundle_completion' in eval_results:
            task2 = eval_results['task2_bundle_completion']
            
            metrics_data = []
            for k in ['5', '10', '20']:
                if k in task2:
                    metrics_data.append({
                        'K': k,
                        'Hit Rate': f"{task2[k]['hit_rate']['mean']:.2%} ± {task2[k]['hit_rate']['ci']:.2%}",
                        'Bundle Precision': f"{task2[k]['bundle_precision']['mean']:.2%} ± {task2[k]['bundle_precision']['ci']:.2%}",
                    })
            
            if metrics_data:
                df = pd.DataFrame(metrics_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("#### 💡 Key Insight")
        
        st.markdown("""
        <div class="info-box">
            <p><strong>Partial bundle ownership is a strong purchase signal!</strong></p>
            <p>Users who own 3 out of 5 games in a bundle are highly likely to purchase the remaining 2 games.</p>
            <p>This model leverages this behavior to make confident recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Task 3
    with tab3:
        st.markdown("### Cross-Bundle Discovery")
        
        st.markdown("""
        <div class="stats-container">
            <h4>How it works:</h4>
            <ol style="color: #c7d5e0;">
                <li><strong>Bundle-Bundle Similarity</strong>: Compute cosine similarity of bundle compositions</li>
                <li><strong>Shared Games Analysis</strong>: Bundles with overlapping games are similar</li>
                <li><strong>User Overlap</strong>: Bundles purchased by similar users</li>
                <li><strong>Content Filtering</strong>: Theme and genre-based recommendations</li>
                <li><strong>Cross-Promotion</strong>: "Users who liked Bundle A also liked Bundle B"</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 💡 Use Cases")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h4>🛍️ Marketing</h4>
                <p>Cross-promote similar bundles to increase sales</p>
                <ul style="color: #c7d5e0;">
                    <li>Bundle discovery</li>
                    <li>Themed collections</li>
                    <li>Franchise bundles</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h4>🎯 Personalization</h4>
                <p>Help users find bundles matching their interests</p>
                <ul style="color: #c7d5e0;">
                    <li>Genre preferences</li>
                    <li>Similar gameplay</li>
                    <li>Developer/publisher</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Technical Details
    st.markdown("---")
    st.markdown("## 🔧 Technical Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="stats-container">
            <h4>Data Structures</h4>
            <ul style="color: #c7d5e0;">
                <li><strong>Sparse Matrices</strong>: Efficient storage for user-item interactions</li>
                <li><strong>CSR Format</strong>: Fast row-based operations</li>
                <li><strong>GPU Tensors</strong>: Accelerated similarity computations</li>
                <li><strong>Similarity Matrices</strong>: Pre-computed item-item similarities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-container">
            <h4>Performance Optimizations</h4>
            <ul style="color: #c7d5e0;">
                <li><strong>GPU Acceleration</strong>: PyTorch MPS/CUDA</li>
                <li><strong>Batch Processing</strong>: Vectorized operations</li>
                <li><strong>Pre-computation</strong>: Similarity matrices cached</li>
                <li><strong>Efficient Indexing</strong>: Fast user/item lookups</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
