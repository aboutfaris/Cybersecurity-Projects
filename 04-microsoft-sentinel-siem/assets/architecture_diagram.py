#!/usr/bin/env python3
"""04 Microsoft Sentinel SIEM: section architecture diagram.

Built from the repo-level assets/architecture_diagram.py (one cloud boundary, an aligned
grid of unfilled dashed groups, official Azure icons on a shared slot grid, right-angle
lines with no crossings, numbered steps with a plain-English legend). Every helper and
layout check is the same; only the EDIT blocks (line kinds, canvas text, grid, groups,
nodes, lines, badges, legend) are scoped to this section's README.

Set up once:  python3 -m venv .venv
              .venv/bin/pip install diagrams==0.25.1   (official Azure icons)
              brew install librsvg                                  (rsvg-convert)
Run:          .venv/bin/python architecture_diagram.py assets/architecture
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
ZOOM = 2  # PNG width = W * ZOOM; rendered at 2x for sharpness, GitHub scales it to fit
# ---------------- EDIT: line kinds ----------------
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "Log or data flow in Azure"),
    "external": (LINE, 1.6, "6 5", "ah", "Attack traffic"),
    "business": (ACCENT, 2.2, None, "ahb", "Incident response"),
}

# ---------------- EDIT: canvas text ----------------
W, H = 1600, 1230
TITLE = "04 Microsoft Sentinel SIEM | Maps, Rules, and Incidents"
SUBTITLE = ("Attack traffic lands in the workspace, Sentinel draws attack maps and raises incidents "
            "from KQL rules, and each incident is worked with NIST 800-61.")
CLOUD, REGION = "Microsoft Azure", "lab subscription, East US 2"
TILE = "azure"

# ---------------- EDIT: grid ----------------
AX0, AX1, AY0, AY1 = 165, 1575, 110, 985             # cloud boundary
COLS = [(190, 623), (653, 1086), (1116, 1549)]        # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
R0, R1, RT, R2 = (150, 440), (470, 760), (150, 760), (790, 960)   # rows (RT = tall)
A1, B1, A2, B2, A3 = 225, 335, 545, 650, 870          # icon lanes (center y)
XL = 85                                               # external column

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
    elif kind == "doc":  # event log or document
        add(f'<path d="M {x+10},{y+4} L {x+34},{y+4} L {x+44},{y+14} L {x+44},{y+48} L {x+10},{y+48} Z '
            f'M {x+34},{y+4} L {x+34},{y+14} L {x+44},{y+14}" {st}/>')
        add(f'<path d="M {x+17},{y+24} L {x+37},{y+24} M {x+17},{y+32} L {x+37},{y+32} '
            f'M {x+17},{y+40} L {x+31},{y+40}" {st}/>')
    elif kind == "viewer":  # log viewer window
        add(f'<rect x="{x+3}" y="{y+7}" width="46" height="38" rx="3" {st}/>')
        add(f'<path d="M {x+3},{y+16} L {x+49},{y+16} M {x+18},{y+16} L {x+18},{y+45} '
            f'M {x+23},{y+24} L {x+43},{y+24} M {x+23},{y+31} L {x+43},{y+31} '
            f'M {x+23},{y+38} L {x+37},{y+38}" {st}/>')
    elif kind == "shield":  # hardening
        add(f'<path d="M {cx},{y+4} L {x+46},{y+12} L {x+46},{y+26} C {x+46},{y+38} {cx+10},{y+45} '
            f'{cx},{y+49} C {cx-10},{y+45} {x+6},{y+38} {x+6},{y+26} L {x+6},{y+12} Z" {st}/>')
        add(f'<path d="M {cx-9},{cy+1} L {cx-2},{cy+8} L {cx+10},{cy-6}" {st}/>')
    elif kind == "trash":  # debloat
        add(f'<path d="M {x+8},{y+12} L {x+44},{y+12} M {cx-6},{y+12} L {cx-6},{y+6} L {cx+6},{y+6} '
            f'L {cx+6},{y+12} M {x+12},{y+12} L {x+15},{y+48} L {x+37},{y+48} L {x+40},{y+12} '
            f'M {cx-6},{y+20} L {cx-6},{y+40} M {cx+6},{y+20} L {cx+6},{y+40}" {st}/>')
    elif kind == "cert":  # certificate
        add(f'<rect x="{x+3}" y="{y+6}" width="46" height="32" rx="3" {st}/>')
        add(f'<path d="M {x+10},{y+15} L {x+30},{y+15} M {x+10},{y+22} L {x+26},{y+22}" {st}/>')
        add(f'<circle cx="{x+38}" cy="{y+36}" r="6" {st}/>')
        add(f'<path d="M {x+34},{y+41} L {x+32},{y+49} L {x+36},{y+46} M {x+42},{y+41} '
            f'L {x+44},{y+49} L {x+40},{y+46}" {st}/>')
    elif kind == "firewall":  # brick wall
        add(f'<rect x="{x+4}" y="{y+8}" width="44" height="36" {st}/>')
        add(f'<path d="M {x+4},{y+20} L {x+48},{y+20} M {x+4},{y+32} L {x+48},{y+32} '
            f'M {x+19},{y+8} L {x+19},{y+20} M {x+34},{y+8} L {x+34},{y+20} M {x+12},{y+20} '
            f'L {x+12},{y+32} M {x+26},{y+20} L {x+26},{y+32} M {x+40},{y+20} L {x+40},{y+32} '
            f'M {x+19},{y+32} L {x+19},{y+44} M {x+34},{y+32} L {x+34},{y+44}" {st}/>')
    elif kind == "policy":  # policy setting: document with a check
        add(f'<path d="M {x+10},{y+4} L {x+34},{y+4} L {x+44},{y+14} L {x+44},{y+48} L {x+10},{y+48} Z '
            f'M {x+34},{y+4} L {x+34},{y+14} L {x+44},{y+14}" {st}/>')
        add(f'<path d="M {x+18},{y+30} L {x+24},{y+36} L {x+36},{y+23}" {st}/>')
    elif kind == "refresh":  # rebuild and resume
        add(f'<path d="M {x+44},{cy} A 18,18 0 1 1 {x+38},{y+13} M {x+38},{y+5} L {x+38},{y+13} '
            f'L {x+30},{y+13}" {st}/>')
    elif kind == "bulb":  # lessons learned
        add(f'<path d="M {cx-7},{y+38} C {cx-7},{y+30} {x+8},{y+28} {x+8},{y+20} A 18,16 0 0 1 '
            f'{x+44},{y+20} C {x+44},{y+28} {cx+7},{y+30} {cx+7},{y+38} Z M {cx-6},{y+43} '
            f'L {cx+6},{y+43} M {cx-4},{y+48} L {cx+4},{y+48}" {st}/>')
    elif kind == "folder":  # folder of files
        add(f'<path d="M {x+4},{y+12} L {x+20},{y+12} L {x+25},{y+17} L {x+48},{y+17} L {x+48},{y+44} '
            f'L {x+4},{y+44} Z M {x+4},{y+22} L {x+48},{y+22}" {st}/>')
    elif kind == "flow":  # written workflow
        add(f'<rect x="{x+4}" y="{y+4}" width="18" height="12" rx="2" {st}/>')
        add(f'<rect x="{x+30}" y="{y+20}" width="18" height="12" rx="2" {st}/>')
        add(f'<rect x="{x+4}" y="{y+36}" width="18" height="12" rx="2" {st}/>')
        add(f'<path d="M {x+22},{y+10} L {x+39},{y+10} L {x+39},{y+20} M {x+39},{y+32} L {x+39},{y+42} '
            f'L {x+22},{y+42}" {st}/>')
    elif kind == "graph":  # investigation graph
        add(f'<path d="M {cx},{cy} L {x+10},{y+10} M {cx},{cy} L {x+42},{y+12} M {cx},{cy} '
            f'L {x+12},{y+42} M {cx},{cy} L {x+42},{y+40}" {st}/>')
        for px, py, r in ((cx, cy, 7), (x+10, y+10, 4), (x+42, y+12, 4), (x+12, y+42, 4), (x+42, y+40, 4)):
            add(f'<circle cx="{px}" cy="{py}" r="{r}" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.8"/>')
    elif kind == "isolate":  # isolate: box cut off by a bar
        add(f'<rect x="{x+12}" y="{y+12}" width="28" height="28" rx="3" {st}/>')
        add(f'<path d="M {x+4},{cy} L {x+12},{cy} M {x+40},{cy} L {x+48},{cy} M {x+6},{y+4} '
            f'L {x+46},{y+48}" {st}/>')
    elif kind == "person":  # a person at their own computer
        add(f'<circle cx="{cx}" cy="{y+15}" r="9" {st}/>')
        add(f'<path d="M {x+8},{y+48} C {x+8},{y+34} {x+16},{y+28} {cx},{y+28} C {x+36},{y+28} '
            f'{x+44},{y+34} {x+44},{y+48}" {st}/>')
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




def tile(kind, tx, ty):
    """24 px boundary tile: the Azure logo, or a stroke-only glyph scaled down."""
    if kind == "azure":
        add(f'<image x="{tx}" y="{ty}" width="24" height="24" xlink:href="{data("azure/azure.png")}"/>')
        return
    add(f'<g transform="translate({tx},{ty}) scale({24 / ICON})">')
    glyph(kind, HALF, HALF)
    add('</g>')


# ---------------- canvas and cloud boundary ----------------
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
tile(TILE, AX0 + 6, AY0 + 5)
add(f'<text x="{AX0+38}" y="{AY0+22}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">{esc(CLOUD)}<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(REGION)}</tspan></text>')

# ---------------- EDIT: groups ----------------
for (x0, x1), (y0, y1), title in [
    (COLS[0], R0, "Internet-facing VMs"),
    (COLS[0], R1, "Identity, secrets, and attack-vm"),
    (COLS[0], R2, "Containment (Part 5)"),
    (COLS[1], RT, "Log Analytics workspace"),
    (COLS[2], RT, "Microsoft Sentinel"),
    (COLS[2], R2, "NIST 800-61 response (Part 5)"),
]:
    group(x0, y0, x1, y1, title)

# ---------------- EDIT: nodes ----------------
AZ = "azure/"
NSG = AZ + "network/network-security-groups-classic.png"
node("attackers", "glyph:globe", XL, A1, "Attackers", "internet")
node("attackvm", AZ + "compute/vm-windows.png", SL[0][0], A2, "attack-vm", "PowerShell scripts")
node("nsg", NSG, SL[0][0], A1, "VM NSGs", "allow all inbound")
node("winvm", AZ + "compute/vm-windows.png", SL[0][1], A1, "windows-vm", "RDP, SQL Server")
node("linvm", AZ + "compute/vm-linux.png", SL[0][1], B1, "linux-vm", "SSH")
node("aad", AZ + "identity/azure-active-directory.png", SL[0][2], A2, "Azure AD", "sign-ins, roles")
node("kv", AZ + "security/key-vaults.png", SL[0][2], B2, "Key Vault", "secret reads")
node("lockdown", NSG, SL[0][1], A3, "NSG lockdown", "your /32 only")
node("law", AZ + "monitor/log-analytics-workspaces.png", SL[1][1], B1, "Log Analytics", "KQL tables")
node("sentinel", AZ + "security/sentinel.png", SL[2][0], B1, "Microsoft Sentinel", "SIEM")
node("workbooks", AZ + "monitor/azure-workbooks.png", SL[2][0], A1, "Workbooks", "4 attack maps")
node("watch", "glyph:table", SL[2][2], A1, "GeoIP watchlists", "from 03")
node("rules", "glyph:rules", SL[2][2], B1, "Analytics rules", "13 active")
node("incidents", "glyph:incident", SL[2][2], A2, "Incidents", "IP, host entities")
node("investigate", "glyph:graph", SL[2][0], A2, "Investigate", "entity graph")
node("nist", "glyph:flow", SL[2][2], A3, "NIST 800-61", "classify, contain")

# ---------------- EDIT: connections ----------------
LX = SL[1][1] - HALF - 5                              # x of the workspace's left port
link("attackers", "r", "nsg", "l", "external")
link("nsg", "r", "winvm", "l", "external")
link("nsg", "b", "linvm", "l", "external", via=[(SL[0][0], B1)])
link("attackvm", "r", "aad", "l", "external")
link("attackvm", "b", "kv", "l", "external", via=[(SL[0][0], B2)])
link("winvm", "r", "law", "t", via=[(SL[1][1], A1)])
link("linvm", "r", "law", "l")
link("aad", "r", "law", "l", via=[(800, A2), (800, B1 + 14)], end=(LX, B1 + 14))
link("kv", "r", "law", "b", via=[(SL[1][1], B2)])
link("law", "r", "sentinel", "l")
link("sentinel", "t", "workbooks", "b")
link("watch", "l", "workbooks", "r")
link("sentinel", "r", "rules", "l")
link("rules", "b", "incidents", "t")
link("incidents", "l", "investigate", "r")
link("incidents", "b", "nist", "t", "business")
link("nist", "l", "lockdown", "r", "business")

# ---------------- EDIT: line labels (white halo keeps them readable over lines) ----------------
LBL = 11.5
text(530, A1 - 8, "SecurityEvent, Event", LBL, 400, TEXT2, "middle", halo=True)
text(530, B1 - 8, "Syslog", LBL, 400, TEXT2, "middle", halo=True)
text(726, A2 - 8, "SigninLogs, AuditLogs", LBL, 400, TEXT2, "middle", halo=True)
text(760, B2 - 8, "AzureDiagnostics", LBL, 400, TEXT2, "middle", halo=True)
text(1036, B1 - 8, "Sentinel reads", LBL, 400, TEXT2, "middle", halo=True)
text(1333, A1 - 8, "GeoIP join", LBL, 400, TEXT2, "middle", halo=True)
text(1333, B1 - 8, "scheduled KQL", LBL, 400, TEXT2, "middle", halo=True)
text(1333, A2 - 8, "scope", LBL, 400, TEXT2, "middle", halo=True)
text(1000, A3 - 8, "lock each NSG to your /32", LBL, 400, TEXT2, "middle", halo=True)

draw_nodes()

# ---------------- EDIT: step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(205, 200, 1), (390, 597, 2), (638, 455, 3), (1333, 255, 4), (1530, 455, 5),
                  (1530, 830, 6), (870, A3 + 30, 7)]:
    badge(cx, cy, n)

# ---------------- EDIT: legend, one short sentence per badge ----------------
LY = AY1 + 55
STEPS = [
    "Part 3: the internet brute forces RDP, SSH, and SQL on both VMs through wide-open NSGs.",
    "Part 3: attack-vm scripts brute force Azure AD and read a Key Vault secret 20 times.",
    "Each source writes its own table in the workspace: SecurityEvent, Syslog, SigninLogs, and more.",
    "Part 1: four workbooks join the logs with the GeoIP watchlists to draw attack maps.",
    "Part 2: scheduled KQL analytics rules (13 active after import) raise incidents with entities.",
    "Part 5: each incident is investigated and classified with the NIST 800-61 lifecycle.",
    "Part 5: containment locks each VM NSG down to your own /32 address.",
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
