"""Generative stippled art and the thermal heat-map graphic used for AssetIQ AI's backgrounds."""
import numpy as np

RAMP = [(0.0, (43, 29, 110)), (0.35, (106, 42, 156)), (0.6, (179, 32, 95)), (0.8, (255, 122, 26)), (1.0, (255, 211, 90))]


def ramp(t):
    t = min(max(float(t), 0.0), 1.0)
    for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
        if t <= b:
            u = (t - a) / (b - a)
            return tuple(int(ca[i] + (cb[i] - ca[i]) * u) for i in range(3))
    return RAMP[-1][1]


def stipple_svg(w=1600, h=900, step=22, seed=3, spots=5):
    """Dots whose size and colour follow a few warm 'heat spots', like a thermal topography."""
    rng = np.random.default_rng(seed)
    cx, cy = rng.uniform(.15 * w, .85 * w, spots), rng.uniform(.15 * h, .85 * h, spots)
    amp, sg = rng.uniform(.65, 1.0, spots), rng.uniform(.08, .16, spots) * w
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#101010"/>']
    for y in range(step // 2, h, step):
        for x in range(step // 2, w, step):
            v = sum(a * np.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * s * s)) for px, py, a, s in zip(cx, cy, amp, sg)) + .1 * np.sin(x / 90) * np.cos(y / 70)
            if v < .14:
                continue
            r = min(step * .46, .8 + v * step * .38)
            out.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="rgb{ramp(v)}"/>')
    out.append("</svg>")
    return "".join(out)


def thermal_svg(temp):
    """A motor and vessel drawn as a heat map. The hot spot grows with the temperature reading."""
    t = max(0.0, min(1.0, (temp - 22) / 83))
    g = .35 + .65 * t
    stops = lambda *s: "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in s)
    rings = "".join(f'<circle cx="300" cy="170" r="{r}"/>' for r in (30, 55, 85, 120))
    scale = "".join(f'<text x="518" y="{y + 4}" fill="#8a8a8a" font-size="11" font-family="monospace">{v}°</text>' for v, y in (("105", 60), ("85", 105), ("65", 150), ("45", 195), ("25", 236)))
    return (f'<svg viewBox="0 0 560 300" role="img" aria-label="Thermal view of the asset"><defs>'
            f'<linearGradient id="hm" x1="0" x2="1">{stops((0, "#2b1d6e"), (.6, "#6a2a9c"), (1, "#b3205f"))}</linearGradient>'
            f'<linearGradient id="hv" x1="0" x2="1" y1="1" y2="0">{stops((0, "#e8541c"), (1, "#ffc54d"))}</linearGradient>'
            f'<linearGradient id="hc" x1="0" x2="0" y1="1" y2="0">{stops((0, "#2b1d6e"), (.4, "#b3205f"), (.75, "#ff7a1a"), (1, "#fff1b8"))}</linearGradient>'
            f'<radialGradient id="gl"><stop offset="0" stop-color="#fff6c8"/><stop offset=".25" stop-color="#ffb347" stop-opacity=".85"/><stop offset="1" stop-color="#ff5a1a" stop-opacity="0"/></radialGradient></defs>'
            f'<g fill="none" stroke="#ff9a4d" stroke-opacity=".3" stroke-dasharray="3 5">{rings}</g>'
            '<rect x="60" y="100" width="190" height="130" rx="16" fill="url(#hm)"/><rect x="95" y="80" width="60" height="22" rx="4" fill="#4a2a8a"/>'
            '<rect x="250" y="160" width="60" height="20" fill="#c0306a"/><circle cx="410" cy="170" r="72" fill="url(#hv)"/>'
            '<rect x="392" y="70" width="36" height="40" rx="3" fill="#f08a2a"/><rect x="60" y="245" width="330" height="14" rx="3" fill="url(#hm)"/>'
            f'<circle cx="285" cy="170" r="{60 + 50 * g:.0f}" fill="url(#gl)" opacity="{.45 + .55 * t:.2f}"/>'
            f'<rect x="500" y="60" width="12" height="180" fill="url(#hc)"/>{scale}</svg>')
