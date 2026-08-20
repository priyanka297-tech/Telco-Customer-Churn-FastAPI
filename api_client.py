"""
Thin client for the Telco Churn Prediction API.

Used by the Streamlit app (see prediction.py) when API_MODE is enabled,
and reusable from any other script:

    from api_client import ChurnAPIClient
    client = ChurnAPIClient("http://127.0.0.1:8000")
    result = client.predict({...})
"""

import requests


class ChurnAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> dict:
        r = requests.get(f"{self.base_url}/api/v1/health", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def model_info(self) -> dict:
        r = requests.get(f"{self.base_url}/api/v1/model-info", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def metrics(self) -> dict:
        r = requests.get(f"{self.base_url}/api/v1/metrics", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def feature_importance(self) -> dict:
        r = requests.get(
            f"{self.base_url}/api/v1/feature-importance", timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def classification_report(self) -> dict:
        r = requests.get(
            f"{self.base_url}/api/v1/classification-report", timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def predict(self, customer: dict) -> dict:
        r = requests.post(
            f"{self.base_url}/api/v1/predict", json=customer, timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def predict_batch(self, customers: list) -> dict:
        r = requests.post(
            f"{self.base_url}/api/v1/predict/batch",
            json={"customers": customers},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def is_reachable(self) -> bool:
        try:
            self.health()
            return True
        except Exception:
            return False
