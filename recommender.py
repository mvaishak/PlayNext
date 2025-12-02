# recommender.py
import os
import numpy as np
import pandas as pd
import json
import pickle
import logging

logger = logging.getLogger(__name__)

class NextGameRecommender:
    def __init__(self, game_index, similarity_matrices: dict, config: dict):
        """
        game_index: dict mapping game_id (string) -> integer index in similarity matrices
        similarity_matrices: dict name -> np.ndarray (N x N)
        config: dict for this recommender (contains 'similarity_matrix' and 'alpha')
        """
        self.game_index = {str(k): int(v) for k, v in game_index.items()}
        self.similarity_matrices = similarity_matrices
        self.config = config
        self.alpha = config.get("alpha", 0.7)
        self.sim_name = config.get("similarity_matrix")
        if self.sim_name not in similarity_matrices:
            raise ValueError(f"Similarity matrix {self.sim_name} not found")
        self.sim = similarity_matrices[self.sim_name]
        # normalize similarity rows to avoid scale issues
        row_sums = self.sim.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        self.norm_sim = self.sim / row_sums

    def _owned_vector(self, owned_game_ids):
        """Return binary owned vector (N,) where N is number of games known."""
        N = self.sim.shape[0]
        vec = np.zeros(N, dtype=float)
        for gid in owned_game_ids:
            gid_s = str(gid)
            idx = self.game_index.get(gid_s)
            if idx is None:
                # try numeric conversion fallback
                try:
                    idx = self.game_index.get(int(gid))
                except Exception:
                    idx = None
            if idx is not None and 0 <= idx < N:
                vec[idx] = 1.0
        return vec

    def predict_next_games(self, owned_game_ids, topk=10):
        """
        Score = sum over owned games (similarity_to_candidate * owned_flag) 
        Returns topk candidate game ids with scores (excluding owned).
        """
        vec = self._owned_vector(owned_game_ids)
        if vec.sum() == 0:
            # cold-start fallback: recommend top-degree games
            degrees = self.sim.sum(axis=1)
            order = np.argsort(-degrees)[:topk]
            return [(self._id_from_index(i), float(degrees[i])) for i in order]

        # score each candidate by weighted sum of similarities to owned games
        scores = self.norm_sim.dot(vec)
        # zero out owned
        owned_idx = np.where(vec > 0)[0]
        scores[owned_idx] = -np.inf
        top_idx = np.argsort(-scores)[:topk]
        return [(self._id_from_index(i), float(scores[i])) for i in top_idx]

    def recommend_bundle_completion(self, owned_game_ids, bundle_map: dict, topk=10):
        """
        bundle_map: dict bundle_id -> list of game_ids
        For each bundle that the user partially owns, compute missing games and rank them by score.
        Returns a dict: bundle_id -> list of (game_id, score)
        """
        vec = self._owned_vector(owned_game_ids)
        scores = self.norm_sim.dot(vec)
        results = {}
        for bundle_id, games in bundle_map.items():
            owned = [g for g in games if str(g) in self.game_index and vec[self.game_index[str(g)]] > 0]
            missing = [g for g in games if str(g) in self.game_index and (vec[self.game_index[str(g)]] == 0)]
            if len(owned) > 0 and len(missing) > 0:
                # rank missing by scores
                miss_idx = [self.game_index[str(g)] for g in missing]
                ranked = sorted([(missing[i], float(scores[miss_idx[i]])) for i in range(len(missing))],
                                key=lambda x: -x[1])
                results[bundle_id] = ranked[:topk]
        return results

    def find_cross_bundle_similarities(self, bundle_map: dict, topn=5):
        """
        For each bundle, compute a centroid vector (average of game rows) and find top similar bundles.
        Returns dict bundle_id -> list of (other_bundle_id, similarity_score)
        """
        # construct bundle centroids
        bundle_centroids = {}
        for b, games in bundle_map.items():
            indices = [self.game_index[str(g)] for g in games if str(g) in self.game_index]
            if len(indices) == 0:
                continue
            centroid = self.sim[indices].mean(axis=0)  # average similarity profile
            bundle_centroids[b] = centroid / (np.linalg.norm(centroid) + 1e-9)

        results = {}
        bundle_items = list(bundle_centroids.items())
        for i, (b1, c1) in enumerate(bundle_items):
            sims = []
            for j, (b2, c2) in enumerate(bundle_items):
                if b1 == b2:
                    continue
                sim_score = float(np.dot(c1, c2))
                sims.append((b2, sim_score))
            sims_sorted = sorted(sims, key=lambda x: -x[1])[:topn]
            results[b1] = sims_sorted
        return results

    def _id_from_index(self, idx):
        # convert back to game id (game_index is id -> idx mapping)
        for gid, i in self.game_index.items():
            if i == idx:
                return gid
        return None


# ---------- helpers to load matrices / trained pickle --------------------

def load_similarity_matrix(path_or_name):
    """Loads .npy or csv. Returns numpy array"""
    if not os.path.exists(path_or_name):
        raise FileNotFoundError(path_or_name)
    if path_or_name.endswith(".npy"):
        return np.load(path_or_name)
    else:
        return np.loadtxt(path_or_name, delimiter=",")

def build_game_index_from_csv(csv_path):
    """CSV expected to contain 'game_id' (string) column"""
    df = pd.read_csv(csv_path, dtype={"game_id": str})
    game_index = {str(g): i for i, g in enumerate(df["game_id"].tolist())}
    return game_index, df

def load_trained_pickle(pkl_path):
    """
    Attempt to load a trained model pickle and extract:
      - similarity_matrices (dict of name -> np.ndarray)
      - game_index (mapping game_id -> index)
      - games_df (pd.DataFrame with columns game_id,name,steam_appid) if available
      - bundle_map (dict)
    Returns a dict: {'similarity_matrices':..., 'game_index':..., 'games_df':..., 'bundle_map':...}
    """
    if not os.path.exists(pkl_path):
        raise FileNotFoundError(pkl_path)

    logger.warning("Loading pickle: ensure this file is from a trusted source. Unpickling arbitrary files can execute code.")
    with open(pkl_path, "rb") as f:
        obj = pickle.load(f)

    result = {
        "similarity_matrices": {},
        "game_index": None,
        "games_df": None,
        "bundle_map": {}
    }

    # If the pickle is already a dict with expected keys, use them
    if isinstance(obj, dict):
        # similarity_matrices may be nested
        if "similarity_matrices" in obj and isinstance(obj["similarity_matrices"], dict):
            result["similarity_matrices"].update(obj["similarity_matrices"])
        # also allow direct named arrays in the dict
        for k, v in obj.items():
            if isinstance(v, np.ndarray) and ("similarity" in k or "game_similarity" in k):
                result["similarity_matrices"][k] = v
        # game_index may be present
        if "game_index" in obj and isinstance(obj["game_index"], dict):
            result["game_index"] = {str(k): int(v) for k, v in obj["game_index"].items()}
        # games dataframe or list
        if "games_df" in obj and isinstance(obj["games_df"], (pd.DataFrame,)):
            result["games_df"] = obj["games_df"]
        elif "games" in obj:
            # try to coerce list-of-dicts to df
            try:
                result["games_df"] = pd.DataFrame(obj["games"])
            except Exception:
                pass
        # bundles
        if "bundle_map" in obj and isinstance(obj["bundle_map"], dict):
            result["bundle_map"] = obj["bundle_map"]
        elif "bundles" in obj and isinstance(obj["bundles"], dict):
            result["bundle_map"] = obj["bundles"]

    # If similarity matrices still empty, try to discover keys in the pickle
    if len(result["similarity_matrices"]) == 0:
        # search for numpy arrays on top-level attributes if obj is an object with __dict__
        if not isinstance(obj, dict):
            # inspect attributes
            for attr in dir(obj):
                if attr.startswith("_"):
                    continue
                try:
                    val = getattr(obj, attr)
                    if isinstance(val, np.ndarray) and val.ndim == 2 and val.shape[0] == val.shape[1]:
                        result["similarity_matrices"][attr] = val
                except Exception:
                    continue
        else:
            # dict but no named similarity found - maybe keys like 'game_similarity_bundle.npy' with string path?
            pass

    # If no game_index provided but we have games_df, build index from it
    if result["game_index"] is None and result["games_df"] is not None:
        df = result["games_df"]
        if "game_id" in df.columns:
            result["game_index"] = {str(g): i for i, g in enumerate(df["game_id"].astype(str).tolist())}

    # If still missing game_index but similarity matrices exist, assume 0..N-1 and create synthetic game ids "0","1",...
    if result["game_index"] is None and len(result["similarity_matrices"]) > 0:
        # pick one matrix to infer N
        any_mat = next(iter(result["similarity_matrices"].values()))
        n = any_mat.shape[0]
        result["game_index"] = {str(i): i for i in range(n)}
        # also synthesize a games_df with those ids
        try:
            result["games_df"] = pd.DataFrame([{"game_id": str(i), "name": f"Game {i}", "steam_appid": ""} for i in range(n)])
        except Exception:
            pass

    # Final: ensure all matrices are numpy arrays and have consistent shape with game_index
    n_expected = len(result["game_index"])
    cleaned = {}
    for name, mat in result["similarity_matrices"].items():
        if isinstance(mat, (list, tuple)):
            mat = np.asarray(mat)
        if isinstance(mat, np.ndarray) and mat.ndim == 2 and mat.shape[0] == mat.shape[1] == n_expected:
            cleaned[name] = mat
        else:
            logger.warning(f"Ignoring similarity matrix '{name}' due to incompatible shape {getattr(mat,'shape',None)} expected {n_expected}x{n_expected}")
    result["similarity_matrices"] = cleaned

    return result
