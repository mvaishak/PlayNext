import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify
import torch
from pathlib import Path

class NextGameRecommender:
    def __init__(
        self,
        train_matrix=None,
        similarity_matrix=None,
        popularity_scores=None,
        alpha=0.7,
        device=None,
        densify_similarity_auto_cap_bytes=1_000_000_000,
    ):
        self.train_matrix = train_matrix
        self.similarity_matrix = similarity_matrix
        self.popularity_scores = popularity_scores
        self.alpha = alpha
        self.n_items = len(popularity_scores) if popularity_scores is not None else 0

    def recommend(self, user_idx, k=10, exclude_owned=True):
        # placeholder — actual logic comes from the pickled object
        return []

# 2. Paths
MODEL_PATH = Path("trained_models.pkl")
MAPPING_PATH = Path("mappings.pkl")

if not MODEL_PATH.exists():
    raise FileNotFoundError("trained_models.pkl not found")

if not MAPPING_PATH.exists():
    raise FileNotFoundError("mappings.pkl not found")

# 3. Load MODEL (FORCE CPU, SAFE)
print("Loading trained_models.pkl on CPU...")

try:
    models = torch.load(
        MODEL_PATH,
        map_location=torch.device("cpu"),
        weights_only=False,   # REQUIRED so full objects load
    )
    print("Models loaded successfully on CPU")
except Exception as e:
    print("torch.load failed:", e)
    raise RuntimeError(
        "trained_models.pkl could not be loaded. "
        "This file contains full CUDA tensors and MUST be loaded using torch.load, "
        "with the class definitions present."
    )

# 4. Load MAPPINGS (safe pickle)
with open(MAPPING_PATH, "rb") as f:
    mappings = pickle.load(f)

print("✓ Loaded mappings")

idx_to_item = mappings["idx_to_item"]
item_to_idx = mappings["item_to_idx"]
idx_to_user = mappings["idx_to_user"]

# 5. Extract recommender models
recommender_bundle = models["recommender_bundle"]
recommender_copurchase = models["recommender_copurchase"]
recommender_combined = models["recommender_combined"]

# Flask App
app = Flask(__name__)

# For autocomplete list
all_game_ids = [idx_to_item[i] for i in sorted(idx_to_item.keys())]

# Helper: SteamDB Image URL
def steamdb_image(game_id):
    return f"https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/header.jpg"


# ROUTES
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/games")
def games_list():
    return jsonify(all_game_ids)


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    owned_games = data.get("owned_games", [])

    # Convert IDs → item indices
    owned_indices = [item_to_idx[g] for g in owned_games if g in item_to_idx]

    # Synthetic user index (you can improve later)
    synthetic_user = 0

    # Get recommendations
    rec_bundle = recommender_bundle.recommend(synthetic_user, k=12)
    rec_copurchase = recommender_copurchase.recommend(synthetic_user, k=12)
    rec_combined = recommender_combined.recommend(synthetic_user, k=12)

    def convert(rec_list):
        results = []
        for idx, score in rec_list:
            game_id = idx_to_item[idx]
            results.append({
                "game_id": game_id,
                "score": float(score),
                "image": steamdb_image(game_id)
            })
        return results

    return jsonify({
        "bundle": convert(rec_bundle),
        "copurchase": convert(rec_copurchase),
        "combined": convert(rec_combined),
    })

# Run server
if __name__ == "__main__":
    app.run(debug=True)
