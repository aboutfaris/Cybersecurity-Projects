#!/usr/bin/env python3
"""Cybersecurity Set: high-level Cloud SOC architecture diagram.

Built from the reference architecture-diagram layout (one cloud boundary, an aligned
grid of unfilled dashed groups, official icons on a shared slot grid, right-angle
lines with no crossings, numbered steps with a plain-English legend), adapted for
Azure: official Azure icons from the `diagrams` package, plain stroke-only glyphs
where no official icon exists, and no company branding.

Every group is labeled with the repo folder it comes from (02 to 07), so a reader
can map the picture to the guides.

Set up once:  python3 -m venv /tmp/c340_diag_venv
              /tmp/c340_diag_venv/bin/pip install diagrams     (official Azure icons)
              brew install librsvg                              (rsvg-convert)
Run:          /tmp/c340_diag_venv/bin/python architecture_diagram.py assets/architecture
It writes <out>.svg and <out>.png and must print "layout problems: none".
"""
import base64
import os
import subprocess
import sys

import diagrams

R = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/arch"
OUT_SVG, OUT_PNG = OUT + ".svg", OUT + ".png"

# ---------------- style ----------------
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, TEXT2, LINE, GROUP, BADGE, RULE, ACCENT = (
    "#232F3E", "#545B64", "#3F4752", "#7D8998", "#146EB4", "#E3E6EA", "#8C4FFF")
ICON, HALF = 52, 26
ZOOM = 1  # PNG width = W * ZOOM; keeps the image near GitHub README width
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "Log or data flow in Azure"),
    "external": (LINE, 1.6, "6 5", "ah", "Attack traffic"),
    "business": (ACCENT, 2.2, None, "ahb", "Incident response"),
}

# ---------------- canvas text ----------------
W, H = 1600, 1200
TITLE = "Cybersecurity Set | Cloud SOC Architecture in Azure"
SUBTITLE = ("Exposed lab resources send logs to Log Analytics, Microsoft Sentinel turns them "
            "into maps and incidents, and hardening shuts the attacks out.")
CLOUD, REGION = "Microsoft Azure", "lab subscription, East US 2"

out, icons, SEGS, BADGES = [], [], [], []
N, BOX, USED = {}, {}, set()


def add(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def est_w(s, size):
    return len(s) * size * 0.53


def text(x, y, s, size=13, weight=400, color=INK, anchor="middle", halo=False):
    h = (' stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
         if halo else "")
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{h}>{esc(s)}</text>')


_cache = {}


def data(rel):
    if rel not in _cache:
        with open(os.path.join(R, rel), "rb") as fh:
            _cache[rel] = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
    return _cache[rel]


def glyph(kind, cx, cy):
    """Stroke-only outline glyph (no fill) for parts with no official icon."""
    x, y = cx - HALF, cy - HALF
    st = f'fill="none" stroke="{LINE}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"'
    if kind == "globe":  # internet
        add(f'<circle cx="{cx}" cy="{cy}" r="22" {st}/>')
        add(f'<ellipse cx="{cx}" cy="{cy}" rx="10" ry="22" {st}/>')
        add(f'<path d="M {cx-22},{cy} L {cx+22},{cy} M {cx-19},{cy-11} L {cx+19},{cy-11} '
            f'M {cx-19},{cy+11} L {cx+19},{cy+11}" {st}/>')
    elif kind == "rules":  # list of detection rules
        add(f'<rect x="{x+8}" y="{y+4}" width="36" height="44" rx="3" {st}/>')
        for i in range(4):
            yy = y + 15 + i * 9
            add(f'<path d="M {x+15},{yy} L {x+18},{yy+3} L {x+23},{yy-3} M {x+27},{yy} '
                f'L {x+38},{yy}" {st}/>')
    elif kind == "incident":  # warning triangle
        add(f'<path d="M {cx},{y+5} L {x+48},{y+46} L {x+4},{y+46} Z" {st}/>')
        add(f'<path d="M {cx},{y+20} L {cx},{y+33}" {st}/>')
        add(f'<circle cx="{cx}" cy="{y+39}" r="1.6" fill="{LINE}"/>')
    elif kind == "table":  # watchlist table
        add(f'<rect x="{x+4}" y="{y+8}" width="44" height="36" rx="3" {st}/>')
        add(f'<path d="M {x+4},{y+20} L {x+48},{y+20} M {x+4},{y+32} L {x+48},{y+32} '
            f'M {x+20},{y+8} L {x+20},{y+44}" {st}/>')
    elif kind == "book":  # playbook
        add(f'<path d="M {cx},{y+10} C {cx-8},{y+5} {x+12},{y+5} {x+4},{y+8} L {x+4},{y+44} '
            f'C {x+12},{y+41} {cx-8},{y+41} {cx},{y+46} C {cx+8},{y+41} {x+40},{y+41} '
            f'{x+48},{y+44} L {x+48},{y+8} C {x+40},{y+5} {cx+8},{y+5} {cx},{y+10} Z '
            f'M {cx},{y+10} L {cx},{y+46}" {st}/>')
    elif kind == "desktop":  # desktop PC
        add(f'<rect x="{x+3}" y="{y+6}" width="46" height="31" rx="3" {st}/>')
        add(f'<path d="M {cx-6},{y+37} L {cx-8},{y+45} M {cx+6},{y+37} L {cx+8},{y+45} '
            f'M {cx-15},{y+46} L {cx+15},{y+46}" {st}/>')
    elif kind == "scan":  # vulnerability scanner
        add(f'<circle cx="{cx-5}" cy="{cy-5}" r="15" {st}/>')
        add(f'<path d="M {cx+6},{cy+6} L {cx+21},{cy+21} M {cx-12},{cy-5} L {cx+2},{cy-5}" {st}/>')
    elif kind == "script":  # PowerShell scripts
        add(f'<rect x="{x+3}" y="{y+8}" width="46" height="36" rx="3" {st}/>')
        add(f'<path d="M {x+11},{y+18} L {x+19},{y+26} L {x+11},{y+34} M {x+23},{y+34} '
            f'L {x+37},{y+34}" {st}/>')
    elif kind == "chart":  # before and after metrics
        add(f'<path d="M {x+4},{y+6} L {x+4},{y+46} L {x+48},{y+46}" {st}/>')
        add(f'<rect x="{x+12}" y="{y+12}" width="10" height="34" {st}/>')
        add(f'<rect x="{x+32}" y="{y+42}" width="10" height="4" {st}/>')
    else:
        raise ValueError(kind)


def node(key, rel, cx, cy, l1, l2=None):
    """Register an icon (official PNG, or 'glyph:<kind>') at slot (cx, cy) with labels."""
    assert key not in N, key
    N[key] = (cx, cy, 2 if l2 else 1)
    icons.append((rel, cx, cy, l1, l2))
    w = max(ICON, est_w(l1, 13), est_w(l2 or "", 12))
    BOX[key] = (cx - w / 2, cy - HALF, cx + w / 2, cy + HALF + (36 if l2 else 21))


def draw_nodes():
    for rel, cx, cy, l1, l2 in icons:
        if rel.startswith("glyph:"):
            glyph(rel[6:], cx, cy)
        else:
            add(f'<image x="{cx-HALF}" y="{cy-HALF}" width="{ICON}" height="{ICON}" '
                f'xlink:href="{data(rel)}"/>')
        text(cx, cy + HALF + 17, l1, 13, 400, INK)
        if l2:
            text(cx, cy + HALF + 32, l2, 12, 400, TEXT2)


def port(key, side, gap=5):
    """Connection point: l, r, t (top edge of icon), b (below the label block)."""
    cx, cy, n = N[key]
    return {"l": (cx - HALF - gap, cy), "r": (cx + HALF + gap, cy),
            "t": (cx, cy - HALF - gap),
            "b": (cx, cy + HALF + (36 if n == 2 else 21) + gap)}[side]


def path(pts, a, b, kind="service"):
    color, width, dash, marker, _ = KINDS[kind]
    USED.add(kind)
    for p, q in zip(pts, pts[1:]):
        assert p[0] == q[0] or p[1] == q[1], ("diagonal segment", a, b, p, q)
        SEGS.append((p, q, a, b))
    d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} '
        f'marker-end="url(#{marker})"/>')


def link(a, sa, b, sb, kind="service", via=None, end=None):
    """Connect two nodes. via = elbow points; end overrides the target point."""
    path([port(a, sa)] + (via or []) + [end or port(b, sb)], a, b, kind)


def badge(cx, cy, n, record=True):
    if record:
        BADGES.append((cx, cy, n))
    add(f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="{BADGE}"/>')
    text(cx, cy + 4.6, str(n), 13, 700, "#FFFFFF")


def group(x0, y0, x1, y1, title):
    add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" '
        f'stroke="{GROUP}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    text(x0 + 14, y0 + 25, title, 14.5, 700, INK, "start")


# ---------------- grid ----------------
AX0, AX1, AY0, AY1 = 165, 1575, 110, 785             # Azure boundary
COLS = [(190, 623), (653, 1086), (1116, 1549)]        # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
R0, R1, RT, R2 = (150, 440), (470, 760), (150, 760), (820, 960)   # rows (RT = tall)
A1, B1, A2, B2, C = 225, 350, 545, 650, 870           # icon lanes (center y)
XL = 85                                               # external column

# ---------------- canvas and Azure boundary ----------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs>'
    '<marker id="ah" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6.5" '
    f'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
    '<marker id="ahb" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" '
    f'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
text(40, 52, TITLE, 26, 700, INK, "start")
text(40, 78, SUBTITLE, 14, 400, TEXT2, "start")
add(f'<rect x="{AX0}" y="{AY0}" width="{AX1-AX0}" height="{AY1-AY0}" fill="none" '
    f'stroke="{INK}" stroke-width="1.6"/>')
add(f'<image x="{AX0+6}" y="{AY0+5}" width="24" height="24" xlink:href="{data("azure/azure.png")}"/>')
add(f'<text x="{AX0+38}" y="{AY0+22}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">{esc(CLOUD)}<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(REGION)}</tspan></text>')

# ---------------- groups: (x0, x1), (y0, y1) -> folder number and title ----------------
for (x0, x1), (y0, y1), title in [
    (COLS[0], R0, "02 Cloud SOC Pre-requisites"),
    (COLS[0], R1, "05 Secure Cloud Configuration"),
    (COLS[1], RT, "03 Logging and Monitoring"),
    (COLS[2], RT, "04 Microsoft Sentinel SIEM"),
    (COLS[0], R2, "06 Vulnerability Management"),
    (COLS[1], R2, "01 Cloud SOC Project Summary"),
    (COLS[2], R2, "07 IR-Playbooks"),
]:
    group(x0, y0, x1, y1, title)
text(AX0, R2[0] - 6, "Outside Azure", 12, 400, TEXT2, "start")

# ---------------- nodes ----------------
AZ = "azure/"
NSG = AZ + "network/network-security-groups-classic.png"

node("attackers", "glyph:globe", XL, A1, "Attackers", "internet, attack-vm")
# 02 exposed lab
node("nsg", NSG, SL[0][0], A1, "VM NSGs", "allow all inbound")
node("winvm", AZ + "compute/vm-windows.png", SL[0][1], A1, "windows-vm", "SQL Server, RDP")
node("linvm", AZ + "compute/vm-linux.png", SL[0][1], B1, "linux-vm", "Ubuntu, SSH")
node("aad", AZ + "identity/azure-active-directory.png", SL[0][2], B1, "Azure AD", "users, RBAC")
# 05 hardening
node("subnsg", NSG, SL[0][0], B2, "Subnet NSG", "locked down")
node("pe", AZ + "network/private-endpoint.png", SL[0][1], A2, "Private endpoints", "in Lab-VNet")
node("kv", AZ + "security/key-vaults.png", SL[0][2], A2, "Key Vault", "public access off")
node("sa", AZ + "storage/storage-accounts.png", SL[0][2], B2, "Storage account", "public access off")
# 03 logging
node("law", AZ + "monitor/log-analytics-workspaces.png", SL[1][1], B1,
     "Log Analytics", "one workspace")
node("defender", AZ + "security/microsoft-defender-for-cloud.png", SL[1][1], A2,
     "Defender for Cloud", "secure score, export")
# 04 Sentinel
node("sentinel", AZ + "security/sentinel.png", SL[2][1], B1, "Microsoft Sentinel", "SIEM")
node("workbooks", AZ + "monitor/azure-workbooks.png", SL[2][1], A1, "Workbooks", "4 attack maps")
node("rules", "glyph:rules", SL[2][2], B1, "Analytics rules", "KQL detections")
node("incidents", "glyph:incident", SL[2][2], A2, "Incidents", "NIST 800-61")
node("watch", "glyph:table", SL[2][1], B2, "GeoIP watchlists", "loaded in 03")
# outside Azure
node("desktop", "glyph:desktop", SL[0][0], C, "Windows 11 desktop", "HardenTools")
node("nessus", "glyph:scan", SL[0][2], C, "Nessus scan", "fix medium findings")
node("scripts", "glyph:script", SL[1][0], C, "Attack scripts", "PowerShell")
node("metrics", "glyph:chart", SL[1][2], C, "24-hour metrics", "before vs after")
node("playbooks", "glyph:book", SL[2][2], C, "IR playbooks", "6 incident types")

# ---------------- connections ----------------
link("attackers", "r", "nsg", "l", "external")
link("attackers", "b", "subnsg", "l", "external", via=[(XL, B2)])
link("nsg", "r", "winvm", "l")
link("nsg", "b", "linvm", "l", via=[(SL[0][0], B1)])
link("pe", "r", "kv", "l")
link("pe", "b", "sa", "l", via=[(SL[0][1], B2)])
link("winvm", "r", "law", "t", via=[(SL[1][1], A1)])
link("aad", "r", "law", "l")
KVX = 780
link("kv", "r", "law", "l", via=[(KVX, A2), (KVX, B1 + 14)],
     end=(SL[1][1] - HALF - 5, B1 + 14))
link("defender", "t", "law", "b")
link("law", "r", "sentinel", "l")
link("sentinel", "t", "workbooks", "b")
link("sentinel", "r", "rules", "l")
link("rules", "b", "incidents", "t")
link("watch", "t", "sentinel", "b")
link("sa", "r", "watch", "l")
link("incidents", "b", "playbooks", "t", "business")
link("nessus", "l", "desktop", "r")

# ---------------- line labels (white halo keeps them readable over lines) ----------------
LBL = 11.5
text(SL[1][0], A1 - 8, "VM, SQL, NSG flow logs", LBL, 400, TEXT2, "middle", halo=True)
text(SL[1][0], B1 - 8, "sign-in, audit logs", LBL, 400, TEXT2, "middle", halo=True)
text(706, A2 - 8, "vault logs", LBL, 400, TEXT2, "middle", halo=True)
text(SL[1][1] + 8, 470, "recommendations", LBL, 400, TEXT2, "start", halo=True)
text(1200, B1 - 8, "queries", LBL, 400, TEXT2, "middle", halo=True)
text(1000, B2 - 8, "GeoIP CSVs", LBL, 400, TEXT2, "middle", halo=True)
text(XL + 6, B2 - 8, "blocked", LBL, 400, TEXT2, "start", halo=True)
text(SL[0][1], C - 8, "scans", LBL, 400, TEXT2, "middle", halo=True)
text(SL[2][2] + 8, 700, "worked with", LBL, 400, TEXT2, "start", halo=True)

draw_nodes()

# ---------------- step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(205, 200, 1), (638, 200, 2), (1101, 325, 3), (1505, 470, 4),
                  (1505, 800, 5), (120, 620, 6), (SL[0][1], C + 26, 7), (SL[1][1], C, 8)]:
    badge(cx, cy, n)

# ---------------- legend: one short sentence per badge ----------------
LY = 1000
STEPS = [
    "02: Attackers on the internet and the lab attack-vm brute force wide-open NSGs and both VMs.",
    "03: VM, SQL, NSG flow, Azure AD, and Key Vault logs all land in one Log Analytics workspace.",
    "04: Sentinel queries the workspace and joins GeoIP watchlists to draw workbook attack maps.",
    "04: KQL analytics rules raise incidents, worked through the NIST 800-61 lifecycle.",
    "07: Each incident type has a playbook: account, critical, data loss, malware, phishing, ransom.",
    "05: NSG lockdown and private endpoints for Key Vault and Storage shut the attackers out.",
    "06: Separately, a Windows 11 desktop is hardened, scanned with Nessus, and fixed.",
    "01: The summary compares 24 hours before and after hardening; every count drops to zero.",
]

text(40, LY, "How it works", 16, 700, INK, "start")
per_col = (len(STEPS) + 1) // 2
for i, s in enumerate(STEPS):
    col, row = divmod(i, per_col)
    bx, by = 52 + col * 780, LY + 32 + row * 30
    badge(bx, by, i + 1, record=False)
    text(bx + 22, by + 4.6, s, 13.5, 400, INK, "start")

# line-style key, one entry per line kind actually used
KEY_Y = LY + 36 + per_col * 30
lx = 40
for k, (color, width, dash, marker, label) in KINDS.items():
    if k not in USED:
        continue
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="M {lx},{KEY_Y} L {lx+52},{KEY_Y}" stroke="{color}" stroke-width="{width}"'
        f'{da} marker-end="url(#{marker})"/>')
    text(lx + 62, KEY_Y + 4.5, label, 12.5, 400, TEXT2, "start")
    lx += 62 + est_w(label, 12.5) + 48
add("</svg>")
assert KEY_Y + 30 <= H, "canvas too short for the legend: raise H"


# ---------------- checks ----------------
def seg_hits_box(p, q, box, pad=2):
    x0, y0, x1, y1 = box
    (ax, ay), (bx, by) = p, q
    if ay == by:
        lo, hi = sorted((ax, bx))
        return y0 - pad < ay < y1 + pad and lo < x1 + pad and hi > x0 - pad
    lo, hi = sorted((ay, by))
    return x0 - pad < ax < x1 + pad and lo < y1 + pad and hi > y0 - pad


def boxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def crossings():
    hs = [s for s in SEGS if s[0][1] == s[1][1]]
    vs = [s for s in SEGS if s[0][0] == s[1][0]]
    found = []
    for hp, hq, ha, hb in hs:
        y = hp[1]
        x0, x1 = sorted((hp[0], hq[0]))
        for vp, vq, va, vb in vs:
            if (ha, hb) == (va, vb):
                continue
            x = vp[0]
            y0, y1 = sorted((vp[1], vq[1]))
            if x0 < x < x1 and y0 < y < y1:
                found.append(f"{ha}->{hb} x {va}->{vb}")
    return found


def shared_segments():
    found = []
    for i in range(len(SEGS)):
        for j in range(i + 1, len(SEGS)):
            (p, q, a, b), (r, s, c, d) = SEGS[i], SEGS[j]
            if (a, b) == (c, d):
                continue
            if p[1] == q[1] == r[1] == s[1]:
                lo1, hi1 = sorted((p[0], q[0]))
                lo2, hi2 = sorted((r[0], s[0]))
            elif p[0] == q[0] == r[0] == s[0]:
                lo1, hi1 = sorted((p[1], q[1]))
                lo2, hi2 = sorted((r[1], s[1]))
            else:
                continue
            if min(hi1, hi2) - max(lo1, lo2) > 0:
                found.append(f"{a}->{b} shares a segment with {c}->{d}")
    return found


problems = []
for p, q, a, b in SEGS:
    for k, box in BOX.items():
        if k not in (a, b) and seg_hits_box(p, q, box):
            problems.append(f"line {a}->{b} crosses {k}")
keys = list(BOX)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        if boxes_overlap(BOX[keys[i]], BOX[keys[j]]):
            problems.append(f"label overlap {keys[i]} / {keys[j]}")
for cx, cy, n in BADGES:
    bb = (cx - 12, cy - 12, cx + 12, cy + 12)
    for p, q, a, b in SEGS:
        if seg_hits_box(p, q, bb, pad=1):
            problems.append(f"badge {n} sits on line {a}->{b}")
    for k, box in BOX.items():
        if boxes_overlap(bb, box):
            problems.append(f"badge {n} overlaps {k}")
for k, (x0, y0, x1, y1) in BOX.items():
    for (c0, c1) in COLS:
        if c0 < (x0 + x1) / 2 < c1 and (x0 < c0 + 4 or x1 > c1 - 4):
            problems.append(f"label of {k} touches its group border")
problems += shared_segments()
X = crossings()
if X:
    problems.append(f"{len(X)} line crossings")

svg = "\n".join(out)
assert "\u2014" not in svg and "\u2013" not in svg, "em or en dash found"
with open(OUT_SVG, "w") as fh:
    fh.write(svg)
subprocess.run(["rsvg-convert", "-z", str(ZOOM), "-o", OUT_PNG, OUT_SVG], check=True)
print("nodes:", len(N), "segments:", len(SEGS), "badges:", len(BADGES))
print("crossings:", len(X), *X)
print("layout problems:", problems if problems else "none")
print("wrote", OUT_SVG, "and", OUT_PNG)
