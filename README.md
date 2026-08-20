# FastAPI Backend — Telco Customer Churn Project

The ML model is now fully decoupled from the Streamlit UI. `api.py` is a
standalone prediction **service** — it owns the model, the scaler, and all
inference logic. Streamlit (and anything else — a web app, mobile app, CRM,
notebook, curl) talks to it only over HTTP. Neither Streamlit page imports
`pickle` or `sklearn`, or touches the `.pkl` file, anymore.

```
┌─────────────────┐        HTTP / JSON        ┌──────────────────────┐
│  Streamlit UI    │  ───────────────────────▶ │  FastAPI service      │
│  prediction.py    │                           │  (api.py)              │
│  Model_Performance │ ◀─────────────────────── │  model + scaler live   │
│  .py               │                           │  only here             │
└─────────────────┘                            └──────────────────────┘
                                                          ▲
                                        also usable by: web apps,
                                        mobile apps, CRM systems, scripts
```

## Files

| File | Purpose |
|---|---|
| `api.py` | The prediction **service**. Loads the model once at startup; owns all encoding, scaling, and inference. Exposes prediction + full model-performance endpoints. This is the only file that imports `sklearn` or opens the `.pkl`. |
| `api_client.py` | Small `requests`-based client (`ChurnAPIClient`). The *only* way either Streamlit page talks to the model. |
| `prediction.py` | Rewritten as a pure API client — collects form input, POSTs it to `/api/v1/predict`, renders the response. No model/scaler/pickle access. |
| `Model_Performance.py` | Rewritten as a pure API client — pulls metrics, ROC curve, feature importance, and the classification report from the API instead of computing them locally. |
| `requirements.txt` | Adds `fastapi`, `uvicorn`, `pydantic`, `requests` to the existing dependencies. |

`app.py` (routing) is unchanged.

## Install

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn api:app --reload --port 8000
```

Interactive docs: `http://127.0.0.1:8000/docs`

## Run the Streamlit app (in a second terminal)

```bash
streamlit run app.py
```

The **API must be running** before you open the Prediction or Model
Performance pages — they no longer fall back to loading the model
in-process. If the API isn't reachable, each page shows a clear error with
the command to start it, instead of silently failing.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Basic info / links |
| GET | `/api/v1/health` | Liveness + whether the model loaded |
| GET | `/api/v1/model-info` | Algorithm, feature list, classes |
| POST | `/api/v1/predict` | Single customer → churn prediction |
| POST | `/api/v1/predict/batch` | List of customers → list of predictions |
| GET | `/api/v1/metrics` | Accuracy / precision / recall / F1 / ROC-AUC / confusion matrix / ROC curve points, all on the held-out test set |
| GET | `/api/v1/feature-importance` | Absolute logistic-regression coefficients, sorted, per feature |
| GET | `/api/v1/classification-report` | Full sklearn classification report (per-class precision/recall/F1/support) |

### Example request

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "total_charges": 845.5
  }'
```

### Example response

```json
{
  "churn_prediction": 1,
  "churn_label": "Churn",
  "churn_probability": 0.7771,
  "risk_level": "High",
  "recommendation": [
    "Immediate retention campaign",
    "Special discount",
    "Dedicated relationship manager",
    "Priority customer support"
  ]
}
```

## Validation

All categorical fields are enums (e.g. `gender` only accepts `"Female"` /
`"Male"`), so bad values return a `422` with a clear error instead of a
silent bad prediction. Numeric fields (`tenure`, `monthly_charges`,
`total_charges`, `senior_citizen`) are range-checked too.

## Consuming it from something other than Streamlit

Because prediction logic now lives only behind REST endpoints, any client
can use it the same way `api_client.py` does — a web frontend, a mobile app,
or a CRM's backend job can `POST /api/v1/predict` directly with a JSON body
and never need Python, sklearn, or the pickle file at all. See the `curl`
example above, or `api_client.py` for a minimal Python reference client.

## Notes

- The encoding used inside `api.py` (`_encode_customer`) is copied 1:1 from
  the ordinal mapping originally in `prediction.py`, since that's how the
  bundled model was actually trained — not the `label_encoder` /
  `onehot_encoder` objects also present in the pickle (those aren't applied
  at inference time either).
- `/api/v1/metrics`, `/api/v1/feature-importance`, and
  `/api/v1/classification-report` need `x_test` / `y_test` (and, for
  feature importance, `coef_`) to be present in the pickle. They are, in the
  uploaded file. If you retrain and repackage without them, those endpoints
  return a 404 with an explanatory message instead of crashing.
- CORS is wide open (`allow_origins=["*"]`) for local development. Restrict
  this before deploying anywhere public.
- Both Streamlit pages now hard-require the API — there's no local-model
  fallback. This is intentional: it's the only way to guarantee the UI
  never touches the model directly.
