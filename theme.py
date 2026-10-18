"""Shared look for AssetIQ AI: dark cinematic pages, stippled heat art, black chart panels."""
import base64
import html
from pathlib import Path

import streamlit as st

from art import stipple_svg, thermal_svg

ASSETS = Path(__file__).resolve().parent / "assets"
FONTS = "@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Inter+Tight:wght@600;700&family=Newsreader:wght@400;500&family=JetBrains+Mono&display=swap');"

BASE = """
:root{--acc:#6fc3ff}
.stApp{color:#ededed;font-family:'Newsreader',Georgia,serif}
[data-testid="stHeader"]{background:transparent}
footer,#MainMenu,[data-testid="stMainMenu"],[data-testid="stAppDeployButton"],.stAppDeployButton{display:none!important}
[data-testid="stExpandSidebarButton"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapseButton"]{display:flex!important;color:#ededed!important}
[data-testid="stSidebar"]{background:rgba(18,18,18,.92);border-right:1px solid #333}
.block-container{max-width:72rem}
h1,h2,h3,[data-testid="stMetricValue"]{font-family:'Inter Tight',sans-serif!important;letter-spacing:-.02em}
[data-testid="stMetricLabel"],button[role="tab"],.lbl{font-family:'JetBrains Mono',monospace!important;font-size:.72rem!important;letter-spacing:.06em}
[data-testid="stMetric"]{background:rgba(0,0,0,.55);border:1px solid #333;border-radius:1rem;padding:1rem 1.2rem}
.stButton>button,.stDownloadButton>button,[data-testid="stPageLink"] a{border-radius:999px;background:#222;border:1px solid #3a3a3a;font-family:'JetBrains Mono',monospace;font-size:.78rem}
.stButton>button:hover,.stDownloadButton>button:hover,[data-testid="stPageLink"] a:hover{border-color:var(--acc);color:#fff}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:1rem;background:rgba(0,0,0,.5);border-color:#333}
[data-baseweb="tab-highlight"]{background:var(--acc)!important}
button[role="tab"][aria-selected="true"]{color:var(--acc)!important}
span[data-baseweb="tag"]{background:#2c3a44!important;color:#cfe9ff!important}
[data-testid="stSlider"] [role="slider"]{background:var(--acc)!important}
[data-testid="stVegaLiteChart"],[data-testid="stArrowVegaLiteChart"]{background:#000;border:1px solid #2a2a2a;border-radius:1rem;overflow:hidden}
[data-testid="stDataFrame"]{border-radius:1rem;overflow:hidden}
.wm{font-family:'Michroma',sans-serif;letter-spacing:.08em;font-size:2.4rem;margin-top:1rem}
.lbl{opacity:.6}
.hero{text-align:center;padding:2rem 0 1rem}
.hero svg{width:110px;color:#6fc3ff}
.hero .tag{font-size:1.25rem;margin-top:.8rem;opacity:.85}
.hm{position:relative;background:#08090c;border:1px solid #4a2c14;border-top:2px solid #f08a2a;border-radius:.5rem;padding:1rem 1rem .8rem;margin:1rem 0}
.hmh{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#e8742c;font:.68rem 'JetBrains Mono',monospace;letter-spacing:.05em}
.hbig{position:absolute;left:1.4rem;bottom:4.2rem;font:600 3.6rem/1 'Inter Tight',sans-serif;color:#fff2c4}.hbig sup{font-size:.4em;color:#e8742c}
.leg{display:flex;gap:1rem;flex-wrap:wrap;margin-top:.6rem;font:.66rem 'JetBrains Mono',monospace;color:#8a8a8a}.leg i{display:inline-block;width:.7rem;height:.7rem;margin-right:.4rem}
"""
ART = ".stApp{background:linear-gradient(rgba(16,16,16,.55),rgba(16,16,16,.93)),url('ARTURL') center/cover fixed #101010}"
BLUEPRINT = """
.stApp{background-color:#0c3b6e;background-image:linear-gradient(rgba(150,200,255,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(150,200,255,.12) 1px,transparent 1px);background-size:24px 24px;color:#dff0ff}
:root{--acc:#ffd35a}[data-testid="stSidebar"]{background:rgba(8,36,70,.95)}[data-testid="stMetric"]{background:rgba(5,22,48,.7);border-color:#2f6aa8}
span[data-baseweb="tag"]{background:#144a82!important;color:#ffe9a8!important}
"""
HERO = """
.stApp{background:linear-gradient(rgba(26,26,26,.86),rgba(26,26,26,.97)),url('ARTURL') center/cover fixed #1a1a1a}
.lhero{min-height:78vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:5rem 1rem;border-radius:1.4rem;background:linear-gradient(rgba(16,16,16,.45),rgba(26,26,26,.95)),url('HEROURL') center/cover no-repeat}
.lhero .wm{font-size:clamp(2.2rem,9vw,6.4rem);margin:1rem 0 0}.lhero .tag{font-size:1.5rem;margin:1.2rem 0 0;max-width:32rem}
.mono{font:.72rem 'JetBrains Mono',monospace;letter-spacing:.06em;color:#9b9b9b}
.s2{padding:4rem 0 1rem;text-align:center}.s2 h2{font-size:clamp(1.8rem,5vw,3rem);margin:.4rem 0}.s2 p.sub{color:#9b9b9b;max-width:34rem;margin:.6rem auto 0}
.cols3{display:grid;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:2rem;margin-top:2.4rem;text-align:left}.cols3 b{display:block;font:700 1.5rem 'Inter Tight',sans-serif;margin:.3rem 0}.cols3 span{color:var(--acc)}.cols3 p{color:#9b9b9b;margin:0}
.rowc{display:flex;gap:1rem;margin-top:2.4rem;overflow-x:auto;align-items:center;padding:.6rem .3rem}
.ind{position:relative;overflow:hidden;flex:0 0 12.5rem;height:17rem;border-radius:1.4rem;padding:1.2rem;display:flex;flex-direction:column;justify-content:flex-end;text-align:left;border:1px solid #333;background-size:cover;background-position:center}
.ind.big{flex-basis:17rem;height:22rem}.ind::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(10,10,10,.9),rgba(10,10,10,.05) 62%)}
.ind h3,.ind p{position:relative;z-index:1;margin:0}.ind h3{color:#fff;font-size:1.25rem}.ind p{font-size:.95rem;color:#d0d0d0;line-height:1.4;margin-top:.3rem}
.nums{display:flex;flex-wrap:wrap;justify-content:center;gap:3rem;margin:2rem 0 1rem}.nums b{display:block;font:700 2.6rem 'Inter Tight',sans-serif;line-height:1}.nums span{font:.7rem 'JetBrains Mono',monospace;color:#9b9b9b}
.end{text-align:center;padding:3rem 0 1rem;border-top:1px solid #333;margin-top:3rem}.end .wm{font-size:clamp(1.6rem,6vw,3.6rem)}
"""


@st.cache_data
def img(name):
    p = ASSETS / name
    if not p.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


@st.cache_data
def art_bg(seed=3):
    return "data:image/svg+xml;base64," + base64.b64encode(stipple_svg(seed=seed).encode()).decode()


def inject(mode="art"):
    """mode: 'art' (stippled heat), 'blueprint' (cyanotype grid) or 'hero' (landing page)."""
    css = BASE
    if mode == "blueprint":
        css += BLUEPRINT
    elif mode == "hero":
        css += HERO.replace("ARTURL", art_bg(5)).replace("HEROURL", img("hero.jpg"))
        css += "".join(f".ind-{k}{{background-image:url('{img(k + '.jpg')}')}}" for k in ("mining", "energy", "transport", "telecoms", "water"))
    else:
        css += ART.replace("ARTURL", art_bg(3))
    css = "\n".join(l for l in css.split("\n") if l.strip())
    st.markdown(f"<style>{FONTS}{css}</style>", unsafe_allow_html=True)


def chart_style(c):
    """Real charts sit on black panels."""
    return (c.configure(background="#000000", padding=16).configure_view(strokeWidth=0)
            .configure_axis(labelColor="#b5b5b5", titleColor="#b5b5b5", gridColor="#262626", domainColor="#444", tickColor="#444"))


def heat_card(r):
    leg = "".join(f'<span><i style="background:{c}"></i>{t}</span>' for c, t in (("#2b1d6e", "AMBIENT 22 °C"), ("#b3205f", "ELEVATED 55 °C"), ("#ff7a1a", "ALARM 80 °C"), ("#fff1b8", "TRIP 105 °C")))
    return (f'<div class="hm"><div class="hmh"><span>THERMAL · {html.escape(str(r["asset"]).upper())}</span><span>{html.escape(str(r["site"]).upper())} · AMBIENT 22 °C</span></div>'
            f'{thermal_svg(float(r["temperature"]))}<div class="hbig">{float(r["temperature"]):.1f}<sup>°C</sup></div>'
            f'<div class="hmh"><span>▲ {float(r["risk"]) * 100:.0f}% FAILURE RISK IN 30 DAYS · {int(r["rul_est"])} DAYS LEFT</span><span>{r["status"]}</span></div><div class="leg">{leg}</div></div>')
