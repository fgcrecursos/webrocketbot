# -*- coding: utf-8 -*-
"""Agrega "Hub de industrias" (/hub) al dropdown Recursos y al menu movil
de las 54 paginas, en los 3 idiomas. Idempotente.

Inserta antes del enlace Blog. El Blog aparece 3 veces por pagina: dropdown,
menu movil y columna Recursos del footer; la del footer va envuelta en <li>,
asi que el patron a nivel de linea la excluye (el pedido era el menu header).
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent

LABEL = {"es": "Hub de industrias", "en": "Industry hub", "pt": "Hub de indústrias"}

BLOG_A = r'<a href="https://rocketbot\.com/es/blog/" target="_blank" rel="noopener">Blog</a>'

# (1) el Blog en su propia linea: dropdown y menu movil sin minificar.
#     La del footer va envuelta en <li>, asi que anclar a la linea la excluye.
BLOG_LINEA = re.compile(r'^([ \t]*)' + BLOG_A + r'[ \t]*$', re.M)

# (2) el Blog minificado dentro del dropdown: viene pegado a un </a>.
#     En el footer viene pegado a un <li>, por eso no matchea.
BLOG_INLINE = re.compile(r'(</a>)(' + BLOG_A + r')')


def lang_of(p: pathlib.Path) -> str:
    parts = p.relative_to(ROOT).parts
    if parts and parts[0] in ("en", "pt"):
        return parts[0]
    return "es"


def main() -> int:
    def incluir(p: pathlib.Path) -> bool:
        rel = p.relative_to(ROOT).parts
        return ("hub" not in rel                 # el hub tiene su propia cabecera
                and "node_modules" not in rel
                and not p.name.startswith("_"))  # _a.html / _b.html son scratch

    pages = [p for p in ROOT.rglob("*.html") if incluir(p)]
    hecho = ya = malas = 0
    for p in sorted(pages):
        t = p.read_text(encoding="utf-8")
        link = f'<a href="/hub">{LABEL[lang_of(p)]}</a>'
        if 'href="/hub"' in t:   # ya parcheada: no reinsertar
            ya += 1
            continue
        t = BLOG_LINEA.sub(lambda m: f'{m.group(1)}{link}\n{m.group(0)}', t)
        t = BLOG_INLINE.sub(lambda m: f'{m.group(1)}{link}{m.group(2)}', t)
        n = t.count('href="/hub"')
        if n != 2:
            print(f"  !! {p.relative_to(ROOT)}: quedaron {n} enlaces (esperaba 2)")
            malas += 1
        p.write_text(t, encoding="utf-8")
        hecho += 1
    print(f"\nparcheadas:{hecho}  ya estaban:{ya}  con problemas:{malas}  total:{len(pages)}")
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main())
