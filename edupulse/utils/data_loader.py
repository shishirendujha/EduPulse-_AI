"""Utility functions for loading configuration and datasets for EduPulse use cases."""
from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd
import yaml

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"


def load_config() -> Dict[str, Any]:
    """Load the full YAML configuration for EduPulse."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("Configuration file is malformed or empty.")

    return config


def get_use_case_params(use_case: str) -> Dict[str, Any]:
    """Return the parameter dictionary for a given use case."""
    config = load_config()
    use_cases = config.get("use_cases", {})

    if use_case not in use_cases:
        raise ValueError(f"Use case '{use_case}' not found in configuration.")

    return dict(use_cases[use_case])


def _resolve_csv_path(csv_path: str) -> Path:
    """Resolve a CSV path relative to the project root when needed."""
    base_dir = CONFIG_PATH.parent.parent
    path = Path(csv_path)
    if not path.is_absolute():
        path = base_dir / path
    return path


def load_dataframe(params: Dict[str, Any]) -> pd.DataFrame:
    """Load a DataFrame based on parameters, applying optional equality filters."""
    if "csv_path" not in params:
        raise ValueError("'csv_path' missing from parameters.")

    csv_path = _resolve_csv_path(params["csv_path"])
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    df = pd.read_csv(csv_path)

    filters = params.get("filters")
    if isinstance(filters, dict):
        for column, value in filters.items():
            if column not in df.columns:
                raise ValueError(f"Filter column '{column}' not found in DataFrame.")
            df = df[df[column] == value]

    return df


def ensure_id_column(df: pd.DataFrame, params: Dict[str, Any], use_case: str) -> pd.DataFrame:
    """Ensure an identifier column exists, creating one when absent."""
    id_column = params.get("id_column")

    if id_column is not None:
        if id_column not in df.columns:
            raise ValueError(
                f"id_column '{id_column}' specified for '{use_case}' but not found in data."
            )
        return df

    if use_case == "dropout":
        new_id = "student_id"
    else:
        new_id = "row_id"

    df = df.copy()
    df[new_id] = df.index.astype(str)
    params["id_column"] = new_id
    return df


def _validate_feature_columns(df: pd.DataFrame, features: Any) -> pd.DataFrame:
    """Validate presence of feature columns and return the subset DataFrame."""
    missing = [col for col in features if col not in df.columns]
    if missing:
        raise ValueError(f"Feature columns missing from DataFrame: {missing}")
    return df[features]


def select_features(df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.Series | None]:
    """Select feature matrix X and optional target y based on parameters."""
    target_column = params.get("target_column")
    id_column = params.get("id_column")

    if params.get("model_type") == "sentiment_nlp":
        label_column = params.get("label_column")
        y = df[label_column] if label_column in df.columns else None
        return df.copy(), y

    features = params.get("features")
    if features:
        X = _validate_feature_columns(df, features)
    else:
        exclude = {col for col in (target_column, id_column) if col}
        X = df[[c for c in df.columns if c not in exclude]]

    if target_column:
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame.")
        y = df[target_column]
    else:
        y = None

    return X, y


def load_prepared_data(use_case: str):
    """Load and prepare data for a given use case."""
    params = get_use_case_params(use_case)
    df = load_dataframe(params)
    df = ensure_id_column(df, params, use_case)

    if use_case == "dropout":
        X, y = select_features(df, params)
        return df, X, y, params

    if use_case == "sentiment":
        return df, params

    # Default: return raw data and params for future extensions
    return df, params
