import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(layout="wide", page_title="Symulacja dwóch soczewek")
try:
    import seaborn as sns
    sns.set_theme(style='darkgrid')
except ImportError:
    plt.style.use('ggplot')

def trace_rays(x, y, d, f1, f2, h_list, eps=1e-6):
    """
    Trace rays through two thin lenses using ray transfer matrices.
    """
    rays = []
    for h in h_list:
        slopes = [0]
        if abs(x - f1) > eps:
            slopes.append(-h / (x - f1))
        if abs(x) > eps:
            slopes.append(-h / x)
        for m in slopes:
            rays.append((h, m))
    segments = []
    for h0, m0 in rays:
        z_obj = -x
        z_l1 = 0
        z_l2 = d
        z_scr = d + y
        pts = [(z_obj, h0)]
        h1 = h0 + m0 * x
        pts.append((z_l1, h1))
        m1 = m0 - h1 / f1
        h2 = h1 + m1 * d
        pts.append((z_l2, h2))
        m2 = m1 - h2 / f2
        h3 = h2 + m2 * y
        pts.append((z_scr, h3))
        segments.append((pts, h0))
    return segments

def plot_case(ax, segments_with_h, x, y, d, f1, f2, title):
    # prepare colors for each ray
    colors = plt.cm.viridis(np.linspace(0, 1, len(segments_with_h)))
    for (pts, h), c in zip(segments_with_h, colors):
        zs, hs = zip(*pts)
        ax.plot(zs, hs, color=c, linewidth=2, label=f'h = {h} mm')
    ax.axvline(0, linestyle='--', label='Lens 1')
    ax.axvline(d, linestyle='-.', label='Lens 2')
    ax.axvline(d + y, linestyle=':', label='Screen')
    ax.set_xlabel('z (mm)', fontsize=12)
    ax.set_ylabel('Height (mm)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize='medium')
    ax.grid(True)

st.title('Interaktywna symulacja dwóch soczewek')

st.sidebar.header('Parametry')
x = st.sidebar.slider('Odległość obiektu od soczewki 1 (x, mm)', 0.1, 200.0, 50.0, 0.1)
d = st.sidebar.slider('Odległość między soczewkami (d, mm)', 0.1, 300.0, 100.0, 0.1)
y = st.sidebar.slider('Odległość od soczewki 2 do ekranu (y, mm)', 0.1, 300.0, 100.0, 0.1)
f1 = st.sidebar.slider('Ogniskowa soczewki 1 (f1, mm)', 0.1, 200.0, 50.0, 0.1)
f2 = st.sidebar.slider('Ogniskowa soczewki 2 (f2, mm)', 0.1, 200.0, 50.0, 0.1)

h_list = [5.0, 10.0]

segments1 = trace_rays(x, y, d, f1, f2, h_list)
segments2 = trace_rays(f1, y, d, f1, f2, h_list)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
plot_case(axes[0], segments1, x, y, d, f1, f2, f'Zwyczajny (x={x})')
plot_case(axes[1], segments2, f1, y, d, f1, f2, f'Interesujący (x=f1={f1})')
plt.tight_layout()
st.pyplot(fig)
