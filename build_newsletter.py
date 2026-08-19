# -*- coding: utf-8 -*-
"""
Inserta el formulario de suscripcion a la newsletter en las dos ubicaciones
pedidas, en los tres idiomas:

  1. En el footer de las 54 paginas, debajo del bloque de redes sociales.
  2. Como seccion propia entre los testimonios de clientes y el CTA comercial
     (`<section class="rb-cta-band">`), solo en index y cfo.

Es idempotente: si la pagina ya tiene el bloque, no lo vuelve a insertar.
Para cambiar textos o campos, editar este archivo y volver a correrlo; nunca
editar el HTML generado a mano, porque son 54 copias.

    python build_newsletter.py            # simulacion
    python build_newsletter.py --apply    # escribe

EL DESTINO DE LOS DATOS AUN NO ESTA DEFINIDO. Mientras `endpoint` este vacio
en la config de abajo, el formulario valida y confirma, pero guarda el alta en
localStorage en lugar de enviarla. Ver README_NEWSLETTER.md.
"""
import re, os, sys

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# Textos
# ─────────────────────────────────────────────────────────────────────────────
T = {
 'es': {
   'foot_title': 'Newsletter',
   'foot_sub':   'Automatización, IA y casos reales. Una vez al mes.',
   'sec_eyebrow':'Newsletter',
   'sec_title':  'Novedades de automatización,',
   'sec_title2': 'una vez al mes',
   'sec_sub':    'Casos reales, buenas prácticas y lo que vamos aprendiendo con más de 700 empresas. Sin relleno y sin spam.',
   'name':       'Nombre y apellido',
   'email':      'Email',
   'company':    'Empresa',
   'country':    'País',
   'country_ph': 'Elige tu país',
   'submit':     'Suscribirme',
   'sending':    'Enviando…',
   'ok_title':   '¡Listo!',
   'ok_text':    'Vas a recibir la próxima edición en tu correo.',
   'err_name':   'Escribe tu nombre y apellido.',
   'err_email':  'Escribe un email válido.',
   'err_company':'Escribe el nombre de tu empresa.',
   'err_country':'Elige tu país.',
   'err_send':   'No pudimos completar la suscripción. Prueba de nuevo en un momento.',
   'privacy':    'Al suscribirte aceptas nuestras',
   'privacy_link':'políticas de privacidad',
   'privacy_href':'politicas-de-privacidad.html',
   'other':      'Otro país',
 },
 'en': {
   'foot_title': 'Newsletter',
   'foot_sub':   'Automation, AI and real cases. Once a month.',
   'sec_eyebrow':'Newsletter',
   'sec_title':  'Automation news,',
   'sec_title2': 'once a month',
   'sec_sub':    'Real cases, best practices and what we keep learning from more than 700 companies. No filler, no spam.',
   'name':       'Full name',
   'email':      'Email',
   'company':    'Company',
   'country':    'Country',
   'country_ph': 'Select your country',
   'submit':     'Subscribe',
   'sending':    'Sending…',
   'ok_title':   "You're in.",
   'ok_text':    'The next edition lands in your inbox.',
   'err_name':   'Enter your full name.',
   'err_email':  'Enter a valid email address.',
   'err_company':'Enter your company name.',
   'err_country':'Select your country.',
   'err_send':   "We couldn't complete your subscription. Please try again in a moment.",
   'privacy':    'By subscribing you accept our',
   'privacy_link':'privacy policy',
   'privacy_href':'/en/politicas-de-privacidad.html',
   'other':      'Other country',
 },
 'pt': {
   'foot_title': 'Newsletter',
   'foot_sub':   'Automação, IA e casos reais. Uma vez por mês.',
   'sec_eyebrow':'Newsletter',
   'sec_title':  'Novidades de automação,',
   'sec_title2': 'uma vez por mês',
   'sec_sub':    'Casos reais, boas práticas e o que aprendemos com mais de 700 empresas. Sem enrolação e sem spam.',
   'name':       'Nome e sobrenome',
   'email':      'E-mail',
   'company':    'Empresa',
   'country':    'País',
   'country_ph': 'Selecione o seu país',
   'submit':     'Quero receber',
   'sending':    'Enviando…',
   'ok_title':   'Pronto!',
   'ok_text':    'Você recebe a próxima edição no seu e-mail.',
   'err_name':   'Escreva o seu nome e sobrenome.',
   'err_email':  'Escreva um e-mail válido.',
   'err_company':'Escreva o nome da sua empresa.',
   'err_country':'Selecione o seu país.',
   'err_send':   'Não conseguimos concluir a inscrição. Tente de novo em instantes.',
   'privacy':    'Ao se inscrever você aceita as nossas',
   'privacy_link':'políticas de privacidade',
   'privacy_href':'/pt/politicas-de-privacidad.html',
   'other':      'Outro país',
 },
}

COUNTRIES = {
 'es': ['Argentina','Bolivia','Brasil','Chile','Colombia','Costa Rica','Ecuador','El Salvador',
        'España','Estados Unidos','Guatemala','Honduras','México','Nicaragua','Panamá','Paraguay',
        'Perú','Portugal','República Dominicana','Uruguay','Venezuela'],
 'en': ['Argentina','Bolivia','Brazil','Chile','Colombia','Costa Rica','Dominican Republic','Ecuador',
        'El Salvador','Guatemala','Honduras','Mexico','Nicaragua','Panama','Paraguay','Peru',
        'Portugal','Spain','United States','Uruguay','Venezuela'],
 'pt': ['Argentina','Bolívia','Brasil','Chile','Colômbia','Costa Rica','El Salvador','Equador',
        'Espanha','Estados Unidos','Guatemala','Honduras','México','Nicarágua','Panamá','Paraguai',
        'Peru','Portugal','República Dominicana','Uruguai','Venezuela'],
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
CSS = """<style id="rb-nl-css">
/* ===== Newsletter — footer ===== */
.rb-nlf{margin-top:28px;max-width:340px;}
.rb-nlf__t{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#fff;margin:0 0 6px;}
.rb-nlf__s{font-size:13px;color:#999;line-height:1.55;margin:0 0 14px;}
.rb-nlf__f{display:grid;gap:8px;}
.rb-nlf__row{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.rb-nl-in{
  width:100%;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.38);
  border-radius:10px;padding:10px 12px;font-family:inherit;font-size:13px;color:#fff;
  transition:border-color .2s,background .2s;
}
.rb-nl-in::placeholder{color:#7d8489;}
.rb-nl-in:focus{outline:none;border-color:var(--rb-red,#BC0017);background:rgba(255,255,255,.09);}
.rb-nl-in:focus-visible{outline:2px solid var(--rb-red,#BC0017);outline-offset:1px;}
.rb-nl-in[aria-invalid="true"]{border-color:#e2566a;}
select.rb-nl-in{appearance:none;cursor:pointer;
  background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237d8489' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 10px center;background-size:14px;padding-right:30px;}
select.rb-nl-in option{background:#12181c;color:#fff;}
.rb-nlf__btn{
  width:100%;background:var(--rb-red,#BC0017);color:#fff;border:none;border-radius:10px;
  padding:11px 16px;font-family:inherit;font-size:13px;font-weight:700;cursor:pointer;
  transition:background .2s,transform .15s;
}
.rb-nlf__btn:hover{background:var(--rb-red-deep,#8E0011);}
.rb-nlf__btn:active{transform:translateY(1px);}
.rb-nlf__btn[disabled]{opacity:.6;cursor:default;transform:none;}
.rb-nl-msg{font-size:12.5px;line-height:1.5;margin-top:4px;min-height:1px;}
.rb-nl-msg--err{color:#ff8a99;}
.rb-nl-msg--ok{color:#4ecf9f;}
.rb-nlf__legal{font-size:11.5px;color:#7d8489;line-height:1.5;margin:2px 0 0;}
.rb-nlf__legal a{color:#9aa3a8;text-decoration:underline;text-underline-offset:2px;}
.rb-nlf__legal a:hover{color:#fff;}

/* ===== Newsletter — seccion ===== */
.rb-nls{padding:96px 0;}
.rb-nls__box{
  background:var(--card,rgba(255,255,255,.7));border:1px solid var(--border,rgba(0,0,0,.08));
  border-radius:var(--r-xl,32px);padding:56px 48px;display:grid;grid-template-columns:1fr 1fr;
  gap:56px;align-items:center;
}
[data-theme="dark"] .rb-nls__box{background:rgba(20,20,30,.55);}
.rb-nls__eyebrow{
  display:inline-block;padding:5px 14px;border-radius:var(--r-pill,9999px);
  background:rgba(188,0,23,.08);border:1px solid rgba(188,0,23,.18);
  font-size:11px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;
  color:var(--rb-red,#BC0017);margin-bottom:20px;
}
.rb-nls__title{font-size:clamp(26px,3vw,38px);font-weight:800;letter-spacing:-.03em;line-height:1.12;margin:0 0 16px;color:var(--foreground);}
.rb-nls__title span{display:block;color:var(--rb-red,#BC0017);}
.rb-nls__sub{font-size:16px;line-height:1.6;color:#666;font-weight:300;margin:0;max-width:44ch;}
[data-theme="dark"] .rb-nls__sub{color:rgba(255,255,255,.55);}
.rb-nls__f{display:grid;gap:12px;}
.rb-nls__row{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.rb-nls .rb-nl-in.rb-nl-in{
  background:#fff;border:1px solid rgba(15,23,42,.52);
  color:#0B0E11;font-size:14px;padding:13px 15px;border-radius:12px;
}
.rb-nls .rb-nl-in.rb-nl-in::placeholder{color:#8b9198;}
.rb-nls .rb-nl-in.rb-nl-in:focus{border-color:var(--rb-red,#BC0017);background:#fff;}
[data-theme="dark"] .rb-nls .rb-nl-in.rb-nl-in{
  background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.38);color:#fff;
}
[data-theme="dark"] .rb-nls .rb-nl-in.rb-nl-in::placeholder{color:#7d8489;}
[data-theme="dark"] .rb-nls .rb-nl-in.rb-nl-in:focus{background:rgba(255,255,255,.09);}
.rb-nls select.rb-nl-in{background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239aa0a6' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;background-size:16px;padding-right:34px;}
.rb-nls select.rb-nl-in option{background:#fff;color:#0B0E11;}
[data-theme="dark"] .rb-nls select.rb-nl-in option{background:#12181c;color:#fff;}
[data-theme="dark"] .rb-nls select.rb-nl-in.rb-nl-in{background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237d8489' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;background-size:16px;}
.rb-nls__btn{
  background:var(--rb-red,#BC0017);color:#fff;border:none;border-radius:12px;padding:14px 20px;
  font-family:inherit;font-size:15px;font-weight:700;cursor:pointer;transition:background .2s,transform .15s;
}
.rb-nls__btn:hover{background:var(--rb-red-deep,#8E0011);}
.rb-nls__btn:active{transform:translateY(1px);}
.rb-nls__btn[disabled]{opacity:.6;cursor:default;transform:none;}
.rb-nls .rb-nl-msg--err{color:#c02a3c;}
.rb-nls .rb-nl-msg--ok{color:var(--rb-green-deep,#0F5C42);}
[data-theme="dark"] .rb-nls .rb-nl-msg--err{color:#ff8a99;}
[data-theme="dark"] .rb-nls .rb-nl-msg--ok{color:#4ecf9f;}
.rb-nls__legal{font-size:12px;color:#8a9095;line-height:1.5;margin:2px 0 0;}
.rb-nls__legal a{color:inherit;text-decoration:underline;text-underline-offset:2px;}
@media(max-width:900px){
  .rb-nls{padding:64px 0;}
  .rb-nls__box{grid-template-columns:1fr;gap:32px;padding:40px 28px;}
}
@media(max-width:560px){
  .rb-nlf__row,.rb-nls__row{grid-template-columns:1fr;}
}
@media(prefers-reduced-motion:reduce){
  .rb-nlf__btn,.rb-nls__btn{transition:none;}
}
</style>"""

# ─────────────────────────────────────────────────────────────────────────────
# JS
# ─────────────────────────────────────────────────────────────────────────────
JS = """<script id="rb-nl-js">
(function(){
  /* Configuracion de la newsletter.
     endpoint: URL que recibe el POST con {name,email,company,country,lang,page}.
               Mientras este vacio el alta NO se envia a ningun lado: queda en
               localStorage bajo 'rb-nl-pending' para no perderla.
     enabled:  poner en false para ocultar los dos formularios sin tocar el HTML. */
  var CFG = { endpoint: '', enabled: true };
  window.RB_NEWSLETTER = CFG;

  var forms = document.querySelectorAll('form[data-rb-nl]');
  if (!forms.length) return;
  if (!CFG.enabled) {
    forms.forEach(function(f){
      var host = f.closest('.rb-nls') || f.closest('.rb-nlf');
      if (host) host.style.display = 'none';
    });
    return;
  }

  var EMAIL = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/;

  forms.forEach(function(form){
    var msg  = form.querySelector('[data-rb-nl-msg]');
    var btn  = form.querySelector('button[type="submit"]');
    var lbl  = btn ? btn.textContent : '';

    function say(text, kind){
      if (!msg) return;
      msg.textContent = text;
      msg.className = 'rb-nl-msg' + (kind ? ' rb-nl-msg--' + kind : '');
    }
    function fail(field, text){
      say(text, 'err');
      if (field){ field.setAttribute('aria-invalid','true'); field.focus(); }
      return false;
    }

    form.addEventListener('input', function(e){
      if (e.target.hasAttribute('aria-invalid')) e.target.removeAttribute('aria-invalid');
    });

    form.addEventListener('submit', function(e){
      e.preventDefault();
      var f = {
        name:    form.elements.name,
        email:   form.elements.email,
        company: form.elements.company,
        country: form.elements.country
      };
      var v = {};
      for (var k in f) v[k] = (f[k] && f[k].value || '').trim();

      if (v.name.length < 3 || v.name.indexOf(' ') < 0) return fail(f.name, form.dataset.errName);
      if (!EMAIL.test(v.email))                          return fail(f.email, form.dataset.errEmail);
      if (v.company.length < 2)                          return fail(f.company, form.dataset.errCompany);
      if (!v.country)                                    return fail(f.country, form.dataset.errCountry);

      var payload = {
        name: v.name, email: v.email, company: v.company, country: v.country,
        lang: document.documentElement.lang || '',
        page: location.pathname,
        sentAt: new Date().toISOString()
      };

      if (btn){ btn.disabled = true; btn.textContent = form.dataset.sending || lbl; }
      say('', '');

      function done(){
        form.reset();
        if (btn){ btn.disabled = false; btn.textContent = lbl; }
        say(form.dataset.okTitle + ' ' + form.dataset.okText, 'ok');
      }
      function oops(){
        if (btn){ btn.disabled = false; btn.textContent = lbl; }
        say(form.dataset.errSend, 'err');
      }

      if (!CFG.endpoint){
        /* Sin destino configurado: se guarda localmente para no perder el alta. */
        try {
          var q = JSON.parse(localStorage.getItem('rb-nl-pending') || '[]');
          q.push(payload);
          localStorage.setItem('rb-nl-pending', JSON.stringify(q));
        } catch(err){}
        console.warn('[newsletter] Sin endpoint configurado. Alta guardada en localStorage:', payload);
        done();
        return;
      }

      fetch(CFG.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function(r){ r.ok ? done() : oops(); }).catch(oops);
    });
  });
})();
</script>"""

# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────
def opts(lang):
    t = T[lang]
    out = ['<option value="" disabled selected>%s</option>' % t['country_ph']]
    for c in COUNTRIES[lang]:
        out.append('<option value="%s">%s</option>' % (c, c))
    out.append('<option value="%s">%s</option>' % (t['other'], t['other']))
    return ''.join(out)

def data_attrs(lang):
    t = T[lang]
    return (' data-rb-nl data-sending="%s" data-ok-title="%s" data-ok-text="%s"'
            ' data-err-name="%s" data-err-email="%s" data-err-company="%s"'
            ' data-err-country="%s" data-err-send="%s"') % (
        t['sending'], t['ok_title'], t['ok_text'], t['err_name'],
        t['err_email'], t['err_company'], t['err_country'], t['err_send'])

def footer_block(lang):
    t = T[lang]
    return """
        <!-- rb-nl-footer -->
        <div class="rb-nlf">
          <p class="rb-nlf__t">%(foot_title)s</p>
          <p class="rb-nlf__s">%(foot_sub)s</p>
          <form class="rb-nlf__f" novalidate%(attrs)s>
            <input class="rb-nl-in" type="text" name="name" autocomplete="name" placeholder="%(name)s" aria-label="%(name)s">
            <input class="rb-nl-in" type="email" name="email" autocomplete="email" placeholder="%(email)s" aria-label="%(email)s">
            <div class="rb-nlf__row">
              <input class="rb-nl-in" type="text" name="company" autocomplete="organization" placeholder="%(company)s" aria-label="%(company)s">
              <select class="rb-nl-in" name="country" autocomplete="country-name" aria-label="%(country)s">%(opts)s</select>
            </div>
            <button class="rb-nlf__btn" type="submit">%(submit)s</button>
            <p class="rb-nl-msg" data-rb-nl-msg role="status" aria-live="polite"></p>
            <p class="rb-nlf__legal">%(privacy)s <a href="%(privacy_href)s">%(privacy_link)s</a>.</p>
          </form>
        </div>""" % dict(t, attrs=data_attrs(lang), opts=opts(lang))

def section_block(lang):
    t = T[lang]
    return """
<!-- rb-nl-section -->
<!-- ════════════════ NEWSLETTER ════════════════ -->
<section class="rb-nls">
  <div class="container">
    <div class="rb-nls__box rb-reveal">
      <div>
        <span class="rb-nls__eyebrow">%(sec_eyebrow)s</span>
        <h2 class="rb-nls__title">%(sec_title)s<span>%(sec_title2)s</span></h2>
        <p class="rb-nls__sub">%(sec_sub)s</p>
      </div>
      <form class="rb-nls__f" novalidate%(attrs)s>
        <div class="rb-nls__row">
          <input class="rb-nl-in" type="text" name="name" autocomplete="name" placeholder="%(name)s" aria-label="%(name)s">
          <input class="rb-nl-in" type="email" name="email" autocomplete="email" placeholder="%(email)s" aria-label="%(email)s">
        </div>
        <div class="rb-nls__row">
          <input class="rb-nl-in" type="text" name="company" autocomplete="organization" placeholder="%(company)s" aria-label="%(company)s">
          <select class="rb-nl-in" name="country" autocomplete="country-name" aria-label="%(country)s">%(opts)s</select>
        </div>
        <button class="rb-nls__btn" type="submit">%(submit)s</button>
        <p class="rb-nl-msg" data-rb-nl-msg role="status" aria-live="polite"></p>
        <p class="rb-nls__legal">%(privacy)s <a href="%(privacy_href)s">%(privacy_link)s</a>.</p>
      </form>
    </div>
  </div>
</section>
""" % dict(t, attrs=data_attrs(lang), opts=opts(lang))

# ─────────────────────────────────────────────────────────────────────────────
# Insercion
# ─────────────────────────────────────────────────────────────────────────────
def close_div(html, start):
    """Devuelve el indice justo despues del </div> que cierra el div abierto en `start`."""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    return -1

def patch(path, lang, with_section):
    raw = open(path, encoding='utf-8').read()
    changed = []

    m = re.search(r'(?s)<style id="rb-nl-css">.*?</style>', raw)
    if m:
        if m.group(0) != CSS:
            raw = raw[:m.start()] + CSS + raw[m.end():]
            changed.append('css (actualizado)')
    else:
        i = raw.find('</head>')
        if i < 0: return ['sin </head>']
        raw = raw[:i] + CSS + '\n' + raw[i:]
        changed.append('css')

    if '<!-- rb-nl-footer -->' not in raw:
        i = raw.find('<div class="rb-footer__social">')
        if i < 0: return changed + ['sin rb-footer__social']
        j = close_div(raw, i)
        if j < 0: return changed + ['div de redes sin cerrar']
        raw = raw[:j] + footer_block(lang) + raw[j:]
        changed.append('footer')

    if with_section and '<!-- rb-nl-section -->' not in raw:
        i = raw.find('<section class="rb-cta-band">')
        if i < 0: return changed + ['sin rb-cta-band']
        raw = raw[:i] + section_block(lang) + raw[i:]
        changed.append('seccion')

    if 'rb-nl-js' not in raw:
        i = raw.rfind('</body>')
        if i < 0: return changed + ['sin </body>']
        raw = raw[:i] + JS + '\n' + raw[i:]
        changed.append('js')

    if changed and APPLY:
        open(path, 'w', encoding='utf-8', newline='').write(raw)
    return changed


def main():
    WITH_SECTION = {'index.html', 'cfo.html'}
    total = 0
    for lang, folder in (('es', '.'), ('en', 'en'), ('pt', 'pt')):
        d = os.path.join(ROOT, folder)
        for f in sorted(x for x in os.listdir(d) if x.endswith('.html') and not x.startswith('_')):
            p = os.path.join(d, f)
            ch = patch(p, lang, f in WITH_SECTION)
            if ch:
                total += 1
                rel = f if folder == '.' else folder + '/' + f
                print('  %-36s %s' % (rel, ', '.join(ch)))
    print('\n%d paginas %s' % (total, 'modificadas' if APPLY else 'a modificar (SIMULACION)'))


if __name__ == '__main__':
    main()
