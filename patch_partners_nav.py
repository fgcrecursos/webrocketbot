# -*- coding: utf-8 -*-
"""
Patch de navegacion para las 42 paginas (es + /en/ + /pt/). Tres cambios:

  1) Los desplegables del header (Productos, Recursos, Soporte y servicios) ahora
     tambien abren al CLIC, no solo al hover. Antes eran hover-only y en pantallas
     sin hover / al clickear el boton no pasaba nada. Se inyecta un <script> que
     alterna la clase .rb-dd-open y una regla CSS que muestra el desplegable.
  2) En "Soporte y servicios" se agrega el acceso de login de partners:
       https://partners.rocketbot.com/wp-login.php
  3) En "Soporte y servicios" se agrega un boton destacado "Quiero ser partner"
     que abre la landing partners.html. Tambien en el menu movil.

Idempotente: cada bloque se guarda por un marcador y se saltea si ya esta.

    python patch_partners_nav.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGIN_URL = 'https://partners.rocketbot.com/wp-login.php'

PARTNER_CTA   = {'es': 'Quiero ser partner', 'en': 'Become a partner', 'pt': 'Quero ser parceiro'}
PARTNER_LOGIN = {'es': 'Login de Partners',  'en': 'Partner Login',    'pt': 'Login de Parceiros'}

# --- CSS que se inyecta antes de </head> ---
DDNAV_CSS = """
<style id="rb-ddnav-css">
.rb-nav__item--dropdown.rb-dd-open>.rb-nav__dropdown{opacity:1 !important;pointer-events:auto !important;transform:translate(-50%,0) !important;}
.rb-nav__dd-cta{display:flex !important;align-items:center;justify-content:center;gap:6px;margin:2px 4px 8px;padding:11px 16px !important;background:linear-gradient(110deg,#FF2942,#BC0017);color:#fff !important;font-weight:800 !important;border-radius:10px;box-shadow:0 6px 16px rgba(188,0,23,.32);transition:filter .2s,transform .2s;}
.rb-nav__dd-cta:hover{color:#fff !important;filter:brightness(1.07);transform:translateY(-1px);background:linear-gradient(110deg,#FF2942,#BC0017) !important;}
.rb-nav__dd-login{color:var(--rb-red) !important;font-weight:700 !important;}
[data-theme="dark"] .rb-nav__dd-login{color:#FF5A6E !important;}
.rb-mobile-menu__partner{color:var(--rb-red) !important;font-weight:800 !important;}
[data-theme="dark"] .rb-mobile-menu__partner{color:#FF5A6E !important;}
</style>
"""

# --- JS que se inyecta antes de </body> ---
DDNAV_JS = """
<script id="rb-ddnav-js">
(function(){
  var items = Array.prototype.slice.call(document.querySelectorAll('.rb-nav__item--dropdown'));
  if(!items.length) return;
  function closeAll(except){
    items.forEach(function(o){
      if(o===except) return;
      o.classList.remove('rb-dd-open');
      var b=o.querySelector(':scope > button');
      if(b) b.setAttribute('aria-expanded','false');
    });
  }
  items.forEach(function(li){
    var btn = li.querySelector(':scope > button');
    if(!btn) return;
    btn.setAttribute('aria-haspopup','true');
    btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click', function(e){
      e.preventDefault(); e.stopPropagation();
      var open = !li.classList.contains('rb-dd-open');
      closeAll(li);
      li.classList.toggle('rb-dd-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function(e){
    if(e.target.closest && e.target.closest('.rb-nav__item--dropdown')) return;
    closeAll(null);
  });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') closeAll(null); });
})();
</script>
"""

# desplegable de Soporte y servicios: primer enlace = foro (igual en los 3 idiomas)
SUP_DD = re.compile(
    r'(<div class="rb-nav__dropdown">)(\s*<a href="https://forum\.rocketbot\.com".*?)(</div>)', re.S)
# seccion movil de Soporte: label + enlaces, hasta el cierre de la seccion
MOB_SUP = re.compile(
    r'(<div class="rb-mobile-menu__label">[^<]*</div>\s*<a href="https://forum\.rocketbot\.com"[^>]*>.*?)(</div>)', re.S)


def dd_cta(lang):
    return '<a href="partners.html" class="rb-nav__dd-cta">✦ %s</a>' % PARTNER_CTA[lang]


def dd_login(lang):
    return '<a href="%s" target="_blank" rel="noopener" class="rb-nav__dd-login">%s →</a>' % (LOGIN_URL, PARTNER_LOGIN[lang])


def patch(path, lang):
    src = io.open(path, encoding='utf-8').read()
    orig = src

    # 1) CSS
    if 'rb-ddnav-css' not in src:
        src = src.replace('</head>', DDNAV_CSS + '</head>', 1)

    # 2) desplegable desktop: CTA arriba, login abajo
    if 'href="partners.html" class="rb-nav__dd-cta"' not in src:
        def rep(m):
            return (m.group(1)
                    + '\n          ' + dd_cta(lang)
                    + m.group(2)
                    + '\n          ' + dd_login(lang) + '\n        '
                    + m.group(3))
        src2 = SUP_DD.sub(rep, src, count=1)
        if src2 == src:
            print('  [!] sin desplegable de Soporte en %s' % path)
        src = src2

    # 3) menu movil
    if 'class="rb-mobile-menu__partner"' not in src:
        mob = ('\n      <a href="partners.html" class="rb-mobile-menu__partner">%s</a>'
               '\n      <a href="%s" target="_blank" rel="noopener">%s</a>\n    '
               % (PARTNER_CTA[lang], LOGIN_URL, PARTNER_LOGIN[lang]))
        src = MOB_SUP.sub(lambda m: m.group(1) + mob + m.group(2), src, count=1)

    # 4) JS click-to-open
    if 'rb-ddnav-js' not in src:
        src = src.replace('</body>', DDNAV_JS + '</body>', 1)

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
            if patch(os.path.join(folder, name), lang):
                n += 1
                print('  %s/%s' % (lang, name))
    print('paginas actualizadas: %d' % n)


if __name__ == '__main__':
    main()
