# -*- coding: utf-8 -*-
"""
Genera la landing "Quiero ser partner" en los 3 idiomas a partir del shell de
contacto.html (head + nav + footer + scripts). Reemplaza el bloque central
(entre <!-- CONTACT PAGE --> y <!-- FOOTER -->) por el contenido de partners,
inyecta el CSS propio, ajusta <title>/meta/canonical, robots=index y PAGE.

Contenido basado en https://rocketbot.com/es/partners-rpa-2/ y modernizado:
  · sin proyecciones de mercado con año fijo (estaban a 2025)
  · productos referidos como "RPA e IA" (los nombres viejos ya no aplican)
  · niveles y certificaciones descritas de forma general (via Rocketbot Academy)

Es idempotente: reescribe partners.html cada vez desde contacto.html actual.
Ejecutar DESPUES de que la nav este al dia y ANTES/DESPUES de patch_partners_nav.py
(el patch de nav tambien recorre partners.html).

    python build_partners.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- CSS propio de la landing (se inyecta antes de </head>) ----
PRT_CSS = """
<style id="rb-prt-css">
.rb-prt{padding-top:72px;}
.rb-prt-eyebrow{display:inline-block;font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;color:var(--rb-red);background:rgba(188,0,23,.10);border:1px solid rgba(188,0,23,.22);padding:7px 16px;border-radius:9999px;margin-bottom:24px;}
.rb-prt-accent{color:var(--rb-red);}
.rb-prt-hero{padding:80px 0 52px;text-align:center;position:relative;}
.rb-prt-hero__inner,.rb-prt-market,.rb-prt-cta__inner{margin-left:auto;margin-right:auto;}
.rb-prt-hero__inner{max-width:860px;}
.rb-prt-hero__title{font-size:clamp(34px,5vw,60px);font-weight:900;letter-spacing:-.03em;margin-bottom:20px;}
.rb-prt-hero__sub{font-size:clamp(16px,1.5vw,20px);line-height:1.6;color:var(--foreground);opacity:.75;max-width:700px;margin:0 auto 34px;}
.rb-prt-hero__cta{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
.rb-prt-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:15px 30px;border-radius:9999px;font-weight:800;font-size:15px;transition:transform .2s,box-shadow .2s,background .2s,color .2s,border-color .2s;white-space:nowrap;}
.rb-prt-btn--primary{background:linear-gradient(110deg,#FF2942,#BC0017);color:#fff;box-shadow:0 10px 30px rgba(188,0,23,.4);}
.rb-prt-btn--primary:hover{transform:translateY(-2px);box-shadow:0 16px 40px rgba(188,0,23,.55);color:#fff;}
.rb-prt-btn--ghost{background:transparent;color:var(--foreground);border:1.5px solid var(--border);}
.rb-prt-btn--ghost:hover{border-color:var(--rb-red);color:var(--rb-red);transform:translateY(-2px);}
.rb-prt-stats{padding:4px 0 56px;}
.rb-prt-stats__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;}
.rb-prt-stat{text-align:center;padding:26px 14px;border:1px solid var(--border);border-radius:20px;background:var(--card);backdrop-filter:blur(6px);}
.rb-prt-stat__v{font-size:clamp(30px,3.4vw,44px);font-weight:900;color:var(--rb-red);letter-spacing:-.02em;line-height:1;}
.rb-prt-stat__l{margin-top:10px;font-size:13px;font-weight:600;opacity:.7;}
.rb-prt-sec{padding:64px 0;}
.rb-prt-sec--alt{background:rgba(188,0,23,.05);}
[data-theme="dark"] .rb-prt-sec--alt{background:rgba(188,0,23,.08);}
.rb-prt-h2{font-size:clamp(26px,3.4vw,42px);font-weight:900;letter-spacing:-.03em;text-align:center;margin-bottom:16px;}
.rb-prt-lead{text-align:center;max-width:700px;margin:0 auto 40px;font-size:17px;line-height:1.6;opacity:.75;}
.rb-prt-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
.rb-prt-card{padding:32px 26px;border:1px solid var(--border);border-radius:22px;background:var(--card);transition:transform .2s,border-color .2s,box-shadow .2s;}
.rb-prt-card:hover{transform:translateY(-4px);border-color:rgba(188,0,23,.35);box-shadow:0 18px 44px rgba(0,0,0,.12);}
.rb-prt-card__icon{font-size:30px;margin-bottom:16px;line-height:1;}
.rb-prt-card__title{font-size:19px;font-weight:800;margin-bottom:10px;}
.rb-prt-card__text{font-size:15px;line-height:1.6;opacity:.75;}
.rb-prt-tiers{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;}
.rb-prt-tier{padding:28px 22px;border:1px solid var(--border);border-radius:20px;background:var(--card);display:flex;flex-direction:column;gap:14px;}
.rb-prt-tier__badge{align-self:flex-start;font-weight:800;font-size:14px;padding:8px 16px;border-radius:9999px;color:#0A0A0F;}
.rb-prt-tier__badge--champ{background:linear-gradient(110deg,#FF2942,#BC0017);color:#fff;}
.rb-prt-tier__badge--silver{background:linear-gradient(120deg,#C7CDD4,#9AA3AD);}
.rb-prt-tier__badge--gold{background:linear-gradient(120deg,#F5D061,#D4A017);}
.rb-prt-tier__badge--platinum{background:linear-gradient(120deg,#E5E8EC,#B9C0C8);}
.rb-prt-tier__text{font-size:14px;line-height:1.6;opacity:.78;}
.rb-prt-note{text-align:center;margin-top:26px;font-size:14px;opacity:.7;}
.rb-prt-note a{color:var(--rb-red);font-weight:700;}
.rb-prt-market{max-width:760px;}
.rb-prt-list{margin:20px 0 0;display:flex;flex-direction:column;gap:12px;}
.rb-prt-list li{position:relative;padding-left:30px;font-size:16px;line-height:1.55;opacity:.82;}
.rb-prt-list li::before{content:'';position:absolute;left:0;top:6px;width:18px;height:18px;border-radius:50%;background:var(--rb-red);}
.rb-prt-list li::after{content:'\\2713';position:absolute;left:4px;top:4px;font-size:11px;font-weight:900;color:#fff;}
.rb-prt-cta{padding:72px 0;text-align:center;}
.rb-prt-cta__inner{max-width:660px;}
.rb-prt-cta__title{font-size:clamp(26px,3.4vw,40px);font-weight:900;letter-spacing:-.03em;margin-bottom:14px;}
.rb-prt-cta__sub{font-size:17px;line-height:1.6;opacity:.75;margin-bottom:30px;}
@media(max-width:900px){.rb-prt-stats__grid{grid-template-columns:repeat(2,1fr);}.rb-prt-cards{grid-template-columns:1fr;}.rb-prt-tiers{grid-template-columns:repeat(2,1fr);}}
@media(max-width:560px){.rb-prt-tiers{grid-template-columns:1fr;}.rb-prt-hero{padding:56px 0 40px;}}
</style>
"""

# ---- textos por idioma ----
T = {
 'es': {
  'title': 'Programa de Partners RPA e IA | Sé Partner de Rocketbot',
  'desc': 'Unete al programa de partners de Rocketbot: apoyo comercial, soporte tecnico, capacitacion y niveles Silver, Gold y Platinum. Haz crecer tu negocio con RPA e IA.',
  'eyebrow': 'Programa de Partners',
  'h1a': 'Conviertete en ', 'h1b': 'partner de Rocketbot',
  'sub': 'Suma la automatizacion con RPA e IA a tu portafolio, haz crecer tu negocio y acompana a tus clientes en su transformacion digital junto a una de las plataformas lideres de Latinoamerica.',
  'cta1': 'Quiero ser partner', 'login': 'Login de Partners →',
  'stats': [('+700','Empresas usan Rocketbot'),('21','Paises'),('+5.000','Procesos automatizados'),('+10','Anos en el mercado')],
  'bh2a': 'Que significa ser ', 'bh2b': 'partner de Rocketbot', 'bh2c': '?',
  'blead': 'Formar parte de nuestro ecosistema es contar con respaldo real para vender, implementar y escalar proyectos de automatizacion.',
  'cards': [('\U0001F91D','Apoyo comercial','Te acompanamos frente al cliente, colaboramos en oportunidades del ecosistema y, segun tu nivel, recibes entrega de leads calificados.'),
            ('\U0001F6E0️','Soporte tecnico','Asistencia en tiempo real de nuestro equipo, ayuda en la construccion de conectores y acompanamiento en implementaciones complejas.'),
            ('\U0001F393','Capacitacion y certificacion','Acceso a formacion y certificaciones de Rocketbot Academy para que tu equipo domine la plataforma sin costo adicional.')],
  'th2a': 'Niveles de ', 'th2b': 'partnership',
  'tlead': 'A medida que tu equipo se certifica y crece, avanzas de nivel y accedes a mas beneficios.',
  'tiers': [('champ','Sales Champion','Reconocimiento al partner con el mayor desempeno de ventas del semestre: insignia destacada, casos de exito publicados y espacios para exponer.'),
            ('silver','Silver','Equipo con ingenieros certificados, capaz de implementar robots de complejidad media. Insignia en el portal y participacion en eventos.'),
            ('gold','Gold','Certificaciones avanzadas para proyectos de mayor complejidad y multiples integraciones. Incluye entrega de leads calificados.'),
            ('platinum','Platinum','Maximo nivel, con capacidad de consultoria certificada. Eventos cerrados y reuniones directas con clientes junto a Rocketbot.')],
  'tnotea': 'Los requisitos de certificacion se obtienen a traves de ', 'tnoteb': 'Rocketbot Academy', 'tnotec': '.',
  'mh2a': 'Un mercado que ', 'mh2b': 'no deja de crecer',
  'mlead': 'La automatizacion con RPA e IA es una de las industrias tecnologicas de mayor expansion a nivel global. Sumarte como partner te posiciona en un mercado con demanda creciente y te permite ofrecer soluciones de alto impacto a tus clientes.',
  'mlist': ['Nuevas fuentes de ingresos con licencias y servicios de implementacion.','Portafolio diferenciado con RPA, agentes de IA y orquestacion.','Relaciones de largo plazo con tus clientes.'],
  'ctitle': 'Listo para crecer con Rocketbot?',
  'csub': 'Cuentanos sobre tu empresa y un asesor te contactara para iniciar tu camino como partner.',
  'clogin': 'Ya soy partner · Login →',
 },
 'en': {
  'title': 'RPA & AI Partner Program | Become a Rocketbot Partner',
  'desc': 'Join the Rocketbot partner program: sales support, technical support, training and Silver, Gold and Platinum tiers. Grow your business with RPA and AI.',
  'eyebrow': 'Partner Program',
  'h1a': 'Become a ', 'h1b': 'Rocketbot partner',
  'sub': 'Add RPA and AI automation to your portfolio, grow your business and guide your clients through their digital transformation alongside one of Latin America’s leading platforms.',
  'cta1': 'I want to be a partner', 'login': 'Partner Login →',
  'stats': [('+700','Companies use Rocketbot'),('21','Countries'),('+5,000','Automated processes'),('+10','Years in the market')],
  'bh2a': 'What does it mean to be a ', 'bh2b': 'Rocketbot partner', 'bh2c': '?',
  'blead': 'Being part of our ecosystem means having real support to sell, implement and scale automation projects.',
  'cards': [('\U0001F91D','Sales support','We stand beside you in front of the client, collaborate on ecosystem opportunities and, depending on your tier, deliver qualified leads.'),
            ('\U0001F6E0️','Technical support','Real-time assistance from our team, help building connectors and support on complex implementations.'),
            ('\U0001F393','Training & certification','Access to Rocketbot Academy training and certifications so your team masters the platform at no extra cost.')],
  'th2a': 'Partnership ', 'th2b': 'tiers',
  'tlead': 'As your team gets certified and grows, you move up tiers and unlock more benefits.',
  'tiers': [('champ','Sales Champion','Recognition for the partner with the best sales performance of the semester: featured badge, published success stories and speaking opportunities.'),
            ('silver','Silver','A team with certified engineers, able to implement medium-complexity robots. Portal badge and participation in events.'),
            ('gold','Gold','Advanced certifications for higher-complexity projects and multiple integrations. Includes qualified lead delivery.'),
            ('platinum','Platinum','Top tier, with certified consulting capability. Closed events and direct client meetings alongside Rocketbot.')],
  'tnotea': 'Certification requirements are earned through ', 'tnoteb': 'Rocketbot Academy', 'tnotec': '.',
  'mh2a': 'A market that ', 'mh2b': 'keeps growing',
  'mlead': 'RPA and AI automation is one of the fastest-growing technology industries worldwide. Joining as a partner positions you in a market with rising demand and lets you offer high-impact solutions to your clients.',
  'mlist': ['New revenue streams from licenses and implementation services.','A differentiated portfolio with RPA, AI agents and orchestration.','Long-term relationships with your clients.'],
  'ctitle': 'Ready to grow with Rocketbot?',
  'csub': 'Tell us about your company and an advisor will reach out to start your journey as a partner.',
  'clogin': 'Already a partner · Login →',
 },
 'pt': {
  'title': 'Programa de Parceiros RPA e IA | Seja Parceiro Rocketbot',
  'desc': 'Entre no programa de parceiros da Rocketbot: apoio comercial, suporte tecnico, capacitacao e niveis Silver, Gold e Platinum. Cresca com RPA e IA.',
  'eyebrow': 'Programa de Parceiros',
  'h1a': 'Torne-se um ', 'h1b': 'parceiro Rocketbot',
  'sub': 'Adicione a automacao com RPA e IA ao seu portfolio, faca seu negocio crescer e acompanhe seus clientes na transformacao digital ao lado de uma das plataformas lideres da America Latina.',
  'cta1': 'Quero ser parceiro', 'login': 'Login de Parceiros →',
  'stats': [('+700','Empresas usam a Rocketbot'),('21','Paises'),('+5.000','Processos automatizados'),('+10','Anos no mercado')],
  'bh2a': 'O que significa ser ', 'bh2b': 'parceiro Rocketbot', 'bh2c': '?',
  'blead': 'Fazer parte do nosso ecossistema e contar com apoio real para vender, implementar e escalar projetos de automacao.',
  'cards': [('\U0001F91D','Apoio comercial','Acompanhamos voce diante do cliente, colaboramos em oportunidades do ecossistema e, conforme o seu nivel, voce recebe leads qualificados.'),
            ('\U0001F6E0️','Suporte tecnico','Assistencia em tempo real da nossa equipe, ajuda na construcao de conectores e acompanhamento em implementacoes complexas.'),
            ('\U0001F393','Capacitacao e certificacao','Acesso a treinamentos e certificacoes da Rocketbot Academy para a sua equipe dominar a plataforma sem custo adicional.')],
  'th2a': 'Niveis de ', 'th2b': 'parceria',
  'tlead': 'A medida que a sua equipe se certifica e cresce, voce avanca de nivel e acessa mais beneficios.',
  'tiers': [('champ','Sales Champion','Reconhecimento ao parceiro com o melhor desempenho de vendas do semestre: selo em destaque, casos de sucesso publicados e espacos para apresentar.'),
            ('silver','Silver','Equipe com engenheiros certificados, capaz de implementar robos de complexidade media. Selo no portal e participacao em eventos.'),
            ('gold','Gold','Certificacoes avancadas para projetos de maior complexidade e multiplas integracoes. Inclui entrega de leads qualificados.'),
            ('platinum','Platinum','Nivel maximo, com capacidade de consultoria certificada. Eventos fechados e reunioes diretas com clientes ao lado da Rocketbot.')],
  'tnotea': 'Os requisitos de certificacao sao obtidos atraves da ', 'tnoteb': 'Rocketbot Academy', 'tnotec': '.',
  'mh2a': 'Um mercado que ', 'mh2b': 'nao para de crescer',
  'mlead': 'A automacao com RPA e IA e uma das industrias de tecnologia que mais cresce no mundo. Entrar como parceiro posiciona voce em um mercado com demanda crescente e permite oferecer solucoes de alto impacto aos seus clientes.',
  'mlist': ['Novas fontes de receita com licencas e servicos de implementacao.','Portfolio diferenciado com RPA, agentes de IA e orquestracao.','Relacionamentos de longo prazo com os seus clientes.'],
  'ctitle': 'Pronto para crescer com a Rocketbot?',
  'csub': 'Conte sobre a sua empresa e um consultor entrara em contato para iniciar a sua jornada como parceiro.',
  'clogin': 'Ja sou parceiro · Login →',
 },
}

LOGIN_URL = 'https://partners.rocketbot.com/wp-login.php'


def build_main(t):
    stats = '\n'.join(
        '        <div class="rb-prt-stat"><div class="rb-prt-stat__v">%s</div><div class="rb-prt-stat__l">%s</div></div>' % (v, l)
        for v, l in t['stats'])
    cards = '\n'.join(
        '        <article class="rb-prt-card"><div class="rb-prt-card__icon">%s</div><h3 class="rb-prt-card__title">%s</h3><p class="rb-prt-card__text">%s</p></article>' % c
        for c in t['cards'])
    tiers = '\n'.join(
        '        <article class="rb-prt-tier"><div class="rb-prt-tier__badge rb-prt-tier__badge--%s">%s</div><p class="rb-prt-tier__text">%s</p></article>' % tr
        for tr in t['tiers'])
    mlist = '\n'.join('        <li>%s</li>' % x for x in t['mlist'])
    f = dict(t)
    f.update(stats=stats, cards=cards, tiers=tiers, mlist=mlist, login_url=LOGIN_URL)
    return """<!-- CONTACT PAGE -->
<!-- ======================= PARTNERS LANDING ======================= -->
<main class="rb-prt">

  <section class="rb-prt-hero">
    <div class="container rb-prt-hero__inner">
      <span class="rb-prt-eyebrow">{eyebrow}</span>
      <h1 class="rb-prt-hero__title">{h1a}<span class="rb-prt-accent">{h1b}</span></h1>
      <p class="rb-prt-hero__sub">{sub}</p>
      <div class="rb-prt-hero__cta">
        <a href="contacto.html" class="rb-prt-btn rb-prt-btn--primary">{cta1}</a>
        <a href="{login_url}" target="_blank" rel="noopener" class="rb-prt-btn rb-prt-btn--ghost">{login}</a>
      </div>
    </div>
  </section>

  <section class="rb-prt-stats">
    <div class="container rb-prt-stats__grid">
{stats}
    </div>
  </section>

  <section class="rb-prt-sec">
    <div class="container">
      <h2 class="rb-prt-h2">{bh2a}<span class="rb-prt-accent">{bh2b}</span>{bh2c}</h2>
      <p class="rb-prt-lead">{blead}</p>
      <div class="rb-prt-cards">
{cards}
      </div>
    </div>
  </section>

  <section class="rb-prt-sec rb-prt-sec--alt">
    <div class="container">
      <h2 class="rb-prt-h2">{th2a}<span class="rb-prt-accent">{th2b}</span></h2>
      <p class="rb-prt-lead">{tlead}</p>
      <div class="rb-prt-tiers">
{tiers}
      </div>
      <p class="rb-prt-note">{tnotea}<a href="https://academy.rocketbot.com" target="_blank" rel="noopener">{tnoteb}</a>{tnotec}</p>
    </div>
  </section>

  <section class="rb-prt-sec">
    <div class="container rb-prt-market">
      <h2 class="rb-prt-h2">{mh2a}<span class="rb-prt-accent">{mh2b}</span></h2>
      <p class="rb-prt-lead">{mlead}</p>
      <ul class="rb-prt-list">
{mlist}
      </ul>
    </div>
  </section>

  <section class="rb-prt-cta">
    <div class="container rb-prt-cta__inner">
      <h2 class="rb-prt-cta__title">{ctitle}</h2>
      <p class="rb-prt-cta__sub">{csub}</p>
      <div class="rb-prt-hero__cta">
        <a href="contacto.html" class="rb-prt-btn rb-prt-btn--primary">{cta1}</a>
        <a href="{login_url}" target="_blank" rel="noopener" class="rb-prt-btn rb-prt-btn--ghost">{clogin}</a>
      </div>
    </div>
  </section>

</main>

<!-- FOOTER -->""".format(**f)


SECTION_RE = re.compile(r'<!-- CONTACT PAGE -->.*?<!-- FOOTER -->', re.S)
TITLE_RE = re.compile(r'<title>.*?</title>', re.S)


def sub_attr(src, prop, value):
    # reemplaza content="..." del meta indicado, sea name= u property=
    pat = re.compile(r'(<meta (?:name|property)="' + re.escape(prop) + r'" content=")[^"]*(">)')
    return pat.sub(lambda m: m.group(1) + value + m.group(2), src)


def build(lang, folder):
    src = io.open(os.path.join(folder, 'contacto.html'), encoding='utf-8').read()
    t = T[lang]

    # 1) bloque central
    src = SECTION_RE.sub(lambda m: build_main(t), src, count=1)

    # 2) titulo + metas
    src = TITLE_RE.sub('<title>' + t['title'] + '</title>', src, count=1)
    src = sub_attr(src, 'description', t['desc'])
    src = sub_attr(src, 'og:title', t['title'])
    src = sub_attr(src, 'og:description', t['desc'])
    src = sub_attr(src, 'twitter:title', t['title'])
    src = sub_attr(src, 'twitter:description', t['desc'])

    # 3) indexable (contacto era noindex)
    src = src.replace('content="noindex, follow"', 'content="index, follow"')

    # 4) canonical / og:url / hreflang -> partners
    src = src.replace('rocketbot.com/contacto"', 'rocketbot.com/partners"')
    src = src.replace('rocketbot.com/en/contacto"', 'rocketbot.com/en/partners"')
    src = src.replace('rocketbot.com/pt/contacto"', 'rocketbot.com/pt/partners"')

    # 5) ld+json: ya no es ContactPage
    src = src.replace('"@type": "ContactPage"', '"@type": "WebPage"')

    # 6) selector de idioma
    src = src.replace("PAGE='contacto.html'", "PAGE='partners.html'")

    # 7) CSS propio antes de </head>
    if 'rb-prt-css' not in src:
        src = src.replace('</head>', PRT_CSS + '</head>', 1)

    out = os.path.join(folder, 'partners.html')
    io.open(out, 'w', encoding='utf-8', newline='\n').write(src)
    print('  escrito %s/partners.html' % lang)


def main():
    for lang, folder in (('es', ROOT), ('en', os.path.join(ROOT, 'en')), ('pt', os.path.join(ROOT, 'pt'))):
        build(lang, folder)
    print('listo.')


if __name__ == '__main__':
    main()
