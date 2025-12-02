import pickle
import torch

PATH = "trained_models.pkl"

try:
    obj = torch.load(PATH, map_location="cpu", weights_only=False)
    print("✓ File loaded successfully — NOT corrupted.")
except Exception as e:
    print("✗ File failed to load. Error:")
    print(e)
