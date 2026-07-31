# -*- coding: utf-8 -*-
"""
Genera faq.html (es/en/pt) a partir del shell de contacto.html (head + nav +
footer + scripts), igual que build_partners.py. Reemplaza el bloque central
por un listado de preguntas frecuentes agrupadas por tema, usando el
componente .rb-faq (details/summary) ya definido en el CSS compartido.

Idempotente: reescribe faq.html cada vez. Ejecutar y luego patch_support_nav.py
para enlazarlo desde el header/mobile/footer.

    python build_faq.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

FAQ_CSS = """
<style id="rb-faq-css">
.rb-faqpg{padding-top:72px;}
.rb-faqpg-hero{padding:76px 0 48px;text-align:center;}
.rb-faqpg-hero .container{max-width:760px;}
.rb-faqpg-hero__title{font-size:clamp(30px,4.4vw,48px);font-weight:900;letter-spacing:-.03em;margin:20px 0 14px;}
.rb-faqpg-hero__sub{font-size:17px;line-height:1.6;opacity:.75;}
.rb-faqpg-cat{padding:36px 0;}
.rb-faqpg-cat + .rb-faqpg-cat{border-top:1px solid var(--border);}
.rb-faqpg-cat__title{font-size:clamp(20px,2.4vw,26px);font-weight:800;letter-spacing:-.01em;margin-bottom:22px;color:var(--foreground);}
.rb-faqpg-cat__title span{color:var(--rb-red);}
.rb-faq{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:12px;}
.rb-faq details{background:var(--card);border:1px solid var(--border);border-radius:var(--r-md);overflow:hidden;transition:background .35s,border-color .3s;}
.rb-faq details[open]{border-color:rgba(188,0,23,.3);}
.rb-faq summary{padding:20px 24px;font-size:15px;font-weight:600;color:var(--foreground);cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;transition:color .2s;}
.rb-faq summary::-webkit-details-marker{display:none;}
.rb-faq summary::after{content:'+';font-size:20px;color:var(--rb-red);font-weight:700;flex-shrink:0;}
.rb-faq details[open] summary::after{content:'\2212';}
.rb-faq summary:hover{color:var(--rb-red);}
.rb-faq__body{padding:0 24px 20px;font-size:14px;color:#666;line-height:1.7;}
[data-theme="dark"] .rb-faq__body{color:rgba(255,255,255,.5);}
</style>
"""

CATS = [
 {
  'key':'general',
  'title':{'es':'Automatización de procesos','en':'Process automation','pt':'Automação de processos'},
  'items':[
   {'es':('¿Qué es la automatización de procesos?','La automatización de procesos consiste en utilizar software para ejecutar tareas repetitivas de forma automática. Permite reducir errores, ahorrar tiempo, aumentar la productividad y liberar a las personas para que se enfoquen en actividades de mayor valor para el negocio.'),
    'en':('What is process automation?','Process automation means using software to run repetitive tasks automatically. It reduces errors, saves time, increases productivity and frees people to focus on higher-value work for the business.'),
    'pt':('O que é automação de processos?','A automação de processos consiste em usar software para executar tarefas repetitivas de forma automática. Isso reduz erros, economiza tempo, aumenta a produtividade e libera as pessoas para se concentrarem em atividades de maior valor para o negócio.')},
   {'es':('¿Qué procesos se pueden automatizar?','Se pueden automatizar procesos repetitivos como el ingreso de datos, gestión de facturas, conciliaciones bancarias, atención al cliente, recursos humanos, compras, generación de reportes y cualquier tarea que siga reglas definidas o conecte varios sistemas.'),
    'en':('What processes can be automated?','Repetitive processes such as data entry, invoice management, bank reconciliation, customer service, HR, purchasing, report generation and any task that follows defined rules or connects several systems can be automated.'),
    'pt':('Quais processos podem ser automatizados?','Processos repetitivos como digitação de dados, gestão de faturas, conciliação bancária, atendimento ao cliente, recursos humanos, compras, geração de relatórios e qualquer tarefa que siga regras definidas ou conecte vários sistemas podem ser automatizados.')},
   {'es':('¿Cómo saber si un proceso se puede automatizar?','Si un proceso consume mucho tiempo, requiere copiar información entre sistemas, genera errores frecuentes o sigue siempre los mismos pasos, probablemente sea un buen candidato para automatización. Mientras más repetitivo y estructurado sea, mayor será el beneficio.'),
    'en':('How do I know if a process can be automated?','If a process takes a lot of time, requires copying information between systems, generates frequent errors or always follows the same steps, it is likely a good candidate for automation. The more repetitive and structured it is, the greater the benefit.'),
    'pt':('Como saber se um processo pode ser automatizado?','Se um processo consome muito tempo, exige copiar informações entre sistemas, gera erros frequentes ou segue sempre os mesmos passos, provavelmente é um bom candidato para automação. Quanto mais repetitivo e estruturado for, maior será o benefício.')},
   {'es':('¿Cuáles son los beneficios de automatizar procesos?','Automatizar procesos ayuda a reducir tiempos de ejecución, disminuir errores manuales, mejorar la productividad, aumentar la trazabilidad y ofrecer una mejor experiencia tanto para los equipos como para los clientes.'),
    'en':('What are the benefits of automating processes?','Automating processes helps reduce execution times, decrease manual errors, improve productivity, increase traceability and deliver a better experience for both teams and customers.'),
    'pt':('Quais são os benefícios de automatizar processos?','Automatizar processos ajuda a reduzir tempos de execução, diminuir erros manuais, melhorar a produtividade, aumentar a rastreabilidade e oferecer uma experiência melhor tanto para as equipes quanto para os clientes.')},
  ],
 },
 {
  'key':'rpa-ia',
  'title':{'es':'RPA e Inteligencia Artificial','en':'RPA and Artificial Intelligence','pt':'RPA e Inteligência Artificial'},
  'items':[
   {'es':('¿Qué es RPA?','RPA (Robotic Process Automation) es una tecnología que utiliza robots de software para ejecutar tareas repetitivas entre aplicaciones y sistemas, igual que lo haría una persona, pero de forma más rápida, precisa y consistente.'),
    'en':('What is RPA?','RPA (Robotic Process Automation) is a technology that uses software robots to run repetitive tasks across applications and systems, just as a person would, but faster, more accurately and more consistently.'),
    'pt':('O que é RPA?','RPA (Robotic Process Automation) é uma tecnologia que utiliza robôs de software para executar tarefas repetitivas entre aplicações e sistemas, da mesma forma que uma pessoa faria, mas de forma mais rápida, precisa e consistente.')},
   {'es':('¿Cuál es la diferencia entre RPA e inteligencia artificial?','RPA sigue reglas para ejecutar tareas repetitivas. La inteligencia artificial interpreta información, reconoce patrones y ayuda a tomar decisiones. Cuando ambas trabajan juntas, es posible automatizar procesos mucho más complejos.'),
    'en':('What is the difference between RPA and artificial intelligence?','RPA follows rules to execute repetitive tasks. Artificial intelligence interprets information, recognizes patterns and helps make decisions. When both work together, it is possible to automate much more complex processes.'),
    'pt':('Qual é a diferença entre RPA e inteligência artificial?','O RPA segue regras para executar tarefas repetitivas. A inteligência artificial interpreta informações, reconhece padrões e ajuda a tomar decisões. Quando as duas trabalham juntas, é possível automatizar processos muito mais complexos.')},
   {'es':('¿Qué es un agente inteligente?','Un agente inteligente utiliza inteligencia artificial para analizar información, tomar decisiones y ejecutar acciones dentro de un proceso. Puede trabajar con documentos, correos, conversaciones y otros datos para apoyar o completar tareas de forma automática.'),
    'en':('What is an intelligent agent?','An intelligent agent uses artificial intelligence to analyze information, make decisions and execute actions within a process. It can work with documents, emails, conversations and other data to support or complete tasks automatically.'),
    'pt':('O que é um agente inteligente?','Um agente inteligente utiliza inteligência artificial para analisar informações, tomar decisões e executar ações dentro de um processo. Pode trabalhar com documentos, e-mails, conversas e outros dados para apoiar ou concluir tarefas de forma automática.')},
   {'es':('¿Cuándo conviene usar inteligencia artificial?','La inteligencia artificial aporta más valor cuando un proceso necesita interpretar documentos, analizar información, clasificar datos o ayudar en la toma de decisiones. Para tareas repetitivas y basadas en reglas, la automatización tradicional suele ser suficiente.'),
    'en':('When does it make sense to use artificial intelligence?','Artificial intelligence adds the most value when a process needs to interpret documents, analyze information, classify data or support decision-making. For repetitive, rule-based tasks, traditional automation is usually enough.'),
    'pt':('Quando vale a pena usar inteligência artificial?','A inteligência artificial traz mais valor quando um processo precisa interpretar documentos, analisar informações, classificar dados ou apoiar a tomada de decisões. Para tarefas repetitivas e baseadas em regras, a automação tradicional costuma ser suficiente.')},
  ],
 },
 {
  'key':'suite',
  'title':{'es':'Suite Rocketbot','en':'Rocketbot Suite','pt':'Suite Rocketbot'},
  'items':[
   {'es':('¿Qué es una plataforma de automatización empresarial?','Es una plataforma que reúne herramientas para crear, ejecutar, administrar y monitorear automatizaciones desde un solo lugar. Además de automatizar tareas, permite integrar sistemas, controlar permisos, supervisar procesos y escalar la operación.'),
    'en':('What is an enterprise automation platform?','It is a platform that brings together tools to create, run, manage and monitor automations from a single place. Beyond automating tasks, it lets you integrate systems, control permissions, oversee processes and scale the operation.'),
    'pt':('O que é uma plataforma de automação empresarial?','É uma plataforma que reúne ferramentas para criar, executar, administrar e monitorar automações em um único lugar. Além de automatizar tarefas, permite integrar sistemas, controlar permissões, supervisionar processos e escalar a operação.')},
   {'es':('¿Qué es la Suite Rocketbot?','La Suite Rocketbot es una plataforma de automatización empresarial que integra automatización de procesos, inteligencia artificial, agentes inteligentes, formularios, aplicaciones, gobierno y monitoreo para gestionar procesos de principio a fin.'),
    'en':('What is the Rocketbot Suite?','The Rocketbot Suite is an enterprise automation platform that integrates process automation, artificial intelligence, intelligent agents, forms, applications, governance and monitoring to manage processes end to end.'),
    'pt':('O que é a Suite Rocketbot?','A Suite Rocketbot é uma plataforma de automação empresarial que integra automação de processos, inteligência artificial, agentes inteligentes, formulários, aplicações, governança e monitoramento para gerenciar processos de ponta a ponta.')},
   {'es':('¿Qué productos incluye la Suite Rocketbot?','La Suite Rocketbot incluye RPA Studio, Saturn Studio, AI Studio, Xperience, Orquestador y Nexus. Cada producto cumple una función específica y juntos permiten automatizar, gestionar y escalar procesos empresariales.'),
    'en':('What products does the Rocketbot Suite include?','The Rocketbot Suite includes RPA Studio, Saturn Studio, AI Studio, Xperience, Orchestrator and Nexus. Each product serves a specific function, and together they let you automate, manage and scale business processes.'),
    'pt':('Quais produtos a Suite Rocketbot inclui?','A Suite Rocketbot inclui RPA Studio, Saturn Studio, AI Studio, Xperience, Orquestrador e Nexus. Cada produto cumpre uma função específica e, juntos, permitem automatizar, gerenciar e escalar processos empresariais.')},
   {'es':('¿La Suite Rocketbot funciona con Claude?','Sí. Claude puede utilizarse dentro de la Suite Rocketbot para crear automatizaciones, aplicaciones y formularios mediante lenguaje natural, mientras la plataforma aporta integración, gobierno, monitoreo y trazabilidad.'),
    'en':('Does the Rocketbot Suite work with Claude?','Yes. Claude can be used within the Rocketbot Suite to create automations, applications and forms using natural language, while the platform provides integration, governance, monitoring and traceability.'),
    'pt':('A Suite Rocketbot funciona com o Claude?','Sim. O Claude pode ser utilizado dentro da Suite Rocketbot para criar automações, aplicações e formulários por meio de linguagem natural, enquanto a plataforma fornece integração, governança, monitoramento e rastreabilidade.')},
   {'es':('¿La Suite Rocketbot funciona con otros modelos de IA?','Sí. La Suite Rocketbot es compatible con diferentes modelos de inteligencia artificial para que las organizaciones puedan elegir la tecnología que mejor se adapte a cada necesidad.'),
    'en':('Does the Rocketbot Suite work with other AI models?','Yes. The Rocketbot Suite is compatible with different artificial intelligence models so organizations can choose the technology that best fits each need.'),
    'pt':('A Suite Rocketbot funciona com outros modelos de IA?','Sim. A Suite Rocketbot é compatível com diferentes modelos de inteligência artificial para que as organizações possam escolher a tecnologia que melhor se adapta a cada necessidade.')},
   {'es':('¿Con qué sistemas se integra Rocketbot?','Rocketbot puede integrarse con ERPs, CRMs, bases de datos, APIs, aplicaciones web, sistemas de escritorio, servicios en la nube y muchas otras herramientas utilizadas por las empresas.'),
    'en':('What systems does Rocketbot integrate with?','Rocketbot can integrate with ERPs, CRMs, databases, APIs, web applications, desktop systems, cloud services and many other tools used by companies.'),
    'pt':('Com quais sistemas a Rocketbot se integra?','A Rocketbot pode se integrar a ERPs, CRMs, bancos de dados, APIs, aplicações web, sistemas desktop, serviços em nuvem e muitas outras ferramentas utilizadas pelas empresas.')},
   {'es':('¿Cómo protege Rocketbot la información?','La Suite Rocketbot incorpora control de acceso por roles, trazabilidad, monitoreo, auditoría y diferentes opciones de despliegue para ayudar a proteger la información y administrar de forma segura cada automatización.'),
    'en':('How does Rocketbot protect information?','The Rocketbot Suite includes role-based access control, traceability, monitoring, auditing and different deployment options to help protect information and securely manage every automation.'),
    'pt':('Como a Rocketbot protege as informações?','A Suite Rocketbot incorpora controle de acesso por papéis, rastreabilidade, monitoramento, auditoria e diferentes opções de implantação para ajudar a proteger as informações e administrar cada automação com segurança.')},
  ],
 },
 {
  'key':'impl',
  'title':{'es':'Implementación','en':'Implementation','pt':'Implementação'},
  'items':[
   {'es':('¿Necesito saber programar para automatizar procesos?','No. Muchas automatizaciones pueden crearse mediante herramientas visuales y asistentes con inteligencia artificial. Cuando un proyecto requiere desarrollos más avanzados, la plataforma también permite extender sus capacidades.'),
    'en':('Do I need to know how to code to automate processes?','No. Many automations can be built using visual tools and AI-powered assistants. When a project requires more advanced development, the platform also lets you extend its capabilities.'),
    'pt':('Preciso saber programar para automatizar processos?','Não. Muitas automações podem ser criadas por meio de ferramentas visuais e assistentes com inteligência artificial. Quando um projeto exige desenvolvimentos mais avançados, a plataforma também permite estender suas capacidades.')},
   {'es':('¿Es más barato construir una solución con Python y Claude?','Depende del proyecto. Para automatizaciones pequeñas puede ser una buena alternativa. Sin embargo, cuando la operación crece, una plataforma ayuda a reducir el esfuerzo de integración, monitoreo, mantenimiento y escalabilidad.'),
    'en':('Is it cheaper to build a solution with Python and Claude?','It depends on the project. For small automations it can be a good option. However, as the operation grows, a platform helps reduce the effort of integration, monitoring, maintenance and scalability.'),
    'pt':('É mais barato construir uma solução com Python e Claude?','Depende do projeto. Para automações pequenas, pode ser uma boa alternativa. No entanto, à medida que a operação cresce, uma plataforma ajuda a reduzir o esforço de integração, monitoramento, manutenção e escalabilidade.')},
   {'es':('¿Qué diferencia hay entre construir una solución y usar una plataforma?','Construir una solución implica desarrollar y mantener cada componente. Una plataforma ya incorpora capacidades como integraciones, monitoreo, seguridad, permisos y trazabilidad, lo que acelera la implementación y simplifica la operación.'),
    'en':('What is the difference between building a solution and using a platform?','Building a solution means developing and maintaining every component yourself. A platform already includes capabilities such as integrations, monitoring, security, permissions and traceability, which speeds up implementation and simplifies operation.'),
    'pt':('Qual é a diferença entre construir uma solução e usar uma plataforma?','Construir uma solução significa desenvolver e manter cada componente. Uma plataforma já incorpora capacidades como integrações, monitoramento, segurança, permissões e rastreabilidade, o que acelera a implementação e simplifica a operação.')},
   {'es':('¿Cómo elegir el primer proceso para automatizar?','Lo ideal es comenzar con un proceso repetitivo, de alto volumen y con un impacto claro en tiempo, costos o calidad. Ese tipo de procesos suele ofrecer resultados rápidos y facilita demostrar el valor de la automatización.'),
    'en':('How do I choose the first process to automate?','It is best to start with a repetitive, high-volume process with a clear impact on time, cost or quality. This type of process tends to deliver quick results and makes it easier to demonstrate the value of automation.'),
    'pt':('Como escolher o primeiro processo para automatizar?','O ideal é começar com um processo repetitivo, de alto volume e com impacto claro em tempo, custos ou qualidade. Esse tipo de processo costuma trazer resultados rápidos e facilita demonstrar o valor da automação.')},
   {'es':('¿Puede una empresa empezar con un piloto?','Sí. Muchas organizaciones comienzan automatizando uno o dos procesos para medir resultados y, una vez validado el retorno, amplían la automatización a otras áreas del negocio.'),
    'en':('Can a company start with a pilot?','Yes. Many organizations start by automating one or two processes to measure results, and once the return is validated, they expand automation to other areas of the business.'),
    'pt':('Uma empresa pode começar com um piloto?','Sim. Muitas organizações começam automatizando um ou dois processos para medir resultados e, depois de validar o retorno, ampliam a automação para outras áreas do negócio.')},
  ],
 },
]

T = {
 'es': {
  'title': 'Preguntas frecuentes | Rocketbot',
  'desc': 'Resolvemos las dudas más comunes sobre automatización de procesos, RPA, inteligencia artificial y la Suite Rocketbot.',
  'eyebrow': 'Ayuda',
  'h1': 'Preguntas frecuentes',
  'sub': 'Todo lo que necesitas saber sobre automatización, RPA, inteligencia artificial y la Suite Rocketbot.',
 },
 'en': {
  'title': 'Frequently Asked Questions | Rocketbot',
  'desc': 'We answer the most common questions about process automation, RPA, artificial intelligence and the Rocketbot Suite.',
  'eyebrow': 'Help',
  'h1': 'Frequently asked questions',
  'sub': 'Everything you need to know about automation, RPA, artificial intelligence and the Rocketbot Suite.',
 },
 'pt': {
  'title': 'Perguntas frequentes | Rocketbot',
  'desc': 'Respondemos as dúvidas mais comuns sobre automação de processos, RPA, inteligência artificial e a Suite Rocketbot.',
  'eyebrow': 'Ajuda',
  'h1': 'Perguntas frequentes',
  'sub': 'Tudo o que você precisa saber sobre automação, RPA, inteligência artificial e a Suite Rocketbot.',
 },
}


def build_main(lang, t):
    cats_html = []
    for cat in CATS:
        items_html = []
        for it in cat['items']:
            q, a = it[lang]
            items_html.append(
                '        <details><summary>%s</summary><div class="rb-faq__body">%s</div></details>' % (q, a))
        cats_html.append(
            '    <div class="container">\n      <h2 class="rb-faqpg-cat__title">%s</h2>\n      <div class="rb-faq">\n%s\n      </div>\n    </div>'
            % (cat['title'][lang], '\n'.join(items_html)))
    cats_block = '\n  </section>\n  <section class="rb-faqpg-cat">\n'.join(cats_html)

    return """<!-- CONTACT PAGE -->
<!-- ======================= FAQ ======================= -->
<main class="rb-faqpg">

  <section class="rb-faqpg-hero">
    <div class="container">
      <span class="rb-eyebrow"><span class="dot"></span>{eyebrow}</span>
      <h1 class="rb-faqpg-hero__title">{h1}</h1>
      <p class="rb-faqpg-hero__sub">{sub}</p>
    </div>
  </section>

  <section class="rb-faqpg-cat">
{cats_block}
  </section>

</main>

<!-- FOOTER -->""".format(eyebrow=t['eyebrow'], h1=t['h1'], sub=t['sub'], cats_block=cats_block)


SECTION_RE = re.compile(r'<!-- CONTACT PAGE -->.*?<!-- FOOTER -->', re.S)
TITLE_RE = re.compile(r'<title>.*?</title>', re.S)


def sub_attr(src, prop, value):
    pat = re.compile(r'(<meta (?:name|property)="' + re.escape(prop) + r'" content=")[^"]*(">)')
    return pat.sub(lambda m: m.group(1) + value + m.group(2), src)


def build(lang, folder):
    src = io.open(os.path.join(folder, 'contacto.html'), encoding='utf-8').read()
    t = T[lang]

    src = SECTION_RE.sub(lambda m: build_main(lang, t), src, count=1)

    src = TITLE_RE.sub('<title>' + t['title'] + '</title>', src, count=1)
    src = sub_attr(src, 'description', t['desc'])
    src = sub_attr(src, 'og:title', t['title'])
    src = sub_attr(src, 'og:description', t['desc'])
    src = sub_attr(src, 'twitter:title', t['title'])
    src = sub_attr(src, 'twitter:description', t['desc'])

    src = src.replace('content="noindex, follow"', 'content="index, follow"')

    src = src.replace('rocketbot.com/contacto"', 'rocketbot.com/faq"')
    src = src.replace('rocketbot.com/en/contacto"', 'rocketbot.com/en/faq"')
    src = src.replace('rocketbot.com/pt/contacto"', 'rocketbot.com/pt/faq"')

    src = src.replace('"@type": "ContactPage"', '"@type": "FAQPage"')

    src = src.replace("PAGE='contacto.html'", "PAGE='faq.html'")

    if 'rb-faq-css' not in src:
        src = src.replace('</head>', FAQ_CSS + '</head>', 1)

    out = os.path.join(folder, 'faq.html')
    io.open(out, 'w', encoding='utf-8', newline='\n').write(src)
    print('  escrito %s/faq.html' % lang)


def main():
    for lang, folder in (('es', ROOT), ('en', os.path.join(ROOT, 'en')), ('pt', os.path.join(ROOT, 'pt'))):
        build(lang, folder)
    print('listo.')


if __name__ == '__main__':
    main()
