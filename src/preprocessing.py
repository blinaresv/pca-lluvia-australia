"""
preprocessing.py
Funciones de carga y preprocesamiento para el dataset Rain in Australia.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# Features utilizadas
NUMERICAL_FEATURES = [
    'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
    'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm',
    'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm',
    'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm'
]
BINARY_FEATURES = ['RainToday']
ALL_FEATURES    = NUMERICAL_FEATURES + BINARY_FEATURES
TARGET          = 'RainTomorrow'


def load_dataset(path: str) -> pd.DataFrame:
    """
    Carga el dataset weatherAUS.csv desde disco.

    Parameters
    ----------
    path : str  ruta al archivo CSV descargado de Kaggle

    Returns
    -------
    pd.DataFrame  crudo
    """
    return pd.read_csv(path)


def preprocess(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Prepara los datos para entrenamiento.

    Pasos:
    1. Eliminar filas sin target.
    2. Codificar RainToday y RainTomorrow como binarias.
    3. Rellenar nulos con la mediana.
    4. Separar X / y.
    5. Train/test split estratificado.
    6. Estandarizar (fit solo en train).

    Returns
    -------
    X_train_s, X_test_s, y_train, y_test, scaler, feature_ranges
    """
    data = df[ALL_FEATURES + [TARGET]].copy()
    data = data.dropna(subset=[TARGET])

    data['RainToday']   = data['RainToday'].map({'Yes': 1, 'No': 0})
    data[TARGET]        = data[TARGET].map({'Yes': 1, 'No': 0})

    for col in NUMERICAL_FEATURES:
        data[col].fillna(data[col].median(), inplace=True)
    data['RainToday'].fillna(0, inplace=True)

    X = data[ALL_FEATURES]
    y = data[TARGET]

    feature_ranges = {
        col: {
            'min':    float(X[col].min()),
            'max':    float(X[col].max()),
            'mean':   float(X[col].mean()),
            'median': float(X[col].median()),
        }
        for col in ALL_FEATURES
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    return X_train_s, X_test_s, y_train, y_test, scaler, feature_ranges


def prepare_single_input(input_dict: dict, scaler: StandardScaler) -> 'np.ndarray':
    """
    Preprocesa una muestra individual para la app.

    Parameters
    ----------
    input_dict : dict  {feature_name: valor, ...}
    scaler     : StandardScaler entrenado

    Returns
    -------
    np.ndarray  forma (1, n_features) estandarizado
    """
    import numpy as np
    row = pd.DataFrame([input_dict], columns=ALL_FEATURES)
    return scaler.transform(row)
