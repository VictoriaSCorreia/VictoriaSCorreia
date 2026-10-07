import html, pathlib, textwrap

OUT = pathlib.Path("assets"); OUT.mkdir(exist_ok=True)
FONT = "'JetBrains Mono','Cascadia Code','Fira Code',Consolas,'DejaVu Sans Mono',Menlo,monospace"
C = dict(win="#05080D", bar="#0b1018", border="#2a313c", text="#d4dae3", dim="#7d8590",
         green="#7ee787", blue="#79c0ff", pink="#b4e3a1", yellow="#e3b341", purple="#e6dc95",
         orange="#ffa657", red="#ff7b72", track="#1a212b")
W = 800
_uid = [0]
def uid(p="c"):
    _uid[0] += 1; return f"{p}{_uid[0]}"

def esc(s): return html.escape(s, quote=True)

def seg(x, y, s, color, size=14, bold=False, anchor="start"):
    if not s: return ""
    cw = size * 0.6
    b = ' font-weight="700"' if bold else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-size="{size}"{b}{a} '
            f'textLength="{len(s)*cw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(s)}</text>')

def line(x, y, parts, size=14):
    out, col = "", 0
    for p in parts:
        t, c = p[0], p[1]; bold = len(p) > 2 and p[2]
        out += seg(x + col*size*0.6, y, t, C[c], size, bold); col += len(t)
    return out

def appear(content, t):
    return (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>{content}</g>')

def typed(x, y, parts, t0, size=14, cps=14):
    total = sum(len(p[0]) for p in parts); cw = size*0.6
    dur = total / cps; i = uid()
    vals = ";".join(f"{k*cw:.1f}" for k in range(total+1))
    kts = ";".join(f"{k/(total+1):.4f}" for k in range(total+1))
    clip = (f'<clipPath id="{i}"><rect x="{x}" y="{y-size}" height="{size*1.6}" width="0">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kts}" calcMode="discrete" '
            f'begin="{t0:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
    return clip + f'<g clip-path="url(#{i})">{line(x, y, parts, size)}</g>', t0 + dur

PROMPT = [("root@vicco", "green", True), (":", "text"), ("~", "blue"), ("# ", "text")]

def prompt_typed(x, y, cmd_parts, t_show, t_type, size=14):
    p = appear(line(x, y, PROMPT, size), t_show)
    tx = x + sum(len(q[0]) for q in PROMPT) * size*0.6
    t, end = typed(tx, y, cmd_parts, t_type, size)
    return p + t, end

def cursor(x, y, t, size=14):
    cw = size*0.6
    return (f'<rect x="{x:.1f}" y="{y-size+2:.1f}" width="{cw:.1f}" height="{size+2}" fill="{C["text"]}" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{t:.2f}s"/>'
            f'<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="1.1s" '
            f'begin="{t:.2f}s" repeatCount="indefinite"/></rect>')

def window(h, title, body, w=W):
    bar = (f'<path d="M0.5 10.5 a10 10 0 0 1 10 -10 h{w-21} a10 10 0 0 1 10 10 v22 h-{w-1} z" fill="{C["bar"]}"/>'
           f'<path d="M0.5 32.5 h{w-1}" stroke="{C["border"]}"/>')
    dots = "".join(f'<circle cx="{20+i*18}" cy="16.5" r="5.5" fill="{c}"/>' for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
            f'<style>text{{white-space:pre}}</style>'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{C["win"]}" stroke="{C["border"]}"/>'
            f'{bar}{dots}{seg(w/2, 21, title, C["dim"], 12, anchor="middle")}{body}</svg>')

def save(name, svg): (OUT/name).write_text(svg, encoding="utf-8"); print("ok", name)

# ---------------------------------------------------------------- whoami
def whoami():
    x, y, lh = 24, 66, 23
    body, t = prompt_typed(x, y, [("whoami", "text")], 0.2, 0.8)
    out = [
        [("[+] ", "green"), ("Hello! I'm ", "text"), ("Victoria", "pink", True), (".", "text")],
        [("[+] ", "green"), ("FullStack developer from Brazil, currently building at ", "text"), ("Athom8", "blue", True), (".", "text")],
        [],
        [("[+] ", "green"), ("I started programming early, and diving into this world", "text")],
        [("    ", "text"), ("was the best choice of my life.", "text")],
        [("[+] ", "green"), ("I want to play a role in the future of technology,", "text")],
        [("    ", "text"), ("or better yet, in the technological future itself.", "text")],
        [],
        [("[+] ", "green"), ("What makes me happy is bringing my ", "text"), ("artistic side", "pink"), (" into code:", "text")],
        [("    ", "text"), ("solutions that don't just work, but also ", "text"), ("inspire", "pink"), (".", "text")],
        [],
        [("[!] ", "yellow", True), ("SUCCESS", "green", True)],
    ]
    t += 0.35
    for i, parts in enumerate(out):
        yy = y + lh*(i+1)
        if parts: body += appear(line(x, yy, parts), t); t += 0.28
    t += 0.4
    yy = y + lh*(len(out)+1)
    body += appear(line(x, yy, PROMPT), t)
    body += cursor(x + 14*0.6*14, yy, t)
    save("whoami.svg", window(yy + 28, "root@vicco: ~/whoami", body))

# ---------------------------------------------------------------- neofetch
ART = [
    "██╗   ██╗ ██████╗",
    "██║   ██║██╔════╝",
    "██║   ██║██║     ",
    "╚██╗ ██╔╝██║     ",
    " ╚████╔╝ ╚██████╗",
    "  ╚═══╝   ╚═════╝",
]
def neofetch():
    x, y, lh = 24, 66, 23
    body, t = prompt_typed(x, y, [("neofetch", "text")], 0.2, 0.6)
    t += 0.3
    info = [
        [("victoria", "pink", True), ("@", "text"), ("vicco", "pink", True)],
        [("-"*14, "dim")],
        [("Name", "blue", True), (": Victoria Correia", "text")],
        [("Role", "blue", True), (": Software Engineer", "text")],
        [("Locale", "blue", True), (": Brazil", "text")],
        [("Education", "blue", True), (": B.Sc. Information Systems", "text")],
    ]
    top = y + lh + 12
    ix = 270
    rows = ""
    for i, parts in enumerate(info): rows += line(ix, top + lh*i, parts)
    py = top + lh*(len(info) - 1)
    grid = ["XX....XX.XXXXXX",
            "XX....XX.XX....",
            "XX....XX.XX....",
            ".XX..XX..XX....",
            ".XX..XX..XX....",
            "..XXXX...XX....",
            "...XX.....XXXXX"]
    grad = ["#a8e3a6", "#b6e3a0", "#c4e29b", "#d2e196", "#dddf93", "#e4db92", "#e8d792"]
    px = 14
    art_h = len(grid)*px
    ay = top - 14 + (lh*len(info) - art_h)/2
    ax = x + 6
    shadow = "".join(f'<rect x="{ax+c*px+3}" y="{ay+r*px+3}" width="{px-2}" height="{px-2}" fill="#1f2a1c"/>'
                     for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "X")
    blocks = "".join(f'<rect x="{ax+c*px}" y="{ay+r*px}" width="{px-2}" height="{px-2}" fill="{grad[r]}"/>'
                     for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "X")
    art = shadow + blocks
    body += appear(art + rows, t)
    h = py + 30
    save("neofetch.svg", window(h, "root@vicco: ~/id", body))

# ---------------------------------------------------------------- git log
def gitlog():
    x, y = 24, 66
    body, t = prompt_typed(x, y, [("git log --graph --oneline career", "text")], 0.2, 0.6, )
    t += 0.3
    commits = [
        ("a3f9c21", [("(HEAD -> main) ", "blue", True)], ("feat", "green"), "FullStack Developer @ Athom8", "2025 - now",
         ["ERP systems, LangGraph multi-agent workflows, AI-powered mobile apps",
          "Spring Boot, React / Native, Django, Celery + Redis, Docker"]),
        ("7be1d04", [], ("feat", "green"), "Hackathon, Tribunal de Justiça da Bahia", "2025", []),
        ("5c2e8aa", [], ("learn", "purple"), "Design Thinking training, Tomorrow / UFBA", "2025", []),
        ("b81f0e9", [], ("build", "orange"), "Java back-end bootcamp, DIO & Santander (87h)", "2024", []),
        ("2f8a6c7", [], ("learn", "purple"), "AI immersion, Alura & Google", "2024", []),
        ("19e4b52", [], ("docs", "yellow"), "Veteran mentor @ Estácio", "2023 - 2024", []),
        ("0a1b2c3", [("(tag: v0.1) ", "yellow", True)], ("init", "pink"), "B.Sc. Information Systems @ Estácio", "2022 - 2025", []),
    ]
    gx = x + 8; cy = y + 34; rows = ""; first = cy
    ys = []
    for h_, refs, (typ, tc), msg, date, details in commits:
        ys.append(cy)
        parts = [(h_ + " ", "yellow")] + refs + [(typ, tc, True), (": " + msg, "text")]
        rows += line(gx + 22, cy, parts)
        rows += seg(W - 24, cy, date, C["dim"], 13, anchor="end")
        for d in details:
            cy += 21; rows += line(gx + 22 + 8*8.4, cy, [(d, "dim")], 13)
        cy += 27
    last = ys[-1]
    graph = f'<path d="M{gx} {first-5} V{last-5}" stroke="{C["pink"]}" stroke-width="2"/>'
    graph += "".join(f'<circle cx="{gx}" cy="{yy-5}" r="5" fill="{C["win"]}" stroke="{C["pink"]}" stroke-width="2"/>' for yy in ys)
    graph += f'<circle cx="{gx}" cy="{ys[0]-5}" r="5" fill="{C["pink"]}"/>'
    body += appear(graph + rows, t)
    save("experience.svg", window(cy - 4, "root@vicco: ~/experience", body))

# ---------------------------------------------------------------- scan + cards
SCAN_END = 4.6
def scan():
    x, y = 24, 66
    body, t = prompt_typed(x, y, [("./scan --repos VictoriaSCorreia", "text")], 0.2, 0.6)
    t += 0.3
    y2 = y + 28
    body += appear(line(x, y2, [("SCANNING REPOSITORIES ", "dim")]), t)
    n = 28; bx = x + 22*8.4; cell = 8.4
    steps = 14; stepdur = (SCAN_END - 0.6 - t) / steps
    cells = ""
    for k in range(n):
        tk = t + stepdur * (k * steps / n)
        cells += f'<rect x="{bx + k*cell:.1f}" y="{y2-11}" width="{cell-2:.1f}" height="12" fill="{C["track"]}"/>'
        cells += f'<rect x="{bx + k*cell:.1f}" y="{y2-11}" width="{cell-2:.1f}" height="12" fill="{C["green"]}" opacity="0"><set attributeName="opacity" to="1" begin="{tk:.2f}s" fill="freeze"/></rect>'
    body += appear(cells, t)
    px = bx + n*cell + 10
    for s in range(steps + 1):
        pct = round(100 * s / steps)
        a, b = t + stepdur*s, t + stepdur*(s+1)
        vis = f'<set attributeName="opacity" to="1" begin="{a:.2f}s"/>'
        if s < steps: vis += f'<set attributeName="opacity" to="0" begin="{b:.2f}s"/>'
        body += f'<g opacity="0">{vis}{seg(px, y2, f"{pct}%", C["text"], 14)}</g>'
    y3 = y2 + 28
    body += appear(line(x, y3, [("[+] ", "green"), ("Scan complete. Opening repositories...", "text")]), SCAN_END - 0.3)
    save("scan.svg", window(y3 + 22, "root@vicco: ~/projects", body))

def card(name, year, desc, tag, fname, delay):
    w, h = 258, 176
    lines = textwrap.wrap(desc, 31)
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{C["win"]}" stroke="{C["border"]}"/>'
            + line(18, 30, [("drwxr-xr-x  ", "dim"), (year, "yellow")], 12)
            + line(18, 56, [(name, "pink", True)], 16)
            + "".join(line(18, 82 + 18*i, [(l, "text")], 12) for i, l in enumerate(lines))
            + line(18, h - 18, [("open ./", "green"), (tag, "green", True)], 12))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+6}" height="{h}" viewBox="-3 0 {w+6} {h}" font-family="{FONT}">'
           f'<style>text{{white-space:pre}}</style>{appear(body, delay)}</svg>')
    save(fname, svg)

# ---------------------------------------------------------------- english
LEVELS = ["LOW", "MODERATE", "ELEVATED", "FLUENT"]
def english(level):
    x, y = 24, 66
    body, t = prompt_typed(x, y, [("cat ~/english", "text")], 0.2, 0.6)
    t += 0.3
    idx = LEVELS.index(level)
    segw = (W - 48 - 3*8) / 4
    by = y + 22
    blocks = ""
    for i, lv in enumerate(LEVELS):
        bx = x + i*(segw + 8)
        blocks += f'<rect x="{bx:.1f}" y="{by}" width="{segw:.1f}" height="10" rx="3" fill="{C["track"]}"/>'
        if i <= idx:
            blocks += (f'<rect x="{bx:.1f}" y="{by}" width="0" height="10" rx="3" fill="{C["pink"] if i == idx else C["purple"]}">'
                       f'<animate attributeName="width" from="0" to="{segw:.1f}" begin="{t + 0.35*i:.2f}s" dur="0.35s" fill="freeze"/></rect>')
        col = "pink" if i == idx else ("text" if i < idx else "dim")
        blocks += line(bx, by + 34, [(lv, col, i == idx)], 13)
    body += appear(blocks, t)
    save(f"english-{level.lower()}.svg", window(by + 52, "root@vicco: ~/english", body))

# ---------------------------------------------------------------- status bar (tmux)
def piece(text_parts, fname, bg, first=False, last=False, extra=""):
    size = 13; cw = size*0.6
    n = sum(len(p[0]) for p in text_parts)
    w = round(n*cw + 24); h = 30; r = 8
    if first:   shape = f'<path d="M{r} 0 H{w} V{h} H{r} a{r} {r} 0 0 1 -{r} -{r} V{r} a{r} {r} 0 0 1 {r} -{r} z" fill="{bg}"/>'
    elif last:  shape = f'<path d="M0 0 H{w-r} a{r} {r} 0 0 1 {r} {r} V{h-r} a{r} {r} 0 0 1 -{r} {r} H0 z" fill="{bg}"/>'
    else:       shape = f'<rect width="{w}" height="{h}" fill="{bg}"/>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
           f'<style>text{{white-space:pre}}</style>{shape}{extra}{line(12, 20, text_parts, size)}</svg>')
    save(fname, svg)

def statusbar():
    piece([("[vicco]", "win", True)], "bar-session.svg", C["green"], first=True)
    piece([("0:readme*", "text", True)], "bar-0-readme.svg", "#2a313c")
    for i, name in enumerate(["linkedin", "github", "email", "instagram", "portfolio"], 1):
        piece([(f"{i}:", "dim"), (name, "text")], f"bar-{i}-{name}.svg", C["bar"])
    dot = (f'<circle cx="16" cy="15" r="4" fill="{C["green"]}"><animate attributeName="opacity" values="1;0.25;1" '
           f'dur="2s" repeatCount="indefinite"/></circle>')
    piece([("  OPERATIONAL", "green", True)], "bar-status.svg", C["bar"], last=True, extra=dot)

def prompt_bar(cmd, fname, t0=0.2):
    x, y = 18, 27
    body, end = prompt_typed(x, y, [(cmd, "text")], t0, t0 + 0.4)
    w, h = W, 42
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
           f'<style>text{{white-space:pre}}</style>'
           f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{C["win"]}" stroke="{C["border"]}"/>{body}'
           f'{cursor(x + (14 + len(cmd) + 1)*8.4, y, end + 0.1)}</svg>')
    save(fname, svg)

whoami(); neofetch(); gitlog(); scan()
card("RepoLogs", "2026", "Chrome extension that audits GitHub repositories for code quality, bugs and vulnerabilities.", "repologs", "project-repologs.svg", SCAN_END)
card("Tech Conecta.dev", "2025", "AI job-search platform that ranks openings against your own profile.", "tech-conecta", "project-techconecta.svg", SCAN_END + 0.25)
card("King of Diamonds", "2024", "Math-based game inspired by Alice in Borderland.", "king-of-diamonds", "project-kingofdiamonds.svg", SCAN_END + 0.5)
for lv in LEVELS: english(lv)
statusbar()
prompt_bar("ls ~/stack", "stack-prompt.svg")
