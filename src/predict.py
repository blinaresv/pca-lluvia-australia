"""
predict.py
Funciones de predicción usando el pipeline PCA + Regresión Logística.
"""

import numpy as np
import joblib
from pathlib import Path


# Ruta base de los modelos (relativa a la raíz del proyecto)
MODELS_DIR = Path(__file__).resolve().parent.parent / 'models'


def load_pipeline(models_dir: Path = MODELS_DIR) -> tuple:
    """
    Carga los artefactos serializados del pipeline.

    Returns
    -------
    (scaler, pca, classifier, feature_ranges, feature_names)
    """
    scaler         = joblib.load(models_dir / 'scaler.pkl')
    pca            = joblib.load(models_dir / 'pca.pkl')
    classifier     = joblib.load(models_dir / 'classifier.pkl')
    feature_ranges = joblib.load(models_dir / 'feature_ranges.pkl')
    feature_names  = joblib.load(models_dir / 'feature_names.pkl')
    return scaler, pca, classifier, feature_ranges, feature_names


def predict(input_array: np.ndarray, scaler, pca, classifier) -> dict:
    """
    Ejecuta el pipeline completo sobre un array de entrada.

    Parameters
    ----------
    input_array : np.ndarray  forma (1, n_features) SIN estandarizar
    scaler      : StandardScaler entrenado
    pca         : PCA entrenado
    classifier  : LogisticRegression entrenado

    Returns
    -------
    dict con:
        - 'label'            : str ('Sin lluvia' | 'Lluvia')
        - 'class'            : int (0 | 1)
        - 'probability'      : float (probabilidad de la clase predicha)
        - 'prob_no_rain'     : float
        - 'prob_rain'        : float
        - 'pca_components'   : int (número de componentes utilizados)
        - 'variance_explained': float (% varianza explicada)
    """
    # 1. Estandarizar
    X_scaled = scaler.transform(input_array)

    # 2. Reducción PCA
    X_pca = pca.transform(X_scaled)

    # 3. Predicción
    prediction    = int(classifier.predict(X_pca)[0])
    probabilities = classifier.predict_proba(X_pca)[0]

    label = 'Lluvia' if prediction == 1 else 'Sin lluvia'
    prob  = float(probabilities[prediction])

    return {
        'label':              label,
        'class':              prediction,
        'probability':        prob,
        'prob_no_rain':       float(probabilities[0]),
        'prob_rain':          float(probabilities[1]),
        'pca_components':     int(pca.n_components_),
        'variance_explained': float(sum(pca.explained_variance_ratio_) * 100),
    }
