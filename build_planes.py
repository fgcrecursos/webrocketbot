# -*- coding: utf-8 -*-
"""
Genera planes.html, en/planes.html y pt/planes.html.

La pagina se arma sobre el esqueleto real del sitio (construir-vs-comprar.html
aporta nav, menu mobile, modal de descarga, footer y scripts) y le inyecta el
contenido de precios. Los tres idiomas salen de la misma estructura, asi que
/en/ y /pt/ no pueden quedar desalineados: si se cambia una fila, se cambia
una sola vez y se vuelve a correr este script.

    python build_planes.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(ROOT, 'construir-vs-comprar.html')
CSS_MARK = '/* ═══ PLANES ═══ */'

LANGS = ('es', 'en', 'pt')
HTML_LANG = {'es': 'es', 'en': 'en', 'pt': 'pt-BR'}
OG_LOCALE = {'es': 'es_LA', 'en': 'en_US', 'pt': 'pt_BR'}


# ───────────────────────── helpers de traduccion ─────────────────────────
def L(es, en, pt):
    return {'es': es, 'en': en, 'pt': pt}


def NUM(n):
    """Miles: 10.000 en es/pt, 10,000 en en."""
    es = '{:,}'.format(n).replace(',', '.')
    en = '{:,}'.format(n)
    return L(es, en, es)


def DIAS(n):
    return L('%d días' % n, '%d days' % n, '%d dias' % n)


def MIN(n):
    return '%d min' % n


ILIM_A = L('Ilimitada', 'Unlimited', 'Ilimitada')
ILIM_AS = L('Ilimitadas', 'Unlimited', 'Ilimitadas')
ILIM_O = L('Ilimitado', 'Unlimited', 'Ilimitado')
ILIM_OS = L('Ilimitados', 'Unlimited', 'Ilimitados')
BASICO = L('Básico', 'Basic', 'Básico')
AVANZADO = L('Avanzado', 'Advanced', 'Avançado')
LIMITADO = L('Limitado', 'Limited', 'Limitado')
CONFIG = L('Configurable', 'Configurable', 'Configurável')
COSTO_AD = L('Costo adicional', 'Additional cost', 'Custo adicional')
COMPARTIDO = L('Compartido', 'Shared', 'Compartilhado')
DEDICADO = L('Dedicado', 'Dedicated', 'Dedicado')


# ───────────────────────── celdas de la tabla ─────────────────────────
def Y():
    return ('y', None)


def N():
    return ('n', None)


def T(v):
    """Texto normal. Acepta str (igual en los 3) o dict."""
    return ('t', v)


def B(v):
    """Texto destacado en rojo: el mejor valor de la fila."""
    return ('b', v)


def tr(val, lang):
    return val[lang] if isinstance(val, dict) else val


# ── aclaracion de no-acumulacion para las lineas con una cantidad concreta ──
# Las tarjetas dicen "Todo lo de X, mas": sin esto se puede leer que las
# cantidades se suman de un plan al siguiente. No se suman.
TIP_CREDITOS = L('Los créditos de AI Studio no son acumulables entre planes: el plan incluye exactamente esta cantidad, no se suma a la del plan anterior.',
                 'AI Studio credits are not cumulative between plans: the plan includes exactly this amount, it is not added to the previous plan’s.',
                 'Os créditos de AI Studio não são acumuláveis entre planos: o plano inclui exatamente esta quantidade, não se soma à do plano anterior.')

TIP_LICENCIAS = L('Las licencias de desarrollo no son acumulables entre planes: el plan incluye exactamente esta cantidad, no se suma a la del plan anterior.',
                  'Development licenses are not cumulative between plans: the plan includes exactly this number, it is not added to the previous plan’s.',
                  'As licenças de desenvolvimento não são acumuláveis entre planos: o plano inclui exatamente esta quantidade, não se soma à do plano anterior.')


def NOTE(text, tip):
    """Item de tarjeta con "?" y el detalle al pasar el cursor."""
    return (text, tip)


# ───────────────────────── contenido de las tarjetas ─────────────────────────
PLANS = [
    {
        'name': 'Entry',
        'feat': False,
        'aud': L('Para equipos que automatizan sus primeros procesos.',
                 'For teams automating their first processes.',
                 'Para times que automatizam seus primeiros processos.'),
        'price': L('7.990', '7,990', '7.990'),
        'cap': L('5 automatizaciones en paralelo',
                 '5 automations running in parallel',
                 '5 automações em paralelo'),
        'inc_lb': L('Incluye', 'Includes', 'Inclui'),
        'inc': [
            L('Todos los productos de la suite',
              'Every product in the suite',
              'Todos os produtos da suíte'),
            NOTE(L('Total de 25M créditos de AI Studio / año',
                   '25M AI Studio credits / year in total',
                   'Total de 25M créditos de AI Studio / ano'), TIP_CREDITOS),
            NOTE(L('Total de 2 licencias de desarrollo', '2 development licenses in total',
                   'Total de 2 licenças de desenvolvimento'),
                 TIP_LICENCIAS),
            L('5 aplicaciones Nexus · 10 usuarios finales',
              '5 Nexus apps · 10 end users',
              '5 aplicativos Nexus · 10 usuários finais'),
            L('Soporte por Slack · respuesta 60 min',
              'Slack support · 60 min first response',
              'Suporte por Slack · resposta em 60 min'),
            L('Auditoría 90 días · 2FA · SSO Google',
              '90-day audit logs · 2FA · Google SSO',
              'Auditoria 90 dias · 2FA · SSO Google'),
        ],
        'addons': [
            L('Atención por evento <b>7×24</b> (costo adicional)',
              '<b>24/7</b> per-event coverage (additional cost)',
              'Atendimento por evento <b>7×24</b> (custo adicional)'),
            L('Créditos de IA extra', 'Extra AI credits', 'Créditos de IA extras'),
        ],
    },
    {
        'name': 'Standard',
        'feat': True,
        'aud': L('Para escalar la automatización a varias áreas.',
                 'For scaling automation across several areas.',
                 'Para escalar a automação para várias áreas.'),
        'price': L('14.990', '14,990', '14.990'),
        'cap': L('20 automatizaciones en paralelo',
                 '20 automations running in parallel',
                 '20 automações em paralelo'),
        'inc_lb': L('Todo lo de Entry, más', 'Everything in Entry, plus', 'Tudo do Entry, mais'),
        'inc': [
            NOTE(L('Total de 50M créditos de AI Studio / año',
                   '50M AI Studio credits / year in total',
                   'Total de 50M créditos de AI Studio / ano'), TIP_CREDITOS),
            NOTE(L('Total de 3 licencias de desarrollo', '3 development licenses in total',
                   'Total de 3 licenças de desenvolvimento'),
                 TIP_LICENCIAS),
            L('Apps ilimitadas (Nexus)',
              'Unlimited apps (Nexus)',
              'Apps ilimitados (Nexus)'),
            L('Bring Your Own Model (IA externa)',
              'Bring Your Own Model (external AI)',
              'Bring Your Own Model (IA externa)'),
            L('Monitoreo en tiempo real', 'Real-time monitoring', 'Monitoramento em tempo real'),
            L('Auditoría 180 días · Customer Success · Meetups',
              '180-day audit logs · Customer Success · Meetups',
              'Auditoria 180 dias · Customer Success · Meetups'),
        ],
        'addons': [
            L('Atención por evento <b>7×24</b> (costo adicional)',
              '<b>24/7</b> per-event coverage (additional cost)',
              'Atendimento por evento <b>7×24</b> (custo adicional)'),
            L('Usuarios finales adicionales', 'Additional end users', 'Usuários finais adicionais'),
            L('Créditos de IA extra', 'Extra AI credits', 'Créditos de IA extras'),
        ],
    },
    {
        'name': 'Enterprise',
        'feat': False,
        'aud': L('Para operaciones críticas con mayor volumen y control.',
                 'For critical operations with more volume and control.',
                 'Para operações críticas com mais volume e controle.'),
        'price': L('24.990', '24,990', '24.990'),
        'cap': L('50 automatizaciones en paralelo',
                 '50 automations running in parallel',
                 '50 automações em paralelo'),
        'inc_lb': L('Todo lo de Standard, más', 'Everything in Standard, plus', 'Tudo do Standard, mais'),
        'inc': [
            NOTE(L('Total de 100M créditos de AI Studio / año',
                   '100M AI Studio credits / year in total',
                   'Total de 100M créditos de AI Studio / ano'), TIP_CREDITOS),
            NOTE(L('Total de 5 licencias de desarrollo', '5 development licenses in total',
                   'Total de 5 licenças de desenvolvimento'),
                 TIP_LICENCIAS),
            L('15 usuarios creadores de apps', '15 app-builder users', '15 usuários criadores de apps'),
            L('50 usuarios finales · 50 usuarios con login',
              '50 end users · 50 users with login',
              '50 usuários finais · 50 usuários com login'),
            L('Respuesta de soporte 30 min', '30 min support response', 'Resposta de suporte em 30 min'),
            L('Mejor capacidad de ejecución en Nexus y Saturn Studio',
              'Better execution capacity in Nexus and Saturn Studio',
              'Melhor capacidade de execução no Nexus e Saturn Studio'),
        ],
        'addons': [
            L('Atención por evento <b>7×24</b> (costo adicional)',
              '<b>24/7</b> per-event coverage (additional cost)',
              'Atendimento por evento <b>7×24</b> (custo adicional)'),
            L('Usuarios y creadores adicionales', 'Additional users and builders', 'Usuários e criadores adicionais'),
            L('Créditos de IA extra', 'Extra AI credits', 'Créditos de IA extras'),
        ],
    },
    {
        'name': 'Corporate',
        'feat': False,
        'aud': L('Para grandes organizaciones con requisitos de seguridad y compliance.',
                 'For large organizations with security and compliance requirements.',
                 'Para grandes organizações com requisitos de segurança e compliance.'),
        'price': L('49.990', '49,990', '49.990'),
        'cap': L('200 en paralelo · 1.000 procesos administrados',
                 '200 in parallel · 1,000 managed processes',
                 '200 em paralelo · 1.000 processos administrados'),
        'inc_lb': L('Todo lo de Enterprise, más', 'Everything in Enterprise, plus', 'Tudo do Enterprise, mais'),
        'inc': [
            NOTE(L('Total de 200M créditos de AI Studio / año',
                   '200M AI Studio credits / year in total',
                   'Total de 200M créditos de AI Studio / ano'), TIP_CREDITOS),
            L('Licencias y usuarios ilimitados', 'Unlimited licenses and users', 'Licenças e usuários ilimitados'),
            L('SSO corporativo (Active Directory) · SCIM',
              'Corporate SSO (Active Directory) · SCIM',
              'SSO corporativo (Active Directory) · SCIM'),
            L('Auditoría 12 meses + export SIEM',
              '12-month audit logs + SIEM export',
              'Auditoria 12 meses + export SIEM'),
            L('Máxima capacidad de ejecución en Nexus y Saturn Studio',
              'Highest execution capacity in Nexus and Saturn Studio',
              'Máxima capacidade de execução no Nexus e Saturn Studio'),
            L('Customer Success dedicado · respuesta 15 min',
              'Dedicated Customer Success · 15 min response',
              'Customer Success dedicado · resposta em 15 min'),
        ],
        'addons': [
            L('Atención por evento <b>7×24</b> (costo adicional)',
              '<b>24/7</b> per-event coverage (additional cost)',
              'Atendimento por evento <b>7×24</b> (custo adicional)'),
            L('Onboarding y capacitación a medida', 'Tailored onboarding and training',
              'Onboarding e capacitação sob medida'),
        ],
    },
]


# ───────────────────────── filas de la comparativa ─────────────────────────
# ('grp', titulo) | ('row', etiqueta, nota, [entry, standard, enterprise, corporate])
ROWS = [
    ('grp', L('Productos incluidos', 'Products included', 'Produtos incluídos')),
    ('row', 'RPA Studio',
     L('Robots de software que operan cualquier sistema como una persona: hacen clic, copian datos, llenan formularios.',
       'Software robots that operate any system like a person: they click, copy data and fill in forms.',
       'Robôs de software que operam qualquer sistema como uma pessoa: clicam, copiam dados, preenchem formulários.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'Saturn Studio',
     L('Constructor de flujos en la nube que conecta más de 500 aplicaciones sin instalar nada.',
       'Cloud flow builder that connects more than 500 apps with nothing to install.',
       'Construtor de fluxos na nuvem que conecta mais de 500 aplicativos sem instalar nada.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Orquestador + Xperience', 'Orchestrator + Xperience', 'Orquestrador + Xperience'),
     L('Panel central para programar, ejecutar y monitorear tus automatizaciones. Incluye portal de formularios de autoservicio.',
       'Central panel to schedule, run and monitor your automations. Includes the self-service forms portal.',
       'Painel central para agendar, executar e monitorar suas automações. Inclui portal de formulários de autoatendimento.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'AI Studio',
     L('IA que lee y entiende documentos, correos, imágenes y audio para automatizar decisiones.',
       'AI that reads and understands documents, email, images and audio to automate decisions.',
       'IA que lê e entende documentos, e-mails, imagens e áudio para automatizar decisões.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'Nexus',
     L('Crea aplicaciones de negocio a medida para tu equipo, sin escribir código.',
       'Build tailor-made business apps for your team, without writing code.',
       'Crie aplicativos de negócio sob medida para seu time, sem escrever código.'),
     [Y(), Y(), Y(), Y()]),

    ('grp', 'RPA Studio'),
    ('row', L('Licencias de desarrollo', 'Development licenses', 'Licenças de desenvolvimento'),
     L('Personas que pueden construir y editar automatizaciones y apps en la plataforma.',
       'People who can build and edit automations and apps on the platform.',
       'Pessoas que podem construir e editar automações e apps na plataforma.'),
     [T('2'), T('3'), T('5'), B(ILIM_AS)]),

    ('grp', L('Saturn Studio — Motor de ejecución', 'Saturn Studio — Execution engine',
              'Saturn Studio — Motor de execução')),
    ('row', L('Automatizaciones en paralelo', 'Automations running in parallel', 'Automações em paralelo'),
     L('Cuántas automatizaciones pueden ejecutarse al mismo tiempo. Es tu capacidad de trabajo simultáneo.',
       'How many automations can run at the same time. This is your simultaneous work capacity.',
       'Quantas automações podem ser executadas ao mesmo tempo. É sua capacidade de trabalho simultâneo.'),
     [T('5'), T('20'), T('50'), B('200')]),
    ('row', L('Tiempo máximo por flujo', 'Maximum time per flow', 'Tempo máximo por fluxo'),
     L('Duración máxima que puede correr una automatización antes de detenerse.',
       'Maximum time an automation can run before it stops.',
       'Duração máxima que uma automação pode rodar antes de parar.'),
     [T(MIN(10)), T(MIN(30)), T(MIN(30)), T(L('1 hora', '1 hour', '1 hora'))]),
    ('row', L('Intervalo mínimo entre ejecuciones', 'Minimum interval between runs',
              'Intervalo mínimo entre execuções'),
     L('Tiempo mínimo de espera entre dos ejecuciones consecutivas de una misma automatización.',
       'Minimum wait between two consecutive runs of the same automation.',
       'Tempo mínimo de espera entre duas execuções consecutivas da mesma automação.'),
     [T(MIN(1)), T(MIN(1)), T(MIN(1)), T(MIN(0))]),
    ('row', L('Tamaño máximo de archivo', 'Maximum file size', 'Tamanho máximo de arquivo'),
     L('Peso máximo de un archivo que una automatización puede procesar.',
       'Maximum size of a file an automation can process.',
       'Peso máximo de um arquivo que uma automação pode processar.'),
     [T('100 MB'), T('250 MB'), T('250 MB'), T('1 GB')]),
    ('row', L('Moons consecutivos por ejecución', 'Consecutive Moons per run',
              'Moons consecutivos por execução'),
     L('Moons son los pasos o acciones que ejecuta un flujo. Este es el máximo por ejecución.',
       'Moons are the steps or actions a flow runs. This is the maximum per run.',
       'Moons são os passos ou ações que um fluxo executa. Este é o máximo por execução.'),
     [T(NUM(10000)), T(NUM(30000)), T(NUM(30000)), T(ILIM_O)]),
    ('row', L('Mejor capacidad de ejecución en Nexus y Saturn Studio',
              'Better execution capacity in Nexus and Saturn Studio',
              'Melhor capacidade de execução no Nexus e Saturn Studio'),
     L('Capacidad de procesamiento asignada a tus ejecuciones cuando hay mucha carga en cola. A mayor capacidad, menos espera.',
       'Processing capacity allocated to your runs when the queue is under heavy load. More capacity means less waiting.',
       'Capacidade de processamento alocada às suas execuções quando há muita carga na fila. Quanto maior a capacidade, menor a espera.'),
     [T(L('Estándar', 'Standard', 'Padrão')), T(L('Alta', 'High', 'Alta')),
      T(L('Alta', 'High', 'Alta')), B(L('Máxima', 'Highest', 'Máxima'))]),

    ('grp', L('Saturn Studio — Builder e integraciones', 'Saturn Studio — Builder and integrations',
              'Saturn Studio — Builder e integrações')),
    ('row', L('Cantidad de flujos', 'Number of flows', 'Quantidade de fluxos'),
     L('Número de automatizaciones distintas que puedes diseñar y guardar.',
       'How many different automations you can design and save.',
       'Número de automações distintas que você pode desenhar e salvar.'),
     [T(ILIM_A), T(ILIM_A), T(ILIM_A), T(ILIM_A)]),
    ('row', L('Funciones personalizadas (JS)', 'Custom functions (JS)', 'Funções personalizadas (JS)'),
     L('Código JavaScript propio para lógica avanzada dentro de los flujos.',
       'Your own JavaScript code for advanced logic inside the flows.',
       'Código JavaScript próprio para lógica avançada dentro dos fluxos.'),
     [N(), T(LIMITADO), T(LIMITADO), T(AVANZADO)]),
    ('row', 'Templates',
     L('Plantillas prediseñadas para acelerar la creación de automatizaciones.',
       'Ready-made templates to speed up building automations.',
       'Modelos prontos para acelerar a criação de automações.'),
     [T('Extended'), T('Full'), T('Full'), T('Full + Custom')]),
    ('row', L('Apps y componentes estándar', 'Standard apps and components',
              'Apps e componentes padrão'),
     L('Conectores e integraciones listas para usar con aplicaciones externas.',
       'Ready-to-use connectors and integrations with external apps.',
       'Conectores e integrações prontos para usar com aplicativos externos.'),
     [T('500+'), T('500+'), T('500+'), T('500+')]),
    ('row', 'Webhooks',
     L('Un webhook permite que un sistema externo dispare una automatización mediante una llamada web.',
       'A webhook lets an external system trigger an automation through a web call.',
       'Um webhook permite que um sistema externo dispare uma automação por meio de uma chamada web.'),
     [T('5'), T('20'), T('50'), B('200')]),
    ('row', L('Apps personalizadas', 'Custom apps', 'Apps personalizados'),
     L('Conectores a medida para sistemas que no están en el catálogo estándar.',
       'Tailor-made connectors for systems outside the standard catalog.',
       'Conectores sob medida para sistemas que não estão no catálogo padrão.'),
     [N(), T(LIMITADO), T(LIMITADO), T(AVANZADO)]),
    ('row', 'Apps Enterprise',
     L('Conectores a sistemas empresariales de gran escala (ERP, mainframe, etc.).',
       'Connectors to large-scale enterprise systems (ERP, mainframe, etc.).',
       'Conectores para sistemas empresariais de grande escala (ERP, mainframe, etc.).'),
     [N(), N(), N(), T('Basic')]),
    ('row', L('Conexión con LLMs', 'LLM connection', 'Conexão com LLMs'),
     L('Usa modelos de lenguaje de terceros dentro de los flujos de Saturn Studio.',
       'Use third-party language models inside Saturn Studio flows.',
       'Use modelos de linguagem de terceiros dentro dos fluxos do Saturn Studio.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'Human in the Loop',
     L('Pasos donde una persona aprueba o interviene dentro de una automatización.',
       'Steps where a person approves or steps into an automation.',
       'Etapas em que uma pessoa aprova ou intervem dentro de uma automação.'),
     [Y(), Y(), Y(), Y()]),

    ('grp', L('Saturn Studio — Monitoreo y analytics', 'Saturn Studio — Monitoring and analytics',
              'Saturn Studio — Monitoramento e analytics')),
    ('row', L('Ejecuciones guardadas', 'Stored runs', 'Execuções salvas'),
     L('Historial de ejecuciones que se conserva para consulta.',
       'Run history kept available for review.',
       'Histórico de execuções mantido para consulta.'),
     [T(NUM(1000)), T(NUM(5000)), T(NUM(5000)), B(NUM(100000))]),
    ('row', L('Retención de logs de ejecución', 'Execution log retention',
              'Retenção de logs de execução'),
     L('Cuánto tiempo se guardan los registros de cada ejecución.',
       'How long the records of each run are kept.',
       'Por quanto tempo os registros de cada execução são guardados.'),
     [T(DIAS(7)), T(DIAS(30)), T(DIAS(30)), B(DIAS(365))]),
    ('row', L('Monitoreo en tiempo real', 'Real-time monitoring', 'Monitoramento em tempo real'),
     L('Visualización en vivo del estado y desempeño de tus automatizaciones.',
       'Live view of the status and performance of your automations.',
       'Visualização ao vivo do status e do desempenho das suas automações.'),
     [N(), T(BASICO), T(BASICO), B(AVANZADO)]),
    ('row', L('Búsqueda full-text en logs', 'Full-text search in logs', 'Busca full-text nos logs'),
     L('Buscar texto libre dentro de los registros de ejecución.',
       'Search free text inside the execution records.',
       'Buscar texto livre dentro dos registros de execução.'),
     [N(), T(BASICO), T(BASICO), B(AVANZADO)]),
    ('row', L('Dashboard de analytics', 'Analytics dashboard', 'Dashboard de analytics'),
     L('Tableros con métricas de uso y desempeño de las automatizaciones.',
       'Dashboards with usage and performance metrics for your automations.',
       'Painéis com métricas de uso e desempenho das automações.'),
     [T('Standard'), T('Advanced'), T('Advanced'), B('Enterprise')]),

    ('grp', L('Saturn Studio — Gobernanza y seguridad', 'Saturn Studio — Governance and security',
              'Saturn Studio — Governança e segurança')),
    ('row', L('Miembros del equipo', 'Team members', 'Membros do time'),
     L('Personas que pueden acceder al espacio de trabajo de Saturn Studio.',
       'People who can access the Saturn Studio workspace.',
       'Pessoas que podem acessar o espaço de trabalho do Saturn Studio.'),
     [T('5'), T('15'), T('15'), B(ILIM_OS)]),
    ('row', L('Equipos y roles', 'Teams and roles', 'Times e papéis'),
     L('Organización de usuarios en equipos con permisos diferenciados.',
       'Organize users into teams with different permissions.',
       'Organização de usuários em times com permissões diferenciadas.'),
     [N(), T(BASICO), T(BASICO), B(AVANZADO)]),
    ('row', L('Bóveda de credenciales cifrada', 'Encrypted secrets store', 'Cofre de credenciais criptografado'),
     L('Bóveda cifrada para guardar credenciales y datos sensibles.',
       'Encrypted vault for credentials and sensitive data.',
       'Cofre criptografado para guardar credenciais e dados sensíveis.'),
     [N(), T(BASICO), T(BASICO), B(AVANZADO)]),
    ('row', L('Autenticación 2FA', 'Two-factor authentication', 'Autenticação 2FA'),
     L('Segundo factor de autenticación. Heredado del Orquestador, punto único de identidad de la suite.',
       'Second authentication factor. Inherited from the Orchestrator, the suite’s single identity point.',
       'Segundo fator de autenticação. Herdado do Orquestrador, ponto único de identidade da suíte.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'SSO (Google / OAuth)',
     L('Inicio de sesión con Google. Heredado del Orquestador.',
       'Sign in with Google. Inherited from the Orchestrator.',
       'Login com Google. Herdado do Orquestrador.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('SSO corporativo (Active Directory)', 'Corporate SSO (Active Directory)',
              'SSO corporativo (Active Directory)'),
     L('Autenticación con el directorio corporativo. Exclusivo de Corporate. Heredado del Orquestador.',
       'Authentication against the corporate directory. Corporate only. Inherited from the Orchestrator.',
       'Autenticação com o diretório corporativo. Exclusivo do Corporate. Herdado do Orquestrador.'),
     [N(), N(), N(), Y()]),
    ('row', 'Audit logs',
     L('Registro de eventos de seguridad de Saturn Studio: quién hizo qué y cuándo.',
       'Security event log for Saturn Studio: who did what and when.',
       'Registro de eventos de segurança do Saturn Studio: quem fez o quê e quando.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Retención de audit logs', 'Audit log retention', 'Retenção de audit logs'),
     L('Cuánto tiempo se conservan los audit logs de Saturn Studio. Corporate cumple el benchmark de 12 meses.',
       'How long Saturn Studio audit logs are kept. Corporate meets the 12-month benchmark.',
       'Por quanto tempo os audit logs do Saturn Studio são mantidos. O Corporate atende ao benchmark de 12 meses.'),
     [T(DIAS(90)), T(DIAS(180)), T(DIAS(180)), B(DIAS(365))]),
    ('row', L('Export de audit logs (API / SIEM)', 'Audit log export (API / SIEM)',
              'Export de audit logs (API / SIEM)'),
     L('Exportar los audit logs a un sistema SIEM externo vía API. Exclusivo de Corporate.',
       'Export audit logs to an external SIEM through the API. Corporate only.',
       'Exportar os audit logs para um SIEM externo via API. Exclusivo do Corporate.'),
     [N(), N(), N(), Y()]),

    ('grp', L('Orquestador — Capacidad de ejecución', 'Orchestrator — Execution capacity',
              'Orquestrador — Capacidade de execução')),
    ('row', L('Procesos administrados', 'Managed processes', 'Processos administrados'),
     L('Total de procesos que el Orquestador retiene y administra (desplegados).',
       'Total processes the Orchestrator holds and manages (deployed).',
       'Total de processos que o Orquestrador retém e administra (implantados).'),
     [T('5'), T('20'), T('50'), B(NUM(1000))]),
    ('row', L('Procesos en ejecución paralela', 'Processes running in parallel',
              'Processos em execução paralela'),
     L('Procesos corriendo simultáneamente en el Orquestador. Independiente del paralelo de Saturn.',
       'Processes running simultaneously in the Orchestrator. Independent from Saturn’s parallelism.',
       'Processos rodando simultaneamente no Orquestrador. Independente do paralelo do Saturn.'),
     [T('5'), T('20'), T('50'), B('200')]),
    ('row', L('Robots registrables', 'Registerable robots', 'Robôs registráveis'),
     L('Máquinas o agentes conectados al Orquestador. Se registran sin límite y no consumen capacidad.',
       'Machines or agents connected to the Orchestrator. They register without limit and consume no capacity.',
       'Máquinas ou agentes conectados ao Orquestrador. Registram-se sem limite e não consomem capacidade.'),
     [T(ILIM_OS), T(ILIM_OS), T(ILIM_OS), T(ILIM_OS)]),

    ('grp', L('Xperience — Portal de autoservicio', 'Xperience — Self-service portal',
              'Xperience — Portal de autoatendimento')),
    ('row', L('Xperience incluido', 'Xperience included', 'Xperience incluído'),
     L('Portal de formularios de autoservicio incluido en todos los planes.',
       'Self-service forms portal included in every plan.',
       'Portal de formulários de autoatendimento incluído em todos os planos.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Formularios públicos', 'Public forms', 'Formulários públicos'),
     L('Formularios con enlace abierto, sin login, para recibir solicitudes externas.',
       'Open-link forms, no login, to receive external requests.',
       'Formulários com link aberto, sem login, para receber solicitações externas.'),
     [T(ILIM_OS), T(ILIM_OS), T(ILIM_OS), T(ILIM_OS)]),
    ('row', L('Formularios privados', 'Private forms', 'Formulários privados'),
     L('Formularios con login y permisos por rol.',
       'Forms with login and role-based permissions.',
       'Formulários com login e permissões por papel.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Usuarios con login', 'Users with login', 'Usuários com login'),
     L('Personas que acceden a formularios privados con usuario y permisos por rol.',
       'People who access private forms with a user account and role-based permissions.',
       'Pessoas que acessam formulários privados com usuário e permissões por papel.'),
     [T('10'), T('25'), T('50'), B(ILIM_OS)]),

    ('grp', L('Orquestador — Gestión y observabilidad', 'Orchestrator — Management and observability',
              'Orquestrador — Gestão e observabilidade')),
    ('row', L('Usuarios Process Control', 'Process Control users', 'Usuários Process Control'),
     L('Personas que operan y supervisan las automatizaciones desde el panel del Orquestador.',
       'People who operate and supervise automations from the Orchestrator panel.',
       'Pessoas que operam e supervisionam as automações pelo painel do Orquestrador.'),
     [T('5'), T('5'), T('15'), B(ILIM_OS)]),
    ('row', L('Retención de logs de ejecución', 'Execution log retention',
              'Retenção de logs de execução'),
     L('Cuánto tiempo se guardan los registros de ejecución del Orquestador.',
       'How long the Orchestrator keeps its execution records.',
       'Por quanto tempo os registros de execução do Orquestrador são guardados.'),
     [T(DIAS(7)), T(DIAS(30)), T(DIAS(30)), B(DIAS(365))]),

    ('grp', L('Orquestador — Gobernanza y seguridad', 'Orchestrator — Governance and security',
              'Orquestrador — Governança e segurança')),
    ('row', L('Autenticación 2FA', 'Two-factor authentication', 'Autenticação 2FA'),
     L('Segundo factor de autenticación. El Orquestador es el punto único de identidad de la suite.',
       'Second authentication factor. The Orchestrator is the suite’s single identity point.',
       'Segundo fator de autenticação. O Orquestrador é o ponto único de identidade da suíte.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'SSO (Google / OAuth)',
     L('Inicio de sesión con Google, para toda la suite.',
       'Sign in with Google, for the whole suite.',
       'Login com Google, para toda a suíte.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('SSO corporativo (Active Directory)', 'Corporate SSO (Active Directory)',
              'SSO corporativo (Active Directory)'),
     L('Autenticación con el directorio corporativo. Exclusivo de Corporate.',
       'Authentication against the corporate directory. Corporate only.',
       'Autenticação com o diretório corporativo. Exclusivo do Corporate.'),
     [N(), N(), N(), Y()]),
    ('row', 'Audit logs',
     L('Registro de eventos de seguridad del Orquestador: quién hizo qué y cuándo.',
       'Security event log for the Orchestrator: who did what and when.',
       'Registro de eventos de segurança do Orquestrador: quem fez o quê e quando.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Retención de audit logs', 'Audit log retention', 'Retenção de audit logs'),
     L('Cuánto tiempo se conservan los audit logs del Orquestador. Corporate cumple el benchmark de 12 meses.',
       'How long the Orchestrator audit logs are kept. Corporate meets the 12-month benchmark.',
       'Por quanto tempo os audit logs do Orquestrador são mantidos. O Corporate atende ao benchmark de 12 meses.'),
     [T(DIAS(90)), T(DIAS(180)), T(DIAS(180)), B(DIAS(365))]),
    ('row', L('Export de audit logs (API / SIEM)', 'Audit log export (API / SIEM)',
              'Export de audit logs (API / SIEM)'),
     L('Exportar los audit logs a un sistema SIEM externo vía API. Exclusivo de Corporate.',
       'Export audit logs to an external SIEM through the API. Corporate only.',
       'Exportar os audit logs para um SIEM externo via API. Exclusivo do Corporate.'),
     [N(), N(), N(), Y()]),

    ('grp', 'AI Studio'),
    ('row', L('Créditos de AI Studio / año', 'AI Studio credits / year', 'Créditos de AI Studio / ano'),
     L('Volumen anual de procesamiento con IA incluido en el plan. Sin acumulación al ciclo siguiente.',
       'Annual AI processing volume included in the plan. It does not roll over to the next cycle.',
       'Volume anual de processamento com IA incluído no plano. Sem acumulação para o ciclo seguinte.'),
     [T('25M'), T('50M'), T('100M'), B('200M')]),
    ('row', L('Modelo de IA incluido', 'AI model included', 'Modelo de IA incluído'),
     L('Motor interno de AI Studio, operando dentro del entorno Rocketbot.',
       'AI Studio’s internal engine, running inside the Rocketbot environment.',
       'Motor interno do AI Studio, operando dentro do ambiente Rocketbot.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'Bring Your Own Model',
     L('Conecta tu propio modelo de IA externo (Azure OpenAI, Bedrock, etc.) en AI Studio.',
       'Connect your own external AI model (Azure OpenAI, Bedrock, etc.) in AI Studio.',
       'Conecte seu próprio modelo de IA externo (Azure OpenAI, Bedrock, etc.) no AI Studio.'),
     [N(), Y(), Y(), Y()]),
    ('row', L('Documentos — tamaño máx. (PDF, TXT)', 'Documents — max size (PDF, TXT)',
              'Documentos — tamanho máx. (PDF, TXT)'),
     L('Peso máximo de un documento que AI Studio puede procesar.',
       'Maximum size of a document AI Studio can process.',
       'Peso máximo de um documento que o AI Studio pode processar.'),
     [T('25 MB'), T('25 MB'), T('25 MB'), T('25 MB')]),
    ('row', L('Correo — tamaño máx.', 'Email — max size', 'E-mail — tamanho máx.'),
     L('Peso máximo por mensaje de correo, incluidos adjuntos (Gmail, Outlook, IMAP, POP3).',
       'Maximum size per email message, attachments included (Gmail, Outlook, IMAP, POP3).',
       'Peso máximo por mensagem de e-mail, anexos incluídos (Gmail, Outlook, IMAP, POP3).'),
     [T('25 MB'), T('25 MB'), T('25 MB'), T('25 MB')]),
    ('row', L('Imágenes — tamaño máx.', 'Images — max size', 'Imagens — tamanho máx.'),
     L('Peso máximo de una imagen (PNG, JPEG, JPG, WEBP, GIF no animado).',
       'Maximum size of an image (PNG, JPEG, JPG, WEBP, non-animated GIF).',
       'Peso máximo de uma imagem (PNG, JPEG, JPG, WEBP, GIF não animado).'),
     [T('10 MB'), T('10 MB'), T('10 MB'), T('10 MB')]),
    ('row', L('Audio — tamaño máx. (MP3, WAV)', 'Audio — max size (MP3, WAV)',
              'Áudio — tamanho máx. (MP3, WAV)'),
     L('Peso máximo de un archivo de audio que AI Studio puede procesar.',
       'Maximum size of an audio file AI Studio can process.',
       'Peso máximo de um arquivo de áudio que o AI Studio pode processar.'),
     [T('25 MB'), T('25 MB'), T('25 MB'), T('25 MB')]),

    ('grp', L('Nexus — Plan y usuarios', 'Nexus — Plan and users', 'Nexus — Plano e usuários')),
    ('row', L('Usuarios creadores de apps', 'App-builder users', 'Usuários criadores de apps'),
     L('Usuarios con permisos para construir aplicaciones en Nexus.',
       'Users allowed to build applications in Nexus.',
       'Usuários com permissão para construir aplicativos no Nexus.'),
     [T('5'), T('5'), T('15'), B(ILIM_OS)]),
    ('row', L('Usuarios finales', 'End users', 'Usuários finais'),
     L('Personas que usan las apps publicadas sin permisos de construcción.',
       'People who use published apps without build permissions.',
       'Pessoas que usam os apps publicados sem permissões de construção.'),
     [T('10'), T('25'), T('50'), B(ILIM_OS)]),
    ('row', L('Creadores adicionales (add-on)', 'Additional builders (add-on)',
              'Criadores adicionais (add-on)'),
     L('Posibilidad de sumar más usuarios creadores como complemento pagado.',
       'Option to add more builder users as a paid add-on.',
       'Possibilidade de somar mais usuários criadores como complemento pago.'),
     [N(), Y(), Y(), Y()]),

    ('grp', L('Nexus — Capacidad', 'Nexus — Capacity', 'Nexus — Capacidade')),
    ('row', L('Aplicaciones', 'Applications', 'Aplicativos'),
     L('Cantidad de aplicaciones de negocio que puedes crear en Nexus.',
       'How many business applications you can create in Nexus.',
       'Quantidade de aplicativos de negócio que você pode criar no Nexus.'),
     [T('5'), T(ILIM_AS), T(ILIM_AS), T(ILIM_AS)]),
    ('row', L('Filas máx. base interna', 'Max rows, internal database', 'Linhas máx. base interna'),
     L('Número máximo de registros en la base de datos interna de Nexus.',
       'Maximum number of records in the Nexus internal database.',
       'Número máximo de registros na base de dados interna do Nexus.'),
     [T(NUM(50000)), T(NUM(500000)), T(NUM(500000)), B(ILIM_O)]),
    ('row', L('Timeout por query', 'Timeout per query', 'Timeout por query'),
     L('Tiempo máximo que puede tardar una consulta a datos antes de cancelarse.',
       'Maximum time a data query can take before it is cancelled.',
       'Tempo máximo que uma consulta a dados pode levar antes de ser cancelada.'),
     [T('30 s'), T('60 s'), T('60 s'), T(CONFIG)]),
    ('row', L('Timeout por función JS', 'Timeout per JS function', 'Timeout por função JS'),
     L('Tiempo máximo de ejecución de una función JavaScript en una app.',
       'Maximum run time for a JavaScript function inside an app.',
       'Tempo máximo de execução de uma função JavaScript em um app.'),
     [T('10 s'), T('30 s'), T('30 s'), T(CONFIG)]),
    ('row', L('Request body máx.', 'Max request body', 'Request body máx.'),
     L('Tamaño máximo del cuerpo de una petición HTTP que la app puede recibir o enviar.',
       'Maximum body size of an HTTP request the app can receive or send.',
       'Tamanho máximo do corpo de uma requisição HTTP que o app pode receber ou enviar.'),
     [T('10 MB'), T('50 MB'), T('50 MB'), T(CONFIG)]),

    ('grp', L('Nexus — Builder e integraciones', 'Nexus — Builder and integrations',
              'Nexus — Builder e integrações')),
    ('row', 'AI Builder (MCP)',
     L('Asistente de IA para construir apps. MCP conecta modelos con herramientas y datos.',
       'AI assistant for building apps. MCP connects models with tools and data.',
       'Assistente de IA para construir apps. O MCP conecta modelos com ferramentas e dados.'),
     [T(BASICO), T(AVANZADO), T(AVANZADO), B(AVANZADO)]),
    ('row', L('Data sources externas', 'External data sources', 'Data sources externas'),
     L('Conexión a MySQL, PostgreSQL, Supabase, Google Sheets, S3 y más.',
       'Connect to MySQL, PostgreSQL, Supabase, Google Sheets, S3 and more.',
       'Conexão com MySQL, PostgreSQL, Supabase, Google Sheets, S3 e mais.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Integración con la suite Rocketbot', 'Integration with the Rocketbot suite',
              'Integração com a suíte Rocketbot'),
     L('Nexus se conecta con el resto de los productos de la suite.',
       'Nexus connects with the rest of the products in the suite.',
       'O Nexus se conecta com o restante dos produtos da suíte.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'On-Premises Gateway',
     L('Puente seguro para conectar Nexus con sistemas en la red interna del cliente.',
       'Secure bridge to connect Nexus with systems on the customer’s internal network.',
       'Ponte segura para conectar o Nexus a sistemas na rede interna do cliente.'),
     [N(), Y(), Y(), Y()]),
    ('row', 'REST API + API externa + MCP Server',
     L('Interfaces de programación para integrar Nexus con otros sistemas.',
       'Programming interfaces to integrate Nexus with other systems.',
       'Interfaces de programação para integrar o Nexus com outros sistemas.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Import/Export de apps (JSON)', 'App import/export (JSON)', 'Import/Export de apps (JSON)'),
     L('Exportar e importar aplicaciones completas en formato JSON.',
       'Export and import complete applications in JSON format.',
       'Exportar e importar aplicativos completos em formato JSON.'),
     [Y(), Y(), Y(), Y()]),

    ('grp', L('Nexus — Observabilidad y seguridad', 'Nexus — Observability and security',
              'Nexus — Observabilidade e segurança')),
    ('row', L('Retención de logs de ejecución', 'Execution log retention',
              'Retenção de logs de execução'),
     L('Cuánto tiempo se guardan los registros de ejecución de Nexus.',
       'How long Nexus keeps its execution records.',
       'Por quanto tempo os registros de execução do Nexus são guardados.'),
     [T(DIAS(7)), T(DIAS(30)), T(DIAS(30)), B(DIAS(365))]),
    ('row', L('Backups y restore', 'Backups and restore', 'Backups e restore'),
     L('Copias de seguridad y restauración de aplicaciones y datos.',
       'Backup and restore of applications and data.',
       'Cópias de segurança e restauração de aplicativos e dados.'),
     [N(), Y(), Y(), Y()]),
    ('row', L('Grupos de usuarios', 'User groups', 'Grupos de usuários'),
     L('Gestión de acceso de varios usuarios a la vez mediante grupos.',
       'Manage access for several users at once through groups.',
       'Gestão de acesso de vários usuários de uma vez por meio de grupos.'),
     [N(), Y(), Y(), Y()]),
    ('row', L('Variables de entorno cifradas', 'Encrypted environment variables',
              'Variáveis de ambiente criptografadas'),
     L('Configuración y secretos almacenados de forma cifrada, separados por ambiente.',
       'Configuration and secrets stored encrypted, separated by environment.',
       'Configuração e segredos armazenados de forma criptografada, separados por ambiente.'),
     [N(), Y(), Y(), Y()]),
    ('row', L('Autenticación 2FA', 'Two-factor authentication', 'Autenticação 2FA'),
     L('Segundo factor de autenticación. Heredado del Orquestador, punto único de identidad de la suite.',
       'Second authentication factor. Inherited from the Orchestrator, the suite’s single identity point.',
       'Segundo fator de autenticação. Herdado do Orquestrador, ponto único de identidade da suíte.'),
     [Y(), Y(), Y(), Y()]),
    ('row', 'SSO (Google / OAuth)',
     L('Inicio de sesión con Google. Heredado del Orquestador.',
       'Sign in with Google. Inherited from the Orchestrator.',
       'Login com Google. Herdado do Orquestrador.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('SSO corporativo (Active Directory)', 'Corporate SSO (Active Directory)',
              'SSO corporativo (Active Directory)'),
     L('Autenticación con el directorio corporativo. Exclusivo de Corporate.',
       'Authentication against the corporate directory. Corporate only.',
       'Autenticação com o diretório corporativo. Exclusivo do Corporate.'),
     [N(), N(), N(), Y()]),
    ('row', 'SSO enforced',
     L('SSO obligatorio para todos los usuarios. Exclusivo de Corporate (Nexus Enterprise).',
       'SSO enforced for every user. Corporate only (Nexus Enterprise).',
       'SSO obrigatório para todos os usuários. Exclusivo do Corporate (Nexus Enterprise).'),
     [N(), N(), N(), Y()]),
    ('row', 'AD / SCIM',
     L('Aprovisionamiento automático de usuarios vía directorio corporativo (SCIM). Exclusivo de Corporate.',
       'Automatic user provisioning through the corporate directory (SCIM). Corporate only.',
       'Provisionamento automático de usuários via diretório corporativo (SCIM). Exclusivo do Corporate.'),
     [N(), N(), N(), Y()]),
    ('row', 'Audit logs',
     L('Registro de eventos de seguridad de Nexus: quién hizo qué y cuándo.',
       'Security event log for Nexus: who did what and when.',
       'Registro de eventos de segurança do Nexus: quem fez o quê e quando.'),
     [Y(), Y(), Y(), Y()]),
    ('row', L('Retención de audit logs', 'Audit log retention', 'Retenção de audit logs'),
     L('Cuánto tiempo se conservan los audit logs de Nexus. Corporate cumple el benchmark de 12 meses.',
       'How long Nexus audit logs are kept. Corporate meets the 12-month benchmark.',
       'Por quanto tempo os audit logs do Nexus são mantidos. O Corporate atende ao benchmark de 12 meses.'),
     [T(DIAS(90)), T(DIAS(180)), T(DIAS(180)), B(DIAS(365))]),
    ('row', L('Export de audit logs (API / SIEM)', 'Audit log export (API / SIEM)',
              'Export de audit logs (API / SIEM)'),
     L('Exportar los audit logs a un sistema SIEM externo vía API. Exclusivo de Corporate.',
       'Export audit logs to an external SIEM through the API. Corporate only.',
       'Exportar os audit logs para um SIEM externo via API. Exclusivo do Corporate.'),
     [N(), N(), N(), Y()]),

    ('grp', L('Soporte', 'Support', 'Suporte')),
    ('row', L('Canal de soporte', 'Support channel', 'Canal de suporte'),
     L('Canal de Slack dedicado con nuestro equipo, en horario hábil (5×8).',
       'Dedicated Slack channel with our team, during business hours (5×8).',
       'Canal de Slack dedicado com nosso time, em horário comercial (5×8).'),
     [T('Slack'), T('Slack'), T('Slack'), T('Slack')]),
    ('row', L('Primera respuesta (horario 5×8)', 'First response (5×8 hours)',
              'Primeira resposta (horário 5×8)'),
     L('Tiempo máximo hasta la primera respuesta del equipo de soporte, en horario hábil.',
       'Maximum time to the support team’s first response, during business hours.',
       'Tempo máximo até a primeira resposta do time de suporte, em horário comercial.'),
     [T(MIN(60)), T(MIN(45)), T(MIN(30)), B(MIN(15))]),
    ('row', L('Atención por evento 7×24', '24/7 per-event coverage', 'Atendimento por evento 7×24'),
     L('Cobertura fuera del horario hábil para eventos puntuales. Disponible en todos los planes con costo adicional.',
       'Out-of-hours coverage for specific events. Available in every plan at an additional cost.',
       'Cobertura fora do horário comercial para eventos pontuais. Disponível em todos os planos com custo adicional.'),
     [T(COSTO_AD), T(COSTO_AD), T(COSTO_AD), T(COSTO_AD)]),
    ('row', 'Customer Success',
     L('Equipo que te acompaña en la adopción y el crecimiento de tu operación. Dedicado en Corporate.',
       'The team that supports you through adoption and the growth of your operation. Dedicated in Corporate.',
       'Time que acompanha você na adoção e no crescimento da sua operação. Dedicado no Corporate.'),
     [T(COMPARTIDO), T(COMPARTIDO), T(COMPARTIDO), B(DEDICADO)]),
    ('row', L('Atención por meetup', 'Meetup sessions', 'Atendimento por meetup'),
     L('Sesiones de acompañamiento presenciales o en línea para tu equipo. Desde el plan Standard.',
       'In-person or online support sessions for your team. From the Standard plan on.',
       'Sessões de acompanhamento presenciais ou online para seu time. A partir do plano Standard.'),
     [N(), Y(), Y(), Y()]),
]


# ───────────────────────── FAQ ─────────────────────────
FAQ = [
    (L('¿Qué es una "automatización en paralelo"?',
       'What is an "automation running in parallel"?',
       'O que é uma "automação em paralelo"?'),
     L('Es una automatización ejecutándose al mismo tiempo que otras. El número de tu plan indica cuántas pueden correr simultáneamente. No pagas por robot ni por usuario: pagas por cada automatización en operación.',
       'It is one automation running at the same time as others. Your plan’s number tells you how many can run simultaneously. You do not pay per robot or per user: you pay for each automation in operation.',
       'É uma automação rodando ao mesmo tempo que outras. O número do seu plano indica quantas podem rodar simultaneamente. Você não paga por robô nem por usuário: paga por cada automação em operação.')),
    (L('¿Todos los planes incluyen la suite completa?',
       'Do all plans include the full suite?',
       'Todos os planos incluem a suíte completa?'),
     L('Sí. RPA Studio, Saturn Studio, Orquestador (con Xperience), AI Studio y Nexus vienen incluidos en todos los planes. Lo que cambia entre planes es la capacidad de ejecución, los límites de usuarios y las características de seguridad y soporte.',
       'Yes. RPA Studio, Saturn Studio, Orchestrator (with Xperience), AI Studio and Nexus are included in every plan. What changes between plans is execution capacity, user limits and the security and support features.',
       'Sim. RPA Studio, Saturn Studio, Orquestrador (com Xperience), AI Studio e Nexus vêm incluídos em todos os planos. O que muda entre os planos é a capacidade de execução, os limites de usuários e os recursos de segurança e suporte.')),
    (L('¿Qué son los créditos de AI Studio?',
       'What are AI Studio credits?',
       'O que são os créditos de AI Studio?'),
     L('Son el volumen anual de procesamiento con inteligencia artificial incluido en tu plan: leer y entender documentos, correos, imágenes y audio. Los créditos no utilizados no se acumulan al ciclo siguiente.',
       'They are the annual volume of AI processing included in your plan: reading and understanding documents, email, images and audio. Unused credits do not roll over to the next cycle.',
       'São o volume anual de processamento com inteligência artificial incluído no seu plano: ler e entender documentos, e-mails, imagens e áudio. Os créditos não utilizados não se acumulam para o ciclo seguinte.')),
    (L('¿Puedo usar mi propio modelo de IA?',
       'Can I use my own AI model?',
       'Posso usar meu próprio modelo de IA?'),
     L('Sí, desde el plan Standard. Con Bring Your Own Model conectas tu proveedor de IA externo (por ejemplo Azure OpenAI o Amazon Bedrock) en AI Studio. Todos los planes incluyen además el modelo interno de AI Studio, que opera dentro del entorno Rocketbot.',
       'Yes, from the Standard plan on. With Bring Your Own Model you connect your external AI provider (Azure OpenAI or Amazon Bedrock, for example) in AI Studio. Every plan also includes the internal AI Studio model, which runs inside the Rocketbot environment.',
       'Sim, a partir do plano Standard. Com o Bring Your Own Model você conecta seu provedor de IA externo (por exemplo Azure OpenAI ou Amazon Bedrock) no AI Studio. Todos os planos incluem ainda o modelo interno do AI Studio, que opera dentro do ambiente Rocketbot.')),
    (L('¿Puedo agregar más usuarios?',
       'Can I add more users?',
       'Posso adicionar mais usuários?'),
     L('Sí. Los planes incluyen add-ons de usuarios finales y usuarios creadores adicionales. El plan Corporate incluye usuarios ilimitados sin necesidad de add-ons.',
       'Yes. Plans include add-ons for additional end users and builder users. The Corporate plan includes unlimited users with no add-ons needed.',
       'Sim. Os planos incluem add-ons de usuários finais e usuários criadores adicionais. O plano Corporate inclui usuários ilimitados sem necessidade de add-ons.')),
    (L('¿Qué cubre el soporte?',
       'What does support cover?',
       'O que o suporte cobre?'),
     L('Todos los planes se atienden por un canal de Slack dedicado en horario hábil (5×8), con tiempos de primera respuesta que van desde 60 hasta 15 minutos según el plan. La atención por evento 7×24 está disponible en todos los planes con costo adicional.',
       'Every plan is served through a dedicated Slack channel during business hours (5×8), with first-response times ranging from 60 down to 15 minutes depending on the plan. 24/7 per-event coverage is available in every plan at an additional cost.',
       'Todos os planos são atendidos por um canal de Slack dedicado em horário comercial (5×8), com tempos de primeira resposta que vão de 60 a 15 minutos conforme o plano. O atendimento por evento 7×24 está disponível em todos os planos com custo adicional.')),
]


# ───────────────────────── textos sueltos ─────────────────────────
COPY = {
    'title': L('Planes y precios | Rocketbot', 'Plans and pricing | Rocketbot', 'Planos e preços | Rocketbot'),
    'desc': L('Todos los planes de la Suite Rocketbot en detalle: capacidad, límites por producto, seguridad y soporte. Compara Entry, Standard, Enterprise y Corporate.',
              'Every Rocketbot Suite plan in detail: capacity, per-product limits, security and support. Compare Entry, Standard, Enterprise and Corporate.',
              'Todos os planos da Suíte Rocketbot em detalhe: capacidade, limites por produto, segurança e suporte. Compare Entry, Standard, Enterprise e Corporate.'),
    'og_desc': L('Capacidad, límites producto por producto, seguridad y soporte. Los cuatro planes de la Suite Rocketbot, comparados en detalle.',
                 'Capacity, product-by-product limits, security and support. The four Rocketbot Suite plans, compared in detail.',
                 'Capacidade, limites produto a produto, segurança e suporte. Os quatro planos da Suíte Rocketbot, comparados em detalhe.'),
    'eyebrow': L('Planes y precios', 'Plans and pricing', 'Planos e preços'),
    'h1_a': L('Automatización que crece', 'Automation that grows', 'Automação que cresce'),
    'h1_b': L('con tu operación', 'with your operations', 'com a sua operação'),
    'hero_sub': L('Una sola suite — RPA, orquestación, IA y aplicaciones. Eliges la capacidad; todos los productos vienen incluidos en cada plan.',
                  'One single suite — RPA, orchestration, AI and applications. You choose the capacity; every product is included in every plan.',
                  'Uma única suíte — RPA, orquestração, IA e aplicativos. Você escolhe a capacidade; todos os produtos vêm incluídos em cada plano.'),
    'cta_sales': L('Hablar con ventas', 'Talk to sales', 'Falar com vendas'),
    'cta_compare': L('Comparar planes', 'Compare plans', 'Comparar planos'),
    'plans_t_a': L('Cuatro planes,', 'Four plans,', 'Quatro planos,'),
    'plans_t_b': L('una sola suite completa.', 'one complete suite.', 'uma suíte completa.'),
    'plans_sub': L('Lo que cambia de un plan a otro es la capacidad de ejecución, los límites de usuarios y las características de seguridad y&nbsp;soporte.',
                   'What changes from one plan to the next is execution capacity, user limits and the security and support&nbsp;features.',
                   'O que muda de um plano para outro é a capacidade de execução, os limites de usuários e os recursos de segurança e&nbsp;suporte.'),
    'suite_lb': L('Incluido en todos los planes', 'Included in every plan', 'Incluído em todos os planos'),
    'price_note': L('Precios en dólares estadounidenses (USD). Licencia anual. '
                    'Los valores no incluyen los impuestos aplicables en cada país.',
                    'Prices in US dollars (USD). Annual license. '
                    'Amounts do not include the taxes applicable in each country.',
                    'Preços em dólares americanos (US$). Licença anual. '
                    'Os valores não incluem os impostos aplicáveis em cada país.'),
    'tax_note': L('No incluye los impuestos de cada país',
                  'Does not include each country&#8217;s taxes',
                  'Não inclui os impostos de cada país'),
    'cur': L('USD', 'USD', 'US$'),
    'per': L('/año', '/year', '/ano'),
    'addons_lb': L('Add-ons', 'Add-ons', 'Add-ons'),
    # Las tarjetas dicen "Todo lo de X, mas": esta nota deja explicito, sin
    # depender del "?", que las cantidades son el total del plan.
    'inc_note': L('Las cantidades indicadas son el total que incluye este plan: '
                  'no se suman a las del plan anterior.',
                  'The amounts shown are the total included in this plan: '
                  'they are not added to those of the previous plan.',
                  'As quantidades indicadas são o total incluído neste plano: '
                  'não se somam às do plano anterior.'),
    'cmp_t_a': L('Compara los planes', 'Compare the plans', 'Compare os planos'),
    'cmp_t_b': L('línea por línea.', 'line by line.', 'linha por linha.'),
    'cmp_sub': L('Todos los límites de la suite, producto por producto. Pasa el cursor sobre <span class="rb-info" aria-hidden="true">i</span> para ver el detalle de cada&nbsp;característica.',
                 'Every limit in the suite, product by product. Hover over <span class="rb-info" aria-hidden="true">i</span> to see the detail of each&nbsp;feature.',
                 'Todos os limites da suíte, produto a produto. Passe o cursor sobre <span class="rb-info" aria-hidden="true">i</span> para ver o detalhe de cada&nbsp;recurso.'),
    'faq_t': L('Preguntas frecuentes', 'Frequently asked questions', 'Perguntas frequentes'),
    'final_t': L('¿No sabes qué plan necesitas?', 'Not sure which plan you need?',
                 'Não sabe de qual plano precisa?'),
    'final_sub': L('Cuéntanos cuántos procesos quieres automatizar y te recomendamos el plan exacto — sin compromiso.',
                   'Tell us how many processes you want to automate and we will recommend the exact plan — no strings attached.',
                   'Conte quantos processos você quer automatizar e recomendamos o plano exato — sem compromisso.'),
    'final_cta': L('Agendar una llamada', 'Book a call', 'Agendar uma chamada'),
    'info_aria': L('Ver detalle', 'See detail', 'Ver detalhe'),
}

SUITE_PRODUCTS = [
    ('rpa-studio.png', L('RPA Studio', 'RPA Studio', 'RPA Studio')),
    ('saturn-studio.png', L('Saturn Studio', 'Saturn Studio', 'Saturn Studio')),
    ('orchestrator.png', L('Orquestador', 'Orchestrator', 'Orquestrador')),
    ('xperience.png', L('Xperience', 'Xperience', 'Xperience')),
    ('ai-studio.png', L('AI Studio', 'AI Studio', 'AI Studio')),
    ('nexus.png', L('Nexus', 'Nexus', 'Nexus')),
]


# ───────────────────────── render ─────────────────────────
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def render_cell(cell, lang, is_std):
    kind, val = cell
    cls = ['is-std'] if is_std else []
    if kind == 'y':
        cls.append('yes')
        body = '✓'
    elif kind == 'n':
        cls.append('no')
        body = '—'
    else:
        if kind == 'b':
            cls.append('best')
        body = tr(val, lang)
    attr = ' class="%s"' % ' '.join(cls) if cls else ''
    return '<td%s>%s</td>' % (attr, body)


def render_table(lang):
    out = []
    out.append('        <thead>')
    out.append('          <tr>')
    out.append('            <th></th>')
    out.append('            <th>Entry</th>')
    out.append('            <th class="is-std">Standard</th>')
    out.append('            <th>Enterprise</th>')
    out.append('            <th class="is-corp">Corporate</th>')
    out.append('          </tr>')
    out.append('        </thead>')
    out.append('        <tbody>')
    rows = [r for r in ROWS]
    for i, row in enumerate(rows):
        last = ' class="is-last"' if i == len(rows) - 1 else ''
        if row[0] == 'grp':
            # la celda is-std es la 3ra columna (Standard), no la 2da (Entry):
            # asi el borde rojo de la columna no da un salto en cada banda
            out.append('          <tr class="rb-ptbl__grp"><td>%s</td><td></td><td class="is-std"></td><td></td><td></td></tr>'
                       % esc(tr(row[1], lang)))
            continue
        _, label, tip, cells = row
        info = ('<span class="rb-info" tabindex="0" role="button" aria-label="%s">i'
                '<span class="rb-info__pop">%s</span></span>') % (esc(tr(COPY['info_aria'], lang)), esc(tr(tip, lang)))
        tds = ''.join(render_cell(c, lang, j == 1) for j, c in enumerate(cells))
        out.append('          <tr%s><td>%s%s</td>%s</tr>' % (last, esc(tr(label, lang)), info, tds))
    out.append('        </tbody>')
    return '\n'.join(out)


def render_cards(lang):
    out = []
    for i, p in enumerate(PLANS):
        cls = 'rb-pcard rb-pcard--feat' if p['feat'] else 'rb-pcard'
        out.append('      <article class="%s">' % cls)
        if p['feat']:
            out.append('        <span class="rb-pcard__badge">%s</span>'
                       % esc(tr(L('Más elegido', 'Most chosen', 'Mais escolhido'), lang)))
        out.append('        <div class="rb-pcard__num">0%d &middot; %s</div>' % (i + 1, p['name']))
        out.append('        <h3>%s</h3>' % p['name'])
        out.append('        <p class="rb-pcard__aud">%s</p>' % esc(tr(p['aud'], lang)))
        out.append('        <div class="rb-pcard__price"><span class="cur">%s</span>%s<span class="per">%s</span></div>'
                   % (tr(COPY['cur'], lang), tr(p['price'], lang), tr(COPY['per'], lang)))
        out.append('        <div class="rb-pcard__tax">%s</div>' % tr(COPY['tax_note'], lang))
        out.append('        <div class="rb-pcard__cap">%s</div>' % esc(tr(p['cap'], lang)))
        btn = 'rb-btn--primary' if p['feat'] else 'rb-btn--ghost'
        out.append('        <a class="rb-btn %s" href="contacto.html">%s</a>' % (btn, esc(tr(COPY['cta_sales'], lang))))
        out.append('        <div class="rb-pcard__lb">%s</div>' % esc(tr(p['inc_lb'], lang)))
        out.append('        <ul class="rb-pcard__inc">')
        for it in p['inc']:
            if isinstance(it, tuple):
                text, tip = it
                out.append('          <li>%s<span class="rb-info" tabindex="0" role="button" '
                           'aria-label="%s">?<span class="rb-info__pop">%s</span></span></li>'
                           % (esc(tr(text, lang)), esc(tr(COPY['info_aria'], lang)),
                              esc(tr(tip, lang))))
            else:
                out.append('          <li>%s</li>' % esc(tr(it, lang)))
        out.append('        </ul>')
        out.append('        <p class="rb-pcard__note">%s</p>' % esc(tr(COPY['inc_note'], lang)))
        out.append('        <div class="rb-pcard__addons">')
        out.append('          <div class="rb-pcard__lb">%s</div>' % esc(tr(COPY['addons_lb'], lang)))
        out.append('          <ul>')
        for it in p['addons']:
            out.append('            <li>%s</li>' % tr(it, lang))  # trae <b> intencional
        out.append('          </ul>')
        out.append('        </div>')
        out.append('      </article>')
    return '\n'.join(out)


def render_faq(lang):
    out = []
    for q, a in FAQ:
        out.append('      <details>')
        out.append('        <summary>%s</summary>' % esc(tr(q, lang)))
        out.append('        <div class="rb-faq__body">%s</div>' % esc(tr(a, lang)))
        out.append('      </details>')
    return '\n'.join(out)


def render_body(lang):
    A = lambda k: tr(COPY[k], lang)
    pre = '' if lang == 'es' else '/'
    suite = '\n'.join(
        '        <span class="rb-suiteband__it"><img src="%sassets/logos/products/%s" alt="" loading="lazy" decoding="async">%s</span>'
        % (pre, f, tr(n, lang)) for f, n in SUITE_PRODUCTS)
    return """<!-- HERO -->
<section class="rb-hero">
  <div class="rb-hero__particles"></div>
  <div class="container">
    <div class="rb-hero__content">
      <span class="rb-eyebrow rb-eyebrow--light"><span class="dot"></span>{eyebrow}</span>
      <h1 class="rb-hero__title">{h1a}<br><span style="color:var(--rb-red);">{h1b}</span></h1>
      <p class="rb-hero__sub">{hero_sub}</p>
      <div class="rb-hero__ctas">
        <a class="rb-btn rb-btn--primary rb-btn--lg" href="contacto.html">{cta_sales}</a>
        <a class="rb-btn rb-btn--ghost rb-btn--lg" href="#comparar" style="color:#fff;border-color:rgba(255,255,255,.25);">{cta_compare}</a>
      </div>
    </div>
  </div>
</section>

<!-- PLANES -->
<section class="rb-section rb-section--alt" id="planes">
  <div class="container">
    <div class="rb-section__head">
      <h2 class="rb-section__title">{plans_ta}<br><span>{plans_tb}</span></h2>
      <p class="rb-section__sub">{plans_sub}</p>
    </div>
    <div class="rb-suiteband">
      <span class="rb-suiteband__lb">&#10003; {suite_lb}</span>
      <div class="rb-suiteband__list">
{suite}
      </div>
    </div>
    <div class="rb-pcards">
{cards}
    </div>
    <p class="rb-price-note">{price_note}</p>
  </div>
</section>

<!-- COMPARATIVA -->
<section class="rb-section" id="comparar">
  <div class="container">
    <div class="rb-section__head">
      <h2 class="rb-section__title">{cmp_ta}<br><span>{cmp_tb}</span></h2>
      <p class="rb-section__sub">{cmp_sub}</p>
    </div>
    <div class="rb-ptbl-wrap">
      <table class="rb-ptbl">
{table}
      </table>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="rb-section rb-section--alt" id="faq">
  <div class="container">
    <div class="rb-section__head"><h2 class="rb-section__title">{faq_t}</h2></div>
    <div class="rb-faq">
{faq}
    </div>
  </div>
</section>

<!-- FINAL -->
<section class="rb-cta-band" id="contacto">
  <div class="container">
    <div class="rb-cta-band__inner">
      <div>
        <h2 class="rb-cta-band__title">{final_t}</h2>
        <p class="rb-cta-band__sub">{final_sub}</p>
      </div>
      <a class="rb-btn rb-btn--white rb-btn--lg" href="contacto.html">{final_cta}</a>
    </div>
  </div>
</section>

""".format(eyebrow=A('eyebrow'), h1a=A('h1_a'), h1b=A('h1_b'), hero_sub=A('hero_sub'),
           cta_sales=A('cta_sales'), cta_compare=A('cta_compare'),
           plans_ta=A('plans_t_a'), plans_tb=A('plans_t_b'), plans_sub=A('plans_sub'),
           suite_lb=A('suite_lb'), suite=suite, cards=render_cards(lang), price_note=A('price_note'),
           cmp_ta=A('cmp_t_a'), cmp_tb=A('cmp_t_b'), cmp_sub=A('cmp_sub'), table=render_table(lang),
           faq_t=A('faq_t'), faq=render_faq(lang),
           final_t=A('final_t'), final_sub=A('final_sub'), final_cta=A('final_cta'))


# ───────────────────────── ensamblado ─────────────────────────
def build(lang, css_extra):
    # 1) el head/nav/footer/scripts salen del esqueleto en el idioma que toca
    base = BASE if lang == 'es' else os.path.join(ROOT, lang, 'construir-vs-comprar.html')
    src = io.open(base, encoding='utf-8').read()

    # 2) CSS propio de esta pagina, antes del cierre del <style> que la
    # precede. El esqueleto tiene 3 bloques <style> distintos antes de
    # </head> (el grande, uno chico "rb-ddnav-css" y uno chico y propio
    # "rb-lang-temp-hide" que cierra en su misma linea). Hay que insertar
    # el CSS de planes DENTRO de un bloque <style> real: ancla al cierre
    # que esta justo antes de <style id="rb-lang-temp-hide">, no al literal
    # "</style>\n</head>" (eso matchea el cierre de rb-lang-temp-hide y deja
    # el CSS de planes suelto, fuera de cualquier <style>, entre dos tags).
    anchor = '</style>\n<style id="rb-lang-temp-hide">'
    if anchor in src:
        src = src.replace(anchor, css_extra + '\n' + anchor, 1)
    else:
        src = src.replace('</style>\n</head>', css_extra + '\n</style>\n</head>', 1)

    # 3) contenido: de <!-- HERO --> hasta el footer
    i = src.index('<!-- HERO -->')
    j = src.index('<footer class="rb-footer">')
    src = src[:i] + render_body(lang) + src[j:]

    # 4) fuera el JS y el JSON-LD especificos de construir-vs-comprar
    i = src.index('<!-- PAGE-SPECIFIC INTERACTIVE -->')
    j = src.index('<script type="application/ld+json">')
    src = src[:i] + src[j:]
    i = src.index('<script type="application/ld+json">')
    j = src.index('</script>', i) + len('</script>')
    ld = ('<script type="application/ld+json">\n{\n'
          '  "@context": "https://schema.org",\n'
          '  "@type": "WebPage",\n'
          '  "name": "%s",\n'
          '  "url": "%s",\n'
          '  "description": "%s",\n'
          '  "provider": { "@type": "Organization", "name": "Rocketbot", "url": "https://rocketbot.com" }\n'
          '}\n</script>') % (tr(COPY['eyebrow'], lang), canonical(lang), tr(COPY['og_desc'], lang))
    src = src[:i] + ld + src[j:]

    # 5) head: titulo, descripcion, canonicas y social
    src = re.sub(r'<title>.*?</title>', '<title>%s</title>' % tr(COPY['title'], lang), src, count=1, flags=re.S)
    src = re.sub(r'<meta name="description" content=".*?">',
                 '<meta name="description" content="%s">' % tr(COPY['desc'], lang), src, count=1, flags=re.S)
    src = src.replace('https://rocketbot.com/construir-vs-comprar', 'https://rocketbot.com/planes')
    src = src.replace('https://rocketbot.com/en/construir-vs-comprar', 'https://rocketbot.com/en/planes')
    src = src.replace('https://rocketbot.com/pt/construir-vs-comprar', 'https://rocketbot.com/pt/planes')
    for prop in ('og:title', 'twitter:title'):
        src = re.sub(r'(<meta (?:property|name)="%s" content=").*?(">)' % prop,
                     lambda m: m.group(1) + tr(COPY['title'], lang) + m.group(2), src, count=1, flags=re.S)
    for prop in ('og:description', 'twitter:description'):
        src = re.sub(r'(<meta (?:property|name)="%s" content=").*?(">)' % prop,
                     lambda m: m.group(1) + tr(COPY['og_desc'], lang) + m.group(2), src, count=1, flags=re.S)
    src = re.sub(r"PAGE='construir-vs-comprar\.html'", "PAGE='planes.html'", src)

    # 6) el esqueleto ya trae el boton "Planes" del header (patch_planes_nav.py):
    #    aca es la pagina actual, y el CTA del header vuelve al de descarga
    src = src.replace('<a href="planes.html" class="rb-nav__plans-hdr">',
                      '<a href="planes.html" class="rb-nav__plans-hdr" aria-current="page">', 1)
    src = re.sub(r'<a href="contacto\.html" class="rb-btn rb-btn--primary">[^<]*</a>(\s*</div>\s*</div>\s*</nav>)',
                 lambda m: '<button type="button" class="rb-btn rb-btn--primary" data-dl-open>%s</button>%s'
                           % ({'es': 'Descarga', 'en': 'Download', 'pt': 'Download'}[lang], m.group(1)),
                 src, count=1)

    return src


def canonical(lang):
    return 'https://rocketbot.com/planes' if lang == 'es' else 'https://rocketbot.com/%s/planes' % lang


def main():
    css_extra = io.open(os.path.join(ROOT, 'planes.build.css'), encoding='utf-8').read()
    for lang in LANGS:
        out = build(lang, css_extra)
        path = os.path.join(ROOT, 'planes.html') if lang == 'es' else os.path.join(ROOT, lang, 'planes.html')
        io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
        print('escrito %s (%d KB)' % (path, len(out) // 1024))


if __name__ == '__main__':
    main()
