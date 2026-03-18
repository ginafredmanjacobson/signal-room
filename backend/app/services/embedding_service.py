from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Simple in-memory vectorizer (fine for MVP)
vectorizer = TfidfVectorizer(max_features=512)

def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Lightweight embedding using TF-IDF.
    Returns numpy array of vectors.
    """
    return vectorizer.fit_transform(texts).toarray()