# -*- coding: utf-8 -*-
"""
Debajo de los planes resumidos de suite-rocketbot (es / en / pt) agrega el
paso a la pagina de planes en detalle.

    python patch_planes_cta.py
"""
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_ANCHOR = '.rb-tier .rb-btn{width:100%;justify-content:center;}'
CSS_ADD = ('\n.rb-tiers-more{text-align:center;margin-top:36px;}'
           '\n.rb-tiers-more .rb-btn{margin:0 auto;}'
           '\n.rb-tiers-more p{font-size:13.5px;color:var(--muted);margin-top:14px;}')

TXT = {
    'es': ('Ver todos los planes en detalle &#8594;',
           'Capacidad, l&#237;mites producto por producto, seguridad y soporte — comparados fila por fila.'),
    'en': ('See every plan in detail &#8594;',
           'Capacity, product-by-product limits, security and support — compared row by row.'),
    'pt': ('Ver todos os planos em detalhe &#8594;',
           'Capacidade, limites produto a produto, seguran&#231;a e suporte — comparados linha a linha.'),
}

BLOCK = """    <div class="rb-tiers-more">
      <a class="rb-btn rb-btn--primary rb-btn--lg" href="planes.html">%s</a>
      <p>%s</p>
    </div>
"""


def patch(path, lang):
    src = io.open(path, encoding='utf-8').read()
    if 'rb-tiers-more' in src:
        print('  ya estaba: %s' % path)
        return
    src = src.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_ADD, 1)

    i = src.index('id="pricing"')
    j = src.index('</section>', i)
    # cierre de la seccion: ...</div>\n    </div>\n  </div>\n</section>
    tail = '    </div>\n  </div>\n</section>'
    k = src.rindex(tail, i, j + len('</section>'))
    src = src[:k] + '    </div>\n' + BLOCK % TXT[lang] + '  </div>\n</section>' + src[k + len(tail):]

    io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
    print('  %s' % path)


def main():
    for lang, folder in (('es', ROOT), ('en', os.path.join(ROOT, 'en')), ('pt', os.path.join(ROOT, 'pt'))):
        patch(os.path.join(folder, 'suite-rocketbot.html'), lang)


if __name__ == '__main__':
    main()
