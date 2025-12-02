"""
Recommendation model classes for Steam Game Recommender System.

This module contains the three main recommender classes:
- NextGameRecommender: Predicts next game purchases
- BundleCompletionRecommender: Recommends games from partially owned bundles
- CrossBundleRecommender: Discovers similar bundles

These classes match the exact implementation from complete_steam_recommender.ipynb
"""

import numpy as np
from scipy.sparse import csr_matrix
from collections import defaultdict
import torch


class NextGameRecommender:
    """
    Hybrid recommender for predicting next-game purchases.
    Combines collaborative filtering, bundle-enhanced similarity, and popularity.
    
    Best parameters (from tuning):
    - alpha=0.7 (70% similarity weight, 30% popularity weight)
    - similarity_matrix=game_similarity_combined
    """
    
    def __init__(self, train_matrix, similarity_matrix, popularity_scores, alpha=0.7,
                 device=None, densify_similarity_auto_cap_bytes=1_000_000_000):
        self.train_matrix = train_matrix
        self.similarity_matrix = similarity_matrix
        self.alpha = alpha
        
        # Set device (GPU if available)
        self.device = torch.device(device) if device is not None else (
            torch.device("mps") if torch.backends.mps.is_available() else
            torch.device("cuda") if torch.cuda.is_available() else
            torch.device("cpu")
        )
        
        # Move popularity scores to GPU
        pop = torch.as_tensor(popularity_scores, dtype=torch.float32)
        self.popularity_t = pop.flatten().to(self.device)
        self.n_items = int(self.popularity_t.numel())
        
        # Try to keep similarity matrix on GPU if feasible
        self.similarity_t = None
        if torch.is_tensor(similarity_matrix):
            self.similarity_t = similarity_matrix.to(self.device, dtype=torch.float32)
        elif isinstance(similarity_matrix, np.ndarray):
            self.similarity_t = torch.from_numpy(similarity_matrix).to(self.device, dtype=torch.float32)
        else:
            # Sparse matrix - densify only if small enough
            shape = getattr(similarity_matrix, "shape", None)
            if shape is not None and len(shape) == 2 and shape[0] == shape[1]:
                est_bytes = int(shape[0]) * int(shape[1]) * 4  # float32
                if self.device.type != "cpu" and est_bytes <= densify_similarity_auto_cap_bytes:
                    dense = similarity_matrix.toarray() if hasattr(similarity_matrix, "toarray") else np.asarray(similarity_matrix)
                    self.similarity_t = torch.from_numpy(dense).to(self.device, dtype=torch.float32)
    
    def recommend(self, user_idx, k=10, exclude_owned=True):
        """
        Generate top-K recommendations for a user.
        
        Args:
            user_idx: User index
            k: Number of recommendations
            exclude_owned: Whether to exclude already owned items
            
        Returns:
            List of (item_idx, score) tuples
        """
        k = int(min(k, self.n_items))
        
        # Get user's owned items
        user_items = self.train_matrix[user_idx].nonzero()[1]
        
        # Cold start: return popular items
        if len(user_items) == 0:
            top_vals, top_idx = torch.topk(self.popularity_t, k)
            return [(int(i), float(v)) for i, v in zip(top_idx.tolist(), top_vals.tolist())]
        
        # Compute similarity scores
        if self.similarity_t is not None:
            # GPU-accelerated similarity computation
            user_items_t = torch.tensor(user_items, device=self.device, dtype=torch.long)
            scores_t = self.similarity_t.index_select(0, user_items_t).sum(dim=0)
            scores_t = scores_t / float(len(user_items))
        else:
            # CPU sparse computation
            user_profile = self.train_matrix[user_idx].copy()
            user_profile.data = np.ones_like(user_profile.data)  # Binarize
            
            cpu_scores = user_profile.dot(self.similarity_matrix)
            if hasattr(cpu_scores, "toarray"):
                scores_np = cpu_scores.toarray().ravel()
            else:
                scores_np = np.asarray(cpu_scores).ravel()
            
            scores_np = scores_np / float(len(user_items))
            scores_t = torch.from_numpy(scores_np).to(self.device, dtype=torch.float32)
        
        # Combine with popularity (on GPU)
        combined_scores_t = self.alpha * scores_t + (1 - self.alpha) * self.popularity_t
        
        # Exclude already owned items
        if exclude_owned:
            user_items_t = torch.tensor(user_items, device=self.device, dtype=torch.long)
            combined_scores_t.index_fill_(0, user_items_t, float("-inf"))
        
        # Get top-K on GPU
        top_vals, top_idx = torch.topk(combined_scores_t, k)
        
        return [(int(i), float(v)) for i, v in zip(top_idx.tolist(), top_vals.tolist())]


class BundleCompletionRecommender:
    """
    Recommends games to complete partially owned bundles.
    
    Key insight: Partial bundle ownership is a strong purchase signal.
    Users who own 2/5 games in a bundle are likely to purchase the remaining 3.
    """
    
    def __init__(self, user_item_matrix, bundle_game_matrix, idx_to_item, item_to_idx):
        self.user_item_matrix = user_item_matrix
        self.bundle_game_matrix = bundle_game_matrix
        self.idx_to_item = idx_to_item
        self.item_to_idx = item_to_idx
    
    def get_partial_bundles(self, user_idx):
        """
        Find bundles that user partially owns.
        
        Returns:
            List of dicts with bundle info and ownership ratios
        """
        user_games = set(self.user_item_matrix[user_idx].nonzero()[1])
        user_game_ids = {self.idx_to_item[idx] for idx in user_games}
        
        partial_bundles = []
        n_bundles = self.bundle_game_matrix.shape[0]
        
        for bundle_idx in range(n_bundles):
            bundle_game_indices = self.bundle_game_matrix[bundle_idx].nonzero()[1]
            bundle_game_ids = {self.idx_to_item[idx] for idx in bundle_game_indices}
            
            if not bundle_game_ids:
                continue
            
            owned = user_game_ids & bundle_game_ids
            missing = bundle_game_ids - user_game_ids
            
            ownership_ratio = len(owned) / len(bundle_game_ids)
            
            # Only consider partial ownership (not 0% or 100%)
            if 0 < ownership_ratio < 1:
                missing_indices = [self.item_to_idx[gid] for gid in missing if gid in self.item_to_idx]
                partial_bundles.append({
                    'bundle_idx': bundle_idx,
                    'ownership_ratio': ownership_ratio,
                    'owned_count': len(owned),
                    'missing_count': len(missing),
                    'missing_games': missing,
                    'missing_indices': missing_indices
                })
        
        return sorted(partial_bundles, key=lambda x: x['ownership_ratio'], reverse=True)
    
    def recommend(self, user_idx, k=10, min_ownership=0.3):
        """
        Recommend games from partially owned bundles.
        
        Args:
            user_idx: User index
            k: Number of recommendations
            min_ownership: Minimum ownership ratio to consider (default 30%)
            
        Returns:
            List of (item_idx, confidence_score) tuples
        """
        partial_bundles = self.get_partial_bundles(user_idx)
        
        # Score missing games by bundle ownership ratio
        game_scores = defaultdict(float)
        
        for bundle in partial_bundles:
            if bundle['ownership_ratio'] >= min_ownership:
                score = bundle['ownership_ratio']
                for item_idx in bundle['missing_indices']:
                    game_scores[item_idx] = max(game_scores[item_idx], score)
        
        # Sort by score and return top-K
        recommendations = sorted(game_scores.items(), key=lambda x: x[1], reverse=True)[:k]
        
        return recommendations


class CrossBundleRecommender:
    """
    Discovers similar bundles based on bundle-bundle similarity.
    
    Uses cosine similarity of bundle game compositions.
    """
    
    def __init__(self, bundle_similarity_matrix, idx_to_bundle):
        self.bundle_similarity_matrix = bundle_similarity_matrix
        self.idx_to_bundle = idx_to_bundle
    
    def recommend(self, bundle_idx, k=5, min_similarity=0.1):
        """
        Recommend similar bundles.
        
        Args:
            bundle_idx: Source bundle index
            k: Number of recommendations
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of dicts with bundle info and similarity scores
        """
        # Get similarities for this bundle
        similarities = self.bundle_similarity_matrix[bundle_idx].copy()
        similarities[bundle_idx] = 0  # Exclude self
        
        # Filter by minimum similarity
        valid_indices = np.where(similarities >= min_similarity)[0]
        valid_similarities = similarities[valid_indices]
        
        # Sort and get top-K
        top_k_indices = valid_indices[np.argsort(-valid_similarities)][:k]
        
        recommendations = []
        for idx in top_k_indices:
            recommendations.append({
                'bundle_idx': int(idx),
                'bundle_id': self.idx_to_bundle.get(int(idx)),
                'similarity': float(similarities[idx])
            })
        
        return recommendations
