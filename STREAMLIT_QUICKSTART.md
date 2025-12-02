# PlayNext Streamlit App - Quick Start Guide

## 🎮 What You've Built

A complete Steam-themed web application with:
- **Home Dashboard** - Performance metrics and visualizations
- **User Recommendations** - Search users and view personalized recommendations
- **Model Explorer** - Compare models and understand methodology  
- **About Page** - Technical details and documentation

## 🚀 How to Run the App

### Step 1: Pre-compute Recommendations (One-time setup)

Navigate to the streamlit_app directory and run:

```bash
cd streamlit_app
python precompute_recommendations.py
```

This will:
- Load your trained models from `model_outputs/trained_models.pkl`
- Generate recommendations for users (default: first 1000 users)
- Save to `model_outputs/all_user_recommendations.json`

**Expected output:**
```
PRE-COMPUTING RECOMMENDATIONS FOR ALL USERS
✓ Models loaded successfully
✓ Mappings loaded successfully  
✓ Generated recommendations for 1000 users
✓ Saved successfully!
File size: ~15 MB
```

**Adjust settings** in `precompute_recommendations.py`:
- `MAX_USERS = 1000` - Increase for more users (watch file size!)
- `K_RECOMMENDATIONS = 20` - Number of recommendations per user

### Step 2: Install Streamlit Dependencies

```bash
pip install streamlit plotly
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Streamlit App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📁 File Structure

```
streamlit_app/
├── app.py                          # Main app with Steam theme
├── utils.py                        # Helper functions (caching, Steam images)
├── precompute_recommendations.py   # Pre-compute script
├── requirements.txt                # Dependencies
├── .streamlit/
│   └── config.toml                 # Steam theme colors
└── pages/
    ├── home.py                     # Dashboard
    ├── user_recommendations.py     # User search
    ├── model_explorer.py           # Model comparison
    └── about.py                    # Documentation
```

## 🎨 Features

### Home Page
- **Performance Metrics**: Hit Rate, Precision, Recall, NDCG
- **Interactive Charts**: Plotly visualizations
- **Dataset Stats**: Users, games, bundles, interactions
- **Task Overview**: Description of all three recommendation tasks

### User Recommendations Page
- **User Search**: Search by user ID
- **Next-Game Predictions**: Top-K game recommendations with Steam images
- **Bundle Completion**: Games from partially owned bundles
- **Owned Games**: View user's game library
- **Export**: Download recommendations as JSON

### Model Explorer Page
- **Task Comparison**: Compare all three recommendation tasks
- **Performance Metrics**: Detailed evaluation results
- **Model Configuration**: Alpha, similarity matrix, GPU acceleration
- **Baseline Comparison**: Random vs Popularity vs Combined
- **Technical Details**: How each model works

### About Page
- **Project Overview**: Hypothesis and approach
- **Dataset Information**: UCSD Steam dataset
- **Methodology**: Feature engineering and evaluation
- **Technical Stack**: Libraries and optimizations
- **Key Results**: Performance highlights
- **Future Work**: Potential improvements

## 🎯 Steam Theme

The app features authentic Steam styling:
- **Colors**: `#1b2838` (dark), `#66c0f4` (blue), `#5cb85c` (green)
- **Game Cards**: Hover effects, Steam images
- **Typography**: Clean, readable fonts
- **Layout**: Responsive, wide columns
- **Images**: Pulled from Steam CDN automatically

## 🖼️ Steam Game Images

Game images are automatically loaded from Steam's CDN using:
```
https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg
```

The app extracts app IDs from game names and provides fallback placeholders.

## ⚡ Performance Tips

1. **Pre-compute recommendations** - Much faster than generating on-the-fly
2. **Limit users** - Start with 1000 users, increase as needed
3. **Caching** - Streamlit caches data/models automatically
4. **File size** - Keep recommendations JSON under 100MB for deployment

## 🚀 Deployment to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add streamlit_app/
   git commit -m "Add Streamlit app"
   git push
   ```

2. **Deploy**:
   - Go to https://streamlit.io/cloud
   - Connect your GitHub repository
   - Point to `streamlit_app/app.py`
   - Deploy!

3. **Important**:
   - Ensure `all_user_recommendations.json` is committed
   - If file is too large, reduce `MAX_USERS` or use Git LFS
   - Models and features must be accessible

## 🛠️ Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#66c0f4"  # Steam blue
backgroundColor = "#1b2838"  # Dark background
textColor = "#c7d5e0"  # Light text
```

### Modify Number of Recommendations

In `pages/user_recommendations.py`, change the slider:
```python
num_recs = st.select_slider(
    "Number of recommendations",
    options=[5, 10, 15, 20, 30],  # Add more options
    value=10
)
```

### Add More Users

Edit `precompute_recommendations.py`:
```python
MAX_USERS = 5000  # Increase this
```

## 🐛 Troubleshooting

### "Models not found"
→ Run `complete_steam_recommender.ipynb` first to train models

### "Pre-computed recommendations not found"  
→ Run `python precompute_recommendations.py`

### "ModuleNotFoundError: No module named 'streamlit'"
→ Install dependencies: `pip install -r requirements.txt`

### Game images not showing
→ Normal! Not all games have images. Fallback placeholders are shown.

### App is slow
→ Pre-compute more recommendations, ensure caching is working

## 📊 Expected Performance

- **Load time**: ~2-3 seconds
- **User search**: Instant (cached)
- **Recommendations display**: < 1 second (pre-computed)
- **Page navigation**: Instant
- **Memory usage**: ~500MB-1GB (depending on data size)

## 🎉 You're All Set!

Your Steam Game Recommender web app is ready! The app provides:
- Beautiful Steam-themed UI
- Fast, pre-computed recommendations
- Interactive visualizations
- Complete model documentation
- Easy user search and exploration

Enjoy exploring the recommendations! 🎮

---

**Questions?**
Check the full README.md in the streamlit_app/ directory for more details.
