# %% [markdown]
# # Model Selection & Training — Evaporation Rate Prediction
# Baseline model, alternative regression models, time-aware cross-validated tuning,
# and a comparison-ready results table for the Evaluation phase.

# %% Imports
import time
import warnings
from pathlib import Path

import joblib
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lightgbm import LGBMRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, RobustScaler
from sklearn.svm import SVR
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")
RANDOM_STATE = 42
OUT = Path(__file__).resolve().parent / "outputs"
(OUT / "models").mkdir(parents=True, exist_ok=True)
TARGET = "Evaporation"

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "/Users/dinuka/Projects/Crop_Prediction_Mahaweli_C_Zone/Dataset/Engineered_Dataset_Full.csv"
# %% Load data
df = pd.read_csv(DATA_PATH, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)
print("Shape:", df.shape, "| Range:", df.Date.min().date(), "->", df.Date.max().date())

# %% Data-validity cleaning (rule-based, physical limits only -> no leakage)
# Values outside physically plausible limits are treated as sensor/entry errors and set to NaN.
# They are imputed (train-set median) INSIDE the pipeline, so nothing leaks from the test set.
rules = {
    "Max_Temperature": lambda s: (s < 22) | (s > 45),
    "S. T. - 10cm Evening": lambda s: (s < 20) | (s > 45),
    "Soil_Mean_Evening": lambda s: (s < 15) | (s > 50),
    "Depression_Mean": lambda s: (s < -10) | (s > 30),
    "Temp_Range": lambda s: s < 0,  # range = max - min cannot be negative
    "VPD_Mean": lambda s: s > 10,
    "Wind_x_VPD": lambda s: s > 100,
    "VPD_mean_7d": lambda s: s > 10,  # contaminated by one corrupted VPD day
}
clean = df.copy()
log = {}
for col, rule in rules.items():
    mask = rule(clean[col])
    log[col] = int(mask.sum())
    clean.loc[mask, col] = np.nan
print("Values flagged as invalid and set to NaN:", log)
clean.to_csv(OUT / "cleaned_dataset.csv", index=False)

# %% Chronological train / test split (no shuffling: avoids look-ahead on a time series)
SPLIT_DATE = "2024-01-01"
train = clean[clean.Date < SPLIT_DATE]
test = clean[clean.Date >= SPLIT_DATE]
features = [c for c in clean.columns if c not in ("Date", TARGET)]
X_train, y_train = train[features], train[TARGET]
X_test, y_test = test[features], test[TARGET]
print(f"Train: {len(train)} rows ({train.Date.min().date()} -> {train.Date.max().date()})")
print(f"Test : {len(test)} rows ({test.Date.min().date()} -> {test.Date.max().date()})")

# Expanding-window CV inside the training period for tuning / model comparison
cv = TimeSeriesSplit(n_splits=5)


# %% Model definitions
def linear_pipe(model):
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", RobustScaler()), ("m", model)])


def tree_pipe(model):
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("m", model)])


poly_pipe = Pipeline(
    [
        ("imp", SimpleImputer(strategy="median")),
        ("sc", RobustScaler()),
        ("poly", PolynomialFeatures(2, include_bias=False)),
        ("sc2", RobustScaler()),
        ("m", Ridge()),
    ]
)

specs = {
    # ---- Reference & baseline ----
    "Mean Predictor (reference)": ("Reference", tree_pipe(DummyRegressor(strategy="mean")), {}),
    "Linear Regression (BASELINE)": ("Baseline", linear_pipe(LinearRegression()), {}),
    # ---- Regularised linear ----
    "Ridge": ("Linear", linear_pipe(Ridge()), {"m__alpha": [0.01, 0.1, 1, 10, 100]}),
    "Lasso": ("Linear", linear_pipe(Lasso(max_iter=20000)), {"m__alpha": [1e-4, 1e-3, 1e-2, 1e-1]}),
    "ElasticNet": (
        "Linear",
        linear_pipe(ElasticNet(max_iter=20000)),
        {"m__alpha": [1e-3, 1e-2, 1e-1], "m__l1_ratio": [0.2, 0.5, 0.8]},
    ),
    "Polynomial(2) + Ridge": ("Non-linear", poly_pipe, {"m__alpha": [10, 100, 1000, 3000]}),
    # ---- Distance / kernel ----
    "KNN": (
        "Non-linear",
        linear_pipe(KNeighborsRegressor()),
        {"m__n_neighbors": [5, 10, 20, 40], "m__weights": ["uniform", "distance"]},
    ),
    "SVR (RBF)": (
        "Non-linear",
        linear_pipe(SVR(kernel="rbf")),
        {"m__C": [1, 3, 10], "m__epsilon": [0.1, 0.3], "m__gamma": ["scale", 0.05]},
    ),
    # ---- Tree ensembles ----
    "Random Forest": (
        "Ensemble",
        tree_pipe(RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)),
        {"m__max_depth": [None, 10, 20], "m__min_samples_leaf": [1, 3, 5], "m__max_features": [0.5, 1.0]},
    ),
    "Extra Trees": (
        "Ensemble",
        tree_pipe(ExtraTreesRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)),
        {"m__max_depth": [None, 15], "m__min_samples_leaf": [1, 3, 5], "m__max_features": [0.5, 1.0]},
    ),
    "Gradient Boosting": (
        "Boosting",
        tree_pipe(GradientBoostingRegressor(subsample=0.8, random_state=RANDOM_STATE)),
        {"m__n_estimators": [200, 400], "m__learning_rate": [0.03, 0.1], "m__max_depth": [2, 3, 4]},
    ),
    "XGBoost": (
        "Boosting",
        tree_pipe(
            XGBRegressor(subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_STATE, n_jobs=-1, verbosity=0)
        ),
        {"m__n_estimators": [300, 600], "m__learning_rate": [0.03, 0.1], "m__max_depth": [3, 5]},
    ),
    "LightGBM": (
        "Boosting",
        tree_pipe(LGBMRegressor(subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                                random_state=RANDOM_STATE, n_jobs=-1, verbose=-1)),
        {"m__n_estimators": [300, 600], "m__learning_rate": [0.03, 0.1], "m__num_leaves": [15, 31]},
    ),
}


# %% Train, tune (time-series CV) and evaluate
def metrics(y, p):
    return {
        "RMSE": float(np.sqrt(mean_squared_error(y, p))),
        "MAE": float(mean_absolute_error(y, p)),
        "R2": float(r2_score(y, p)),
    }


rows, preds, fitted = [], {}, {}
for name, (family, pipe, grid) in specs.items():
    t0 = time.time()
    gs = GridSearchCV(pipe, grid, cv=cv, scoring="neg_root_mean_squared_error", refit=True, n_jobs=1)
    gs.fit(X_train, y_train)
    secs = time.time() - t0
    best = gs.best_estimator_
    p_tr, p_te = best.predict(X_train), best.predict(X_test)
    m_tr, m_te = metrics(y_train, p_tr), metrics(y_test, p_te)
    # CV R2 / MAE for the chosen config (re-run folds cheaply)
    cv_r2, cv_mae = [], []
    for tr_idx, va_idx in cv.split(X_train):
        from sklearn.base import clone

        est = clone(best).fit(X_train.iloc[tr_idx], y_train.iloc[tr_idx])
        pv = est.predict(X_train.iloc[va_idx])
        cv_r2.append(r2_score(y_train.iloc[va_idx], pv))
        cv_mae.append(mean_absolute_error(y_train.iloc[va_idx], pv))
    rows.append(
        {
            "Model": name,
            "Family": family,
            "CV_RMSE": -gs.best_score_,
            "CV_RMSE_std": float(gs.cv_results_["std_test_score"][gs.best_index_]),
            "CV_MAE": float(np.mean(cv_mae)),
            "CV_R2": float(np.mean(cv_r2)),
            "Train_RMSE": m_tr["RMSE"],
            "Train_R2": m_tr["R2"],
            "Test_RMSE": m_te["RMSE"],
            "Test_MAE": m_te["MAE"],
            "Test_R2": m_te["R2"],
            "Overfit_gap_RMSE": m_te["RMSE"] - m_tr["RMSE"],
            "Train_time_s": round(secs, 1),
            "Best_params": {k.replace("m__", ""): v for k, v in gs.best_params_.items()},
        }
    )
    preds[name] = p_te
    fitted[name] = best
    joblib.dump(best, OUT / "models" / (name.split(" (")[0].replace(" ", "_").replace("+", "plus") + ".joblib"))
    print(f"{name:32s} CV RMSE {-gs.best_score_:.3f} | Test RMSE {m_te['RMSE']:.3f} | Test R2 {m_te['R2']:.3f} | {secs:.0f}s")

results = pd.DataFrame(rows).sort_values("Test_RMSE").reset_index(drop=True)
results.to_csv(OUT / "model_comparison.csv", index=False)
pd.DataFrame({"Date": test.Date.values, "Actual": y_test.values, **preds}).to_csv(
    OUT / "test_predictions.csv", index=False
)
print(results[["Model", "CV_RMSE", "Test_RMSE", "Test_MAE", "Test_R2"]].round(3).to_string(index=False))

# %% Plots for the comparison / evaluation phase
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False})
order = results.sort_values("Test_RMSE", ascending=False)

fig, ax = plt.subplots(figsize=(9, 5.5))
y = np.arange(len(order))
ax.barh(y + 0.2, order.CV_RMSE, 0.4, label="CV RMSE (train period)", color="#9ab")
ax.barh(y - 0.2, order.Test_RMSE, 0.4, label="Test RMSE (2024-25)", color="#27a")
ax.set_yticks(y, order.Model)
ax.set_xlabel("RMSE (mm/day)")
ax.set_title("Model comparison — lower is better")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "fig_model_comparison.png")
plt.close()

best_name = results.loc[results.Model != "Mean Predictor (reference)", "Model"].iloc[0]
base_name = "Linear Regression (BASELINE)"
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharex=True, sharey=True)
for ax, n in zip(axes, [base_name, best_name]):
    ax.scatter(y_test, preds[n], s=8, alpha=0.5)
    lim = [0, max(y_test.max(), preds[n].max()) + 0.5]
    ax.plot(lim, lim, "r--", lw=1)
    r = results.set_index("Model").loc[n]
    ax.set_title(f"{n}\nRMSE {r.Test_RMSE:.2f} | R² {r.Test_R2:.2f}", fontsize=10)
    ax.set_xlabel("Actual")
axes[0].set_ylabel("Predicted")
plt.tight_layout()
plt.savefig(OUT / "fig_actual_vs_predicted.png")
plt.close()

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(test.Date, y_test, color="k", lw=0.8, label="Actual")
ax.plot(test.Date, preds[best_name], color="#d62", lw=0.8, label=best_name)
ax.plot(test.Date, preds[base_name], color="#27a", lw=0.8, alpha=0.6, label="Baseline")
ax.set_ylabel("Evaporation (mm/day)")
ax.legend()
ax.set_title("Test period: actual vs predicted")
plt.tight_layout()
plt.savefig(OUT / "fig_test_timeseries.png")
plt.close()

pi = permutation_importance(
    fitted[best_name], X_test, y_test, n_repeats=15, random_state=RANDOM_STATE, scoring="neg_root_mean_squared_error"
)
imp = pd.Series(pi.importances_mean, index=features).sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
imp.plot.barh(ax=ax, color="#27a")
ax.set_title(f"Permutation importance — {best_name}")
ax.set_xlabel("Increase in test RMSE when shuffled")
plt.tight_layout()
plt.savefig(OUT / "fig_feature_importance.png")
plt.close()
imp.sort_values(ascending=False).to_csv(OUT / "feature_importance.csv", header=["importance"])
print("Best model:", best_name)
