# -*- coding: utf-8 -*-
"""
El banner "Juntos, ayudan a que la operación avance" del index tenia el texto
en rojo sobre un fondo con tinte rojo: en tema oscuro no se leia. Pasa el texto
a un color legible segun el tema (oscuro sobre claro, blanco sobre oscuro) y el
enlace, que tambien era rojo, a blanco en oscuro.

    python patch_banner_contrast.py
"""
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = ['index.html', 'en/index.html', 'pt/index.html']

REPL = [
    # cuerpo del parrafo: rojo -> gris oscuro en claro
    ('.rb-solution__banner-desc{font-size:13px;color:var(--rb-red);line-height:1.6;}',
     '.rb-solution__banner-desc{font-size:13px;color:#555;line-height:1.6;}'),
    # cuerpo en oscuro: rojo tenue -> blanco legible, y el enlace theme-aware
    ('[data-theme="dark"] .rb-solution__banner-desc{color:rgba(188,0,23,.85);}',
     '[data-theme="dark"] .rb-solution__banner-desc{color:rgba(255,255,255,.72);}'
     '.rb-solution__banner-desc a{color:var(--rb-red);font-weight:700;}'
     '[data-theme="dark"] .rb-solution__banner-desc a{color:#fff;text-decoration:underline;}'),
    # el enlace deja de fijar el color inline para que mande el CSS por tema
    ('<a href="construir-vs-comprar.html" style="color:var(--rb-red);font-weight:700">',
     '<a href="construir-vs-comprar.html">'),
]


def main():
    n = 0
    for rel in FILES:
        path = os.path.join(ROOT, rel)
        src = io.open(path, encoding='utf-8').read()
        orig = src
        for old, new in REPL:
            if old not in src:
                raise SystemExit('no encontrado en %s: %s' % (rel, old[:60]))
            src = src.replace(old, new, 1)
        if src != orig:
            io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
            n += 1
            print('  %s' % rel)
    print('paginas actualizadas: %d' % n)


if __name__ == '__main__':
    main()
