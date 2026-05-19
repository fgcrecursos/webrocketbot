import re, os
os.chdir(r'C:\Users\frani\.claude\worktrees\quirky-aryabhata-b7856b')

FILES = ['index.html','saturn-studio.html','rpa-studio.html','ai-studio.html',
         'orquestador.html','xperience.html','contacto.html','blog.html']

# ── CSS to inject (before </style>) ───────────────────────────────────────────
LANG_CSS = """
/* LANGUAGE SWITCHER */
.rb-lang{position:relative;}
.rb-lang__menu{position:absolute;top:calc(100% + 10px);right:0;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:14px;padding:6px;min-width:148px;box-shadow:0 16px 40px rgba(0,0,0,.12);opacity:0;pointer-events:none;transition:opacity .2s,transform .18s;transform:translateY(-6px);z-index:200;}
[data-theme="dark"] .rb-lang__menu{background:var(--rb-dark-2);border-color:rgba(255,255,255,.08);}
.rb-lang__menu.open{opacity:1;pointer-events:auto;transform:translateY(0);}
.rb-lang__opt{display:flex;align-items:center;gap:8px;padding:9px 14px;border-radius:9px;font-size:13px;font-weight:600;color:#333;cursor:pointer;transition:background .15s,color .15s;border:none;background:none;width:100%;font-family:inherit;text-align:left;}
[data-theme="dark"] .rb-lang__opt{color:rgba(255,255,255,.75);}
.rb-lang__opt:hover{background:rgba(188,0,23,.07);color:var(--rb-red);}
.rb-lang__opt.rb-lang--active{color:var(--rb-red);background:rgba(188,0,23,.05);}
/* Hide Google Translate toolbar */
.goog-te-banner-frame,.goog-te-gadget,.goog-te-gadget-icon,#goog-gt-tt,.goog-te-balloon-frame,.goog-tooltip,.goog-tooltip:hover,.skiptranslate{display:none !important;height:0 !important;}
body{top:0 !important;}
.goog-text-highlight{background:none !important;box-shadow:none !important;}
"""

# ── Language button HTML ───────────────────────────────────────────────────────
LANG_BTN = '''<div class="rb-lang" id="rb-lang">
      <button class="rb-iconbtn" id="rb-lang-btn" title="Idioma" type="button" aria-haspopup="true" aria-expanded="false">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
      </button>
      <div class="rb-lang__menu" id="rb-lang-menu" role="menu">
        <button class="rb-lang__opt rb-lang--active" data-lang="es" type="button">🇪🇸 Español</button>
        <button class="rb-lang__opt" data-lang="en" type="button">🇺🇸 English</button>
        <button class="rb-lang__opt" data-lang="pt" type="button">🇧🇷 Português</button>
      </div>
    </div>'''

# ── Google Translate init (before </body>) ────────────────────────────────────
GT_SCRIPT = """
<!-- Google Translate -->
<div id="google_translate_element" style="display:none;visibility:hidden;position:absolute;"></div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({
    pageLanguage:'es',
    includedLanguages:'es,en,pt',
    autoDisplay:false
  },'google_translate_element');
}
</script>
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" async defer></script>
"""

# ── Language switcher JS (before </body>) ─────────────────────────────────────
LANG_JS = """
<script>
/* Language Switcher */
(function(){
  var btn  = document.getElementById('rb-lang-btn');
  var menu = document.getElementById('rb-lang-menu');
  if(!btn || !menu) return;

  btn.addEventListener('click', function(e){
    e.stopPropagation();
    var open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
  document.addEventListener('click', function(){
    menu.classList.remove('open');
    btn.setAttribute('aria-expanded','false');
  });

  function setLang(lang){
    try{ localStorage.setItem('rb-lang', lang); }catch(e){}
    menu.querySelectorAll('.rb-lang__opt').forEach(function(o){
      o.classList.toggle('rb-lang--active', o.dataset.lang === lang);
    });
    menu.classList.remove('open');
    btn.setAttribute('aria-expanded','false');

    if(lang === 'es'){
      var exp0 = new Date(0).toUTCString();
      document.cookie = 'googtrans=; path=/; expires=' + exp0;
      document.cookie = 'googtrans=; path=/; domain=.' + location.hostname + '; expires=' + exp0;
      location.reload();
      return;
    }
    // Try live Google Translate select
    var sel = document.querySelector('.goog-te-combo');
    if(sel){
      sel.value = lang;
      sel.dispatchEvent(new Event('change'));
    } else {
      var exp1 = new Date(); exp1.setFullYear(exp1.getFullYear()+1);
      var expStr = exp1.toUTCString();
      document.cookie = 'googtrans=/es/'+lang+'; path=/; expires='+expStr;
      document.cookie = 'googtrans=/es/'+lang+'; path=/; domain=.'+location.hostname+'; expires='+expStr;
      location.reload();
    }
  }

  menu.querySelectorAll('.rb-lang__opt').forEach(function(o){
    o.addEventListener('click', function(){ setLang(o.dataset.lang); });
  });

  // Restore saved preference
  var saved = 'es';
  try{ saved = localStorage.getItem('rb-lang') || 'es'; }catch(e){}
  menu.querySelectorAll('.rb-lang__opt').forEach(function(o){
    o.classList.toggle('rb-lang--active', o.dataset.lang === saved);
  });
  if(saved !== 'es' && document.cookie.indexOf('googtrans') === -1){
    document.cookie = 'googtrans=/es/'+saved+'; path=/';
  }
})();
</script>
"""

# ── Old standalone lang button (index.html only) ──────────────────────────────
OLD_LANG_BTN_IDX = (
    '<button class="rb-iconbtn" title="Idioma" type="button">\n'
    '        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" '
    'stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"/>'
    '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>'
    '<path d="M2 12h20"/></svg>\n'
    '      </button>'
)

# Anchor to insert language btn before (common to all pages)
THEME_BTN_ANCHOR_IDX  = '<button class="rb-iconbtn" id="theme-btn" title="Cambiar tema" type="button">'
# Minified version for product pages
THEME_BTN_ANCHOR_MINI = '<button class="rb-iconbtn" id="theme-btn" title="Cambiar tema" type="button">'

for fname in FILES:
    if not os.path.exists(fname):
        print(f'{fname}: not found, skipping')
        continue

    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Inject CSS
    if 'rb-lang__menu' not in content:
        content = content.replace('</style>', LANG_CSS + '\n</style>', 1)
        changed = True

    # 2. Handle language button
    if 'id="rb-lang-btn"' not in content:
        if fname == 'index.html' and OLD_LANG_BTN_IDX in content:
            # Replace existing standalone button with full dropdown
            content = content.replace(OLD_LANG_BTN_IDX, LANG_BTN, 1)
            changed = True
        else:
            # Insert before theme button (works for both formatted and minified)
            anchor = THEME_BTN_ANCHOR_IDX
            if anchor in content:
                content = content.replace(anchor, LANG_BTN + '\n      ' + anchor, 1)
                changed = True
            else:
                print(f'  WARNING: theme-btn anchor not found in {fname}')

    # 3. Inject Google Translate script
    if 'googleTranslateElementInit' not in content:
        content = content.replace('</body>', GT_SCRIPT + LANG_JS + '\n</body>', 1)
        changed = True
    elif 'rb-lang' in content and '/* Language Switcher */' not in content:
        # CSS/btn already there but JS missing
        content = content.replace('</body>', LANG_JS + '\n</body>', 1)
        changed = True

    if changed:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

    has_css = 'rb-lang__menu' in content
    has_btn = 'id="rb-lang-btn"' in content
    has_js  = '/* Language Switcher */' in content
    print(f'{fname}: CSS={has_css} BTN={has_btn} JS={has_js}')

print('\nDone.')
