"""The Old Campus, College of William & Mary — drawn from memory (schematic).
Local coordinates in feet: x = east along the Duke of Gloucester St axis, y = north.
Origin = centre of the Wren Building."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyArrowPatch
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.patheffects as pe

rng = np.random.default_rng(1693)

PAPER = "#efe5cf"
INK = "#3a2a1b"
INK_SOFT = "#7a6248"
BRICK = "#9e3d2b"
BRICK_DK = "#5e2117"
HALL = "#cdb08a"
LAWN = "#c9cf9f"
LAWN_DK = "#a9b37c"
SUNK = "#b7c18a"
WATER = "#9db5b0"
ROAD = "#e4d6b8"
SERIF = "GFS Baskerville"
SERIF2 = "Lora"

XMIN, XMAX, YMIN, YMAX = -1400, 1050, -820, 820
fig = plt.figure(figsize=(16, 12.2), dpi=200, facecolor=PAPER)
ax = fig.add_axes([0.045, 0.06, 0.91, 0.78])
ax.set_xlim(XMIN, XMAX); ax.set_ylim(YMIN, YMAX)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor(PAPER)

# paper grain
grain = rng.normal(0, 1, (400, 600))
fig.figimage(np.dstack([np.full_like(grain, 0.36), np.full_like(grain, 0.27),
                        np.full_like(grain, 0.16), np.clip(grain * 0.02 + 0.02, 0, 0.06)]),
             xo=0, yo=0, resize=True, zorder=0)


def poly(pts, **kw):
    ax.add_patch(Polygon(pts, closed=True, **kw))


def rect(x0, x1, y0, y1, **kw):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))


def smooth(pts, n=200):
    pts = np.asarray(pts, float)
    t = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    tt = np.linspace(0, t[-1], n)
    # Catmull-Rom-ish via cubic interpolation of each coordinate
    from numpy.polynomial import polynomial as P  # noqa
    xs = np.interp(tt, t, pts[:, 0]); ys = np.interp(tt, t, pts[:, 1])
    k = 9
    ker = np.ones(k) / k
    xs = np.r_[xs[:k//2], np.convolve(xs, ker, "valid"), xs[-(k//2):]]
    ys = np.r_[ys[:k//2], np.convolve(ys, ker, "valid"), ys[-(k//2):]]
    return xs, ys


def road(pts, w, label=None, lpos=0.5, lsize=12, lrot=None, loff=0):
    xs, ys = smooth(pts)
    lw = w * 0.30  # points per foot at this scale (approx)
    ax.plot(xs, ys, color=INK_SOFT, lw=lw + 2.2, solid_capstyle="butt", zorder=2)
    ax.plot(xs, ys, color=ROAD, lw=lw, solid_capstyle="butt", zorder=2.1)
    if label:
        i = int(lpos * (len(xs) - 1))
        dx, dy = xs[i + 3] - xs[i - 3], ys[i + 3] - ys[i - 3]
        ang = np.degrees(np.arctan2(dy, dx)) if lrot is None else lrot
        if ang > 90: ang -= 180
        if ang < -90: ang += 180
        ax.text(xs[i], ys[i] + loff, label, rotation=ang, rotation_mode="anchor",
                ha="center", va="center", fontsize=lsize, family=SERIF, style="italic",
                color=INK, zorder=6)
    return xs, ys


def trees(xs, ys, r=14, color="#6f7d47", jitter=4):
    for x, y in zip(xs, ys):
        x += rng.normal(0, jitter); y += rng.normal(0, jitter)
        rr = r * rng.uniform(0.85, 1.15)
        ax.add_patch(Circle((x, y), rr, fc=color, ec=INK, lw=0.5, alpha=0.9, zorder=4))
        ax.add_patch(Circle((x - rr * 0.3, y + rr * 0.3), rr * 0.35, fc="#93a062", ec="none",
                            alpha=0.8, zorder=4.1))


def hall(x0, x1, y0, y1, label=None, lsize=9.5, rot=0):
    rect(x0, x1, y0, y1, fc=HALL, ec=INK, lw=1.0, hatch="////", zorder=5)
    rect(x0, x1, y0, y1, fc="none", ec=INK, lw=1.2, zorder=5.1)
    if label:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, label, ha="center", va="center", fontsize=lsize,
                family=SERIF, color=INK, rotation=rot, zorder=7,
                path_effects=[pe.withStroke(linewidth=3.5, foreground=HALL)])


# ---------------- ground ----------------
# general campus grounds between the roads
ground = [(560, 0), (380, 270), (150, 430), (-300, 570), (-900, 705), (-1450, 815),
          (-1450, -775), (-900, -690), (-300, -570), (150, -440), (380, -270)]
poly(ground, fc="#e2dcb8", ec="none", zorder=1)

# ---------------- roads ----------------
road([(560, 0), (1100, 0)], 95)
ax.text(830, 0, "DUKE OF GLOUCESTER STREET", ha="center", va="center", fontsize=11.5,
        family=SERIF, color=INK, zorder=6)
road([(560, 0), (380, 270), (150, 430), (-300, 570), (-900, 705), (-1450, 815)], 55,
     "Richmond Road", lpos=0.62, lsize=13, loff=0)
road([(560, 0), (380, -270), (150, -440), (-300, -570), (-900, -690), (-1450, -775)], 55,
     "Jamestown Road", lpos=0.62, lsize=13, loff=0)
ax.text(615, 95, "College\nCorner", ha="left", va="bottom", fontsize=10.5, family=SERIF,
        style="italic", color=INK_SOFT, zorder=6, linespacing=0.95)

# Merchants Square (east, schematic blocks)
for (x0, x1, y0, y1) in [(640, 760, 70, 190), (790, 940, 70, 170), (640, 780, -190, -70),
                          (810, 960, -175, -70)]:
    rect(x0, x1, y0, y1, fc="#d9c7a6", ec=INK_SOFT, lw=0.8, hatch="....", zorder=3)
ax.text(800, 245, "MERCHANTS SQUARE", ha="center", fontsize=9.5, family=SERIF, color=INK_SOFT,
        zorder=6)
ax.annotate("", xy=(1040, -40), xytext=(930, -40),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=1.2), zorder=6)
ax.text(985, -60, "to the Capitol, ~1 mile", ha="center", va="top", fontsize=9, family=SERIF,
        style="italic", color=INK_SOFT, zorder=6)

# ---------------- Wren Yard (the Ancient Campus) ----------------
yard = [(445, 32), (360, 228), (130, 365), (-40, 300), (-40, -300), (130, -370), (360, -232),
        (445, -32)]
poly(yard, fc=LAWN, ec="none", zorder=2.5)
# brick wall with gate gap
wall_n = np.array([(445, 32), (360, 228), (130, 365), (-40, 300)])
wall_s = np.array([(445, -32), (360, -232), (130, -370), (-40, -300)])
for w in (wall_n, wall_s):
    ax.plot(w[:, 0], w[:, 1], color=BRICK_DK, lw=3.2, zorder=3)
    ax.plot(w[:, 0], w[:, 1], color=BRICK, lw=1.6, zorder=3.1)
for y in (32, -32):
    ax.add_patch(Rectangle((438, y - 7), 14, 14, fc=BRICK, ec=BRICK_DK, lw=1, zorder=3.2))

# walks
walk = dict(color="#e8dcc0", lw=6, solid_capstyle="round", zorder=3.3)
edge = dict(color=INK_SOFT, lw=7.6, solid_capstyle="round", zorder=3.25)
for seg in [[(445, 0), (33, 0)], [(235, 0), (235, 150)], [(235, 0), (235, -150)]]:
    s = np.array(seg); ax.plot(s[:, 0], s[:, 1], **edge); ax.plot(s[:, 0], s[:, 1], **walk)
# yard trees
trees([380, 330, 300, 380, 330, 300, 140, 90, 140, 90],
      [130, 175, 230, -130, -175, -230, 255, 205, -255, -205], r=17)

# Wren Building — U plan: main block + Great Hall (N) and Chapel (S) wings to the west
wren = [(25, 70), (25, -70), (-25, -70), (-25, -72), (-95, -72), (-95, -40), (-25, -40),
        (-25, 40), (-95, 40), (-95, 72), (-25, 72), (-25, 70)]
wren = [(25, 72), (25, -72), (-95, -72), (-95, -40), (-25, -40), (-25, 40), (-95, 40),
        (-95, 72)]
poly(wren, fc=BRICK, ec=BRICK_DK, lw=1.6, zorder=5)
rect(25, 34, -13, 13, fc=BRICK, ec=BRICK_DK, lw=1.2, zorder=5)   # entrance porch
ax.add_patch(Circle((0, 0), 6, fc=PAPER, ec=BRICK_DK, lw=1.0, zorder=5.2))  # cupola
ax.text(-60, 56, "Great Hall", fontsize=7.5, family=SERIF, style="italic", color=PAPER,
        ha="center", va="center", zorder=6)
ax.text(-60, -56, "Chapel", fontsize=7.5, family=SERIF, style="italic", color=PAPER,
        ha="center", va="center", zorder=6)

# President's House (N) and Brafferton (S) facing each other across the yard
rect(205, 268, 150, 195, fc=BRICK, ec=BRICK_DK, lw=1.6, zorder=5)
rect(210, 262, -190, -150, fc=BRICK, ec=BRICK_DK, lw=1.6, zorder=5)


def label(x, y, txt, size=12, color=INK, ha="center", va="center", style="normal",
          weight="normal", halo=PAPER, family=SERIF, **kw):
    ax.text(x, y, txt, fontsize=size, family=family, color=color, ha=ha, va=va, style=style,
            weight=weight, zorder=8, path_effects=[pe.withStroke(linewidth=4, foreground=halo)],
            **kw)


label(-35, 112, "WREN BUILDING", size=13.5, weight="bold")
label(-35, 89, "begun 1695", size=9, style="italic", color=INK_SOFT)
label(236, 222, "PRESIDENT'S HOUSE", size=11, weight="bold")
label(236, 204, "1732", size=9, style="italic", color=INK_SOFT, halo=LAWN)
label(236, -217, "THE BRAFFERTON", size=11, weight="bold")
label(236, -235, "1723", size=9, style="italic", color=INK_SOFT, halo=LAWN)
label(235, 85, "Wren Yard", size=13, style="italic", halo=LAWN, family=SERIF2)

# Botetourt statue
ax.add_patch(Circle((112, 0), 9, fc=PAPER, ec=INK, lw=1.2, zorder=5))
ax.add_patch(Circle((112, 0), 3.5, fc=INK, ec="none", zorder=5.1))
label(112, -26, "Botetourt\nstatue", size=8, style="italic", color=INK_SOFT, halo=LAWN,
      linespacing=0.9)

# ---------------- Sunken Garden ----------------
SG_X0, SG_X1, SG_Y = -1010, -190, 92
# terrace (upper lawn)
rect(SG_X0 - 40, SG_X1 + 10, -SG_Y - 70, SG_Y + 70, fc=LAWN, ec="none", zorder=2.5)
# the sunken lawn, with slope hachures
rect(SG_X0, SG_X1, -SG_Y, SG_Y, fc=SUNK, ec=INK, lw=1.0, zorder=3)
for x in np.arange(SG_X0 + 6, SG_X1, 12):
    ax.plot([x, x], [SG_Y, SG_Y - 11], color=INK_SOFT, lw=0.6, zorder=3.1)
    ax.plot([x, x], [-SG_Y, -SG_Y + 11], color=INK_SOFT, lw=0.6, zorder=3.1)
for y in np.arange(-SG_Y + 6, SG_Y, 12):
    ax.plot([SG_X0, SG_X0 + 11], [y, y], color=INK_SOFT, lw=0.6, zorder=3.1)
    ax.plot([SG_X1, SG_X1 - 11], [y, y], color=INK_SOFT, lw=0.6, zorder=3.1)
# walk from the back of the Wren to the Sunken Garden + flanking walks
for seg in [[(-95, 0), (SG_X1 + 10, 0)],
            [(SG_X1 + 10, 140), (SG_X0 - 40, 140)], [(SG_X1 + 10, -140), (SG_X0 - 40, -140)],
            [(SG_X1 + 10, 140), (SG_X1 + 10, -140)]]:
    s = np.array(seg); ax.plot(s[:, 0], s[:, 1], **edge); ax.plot(s[:, 0], s[:, 1], **walk)
# Jefferson statue behind the Wren
ax.add_patch(Circle((-130, 0), 8, fc=PAPER, ec=INK, lw=1.2, zorder=5))
ax.add_patch(Circle((-130, 0), 3, fc=INK, ec="none", zorder=5.1))
label(-150, -24, "Jefferson\nstatue", size=8, style="italic", color=INK_SOFT, halo=LAWN,
      linespacing=0.9)
# allées of trees
tx = np.arange(SG_X0 + 10, SG_X1, 52)
trees(tx, np.full_like(tx, 116.0), r=13)
trees(tx, np.full_like(tx, -116.0), r=13)
ax.text((SG_X0 + SG_X1) / 2, 18, "THE SUNKEN GARDEN", ha="center", va="center", fontsize=19,
        family=SERIF, color=INK, zorder=8,
        path_effects=[pe.withStroke(linewidth=4, foreground=SUNK)])
ax.text((SG_X0 + SG_X1) / 2, -22, "laid out 1920s, after the Bodleian Plate garden",
        ha="center", va="center", fontsize=9.5, family=SERIF, style="italic", color=INK_SOFT,
        zorder=8, path_effects=[pe.withStroke(linewidth=3, foreground=SUNK)])

# ---------------- Old Campus halls (schematic) ----------------
hall(-330, -205, 178, 262, "Tucker\nHall")
hall(-530, -400, 178, 250)
hall(-730, -600, 178, 250)
hall(-940, -800, 178, 250)
hall(-330, -205, -262, -178, "Ewell\nHall")
hall(-530, -400, -250, -178)
hall(-730, -600, -250, -178)
hall(-940, -800, -250, -178)
hall(-1135, -1065, -150, 150)            # hall closing the west end
# second row toward the roads
hall(-470, -350, 330, 410); hall(-700, -560, 360, 440); hall(-980, -840, 420, 500)
hall(-470, -350, -410, -330); hall(-720, -590, -440, -360)
# trees on the margins
for _ in range(70):
    x = rng.uniform(-1380, -60); y = rng.choice([-1, 1]) * rng.uniform(290, 640)
    lim = 0.215 * abs(x) + 520 if x < -300 else 0.32 * abs(x) + 470
    if abs(y) < min(lim, 0.22 * abs(x) + 470) - 40:
        trees([x], [y], r=rng.uniform(10, 16), color="#7d8a52", jitter=0)

# ---------------- Crim Dell ----------------
dell = [(-1230, -380), (-1180, -330), (-1100, -320), (-1040, -345), (-990, -330), (-955, -365),
        (-985, -420), (-1060, -430), (-1120, -470), (-1200, -455), (-1245, -420)]
xs, ys = smooth(dell + [dell[0]], 120)
trees(rng.uniform(-1300, -900, 22), rng.uniform(-560, -270, 22), r=15, color="#6c7a43")
ax.fill(xs, ys, fc=WATER, ec=INK, lw=1.2, zorder=4.5)
for k in range(1, 4):  # ripple lines
    ax.plot(-1100 + (xs + 1100) * (1 - k * 0.2), -390 + (ys + 390) * (1 - k * 0.2),
            color="#7f9a95", lw=0.7, zorder=4.6)
# the bridge
bx = np.linspace(-1085, -1045, 30); by = -330 - 95 * (bx - bx[0]) / 40
ax.plot(bx, by, color=INK, lw=5, solid_capstyle="butt", zorder=4.8)
ax.plot(bx, by, color="#d9c3a0", lw=3, solid_capstyle="butt", zorder=4.9)
label(-1100, -515, "CRIM DELL", size=13, weight="bold")
label(-1100, -540, "and its bridge", size=9, style="italic", color=INK_SOFT)

ax.annotate("", xy=(-1395, 0), xytext=(-1215, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=1.2), zorder=6)
label(-1300, 26, "to New Campus\n& Swem Library", size=9, style="italic", color=INK_SOFT,
      halo="#e2dcb8", linespacing=0.95)

# ---------------- neatline, compass, scale ----------------
for inset, lw in ((0, 2.4), (14, 0.8)):
    ax.add_patch(Rectangle((XMIN + inset, YMIN + inset), XMAX - XMIN - 2 * inset,
                           YMAX - YMIN - 2 * inset, fc="none", ec=INK, lw=lw, zorder=10,
                           clip_on=False))

# compass rose (north approximately up; plan is schematic)
cx, cy, R = 820, 560, 120
for ang, length, col in [(90, R, INK), (270, R, INK), (0, R * .8, INK), (180, R * .8, INK),
                         (45, R * .45, INK_SOFT), (135, R * .45, INK_SOFT),
                         (225, R * .45, INK_SOFT), (315, R * .45, INK_SOFT)]:
    a = np.radians(ang); w = np.radians(90)
    tip = (cx + length * np.cos(a), cy + length * np.sin(a))
    l = (cx + 0.14 * length * np.cos(a + w), cy + 0.14 * length * np.sin(a + w))
    r = (cx + 0.14 * length * np.cos(a - w), cy + 0.14 * length * np.sin(a - w))
    poly([(cx, cy), l, tip], fc=col, ec=INK, lw=0.7, zorder=9)
    poly([(cx, cy), r, tip], fc=PAPER, ec=INK, lw=0.7, zorder=9)
ax.add_patch(Circle((cx, cy), R * 0.62, fc="none", ec=INK, lw=0.8, zorder=9))
ax.add_patch(Circle((cx, cy), R * 0.56, fc="none", ec=INK, lw=0.4, zorder=9))
ax.text(cx, cy + R + 14, "N", ha="center", va="bottom", fontsize=16, family=SERIF, color=INK,
        zorder=9)

# scale bar
sx, sy = 560, -690
for i, (a, b) in enumerate([(0, 100), (100, 200), (200, 300), (300, 400)]):
    rect(sx + a, sx + b, sy, sy + 14, fc=INK if i % 2 == 0 else PAPER, ec=INK, lw=0.9, zorder=9)
for v in (0, 100, 200, 400):
    ax.text(sx + v, sy + 24, f"{v}", ha="center", va="bottom", fontsize=9, family=SERIF,
            color=INK, zorder=9)
ax.text(sx + 420, sy + 7, "feet", ha="left", va="center", fontsize=9, family=SERIF,
        style="italic", color=INK, zorder=9)
ax.text(sx + 200, sy - 18, "approximate scale", ha="center", va="top", fontsize=8.5,
        family=SERIF, style="italic", color=INK_SOFT, zorder=9)

# legend
lx, ly = 560, -380
ax.text(lx, ly + 40, "REFERENCES", fontsize=10.5, family=SERIF, color=INK, zorder=9)
items = [("brick", "Colonial buildings, 1695–1732"), ("hall", "Old Campus halls (schematic)"),
         ("sunk", "Sunken lawn"), ("wall", "Yard wall & gate")]
for i, (kind, txt) in enumerate(items):
    y = ly - i * 48
    if kind == "brick":
        rect(lx, lx + 50, y - 12, y + 12, fc=BRICK, ec=BRICK_DK, lw=1.2, zorder=9)
    elif kind == "hall":
        rect(lx, lx + 50, y - 12, y + 12, fc=HALL, ec=INK, lw=1, hatch="////", zorder=9)
    elif kind == "sunk":
        rect(lx, lx + 50, y - 12, y + 12, fc=SUNK, ec=INK, lw=0.9, zorder=9)
    else:
        ax.plot([lx, lx + 50], [y, y], color=BRICK_DK, lw=3.2, zorder=9)
        ax.plot([lx, lx + 50], [y, y], color=BRICK, lw=1.6, zorder=9.1)
    ax.text(lx + 66, y, txt, va="center", fontsize=10, family=SERIF, color=INK, zorder=9)

# ---------------- titling ----------------
fig.text(0.5, 0.945, "The Old Campus", ha="center", va="center", fontsize=46, family=SERIF,
         color=INK)
fig.text(0.5, 0.893, "THE COLLEGE OF WILLIAM & MARY IN VIRGINIA  ·  WILLIAMSBURG  ·  CHARTERED 1693",
         ha="center", va="center", fontsize=13, family=SERIF, color=INK_SOFT)
fig.lines.append(plt.Line2D([0.33, 0.67], [0.869, 0.869], transform=fig.transFigure, color=INK,
                            lw=0.8))
fig.text(0.045, 0.035,
         "#30DayMapChallenge · Day 10, alternate prompt  ·  Drawn from memory by Claude, without "
         "survey data. Positions & footprints approximate; unlabeled halls are schematic.",
         ha="left", va="center", fontsize=9.5, family=SERIF, style="italic", color=INK_SOFT)
fig.text(0.955, 0.035, "Map: Jack Zamary", ha="right", va="center", fontsize=9.5,
         family=SERIF, color=INK_SOFT)

fig.savefig("/home/claude/wm_old_campus_day10.png", facecolor=PAPER, dpi=200)
print("saved")
