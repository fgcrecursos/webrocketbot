# -*- coding: utf-8 -*-
"""
Achica el logo y aprieta un poco la barra para que el menu completo entre en
mas anchos sin caer a la hamburguesa. Frani pidio, expresamente, ganar espacio
achicando el logo en vez de colapsar el menu.

Medido sobre las 39 paginas (con enlaces visibles): la mas ancha
(pt/construir-vs-comprar, con el CTA "Vamos falar do seu caso") pasa a pedir
1427px, asi que el menu sobrevive a 1440 / 1536 / 1600 / 1920 sin hamburguesa.

  · logo del header 32px -> 24px de alto (el mobile ya baja a 22/19, intacto)
  · gap de enlaces 19px -> 16px
  · gap del inner 24px -> 20px
  · padding lateral del nav 24px -> 20px (reposo y scrolled)
  · el corte de la hamburguesa baja de 1560px a 1432px

Idempotente y para los dos formatos de CSS (compacto y el de index).

    python patch_header_fit.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BREAKPOINT = 1432

SUBS = [
    (re.compile(r'(\.rb-nav__logo\s*\{\s*height:\s*)32px'), r'\g<1>24px'),
    (re.compile(r'(\.rb-nav__links\s*\{[^}]*?gap:\s*)19px'), r'\g<1>16px'),
    (re.compile(r'(\.rb-nav__inner\s*\{[^}]*?gap:\s*)24px'), r'\g<1>20px'),
    (re.compile(r'(\.rb-nav\s*\{[^}]*?padding:\s*18px\s+)24px'), r'\g<1>20px'),
    (re.compile(r'(\.rb-nav\.scrolled\s*\{[^}]*?padding:\s*10px\s+)24px'), r'\g<1>20px'),
    (re.compile(r'@media\s*\(max-width:\s*1560px\)'), '@media(max-width:%dpx)' % BREAKPOINT),
]


def patch(path):
    src = io.open(path, encoding='utf-8').read()
    orig = src
    for rx, rep in SUBS:
        src = rx.sub(rep, src, count=1)
    if src != orig:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
        return True
    return False


def main():
    n = 0
    for folder, prefix in ((ROOT, ''), (os.path.join(ROOT, 'en'), 'en/'), (os.path.join(ROOT, 'pt'), 'pt/')):
        for name in sorted(os.listdir(folder)):
            if not name.endswith('.html') or name == 'planes.html':
                continue  # planes se regenera con build_planes.py
            if patch(os.path.join(folder, name)):
                n += 1
    print('paginas actualizadas: %d' % n)


if __name__ == '__main__':
    main()
