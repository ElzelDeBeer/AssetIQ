"""Shared helpers for the AI4I 2020 model: loading, feature engineering and scoring."""
import numpy as np
import pandas as pd

MODES = ["TWF", "HDF", "PWF", "OSF"]
MODE_NAMES = {"TWF": "Tool wear", "HDF": "Heat dissipation", "PWF": "Power", "OSF": "Overstrain"}
ACTIONS = {
    "TWF": "Replace or re-sharpen the tool before it reaches its wear limit.",
    "HDF": "Check cooling and airflow. The process-to-air temperature gap is too small at this speed.",
    "PWF": "Check the drive and load. Power draw is outside its normal band.",
    "OSF": "Reduce load or inspect for overstrain. Torque and tool wear are high together.",
}


def load(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    names = {"air temp": "Air temperature [K]", "process temp": "Process temperature [K]", "rotational": "Rotational speed [rpm]",
             "torque": "Torque [Nm]", "tool wear": "Tool wear [min]", "machine failure": "Machine failure", "product id": "Product ID"}
    ren = {c: v for c in df.columns for k, v in names.items() if c.lower().startswith(k)}
    return df.rename(columns=ren)


def features(df):
    d = pd.DataFrame(index=df.index)
    d["type_L"] = (df["Type"] == "L").astype(int)
    d["type_M"] = (df["Type"] == "M").astype(int)
    d["air_temp"] = df["Air temperature [K]"]
    d["proc_temp"] = df["Process temperature [K]"]
    d["rpm"] = df["Rotational speed [rpm]"]
    d["torque"] = df["Torque [Nm]"]
    d["tool_wear"] = df["Tool wear [min]"]
    d["temp_diff"] = d["proc_temp"] - d["air_temp"]
    d["power_w"] = d["torque"] * d["rpm"] * 2 * np.pi / 60
    return d


def score_frame(bundle, df):
    X = features(df)
    out = df.copy()
    out["risk"] = bundle["clf"].predict_proba(X)[:, 1]
    mp = np.column_stack([p[:, 1] if p.shape[1] > 1 else np.zeros(len(X)) for p in bundle["modes"].predict_proba(X)])
    out["mode"] = [MODES[i] for i in mp.argmax(axis=1)]
    out["anomaly"] = bundle["iso"].predict(X) == -1
    out["flag"] = out["risk"] >= bundle["threshold"]
    return out
