# -*- coding: utf-8 -*-
"""
Tres parches sobre las 54 paginas:

  1. Formularios de Clientify por idioma en la pagina de contacto.
  2. Redes sociales del footer, cada idioma con sus propias cuentas.
  3. Boton flotante de WhatsApp en la esquina inferior derecha.

Idempotente y re-ejecutable.

    python patch_social_wa.py            # simulacion
    python patch_social_wa.py --apply    # escribe
"""
import re, os, sys
from urllib.parse import quote

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))

# ── 1. Clientify ────────────────────────────────────────────────────────────
# Cada idioma con su propio superform. El espanol conserva el original.
CLIENTIFY = {'es': '251784', 'en': '296117', 'pt': '297756'}

# ── 2. Redes sociales ───────────────────────────────────────────────────────
ICON = {
 'facebook': '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>',
 'instagram': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
 'linkedin': '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>',
 'youtube': '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 0 0-1.95 1.96A29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58A2.78 2.78 0 0 0 3.41 19.6C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.95A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="#1a242a"/></svg>',
}

# Solo las cuentas que existen en cada idioma. El TikTok en espanol queda fuera
# a pedido de Frani: la cuenta esta sin uso.
SOCIAL = {
 'es': [('Facebook',  'facebook',  'https://www.facebook.com/rocketbot.es'),
        ('Instagram', 'instagram', 'https://www.instagram.com/rocketbot_es/'),
        ('LinkedIn',  'linkedin',  'https://www.linkedin.com/company/rocketrobot/'),
        ('YouTube',   'youtube',   'https://www.youtube.com/@Rocketbot_Plataforma')],
 'en': [('Facebook',  'facebook',  'https://www.facebook.com/profile.php?id=61591945872705'),
        ('Instagram', 'instagram', 'https://www.instagram.com/rocketbothq/')],
 'pt': [('Facebook',  'facebook',  'https://www.facebook.com/profile.php?id=61586735514304'),
        ('LinkedIn',  'linkedin',  'https://www.linkedin.com/company/rocketbot-br/')],
}

def social_block(lang):
    out = ['<div class="rb-footer__social">']
    for label, icon, href in SOCIAL[lang]:
        out.append('          <a href="%s" target="_blank" rel="noopener" aria-label="%s">\n            %s\n          </a>'
                   % (href, label, ICON[icon]))
    out.append('        </div>')
    return '\n'.join(out)

# ── 3. WhatsApp ─────────────────────────────────────────────────────────────
WA_NUMBER = '56972518446'          # +56 9 7251 8446
WA_TEXT = {
 'es': 'Hola, quiero saber más sobre Rocketbot.',
 'en': "Hi, I'd like to know more about Rocketbot.",
 'pt': 'Olá, quero saber mais sobre a Rocketbot.',
}
WA_LABEL = {'es': 'Escríbenos por WhatsApp', 'en': 'Message us on WhatsApp', 'pt': 'Fale conosco pelo WhatsApp'}

WA_CSS = """<style id="rb-wa-css">
.rb-wa{
  position:fixed;right:20px;bottom:20px;z-index:60;
  width:56px;height:56px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:#25D366;color:#fff;
  box-shadow:0 6px 20px rgba(0,0,0,.28);
  transition:transform .2s,box-shadow .2s;
}
.rb-wa:hover{transform:scale(1.06);box-shadow:0 10px 26px rgba(0,0,0,.34);}
.rb-wa:active{transform:scale(.98);}
.rb-wa:focus-visible{outline:3px solid #fff;outline-offset:3px;}
.rb-wa svg{width:30px;height:30px;display:block;}
@media(max-width:600px){.rb-wa{right:14px;bottom:14px;width:52px;height:52px;}.rb-wa svg{width:27px;height:27px;}}
@media(prefers-reduced-motion:reduce){.rb-wa{transition:none;}.rb-wa:hover{transform:none;}}
@media print{.rb-wa{display:none;}}
</style>"""

def wa_block(lang):
    return ('<!-- rb-wa -->\n<a class="rb-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener" aria-label="%s" title="%s">'
            '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.56 4.19 1.62 6.02L4 29l8.13-1.58a12 12 0 0 0 3.9.66h.01C22.68 28.08 28 22.68 28 16.04 28 9.4 22.68 3 16.04 3zm0 22.02h-.01a10 10 0 0 1-5.09-1.4l-.36-.21-4.82.94.96-4.7-.24-.38a9.96 9.96 0 0 1-1.53-5.33c0-5.5 4.48-9.98 10-9.98 5.51 0 9.99 4.48 9.99 9.98 0 5.51-4.48 10.08-8.9 11.08zm5.48-7.47c-.3-.15-1.77-.87-2.05-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.06 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35z"/></svg>'
            '</a>' % (WA_NUMBER, quote(WA_TEXT[lang]), WA_LABEL[lang], WA_LABEL[lang]))


def close_div(html, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    return -1


def patch(path, lang):
    raw = open(path, encoding='utf-8').read()
    changed = []

    # 1) Clientify solo en la pagina de contacto
    if os.path.basename(path) == 'contacto.html':
        want = CLIENTIFY[lang]
        new, n = re.subn(r'(superforms/script/)\d+(\.js)', r'\g<1>%s\g<2>' % want, raw)
        if n and new != raw:
            raw = new
            changed.append('clientify→%s' % want)

    # 2) redes del footer
    i = raw.find('<div class="rb-footer__social">')
    if i >= 0:
        j = close_div(raw, i)
        block = social_block(lang)
        if raw[i:j] != block:
            raw = raw[:i] + block + raw[j:]
            changed.append('redes (%d)' % len(SOCIAL[lang]))

    # 3) WhatsApp
    if 'rb-wa-css' not in raw:
        k = raw.find('</head>')
        if k < 0: return changed + ['sin </head>']
        raw = raw[:k] + WA_CSS + '\n' + raw[k:]
        changed.append('wa css')
    m = re.search(r'(?s)<!-- rb-wa -->\s*<a class="rb-wa".*?</a>', raw)
    want = wa_block(lang)
    if m:
        if m.group(0) != want:
            raw = raw[:m.start()] + want + raw[m.end():]
            changed.append('wa (actualizado)')
    else:
        k = raw.rfind('</body>')
        if k < 0: return changed + ['sin </body>']
        raw = raw[:k] + want + '\n' + raw[k:]
        changed.append('wa')

    if changed and APPLY:
        open(path, 'w', encoding='utf-8', newline='').write(raw)
    return changed


def main():
    total = 0
    for lang, folder in (('es', '.'), ('en', 'en'), ('pt', 'pt')):
        d = os.path.join(ROOT, folder)
        for f in sorted(x for x in os.listdir(d) if x.endswith('.html') and not x.startswith('_')):
            ch = patch(os.path.join(d, f), lang)
            if ch:
                total += 1
                rel = f if folder == '.' else folder + '/' + f
                print('  %-36s %s' % (rel, ', '.join(ch)))
    print('\n%d paginas %s' % (total, 'modificadas' if APPLY else 'a modificar (SIMULACION)'))


if __name__ == '__main__':
    main()
