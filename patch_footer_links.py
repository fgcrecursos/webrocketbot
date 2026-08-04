# -*- coding: utf-8 -*-
"""
Dos cambios de navegacion aplicados a las 54 paginas (es/en/pt):

  1. Elimina el item "Certificacion" de la columna "Soporte y servicios" del
     footer. Era un link muerto (href="#") y se pidio sacarlo. No toca el sello
     ISO del footer, que usa la palabra "Certificacion" solo en su atributo
     title.
  2. Reapunta el link "Foro" de forum.rocketbot.com a market.rocketbot.com
     (aparece 3 veces por pagina: dropdown del header, menu mobile y footer).

Idempotente: correrlo dos veces no cambia nada.

    python patch_footer_links.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Solo el <li> del footer. El sello ISO lleva "Certificacion" dentro de title="",
# nunca como texto de un <li>, asi que este patron no lo alcanza.
CERT_RE = re.compile(
    r'\n?[ \t]*<li><a href="#">(?:Certificaci[oó]n|Certification|Certifica[çc][ãa]o)</a></li>'
)

OLD_FORUM = 'https://forum.rocketbot.com'
NEW_FORUM = 'https://market.rocketbot.com/'


def patch(path):
    with io.open(path, encoding='utf-8') as f:
        src = f.read()
    orig = src

    src = CERT_RE.sub('', src)
    src = src.replace(OLD_FORUM, NEW_FORUM)

    if src == orig:
        return None

    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    return (len(CERT_RE.findall(orig)), orig.count(OLD_FORUM))


def main():
    files = 0
    certs = 0
    forums = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in sorted(filenames):
            if not fn.endswith('.html'):
                continue
            res = patch(os.path.join(dirpath, fn))
            if res:
                files += 1
                certs += res[0]
                forums += res[1]
    print('archivos tocados: %d' % files)
    print('items "Certificacion" eliminados: %d' % certs)
    print('links de Foro reapuntados: %d' % forums)


if __name__ == '__main__':
    main()
