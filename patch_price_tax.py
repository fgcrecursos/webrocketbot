# -*- coding: utf-8 -*-
"""Aclara bajo cada precio de la Suite que los valores no incluyen los
impuestos de cada pais. planes.html lo trae desde build_planes.py; aca solo
queda suite-rocketbot.html (es/en/pt), que es HTML a mano.

Idempotente: si la tarjeta ya tiene .rb-tier__tax, no toca el archivo."""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

TAX = {
    'es': u'No incluye los impuestos de cada país',
    'en': u'Does not include each country&#8217;s taxes',
    'pt': u'Não inclui os impostos de cada país',
}

# la nota general de la seccion: se le agrega la frase de impuestos
NOTE = {
    'es': (u'Precios en dólares estadounidenses (USD).',
           u'Precios en dólares estadounidenses (USD). '
           u'No incluyen los impuestos aplicables en cada país.'),
    'en': (u'Prices in US dollars (USD).',
           u'Prices in US dollars (USD). '
           u'They do not include the taxes applicable in each country.'),
    'pt': (u'Preços em dólares americanos (US$).',
           u'Preços em dólares americanos (US$). '
           u'Não incluem os impostos aplicáveis em cada país.'),
}

CSS = (u'.rb-tier__tax{font-size:11.5px;font-weight:600;color:var(--muted);'
       u'line-height:1.35;margin:2px 0 8px;}\n')

PRICE_RE = re.compile(r'(^([ \t]*)<div class="rb-tier__price">.*?</div>$)', re.M)


def patch(lang):
    path = os.path.join(ROOT, 'suite-rocketbot.html') if lang == 'es' \
        else os.path.join(ROOT, lang, 'suite-rocketbot.html')
    src = io.open(path, encoding='utf-8').read()
    if 'rb-tier__tax' in src:
        print('ya estaba: %s' % path)
        return

    # 1) CSS, justo despues de la regla del precio
    anchor = u'.rb-tier__price .per{font-size:14px;font-weight:600;color:var(--muted);}\n'
    assert anchor in src, path
    src = src.replace(anchor, anchor + CSS, 1)

    # 2) una linea de impuestos bajo cada precio
    src, n = PRICE_RE.subn(
        lambda m: u'%s\n%s<div class="rb-tier__tax">%s</div>'
                  % (m.group(1), m.group(2), TAX[lang]), src)
    assert n == 4, '%s: %d precios' % (path, n)

    # 3) la nota al pie de la cabecera de la seccion
    old, new = NOTE[lang]
    assert old in src, path
    src = src.replace(old, new, 1)

    # 4) subgrid: las tarjetas pasan de 7 a 8 filas
    src = src.replace(u'grid-template-rows:subgrid;grid-row:span 7;',
                      u'grid-template-rows:subgrid;grid-row:span 8;')
    src = src.replace(u'@media(min-width:981px){.rb-tiers{grid-template-rows:repeat(7,auto);}}',
                      u'@media(min-width:981px){.rb-tiers{grid-template-rows:repeat(8,auto);}}')
    src = src.replace(u'@media(min-width:561px) and (max-width:980px){.rb-tiers{grid-template-rows:repeat(14,auto);}}',
                      u'@media(min-width:561px) and (max-width:980px){.rb-tiers{grid-template-rows:repeat(16,auto);}}')

    io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
    print('parcheado %s' % path)


if __name__ == '__main__':
    for lg in ('es', 'en', 'pt'):
        patch(lg)
