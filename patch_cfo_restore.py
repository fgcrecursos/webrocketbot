# -*- coding: utf-8 -*-
"""
Devuelve el boton "Para CFOs" a las acciones del header, tal cual estaba antes
del commit de /planes (se recupera el markup exacto de HEAD, sin reescribirlo),
y hace lugar para que convivan los dos botones sin desbordar la barra:

  · gap de los enlaces 22px -> 19px
  · gap del contenedor del nav 32px -> 24px
  · padding lateral del nav 32px -> 24px
  · el corte donde se ocultan los enlaces sube de 1480px al ancho que la barra
    pide de verdad (BREAKPOINT). Por debajo no se pierde nada: la hamburguesa
    ya lleva CFOs, Planes y todo el resto.

    python patch_cfo_restore.py <commit-con-el-boton>
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BREAKPOINT = 1560

# el boton va delante del ultimo CTA de las acciones (Descarga / Hablemos / ...)
LAST_CTA = re.compile(r'([ \t]*)(<(?:a|button)[^>]*class="rb-btn rb-btn--primary"[^>]*>.*?</(?:a|button)>\s*</div>\s*</div>\s*</nav>)', re.S)
NAV_ACTIONS = re.compile(r'<div class="rb-nav__actions">.*?</nav>', re.S)
OLD_CFO = re.compile(r'<a href="cfo\.html" class="rb-btn (?:rb-cfo-btn|rb-btn--cfo)">[^<]*</a>')


def original_cfo(rel, ref):
    """El <a> del CFO tal como estaba en `ref`; None si esa pagina no lo tenia."""
    out = subprocess.run(['git', 'show', '%s:%s' % (ref, rel)],
                         capture_output=True, cwd=ROOT)
    if out.returncode:
        return None
    old = out.stdout.decode('utf-8')
    acts = NAV_ACTIONS.search(old)
    if not acts:
        return None
    m = OLD_CFO.search(acts.group(0))
    return m.group(0) if m else None


def patch(path, rel, ref):
    src = io.open(path, encoding='utf-8').read()
    orig = src

    # 1) el boton vuelve a su lugar, delante del CTA principal
    acts = NAV_ACTIONS.search(src)
    if acts and 'cfo.html' not in acts.group(0):
        cfo = original_cfo(rel, ref)
        if cfo:
            def _ins(m):
                return '%s%s\n%s%s' % (m.group(1), cfo, m.group(1), m.group(2))
            head, tail = src[:acts.start()], src[acts.start():]
            tail = LAST_CTA.sub(_ins, tail, count=1)
            src = head + tail

    # 2) el espacio que hace falta para que entren los dos botones
    src = re.sub(r'(\.rb-nav__links\s*\{[^}]*?gap:\s*)22px', lambda m: m.group(1) + '19px', src, count=1)
    src = re.sub(r'(\.rb-nav__inner\s*\{[^}]*?gap:\s*)32px', lambda m: m.group(1) + '24px', src, count=1)
    src = re.sub(r'(\.rb-nav\s*\{[^}]*?padding:\s*18px\s+)32px', lambda m: m.group(1) + '24px', src, count=1)
    src = re.sub(r'(\.rb-nav\.scrolled\s*\{[^}]*?padding:\s*10px\s+)32px', lambda m: m.group(1) + '24px', src, count=1)
    src = re.sub(r'(\.rb-nav__plans-hdr\{[^}]*?padding:8px\s+)17px', lambda m: m.group(1) + '14px', src, count=1)
    # suite-rocketbot repite el bloque de la pastilla mas abajo y gana el ultimo:
    # hay que tocar todas las copias, no la primera
    src = src.replace('.rb-nav__suite-hdr{display:inline-flex !important;align-items:center;gap:6px;padding:9px 18px !important;',
                      '.rb-nav__suite-hdr{display:inline-flex !important;align-items:center;gap:6px;padding:9px 15px !important;')

    # 3) los enlaces se ocultan cuando de verdad dejan de entrar
    src = re.sub(r'@media\s*\(max-width:\s*1480px\)', '@media(max-width:%dpx)' % BREAKPOINT, src)

    # 4) la barra dejaba de estar contenida cuando su contenido pasaba los
    #    1280px del inner: como el inner esta centrado con max-width fija, todo
    #    lo que sobra se va para la derecha y se sale de la pantalla (ya pasaba
    #    en construir-vs-comprar antes de /planes). Con esto el inner mantiene
    #    los 1280px mientras el contenido entre — o sea, el mismo dibujo de
    #    siempre — y recien crece, siempre centrado, cuando no entra.
    src = re.sub(r'(\.rb-nav__inner\s*\{[^}]*?)max-width:\s*1280px',
                 lambda m: m.group(1) + 'width:fit-content;min-width:min(1280px,100%);max-width:100%',
                 src, count=1)

    if src != orig:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
        return True
    return False


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else 'HEAD~1'
    n = 0
    for folder, prefix in ((ROOT, ''), (os.path.join(ROOT, 'en'), 'en/'), (os.path.join(ROOT, 'pt'), 'pt/')):
        for name in sorted(os.listdir(folder)):
            # planes.html se regenera despues con build_planes.py, que hereda
            # el header ya corregido de construir-vs-comprar
            if not name.endswith('.html') or name == 'planes.html':
                continue
            if patch(os.path.join(folder, name), prefix + name, ref):
                n += 1
                print('  %s%s' % (prefix, name))
    print('paginas actualizadas: %d' % n)


if __name__ == '__main__':
    main()
