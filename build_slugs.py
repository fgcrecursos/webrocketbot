# -*- coding: utf-8 -*-
"""
Traduce los nombres de archivo de /en/ y /pt/ al idioma de cada version.

Hasta ahora las tres versiones compartian el slug espanol: /en/planes.html,
/pt/contacto.html. Este script renombra los archivos, reescribe todos los
enlaces internos, los canonical, los hreflang, el og:url, el JSON-LD y el
sitemap, y genera las redirecciones para que las URLs viejas no queden en 404.

Los nombres de producto no se traducen; la unica excepcion es Orquestador,
que ya se traduce en el resto del sitio.

    python build_slugs.py            # simulacion
    python build_slugs.py --apply    # renombra y reescribe
"""
import re, os, sys, json, shutil

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))

# slug espanol -> slug por idioma
SLUGS = {
 'index.html':                    {'en': 'index.html',                  'pt': 'index.html'},
 'suite-rocketbot.html':          {'en': 'rocketbot-suite.html',        'pt': 'suite-rocketbot.html'},
 'planes.html':                   {'en': 'pricing.html',                'pt': 'planos.html'},
 'contacto.html':                 {'en': 'contact.html',                'pt': 'contato.html'},
 'orquestador.html':              {'en': 'orchestrator.html',           'pt': 'orquestrador.html'},
 'construir-vs-comprar.html':     {'en': 'build-vs-buy.html',           'pt': 'construir-ou-comprar.html'},
 'politicas-de-privacidad.html':  {'en': 'privacy-policy.html',         'pt': 'politicas-de-privacidade.html'},
 'politicas-de-seguridad.html':   {'en': 'security-policy.html',        'pt': 'politicas-de-seguranca.html'},
 'terminos-y-condiciones.html':   {'en': 'terms-and-conditions.html',   'pt': 'termos-e-condicoes.html'},
 'partners.html':                 {'en': 'partners.html',               'pt': 'parceiros.html'},
 'faq.html':                      {'en': 'faq.html',                    'pt': 'faq.html'},
 'blog.html':                     {'en': 'blog.html',                   'pt': 'blog.html'},
 'cfo.html':                      {'en': 'cfo.html',                    'pt': 'cfo.html'},
 # nombres de producto: no se traducen
 'ai-studio.html':                {'en': 'ai-studio.html',              'pt': 'ai-studio.html'},
 'rpa-studio.html':               {'en': 'rpa-studio.html',             'pt': 'rpa-studio.html'},
 'saturn-studio.html':            {'en': 'saturn-studio.html',          'pt': 'saturn-studio.html'},
 'nexus.html':                    {'en': 'nexus.html',                  'pt': 'nexus.html'},
 'xperience.html':                {'en': 'xperience.html',              'pt': 'xperience.html'},
}

def slug(es_name, lang):
    if lang == 'es':
        return es_name
    return SLUGS[es_name][lang]

def canon_url(es_name, lang):
    s = slug(es_name, lang)
    base = 'https://rocketbot.com/'
    if lang != 'es':
        base += lang + '/'
    return base if s == 'index.html' else base + s

# ── el switcher deja de asumir que el archivo se llama igual en los 3 idiomas ─
OLD_URL_FN = "function url(l){ return l==='es' ? '/'+PAGE : '/'+l+'/'+PAGE; }"
NEW_URL_FN = ("function url(l){ var t=l==='pt'?'pt-BR':l;"
              " var a=document.querySelector('link[rel=\"alternate\"][hreflang=\"'+t+'\"]');"
              " if(a){ try{ return new URL(a.getAttribute('href'), location.href).pathname; }catch(e){} }"
              " return l==='es' ? '/'+PAGE : '/'+l+'/'+PAGE; }")


def rewrite(raw, lang):
    """Reescribe enlaces y URLs absolutas de un documento de `lang`."""
    n = 0

    # 1) enlaces internos relativos y absolutos dentro de la misma version
    for es_name, m in SLUGS.items():
        tgt = slug(es_name, lang)
        if tgt == es_name:
            continue
        prefix = '' if lang == 'es' else lang + '/'
        for pat, rep in (
            ('href="%s"' % es_name,                  'href="%s"' % tgt),
            ('href="/%s%s"' % (prefix, es_name),     'href="/%s%s"' % (prefix, tgt)),
        ):
            c = raw.count(pat)
            if c:
                raw = raw.replace(pat, rep); n += c

    # 2) URLs absolutas de cualquier idioma (canonical, hreflang, og:url, JSON-LD)
    def abs_sub(mm):
        nonlocal n
        folder, name = mm.group(1), mm.group(2)
        l = folder.strip('/') or 'es'
        if l not in ('es', 'en', 'pt') or name not in SLUGS:
            return mm.group(0)
        new = canon_url(name, l)
        if new != mm.group(0):
            n += 1
        return new
    raw = re.sub(r'https://rocketbot\.com/((?:en/|pt/)?)([a-z-]+\.html)', abs_sub, raw)

    # 3) PAGE del switcher + la funcion url()
    m = re.search(r"PAGE='([a-z-]+\.html)'", raw)
    if m and m.group(1) in SLUGS:
        tgt = slug(m.group(1), lang)
        if tgt != m.group(1):
            raw = raw.replace("PAGE='%s'" % m.group(1), "PAGE='%s'" % tgt); n += 1
    if OLD_URL_FN in raw:
        raw = raw.replace(OLD_URL_FN, NEW_URL_FN); n += 1

    return raw, n


def main():
    moves = []
    for lang in ('en', 'pt'):
        for es_name in SLUGS:
            tgt = slug(es_name, lang)
            if tgt != es_name:
                moves.append(('%s/%s' % (lang, es_name), '%s/%s' % (lang, tgt)))

    print('Renombrados (%d):' % len(moves))
    for a, b in moves:
        print('  %-38s → %s' % (a, b))

    if APPLY:
        for a, b in moves:
            src, dst = os.path.join(ROOT, a), os.path.join(ROOT, b)
            if os.path.exists(src):
                shutil.move(src, dst)

    # reescritura de contenidos
    print('\nReescritura de enlaces:')
    total = 0
    for lang, folder in (('es', '.'), ('en', 'en'), ('pt', 'pt')):
        d = os.path.join(ROOT, folder)
        for f in sorted(x for x in os.listdir(d) if x.endswith('.html') and not x.startswith('_')):
            p = os.path.join(d, f)
            raw = open(p, encoding='utf-8').read()
            new, n = rewrite(raw, lang)
            if n:
                total += n
                if APPLY:
                    open(p, 'w', encoding='utf-8', newline='').write(new)
    print('  %d referencias actualizadas' % total)

    # sitemap
    sm = os.path.join(ROOT, 'sitemap.xml')
    raw = open(sm, encoding='utf-8').read()
    new, n = rewrite(raw, 'es')
    if APPLY and n:
        open(sm, 'w', encoding='utf-8', newline='').write(new)
    print('  sitemap.xml: %d URLs' % n)

    # redirecciones para que las URLs viejas no queden en 404
    lines_nginx, redirects_vercel = [], []
    for lang in ('en', 'pt'):
        for es_name in SLUGS:
            tgt = slug(es_name, lang)
            if tgt == es_name:
                continue
            old_p, new_p = '/%s/%s' % (lang, es_name), '/%s/%s' % (lang, tgt)
            lines_nginx.append('rewrite ^%s$ %s permanent;' % (old_p.replace('.', chr(92)+'.'), new_p))
            lines_nginx.append('rewrite ^%s$ %s permanent;' % (old_p[:-5], new_p[:-5]))
            redirects_vercel.append({'source': old_p, 'destination': new_p, 'permanent': True})
            redirects_vercel.append({'source': old_p[:-5], 'destination': new_p[:-5], 'permanent': True})

    if APPLY:
        with open(os.path.join(ROOT, 'redirects-nginx.conf'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# Redirecciones 301 de los slugs viejos a los traducidos.\n'
                     '# Pegar dentro del bloque server { } de rocketbot.com.\n'
                     '# Generado por build_slugs.py — no editar a mano.\n\n')
            fh.write('\n'.join(lines_nginx) + '\n')
        vj = os.path.join(ROOT, 'vercel.json')
        cfg = json.load(open(vj, encoding='utf-8'))
        cfg['redirects'] = redirects_vercel
        json.dump(cfg, open(vj, 'w', encoding='utf-8', newline='\n'), indent=2, ensure_ascii=False)
        open(vj, 'a', encoding='utf-8', newline='\n').write('\n')

    print('\nRedirecciones: %d reglas (redirects-nginx.conf + vercel.json)' % len(redirects_vercel))
    if not APPLY:
        print('\n*** SIMULACION — nada se escribio. Correr con --apply ***')


if __name__ == '__main__':
    main()
