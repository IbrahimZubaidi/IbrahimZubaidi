"""Build the profile's SVGs: the animated "decrypt" header and the project cards.
Run: python assets/make_svgs.py   (writes into assets/)"""
import os
import random
from html import escape

OUT = os.path.dirname(os.path.abspath(__file__))
BG, PANEL, LINE = "#0b0f14", "#11161d", "#1f2933"
GREEN, CYAN, AMBER, DIM, TEXT = "#39d353", "#58c4dc", "#e3b341", "#6e7681", "#c9d1d9"
FONT = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
NOISE = "!#$%&*+<>?@^~0123456789abcdefABCDEF/\\|=-"


def header():
    random.seed(7)
    w, h = 900, 230
    cmd = "$ cat about.enc | ./decrypt --key ICPC"
    plain = "backend engineer  ·  crypto from scratch  ·  competitive programmer"
    frames = 14
    t_type = 1.6            # seconds to type the command
    t0 = t_type + 0.3       # decrypt starts
    step = 0.09             # seconds per frame
    t_done = t0 + frames * step

    def scramble(k):
        keep = int(len(plain) * k / frames)
        return "".join(c if i < keep or c == " " else random.choice(NOISE)
                       for i, c in enumerate(plain))

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(plain)}">',
             f'<style>text{{font-family:{FONT};}} .c{{animation:b 1s steps(1) infinite}} @keyframes b{{50%{{opacity:0}}}}</style>',
             f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
             f'<rect x="1" y="1" width="{w-2}" height="38" rx="13" fill="{PANEL}"/>',
             f'<rect x="1" y="26" width="{w-2}" height="13" fill="{PANEL}"/>',
             f'<line x1="0" y1="39" x2="{w}" y2="39" stroke="{LINE}"/>']
    for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        parts.append(f'<circle cx="{24 + i*20}" cy="20" r="6" fill="{col}"/>')
    parts.append(f'<text x="{w/2}" y="25" fill="{DIM}" font-size="13" text-anchor="middle">~/profile  ·  session 0x2A</text>')

    # line 1: typed command (revealed by a growing clip)
    parts.append('<clipPath id="t"><rect x="0" y="60" height="30" width="0">'
                 f'<animate attributeName="width" from="0" to="{w}" dur="{t_type}s" fill="freeze"/></rect></clipPath>')
    parts.append(f'<text x="32" y="82" fill="{GREEN}" font-size="18" clip-path="url(#t)">{escape(cmd)}</text>')

    # line 2: ciphertext frames that settle into the plain text
    for k in range(frames + 1):
        txt = plain if k == frames else scramble(k)
        col = TEXT if k == frames else CYAN
        begin = t0 + k * step
        end = "" if k == frames else f'<set attributeName="opacity" to="0" begin="{begin + step:.2f}s" fill="freeze"/>'
        parts.append(f'<text x="32" y="124" fill="{col}" font-size="19" font-weight="600" opacity="0">{escape(txt)}'
                     f'<set attributeName="opacity" to="1" begin="{begin:.2f}s" fill="freeze"/>{end}</text>')

    # line 3 and 4 fade in after decrypting
    for y, label, value, col in ((166, "status", "building my own apps, one idea at a time", AMBER),
                                 (196, "stack ", "Python · FastAPI · PHP · SQL · C++", DIM)):
        parts.append(f'<text x="32" y="{y}" font-size="16" opacity="0"><tspan fill="{GREEN}">&gt; {label}:</tspan>'
                     f'<tspan fill="{col}"> {escape(value)}</tspan>'
                     f'<animate attributeName="opacity" from="0" to="1" begin="{t_done + (0.3 if y == 166 else 0.6):.2f}s" dur="0.4s" fill="freeze"/></text>')
    parts.append(f'<rect class="c" x="{32 + 10*48}" y="182" width="10" height="18" fill="{GREEN}" opacity="0">'
                 f'<set attributeName="opacity" to="1" begin="{t_done + 0.9:.2f}s" fill="freeze"/></rect>')
    parts.append('</svg>')
    with open(os.path.join(OUT, "header.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


CARDS = [
    ("cryptography-algorithms", "DES, AES, RSA, ElGamal, Diffie-Hellman,", "digital signatures and elliptic curves, no libraries.", "C++", "#f34b7d", "crypto"),
    ("password-manager", "Salted hashes for accounts and per-password", "AES encryption, behind a small Flask app.", "Python", "#3572A5", "security"),
    ("coding-framework", "My web app framework and conventions:", "FastAPI backend, no-build HTML/JS, PostgreSQL.", "JavaScript", "#f1e05a", "framework"),
    ("cat-game", "2D Java Swing game with login and a", "MySQL leaderboard. Playable build in releases.", "Java", "#b07219", "game"),
]


def card(name, l1, l2, lang, color, tag):
    w, h = 430, 132
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{name}">
<style>text{{font-family:{FONT};}}</style>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{BG}" stroke="{LINE}"/>
<rect x="0.5" y="0.5" width="4" height="{h-1}" rx="2" fill="{color}"/>
<text x="22" y="34" fill="{GREEN}" font-size="16" font-weight="700">./{escape(name)}</text>
<text x="{w-20}" y="33" fill="{DIM}" font-size="12" text-anchor="end">[{tag}]</text>
<text x="22" y="64" fill="{TEXT}" font-size="13">{escape(l1)}</text>
<text x="22" y="84" fill="{TEXT}" font-size="13">{escape(l2)}</text>
<circle cx="28" cy="111" r="5" fill="{color}"/>
<text x="40" y="115" fill="{DIM}" font-size="12">{lang}</text>
</svg>'''
    with open(os.path.join(OUT, f"card-{name}.svg"), "w", encoding="utf-8") as f:
        f.write(s)


if __name__ == "__main__":
    header()
    for c in CARDS:
        card(*c)
    print("done")
