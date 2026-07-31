# -*- coding: utf-8 -*-
"""
Patch idempotente sobre TODAS las paginas HTML (es/en/pt):

1) Quita el link "Media kit" (header dropdown, mobile menu, footer) en
   cualquiera de sus variantes de href.
2) Agrega FAQs y Terminos y condiciones al dropdown "Soporte y servicios"
   del header y al mobile menu.
3) Conecta los links de Politicas de privacidad / Politicas de seguridad
   (footer "Empresa" y footer bottom "legal") que hoy apuntan a href="#".
4) Conecta el link "FAQs" de la columna "Soporte y servicios" del footer.

Se ejecuta sobre todos los .html del repo (raiz, en/, pt/), incluyendo las
paginas nuevas (faq.html, terminos-y-condiciones.html, politicas-de-*.html)
para que tambien tengan su propio nav consistente.

    python patch_support_nav.py
"""
import glob
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

LABELS = {
 'es': {'faq': 'FAQs', 'tyc': 'Términos y condiciones'},
 'en': {'faq': 'FAQs', 'tyc': 'Terms & Conditions'},
 'pt': {'faq': 'FAQs', 'tyc': 'Termos e condições'},
}

MEDIA_KIT_LI_RE = re.compile(r'\s*<li>\s*<a href="[^"]*"[^>]*>Media [Kk]it</a>\s*</li>')
MEDIA_KIT_A_RE = re.compile(r'\s*<a href="[^"]*"(?: target="_blank" rel="noopener")?>Media [Kk]it</a>')

# header dropdown: insert right before the "Login de Partners" link
HEADER_LOGIN_RE = re.compile(r'(<a href="https://partners\.rocketbot\.com/wp-login\.php" target="_blank" rel="noopener" class="rb-nav__dd-login">)')
# mobile menu: insert right before the "Quiero ser partner" mobile CTA
MOBILE_PARTNER_RE = re.compile(r'(\s*<a href="partners\.html" class="rb-mobile-menu__partner">)')


def detect_lang(path):
    parts = path.replace(ROOT, '').replace('\\', '/').strip('/').split('/')
    if parts and parts[0] == 'en':
        return 'en'
    if parts and parts[0] == 'pt':
        return 'pt'
    return 'es'


def patch(path):
    lang = detect_lang(path)
    lbl = LABELS[lang]
    src = io.open(path, encoding='utf-8').read()
    orig = src
    is_new_legal_page = os.path.basename(path) in (
        'faq.html', 'terminos-y-condiciones.html',
        'politicas-de-privacidad.html', 'politicas-de-seguridad.html')

    # 1) quitar Media kit (footer <li>, luego cualquier <a> suelta restante)
    src = MEDIA_KIT_LI_RE.sub('', src)
    src = MEDIA_KIT_A_RE.sub('', src)

    # 2) agregar FAQs + T&C al header dropdown (si no estan ya)
    if 'href="faq.html" class="rb-nav__dd-faq"' not in src:
        def header_ins(m):
            return ('<a href="faq.html" class="rb-nav__dd-faq">%s</a>'
                    '<a href="terminos-y-condiciones.html" class="rb-nav__dd-tyc">%s</a>' % (lbl['faq'], lbl['tyc'])) + m.group(1)
        new_src, n = HEADER_LOGIN_RE.subn(header_ins, src, count=1)
        if n:
            src = new_src

    # 2b) agregar al mobile menu (si no estan ya)
    if 'class="rb-mobile-menu__faq"' not in src:
        def mobile_ins(m):
            return ('\n      <a href="faq.html" class="rb-mobile-menu__faq">%s</a>'
                    '\n      <a href="terminos-y-condiciones.html" class="rb-mobile-menu__tyc">%s</a>' % (lbl['faq'], lbl['tyc'])) + m.group(1)
        new_src, n = MOBILE_PARTNER_RE.subn(mobile_ins, src, count=1)
        if n:
            src = new_src

    # 3) conectar links de privacidad/seguridad (footer Empresa + footer bottom)
    src = src.replace('<a href="#">Políticas de privacidad</a>', '<a href="politicas-de-privacidad.html">Políticas de privacidad</a>')
    src = src.replace('<a href="#">Políticas de seguridad</a>', '<a href="politicas-de-seguridad.html">Políticas de seguridad</a>')
    src = src.replace('<a href="#">Privacy policy</a>', '<a href="politicas-de-privacidad.html">Privacy policy</a>')
    src = src.replace('<a href="#">Security policy</a>', '<a href="politicas-de-seguridad.html">Security policy</a>')
    src = src.replace('<a href="#">Políticas de privacidade</a>', '<a href="politicas-de-privacidad.html">Políticas de privacidade</a>')
    src = src.replace('<a href="#">Políticas de segurança</a>', '<a href="politicas-de-seguridad.html">Políticas de segurança</a>')

    # 4) conectar FAQs del footer "Soporte y servicios"
    src = re.sub(r'<li><a href="#">FAQs?</a></li>', '<li><a href="faq.html">%s</a></li>' % lbl['faq'], src)

    # 5) agregar T&C al footer "Empresa/Company" junto a privacidad/seguridad
    if 'class="rb-footer__tyc"' not in src:
        for seg_txt in ('Políticas de seguridad', 'Security policy', 'Políticas de segurança'):
            marker = '<li><a href="politicas-de-seguridad.html">%s</a></li>' % seg_txt
            if marker in src:
                src = src.replace(
                    marker,
                    marker + '<li><a href="terminos-y-condiciones.html" class="rb-footer__tyc">%s</a></li>' % lbl['tyc'],
                    1)
                break

    if is_new_legal_page:
        # las paginas nuevas no deben auto-referenciarse con is-current visual extra;
        # no-op por ahora, dejamos el link normal.
        pass

    if src != orig:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
        return True
    return False


def main():
    files = []
    for pattern in ('*.html', 'en/*.html', 'pt/*.html'):
        files.extend(glob.glob(os.path.join(ROOT, pattern)))
    changed = 0
    for f in sorted(files):
        if patch(f):
            changed += 1
    print('patched %d / %d files' % (changed, len(files)))


if __name__ == '__main__':
    main()
