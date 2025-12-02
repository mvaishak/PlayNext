"""
Pre-compute recommendations for all users to speed up the Streamlit app.
Run this script after training the models in complete_steam_recommender.ipynb
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from scipy.sparse import load_npz
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 70)
print("PRE-COMPUTING RECOMMENDATIONS FOR ALL USERS")
print("=" * 70)

# Load trained models
print("\nLoading trained models...")
try:
    with open("../model_outputs/trained_models.pkl", "rb") as f:
        models = pickle.load(f)
    next_game_recommender = models['next_game_recommender']
    bundle_completion_recommender = models['bundle_completion_recommender']
    print("✓ Models loaded successfully")
except FileNotFoundError:
    print("✗ Error: Trained models not found. Please run complete_steam_recommender.ipynb first.")
    sys.exit(1)

# Load mappings
print("Loading mappings...")
try:
    with open("../features/mappings.pkl", "rb") as f:
        mappings = pickle.load(f)
    user_to_idx = mappings['user_to_idx']
    idx_to_user = mappings['idx_to_user']
    item_to_idx = mappings['item_to_idx']
    idx_to_item = mappings['idx_to_item']
    print("✓ Mappings loaded successfully")
except FileNotFoundError:
    print("✗ Error: Mappings not found.")
    sys.exit(1)

# Load train matrix
print("Loading train matrix...")
try:
    train_matrix = load_npz("../model_outputs/train_matrix.npz")
    print(f"✓ Train matrix loaded: {train_matrix.shape}")
except FileNotFoundError:
    print("✗ Error: Train matrix not found.")
    sys.exit(1)

# Configuration
MAX_USERS = 1000  # Limit for demo purposes (adjust as needed)
K_RECOMMENDATIONS = 20  # Number of recommendations per user

print(f"\nConfiguration:")
print(f"  Max users to process: {MAX_USERS}")
print(f"  Recommendations per user: {K_RECOMMENDATIONS}")

# Select users to process
all_users = list(user_to_idx.keys())
users_to_process = all_users[:MAX_USERS]

print(f"\nProcessing {len(users_to_process)} users...")

# Generate recommendations for each user
all_recommendations = []

for i, user_id in enumerate(users_to_process):
    if i % 100 == 0:
        print(f"  Progress: {i}/{len(users_to_process)} users...")
    
    user_idx = user_to_idx[user_id]
    
    # Get user info
    owned_items = train_matrix[user_idx].nonzero()[1]
    owned_game_ids = [idx_to_item[idx] for idx in owned_items[:10]]  # Sample
    
    user_data = {
        'user_idx': int(user_idx),
        'user_id': user_id,
        'owned_games_count': len(owned_items),
        'owned_games_sample': owned_game_ids,
    }
    
    # Task 1: Next-game recommendations
    try:
        task1_recs = next_game_recommender.recommend(user_idx, k=K_RECOMMENDATIONS)
        user_data['next_game_recommendations'] = [
            {'item_idx': int(item_idx), 'item_id': idx_to_item[item_idx], 'score': float(score)}
            for item_idx, score in task1_recs
        ]
    except Exception as e:
        print(f"  Warning: Error generating next-game recommendations for user {user_id}: {e}")
        user_data['next_game_recommendations'] = []
    
    # Task 2: Bundle completion recommendations
    try:
        partial_bundles = bundle_completion_recommender.get_partial_bundles(user_idx)
        user_data['partial_bundles_count'] = len(partial_bundles)
        
        if partial_bundles:
            task2_recs = bundle_completion_recommender.recommend(user_idx, k=K_RECOMMENDATIONS, min_ownership=0.3)
            user_data['bundle_completion_recommendations'] = [
                {'item_idx': int(item_idx), 'item_id': idx_to_item[item_idx], 'confidence': float(score)}
                for item_idx, score in task2_recs
            ]
            user_data['top_partial_bundles'] = [
                {
                    'bundle_idx': bundle['bundle_idx'],
                    'ownership_ratio': bundle['ownership_ratio'],
                    'owned_count': bundle['owned_count'],
                    'missing_count': bundle['missing_count']
                }
                for bundle in partial_bundles[:3]
            ]
        else:
            user_data['bundle_completion_recommendations'] = []
            user_data['top_partial_bundles'] = []
    except Exception as e:
        print(f"  Warning: Error generating bundle recommendations for user {user_id}: {e}")
        user_data['bundle_completion_recommendations'] = []
        user_data['top_partial_bundles'] = []
        user_data['partial_bundles_count'] = 0
    
    all_recommendations.append(user_data)

print(f"\n✓ Generated recommendations for {len(all_recommendations)} users")

# Save to JSON
output_path = "../model_outputs/all_user_recommendations.json"
print(f"\nSaving to {output_path}...")

try:
    with open(output_path, "w") as f:
        json.dump(all_recommendations, f, indent=2)
    print(f"✓ Saved successfully!")
    
    # Check file size
    file_size = Path(output_path).stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    print(f"  File size: {file_size_mb:.2f} MB")
    
    if file_size_mb > 100:
        print(f"  ⚠️  Warning: File is large ({file_size_mb:.2f} MB). Consider reducing MAX_USERS.")
    
except Exception as e:
    print(f"✗ Error saving: {e}")
    sys.exit(1)

# Create summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total users processed: {len(all_recommendations)}")
print(f"Average recommendations per user: {K_RECOMMENDATIONS}")
print(f"Users with bundle recommendations: {sum(1 for u in all_recommendations if u['bundle_completion_recommendations'])}")
print(f"Output file: {output_path}")
print(f"File size: {file_size_mb:.2f} MB")
print("\n✓ Pre-computation complete! You can now run the Streamlit app.")
print("=" * 70)
