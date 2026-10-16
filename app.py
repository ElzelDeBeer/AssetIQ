import zlib
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest, RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="AssetIQ AI", page_icon="⚙️", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Inter+Tight:wght@600;700&family=Newsreader:wght@400;500&family=JetBrains+Mono&display=swap');
:root{--acc:#6fc3ff}
.stApp{background:radial-gradient(60rem 28rem at 50% 0,#2a2f33 0,#1a1a1a 70%) #1a1a1a;color:#ededed;font-family:'Newsreader',Georgia,serif}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:#202020;border-right:1px solid #333}
h1,h2,h3,[data-testid="stMetricValue"]{font-family:'Inter Tight',sans-serif!important;letter-spacing:-.02em}
[data-testid="stMetricLabel"],button[role="tab"],.lbl{font-family:'JetBrains Mono',monospace!important;font-size:.72rem!important;letter-spacing:.06em}
.stButton>button,.stDownloadButton>button{border-radius:999px;background:#222;border:1px solid #3a3a3a;font-family:'JetBrains Mono',monospace;font-size:.78rem}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--acc);color:#fff}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:1rem;background:#202020;border-color:#333}
[data-baseweb="tab-highlight"]{background:var(--acc)!important}
button[role="tab"][aria-selected="true"]{color:var(--acc)!important}
span[data-baseweb="tag"]{background:#2c3a44!important;color:#cfe9ff!important}
.wm{font-family:'Michroma',sans-serif;letter-spacing:.08em;font-size:2.4rem;margin-top:1rem}
.lbl{opacity:.6}
[data-testid="stToolbar"],footer{display:none!important}
[data-testid="stMetric"]{background:#202020;border:1px solid #333;border-radius:1rem;padding:1rem 1.2rem}
[data-testid="stSlider"] [role="slider"]{background:#6fc3ff!important}
.hero{text-align:center;padding:2rem 0 1rem}
.hero svg{width:110px;color:#6fc3ff}
.hero .tag{font-size:1.25rem;margin-top:.8rem;opacity:.85}
</style>""", unsafe_allow_html=True)

FEATS = ["vibration", "temperature", "pressure", "load", "age"]
DRIVERS = FEATS[:3]
SECTORS = {"Mining": ["Conveyor", "Ventilation fan", "Underground pump"], "Energy": ["Transformer", "Turbine"],
           "Transport": ["Locomotive", "Port crane"], "Telecoms": ["Base-station battery", "Backup generator"],
           "Water": ["Pump station"]}
SITES = {"Mining": ["Rustenburg", "Welkom", "Sishen"], "Energy": ["Witbank", "Secunda"],
         "Transport": ["Durban Port", "Richards Bay"], "Telecoms": ["Soweto", "Polokwane"], "Water": ["Vaal", "Tshwane"]}
COST_HR = {"Mining": 180000, "Energy": 250000, "Transport": 120000, "Telecoms": 60000, "Water": 45000}  # assumed R/hour
ACTION = {"vibration": "Inspect bearings, alignment and mounting",
          "temperature": "Check cooling, lubrication and electrical connections",
          "pressure": "Check seals, filters and for leaks"}
fmt = lambda x: f"R {x / 1e6:.1f}M"


def gen(n, rng):
    w = rng.beta(2, 2, n)
    return pd.DataFrame({
        "wear": w, "vibration": 2 + 6 * w ** 1.5 + rng.normal(0, .5, n), "temperature": 55 + 35 * w + rng.normal(0, 4, n),
        "pressure": 6 - 1.5 * w + rng.normal(0, .3, n), "load": rng.normal(65, 10, n),
        "age": np.clip(3 + 8 * w + rng.normal(0, 2, n), 0, None), "rul": np.clip((1 - w) * 120 + rng.normal(0, 12, n), 1, None)})


@st.cache_resource
def models():
    d = gen(4000, np.random.default_rng(1))
    X, y = d[FEATS], d.rul <= 30
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=1, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, class_weight="balanced", min_samples_leaf=5, random_state=1).fit(Xtr, ytr)
    reg = GradientBoostingRegressor(random_state=1).fit(X, d.rul)
    healthy = d[d.wear < .4][FEATS]
    iso = IsolationForest(contamination=.03, random_state=1).fit(healthy)
    p = clf.predict(Xte)
    return clf, reg, iso, healthy.agg(["mean", "std"]), precision_score(yte, p), recall_score(yte, p)


@st.cache_data
def fleet():
    rng = np.random.default_rng(7)
    d = gen(48, rng)
    rows = []
    for i in range(48):
        s = str(rng.choice(list(SECTORS)))
        rows.append((s, f"{rng.choice(SECTORS[s])} {chr(65 + i % 26)}{i + 1:02d}", str(rng.choice(SITES[s])), int(rng.integers(1, 6))))
    return pd.concat([pd.DataFrame(rows, columns=["sector", "asset", "site", "crit"]), d], axis=1)


def score(d, stage):
    clf, reg, _, hs, _, _ = models()
    d = d.copy()
    boost = d.sector.isin(["Energy", "Telecoms"]) * 0.04 * stage  # assumption: load shedding strains backup power
    d["risk"] = np.minimum(1, clf.predict_proba(d[FEATS])[:, 1] * (1 + boost))
    d["risk_pct"] = (d.risk * 100).round()
    d["rul_est"] = np.clip(reg.predict(d[FEATS]), 1, None).round()
    d["health"] = ((1 - d.risk) * 100).round()
    d["status"] = pd.cut(d.risk, [-1, .3, .6, 2], labels=["Healthy", "Watch", "Critical"])
    d["fail_cost"] = 40000 * d.crit + 4 * d.crit * d.sector.map(COST_HR).fillna(100000)
    d["priority"] = d.risk * d.fail_cost
    d["priority"] = (100 * d.priority / max(d.priority.max(), 1e-9)).round(1)
    z = ((d[DRIVERS] - hs.loc["mean", DRIVERS]) / hs.loc["std", DRIVERS]).abs()
    d["driver"] = z.idxmax(axis=1)
    return d.sort_values("priority", ascending=False).reset_index(drop=True)


def history(r, days=90):
    if src is not None:
        h = src[src.asset == r.asset].reset_index(drop=True)
        h["day"] = h["date"] if "date" in h and h["date"].notna().any() else h.index
        h["anomaly"] = models()[2].predict(h[FEATS]) == -1
        return h
    rng = np.random.default_rng(zlib.crc32(r.asset.encode()))
    w = np.linspace(max(0, r.wear - .3), r.wear, days)
    h = pd.DataFrame({"day": np.arange(-days + 1, 1), "vibration": 2 + 6 * w ** 1.5 + rng.normal(0, .5, days),
                      "temperature": 55 + 35 * w + rng.normal(0, 4, days), "pressure": 6 - 1.5 * w + rng.normal(0, .3, days),
                      "load": rng.normal(65, 10, days), "age": r.age})
    h["anomaly"] = models()[2].predict(h[FEATS]) == -1
    return h


TEMPLATE = ("asset,sector,site,crit,date,vibration,temperature,pressure,load,age\n"
            "Pump P-01,Water,Vaal,4,2026-10-01,3.1,62,5.8,64,6\n"
            "Pump P-01,Water,Vaal,4,2026-10-08,3.4,64,5.7,66,6\n")


@st.cache_data
def ranges():
    return gen(4000, np.random.default_rng(1))[DRIVERS].agg(["min", "max"])


def load_csv(f):
    try:
        raw = pd.read_csv(f)
    except Exception:
        return None, "Could not read that file. Upload a plain .csv."
    raw.columns = [str(c).strip().lower().replace(" ", "_") for c in raw.columns]
    raw = raw.rename(columns={"criticality": "crit", "age_years": "age", "timestamp": "date"})
    miss = [c for c in ["asset", "vibration", "temperature", "pressure"] if c not in raw.columns]
    if miss:
        return None, "Missing columns: " + ", ".join(miss)
    for c, v in {"load": 65, "age": 5, "crit": 3, "sector": "Other", "site": "Unknown"}.items():
        if c not in raw.columns:
            raw[c] = v
    for c in ["vibration", "temperature", "pressure", "load", "age", "crit"]:
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw = raw.dropna(subset=["asset", "vibration", "temperature", "pressure"])
    if raw.empty:
        return None, "No valid rows found. Check the numeric columns."
    raw["asset"] = raw.asset.astype(str)
    raw["sector"] = raw.sector.fillna("Other").astype(str)
    raw["site"] = raw.site.fillna("Unknown").astype(str)
    raw["crit"] = raw.crit.fillna(3).clip(1, 5).round().astype(int)
    raw["load"], raw["age"] = raw.load.fillna(65), raw.age.fillna(5)
    if "date" in raw.columns:
        raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
        raw = raw.sort_values("date", kind="stable")
    return raw.reset_index(drop=True), None


def bars(s):
    d = s.rename("value").rename_axis("name").reset_index()
    st.altair_chart(alt.Chart(d).mark_bar(color="#6fc3ff", cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("name:N", sort=None, title=None, axis=alt.Axis(labelAngle=0)), y=alt.Y("value:Q", title=None)).properties(height=260),
        use_container_width=True)


def action(r):
    when = "within 48 hours" if r.risk >= .6 else "within 2 weeks" if r.risk >= .3 else "at the next routine check"
    return f"{ACTION[r.driver]} {when}."


_, _, _, _, prec, rec = models()
src = None
with st.sidebar:
    st.markdown('<div class="lbl">Your data</div>', unsafe_allow_html=True)
    up = st.file_uploader("Upload sensor CSV", type="csv",
                          help="Required: asset, vibration (mm/s), temperature (C), pressure (bar). Optional: sector, site, crit (1-5), date, load, age. Several rows per asset (with a date) enable the anomaly timeline.")
    st.download_button("Download CSV template", TEMPLATE, "assetiq_template.csv")
    if up is not None:
        src, err = load_csv(up)
        if err:
            st.error(err)
    st.markdown('<div class="lbl">Scenario</div>', unsafe_allow_html=True)
    opts = sorted(src.sector.unique()) if src is not None else list(SECTORS)
    sel = st.multiselect("Industry", opts, default=opts, key="sel_up" if src is not None else "sel_sim")
    stage = st.slider("Load-shedding stage", 0, 6, 2, help="Raises risk for Energy and Telecoms assets (assumption).")
snap = src.groupby("asset", sort=False).tail(1).reset_index(drop=True) if src is not None else fleet()
df = score(snap, stage)
df = df[df.sector.isin(sel)].reset_index(drop=True)
if df.empty:
    st.warning("Select at least one industry in the sidebar.")
    st.stop()

st.markdown('<div class="hero"><svg viewBox="0 0 220 220" fill="none"><circle cx="110" cy="110" r="100" stroke="currentColor" stroke-opacity=".25" stroke-width="2"/><circle cx="110" cy="110" r="72" stroke="currentColor" stroke-opacity=".5" stroke-width="2"/><path d="M14 112h50l14-40 24 78 18-54 12 16h74" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="wm">AssetIQ AI</div><div class="tag">Predict failures. Optimize maintenance. Protect operations.</div></div>', unsafe_allow_html=True)
if src is None:
    st.info("This demo uses a **simulated** South African fleet. Rand costs are assumptions, not client data. Upload your own CSV in the sidebar to score real assets.")
else:
    st.warning("Showing **your uploaded data**. Scores come from a model trained on simulated data, so treat them as indicative until it is retrained on your own failure history. Expected units: vibration mm/s, temperature °C, pressure bar.")
    rg = ranges()
    out = [c for c in DRIVERS if ((snap[c] < rg.loc["min", c] * .5) | (snap[c] > rg.loc["max", c] * 1.5)).any()]
    if out:
        st.warning("Readings in " + ", ".join(out) + " are outside the range the model was trained on. Check your units.")
t1, t2, t3, t4, t5 = st.tabs(["Overview", "Anomalies", "Priorities & actions", "Simulation", "Report"])

with t1:
    exposure = (df.risk * df.fail_cost).sum()
    a, b, c, d_ = st.columns(4)
    a.metric("Assets monitored", len(df))
    b.metric("Critical", int((df.status == "Critical").sum()))
    c.metric("Watch", int((df.status == "Watch").sum()))
    d_.metric("Expected failure cost", fmt(exposure))
    st.subheader("Average health by industry")
    bars(df.groupby("sector").health.mean())
    st.dataframe(df[["asset", "sector", "site", "status", "risk_pct", "rul_est", "health", "priority"]], hide_index=True,
                 use_container_width=True, column_config={
                     "risk_pct": st.column_config.ProgressColumn("Failure risk (30 days)", min_value=0, max_value=100, format="%d%%"),
                     "rul_est": st.column_config.NumberColumn("Est. days left"),
                     "health": st.column_config.NumberColumn("Health score"), "priority": st.column_config.NumberColumn("Priority")})

with t2:
    st.caption("Readings that deviate from normal healthy operation are flagged by an Isolation Forest.")
    c1, c2 = st.columns([2, 1])
    asset = c1.selectbox("Asset", df.asset)
    sensor = c2.radio("Sensor", DRIVERS, horizontal=True)
    h = history(df[df.asset == asset].iloc[0])
    if len(h) < 2:
        st.info("Upload several readings per asset, with a date column, to see its timeline.")
    else:
        xt = "T" if pd.api.types.is_datetime64_any_dtype(h["day"]) else "Q"
        ch = alt.Chart(h).encode(x=alt.X(f"day:{xt}", title="Date" if xt == "T" else ("Days ago" if src is None else "Reading")))
        line = ch.mark_line(color="#6fc3ff").encode(y=alt.Y(f"{sensor}:Q", scale=alt.Scale(zero=False)))
        pts = ch.transform_filter("datum.anomaly").mark_circle(size=80, color="#ff5a4d").encode(y=f"{sensor}:Q")
        st.altair_chart(line + pts, use_container_width=True)
        st.write(f"**{int(h.anomaly.sum())}** unusual readings out of {len(h)}.")

with t3:
    st.caption("Suggestions for a qualified technician to review and approve before any work is scheduled.")
    for _, r in df.head(8).iterrows():
        with st.container(border=True):
            st.markdown(f"**{r.asset}** ({r.site}) is **{r.status}**: {r.risk_pct:.0f}% failure risk, about {r.rul_est:.0f} days of life left.")
            st.write(action(r))
            st.checkbox("Reviewed by a qualified person", key=f"rev_{r.asset}")

with t4:
    st.caption("Compares maintenance strategies over a 4-week window using the model's risk scores.")
    c1, c2, c3 = st.columns(3)
    crew = c1.slider("Inspection crew size", 1, 10, 3)
    per = c2.slider("Inspections per crew per week", 1, 10, 4)
    det = c3.slider("Inspection catch rate (%)", 50, 100, 85) / 100
    N, plan, insp = min(len(df), crew * per * 4), .3, 1500  # planned repair = 30% of failure cost; R1,500 per inspection (assumed)
    exp_cost = df.risk * df.fail_cost
    f = N / len(df)
    reactive = exp_cost.sum()
    sched = (exp_cost * (1 - f * det * (1 - plan))).sum() + N * insp
    caught = np.where(df.index < N, det, 0)
    pred = (exp_cost * (1 - caught * (1 - plan))).sum() + N * insp
    m1, m2, m3 = st.columns(3)
    m1.metric("Reactive (fix after failure)", fmt(reactive))
    m2.metric("Scheduled (random inspections)", fmt(sched), f"{(sched / reactive - 1) * 100:.0f}%", delta_color="inverse")
    m3.metric("Predictive (AssetIQ ranking)", fmt(pred), f"{(pred / reactive - 1) * 100:.0f}%", delta_color="inverse")
    bars(pd.Series({"Reactive": reactive, "Scheduled": sched, "Predictive": pred}))
    st.caption(f"{N} inspections available. Failure cost = repair + downtime hours x assumed R/hour for the industry.")

with t5:
    top = df.head(5)
    lines = [f"{i + 1}. {r.asset} ({r.site}): {r.risk_pct:.0f}% risk, about {r.rul_est:.0f} days left. {action(r)}" for i, r in top.iterrows()]
    rep = (f"# AssetIQ AI weekly report\n\n**Assets:** {len(df)}  \n**Critical:** {int((df.status == 'Critical').sum())}  \n"
           f"**Watch:** {int((df.status == 'Watch').sum())}  \n**Expected failure cost:** {fmt((df.risk * df.fail_cost).sum())}\n\n"
           "## Top priorities\n" + "\n".join(lines) +
           "\n\n*" + ("Simulated data. " if src is None else "Scores come from a model trained on simulated data. ") + "Recommendations must be reviewed by a qualified person.*")
    st.markdown(rep)
    st.download_button("Download report (.md)", rep, "assetiq_weekly_report.md")

with st.expander("Model card and responsible AI"):
    st.markdown(f"""
- **Failure model:** Random Forest predicting failure within 30 days. Holdout precision **{prec:.2f}**, recall **{rec:.2f}** (simulated data).
- **Remaining life:** Gradient Boosting regression. **Anomalies:** Isolation Forest trained on healthy readings.
- **Limits:** trained on simulated data, so retrain on real maintenance history before any real use. Costs and the load-shedding effect are assumptions.
- **Human in the loop:** the system only suggests actions. A qualified person approves every inspection or repair.""")