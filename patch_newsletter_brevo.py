# -*- coding: utf-8 -*-
"""Conecta el formulario de newsletter al formulario alojado de Brevo.

Idempotente: si la pagina ya apunta a sibforms.com no la vuelve a tocar.
Recorre las 54 paginas (es + en/ + pt/), como el resto de los patch_*.py.
"""
import io, os, sys

ENDPOINT = ("https://18798c01.sibforms.com/serve/MUIFAFEDG9g8wYMo1u_0GAlk8-BNugevt_A3lx"
            "NeaYPPL_GvHxtOX0qZZ12tkqx3dibjByP5Euc6pbkwkb6vUdphQTaxQaTgEaOljMA3xLYWTfVU"
            "T6ItPTvBfbnCkD622yuViT2XOiOSmBB_78UAoj4PmF-iUnfRYMZloBs5-c1LTIwEun5CZOU0X8"
            "SchcOaOpquTTBHX90iQ16Y")

OLD_DOC = """  /* Configuracion de la newsletter.
     endpoint: URL que recibe el POST con {name,email,company,country,lang,page}.
               Mientras este vacio el alta NO se envia a ningun lado: queda en
               localStorage bajo 'rb-nl-pending' para no perderla.
     enabled:  poner en false para ocultar los dos formularios sin tocar el HTML. */
  var CFG = { endpoint: '', enabled: true };"""

NEW_DOC = """  /* Configuracion de la newsletter.
     endpoint: formulario alojado de Brevo, lista "Newsletter web" (#210). Espera un
               POST x-www-form-urlencoded con los campos NOMBRE / SURNAME / EMPRESA /
               PAIS / EMAIL, que son los declarados en ese formulario: lo que no este
               declarado alli, Brevo lo descarta al recibirlo.
               Si se deja vacio el alta NO se envia a ningun lado: queda en
               localStorage bajo 'rb-nl-pending' para no perderla.
     enabled:  poner en false para ocultar los dos formularios sin tocar el HTML. */
  var CFG = { endpoint: '%s', enabled: true };""" % ENDPOINT

OLD_SEND = """      fetch(CFG.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function(r){ r.ok ? done() : oops(); }).catch(oops);"""

NEW_SEND = """      /* Brevo exige los nombres de campo de su formulario alojado. Se manda como
         x-www-form-urlencoded (URLSearchParams) y sin cabeceras propias a proposito:
         asi es una "simple request" y no dispara el preflight CORS.
         email_address_check es el honeypot antispam de Brevo y viaja vacio.
         El sitio pide "Nombre y apellido" en un solo campo y valida que haya al
         menos un espacio, asi que se corta en el primero para separar SURNAME. */
      var sp = v.name.indexOf(' ');
      var body = new URLSearchParams();
      body.set('NOMBRE',  sp < 0 ? v.name : v.name.slice(0, sp));
      body.set('SURNAME', sp < 0 ? ''     : v.name.slice(sp + 1).trim());
      body.set('EMAIL',   v.email);
      body.set('EMPRESA', v.company);
      body.set('PAIS',    v.country);
      body.set('email_address_check', '');
      body.set('locale', 'es');

      fetch(CFG.endpoint, { method: 'POST', body: body })
        .then(function(r){ return r.ok ? r.json().catch(function(){ return { success: true }; }) : null; })
        .then(function(d){ (d && d.success) ? done() : oops(); })
        .catch(oops);"""

changed, skipped, missing = [], [], []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'assets', 'node_modules')]
    for fn in sorted(files):
        if not fn.endswith('.html') or fn.startswith('_'):
            continue
        path = os.path.join(root, fn)
        with io.open(path, encoding='utf-8') as fh:
            html = fh.read()
        if 'rb-nl-js' not in html:
            continue
        if 'sibforms.com' in html:
            skipped.append(path)
            continue
        if OLD_DOC not in html or OLD_SEND not in html:
            missing.append(path)
            continue
        html = html.replace(OLD_DOC, NEW_DOC).replace(OLD_SEND, NEW_SEND)
        with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(html)
        changed.append(path)

print('modificadas: %d' % len(changed))
print('ya estaban:  %d' % len(skipped))
print('sin match:   %d' % len(missing))
for p in missing:
    print('   !! %s' % p)
sys.exit(1 if missing else 0)
