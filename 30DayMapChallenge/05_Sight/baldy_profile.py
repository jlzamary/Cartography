import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.ticker import MultipleLocator

# Global Params
CSV = "poly_line.csv"
ELEV = "USGS3DEPElevation_PHIL"   # meters
OBS_OFFSET_M = 1.8                # eye height above the summit
VIS_FILL, VIS_EDGE = "#D9785F", "#E0954A"
HIDDEN, NAVY = "#D9D9D9", "#1C2333"
plt.rcParams["font.size"] = 18

df = pd.read_csv(CSV, encoding="utf-8-sig")

# Export scrambled the order, so sort by distance from the summit (start of the line)
start = df.loc[df[ELEV].idxmax()]
df["d_m"] = np.hypot(df.Point_X - start.Point_X, df.Point_Y - start.Point_Y)
df = df.sort_values("d_m").reset_index(drop=True)

d = df["d_m"].to_numpy()
z = df[ELEV].to_numpy()

# Line of sight from the summit (earth curvature + refraction, k = 0.13)
R = 6_371_000
z_eff = z - (d**2 / (2 * R)) * (1 - 0.13)
z_obs = z[0] + OBS_OFFSET_M
with np.errstate(divide="ignore", invalid="ignore"):
    angle = (z_eff - z_obs) / d
angle[0] = -np.inf
visible = angle >= np.maximum.accumulate(np.r_[-np.inf, angle[:-1]])
visible[0] = True

# Units for the chart
dist_mi = d / 1609.34
elev_ft = z * 3.28084
base = np.floor((elev_ft.min() - 300) / 500) * 500

fig, ax = plt.subplots(figsize=(11, 4.2))
ax.fill_between(dist_mi, elev_ft, base, color=HIDDEN, lw=0, label="Hidden from summit")
ax.fill_between(dist_mi, elev_ft, base, where=visible, color=VIS_FILL, lw=0,
                step="mid", label="Visible from summit")
ax.plot(dist_mi, elev_ft, color=NAVY, lw=1)

# A / A' labels and summit marker
ax.annotate("A", (0, elev_ft[0]), xytext=(-20, 4), textcoords="offset points",
            fontsize=24, fontweight="bold", color=NAVY)
ax.annotate("A′", (dist_mi[-1], elev_ft[-1]), xytext=(4, 4), textcoords="offset points",
            fontsize=24, fontweight="bold", color=NAVY)
ax.annotate("Baldy Mt. summit", (0, elev_ft[0]),
            xytext=(10, -6), textcoords="offset points", fontsize=18, color=NAVY, va="top")

ax.set_xlim(0, dist_mi[-1])
ax.set_ylim(base, elev_ft.max() * 1.05)
ax.set_xlabel("Distance from summit (mi)", color=NAVY, fontsize=20)
ax.set_ylabel("Elevation (ft)", color=NAVY, fontsize=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f} ft"))
ax.xaxis.set_major_locator(MultipleLocator(40))
ax.set_yticks([elev_ft[0]])
ax.tick_params(axis="y", direction="in", pad=-6)
for lbl in ax.get_yticklabels():
    lbl.set_horizontalalignment("left")
    lbl.set_verticalalignment("bottom")
ax.tick_params(colors=NAVY, labelsize=18)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(NAVY)

# Slight white halo behind all dark labels
halo = [pe.withStroke(linewidth=3, foreground=(1, 1, 1, 0.25))]  # 75% transparent
fig.canvas.draw()  # materialize tick labels before styling them
for t in (ax.texts + [ax.xaxis.label, ax.yaxis.label]
          + ax.get_xticklabels() + ax.get_yticklabels()):
    t.set_path_effects(halo)

plt.tight_layout()
plt.savefig("baldy_profile.png", dpi=300, transparent=True)
print(f"{visible.mean():.0%} of the profile is visible from the summit")
