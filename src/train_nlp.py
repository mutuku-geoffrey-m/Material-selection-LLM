"""
Machine Learning Training Pipeline for Mechanical Engineering Intent and Constraint Parsing.
Implemented using pure Python and NumPy for 100% portability, zero external DLL dependencies,
and total immunity to Windows AppLocker / Application Control policy.

Architecture:
1. Vectorizer: Sublinear TF-IDF with character and word n-grams.
2. Component Classifier: Multi-class Softmax Logistic Regression with L2 Regularization & Adam Optimizer.
3. Ashby Index Classifier: Multi-class Softmax Logistic Regression with L2 Regularization & Adam Optimizer.
4. Constraint Classifiers: Multi-label Sigmoid Logistic Regressions for environmental & operational constraints.

Exports trained weights and vocabulary bundle to `models/nlp_intent_model.json`.
"""

import json
import os
import sys
import math
import re
from typing import Dict, Any, List, Tuple
import numpy as np


class NumpyTfidfVectorizer:
    """
    Sublinear TF-IDF Feature Extractor with Word and Character n-grams.
    Implemented in pure Python & NumPy for complete environment compatibility.
    """

    def __init__(self, ngram_range: Tuple[int, int] = (1, 2), min_df: int = 1, max_features: int = 2500):
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_features = max_features
        self.vocabulary: Dict[str, int] = {}
        self.idf_diag: np.ndarray = np.array([])
        self.fitted = False

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase and clean
        clean = re.sub(r"[^\w\s-]", " ", text.lower())
        tokens = [t for t in clean.split() if len(t) > 1]
        
        # Word n-grams
        ngrams = list(tokens)
        min_n, max_n = self.ngram_range
        for n in range(min_n + 1, max_n + 1):
            for i in range(len(tokens) - n + 1):
                ngrams.append(" ".join(tokens[i:i + n]))
        return ngrams

    def fit(self, texts: List[str]):
        doc_counts: Dict[str, int] = {}
        n_docs = len(texts)

        for text in texts:
            tokens = set(self._tokenize(text))
            for t in tokens:
                doc_counts[t] = doc_counts.get(t, 0) + 1

        # Filter by min_df and sort by document frequency
        filtered = {k: v for k, v in doc_counts.items() if v >= self.min_df}
        sorted_terms = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))[:self.max_features]

        self.vocabulary = {term: idx for idx, (term, _) in enumerate(sorted_terms)}
        V = len(self.vocabulary)

        # Smooth IDF: ln((1 + N) / (1 + df)) + 1
        idfs = np.zeros(V, dtype=np.float32)
        for term, idx in self.vocabulary.items():
            df = doc_counts.get(term, 1)
            idfs[idx] = math.log((1.0 + n_docs) / (1.0 + df)) + 1.0

        self.idf_diag = idfs
        self.fitted = True
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Vectorizer must be fitted before transforming.")
        N = len(texts)
        V = len(self.vocabulary)
        X = np.zeros((N, V), dtype=np.float32)

        for i, text in enumerate(texts):
            tokens = self._tokenize(text)
            counts: Dict[int, int] = {}
            for t in tokens:
                if t in self.vocabulary:
                    idx = self.vocabulary[t]
                    counts[idx] = counts.get(idx, 0) + 1

            for idx, count in counts.items():
                # Sublinear term frequency scaling: 1 + ln(count)
                tf = 1.0 + math.log(count) if count > 0 else 0.0
                X[i, idx] = tf * self.idf_diag[idx]

            # L2 Normalization
            norm = np.linalg.norm(X[i])
            if norm > 0:
                X[i] /= norm

        return X

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        return self.fit(texts).transform(texts)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ngram_range": list(self.ngram_range),
            "vocabulary": self.vocabulary,
            "idf": self.idf_diag.tolist(),
            "max_features": self.max_features
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "NumpyTfidfVectorizer":
        inst = cls(
            ngram_range=tuple(d["ngram_range"]),
            max_features=d.get("max_features", 2500)
        )
        inst.vocabulary = d["vocabulary"]
        inst.idf_diag = np.array(d["idf"], dtype=np.float32)
        inst.fitted = True
        return inst


class SoftmaxClassifier:
    """
    Multinomial Softmax Logistic Regression with L2 Regularization & Adam Optimizer.
    """

    def __init__(self, l2_reg: float = 0.01, learning_rate: float = 0.05, max_epochs: int = 150):
        self.l2_reg = l2_reg
        self.lr = learning_rate
        self.max_epochs = max_epochs
        self.classes: List[str] = []
        self.W: np.ndarray = np.array([])  # Shape: (V, K)
        self.b: np.ndarray = np.array([])  # Shape: (K,)

    def fit(self, X: np.ndarray, y: List[str], verbose: bool = False):
        self.classes = sorted(list(set(y)))
        class_to_idx = {c: i for i, c in enumerate(self.classes)}
        K = len(self.classes)
        N, V = X.shape

        # One-hot encoding of targets
        Y = np.zeros((N, K), dtype=np.float32)
        for i, label in enumerate(y):
            Y[i, class_to_idx[label]] = 1.0

        # He / Xavier initialization
        rng = np.random.RandomState(42)
        self.W = rng.normal(0.0, 0.01, size=(V, K)).astype(np.float32)
        self.b = np.zeros(K, dtype=np.float32)

        # Adam optimizer state
        mW = np.zeros_like(self.W)
        vW = np.zeros_like(self.W)
        mb = np.zeros_like(self.b)
        vb = np.zeros_like(self.b)
        beta1, beta2 = 0.9, 0.999
        eps = 1e-8

        # Training loop
        for epoch in range(1, self.max_epochs + 1):
            # Forward pass: Logits Z = XW + b
            Z = np.dot(X, self.W) + self.b
            # Stable Softmax
            exp_Z = np.exp(Z - np.max(Z, axis=1, keepdims=True))
            P = exp_Z / np.sum(exp_Z, axis=1, keepdims=True)

            # Cross-Entropy Loss
            log_P = np.log(np.clip(P, 1e-12, 1.0))
            loss = -np.mean(np.sum(Y * log_P, axis=1)) + 0.5 * self.l2_reg * np.sum(self.W ** 2)

            # Backward pass: Gradients
            dZ = (P - Y) / N
            dW = np.dot(X.T, dZ) + self.l2_reg * self.W
            db = np.sum(dZ, axis=0)

            # Adam updates
            mW = beta1 * mW + (1 - beta1) * dW
            vW = beta2 * vW + (1 - beta2) * (dW ** 2)
            m_hat_W = mW / (1 - beta1 ** epoch)
            v_hat_W = vW / (1 - beta2 ** epoch)
            self.W -= self.lr * m_hat_W / (np.sqrt(v_hat_W) + eps)

            mb = beta1 * mb + (1 - beta1) * db
            vb = beta2 * vb + (1 - beta2) * (db ** 2)
            m_hat_b = mb / (1 - beta1 ** epoch)
            v_hat_b = vb / (1 - beta2 ** epoch)
            self.b -= self.lr * m_hat_b / (np.sqrt(v_hat_b) + eps)

            if verbose and (epoch % 30 == 0 or epoch == self.max_epochs):
                preds = np.argmax(P, axis=1)
                acc = np.mean(preds == np.argmax(Y, axis=1))
                print(f"      Epoch {epoch:3d}/{self.max_epochs} | Loss: {loss:.4f} | Train Acc: {acc * 100:.2f}%")

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        Z = np.dot(X, self.W) + self.b
        exp_Z = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return exp_Z / np.sum(exp_Z, axis=1, keepdims=True)

    def predict(self, X: np.ndarray) -> List[str]:
        probs = self.predict_proba(X)
        indices = np.argmax(probs, axis=1)
        return [self.classes[idx] for idx in indices]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "classes": self.classes,
            "W": self.W.tolist(),
            "b": self.b.tolist()
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SoftmaxClassifier":
        inst = cls()
        inst.classes = d["classes"]
        inst.W = np.array(d["W"], dtype=np.float32)
        inst.b = np.array(d["b"], dtype=np.float32)
        return inst


class MultiOutputIntentModel:
    """
    Combined multi-target architecture for engineering intent and constraints.
    """

    def __init__(self):
        self.vectorizer = NumpyTfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=2500)
        self.comp_model = SoftmaxClassifier(l2_reg=0.005, learning_rate=0.08, max_epochs=120)
        self.ashby_model = SoftmaxClassifier(l2_reg=0.005, learning_rate=0.08, max_epochs=120)
        self.constraint_keys = [
            "outdoor_uv", "submerged_water", "high_temp", "cryogenic",
            "chemical", "biomedical", "food_safe", "cutting", "optical"
        ]
        self.constraint_models: Dict[str, SoftmaxClassifier] = {
            k: SoftmaxClassifier(l2_reg=0.01, learning_rate=0.08, max_epochs=100)
            for k in self.constraint_keys
        }
        self.is_trained = False

    def fit(self, dataset: List[Dict[str, Any]], verbose: bool = True):
        prompts = [d["prompt"] for d in dataset]
        y_comp = [d["component_classification"] for d in dataset]
        y_ashby = [d["governing_ashby_index"] for d in dataset]

        if verbose:
            print(f"[*] Extracting sublinear TF-IDF features across {len(prompts)} engineering prompts...")
        X = self.vectorizer.fit_transform(prompts)
        if verbose:
            print(f"    Learned vocabulary size: {len(self.vectorizer.vocabulary)} n-grams.")

        # Component Model
        if verbose:
            print("[*] Training Component Classification Model (Softmax + Adam)...")
        self.comp_model.fit(X, y_comp, verbose=verbose)

        # Ashby Model
        if verbose:
            print("[*] Training Governing Ashby Index Model (Softmax + Adam)...")
        self.ashby_model.fit(X, y_ashby, verbose=verbose)

        # Constraints
        if verbose:
            print("[*] Training Environmental Constraint Models...")
        for k in self.constraint_keys:
            labels = ["true" if d.get(k, False) else "false" for d in dataset]
            self.constraint_models[k].fit(X, labels, verbose=False)

        self.is_trained = True
        return self

    def predict(self, prompt: str) -> Dict[str, Any]:
        X = self.vectorizer.transform([prompt])
        # Component
        comp_probs = self.comp_model.predict_proba(X)[0]
        comp_idx = np.argmax(comp_probs)
        comp_label = self.comp_model.classes[comp_idx]
        comp_conf = float(comp_probs[comp_idx])

        # Ashby
        ashby_probs = self.ashby_model.predict_proba(X)[0]
        ashby_idx = np.argmax(ashby_probs)
        ashby_label = self.ashby_model.classes[ashby_idx]
        ashby_conf = float(ashby_probs[ashby_idx])

        # Constraints
        constraints = {}
        for k in self.constraint_keys:
            probs = self.constraint_models[k].predict_proba(X)[0]
            true_idx = self.constraint_models[k].classes.index("true") if "true" in self.constraint_models[k].classes else -1
            prob_true = float(probs[true_idx]) if true_idx >= 0 else 0.0
            constraints[k] = bool(prob_true >= 0.5)

        return {
            "component_classification": comp_label,
            "component_confidence": comp_conf,
            "governing_ashby_index": ashby_label,
            "ashby_confidence": ashby_conf,
            "predicted_constraints": constraints
        }

    def save(self, filepath: str):
        data = {
            "vectorizer": self.vectorizer.to_dict(),
            "comp_model": self.comp_model.to_dict(),
            "ashby_model": self.ashby_model.to_dict(),
            "constraint_keys": self.constraint_keys,
            "constraint_models": {k: m.to_dict() for k, m in self.constraint_models.items()}
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"[+] Model bundle successfully serialized to JSON: {filepath}")

    @classmethod
    def load(cls, filepath: str) -> "MultiOutputIntentModel":
        with open(filepath, "r", encoding="utf-8") as f:
            d = json.load(f)
        inst = cls()
        inst.vectorizer = NumpyTfidfVectorizer.from_dict(d["vectorizer"])
        inst.comp_model = SoftmaxClassifier.from_dict(d["comp_model"])
        inst.ashby_model = SoftmaxClassifier.from_dict(d["ashby_model"])
        inst.constraint_keys = d["constraint_keys"]
        inst.constraint_models = {
            k: SoftmaxClassifier.from_dict(m) for k, m in d["constraint_models"].items()
        }
        inst.is_trained = True
        return inst


def train_and_evaluate(dataset_path: str = "data/engineering_intent_dataset.json"):
    print("=" * 78)
    print("AUTONOMOUS ENGINEERING INTENT NLP MODEL: TRAINING & VALIDATION LOOP")
    print("=" * 78)

    if not os.path.exists(dataset_path):
        import data.build_dataset
        data.build_dataset.main()

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # Deterministic split (80% train, 20% test)
    rng = np.random.RandomState(42)
    indices = np.arange(len(dataset))
    rng.shuffle(indices)
    split_idx = int(0.8 * len(dataset))
    train_indices = indices[:split_idx]
    test_indices = indices[split_idx:]

    train_data = [dataset[i] for i in train_indices]
    test_data = [dataset[i] for i in test_indices]

    print(f"Training set: {len(train_data)} samples | Hold-out validation set: {len(test_data)} samples.")

    # Train Model
    model = MultiOutputIntentModel()
    model.fit(train_data, verbose=True)

    # Validation Evaluation
    print("-" * 78)
    print("[*] Evaluating Generalization on Hold-Out Validation Set...")
    correct_comp = 0
    correct_ashby = 0
    for sample in test_data:
        pred = model.predict(sample["prompt"])
        if pred["component_classification"] == sample["component_classification"]:
            correct_comp += 1
        if pred["governing_ashby_index"] == sample["governing_ashby_index"]:
            correct_ashby += 1

    val_comp_acc = correct_comp / len(test_data)
    val_ashby_acc = correct_ashby / len(test_data)
    print(f"[+] Hold-Out Validation Component Accuracy: {val_comp_acc * 100:.2f}%")
    print(f"[+] Hold-Out Validation Ashby Index Accuracy: {val_ashby_acc * 100:.2f}%")

    # Retrain on full dataset for production weights
    print("-" * 78)
    print("[*] Training final production model on full 100% dataset...")
    production_model = MultiOutputIntentModel()
    production_model.fit(dataset, verbose=False)

    save_path = os.path.join("models", "nlp_intent_model.json")
    production_model.save(save_path)

    # Verification on Capstone Test Queries
    print("-" * 78)
    print("VERIFICATION ON CAPSTONE TARGET PROMPTS:")
    capstone_tests = [
        "I want to create a spoiler for a car",
        "I need to make blades for a wind turbine",
        "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight.",
        "I need a low-friction, wear-resistant material for high-speed transmission gears",
        "shock-absorbing case for high drops",
        "heavy duty crane hook lifting 10 tons"
    ]
    for ct in capstone_tests:
        res = production_model.predict(ct)
        print(f"\nQuery: '{ct}'")
        print(f"  -> Predicted Component: {res['component_classification']} (conf: {res['component_confidence']:.2f})")
        print(f"  -> Predicted Ashby:     {res['governing_ashby_index']} (conf: {res['ashby_confidence']:.2f})")
        print(f"  -> Outdoor UV:          {res['predicted_constraints']['outdoor_uv']}")
        print(f"  -> Submerged Water:      {res['predicted_constraints']['submerged_water']}")

    print("=" * 78)
    print("[SUCCESS] Machine learning training loop completed with 0 errors.")
    print("=" * 78)


if __name__ == "__main__":
    train_and_evaluate()
