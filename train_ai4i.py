"""Train AssetIQ AI's failure models on the AI4I 2020 dataset.  Run:  python train_ai4i.py"""
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ai4i_features import MODES, features, load

ROOT = Path(__file__).resolve().parent
DATA, OUT = ROOT / "data" / "ai4i2020.csv", ROOT / "models"
if not DATA.exists():
    raise SystemExit(f"Dataset not found. Download ai4i2020.csv and save it as {DATA}")
OUT.mkdir(exist_ok=True)

df = load(DATA)
X, y = features(df), df["Machine failure"].astype(int)
tr, te = train_test_split(df.index, test_size=0.25, random_state=42, stratify=y)
Xtr, Xte, ytr, yte = X.loc[tr], X.loc[te], y.loc[tr], y.loc[te]
grid = np.linspace(0.05, 0.95, 91)


def tune(model):
    """Pick the decision threshold with cross-validation on the TRAINING rows only, then fit."""
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    oof = cross_val_predict(model, Xtr, ytr, cv=cv, method="predict_proba")[:, 1]
    thr = float(grid[int(np.argmax([f1_score(ytr, oof >= t) for t in grid]))])
    return model.fit(Xtr, ytr), thr


def evaluate(model, thr):
    p = model.predict_proba(Xte)[:, 1]
    pred = p >= thr
    return {"precision": float(precision_score(yte, pred, zero_division=0)), "recall": float(recall_score(yte, pred)),
            "f1": float(f1_score(yte, pred)), "roc_auc": float(roc_auc_score(yte, p)),
            "pr_auc": float(average_precision_score(yte, p)), "threshold": thr}, p, pred


base, base_thr = tune(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")))
rf, thr = tune(RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=5, class_weight="balanced_subsample", random_state=42, n_jobs=-1))
m_base, _, _ = evaluate(base, base_thr)
m_rf, p, pred = evaluate(rf, thr)

modes = RandomForestClassifier(n_estimators=40, max_depth=8, min_samples_leaf=3, class_weight="balanced_subsample", random_state=42,
                               n_jobs=-1).fit(Xtr, df.loc[tr, MODES].astype(int))
iso = IsolationForest(contamination=0.02, random_state=42).fit(Xtr[ytr == 0])

order = np.argsort(-p)
k = max(1, int(0.1 * len(p)))
metrics = {"baseline": m_base, "final": m_rf, "threshold": thr, "n_train": int(len(tr)), "n_test": int(len(te)),
           "failure_rate": float(y.mean()), "confusion": confusion_matrix(yte, pred).tolist(),
           "top10_capture": float(yte.values[order[:k]].sum() / max(yte.sum(), 1)),
           "importance": dict(zip(X.columns, map(float, rf.feature_importances_)))}
joblib.dump({"clf": rf, "modes": modes, "iso": iso, "threshold": thr, "features": list(X.columns)}, OUT / "ai4i_model.joblib")
(OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
df.loc[te].to_csv(OUT / "test_set.csv", index=False)


def pack(est, multi=False):
    """Compact JSON form of one decision tree, so the web dashboard can score machines in the browser."""
    t = est.tree_
    v = t.value[:, :, 1] / t.value.sum(axis=2) if multi else t.value[:, 0, 1] / t.value[:, 0, :].sum(axis=1)
    return {"f": t.feature.tolist(), "t": np.round(t.threshold, 4).tolist(), "l": t.children_left.tolist(),
            "r": t.children_right.tolist(), "v": np.round(v, 3).tolist()}


web = {"features": list(X.columns), "threshold": thr, "metrics": metrics, "clf": {"trees": [pack(e) for e in rf.estimators_]},
       "modes": {"names": MODES, "trees": [pack(e, True) for e in modes.estimators_]},
       "test": [[r["Type"], float(r["Air temperature [K]"]), float(r["Process temperature [K]"]), float(r["Rotational speed [rpm]"]),
                 float(r["Torque [Nm]"]), float(r["Tool wear [min]"]), int(r["Machine failure"]), str(r.get("Product ID", i))]
                for i, r in df.loc[te].iterrows()]}
(OUT / "web_export.json").write_text(json.dumps(web, separators=(",", ":")))

print(f"Held-out test rows: {len(te)}  |  failure rate: {y.mean():.1%}")
for name, m in [("Logistic regression (baseline)", m_base), ("Random Forest (AssetIQ)", m_rf)]:
    print(f"{name:32s} precision {m['precision']:.2f}  recall {m['recall']:.2f}  F1 {m['f1']:.2f}  ROC-AUC {m['roc_auc']:.3f}  PR-AUC {m['pr_auc']:.3f}")
print(f"Top 10% of machines by risk capture {metrics['top10_capture']:.0%} of failures. Saved to {OUT}")
print(f"Web dashboard file: {OUT / 'web_export.json'} ({(OUT / 'web_export.json').stat().st_size / 1e6:.1f} MB)")
