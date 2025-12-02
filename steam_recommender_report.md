# Steam Bundle-Aware Recommender System: Comprehensive Analysis

## 1. Problem Statement

Steam offers thousands of games, many of which are sold in bundles. Traditional recommender systems often ignore bundle relationships, missing opportunities to suggest games that help users complete bundles or discover related content. The goal of this project is to build and rigorously evaluate a recommender system that leverages bundle information to improve next-game prediction, bundle completion, and cross-bundle discovery.

## 2. Data & Features

- **User-Item Matrix:** Sparse matrix of user-game interactions.
- **Bundle-Game Matrix:** Mapping of bundles to their constituent games.
- **Game Similarity Matrices:** Computed from bundle co-occurrence and copurchase data.
- **Popularity Scores:** Frequency of game purchases.
- **Mappings:** User, item, and bundle indices for efficient computation.

## 3. Models Implemented

### 3.1 NextGameRecommender (Hybrid)
- Combines bundle-based similarity and popularity scores.
- Tunable alpha parameter balances the two signals.
- GPU-accelerated for scalability.

### 3.2 BundleCompletionRecommender
- Identifies partially owned bundles for each user.
- Recommends games that help complete these bundles.

### 3.3 CrossBundleRecommender
- Suggests similar bundles based on content overlap and similarity scores.

### 3.4 Baseline Models
- **Random:** Recommends random games not owned by the user.
- **Popularity:** Recommends most popular games, excluding owned ones.

## 4. Evaluation Methodology

### 4.1 Metrics
- **Precision@K:** Fraction of recommended games that are relevant.
- **Recall@K:** Fraction of relevant games that are recommended.
- **Hit Rate@K:** Probability that at least one relevant game is recommended.
- **NDCG@K:** Measures ranking quality, rewarding higher placement of relevant items.
- **Bundle Precision:** For bundle completion, fraction of recommendations that help complete a bundle.
- **Similarity, Diversity, User Overlap:** For cross-bundle recommendations.
- **Confidence Intervals:** 95% CIs for all metrics to ensure statistical robustness.

### 4.2 Experimental Design
- **Alpha Tuning:** Multiple alpha values tested to find optimal hybridization.
- **Baseline Comparison:** Hybrid model compared against random and popularity baselines.
- **Task-Specific Evaluation:** Bundle completion and cross-bundle discovery evaluated with custom metrics.
- **Visualization:** Results plotted for interpretability.
- **Reproducibility:** All results saved to JSON; code is GPU-ready and well-documented.

## 5. Key Findings

- **Hybrid recommender (bundle + popularity) significantly outperforms baselines.**
- **BundleCompletionRecommender achieves high bundle precision, proving bundle-awareness.**
- **CrossBundleRecommender provides relevant and diverse bundle suggestions.**
- **Statistical rigor (confidence intervals, NDCG) ensures credible claims.**


---

**In summary:**
This project demonstrates the value of bundle-aware recommendation on Steam, with robust evaluation and clear improvements over traditional baselines. The methodology and results are reproducible and ready for further research or deployment.
