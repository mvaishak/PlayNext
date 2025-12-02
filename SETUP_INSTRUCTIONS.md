# Setup Instructions

This repository contains the Steam Game Recommendation System code. Due to GitHub file size limits, large model files and data matrices are excluded from the repository.

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mvaishak/PlayNext.git
cd PlayNext
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

For Mac GPU support (Apple Silicon):
```bash
pip install --upgrade torch torchvision torchaudio
```

### 3. Generate Required Files

**Important**: Before running the Streamlit app, you need to generate the model files by running the complete notebook.

```bash
# Run the complete recommendation notebook
jupyter notebook complete_steam_recommender.ipynb
```

Execute all cells in the notebook. This will:
- Process the raw data
- Generate feature matrices in `features/`
- Train models and save them in `model_outputs/`
- Create evaluation results

**Expected files to be generated:**
```
features/
├── user_item_matrix.npz           (User-item interactions)
├── bundle_game_matrix.npz         (Bundle-game mappings)
├── game_similarity_*.npz          (Item similarity matrices)
└── interactions.csv               (Processed interactions)

model_outputs/
├── trained_models.pkl             (Trained recommendation models)
├── train_matrix.npz               (Training data split)
├── test_set.csv                   (Test data)
└── comprehensive_results.json     (Evaluation metrics)
```

## Running the Streamlit App

### Option 1: Without Pre-computation (Faster startup)

```bash
cd streamlit_app
streamlit run app.py
```

The app will load models and generate recommendations on-demand.

### Option 2: With Pre-computation (Better performance)

```bash
# Pre-compute recommendations for 1000 users
cd streamlit_app
python precompute_recommendations.py

# Then run the app
streamlit run app.py
```

Pre-computing recommendations:
- Takes 5-10 minutes
- Generates `model_outputs/all_user_recommendations.json`
- Improves app performance significantly
- You can adjust the number of users in `precompute_recommendations.py`

## File Size Information

The following files are excluded from git (see `.gitignore`) due to size:

- `data/steam_reviews.json.gz` (~1.3 GB)
- `Archive.zip` (~903 MB)
- `features/game_similarity_*.npz` (~484 MB, ~466 MB)
- `model_outputs/trained_models.pkl` (~112 MB)
- Large sparse matrices and similarity matrices

These files will be regenerated when you run the notebook.

## Quick Start Guide

For detailed instructions on using the Streamlit app, see [STREAMLIT_QUICKSTART.md](STREAMLIT_QUICKSTART.md).

For deployment instructions, see [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md).

## Troubleshooting

### "Model files not found" error

Make sure you've run `complete_steam_recommender.ipynb` first to generate the model files.

### "No module named 'torch'" error

Install PyTorch:
```bash
pip install torch torchvision torchaudio
```

### Mac GPU support not working

For Apple Silicon Macs, ensure you have the latest PyTorch:
```bash
pip install --upgrade torch torchvision torchaudio
```

### Slow recommendation generation

Run the pre-computation script to cache recommendations:
```bash
cd streamlit_app
python precompute_recommendations.py
```

## Data Requirements

This project expects the following data files in the `data/` directory:
- `australian_users_items.json.gz`
- `bundle_data.json.gz`
- `steam_reviews.json.gz`

If you don't have these files, please contact the project maintainer.

---

**Note**: This is an academic project for CSE258R Recommender Systems & Web Mining.
