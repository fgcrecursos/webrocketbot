# -*- coding: utf-8 -*-
"""
Agrega los requisitos minimos de sistema operativo al modal de descargas.

Ojo: el modal de descargas NO vive solo en suite-rocketbot.html, esta embebido
en las 54 paginas del sitio (3 acordeones: Windows / macOS / Linux). Por eso
este patcher recorre todo el repo y no un archivo puntual.

Los requisitos van FUERA de .rb-dlmodal__vwrap (que arranca colapsado con
max-height:0), asi se leen sin tener que desplegar el acordeon.

Idempotente: si la pagina ya tiene .rb-dlmodal__osreq, no la vuelve a tocar.

    python patch_dl_os_reqs.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_ANCHOR = ('.rb-dlmodal__vwrap{max-height:0;overflow:hidden;opacity:0;'
              'transition:max-height .4s cubic-bezier(.4,0,.2,1),opacity .3s ease;}')
CSS_BLOCK = ("\n.rb-dlmodal__osreq{display:flex;align-items:flex-start;gap:8px;font-size:11.5px;"
             "line-height:1.5;color:var(--muted);padding:0 0 13px;margin-top:-6px;}"
             "\n.rb-dlmodal__osreq svg{width:13px;height:13px;flex:0 0 auto;margin-top:2px;"
             "color:var(--rb-green,#1D9E75);}"
             "\n.rb-dlmodal__osreq b{color:var(--foreground);font-weight:700;}")

ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>')

REQS = {
    'es': {
        'windows': 'Requiere <b>Windows 10</b> o superior &middot; <b>Windows Server 2016</b> o superior',
        'macos':   'Requiere <b>macOS 11</b> (Big Sur) o superior',
        'linux':   'Requiere <b>Ubuntu 20.04 LTS</b> o superior &middot; <b>RHEL 8</b> o superior',
    },
    'en': {
        'windows': 'Requires <b>Windows 10</b> or higher &middot; <b>Windows Server 2016</b> or higher',
        'macos':   'Requires <b>macOS 11</b> (Big Sur) or higher',
        'linux':   'Requires <b>Ubuntu 20.04 LTS</b> or higher &middot; <b>RHEL 8</b> or higher',
    },
    'pt': {
        'windows': 'Requer <b>Windows 10</b> ou superior &middot; <b>Windows Server 2016</b> ou superior',
        'macos':   'Requer <b>macOS 11</b> (Big Sur) ou superior',
        'linux':   'Requer <b>Ubuntu 20.04 LTS</b> ou superior &middot; <b>RHEL 8</b> ou superior',
    },
}

# oshead ... </div> seguido directamente del vwrap = grupo todavia sin requisitos
GROUP_RE = re.compile(
    r'(<div class="rb-dlmodal__oshead">.*?</div>)(\s*\n)([ \t]*)<div class="rb-dlmodal__vwrap">',
    re.S
)
TAGS_RE = re.compile(r'<[^>]+>')


def lang_of(path):
    norm = path.replace('\\', '/')
    if '/en/' in norm:
        return 'en'
    if '/pt/' in norm:
        return 'pt'
    return 'es'


def which_os(oshead_html):
    label = TAGS_RE.sub('', oshead_html).strip().lower()
    if 'windows' in label:
        return 'windows'
    if 'macos' in label:
        return 'macos'
    if 'linux' in label:
        return 'linux'
    raise SystemExit('SO no reconocido en oshead: %r' % label[:60])


def patch(path):
    with io.open(path, encoding='utf-8') as f:
        src = f.read()

    if 'rb-dlmodal__osgroup' not in src:
        return 0
    if 'rb-dlmodal__osreq' in src:
        return 0  # ya patcheada

    if src.count(CSS_ANCHOR) != 1:
        raise SystemExit('ancla CSS no encontrada 1 vez en %s' % path)
    src = src.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_BLOCK, 1)

    lang = lang_of(path)

    def repl(m):
        oshead, gap, indent = m.group(1), m.group(2), m.group(3)
        text = REQS[lang][which_os(oshead)]
        return ('%s%s%s<div class="rb-dlmodal__osreq">%s<span>%s</span></div>\n'
                '%s<div class="rb-dlmodal__vwrap">'
                % (oshead, gap, indent, ICON, text, indent))

    src, n = GROUP_RE.subn(repl, src)
    if n != 3:
        raise SystemExit('esperaba 3 acordeones en %s, patchee %d' % (path, n))

    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    return n


def main():
    touched = 0
    groups = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in sorted(filenames):
            if not fn.endswith('.html'):
                continue
            n = patch(os.path.join(dirpath, fn))
            if n:
                touched += 1
                groups += n
    print('paginas patcheadas: %d (acordeones: %d)' % (touched, groups))


if __name__ == '__main__':
    main()
