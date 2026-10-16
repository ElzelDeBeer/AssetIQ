import streamlit as st


def inject():
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
