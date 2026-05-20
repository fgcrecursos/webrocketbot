import re, os
os.chdir(r'C:\Users\frani\.claude\worktrees\rocketbot')

# ─── CONFIG ────────────────────────────────────────────────────────────────────
BASE_URL  = 'https://rocketbot.com'
OG_IMAGE  = f'{BASE_URL}/assets/logos/og-image.jpg'  # 1200×630px – generar este archivo
GA4_ID    = 'G-XXXXXXXXXX'   # ← reemplazar con el Measurement ID real de GA4
GSC_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # ← Google Search Console

# ─── PER-PAGE DATA ─────────────────────────────────────────────────────────────
PAGES = {
    'index.html': {
        'title': 'Rocketbot | Suite de Automatización Empresarial RPA e IA para Latinoamérica',
        'desc':  'Suite completa de automatización empresarial end-to-end. Agentes digitales con RPA e IA disponibles 24/7. Saturn Studio, RPA Studio, AI Studio, Orquestador y Xperience.',
        'url':   BASE_URL + '/',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'Organization',
                'name': 'Rocketbot',
                'url': BASE_URL,
                'logo': f'{BASE_URL}/assets/logos/logo-header.png',
                'description': 'Suite completa de automatización empresarial end-to-end para Latinoamérica.',
                'foundingDate': '2018',
                'areaServed': 'Latin America',
                'sameAs': [
                    'https://www.linkedin.com/company/rocketbot',
                    'https://twitter.com/rocketbot',
                    'https://www.facebook.com/rocketbot',
                    'https://www.instagram.com/rocketbot',
                ]
            },
            {
                '@context': 'https://schema.org',
                '@type': 'WebSite',
                'name': 'Rocketbot',
                'url': BASE_URL,
            }
        ],
    },
    'saturn-studio.html': {
        'title': 'Saturn Studio | Plataforma de Automatización Inteligente sin Código · Rocketbot',
        'desc':  'Crea agentes digitales sin código con Saturn Studio. Conecta más de 38 integraciones nativas y automatiza procesos empresariales con IA. Suite Rocketbot.',
        'url':   BASE_URL + '/saturn-studio',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'SoftwareApplication',
                'name': 'Saturn Studio',
                'applicationCategory': 'BusinessApplication',
                'operatingSystem': 'Windows, Web',
                'description': 'Plataforma de automatización inteligente con IA, sin código. Más de 38 integraciones nativas.',
                'url': BASE_URL + '/saturn-studio',
                'offers': {'@type': 'Offer', 'url': BASE_URL + '/contacto'},
                'provider': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            },
            {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE_URL},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Saturn Studio', 'item': BASE_URL + '/saturn-studio'}
                ]
            }
        ],
    },
    'rpa-studio.html': {
        'title': 'RPA Studio | Automatización Robótica de Procesos Empresariales · Rocketbot',
        'desc':  'Automatiza tareas repetitivas con RPA Studio. Robots de software que aumentan la productividad y reducen errores. Escala tus operaciones en Latinoamérica.',
        'url':   BASE_URL + '/rpa-studio',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'SoftwareApplication',
                'name': 'RPA Studio',
                'applicationCategory': 'BusinessApplication',
                'operatingSystem': 'Windows',
                'description': 'Herramienta de automatización robótica de procesos (RPA) para empresas de Latinoamérica.',
                'url': BASE_URL + '/rpa-studio',
                'offers': {'@type': 'Offer', 'url': BASE_URL + '/contacto'},
                'provider': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            },
            {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE_URL},
                    {'@type': 'ListItem', 'position': 2, 'name': 'RPA Studio', 'item': BASE_URL + '/rpa-studio'}
                ]
            }
        ],
    },
    'ai-studio.html': {
        'title': 'AI Studio | Automatización con Inteligencia Artificial para Empresas · Rocketbot',
        'desc':  'Potencia tus procesos con IA. AI Studio procesa correos con NLP, aplica visión computacional y OCR avanzado. Automatización inteligente con Rocketbot.',
        'url':   BASE_URL + '/ai-studio',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'SoftwareApplication',
                'name': 'AI Studio',
                'applicationCategory': 'BusinessApplication',
                'operatingSystem': 'Windows, Web',
                'description': 'Módulo de inteligencia artificial para automatización avanzada: NLP, visión computacional y OCR.',
                'url': BASE_URL + '/ai-studio',
                'offers': {'@type': 'Offer', 'url': BASE_URL + '/contacto'},
                'provider': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            },
            {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE_URL},
                    {'@type': 'ListItem', 'position': 2, 'name': 'AI Studio', 'item': BASE_URL + '/ai-studio'}
                ]
            }
        ],
    },
    'orquestador.html': {
        'title': 'Orquestador | Gestión Centralizada de Robots RPA · Rocketbot',
        'desc':  'Gestiona, monitorea y escala todos tus robots desde un solo lugar. El Orquestador de Rocketbot da control total sobre tus agentes digitales de automatización.',
        'url':   BASE_URL + '/orquestador',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'SoftwareApplication',
                'name': 'Orquestador Rocketbot',
                'applicationCategory': 'BusinessApplication',
                'operatingSystem': 'Web',
                'description': 'Plataforma centralizada de gestión, monitoreo y orquestación de robots de automatización RPA.',
                'url': BASE_URL + '/orquestador',
                'offers': {'@type': 'Offer', 'url': BASE_URL + '/contacto'},
                'provider': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            },
            {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE_URL},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Orquestador', 'item': BASE_URL + '/orquestador'}
                ]
            }
        ],
    },
    'xperience.html': {
        'title': 'Xperience | Portal de Autoservicio para Automatización Empresarial · Rocketbot',
        'desc':  'Permite a los usuarios ejecutar robots sin intervención de TI. Xperience acelera la adopción de automatización en toda tu organización. Suite Rocketbot.',
        'url':   BASE_URL + '/xperience',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'SoftwareApplication',
                'name': 'Xperience',
                'applicationCategory': 'BusinessApplication',
                'operatingSystem': 'Web',
                'description': 'Portal de autoservicio para ejecución de robots de automatización sin dependencia del área de TI.',
                'url': BASE_URL + '/xperience',
                'offers': {'@type': 'Offer', 'url': BASE_URL + '/contacto'},
                'provider': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            },
            {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE_URL},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Xperience', 'item': BASE_URL + '/xperience'}
                ]
            }
        ],
    },
    'contacto.html': {
        'title': 'Contacto | Habla con un Asesor de Automatización Empresarial · Rocketbot',
        'desc':  '¿Listo para automatizar tu empresa? Contacta a un asesor especializado de Rocketbot. Respuesta en 24 horas hábiles. RPA e IA para Latinoamérica.',
        'url':   BASE_URL + '/contacto',
        'robots': 'noindex, follow',   # no indexar el formulario de contacto
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'ContactPage',
                'name': 'Contacto Rocketbot',
                'url': BASE_URL + '/contacto',
                'description': 'Formulario de contacto para hablar con un asesor especializado en automatización empresarial.',
                'provider': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            }
        ],
    },
    'blog.html': {
        'title': 'Blog | Automatización, RPA e Inteligencia Artificial · Rocketbot',
        'desc':  'Artículos, tutoriales y casos de éxito sobre automatización empresarial, RPA e inteligencia artificial. Tendencias del sector con el equipo de Rocketbot.',
        'url':   BASE_URL + '/blog',
        'schema': [
            {
                '@context': 'https://schema.org',
                '@type': 'Blog',
                'name': 'Blog Rocketbot',
                'url': BASE_URL + '/blog',
                'description': 'Blog sobre automatización empresarial, RPA e inteligencia artificial.',
                'publisher': {'@type': 'Organization', 'name': 'Rocketbot', 'url': BASE_URL}
            }
        ],
    },
}

# ─── GA4 SNIPPET (inject once per page, right after <meta charset>) ───────────
GA4_SNIPPET = f"""<!-- Google tag (gtag.js) – GA4 | reemplaza {GA4_ID} con tu Measurement ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
</script>"""

import json as _json

def build_seo_block(page_data):
    """Returns the full SEO meta block to insert after <title>."""
    d = page_data
    robots   = d.get('robots', 'index, follow')
    url      = d['url']
    title    = d['title']
    desc     = d['desc']

    block = f"""<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<meta name="google-site-verification" content="{GSC_TOKEN}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/logos/favicon.ico" sizes="any">
<link rel="icon" href="/assets/logos/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/logos/apple-touch-icon.png">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rocketbot">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_LA">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@rocketbot">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">"""
    return block


def build_schema_block(schemas):
    parts = []
    for s in schemas:
        parts.append(
            '<script type="application/ld+json">\n'
            + _json.dumps(s, ensure_ascii=False, indent=2)
            + '\n</script>'
        )
    return '\n'.join(parts)


for fname, data in PAGES.items():
    if not os.path.exists(fname):
        print(f'{fname}: not found, skipping')
        continue

    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Update <title> and inject SEO meta block
    if '<meta name="description"' not in content:
        new_title = f'<title>{data["title"]}</title>\n{build_seo_block(data)}'
        content = re.sub(r'<title>[^<]*</title>', new_title, content, count=1)
        changed = True
    else:
        # Just update the title if description already present
        content = re.sub(r'<title>[^<]*</title>', f'<title>{data["title"]}</title>', content, count=1)
        changed = True

    # 2. Inject GA4 after <meta charset="utf-8"> (only once)
    if f'gtag/js?id={GA4_ID}' not in content and 'googletagmanager' not in content:
        content = content.replace(
            '<meta charset="utf-8">',
            '<meta charset="utf-8">\n' + GA4_SNIPPET,
            1
        )
        changed = True

    # 3. Inject schema markup before </body>
    if 'application/ld+json' not in content:
        schema_block = build_schema_block(data['schema'])
        content = content.replace('</body>', schema_block + '\n</body>', 1)
        changed = True

    if changed:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

    has_desc   = '<meta name="description"' in content
    has_og     = 'og:title' in content
    has_canon  = 'rel="canonical"' in content
    has_ga4    = 'googletagmanager' in content
    has_schema = 'application/ld+json' in content
    print(f'{fname}: desc={has_desc} og={has_og} canonical={has_canon} ga4={has_ga4} schema={has_schema}')

print('\nDone.')
