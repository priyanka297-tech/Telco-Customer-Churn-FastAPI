"""
Run locally:
    uvicorn api:app --reload --port 8000

Docs:
    http://127.0.0.1:8000/docs   (Swagger UI)
    http://127.0.0.1:8000/redoc  (ReDoc)
"""

from contextlib import asynccontextmanager
from enum import Enum
from typing import List

import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    auc,
    classification_report,
)

MODEL_PATH = "models/Telco_customer_churn_model_and_preprocessors.pkl"

# ---------------------------------------------------------------------------
# Encoding maps — must stay identical to the ones used in prediction.py,
# since that is how the model was trained (ordinal-style manual encoding).
# ---------------------------------------------------------------------------

BINARY_MAP = {"Female": 0, "Male": 1, "No": 0, "Yes": 1}
MULTIPLE_MAP = {"No": 0, "Yes": 1, "No phone service": 2}
INTERNET_MAP = {"DSL": 0, "Fiber optic": 1, "No": 2}
SERVICE_MAP = {"No": 0, "Yes": 1, "No internet service": 2}
CONTRACT_MAP = {"Month-to-month": 0, "One year": 1, "Two year": 2}
PAYMENT_MAP = {
    "Electronic check": 0,
    "Mailed check": 1,
    "Bank transfer (automatic)": 2,
    "Credit card (automatic)": 3,
}


# ---------------------------------------------------------------------------
# Enums — used both for validation and to auto-populate the Swagger UI
# with the exact allowed values (mirrors the selectboxes in prediction.py).
# ---------------------------------------------------------------------------

class GenderEnum(str, Enum):
    female = "Female"
    male = "Male"


class YesNoEnum(str, Enum):
    yes = "Yes"
    no = "No"


class MultipleLinesEnum(str, Enum):
    no = "No"
    yes = "Yes"
    no_phone_service = "No phone service"


class InternetServiceEnum(str, Enum):
    dsl = "DSL"
    fiber = "Fiber optic"
    no = "No"


class ServiceEnum(str, Enum):
    no = "No"
    yes = "Yes"
    no_internet_service = "No internet service"


class ContractEnum(str, Enum):
    month_to_month = "Month-to-month"
    one_year = "One year"
    two_year = "Two year"


class PaymentMethodEnum(str, Enum):
    electronic_check = "Electronic check"
    mailed_check = "Mailed check"
    bank_transfer = "Bank transfer (automatic)"
    credit_card = "Credit card (automatic)"


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class CustomerData(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gender": "Female",
                "senior_citizen": 0,
                "partner": "Yes",
                "dependents": "No",
                "tenure": 12,
                "phone_service": "Yes",
                "multiple_lines": "No",
                "internet_service": "Fiber optic",
                "online_security": "No",
                "online_backup": "Yes",
                "device_protection": "No",
                "tech_support": "No",
                "streaming_tv": "Yes",
                "streaming_movies": "No",
                "contract": "Month-to-month",
                "paperless_billing": "Yes",
                "payment_method": "Electronic check",
                "monthly_charges": 70.35,
                "total_charges": 845.5,
            }
        }
    )

    gender: GenderEnum
    senior_citizen: int = Field(..., ge=0, le=1, description="0 = No, 1 = Yes")
    partner: YesNoEnum
    dependents: YesNoEnum
    tenure: int = Field(..., ge=0, le=100, description="Months with the company")
    phone_service: YesNoEnum
    multiple_lines: MultipleLinesEnum
    internet_service: InternetServiceEnum
    online_security: ServiceEnum
    online_backup: ServiceEnum
    device_protection: ServiceEnum
    tech_support: ServiceEnum
    streaming_tv: ServiceEnum
    streaming_movies: ServiceEnum
    contract: ContractEnum
    paperless_billing: YesNoEnum
    payment_method: PaymentMethodEnum
    monthly_charges: float = Field(..., ge=0)
    total_charges: float = Field(..., ge=0)


class PredictionResponse(BaseModel):
    churn_prediction: int
    churn_label: str
    churn_probability: float
    risk_level: str
    recommendation: List[str]


class BatchPredictionRequest(BaseModel):
    customers: List[CustomerData]


class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]


class ModelInfoResponse(BaseModel):
    algorithm: str
    n_features: int
    feature_columns: List[str]
    classes: List[int]
    test_set_size: int


class ROCCurve(BaseModel):
    fpr: List[float]
    tpr: List[float]


class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: List[List[int]]
    roc_curve: ROCCurve


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class FeatureImportanceItem(BaseModel):
    feature: str
    importance: float


class FeatureImportanceResponse(BaseModel):
    items: List[FeatureImportanceItem]


class ClassificationReportResponse(BaseModel):
    report: dict


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

ml_resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load the model + preprocessors once and keep them in memory.
    with open(MODEL_PATH, "rb") as f:
        model_data = pickle.load(f)

    ml_resources["model"] = model_data["model"]
    ml_resources["scaler"] = model_data["scaler"]
    ml_resources["feature_columns"] = model_data["feature_columns"]
    ml_resources["x_test"] = model_data.get("x_test")
    ml_resources["y_test"] = model_data.get("y_test")

    yield

    ml_resources.clear()


app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="Serves churn predictions and model performance metrics "
    "for the Telco Customer Churn Dashboard project.",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the Streamlit app (or any other frontend) to call this API from
# a different origin/port during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _encode_customer(data: CustomerData) -> pd.DataFrame:
    """Convert a validated CustomerData object into the exact numeric
    row shape the model was trained on (same encoding as prediction.py)."""

    row = {
        "gender": BINARY_MAP[data.gender.value],
        "SeniorCitizen": data.senior_citizen,
        "Partner": BINARY_MAP[data.partner.value],
        "Dependents": BINARY_MAP[data.dependents.value],
        "tenure": data.tenure,
        "PhoneService": BINARY_MAP[data.phone_service.value],
        "MultipleLines": MULTIPLE_MAP[data.multiple_lines.value],
        "InternetService": INTERNET_MAP[data.internet_service.value],
        "OnlineSecurity": SERVICE_MAP[data.online_security.value],
        "OnlineBackup": SERVICE_MAP[data.online_backup.value],
        "DeviceProtection": SERVICE_MAP[data.device_protection.value],
        "TechSupport": SERVICE_MAP[data.tech_support.value],
        "StreamingTV": SERVICE_MAP[data.streaming_tv.value],
        "StreamingMovies": SERVICE_MAP[data.streaming_movies.value],
        "Contract": CONTRACT_MAP[data.contract.value],
        "PaperlessBilling": BINARY_MAP[data.paperless_billing.value],
        "PaymentMethod": PAYMENT_MAP[data.payment_method.value],
        "MonthlyCharges": data.monthly_charges,
        "TotalCharges": data.total_charges,
    }

    df = pd.DataFrame([row])
    return df[ml_resources["feature_columns"]]


def _risk_and_recommendation(probability: float):
    if probability < 0.30:
        return "Low", [
            "Continue current plan",
            "Offer loyalty rewards",
            "Regular engagement",
        ]
    elif probability < 0.60:
        return "Medium", [
            "Offer annual contract",
            "Personalized offers",
            "Customer support follow-up",
        ]
    else:
        return "High", [
            "Immediate retention campaign",
            "Special discount",
            "Dedicated relationship manager",
            "Priority customer support",
        ]


def _predict_one(data: CustomerData) -> PredictionResponse:
    model = ml_resources["model"]
    scaler = ml_resources["scaler"]

    df = _encode_customer(data)
    scaled = scaler.transform(df)

    prediction = int(model.predict(scaled)[0])
    probability = float(model.predict_proba(scaled)[0][1])
    risk_level, recommendation = _risk_and_recommendation(probability)

    return PredictionResponse(
        churn_prediction=prediction,
        churn_label="Churn" if prediction == 1 else "No Churn",
        churn_probability=round(probability, 4),
        risk_level=risk_level,
        recommendation=recommendation,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["General"])
def root():
    return {
        "message": "Telco Customer Churn Prediction API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["General"])
def health_check():
    return HealthResponse(
        status="ok",
        model_loaded="model" in ml_resources and ml_resources["model"] is not None,
    )


@app.get("/api/v1/model-info", response_model=ModelInfoResponse, tags=["General"])
def model_info():
    model = ml_resources["model"]
    y_test = ml_resources.get("y_test")
    return ModelInfoResponse(
        algorithm=type(model).__name__,
        n_features=len(ml_resources["feature_columns"]),
        feature_columns=ml_resources["feature_columns"],
        classes=[int(c) for c in model.classes_],
        test_set_size=int(len(y_test)) if y_test is not None else 0,
    )


@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(customer: CustomerData):
    try:
        return _predict_one(customer)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")


@app.post(
    "/api/v1/predict/batch",
    response_model=BatchPredictionResponse,
    tags=["Prediction"],
)
def predict_batch(request: BatchPredictionRequest):
    if not request.customers:
        raise HTTPException(status_code=400, detail="No customers provided.")
    try:
        results = [_predict_one(c) for c in request.customers]
        return BatchPredictionResponse(results=results)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {exc}")


@app.get("/api/v1/metrics", response_model=MetricsResponse, tags=["Model Performance"])
def metrics():
    model = ml_resources["model"]
    x_test = ml_resources.get("x_test")
    y_test = ml_resources.get("y_test")

    if x_test is None or y_test is None:
        raise HTTPException(
            status_code=404,
            detail="No held-out test set was bundled with this model file.",
        )

    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    return MetricsResponse(
        accuracy=round(float(accuracy_score(y_test, y_pred)), 4),
        precision=round(float(precision_score(y_test, y_pred)), 4),
        recall=round(float(recall_score(y_test, y_pred)), 4),
        f1_score=round(float(f1_score(y_test, y_pred)), 4),
        roc_auc=round(float(roc_auc), 4),
        confusion_matrix=confusion_matrix(y_test, y_pred).tolist(),
        roc_curve=ROCCurve(
            fpr=[round(float(x), 4) for x in fpr],
            tpr=[round(float(x), 4) for x in tpr],
        ),
    )


@app.get(
    "/api/v1/feature-importance",
    response_model=FeatureImportanceResponse,
    tags=["Model Performance"],
)
def feature_importance():
    model = ml_resources["model"]
    feature_columns = ml_resources["feature_columns"]

    if not hasattr(model, "coef_"):
        raise HTTPException(
            status_code=404,
            detail="The loaded model does not expose coefficients.",
        )

    importance = np.abs(model.coef_[0])
    items = [
        FeatureImportanceItem(feature=f, importance=round(float(i), 4))
        for f, i in sorted(zip(feature_columns, importance), key=lambda x: -x[1])
    ]
    return FeatureImportanceResponse(items=items)


@app.get(
    "/api/v1/classification-report",
    response_model=ClassificationReportResponse,
    tags=["Model Performance"],
)
def classification_report_endpoint():
    model = ml_resources["model"]
    x_test = ml_resources.get("x_test")
    y_test = ml_resources.get("y_test")

    if x_test is None or y_test is None:
        raise HTTPException(
            status_code=404,
            detail="No held-out test set was bundled with this model file.",
        )

    y_pred = model.predict(x_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    return ClassificationReportResponse(report=report)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
