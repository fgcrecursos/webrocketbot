# -*- coding: utf-8 -*-
"""
Suma el acceso a /planes en las 39 paginas (es + /en/ + /pt/):

  · header  — boton propio "Planes", pastilla contorneada al lado de "✦ Suite"
  · menu mobile — boton "Planes y precios"
  · footer  — enlace en la columna de Recursos

Y aprieta un poco los enlaces para hacerle lugar (gap 28px -> 19px). El resto
del reacomodo del header — que los dos botones convivan sin desbordar — vive en
patch_cfo_restore.py, que es donde esta el corte de 1560px.

  · en /planes el CTA del header pasa a ser el de descarga, el mismo del
    resto del sitio (heredaba "Hablemos de tu caso" del esqueleto).

Es idempotente: si la pagina ya esta al dia, la saltea.

    python patch_planes_nav.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_ANCHOR = '@media(max-width:1260px){.rb-nav__suite-li{display:none !important;}}'
CSS_ADD = """
.rb-nav__plans-li{display:flex;align-items:center;flex:0 0 auto;}
.rb-nav__plans-hdr{display:inline-flex !important;align-items:center;gap:6px;padding:8px 17px !important;border:1.5px solid rgba(188,0,23,.55);border-radius:9999px;white-space:nowrap;line-height:1;flex:0 0 auto;color:var(--rb-red) !important;font-weight:800 !important;font-size:13px !important;transition:background .2s,color .2s,border-color .2s,transform .2s;}
[data-theme="dark"] .rb-nav__plans-hdr{color:#FF5A6E !important;border-color:rgba(255,90,110,.55);}
.rb-nav__plans-hdr:hover{background:var(--rb-red);border-color:var(--rb-red);color:#fff !important;transform:translateY(-1px);}
.rb-nav__plans-hdr[aria-current="page"]{background:var(--rb-red);border-color:var(--rb-red);color:#fff !important;}
@media(max-width:1260px){.rb-nav__plans-li{display:none !important;}}"""

NAV_LABEL = {'es': 'Planes', 'en': 'Plans', 'pt': 'Planos'}
LONG_LABEL = {'es': 'Planes y precios', 'en': 'Plans and pricing', 'pt': 'Planos e preços'}
DL_LABEL = {'es': 'Descarga', 'en': 'Download', 'pt': 'Download'}
SUITE_LI = re.compile(r'<li class="rb-nav__suite-li">.*?</li>', re.S)
NAV_GAP = re.compile(r'(\.rb-nav__links\s*\{[^}]*?gap:\s*)28px')
PLANES_CTA = re.compile(r'<a href="contacto\.html" class="rb-btn rb-btn--primary">[^<]*</a>(\s*</div>\s*</div>\s*</nav>)')
MOBILE_SUITE = re.compile(r'(<div class="rb-mobile-menu__actions">\s*<a href="suite-rocketbot\.html"[^>]*>[^<]*</a>)', re.S)
FOOTER_RES = re.compile(r'(<h6[^>]*>(?:Recursos|Resources)</h6>(\s*)<ul>)')


def patch(path, lang, is_planes):
    src = io.open(path, encoding='utf-8').read()
    orig = src

    # 1) estilos del boton
    if 'rb-nav__plans-hdr' not in src:
        src = src.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_ADD, 1)

    # 2) header: pastilla propia, justo despues de "✦ Suite"
    if 'class="rb-nav__plans-li"' not in src:
        cur = ' aria-current="page"' if is_planes else ''
        li = ('\n      <li class="rb-nav__plans-li"><a href="planes.html" '
              'class="rb-nav__plans-hdr"%s>%s</a></li>' % (cur, NAV_LABEL[lang]))
        m = SUITE_LI.search(src)
        if not m:
            raise SystemExit('sin <li> de Suite en %s' % path)
        src = src[:m.end()] + li + src[m.end():]

    # 3) menu mobile
    if '<a href="planes.html" class="rb-mobile-menu__btn">' not in src:
        btn = ('\n      <a href="planes.html" class="rb-mobile-menu__btn">%s</a>' % LONG_LABEL[lang])
        src = MOBILE_SUITE.sub(lambda m: m.group(1) + btn, src, count=1)

    # 4) footer, columna de recursos
    if '<li><a href="planes.html">' not in src:
        def _foot(m):
            indent = m.group(2) if '\n' in m.group(2) else ''
            item = '<li><a href="planes.html">%s</a></li>' % LONG_LABEL[lang]
            return m.group(1) + (indent + '  ' + item if indent else item)
        src = FOOTER_RES.sub(_foot, src, count=1)

    # 5) enlaces un poco mas juntos para que entre el boton nuevo
    src = NAV_GAP.sub(lambda m: m.group(1) + '19px', src, count=1)

    # 6) en /planes, el CTA del header es el de descarga como en el resto
    if is_planes:
        src = PLANES_CTA.sub(
            lambda m: '<button type="button" class="rb-btn rb-btn--primary" data-dl-open>%s</button>%s'
                      % (DL_LABEL[lang], m.group(1)), src, count=1)

    if src != orig:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
        return True
    return False


def main():
    n = 0
    for lang, folder in (('es', ROOT), ('en', os.path.join(ROOT, 'en')), ('pt', os.path.join(ROOT, 'pt'))):
        for name in sorted(os.listdir(folder)):
            if not name.endswith('.html'):
                continue
            if patch(os.path.join(folder, name), lang, name == 'planes.html'):
                n += 1
                print('  %s/%s' % (lang, name))
    print('paginas actualizadas: %d' % n)


if __name__ == '__main__':
    main()
