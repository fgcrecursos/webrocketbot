#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Absolutiza los links internos de las paginas de en/ y pt/.

Por que: Vercel sirve el sitio con cleanUrls:true, asi que /en/ contesta 308
hacia /en (sin barra final). Con esa URL el baseURI del documento pasa a ser
".../en", cuyo directorio es la raiz "/", y entonces un href relativo como
"suite-rocketbot.html" resuelve a /suite-rocketbot.html -> la version en
espanol. Resultado: entrar por la home en ingles o portugues y hacer un solo
click devolvia al usuario al espanol.

El arreglo es no depender del baseURI: cada link interno de en/ lleva prefijo
/en/ y cada uno de pt/ lleva /pt/. Funciona igual con o sin barra final, en
Vercel y en el nginx de rocketbot.com.

Idempotente: los href que ya empiezan con "/" no matchean.

IMPORTANTE: correr este script al final de cualquier build_*.py / patch_*.py
que toque en/ o pt/, porque esos generadores escriben los href relativos y
reintroducen el bug.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
LANGS = ("en", "pt")

# Paginas internas del sitio (las que existen en los tres idiomas).
PAGES = [
    "ai-studio", "blog", "cfo", "construir-vs-comprar", "contacto", "faq",
    "index", "nexus", "orquestador", "partners", "planes",
    "politicas-de-privacidad", "politicas-de-seguridad", "rpa-studio",
    "saturn-studio", "suite-rocketbot", "terminos-y-condiciones", "xperience",
]

# href="pagina.html" / href="pagina.html#ancla" / href="pagina.html?x=1"
LINK_RE = re.compile(
    r'(href=")(' + "|".join(re.escape(p) for p in PAGES) + r')\.html([^"]*)(")'
)


def patch(lang):
    folder = os.path.join(ROOT, lang)
    changed = []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(folder, name)
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        out, n = LINK_RE.subn(
            lambda m: "%s/%s/%s.html%s%s" % (m.group(1), lang, m.group(2), m.group(3), m.group(4)),
            src,
        )
        if n:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
            changed.append((name, n))
    return changed


def main():
    total = 0
    for lang in LANGS:
        changed = patch(lang)
        for name, n in changed:
            print("  %s/%-32s %3d links" % (lang, name, n))
            total += n
        if not changed:
            print("  %s/  sin cambios (ya estaba absolutizado)" % lang)
    print("Total: %d links absolutizados." % total)


if __name__ == "__main__":
    main()
