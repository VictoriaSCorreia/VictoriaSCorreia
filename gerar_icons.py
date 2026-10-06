import re, urllib.request, pathlib

ICONS = {
    "java":       "https://techstack-generator.vercel.app/java-icon.svg",
    "python":     "https://techstack-generator.vercel.app/python-icon.svg",
    "go":         "https://www.vectorlogo.zone/logos/golang/golang-icon.svg",
    "cpp":        "https://techstack-generator.vercel.app/cpp-icon.svg",
    "typescript": "https://techstack-generator.vercel.app/ts-icon.svg",
    "spring":     "https://www.vectorlogo.zone/logos/springio/springio-icon.svg",
    "django":     "https://techstack-generator.vercel.app/django-icon.svg",
    "flask":      "https://www.vectorlogo.zone/logos/palletsprojects_flask/palletsprojects_flask-icon.svg",
    "react":      "https://www.vectorlogo.zone/logos/reactjs/reactjs-icon.svg",
    "postgresql": "https://www.vectorlogo.zone/logos/postgresql/postgresql-icon.svg",
    "mysql":      "https://techstack-generator.vercel.app/mysql-icon.svg",
    "redis":      "https://www.vectorlogo.zone/logos/redis/redis-icon.svg",
    "docker":     "https://techstack-generator.vercel.app/docker-icon.svg",
    "git":        "https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg",
    "raspberry":  "https://techstack-generator.vercel.app/raspberrypi-icon.svg",
}

LARGURA = ALTURA = 76                  # tamanho do arquivo (quadrado de 64 + espaço em volta = 12px entre ícones)
SIZE, RADIUS, BG = 64, 14, "#05080d"   # tamanho do quadrado, arredondamento, cor do fundo
PAD = 10                               # margem interna padrão (px)
PAD_ESPECIAL = {                       # ícones desenhados com muita margem vazia: margem menor
    "cpp": 3, "typescript": 3, "raspberry": 3,
}

# Alguns SVGs aplicam CSS de layout neles mesmos (ex.: "#js-icon { width:100px; transform:... }").
# Isso desloca/redimensiona o ícone quando ele é embutido, então removemos essas propriedades.
LAYOUT = r"(?:position|top|left|right|bottom|transform|width|height|margin|inset)"

def neutralizar_css_da_raiz(svg, root_tag):
    rid = re.search(r'\sid="([^"]+)"', root_tag)
    if not rid:
        return svg
    sel = re.escape("#" + rid.group(1))
    def limpar(m):
        return m.group(1) + re.sub(rf"\b{LAYOUT}\s*:[^;}}]*;?", "", m.group(2)) + m.group(3)
    return re.sub(rf"((?<![\w-]){sel}\s*\{{)([^}}]*)(\}})", limpar, svg)

def montar(svg, nome):
    pad = PAD_ESPECIAL.get(nome, PAD)
    svg = re.sub(r"<\?xml.*?\?>|<!DOCTYPE.*?>", "", svg, flags=re.S)
    root = re.search(r"<svg\b[^>]*>", svg).group(0)
    svg = neutralizar_css_da_raiz(svg, root)
    root = re.search(r"<svg\b[^>]*>", svg).group(0)

    w = re.search(r'\swidth="([\d.]+)', root)
    h = re.search(r'\sheight="([\d.]+)', root)
    novo = root
    if "viewBox" not in novo and w and h:
        novo = novo[:-1] + f' viewBox="0 0 {w.group(1)} {h.group(1)}">'
    novo = re.sub(r'\s(width|height|x|y|style)="[^"]*"', "", novo)
    inner = SIZE - 2 * pad
    novo = novo[:-1] + f' x="{pad}" y="{pad}" width="{inner}" height="{inner}">'
    svg = svg.replace(root, novo, 1)

    x0 = (LARGURA - SIZE) // 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" height="{ALTURA}" viewBox="0 0 {LARGURA} {ALTURA}">'
            f'<svg x="{x0}" y="{x0}" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">'
            f'<rect width="{SIZE}" height="{SIZE}" rx="{RADIUS}" fill="{BG}"/>{svg}</svg></svg>')

out = pathlib.Path("icons")
out.mkdir(exist_ok=True)

for nome, url in ICONS.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        svg = urllib.request.urlopen(req).read().decode("utf-8")
        (out / f"{nome}.svg").write_text(montar(svg, nome), encoding="utf-8")
        print("ok:", nome)
    except Exception as e:
        print("FALHOU:", nome, "->", e)