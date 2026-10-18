import streamlit as st

from theme import inject

inject("hero")

st.markdown('<div class="lhero"><div class="mono">AI PREDICTIVE MAINTENANCE AND ASSET INTELLIGENCE</div><div class="wm">AssetIQ AI</div>'
            '<div class="tag">Predict failures. Optimize maintenance. Protect operations.</div></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.page_link("views/dashboard.py", label="Open the dashboard")
with c2:
    st.page_link("views/evidence.py", label="See the model evidence")

pillars = [("FAILURE RISK", "Predict", "Each asset gets a 30-day failure probability and an estimate of days left."),
           ("UNUSUAL BEHAVIOUR", "Detect", "Readings that drift away from normal operation are flagged on a timeline."),
           ("RANKED ACTIONS", "Prioritize", "Risk, impact and crew capacity become one inspection list for a qualified person to approve.")]
st.markdown('<p class="mono" style="text-align:center;margin-top:.5rem">Upload your own sensor CSV on the dashboard page, or pick an industry there.</p>', unsafe_allow_html=True)
st.markdown('<div class="s2"><h2>One platform, three answers</h2><p class="sub">AssetIQ reads your sensor and maintenance history, then tells a planner where to look first.</p></div>'
            '<div class="cols3">' + "".join(f'<div><span class="mono">{a}</span><b>{b}</b><p>{c}</p></div>' for a, b, c in pillars) + '</div>', unsafe_allow_html=True)

industries = [("mining", "Mining", "Conveyors, ventilation fans, underground pumps"), ("energy", "Energy", "Transformers and turbines under load-shedding strain"),
              ("transport", "Transport", "Locomotives and port cranes, ranked by what a stoppage costs"), ("telecoms", "Telecoms", "Base-station batteries and backup generators"),
              ("water", "Water", "Pump stations that communities depend on")]
cards = "".join(f'<div class="ind ind-{k}{" big" if k == "transport" else ""}"><h3>{n}</h3><p>{d}</p></div>' for k, n, d in industries)
st.markdown('<div class="s2"><div class="mono">ALWAYS WATCHING</div><h2>Built for the assets that keep the country running</h2>'
            '<p class="sub">The same models adapt across industries. Swap the sensors and the cost of downtime, keep the workflow.</p></div>'
            f'<div class="rowc">{cards}</div>', unsafe_allow_html=True)

st.markdown('<div class="s2"><div class="mono">FAULT TO FIX</div><h2>Find the problem before it stops the line</h2>'
            '<div class="nums"><div><b>30 days</b><span>FAILURE RISK WINDOW</span></div><div><b>5</b><span>INDUSTRIES COVERED</span></div><div><b>1</b><span>RANKED ACTION LIST</span></div></div>'
            '<p>One ranked list <i style="color:#9b9b9b">or</i> a hundred alarms <i style="color:#9b9b9b">or</i> a week of guesswork.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="end"><div class="wm">AssetIQ AI</div><p>Human-reviewed. Responsibly built.</p></div>', unsafe_allow_html=True)
e1, e2, e3 = st.columns([1, 1, 1])
with e1:
    st.page_link("views/dashboard.py", label="Launch the dashboard")
with e2:
    st.page_link("views/evidence.py", label="Model evidence")
st.markdown('<p class="mono" style="text-align:center;margin-top:2rem">Demo uses a simulated South African fleet and the public AI4I benchmark. Recommendations must be reviewed by a qualified person. Built by Elzel De Beer.</p>', unsafe_allow_html=True)
