import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess(features: dict) -> np.ndarray:
    values = list(features.values())
    X = np.array([values], dtype=float)
    scaler = StandardScaler()
    return scaler.fit_transform(X)