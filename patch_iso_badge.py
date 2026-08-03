# -*- coding: utf-8 -*-
"""
Agrega un sello/badge "ISO/IEC 27001" al footer de todas las paginas (es/en/pt).
No usa el logo oficial de ISO (su uso esta reservado a la organizacion ISO y a
marcas de certificacion emitidas por el organismo certificador); en su lugar
dibuja un icono generico tipo escudo + el texto del estandar, coherente con el
resto del sitio. Idempotente: si ya existe rb-iso-badge, no vuelve a tocar el
archivo.

    python patch_iso_badge.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_MARK = 'rb-iso-badge{'
CSS_BLOCK = """
.rb-iso-badge{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;letter-spacing:.02em;color:#999;border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:5px 12px;white-space:nowrap;}
.rb-iso-badge svg{width:14px;height:14px;color:var(--rb-green,#1D9E75);flex:0 0 auto;}
.rb-iso-badge:hover{border-color:rgba(255,255,255,.3);color:#ccc;}
@media(max-width:640px){.rb-footer__bottom{flex-wrap:wrap;gap:14px;}}
"""

BADGE_HTML = ('<span class="rb-iso-badge" title="{title}">'
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
              'stroke-linecap="round" stroke-linejoin="round">'
              '<path d="M12 2 4 5v6c0 5 3.4 8.5 8 11 4.6-2.5 8-6 8-11V5l-8-3Z"/>'
              '<path d="m9 12 2 2 4-4"/></svg>ISO/IEC 27001</span>')

TITLE = {
    'es': 'Certificación ISO/IEC 27001 — Gestión de seguridad de la información',
    'en': 'ISO/IEC 27001 certification — Information security management',
    'pt': 'Certificação ISO/IEC 27001 — Gestão de segurança da informação',
}

COPY_RE = re.compile(r'(<span>© Rocketbot SpA \| All rights reserved 2018 – 2025</span>)')


def lang_of(path):
    norm = path.replace('\\', '/')
    if '/en/' in norm:
        return 'en'
    if '/pt/' in norm:
        return 'pt'
    return 'es'


def patch(path):
    with io.open(path, encoding='utf-8') as f:
        src = f.read()

    if 'rb-iso-badge' in src:
        return False
    if '<span>© Rocketbot SpA | All rights reserved 2018 – 2025</span>' not in src:
        return False

    lang = lang_of(path)
    badge = BADGE_HTML.format(title=TITLE[lang])
    new_src = COPY_RE.sub(lambda m: m.group(1) + badge, src, count=1)
    if new_src == src:
        return False

    if CSS_MARK not in new_src:
        new_src = new_src.replace('</style>', CSS_BLOCK + '</style>', 1)

    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_src)
    return True


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in filenames:
            if fn.endswith('.html'):
                p = os.path.join(dirpath, fn)
                if patch(p):
                    changed.append(p)
    print('patched %d files' % len(changed))
    for p in changed:
        print(' -', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
