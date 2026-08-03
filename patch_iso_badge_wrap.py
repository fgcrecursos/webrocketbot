# -*- coding: utf-8 -*-
"""
Sigue a patch_iso_badge.py: agrupa el copyright + el badge ISO en un mismo
contenedor flex para que queden pegados a la izquierda del footer, en vez de
quedar centrados sueltos por el justify-content:space-between de
.rb-footer__bottom. Idempotente.

    python patch_iso_badge_wrap.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_MARK = 'rb-footer__bottomleft{'
CSS_BLOCK = "\n.rb-footer__bottomleft{display:flex;align-items:center;gap:14px;flex-wrap:wrap;}\n"

PAT = re.compile(
    r'(<span>© Rocketbot SpA \| All rights reserved 2018 – 2025</span><span class="rb-iso-badge"[^>]*>.*?</span>)',
    re.S
)


def patch(path):
    with io.open(path, encoding='utf-8') as f:
        src = f.read()

    if 'rb-footer__bottomleft' in src:
        return False
    if not PAT.search(src):
        return False

    new_src = PAT.sub(lambda m: '<div class="rb-footer__bottomleft">' + m.group(1) + '</div>', src, count=1)
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


if __name__ == '__main__':
    main()
