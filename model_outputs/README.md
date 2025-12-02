# Steam Recommender System - Model Outputs

## Files in this directory:

### Model Configuration
- `model_configs.json` - Configuration parameters for all three NextGameRecommender variants
- `trained_models.pkl` - Serialized model objects (requires features/ directory to reload)

### Evaluation Results (Task 1)
- `task1_evaluation_results.json` - Full evaluation metrics (Precision, Recall, Hit Rate) for K=[5,10,20]
- `task1_results_comparison.csv` - Comparison table of all three approaches

### Training Data
- `train_matrix.npz` - Sparse training matrix (user-item interactions with test data removed)
- `test_set.csv` - Test set user-item pairs
- `train_test_split_info.json` - Statistics about the train/test split

### Sample Outputs
- `sample_recommendations.json` - Example recommendations for 10 random users with their actual purchases

## Model Performance Summary

Evaluate using K=[5, 10, 20] for Precision@K, Recall@K, and Hit Rate@K.

**Best Model**: See task1_results_comparison.csv for detailed comparison.

## How to Load Models

```python
import pickle
from scipy.sparse import load_npz

# Load trained matrix
train_matrix = load_npz('model_outputs/train_matrix.npz')

# Load model objects
with open('model_outputs/trained_models.pkl', 'rb') as f:
    models = pickle.load(f)

recommender = models['recommender_combined']

# Generate recommendations for a user
recommendations = recommender.recommend(user_idx=0, k=10)
```

## Dependencies

Models require:
- Feature matrices from `./features/` directory
- User/item mappings from `./features/mappings.pkl`
- scipy, numpy, pandas
