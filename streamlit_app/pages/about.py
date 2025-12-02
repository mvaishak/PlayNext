"""
About page - Technical details and methodology
"""

import streamlit as st

def show():
    st.title("📊 About PlayNext")
    
    st.markdown("""
    <div class="info-box">
        <h3>Steam Game Recommendation System</h3>
        <p>An intelligent recommendation engine powered by bundle relationships and collaborative filtering.</p>
        <p><strong>Course:</strong> CSE258R - Recommender Systems & Web Mining</p>
        <p><strong>Dataset:</strong> UCSD Steam Dataset</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Overview
    st.markdown("## 🎯 Project Overview")
    
    st.markdown("""
    PlayNext is a comprehensive game recommendation system that leverages the unique structure of Steam's bundle ecosystem
    to improve recommendation accuracy. Unlike traditional collaborative filtering approaches, PlayNext recognizes that
    **games sold together in bundles provide stronger recommendation signals** than individual item preferences alone.
    """)
    
    # Key Hypothesis
    st.markdown("""
    <div class="stats-container">
        <h3>💡 Key Hypothesis</h3>
        <p style="font-size: 1.1rem; color: #66c0f4;">
            <strong>Bundle co-occurrence provides stronger signals than individual item preferences alone.</strong>
        </p>
        <p style="color: #c7d5e0;">
            Games that are bundled together often share similar themes, genres, or target audiences.
            By incorporating bundle relationships into the recommendation algorithm, we can make more
            accurate predictions about what games users will enjoy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset Statistics
    st.markdown("## 📚 Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>Source</h4>
            <p><a href="https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data" 
                style="color: #66c0f4;">UCSD Steam Dataset</a></p>
            <p class="game-meta">Collected from Steam's public API</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Scale</h4>
            <ul style="color: #c7d5e0;">
                <li>88,310 users</li>
                <li>32,135 games</li>
                <li>615 bundles</li>
                <li>5.8M+ interactions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Three Tasks
    st.markdown("## 🎯 Three Recommendation Tasks")
    
    st.markdown("""
    <div class="stats-container">
        <h3>Task 1: Next-Game Purchase Prediction</h3>
        <p><strong>Goal:</strong> Predict which games users are likely to purchase next</p>
        <p><strong>Approach:</strong></p>
        <ul style="color: #c7d5e0;">
            <li><strong>Item-based Collaborative Filtering:</strong> Find similar games based on co-purchase patterns</li>
            <li><strong>Bundle-Enhanced Similarity:</strong> Games from the same bundle are weighted as more similar</li>
            <li><strong>Hybrid Scoring:</strong> Combine similarity scores with popularity baseline</li>
            <li><strong>Formula:</strong> score = α × similarity + (1-α) × popularity</li>
        </ul>
        <p><strong>Best Result:</strong> <span class="badge badge-blue">79.5% Hit Rate@10</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-container">
        <h3>Task 2: Bundle Completion</h3>
        <p><strong>Goal:</strong> Recommend missing games from partially owned bundles</p>
        <p><strong>Approach:</strong></p>
        <ul style="color: #c7d5e0;">
            <li><strong>Partial Bundle Detection:</strong> Identify bundles where user owns some but not all games</li>
            <li><strong>Ownership Ratio:</strong> Calculate owned_games / total_bundle_games</li>
            <li><strong>Prioritization:</strong> Recommend from bundles with highest ownership ratios</li>
            <li><strong>Confidence Scoring:</strong> Higher ownership ratio = higher confidence</li>
        </ul>
        <p><strong>Key Insight:</strong> Partial ownership (e.g., 3/5 games) is a strong purchase indicator</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-container">
        <h3>Task 3: Cross-Bundle Discovery</h3>
        <p><strong>Goal:</strong> Find similar bundles for cross-promotion</p>
        <p><strong>Approach:</strong></p>
        <ul style="color: #c7d5e0;">
            <li><strong>Bundle-Bundle Similarity:</strong> Compute cosine similarity of bundle compositions</li>
            <li><strong>Shared Games:</strong> Bundles with overlapping games are similar</li>
            <li><strong>User Overlap:</strong> Measure Jaccard similarity of user bases</li>
            <li><strong>Content Filtering:</strong> Theme and genre-based recommendations</li>
        </ul>
        <p><strong>Use Case:</strong> "Users who liked Action Bundle A also liked Action Bundle B"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Methodology
    st.markdown("## 🔬 Methodology")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>Feature Engineering</h4>
            <ul style="color: #c7d5e0;">
                <li><strong>User-Item Matrix:</strong> Sparse matrix (88K × 32K)</li>
                <li><strong>Bundle-Game Matrix:</strong> Bundle composition</li>
                <li><strong>Game Similarity (Bundle):</strong> Based on bundle co-occurrence</li>
                <li><strong>Game Similarity (Co-purchase):</strong> Based on user co-purchase</li>
                <li><strong>Combined Similarity:</strong> 60% bundle + 40% co-purchase</li>
                <li><strong>Bundle Similarity:</strong> Cosine similarity of bundles</li>
                <li><strong>Popularity Scores:</strong> Purchase frequency normalization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Evaluation</h4>
            <ul style="color: #c7d5e0;">
                <li><strong>Train-Test Split:</strong> 80-20 temporal split per user</li>
                <li><strong>Precision@K:</strong> Fraction of relevant recommendations</li>
                <li><strong>Recall@K:</strong> Fraction of relevant items found</li>
                <li><strong>Hit Rate@K:</strong> At least one relevant item</li>
                <li><strong>NDCG@K:</strong> Ranking quality metric</li>
                <li><strong>Confidence Intervals:</strong> 95% CI for statistical significance</li>
                <li><strong>Baseline Comparison:</strong> Random, Popularity, Combined</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Stack
    st.markdown("## 💻 Technical Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-container">
            <h4>Core Libraries</h4>
            <ul style="color: #c7d5e0;">
                <li>Python 3.8+</li>
                <li>NumPy</li>
                <li>Pandas</li>
                <li>SciPy (Sparse)</li>
                <li>PyTorch</li>
                <li>Scikit-learn</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-container">
            <h4>Visualization</h4>
            <ul style="color: #c7d5e0;">
                <li>Matplotlib</li>
                <li>Seaborn</li>
                <li>Plotly</li>
                <li>Streamlit</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-container">
            <h4>Optimization</h4>
            <ul style="color: #c7d5e0;">
                <li>GPU Acceleration</li>
                <li>PyTorch MPS/CUDA</li>
                <li>Sparse Matrices</li>
                <li>Vectorization</li>
                <li>Caching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Results
    st.markdown("## 🏆 Key Results")
    
    st.markdown("""
    <div class="stats-container">
        <h3>Performance Highlights</h3>
        <ul style="color: #c7d5e0; font-size: 1.1rem;">
            <li><strong>79.5% Hit Rate@10</strong> - Successfully recommends at least one relevant game 
                for 4 out of 5 users</li>
            <li><strong>Significant Improvement Over Baselines</strong> - Outperforms both random and 
                popularity-based approaches</li>
            <li><strong>Bundle-Enhanced > Pure CF</strong> - Bundle relationships provide 15-20% lift 
                over pure collaborative filtering</li>
            <li><strong>GPU Acceleration</strong> - 10-50× speedup on Apple Silicon (MPS) and NVIDIA GPUs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Future Work
    st.markdown("## 🚀 Future Enhancements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>Model Improvements</h4>
            <ul style="color: #c7d5e0;">
                <li>Deep learning embeddings</li>
                <li>Temporal dynamics</li>
                <li>Multi-task learning</li>
                <li>Context-aware recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Features</h4>
            <ul style="color: #c7d5e0;">
                <li>Game metadata (genres, tags)</li>
                <li>User reviews and ratings</li>
                <li>Playtime information</li>
                <li>Social network features</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # References
    st.markdown("## 📖 References")
    
    st.markdown("""
    <div class="info-box">
        <ul style="color: #c7d5e0;">
            <li><strong>Dataset:</strong> UCSD Steam Dataset - 
                <a href="https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data" 
                style="color: #66c0f4;">Link</a></li>
            <li><strong>Course:</strong> CSE258R - Recommender Systems & Web Mining, UC San Diego</li>
            <li><strong>Techniques:</strong> Collaborative Filtering, Content-Based Filtering, 
                Hybrid Methods</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8f98a0;">
        <p>Built with ❤️ using Streamlit</p>
        <p>Fall 2024</p>
    </div>
    """, unsafe_allow_html=True)
