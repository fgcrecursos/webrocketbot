# -*- coding: utf-8 -*-
"""Agrega el manual de marca descargable a la seccion Recursos de las 54 paginas.

Tres puntos por pagina, los mismos tres donde aparece Academy: el dropdown
Recursos del header, la seccion Recursos del menu movil y la columna Recursos
del footer. Se inserta despues de Academy, que cierra la lista en los tres.
Las tres paginas de contacto tienen ademas un bloque Recursos propio en la
columna lateral, que suma un cuarto enlace.

El PDF es distinto por idioma y los href van root-absolutos (con la extension
.pdf puesta, que nginx no tiene cleanUrls). Idempotente.
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent

DOC = {
    "es": ("/assets/docs/rocketbot-manual-de-marca-2026.pdf", "Manual de marca"),
    "en": ("/assets/docs/rocketbot-brandbook-2026.pdf", "Brandbook"),
    "pt": ("/assets/docs/rocketbot-manual-da-marca-2026.pdf", "Manual da marca"),
}

ACADEMY = (r'<a href="https://academy\.rocketbot\.com" target="_blank" '
           r'rel="noopener">Academy</a>')

# (1) columna Recursos del footer: el Academy va envuelto en <li>. El footer
#     esta minificado en unas paginas y expandido en otras, asi que se captura
#     la sangria para no pegar el <li> nuevo al final de una linea existente.
FOOTER = re.compile(r'(^[ \t]*)?(<li>' + ACADEMY + r'</li>)', re.M)
# (2) dropdown del header: viene minificado y pegado al </div> que lo cierra.
DROPDOWN = re.compile(r'(' + ACADEMY + r')(</div>)')
# (3) menu movil: el Academy ocupa su propia linea.
MOVIL = re.compile(r'^([ \t]*)' + ACADEMY + r'[ \t]*$', re.M)
# (4) bloque Recursos de la columna lateral de las paginas de contacto: los
#     enlaces van en rojo, separados por <br>, y el ultimo es Marketplace.
ESTILO_CONTACTO = 'style="color:var(--rb-red);font-weight:600;"'
CONTACTO = re.compile(
    r'^([ \t]*)(<a href="https://market\.rocketbot\.com/" target="_blank" '
    r'rel="noopener" ' + re.escape(ESTILO_CONTACTO) + r'>[^<]*</a>)[ \t]*$', re.M)


def idioma(p: pathlib.Path) -> str:
    partes = p.relative_to(ROOT).parts
    return partes[0] if partes and partes[0] in ("en", "pt") else "es"


def main() -> int:
    def incluir(p: pathlib.Path) -> bool:
        partes = p.relative_to(ROOT).parts
        return ("hub" not in partes              # el hub tiene su propia cabecera
                and "node_modules" not in partes
                and not p.name.startswith("_"))  # _a.html / _b.html son scratch

    paginas = [p for p in ROOT.rglob("*.html") if incluir(p)]
    hechas = ya = malas = 0
    for p in sorted(paginas):
        t = p.read_text(encoding="utf-8")
        href, rotulo = DOC[idioma(p)]
        if href in t:                            # ya parcheada: no reinsertar
            ya += 1
            continue
        a = '<a href="%s" download>%s</a>' % (href, rotulo)

        def footer(m):
            sangria = m.group(1)
            if sangria is None:            # footer minificado: todo en una linea
                return "%s<li>%s</li>" % (m.group(2), a)
            return "%s%s\n%s<li>%s</li>" % (sangria, m.group(2), sangria, a)

        t = FOOTER.sub(footer, t)
        t = DROPDOWN.sub(lambda m: "%s%s%s" % (m.group(1), a, m.group(2)), t)
        t = MOVIL.sub(lambda m: "%s\n%s%s" % (m.group(0), m.group(1), a), t)

        esperados = 3
        if CONTACTO.search(t):
            lateral = ('<a href="%s" download %s>%s &rarr;</a>'
                       % (href, ESTILO_CONTACTO, rotulo))
            t = CONTACTO.sub(
                lambda m: "%s%s<br>\n%s%s" % (m.group(1), m.group(2), m.group(1), lateral), t)
            esperados = 4

        n = t.count(href)
        if n != esperados:
            print("  !! %s: quedaron %d enlaces (esperaba %d)"
                  % (p.relative_to(ROOT), n, esperados))
            malas += 1
        p.write_text(t, encoding="utf-8")
        hechas += 1
    print("\nparcheadas:%d  ya estaban:%d  con problemas:%d  total:%d"
          % (hechas, ya, malas, len(paginas)))
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main())
