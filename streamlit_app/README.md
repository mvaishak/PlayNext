# PlayNext - Steam Game Recommender Web App

A comprehensive Streamlit web application for exploring game recommendations with a Steam-inspired design.

## 🚀 Quick Start

### 1. Pre-compute Recommendations

First, run the Jupyter notebook to train models:
```bash
jupyter notebook ../complete_steam_recommender.ipynb
```

Then pre-compute recommendations for fast loading:
```bash
python precompute_recommendations.py
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
streamlit_app/
├── app.py                          # Main Streamlit application
├── utils.py                        # Utility functions
├── precompute_recommendations.py   # Pre-compute recommendations
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── pages/
│   ├── __init__.py
│   ├── home.py                     # Home/Dashboard page
│   ├── user_recommendations.py     # User search and recommendations
│   ├── model_explorer.py           # Model comparison and details
│   └── about.py                    # About and technical details
└── README.md                       # This file
```

## 🎯 Features

### 🏠 Home Dashboard
- Overview of model performance metrics
- Dataset statistics
- Interactive visualizations with Plotly
- Quick access to all sections

### 👤 User Recommendations
- Search for users by ID
- View personalized game recommendations
- See bundle completion suggestions
- Display owned games
- Export recommendations as JSON

### 🔬 Model Explorer
- Compare three recommendation tasks
- Understand model architecture
- View baseline comparisons
- Explore technical implementation

### 📊 About
- Project overview and methodology
- Dataset information
- Technical stack details
- Key results and findings

## 🎨 Design

The app features a custom Steam-inspired dark theme with:
- Steam's signature dark blue color scheme (#1b2838, #66c0f4)
- Game cards with hover effects
- Responsive layout
- Steam CDN integration for game images

## 📊 Data Requirements

The app expects the following files in the parent directories:

### Required Files:
- `../model_outputs/trained_models.pkl` - Trained recommendation models
- `../model_outputs/final_evaluation_results.json` - Evaluation metrics
- `../model_outputs/train_matrix.npz` - Training data
- `../features/mappings.pkl` - ID mappings
- `../features/game_popularity.csv` - Game metadata

### Generated Files:
- `../model_outputs/all_user_recommendations.json` - Pre-computed recommendations

## 🛠️ Configuration

### Adjust Pre-computation Settings

Edit `precompute_recommendations.py`:
```python
MAX_USERS = 1000  # Number of users to process
K_RECOMMENDATIONS = 20  # Recommendations per user
```

### Customize Theme

Edit `.streamlit/config.toml` to change colors and fonts.

## 📦 Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Connect to Streamlit Cloud
3. Deploy from your repository

**Note:** Ensure your repository size is under GitHub's limits:
- Pre-computed recommendations file should be < 100MB
- Consider using Git LFS for large files
- Or reduce `MAX_USERS` in pre-computation

### Local Deployment

```bash
streamlit run app.py --server.port 8501
```

## 🔧 Troubleshooting

### Models Not Found
- Run `../complete_steam_recommender.ipynb` first to train models

### No Recommendations Data
- Run `python precompute_recommendations.py`

### Import Errors
- Install all dependencies: `pip install -r requirements.txt`

### Game Images Not Loading
- Images are loaded from Steam CDN using public URLs
- Fallback placeholder images are provided automatically

## 📝 Notes

- The app uses Streamlit's caching for optimal performance
- Game images are fetched from Steam CDN on-demand
- Pre-computed recommendations significantly improve load times
- The app supports thousands of users with efficient data structures

## 🎮 About PlayNext

PlayNext is an intelligent game recommendation system that leverages bundle relationships and collaborative filtering to provide personalized game recommendations. Built as part of CSE258R - Recommender Systems & Web Mining.

**Key Features:**
- 79.5% Hit Rate@10
- Three recommendation tasks
- GPU-accelerated inference
- Bundle-enhanced recommendations

---

**Built with ❤️ using Streamlit**
