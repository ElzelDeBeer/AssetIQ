import json
from pathlib import Path

import altair as alt
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from ai4i_features import ACTIONS, MODE_NAMES, score_frame
from theme import chart_style, inject
from train_ai4i import DATA, train_and_save

inject("blueprint")
ROOT = Path(__file__).resolve().parent.parent
MP, TP, JP = ROOT / "models" / "ai4i_model.joblib", ROOT / "models" / "test_set.csv", ROOT / "models" / "metrics.json"

st.markdown('<div class="hero"><div class="wm">Model evidence</div><div class="tag">Failure prediction trained and tested on the public AI4I 2020 dataset.</div></div>', unsafe_allow_html=True)
if not (MP.exists() and TP.exists() and JP.exists()) and not DATA.exists():
    up = st.file_uploader("Upload ai4i2020.csv to train the model", type="csv")
    if up is not None:
        DATA.parent.mkdir(exist_ok=True)
        DATA.write_bytes(up.getvalue())
        st.rerun()
if not (MP.exists() and TP.exists() and JP.exists()) and DATA.exists():
    with st.spinner("Training the model on the AI4I dataset for the first time. This takes about a minute."):
        train_and_save()
if not (MP.exists() and TP.exists() and JP.exists()):
    st.warning("Upload ai4i2020.csv above (from the UCI page). The model then trains automatically, which takes about a minute.")
    st.stop()
st.info("AI4I 2020 is a public benchmark dataset made by researchers to mimic industrial machine failures (10,000 records, about 3.4% failures). "
        "It is not data from a real plant. The model never saw the test machines it is scored on below.")


@st.cache_resource
def load():
    return joblib.load(MP), pd.read_csv(TP), json.loads(JP.read_text())


bundle, test, met = load()
scored = score_frame(bundle, test).sort_values("risk", ascending=False).reset_index(drop=True)
t1, t2, t3 = st.tabs(["Evidence", "Rank real machines", "Score a machine"])

with t1:
    m, b = met["final"], met["baseline"]
    c = st.columns(4)
    c[0].metric("Precision", f'{m["precision"]:.2f}', f'{m["precision"] - b["precision"]:+.2f} vs baseline')
    c[1].metric("Recall", f'{m["recall"]:.2f}', f'{m["recall"] - b["recall"]:+.2f} vs baseline')
    c[2].metric("PR-AUC", f'{m["pr_auc"]:.2f}', f'{m["pr_auc"] - b["pr_auc"]:+.2f} vs baseline')
    c[3].metric("Top 10% of machines catch", f'{met["top10_capture"] * 100:.0f}% of failures')
    cols = ["precision", "recall", "f1", "roc_auc", "pr_auc"]
    st.dataframe(pd.DataFrame({"Logistic regression (baseline)": b, "Random Forest (AssetIQ)": m}).T[cols].round(3), use_container_width=True)
    st.caption(f'Held-out test set: {met["n_test"]} machines. A model that always says "no failure" would be {100 * (1 - met["failure_rate"]):.1f}% accurate, '
               "so accuracy is not used. Precision, recall and PR-AUC are what matter for rare failures.")
    tn, fp, fn, tp = np.ravel(met["confusion"])
    st.dataframe(pd.DataFrame([[tn, fp], [fn, tp]], index=["Actually OK", "Actually failed"], columns=["Predicted OK", "Predicted failure"]), use_container_width=True)
    imp = pd.Series(met["importance"]).sort_values().rename("importance").rename_axis("feature").reset_index()
    st.altair_chart(chart_style(alt.Chart(imp).mark_bar(color="#ffd35a").encode(x=alt.X("importance:Q", title="Importance"), y=alt.Y("feature:N", sort=None, title=None)).properties(height=280)),
                    use_container_width=True)

with t2:
    n = st.slider("Machines to show", 10, 50, 20)
    top = scored.head(n)
    ids = top["Product ID"] if "Product ID" in top else top.index
    a, b2, c2 = st.columns(3)
    a.metric(f"Actually failed in the top {n}", f'{int(top["Machine failure"].sum())} of {n}')
    b2.metric("Failures in the whole test set", int(scored["Machine failure"].sum()))
    c2.metric("Test machines", len(scored))
    view = pd.DataFrame({"Machine": ids, "Type": top["Type"], "risk_pct": (top["risk"] * 100).round(), "Likely failure mode": top["mode"].map(MODE_NAMES),
                         "Unusual reading": top["anomaly"].map({True: "Yes", False: "-"}), "Actually failed": top["Machine failure"].map({1: "Yes", 0: "No"}),
                         "Suggested action": top["mode"].map(ACTIONS)})
    st.dataframe(view, hide_index=True, use_container_width=True,
                 column_config={"risk_pct": st.column_config.ProgressColumn("Failure risk", min_value=0, max_value=100, format="%d%%")})
    st.caption("Suggestions are for a qualified person to review. 'Actually failed' comes from the dataset labels and is shown only to check the ranking.")

with t3:
    c1, c2 = st.columns(2)
    typ = c1.radio("Product type", ["L", "M", "H"], horizontal=True)
    air = c1.slider("Air temperature [K]", 295.0, 305.0, 300.0, 0.1)
    proc = c1.slider("Process temperature [K]", 305.0, 315.0, 310.0, 0.1)
    rpm = c2.slider("Rotational speed [rpm]", 1100, 2900, 1500, 10)
    tq = c2.slider("Torque [Nm]", 3.0, 80.0, 40.0, 0.5)
    wear = c2.slider("Tool wear [min]", 0, 255, 100)
    row = pd.DataFrame([{"Type": typ, "Air temperature [K]": air, "Process temperature [K]": proc, "Rotational speed [rpm]": rpm, "Torque [Nm]": tq, "Tool wear [min]": wear}])
    r = score_frame(bundle, row).iloc[0]
    st.metric("Failure risk", f"{r['risk'] * 100:.0f}%")
    if r["flag"]:
        st.error(f"Flagged for inspection. Most likely cause: {MODE_NAMES[r['mode']]}. {ACTIONS[r['mode']]}")
    else:
        st.success("Below the inspection threshold. Keep to the routine schedule.")
    if r["anomaly"]:
        st.warning("This combination of readings is unusual compared with normal operation.")
    st.caption(f"Temperature gap {proc - air:.1f} K. Power {tq * rpm * 2 * np.pi / 60:,.0f} W. Suggestions are for a qualified person to review.")
