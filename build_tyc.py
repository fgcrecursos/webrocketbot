# -*- coding: utf-8 -*-
"""
Genera terminos-y-condiciones.html (es/en/pt): una sola pagina con selector
de producto (Suite, RPA Studio, Saturn Studio, Orquestador, AI Studio, Nexus),
igual patron de tabs que el selector de industrias de index.html
(.rb-ind-tab / .rb-ind-panel), renombrado rb-tyc- para no chocar con el CSS
de otras paginas.

Contenido basado en los 6 documentos "Terminos y Condiciones Tecnicas" en
C:\\Users\\frani\\Downloads\\files (2)\\ (Suite, RPA Studio, Saturn Studio,
Orquestador, AI Studio, Nexus). La version en espanol es la oficial; en/pt
son traduccion de referencia (asi lo indican los propios documentos fuente).

    python build_tyc.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

TYC_CSS = """
<style id="rb-tyc-css">
.rb-tycpg{padding-top:72px;}
.rb-tycpg-hero{padding:72px 0 32px;text-align:center;}
.rb-tycpg-hero .container{max-width:780px;}
.rb-tycpg-hero__title{font-size:clamp(28px,4vw,44px);font-weight:900;letter-spacing:-.03em;margin:20px 0 10px;}
.rb-tycpg-hero__sub{font-size:15.5px;line-height:1.6;opacity:.75;}
.rb-tyc-tabs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0 40px;}
.rb-tyc-tab{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:100px;border:1px solid var(--border);background:transparent;font-size:14px;font-weight:600;color:var(--foreground);cursor:pointer;transition:all .2s;white-space:nowrap;}
.rb-tyc-tab:hover{border-color:rgba(188,0,23,.35);color:var(--rb-red);}
.rb-tyc-tab.active{background:var(--rb-red);color:#fff;border-color:var(--rb-red);box-shadow:0 8px 24px rgba(188,0,23,.25);}
.rb-tyc-panel{display:none;}
.rb-tyc-panel.active{display:block;animation:rb-tycFade .3s ease;}
@keyframes rb-tycFade{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}
.rb-tyc-panel__head{max-width:820px;margin:0 auto 28px;padding-bottom:20px;border-bottom:1px solid var(--border);}
.rb-tyc-panel__eyebrow{font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--rb-red);}
.rb-tyc-panel__title{font-size:clamp(20px,2.6vw,28px);font-weight:800;margin:8px 0 6px;}
.rb-tyc-panel__meta{font-size:13px;opacity:.55;}
.rb-legal{max-width:820px;margin:0 auto;padding:0 0 40px;}
.rb-legal h2{font-size:clamp(18px,2.1vw,22px);font-weight:800;letter-spacing:-.01em;margin:38px 0 14px;color:var(--rb-red);}
.rb-legal h2:first-child{margin-top:0;}
.rb-legal h3{font-size:15.5px;font-weight:700;margin:22px 0 10px;color:var(--foreground);}
.rb-legal p{font-size:14.5px;line-height:1.75;color:var(--foreground);opacity:.82;margin:0 0 14px;}
.rb-legal ul{margin:0 0 14px;padding-left:22px;list-style:disc;}
.rb-legal li{font-size:14.5px;line-height:1.7;color:var(--foreground);opacity:.82;margin-bottom:7px;}
.rb-legal li::marker{color:var(--rb-red);}
.rb-legal strong{color:var(--foreground);opacity:1;}
.rb-legal-note{background:rgba(188,0,23,.06);border:1px solid rgba(188,0,23,.18);border-radius:12px;padding:14px 18px;font-size:13.5px;line-height:1.6;margin:0 0 20px;}
.rb-legal-table-wrap{overflow-x:auto;margin:0 0 20px;}
.rb-legal table{width:100%;min-width:520px;border-collapse:collapse;font-size:13px;}
.rb-legal table th,.rb-legal table td{padding:9px 12px;text-align:left;border-bottom:1px solid var(--border);white-space:nowrap;}
.rb-legal table th{background:rgba(0,0,0,.02);font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted,#888);}
[data-theme="dark"] .rb-legal table th{background:rgba(255,255,255,.03);}
.rb-legal table td:first-child,.rb-legal table th:first-child{white-space:normal;font-weight:600;}
@media(max-width:640px){.rb-tyc-tabs{gap:6px;}.rb-tyc-tab{font-size:12.5px;padding:8px 14px;}}
</style>
"""

TYC_JS = """
<script>
(function () {
  var tabs   = document.querySelectorAll('.rb-tyc-tab[data-tyc]');
  var panels = document.querySelectorAll('.rb-tyc-panel');
  function activate(key, updateHash) {
    var tab = document.querySelector('.rb-tyc-tab[data-tyc="' + key + '"]');
    var panel = document.getElementById('tyc-' + key);
    if (!tab || !panel) return false;
    tabs.forEach(function (t)   { t.classList.remove('active'); });
    panels.forEach(function (p) { p.classList.remove('active'); });
    tab.classList.add('active');
    panel.classList.add('active');
    if (updateHash) history.replaceState(null, '', '#' + key);
    return true;
  }
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      activate(tab.dataset.tyc, true);
    });
  });
  var initial = (location.hash || '').replace('#', '');
  if (initial) {
    var target = document.querySelector('.rb-tyc-tab[data-tyc="' + initial + '"]');
    if (target) {
      activate(initial, false);
      setTimeout(function () { target.scrollIntoView({block: 'start'}); }, 0);
    }
  }
})();
</script>
"""

# order + tab labels
PRODUCTS = ['suite', 'saturn', 'rpa', 'orquestador', 'ai', 'nexus']

TAB_LABEL = {
 'suite':       {'es':'Suite Rocketbot','en':'Rocketbot Suite','pt':'Suite Rocketbot'},
 'saturn':      {'es':'Saturn Studio','en':'Saturn Studio','pt':'Saturn Studio'},
 'rpa':         {'es':'RPA Studio','en':'RPA Studio','pt':'RPA Studio'},
 'orquestador': {'es':'Orquestador','en':'Orchestrator','pt':'Orquestrador'},
 'ai':          {'es':'AI Studio','en':'AI Studio','pt':'AI Studio'},
 'nexus':       {'es':'Nexus','en':'Nexus','pt':'Nexus'},
}
DOC_META = {
 'suite':       {'name':{'es':'Suite Rocketbot','en':'Rocketbot Suite','pt':'Suite Rocketbot'}, 'version':'1.0'},
 'saturn':      {'name':{'es':'Saturn Studio','en':'Saturn Studio','pt':'Saturn Studio'}, 'version':'4.0'},
 'rpa':         {'name':{'es':'RPA Studio','en':'RPA Studio','pt':'RPA Studio'}, 'version':'1.0'},
 'orquestador': {'name':{'es':'Rocketbot Orquestador','en':'Rocketbot Orchestrator','pt':'Rocketbot Orquestrador'}, 'version':'3.0'},
 'ai':          {'name':{'es':'AI Studio','en':'AI Studio','pt':'AI Studio'}, 'version':'2.0'},
 'nexus':       {'name':{'es':'Nexus','en':'Nexus','pt':'Nexus'}, 'version':'2.0'},
}

META = {
 'es': {'eyebrow':'Legal','title':'Términos y condiciones técnicas | Rocketbot','desc':'Términos y condiciones técnicas de la Suite Rocketbot y de cada producto: Saturn Studio, RPA Studio, Orquestador, AI Studio y Nexus.','h1':'Términos y condiciones técnicas','sub':'Capacidades, límites por plan y condiciones de uso de cada producto de la Suite Rocketbot. Selecciona un producto para ver su documento.'},
 'en': {'eyebrow':'Legal','title':'Technical Terms & Conditions | Rocketbot','desc':'Technical terms and conditions for the Rocketbot Suite and each product: Saturn Studio, RPA Studio, Orchestrator, AI Studio and Nexus.','h1':'Technical terms & conditions','sub':'Capabilities, plan limits and conditions of use for every product in the Rocketbot Suite. Select a product to view its document.'},
 'pt': {'eyebrow':'Legal','title':'Termos e condições técnicas | Rocketbot','desc':'Termos e condições técnicas da Suite Rocketbot e de cada produto: Saturn Studio, RPA Studio, Orquestrador, AI Studio e Nexus.','h1':'Termos e condições técnicas','sub':'Capacidades, limites por plano e condições de uso de cada produto da Suite Rocketbot. Selecione um produto para ver o documento.'},
}

LANG_NOTE = {
 'es': None,
 'en': "This is a reference translation for informational purposes. The Spanish-language version of each document is the official, legally binding text.",
 'pt': "Esta é uma tradução de referência, apenas para fins informativos. A versão em espanhol de cada documento é o texto oficial e juridicamente vinculante.",
}

def table(headers, rows):
    th = ''.join('<th>%s</th>' % h for h in headers)
    trs = ''
    for r in rows:
        trs += '<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>'
    return '<div class="rb-legal-table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs)

PLAN_COLS = ['', 'Entry 1', 'Standard', 'Enterprise', 'Corporate']

# ═══════════════════════════════════════════════════════════════════════
# CONTENT — one function per product returning {'es':html,'en':html,'pt':html}
# ═══════════════════════════════════════════════════════════════════════

def content_suite():
    plan_rows_es = [
        ['Procesos administrados (Orquestador)','5','20','50','1.000'],
        ['Procesos en ejecución paralela (Orquestador)','5','20','50','200'],
        ['Ejecuciones en paralelo (Saturn Studio)','5','20','50','200'],
        ['Licencias de desarrollo (RPA Studio)','2','3','5','Ilimitadas'],
        ['Créditos de AI Studio incluidos / año (sin rollover)','25M','50M','100M','250M'],
        ['Creators de Nexus incluidos','5','5','15','Ilimitados'],
        ['End Users de Nexus incluidos','10','25','50','Ilimitados'],
        ['Usuarios con login de Xperience','10','25','50','Ilimitados'],
        ['Robots registrables','Ilimitados','Ilimitados','Ilimitados','Ilimitados'],
    ]
    plan_rows_en = [
        ['Managed processes (Orchestrator)','5','20','50','1,000'],
        ['Parallel-running processes (Orchestrator)','5','20','50','200'],
        ['Parallel executions (Saturn Studio)','5','20','50','200'],
        ['Development licenses (RPA Studio)','2','3','5','Unlimited'],
        ['AI Studio credits included / year (no rollover)','25M','50M','100M','250M'],
        ['Nexus Creators included','5','5','15','Unlimited'],
        ['Nexus End Users included','10','25','50','Unlimited'],
        ['Xperience login users','10','25','50','Unlimited'],
        ['Registerable robots','Unlimited','Unlimited','Unlimited','Unlimited'],
    ]
    plan_rows_pt = [
        ['Processos administrados (Orquestrador)','5','20','50','1.000'],
        ['Processos em execução paralela (Orquestrador)','5','20','50','200'],
        ['Execuções em paralelo (Saturn Studio)','5','20','50','200'],
        ['Licenças de desenvolvimento (RPA Studio)','2','3','5','Ilimitadas'],
        ['Créditos de AI Studio incluídos / ano (sem rollover)','25M','50M','100M','250M'],
        ['Creators de Nexus incluídos','5','5','15','Ilimitados'],
        ['End Users de Nexus incluídos','10','25','50','Ilimitados'],
        ['Usuários com login do Xperience','10','25','50','Ilimitados'],
        ['Robôs registráveis','Ilimitados','Ilimitados','Ilimitados','Ilimitados'],
    ]
    support_rows = [
        ['Canal de soporte','Slack','Slack','Slack','Slack'],
        ['Horario de soporte','8×5','8×5','8×5','8×5'],
        ['Atención por evento 7×24','Costo adicional','Costo adicional','Costo adicional','Costo adicional'],
        ['Tiempo de primera respuesta (min)','60','45','30','15'],
        ['Customer Success Manager','Compartido','Compartido','Compartido','Dedicado'],
        ['Atención por meetup','No','Sí','Sí','Sí'],
    ]
    support_rows_en = [
        ['Support channel','Slack','Slack','Slack','Slack'],
        ['Support hours','8×5','8×5','8×5','8×5'],
        ['24/7 event coverage','Extra cost','Extra cost','Extra cost','Extra cost'],
        ['First-response time (min)','60','45','30','15'],
        ['Customer Success Manager','Shared','Shared','Shared','Dedicated'],
        ['Meetup support','No','Yes','Yes','Yes'],
    ]
    support_rows_pt = [
        ['Canal de suporte','Slack','Slack','Slack','Slack'],
        ['Horário de suporte','8×5','8×5','8×5','8×5'],
        ['Atendimento por evento 7×24','Custo adicional','Custo adicional','Custo adicional','Custo adicional'],
        ['Tempo de primeira resposta (min)','60','45','30','15'],
        ['Customer Success Manager','Compartilhado','Compartilhado','Compartilhado','Dedicado'],
        ['Atendimento por meetup','Não','Sim','Sim','Sim'],
    ]

    es = """
<h2>1. Objeto y alcance</h2>
<p>Este documento establece los términos y condiciones técnicas de la Suite Rocketbot ("la Suite"), conjunto integrado compuesto por RPA Studio, Saturn Studio, el Orquestador (incluido su módulo Xperience), AI Studio y Nexus. Define el modelo comercial por planes, las capacidades y límites transversales a todos los productos, y el orden de precedencia respecto de los T&C de cada producto.</p>
<p>Aplica a toda persona física o jurídica ("el Cliente") que adquiera y utilice la Suite en cualquiera de sus planes: Entry 1, Standard, Enterprise y Corporate. El alcance se limita a los aspectos técnicos; las condiciones comerciales, legales y de licenciamiento se rigen por el contrato de adquisición.</p>
<p>Es un documento técnico y descriptivo, no un contrato ni un SLA vinculante por sí mismo. En caso de discrepancia, el orden de precedencia es: (1) el contrato comercial; (2) la tabla canónica de límites por plan; (3) este documento marco; (4) los T&C de cada producto.</p>
<h2>2. Composición y modelo comercial</h2>
<p>Todos los planes incluyen los cinco productos: <strong>RPA Studio</strong> (entorno de desarrollo de robots), <strong>Saturn Studio</strong> (constructor de workflows cloud con 500+ apps), <strong>Orquestador</strong> (administración, calendarización, despacho, monitoreo y autenticación central, incluye Xperience), <strong>AI Studio</strong> (procesamiento inteligente de documentos, correos, imágenes y audio) y <strong>Nexus</strong> (plataforma low-code de aplicaciones internas). Cada nivel de plan incluye al menos las prestaciones del nivel inmediatamente inferior.</p>
<p>La capacidad de ejecución se gobierna por procesos administrados por el Orquestador; no existe cobro por robot, agente o runner. Se distinguen procesos administrados (total desplegado y retenido) y procesos en ejecución paralela (concurrencia). Los límites de ejecución paralela del Orquestador y de Saturn Studio son independientes: cada producto dispone de su capacidad completa.</p>
<h2>3. Autenticación, auditoría e inteligencia artificial</h2>
<p>El Orquestador actúa como proveedor único de identidad de la Suite: todos los productos inician sesión contra él. El SSO con Google/OAuth está disponible en todos los planes; la integración con Active Directory es exclusiva del plan Corporate (en Nexus, además habilita SSO obligatorio y aprovisionamiento SCIM).</p>
<p>Los audit logs (registro de acciones administrativas) están disponibles en todos los planes y productos, con retención escalonada. El plan Corporate cumple el benchmark de 12 meses asociado a la certificación ISO 27001 (control A.8.15) y habilita export vía API hacia sistemas SIEM.</p>
<p>Todos los planes incluyen el modelo interno de AI Studio y conexión con LLMs de terceros en Saturn Studio. Desde el plan Standard, el Cliente puede conectar su propio modelo externo (Bring Your Own Model). Los créditos de AI Studio se asignan como cuota anual sin rollover. <strong>Cuando un flujo envía información a un modelo de IA externo al entorno Rocketbot, el tratamiento y la seguridad de esa información quedan sujetos a los términos del proveedor de ese modelo</strong> — el proveedor de la Suite no responde por la seguridad de datos ya transferidos fuera de su entorno.</p>
<h2>4. Límites por plan</h2>
{plan_table}
<h2>5. Soporte y despliegue</h2>
<p>El soporte se define a nivel de Suite y aplica a todos los productos por igual. Los tiempos de primera respuesta se miden en minutos hábiles 5×8 y no constituyen compromiso de resolución. Todos los planes en modalidad SaaS operan sobre el cloud público de AWS.</p>
{support_table}
<h2>6. Responsabilidades técnicas</h2>
<p><strong>Del Cliente:</strong> dimensionar el plan según su carga, usuarios y requisitos de seguridad; administrar usuarios, credenciales y accesos con mínimo privilegio; evitar el registro de datos confidenciales en logs y aplicar enmascaramiento; evaluar qué contenido envía a modelos de IA externos; cumplir los términos de los sistemas de terceros automatizados y la normativa aplicable.</p>
<p><strong>Del proveedor:</strong> mantener disponibles los productos de la Suite conforme al contrato; prestar soporte y corregir defectos reproducibles; notificar modificaciones materiales; mantener la certificación ISO 27001 vigente a nivel de suite.</p>
<h2>7. Limitaciones y disposiciones finales</h2>
<p>Los resultados de modelos de IA están sujetos a limitaciones inherentes (error, sesgos, variabilidad) y no deben interpretarse como consejo profesional; su uso en decisiones de alto impacto requiere validación del Cliente. La Suite no provee de forma nativa mecanismos de integridad evidencial forense (firma digital, sellado de tiempo); cuando existan requisitos regulatorios probatorios, el Cliente debe implementar controles compensatorios externos.</p>
<p>El detalle de las responsabilidades compartidas entre el Cliente y el proveedor se describe en la <a href="https://docs.rocketbot.com/2024/05/16/matriz-de-responsabilidad/" target="_blank" rel="noopener">matriz de responsabilidad</a>.</p>
<p>En caso de discrepancia entre este documento y el contrato comercial, prevalece el contrato. <strong>La versión en español de este documento es la versión oficial</strong>; las traducciones existentes tienen carácter referencial.</p>
""".format(plan_table=table(PLAN_COLS, plan_rows_es), support_table=table(PLAN_COLS, support_rows))

    en = """
<div class="rb-legal-note">{note}</div>
<h2>1. Purpose and scope</h2>
<p>This document sets out the technical terms and conditions of the Rocketbot Suite ("the Suite"), an integrated set made up of RPA Studio, Saturn Studio, the Orchestrator (including its Xperience module), AI Studio and Nexus. It defines the plan-based commercial model, cross-product capabilities and limits, and the order of precedence relative to each product's own technical terms.</p>
<p>It applies to any individual or legal entity ("the Client") that acquires and uses the Suite under any of its plans: Entry 1, Standard, Enterprise and Corporate. Scope is limited to technical aspects; commercial, legal and licensing terms are governed by the acquisition contract.</p>
<p>This is a technical, descriptive document, not itself a contract or a binding SLA. In case of discrepancy, the order of precedence is: (1) the commercial contract; (2) the canonical plan-limits table; (3) this framework document; (4) each product's own technical terms.</p>
<h2>2. Composition and commercial model</h2>
<p>Every plan includes all five products: <strong>RPA Studio</strong> (robot development environment), <strong>Saturn Studio</strong> (cloud workflow builder with 500+ apps), <strong>Orchestrator</strong> (central management, scheduling, dispatch, monitoring and authentication, including Xperience), <strong>AI Studio</strong> (intelligent processing of documents, emails, images and audio) and <strong>Nexus</strong> (low-code platform for internal applications). Each higher plan tier includes at least the features of the tier immediately below it.</p>
<p>Execution capacity is governed by processes managed by the Orchestrator; there is no charge per robot, agent or runner. A distinction is made between managed processes (total deployed and retained) and processes running in parallel (concurrency). Parallel-execution limits for the Orchestrator and for Saturn Studio are independent: each product has its own full capacity.</p>
<h2>3. Authentication, auditing and artificial intelligence</h2>
<p>The Orchestrator acts as the Suite's single identity provider: every product signs in against it. Google/OAuth SSO is available on all plans; Active Directory integration is exclusive to the Corporate plan (in Nexus, Corporate additionally enables enforced SSO and SCIM provisioning).</p>
<p>Audit logs (administrative action records) are available on every plan and product, with tiered retention. The Corporate plan meets the 12-month traceability benchmark associated with the provider's ISO 27001 certification (control A.8.15) and enables API export to SIEM systems.</p>
<p>Every plan includes AI Studio's internal model and connection to third-party LLMs within Saturn Studio. From the Standard plan up, the Client may connect its own external model (Bring Your Own Model). AI Studio credits are allocated as an annual quota with no rollover. <strong>When a flow sends information to an AI model hosted outside the Rocketbot environment, the processing and security of that information are subject to the terms of that model's provider</strong> — the Suite provider is not responsible for the security of data once transferred outside its environment.</p>
<h2>4. Plan limits</h2>
{plan_table}
<h2>5. Support and deployment</h2>
<p>Support is defined at the Suite level and applies equally to every product. First-response times are measured in minutes within business hours (5×8) and do not constitute a resolution-time commitment. All SaaS-mode plans run on the AWS public cloud.</p>
{support_table}
<h2>6. Technical responsibilities</h2>
<p><strong>Client:</strong> size the plan to its load, user count and security requirements; manage users, credentials and access under least privilege; avoid logging confidential data and apply masking; assess what content it sends to external AI models; comply with the terms of automated third-party systems and applicable regulations.</p>
<p><strong>Provider:</strong> keep the Suite's products available per the contract; provide support and fix reproducible defects; notify material changes; maintain the Suite's ISO 27001 certification.</p>
<h2>7. Limitations and final provisions</h2>
<p>Outputs from AI models are subject to inherent limitations (error, bias, variability) and should not be treated as professional advice; using them in high-impact decisions requires Client validation. The Suite does not natively provide forensic evidentiary-integrity mechanisms (digital signature, timestamping); where regulatory evidentiary requirements exist, the Client must implement external compensating controls.</p>
<p>The breakdown of shared responsibilities between the Client and the provider is described in the <a href="https://docs.rocketbot.com/2024/05/16/matriz-de-responsabilidad/" target="_blank" rel="noopener">responsibility matrix</a>.</p>
<p>In case of discrepancy between this document and the commercial contract, the contract prevails. <strong>The Spanish-language version of this document is the official version</strong>; any existing translations are for reference only.</p>
""".format(note=LANG_NOTE['en'], plan_table=table(PLAN_COLS, plan_rows_en), support_table=table(PLAN_COLS, support_rows_en))

    pt = """
<div class="rb-legal-note">{note}</div>
<h2>1. Objeto e escopo</h2>
<p>Este documento estabelece os termos e condições técnicas da Suite Rocketbot ("a Suite"), conjunto integrado composto por RPA Studio, Saturn Studio, o Orquestrador (incluindo seu módulo Xperience), AI Studio e Nexus. Define o modelo comercial por planos, as capacidades e limites transversais a todos os produtos, e a ordem de precedência em relação aos T&C de cada produto.</p>
<p>Aplica-se a qualquer pessoa física ou jurídica ("o Cliente") que adquira e utilize a Suite em qualquer um de seus planos: Entry 1, Standard, Enterprise e Corporate. O escopo se limita aos aspectos técnicos; as condições comerciais, legais e de licenciamento são regidas pelo contrato de aquisição.</p>
<p>É um documento técnico e descritivo, não um contrato nem um SLA vinculante por si só. Em caso de divergência, a ordem de precedência é: (1) o contrato comercial; (2) a tabela canônica de limites por plano; (3) este documento-quadro; (4) os T&C de cada produto.</p>
<h2>2. Composição e modelo comercial</h2>
<p>Todos os planos incluem os cinco produtos: <strong>RPA Studio</strong> (ambiente de desenvolvimento de robôs), <strong>Saturn Studio</strong> (construtor de workflows em nuvem com mais de 500 apps), <strong>Orquestrador</strong> (administração, agendamento, despacho, monitoramento e autenticação central, incluindo o Xperience), <strong>AI Studio</strong> (processamento inteligente de documentos, e-mails, imagens e áudio) e <strong>Nexus</strong> (plataforma low-code de aplicações internas). Cada nível de plano inclui pelo menos os recursos do nível imediatamente inferior.</p>
<p>A capacidade de execução é governada por processos administrados pelo Orquestrador; não há cobrança por robô, agente ou runner. Distinguem-se processos administrados (total implantado e retido) e processos em execução paralela (concorrência). Os limites de execução paralela do Orquestrador e do Saturn Studio são independentes: cada produto dispõe de sua capacidade completa.</p>
<h2>3. Autenticação, auditoria e inteligência artificial</h2>
<p>O Orquestrador atua como provedor único de identidade da Suite: todos os produtos fazem login contra ele. O SSO com Google/OAuth está disponível em todos os planos; a integração com Active Directory é exclusiva do plano Corporate (no Nexus, também habilita SSO obrigatório e provisionamento via SCIM).</p>
<p>Os audit logs (registro de ações administrativas) estão disponíveis em todos os planos e produtos, com retenção escalonada. O plano Corporate atende ao benchmark de 12 meses de rastreabilidade associado à certificação ISO 27001 (controle A.8.15) e habilita exportação via API para sistemas SIEM.</p>
<p>Todos os planos incluem o modelo interno do AI Studio e a conexão com LLMs de terceiros no Saturn Studio. A partir do plano Standard, o Cliente pode conectar seu próprio modelo externo (Bring Your Own Model). Os créditos do AI Studio são alocados como cota anual sem rollover. <strong>Quando um fluxo envia informações a um modelo de IA externo ao ambiente Rocketbot, o tratamento e a segurança dessas informações ficam sujeitos aos termos do provedor desse modelo</strong> — o provedor da Suite não se responsabiliza pela segurança dos dados já transferidos para fora de seu ambiente.</p>
<h2>4. Limites por plano</h2>
{plan_table}
<h2>5. Suporte e implantação</h2>
<p>O suporte é definido em nível de Suite e se aplica igualmente a todos os produtos. Os tempos de primeira resposta são medidos em minutos dentro do horário comercial 5×8 e não constituem compromisso de tempo de resolução. Todos os planos em modalidade SaaS operam na nuvem pública da AWS.</p>
{support_table}
<h2>6. Responsabilidades técnicas</h2>
<p><strong>Do Cliente:</strong> dimensionar o plano de acordo com sua carga, usuários e requisitos de segurança; administrar usuários, credenciais e acessos com privilégio mínimo; evitar o registro de dados confidenciais em logs e aplicar mascaramento; avaliar qual conteúdo envia a modelos de IA externos; cumprir os termos dos sistemas de terceiros automatizados e a normativa aplicável.</p>
<p><strong>Do provedor:</strong> manter disponíveis os produtos da Suite conforme o contrato; prestar suporte e corrigir defeitos reproduzíveis; notificar modificações materiais; manter a certificação ISO 27001 vigente em nível de suite.</p>
<h2>7. Limitações e disposições finais</h2>
<p>Os resultados de modelos de IA estão sujeitos a limitações inerentes (erro, viés, variabilidade) e não devem ser interpretados como aconselhamento profissional; seu uso em decisões de alto impacto requer validação do Cliente. A Suite não fornece nativamente mecanismos de integridade evidencial forense (assinatura digital, carimbo de tempo); quando existirem requisitos regulatórios probatórios, o Cliente deve implementar controles compensatórios externos.</p>
<p>O detalhamento das responsabilidades compartilhadas entre o Cliente e o provedor está descrito na <a href="https://docs.rocketbot.com/2024/05/16/matriz-de-responsabilidad/" target="_blank" rel="noopener">matriz de responsabilidade</a>.</p>
<p>Em caso de divergência entre este documento e o contrato comercial, prevalece o contrato. <strong>A versão em espanhol deste documento é a versão oficial</strong>; as traduções existentes têm caráter referencial.</p>
""".format(note=LANG_NOTE['pt'], plan_table=table(PLAN_COLS, plan_rows_pt), support_table=table(PLAN_COLS, support_rows_pt))

    return {'es': es, 'en': en, 'pt': pt}


def content_rpa():
    dev_rows = {
        'es': [['Licencias de desarrollo incluidas','2','3','5','Ilimitadas'],['Robots construibles','Ilimitados','Ilimitados','Ilimitados','Ilimitados'],['Agentes registrables','Ilimitados','Ilimitados','Ilimitados','Ilimitados']],
        'en': [['Development licenses included','2','3','5','Unlimited'],['Buildable robots','Unlimited','Unlimited','Unlimited','Unlimited'],['Registerable agents','Unlimited','Unlimited','Unlimited','Unlimited']],
        'pt': [['Licenças de desenvolvimento incluídas','2','3','5','Ilimitadas'],['Robôs construíveis','Ilimitados','Ilimitados','Ilimitados','Ilimitados'],['Agentes registráveis','Ilimitados','Ilimitados','Ilimitados','Ilimitados']],
    }
    sup_rows = {
        'es': [['Canal de soporte','Slack','Slack','Slack','Slack'],['Horario','8×5','8×5','8×5','8×5'],['Evento 7×24','Costo adicional','Costo adicional','Costo adicional','Costo adicional'],['1ra respuesta (min)','60','45','30','15'],['CSM','Compartido','Compartido','Compartido','Dedicado'],['Meetup','No','Sí','Sí','Sí']],
        'en': [['Support channel','Slack','Slack','Slack','Slack'],['Hours','8×5','8×5','8×5','8×5'],['24/7 event coverage','Extra cost','Extra cost','Extra cost','Extra cost'],['1st response (min)','60','45','30','15'],['CSM','Shared','Shared','Shared','Dedicated'],['Meetup','No','Yes','Yes','Yes']],
        'pt': [['Canal de suporte','Slack','Slack','Slack','Slack'],['Horário','8×5','8×5','8×5','8×5'],['Evento 7×24','Custo adicional','Custo adicional','Custo adicional','Custo adicional'],['1ª resposta (min)','60','45','30','15'],['CSM','Compartilhado','Compartilhado','Compartilhado','Dedicado'],['Meetup','Não','Sim','Sim','Sim']],
    }
    es = """
<h2>1. Objeto y alcance</h2>
<p>Este documento describe RPA Studio ("el Studio"), el entorno de desarrollo integrado (IDE) de construcción de robots RPA de la Suite Rocketbot: sus capacidades, componentes, límites técnicos y condiciones de uso. Aplica a todo Cliente que utilice RPA Studio dentro de cualquier plan de la Suite. Es un documento técnico y descriptivo, no un contrato ni un SLA vinculante por sí mismo.</p>
<h2>2. Arquitectura y niveles de servicio</h2>
<p>RPA Studio es una aplicación de escritorio multiplataforma instalada en las estaciones de los desarrolladores del Cliente: allí se construyen, prueban y depuran los robots, que luego se publican al repositorio central para su ejecución productiva. El acceso se autentica contra el Orquestador, con 2FA en todos los planes y SSO según el plan.</p>
<p>Se ofrece en todos los planes de la Suite. El único límite cuantitativo propio del Studio son las licencias de desarrollo por plan:</p>
{dev_table}
<h2>3. Editor de robots</h2>
<p>Entorno visual de composición de comandos con lógica condicional, ciclos, variables y manejo de errores, y ejecución local paso a paso para prueba y depuración. La cantidad de robots construibles es ilimitada en todos los planes; la ejecución productiva se realiza a través del Orquestador y está sujeta a la cuota de procesos del plan. El versionado formal de robots publicados es responsabilidad del repositorio del Orquestador.</p>
<h2>4. Comandos y módulos</h2>
<p>Catálogo de comandos y módulos oficiales mantenidos por el proveedor: interacción con interfaces gráficas (clics, escritura, lectura de pantalla), integración con APIs, bases de datos y servicios web, y desarrollo de comandos personalizados por el Cliente. El catálogo puede variar por cambios en los sistemas externos integrados; el proveedor no garantiza su disponibilidad permanente. <strong>Los comandos y módulos personalizados desarrollados por el Cliente o terceros quedan bajo su responsabilidad</strong> respecto a seguridad, mantenimiento y cumplimiento normativo — el proveedor no responde por errores o vulnerabilidades introducidas por dicho código. La automatización de sistemas de terceros debe respetar los términos de uso de esos sistemas.</p>
<h2>5. Publicación, ciclo de vida y seguridad</h2>
<p>Los robots se publican al repositorio centralizado del Orquestador, que gestiona su versionado y actualización en producción; la promoción entre etapas (desarrollo, calidad, producción) se gestiona mediante procedimientos organizacionales del Cliente, quien es responsable de probar los robots antes de publicarlos productivamente.</p>
<p>La gestión de credenciales de los robots debe hacerse mediante los mecanismos seguros de la Suite (no en texto plano). <strong>Cuando un robot envía información a servicios externos al entorno Rocketbot</strong> (incluyendo modelos de IA de terceros vía AI Studio o integraciones directas), el tratamiento y la seguridad de esa información quedan sujetos a los términos del servicio externo elegido por el Cliente. La seguridad de las estaciones de trabajo donde se instala el Studio es responsabilidad del Cliente.</p>
<h2>6. Soporte</h2>
<p>El soporte se define a nivel de Suite y aplica a todos los productos por igual. Los tiempos de primera respuesta se miden en minutos hábiles 5×8; la atención 7×24 tiene costo adicional en todos los planes y la atención por meetup se incluye desde Standard. No incluye, salvo pacto expreso, el desarrollo de robots ni la administración de las estaciones de trabajo.</p>
{sup_table}
<h2>7. Responsabilidades técnicas</h2>
<p><strong>Del Cliente:</strong> administrar la asignación de licencias de desarrollo sin exceder el plan; mantener las estaciones de desarrollo seguras y compatibles; diseñar, probar y mantener los robots ante cambios en los sistemas automatizados; verificar el cumplimiento normativo de sus automatizaciones; implementar controles compensatorios de separación de etapas y aprobación de cambios cuando el producto no los soporte nativamente.</p>
<p><strong>Del proveedor:</strong> mantener disponibles los instaladores, módulos oficiales y documentación; corregir defectos reproducibles; notificar modificaciones materiales.</p>
<h2>8. Limitaciones</h2>
<p>RPA Studio es una herramienta de construcción; la operación productiva (calendarización, despacho, monitoreo, logs) se rige por el T&C del Orquestador. El proveedor no garantiza que un robot funcione indefinidamente sin mantenimiento ante cambios en los sistemas automatizados. El uso de RPA Studio para acciones que requieran juicio profesional, decisiones regulatorias o consentimiento de terceros es responsabilidad exclusiva del Cliente.</p>
<p><strong>La versión en español de este documento es la versión oficial</strong>; las traducciones existentes tienen carácter referencial.</p>
""".format(dev_table=table(PLAN_COLS, dev_rows['es']), sup_table=table(PLAN_COLS, sup_rows['es']))

    en = """
<div class="rb-legal-note">{note}</div>
<h2>1. Purpose and scope</h2>
<p>This document describes RPA Studio ("the Studio"), the integrated development environment (IDE) for building RPA robots within the Rocketbot Suite: its capabilities, components, technical limits and conditions of use. It applies to any Client using RPA Studio under any Suite plan. It is a technical, descriptive document, not itself a contract or binding SLA.</p>
<h2>2. Architecture and service levels</h2>
<p>RPA Studio is a cross-platform desktop application installed on the Client's developer workstations: robots are built, tested and debugged there, then published to the central repository for production execution. Access is authenticated against the Orchestrator, with 2FA on every plan and SSO depending on the plan.</p>
<p>It is offered on every Suite plan. The Studio's only quantitative limit of its own is development licenses per plan:</p>
{dev_table}
<h2>3. Robot editor</h2>
<p>A visual command-composition environment with conditional logic, loops, variables, error handling, and step-by-step local execution for testing and debugging. The number of buildable robots is unlimited on every plan; production execution runs through the Orchestrator and is subject to the plan's process quota. Formal versioning of published robots is the responsibility of the Orchestrator's repository.</p>
<h2>4. Commands and modules</h2>
<p>A catalog of official commands and modules maintained by the provider: interaction with graphical interfaces (clicks, typing, screen reading), integration with APIs, databases and web services, and custom command development by the Client. The catalog may vary due to changes in integrated external systems; the provider does not guarantee its permanent availability. <strong>Custom commands and modules developed by the Client or third parties remain the Client's responsibility</strong> for security, maintenance and regulatory compliance — the provider is not liable for errors or vulnerabilities introduced by such code. Automating third-party systems must respect those systems' terms of use.</p>
<h2>5. Publishing, lifecycle and security</h2>
<p>Robots are published to the Orchestrator's centralized repository, which manages their versioning and production updates; promotion between stages (development, QA, production) is managed through the Client's own organizational procedures, and the Client is responsible for testing robots before publishing them to production.</p>
<p>Robot credentials must be managed through the Suite's secure mechanisms (never in plain text). <strong>When a robot sends information to services outside the Rocketbot environment</strong> (including third-party AI models via AI Studio or direct integrations), the processing and security of that information are subject to the terms of the external service chosen by the Client. Security of the workstations where the Studio is installed is the Client's responsibility.</p>
<h2>6. Support</h2>
<p>Support is defined at the Suite level and applies equally to every product. First-response times are measured in business-hour minutes (5×8); 24/7 coverage carries an extra cost on every plan, and meetup support is included from Standard up. Support does not include, absent express agreement, robot development or administration of workstations.</p>
{sup_table}
<h2>7. Technical responsibilities</h2>
<p><strong>Client:</strong> manage development-license allocation without exceeding the plan; keep development workstations secure and compatible; design, test and maintain robots as automated systems change; verify the regulatory compliance of its automations; implement compensating controls for stage separation and change approval when not natively supported.</p>
<p><strong>Provider:</strong> keep installers, official modules and documentation available; fix reproducible defects; notify material changes.</p>
<h2>8. Limitations</h2>
<p>RPA Studio is a build tool; production operation (scheduling, dispatch, monitoring, logs) is governed by the Orchestrator's technical terms. The provider does not guarantee a robot will keep working indefinitely without maintenance as automated systems change. Using RPA Studio for actions requiring professional judgment, regulatory decisions or third-party consent is the Client's sole responsibility.</p>
<p><strong>The Spanish-language version of this document is the official version</strong>; any existing translations are for reference only.</p>
""".format(note=LANG_NOTE['en'], dev_table=table(PLAN_COLS, dev_rows['en']), sup_table=table(PLAN_COLS, sup_rows['en']))

    pt = """
<div class="rb-legal-note">{note}</div>
<h2>1. Objeto e escopo</h2>
<p>Este documento descreve o RPA Studio ("o Studio"), o ambiente de desenvolvimento integrado (IDE) de construção de robôs RPA da Suite Rocketbot: suas capacidades, componentes, limites técnicos e condições de uso. Aplica-se a todo Cliente que utilize o RPA Studio dentro de qualquer plano da Suite. É um documento técnico e descritivo, não um contrato nem um SLA vinculante por si só.</p>
<h2>2. Arquitetura e níveis de serviço</h2>
<p>O RPA Studio é uma aplicação desktop multiplataforma instalada nas estações de trabalho dos desenvolvedores do Cliente: ali os robôs são construídos, testados e depurados, sendo depois publicados no repositório central para execução em produção. O acesso é autenticado contra o Orquestrador, com 2FA em todos os planos e SSO conforme o plano.</p>
<p>É oferecido em todos os planos da Suite. O único limite quantitativo próprio do Studio são as licenças de desenvolvimento por plano:</p>
{dev_table}
<h2>3. Editor de robôs</h2>
<p>Ambiente visual de composição de comandos com lógica condicional, laços, variáveis e tratamento de erros, além de execução local passo a passo para teste e depuração. A quantidade de robôs construíveis é ilimitada em todos os planos; a execução em produção ocorre por meio do Orquestrador e está sujeita à cota de processos do plano. O versionamento formal dos robôs publicados é responsabilidade do repositório do Orquestrador.</p>
<h2>4. Comandos e módulos</h2>
<p>Catálogo de comandos e módulos oficiais mantidos pelo provedor: interação com interfaces gráficas (cliques, digitação, leitura de tela), integração com APIs, bancos de dados e serviços web, e desenvolvimento de comandos personalizados pelo Cliente. O catálogo pode variar devido a mudanças nos sistemas externos integrados; o provedor não garante sua disponibilidade permanente. <strong>Os comandos e módulos personalizados desenvolvidos pelo Cliente ou por terceiros ficam sob sua responsabilidade</strong> quanto à segurança, manutenção e conformidade normativa — o provedor não responde por erros ou vulnerabilidades introduzidas por esse código. A automação de sistemas de terceiros deve respeitar os termos de uso desses sistemas.</p>
<h2>5. Publicação, ciclo de vida e segurança</h2>
<p>Os robôs são publicados no repositório centralizado do Orquestrador, que gerencia seu versionamento e atualizações em produção; a promoção entre etapas (desenvolvimento, qualidade, produção) é gerenciada por procedimentos organizacionais do Cliente, que é responsável por testar os robôs antes de publicá-los em produção.</p>
<p>As credenciais dos robôs devem ser gerenciadas pelos mecanismos seguros da Suite (nunca em texto simples). <strong>Quando um robô envia informações a serviços externos ao ambiente Rocketbot</strong> (incluindo modelos de IA de terceiros via AI Studio ou integrações diretas), o tratamento e a segurança dessas informações ficam sujeitos aos termos do serviço externo escolhido pelo Cliente. A segurança das estações de trabalho onde o Studio é instalado é responsabilidade do Cliente.</p>
<h2>6. Suporte</h2>
<p>O suporte é definido em nível de Suite e se aplica igualmente a todos os produtos. Os tempos de primeira resposta são medidos em minutos do horário comercial 5×8; o atendimento 7×24 tem custo adicional em todos os planos e o atendimento por meetup é incluído a partir do Standard. O suporte não inclui, salvo acordo expresso, o desenvolvimento de robôs nem a administração das estações de trabalho.</p>
{sup_table}
<h2>7. Responsabilidades técnicas</h2>
<p><strong>Do Cliente:</strong> administrar a alocação de licenças de desenvolvimento sem exceder o plano; manter as estações de desenvolvimento seguras e compatíveis; projetar, testar e manter os robôs diante de mudanças nos sistemas automatizados; verificar a conformidade normativa de suas automações; implementar controles compensatórios de separação de etapas e aprovação de mudanças quando o produto não os suportar nativamente.</p>
<p><strong>Do provedor:</strong> manter disponíveis os instaladores, módulos oficiais e documentação; corrigir defeitos reproduzíveis; notificar modificações materiais.</p>
<h2>8. Limitações</h2>
<p>O RPA Studio é uma ferramenta de construção; a operação em produção (agendamento, despacho, monitoramento, logs) é regida pelos T&C do Orquestrador. O provedor não garante que um robô funcionará indefinidamente sem manutenção diante de mudanças nos sistemas automatizados. O uso do RPA Studio para ações que exijam julgamento profissional, decisões regulatórias ou consentimento de terceiros é responsabilidade exclusiva do Cliente.</p>
<p><strong>A versão em espanhol deste documento é a versão oficial</strong>; as traduções existentes têm caráter referencial.</p>
""".format(note=LANG_NOTE['pt'], dev_table=table(PLAN_COLS, dev_rows['pt']), sup_table=table(PLAN_COLS, sup_rows['pt']))

    return {'es': es, 'en': en, 'pt': pt}


def content_saturn():
    limits_es = [['Ejecuciones en paralelo','5','20','50','200'],['Tiempo máximo por flow','10 min','30 min','30 min','1 hora'],['Tamaño máximo de archivo','100 MB','250 MB','250 MB','1 GB'],['Moons consecutivos por ejecución','10.000','30.000','30.000','Ilimitado'],['Apps y componentes estándar','500+','500+','500+','500+'],['Funciones custom (JS)','No','Limitado','Limitado','Avanzado'],['Miembros del equipo','5','15','15','Ilimitados'],['Retención de logs de ejecución','7 días','30 días','30 días','365 días']]
    limits_en = [['Parallel executions','5','20','50','200'],['Maximum time per flow','10 min','30 min','30 min','1 hour'],['Maximum file size','100 MB','250 MB','250 MB','1 GB'],['Consecutive moons per execution','10,000','30,000','30,000','Unlimited'],['Standard apps and components','500+','500+','500+','500+'],['Custom functions (JS)','No','Limited','Limited','Advanced'],['Team members','5','15','15','Unlimited'],['Execution log retention','7 days','30 days','30 days','365 days']]
    limits_pt = [['Execuções em paralelo','5','20','50','200'],['Tempo máximo por flow','10 min','30 min','30 min','1 hora'],['Tamanho máximo de arquivo','100 MB','250 MB','250 MB','1 GB'],['Moons consecutivos por execução','10.000','30.000','30.000','Ilimitado'],['Apps e componentes padrão','500+','500+','500+','500+'],['Funções custom (JS)','Não','Limitado','Limitado','Avançado'],['Membros da equipe','5','15','15','Ilimitados'],['Retenção de logs de execução','7 dias','30 dias','30 dias','365 dias']]

    es = """
<h2>1. Objeto y alcance</h2>
<p>Este documento describe Saturn Studio ("la Plataforma"), el componente de orquestación de workflows cloud de la Suite Rocketbot: capacidades funcionales, límites técnicos, restricciones operativas y responsabilidades por módulo y plan. Saturn no se comercializa ni se factura como producto independiente: se contrata exclusivamente dentro de un plan de la Suite.</p>
<h2>2. Workflow Builder</h2>
<p>Constructor visual no-code para diseñar flows mediante drag-and-drop, con lógica condicional, ciclos, transformaciones de datos e integración con servicios externos. La cantidad de flows es ilimitada en todos los planes (sujeta a los límites prácticos de ejecución del plan). Las funciones personalizadas en JavaScript están disponibles desde Standard (modo limitado) y con capacidades avanzadas en Corporate — <strong>su uso es responsabilidad del Cliente</strong>, el proveedor no garantiza el comportamiento de dicho código.</p>
<h2>3. Integraciones</h2>
<p>Catálogo de más de 500 apps y componentes estándar en todos los planes, webhooks de entrada, conector nativo a robots RPA Rocketbot, capacidad de Human-in-the-Loop y conexión con LLMs de terceros (todos los planes). Las apps personalizadas están disponibles de forma limitada en Standard/Enterprise y avanzada en Corporate; las Apps Enterprise (conectores a sistemas corporativos especializados) son exclusivas de Corporate. <strong>Cuando un flow envía información a un modelo de IA externo al entorno Rocketbot, el tratamiento y la seguridad de esa información quedan sujetos a los términos del proveedor de ese modelo</strong> — Rocketbot no responde por la seguridad de datos ya transferidos fuera de su entorno.</p>
<h2>4. Motor de ejecución</h2>
<p>Procesa las instancias de flows administrando concurrencia, tiempos de ejecución, colas, prioridades y archivos. Es el componente más sensible a los límites técnicos del plan:</p>
{limits_table}
<p>El tiempo máximo por flow es un techo duro: una ejecución que lo alcance es terminada por la Plataforma. Al alcanzarse el límite de procesos simultáneos, las nuevas solicitudes se encolan hasta liberar capacidad.</p>
<h2>5. Monitoreo, gobernanza y seguridad</h2>
<p>Incluye historial de ejecuciones, logs detallados y dashboards de analytics, con retención FIFO según plan (para necesidades de retención mayor, el Cliente debe exportar logs periódicamente bajo su responsabilidad). Los audit logs de acciones administrativas están disponibles en todos los planes.</p>
<p>2FA en todos los planes; SSO con Google/OAuth en todos los planes y Active Directory exclusivo de Corporate; almacén cifrado de secretos desde Standard (no existe en Entry 1, por lo que no se recomienda uso productivo con credenciales sensibles en esos planes); comunicación cifrada TLS y aislamiento lógico entre tenants en todos los planes.</p>
<h2>6. Soporte y responsabilidades</h2>
<p>El soporte se define a nivel de Suite. <strong>Del Cliente:</strong> dimensionar el plan, diseñar flows dentro de los límites técnicos, gestionar credenciales y su rotación, evitar datos confidenciales en logs, exportar evidencia cuando la retención del plan sea insuficiente, configurar accesos y 2FA. <strong>Del proveedor:</strong> disponibilidad conforme al plan, parches sin afectar flows del Cliente, aviso de mantenimientos, soporte técnico, cifrado en tránsito y en reposo, aislamiento entre tenants.</p>
<h2>7. Limitaciones</h2>
<p>La Plataforma no garantiza el comportamiento de código JavaScript o apps personalizadas del Cliente, ni la disponibilidad de servicios externos integrados. No provee de forma nativa versionado por Git, ambientes DEV/QA/PROD separados ni integridad evidencial forense sobre logs. La precisión de AI Studio dentro de los flows está sujeta a las limitaciones de los modelos de IA generativa y debe validarse antes de su uso productivo.</p>
<p><strong>La versión en español de este documento es la versión oficial</strong>; las traducciones existentes tienen carácter referencial.</p>
""".format(limits_table=table(PLAN_COLS, limits_es))

    en = """
<div class="rb-legal-note">{note}</div>
<h2>1. Purpose and scope</h2>
<p>This document describes Saturn Studio ("the Platform"), the cloud workflow-orchestration component of the Rocketbot Suite: functional capabilities, technical limits, operational restrictions and responsibilities by module and plan. Saturn is not sold or billed as a standalone product: it is only contracted within a Suite plan.</p>
<h2>2. Workflow Builder</h2>
<p>A no-code visual builder for designing flows via drag-and-drop, with conditional logic, loops, data transformations and integration with external services. The number of flows is unlimited on every plan (subject to the plan's practical execution limits). Custom JavaScript functions are available from Standard up (limited mode) with advanced capabilities on Corporate — <strong>their use is the Client's responsibility</strong>; the provider does not guarantee the behavior of such code.</p>
<h2>3. Integrations</h2>
<p>A catalog of 500+ standard apps and components on every plan, inbound webhooks, a native connector to Rocketbot RPA robots, Human-in-the-Loop capability, and connection to third-party LLMs (every plan). Custom apps are available in limited form on Standard/Enterprise and in advanced form on Corporate; Enterprise Apps (connectors to specialized corporate systems) are Corporate-only. <strong>When a flow sends information to an AI model hosted outside the Rocketbot environment, the processing and security of that information are subject to that model provider's terms</strong> — Rocketbot is not responsible for the security of data once transferred outside its environment.</p>
<h2>4. Execution engine</h2>
<p>Processes flow instances, managing concurrency, execution times, queues, priorities and files. It is the component most sensitive to the plan's technical limits:</p>
{limits_table}
<p>The maximum time per flow is a hard ceiling: an execution that reaches it is terminated by the Platform. Once the concurrent-process limit is reached, new requests queue until capacity frees up.</p>
<h2>5. Monitoring, governance and security</h2>
<p>Includes execution history, detailed logs and analytics dashboards, with FIFO retention by plan (for greater retention needs, the Client must periodically export logs at its own responsibility). Audit logs of administrative actions are available on every plan.</p>
<p>2FA on every plan; Google/OAuth SSO on every plan and Active Directory exclusive to Corporate; encrypted secrets store from Standard up (not present on Entry 1, so production use with sensitive credentials is not recommended on those plans); encrypted TLS communication and logical tenant isolation on every plan.</p>
<h2>6. Support and responsibilities</h2>
<p>Support is defined at the Suite level. <strong>Client:</strong> size the plan, design flows within technical limits, manage credentials and their rotation, avoid confidential data in logs, export evidence when the plan's retention is insufficient, configure access and 2FA. <strong>Provider:</strong> availability per the plan, patches that do not affect the Client's flows, maintenance notices, technical support, encryption in transit and at rest, tenant isolation.</p>
<h2>7. Limitations</h2>
<p>The Platform does not guarantee the behavior of the Client's custom JavaScript code or apps, nor the availability of integrated external services. It does not natively provide Git-style versioning, separate DEV/QA/PROD environments, or forensic evidentiary integrity over logs. AI Studio's accuracy within flows is subject to the limitations of generative AI models and must be validated before production use.</p>
<p><strong>The Spanish-language version of this document is the official version</strong>; any existing translations are for reference only.</p>
""".format(note=LANG_NOTE['en'], limits_table=table(PLAN_COLS, limits_en))

    pt = """
<div class="rb-legal-note">{note}</div>
<h2>1. Objeto e escopo</h2>
<p>Este documento descreve o Saturn Studio ("a Plataforma"), o componente de orquestração de workflows em nuvem da Suite Rocketbot: capacidades funcionais, limites técnicos, restrições operacionais e responsabilidades por módulo e plano. O Saturn não é comercializado nem faturado como produto independente: é contratado exclusivamente dentro de um plano da Suite.</p>
<h2>2. Workflow Builder</h2>
<p>Construtor visual no-code para desenhar flows por drag-and-drop, com lógica condicional, laços, transformações de dados e integração com serviços externos. A quantidade de flows é ilimitada em todos os planos (sujeita aos limites práticos de execução do plano). As funções personalizadas em JavaScript estão disponíveis a partir do Standard (modo limitado) e com capacidades avançadas no Corporate — <strong>seu uso é responsabilidade do Cliente</strong>, o provedor não garante o comportamento desse código.</p>
<h2>3. Integrações</h2>
<p>Catálogo com mais de 500 apps e componentes padrão em todos os planos, webhooks de entrada, conector nativo a robôs RPA Rocketbot, capacidade de Human-in-the-Loop e conexão com LLMs de terceiros (todos os planos). Apps personalizados estão disponíveis de forma limitada no Standard/Enterprise e avançada no Corporate; os Apps Enterprise (conectores a sistemas corporativos especializados) são exclusivos do Corporate. <strong>Quando um flow envia informações a um modelo de IA externo ao ambiente Rocketbot, o tratamento e a segurança dessas informações ficam sujeitos aos termos do provedor desse modelo</strong> — a Rocketbot não se responsabiliza pela segurança dos dados já transferidos para fora de seu ambiente.</p>
<h2>4. Motor de execução</h2>
<p>Processa as instâncias de flows administrando concorrência, tempos de execução, filas, prioridades e arquivos. É o componente mais sensível aos limites técnicos do plano:</p>
{limits_table}
<p>O tempo máximo por flow é um teto rígido: uma execução que o atinja é encerrada pela Plataforma. Ao atingir o limite de processos simultâneos, novas solicitações entram em fila até a liberação de capacidade.</p>
<h2>5. Monitoramento, governança e segurança</h2>
<p>Inclui histórico de execuções, logs detalhados e dashboards de analytics, com retenção FIFO conforme o plano (para necessidades de retenção maiores, o Cliente deve exportar logs periodicamente sob sua responsabilidade). Os audit logs de ações administrativas estão disponíveis em todos os planos.</p>
<p>2FA em todos os planos; SSO com Google/OAuth em todos os planos e Active Directory exclusivo do Corporate; armazenamento cifrado de segredos a partir do Standard (inexistente no Entry 1, portanto o uso produtivo com credenciais sensíveis não é recomendado nesses planos); comunicação cifrada TLS e isolamento lógico entre tenants em todos os planos.</p>
<h2>6. Suporte e responsabilidades</h2>
<p>O suporte é definido em nível de Suite. <strong>Do Cliente:</strong> dimensionar o plano, projetar flows dentro dos limites técnicos, gerenciar credenciais e sua rotação, evitar dados confidenciais em logs, exportar evidências quando a retenção do plano for insuficiente, configurar acessos e 2FA. <strong>Do provedor:</strong> disponibilidade conforme o plano, patches sem afetar os flows do Cliente, aviso de manutenções, suporte técnico, criptografia em trânsito e em repouso, isolamento entre tenants.</p>
<h2>7. Limitações</h2>
<p>A Plataforma não garante o comportamento de código JavaScript ou apps personalizados do Cliente, nem a disponibilidade de serviços externos integrados. Não fornece nativamente versionamento por Git, ambientes DEV/QA/PROD separados nem integridade evidencial forense sobre logs. A precisão do AI Studio dentro dos flows está sujeita às limitações dos modelos de IA generativa e deve ser validada antes do uso produtivo.</p>
<p><strong>A versão em espanhol deste documento é a versão oficial</strong>; as traduções existentes têm caráter referencial.</p>
""".format(note=LANG_NOTE['pt'], limits_table=table(PLAN_COLS, limits_pt))

    return {'es': es, 'en': en, 'pt': pt}


def content_orquestador():
    limits_es = [['Procesos administrados','5','20','50','1.000'],['Procesos en ejecución paralela','5','20','50','200'],['Robots registrables','Ilimitados','Ilimitados','Ilimitados','Ilimitados'],['Licencias de desarrollo (RPA Studio)','2','3','5','Ilimitadas'],['Usuarios Process Control','5','5','15','Ilimitados'],['Usuarios con login (Xperience)','10','25','50','Ilimitados'],['Retención de logs de ejecución','7 días','30 días','30 días','365 días'],['Retención de audit logs','90 días','180 días','180 días','365 días']]
    limits_en = [['Managed processes','5','20','50','1,000'],['Parallel-running processes','5','20','50','200'],['Registerable robots','Unlimited','Unlimited','Unlimited','Unlimited'],['Development licenses (RPA Studio)','2','3','5','Unlimited'],['Process Control users','5','5','15','Unlimited'],['Login users (Xperience)','10','25','50','Unlimited'],['Execution log retention','7 days','30 days','30 days','365 days'],['Audit log retention','90 days','180 days','180 days','365 days']]
    limits_pt = [['Processos administrados','5','20','50','1.000'],['Processos em execução paralela','5','20','50','200'],['Robôs registráveis','Ilimitados','Ilimitados','Ilimitados','Ilimitados'],['Licenças de desenvolvimento (RPA Studio)','2','3','5','Ilimitadas'],['Usuários Process Control','5','5','15','Ilimitados'],['Usuários com login (Xperience)','10','25','50','Ilimitados'],['Retenção de logs de execução','7 dias','30 dias','30 dias','365 dias'],['Retenção de audit logs','90 dias','180 dias','180 dias','365 dias']]

    es = """
<h2>1. Objeto y alcance</h2>
<p>Este documento describe Rocketbot Orquestador ("el Orquestador"), incluyendo su módulo Xperience de formularios y portal self-service: capacidades funcionales, componentes, límites técnicos y condiciones por plan. No se comercializa como producto independiente; se contrata dentro de uno de los cinco planes de la Suite.</p>
<h2>2. Arquitectura y Process Control</h2>
<p>Opera bajo un modelo cliente-servidor: el servidor centraliza administración, scheduling, cola y persistencia, mientras los agentes instalados en hosts del Cliente ejecutan los robots asignados y reportan resultados. <strong>Process Control</strong> es la interfaz unificada de administración (single-instance): gestión de robots, agentes, calendarios, cola, usuarios, roles, logs, reportes y formularios de Xperience, sujeta al modelo RBAC de permisos.</p>
<h2>3. Gestión de robots, agentes y calendarización</h2>
<p>Publicación, versionado y etiquetado de robots en el repositorio central; registro, monitoreo y configuración de agentes (que operan sin límite cuantitativo — la capacidad efectiva la gobierna la cuota de procesos del plan). La calendarización admite expresiones cron, disparo por webhook, por finalización de otro robot o por envío de un formulario de Xperience.</p>
<h2>4. Cola, motor de ejecución y logs</h2>
<p>La cola encola, prioriza y asigna ejecuciones al agente disponible según reglas de tags, capacidad y prioridad (diseñadas por el Cliente). El Orquestador almacena de forma nativa cuatro tipos de log (Robot, Proceso, Usuario, Instancia) con registro obligatorio del dato de entrada y del componente donde ocurrió cada error, consultables desde Control Room o vía API. La retención depende del plan; para necesidades regulatorias mayores, el Cliente debe exportar logs periódicamente. <strong>El Orquestador no aplica de forma nativa integridad evidencial forense</strong> (firma digital, sellado de tiempo TSA) — cuando se requieran garantías probatorias formales, deben implementarse controles compensatorios externos.</p>
<h2>5. RBAC, repositorio y Xperience</h2>
<p>El control de accesos basado en roles opera a nivel de la instancia única de Process Control, con SSO Google/OAuth en todos los planes y Active Directory exclusivo de Corporate. El repositorio de robots es un almacén de artefactos (no reemplaza un sistema Git de control de versiones). <strong>Xperience</strong>, incluido en todos los planes, permite formularios públicos (sin login) o privados (con login y permisos por rol) cuyo envío dispara automáticamente una ejecución; no tiene límite cuantitativo propio — el límite real lo gobierna la cuota de procesos del plan, y el Cliente debe diseñar los formularios públicos evitando exposición de datos sensibles o disparo abusivo.</p>
<h2>6. Límites por plan</h2>
{limits_table}
<h2>7. Seguridad, integraciones y soporte</h2>
<p>2FA en todos los planes; SSO Google/OAuth en todos los planes y Active Directory en Corporate. El Orquestador es el proveedor único de identidad de la Suite. Comunicación TLS, almacén cifrado de credenciales de robots, y cifrado simétrico autenticado (Fernet/AES-128-CBC+HMAC-SHA256) de los pasos del robot en el repositorio, con rotación de claves vía MultiFernet. La API REST habilita integración con sistemas del Cliente bajo sus propios controles de autenticación. El soporte se define a nivel de Suite, con primera respuesta en minutos hábiles 5×8, evento 7×24 con costo adicional y meetup desde Standard.</p>
<h2>8. Responsabilidades y limitaciones</h2>
<p><strong>Del Cliente:</strong> dimensionar infraestructura y hosts de agentes; en modalidad on-premise, administrar SO, red y seguridad perimetral; gestionar credenciales y su rotación; diseñar robots y formularios evitando exposición de datos confidenciales; mantener actualizados los agentes; configurar RBAC con mínimo privilegio; exportar logs cuando la retención del plan sea insuficiente. <strong>Del proveedor:</strong> disponibilidad conforme al plan; actualizaciones y parches; aviso de mantenimientos; soporte técnico; cifrado en tránsito y en reposo según modalidad.</p>
<p>El Orquestador no provee de forma nativa ambientes DEV/QA/PROD separados dentro de una misma instancia ni control de versiones tipo Git sobre el código de los robots; estos controles, cuando se requieran, deben implementarse mediante instancias separadas o herramientas externas bajo administración del Cliente.</p>
<p><strong>La versión en español de este documento es la versión oficial</strong>; las traducciones existentes tienen carácter referencial.</p>
""".format(limits_table=table(PLAN_COLS, limits_es))

    en = """
<div class="rb-legal-note">{note}</div>
<h2>1. Purpose and scope</h2>
<p>This document describes Rocketbot Orchestrator ("the Orchestrator"), including its Xperience forms and self-service portal module: functional capabilities, components, technical limits and per-plan conditions. It is not sold as a standalone product; it is contracted within one of the Suite's five plans.</p>
<h2>2. Architecture and Process Control</h2>
<p>Operates on a client-server model: the server centralizes administration, scheduling, queueing and persistence, while agents installed on the Client's hosts run assigned robots and report results back. <strong>Process Control</strong> is the unified (single-instance) management interface: robots, agents, calendars, queue, users, roles, logs, reports and Xperience forms, all subject to the RBAC permission model.</p>
<h2>3. Robot, agent and scheduling management</h2>
<p>Publishing, versioning and tagging of robots in the central repository; registration, monitoring and configuration of agents (which register with no quantitative limit — effective capacity is governed by the plan's process quota). Scheduling supports cron expressions, webhook triggers, chaining on another robot's completion, or triggering on submission of an Xperience form.</p>
<h2>4. Queue, execution engine and logs</h2>
<p>The queue enqueues, prioritizes and assigns executions to the best-available agent according to tag, capacity and priority rules (designed by the Client). The Orchestrator natively stores four log types (Robot, Process, User, Instance) with mandatory recording of input data and of the component where each error occurred, queryable from Control Room or via API. Retention depends on the plan; for greater regulatory needs, the Client must periodically export logs. <strong>The Orchestrator does not natively apply forensic evidentiary integrity</strong> (digital signature, TSA timestamping) — where formal evidentiary guarantees are required, external compensating controls must be implemented.</p>
<h2>5. RBAC, repository and Xperience</h2>
<p>Role-based access control operates at the level of Process Control's single instance, with Google/OAuth SSO on every plan and Active Directory exclusive to Corporate. The robot repository is an artifact store (it does not replace a Git-style version-control system). <strong>Xperience</strong>, included on every plan, allows public forms (no login) or private forms (login and role-based permissions) whose submission automatically triggers an execution; it has no quantitative limit of its own — the real limit is governed by the plan's process quota, and the Client must design public forms to avoid exposing sensitive data or abusive triggering.</p>
<h2>6. Plan limits</h2>
{limits_table}
<h2>7. Security, integrations and support</h2>
<p>2FA on every plan; Google/OAuth SSO on every plan and Active Directory on Corporate. The Orchestrator is the Suite's single identity provider. TLS communication, an encrypted store for robot credentials, and authenticated symmetric encryption (Fernet / AES-128-CBC+HMAC-SHA256) of robot steps in the repository, with key rotation via MultiFernet. The REST API enables integration with Client systems under its own authentication controls. Support is defined at the Suite level, with first response in business-hour minutes (5×8), 24/7 event coverage at extra cost, and meetup support from Standard up.</p>
<h2>8. Responsibilities and limitations</h2>
<p><strong>Client:</strong> size infrastructure and agent hosts; in on-premise mode, administer the OS, network and perimeter security; manage credentials and their rotation; design robots and forms to avoid exposing confidential data; keep agents up to date; configure RBAC with least privilege; export logs when the plan's retention is insufficient. <strong>Provider:</strong> availability per the plan; updates and patches; maintenance notices; technical support; encryption in transit and at rest depending on deployment mode.</p>
<p>The Orchestrator does not natively provide separate DEV/QA/PROD environments within a single instance, nor Git-style version control over robot code; where required, these controls must be implemented via separate instances or external tools under Client administration.</p>
<p><strong>The Spanish-language version of this document is the official version</strong>; any existing translations are for reference only.</p>
""".format(note=LANG_NOTE['en'], limits_table=table(PLAN_COLS, limits_en))

    pt = """
<div class="rb-legal-note">{note}</div>
<h2>1. Objeto e escopo</h2>
<p>Este documento descreve o Rocketbot Orquestrador ("o Orquestrador"), incluindo seu módulo Xperience de formulários e portal self-service: capacidades funcionais, componentes, limites técnicos e condições por plano. Não é comercializado como produto independente; é contratado dentro de um dos cinco planos da Suite.</p>
<h2>2. Arquitetura e Process Control</h2>
<p>Opera sob um modelo cliente-servidor: o servidor centraliza administração, agendamento, fila e persistência, enquanto os agentes instalados nos hosts do Cliente executam os robôs atribuídos e reportam os resultados. O <strong>Process Control</strong> é a interface unificada de administração (instância única): gestão de robôs, agentes, calendários, fila, usuários, papéis, logs, relatórios e formulários do Xperience, sujeita ao modelo RBAC de permissões.</p>
<h2>3. Gestão de robôs, agentes e agendamento</h2>
<p>Publicação, versionamento e marcação de robôs no repositório central; registro, monitoramento e configuração de agentes (que se registram sem limite quantitativo — a capacidade efetiva é governada pela cota de processos do plano). O agendamento admite expressões cron, disparo por webhook, por conclusão de outro robô ou pelo envio de um formulário do Xperience.</p>
<h2>4. Fila, motor de execução e logs</h2>
<p>A fila enfileira, prioriza e atribui execuções ao agente disponível segundo regras de tags, capacidade e prioridade (definidas pelo Cliente). O Orquestrador armazena nativamente quatro tipos de log (Robô, Processo, Usuário, Instância) com registro obrigatório do dado de entrada e do componente onde ocorreu cada erro, consultáveis pelo Control Room ou via API. A retenção depende do plano; para necessidades regulatórias maiores, o Cliente deve exportar logs periodicamente. <strong>O Orquestrador não aplica nativamente integridade evidencial forense</strong> (assinatura digital, carimbo de tempo TSA) — quando forem exigidas garantias probatórias formais, devem ser implementados controles compensatórios externos.</p>
<h2>5. RBAC, repositório e Xperience</h2>
<p>O controle de acesso baseado em papéis opera no nível da instância única do Process Control, com SSO Google/OAuth em todos os planos e Active Directory exclusivo do Corporate. O repositório de robôs é um armazém de artefatos (não substitui um sistema Git de controle de versões). O <strong>Xperience</strong>, incluído em todos os planos, permite formulários públicos (sem login) ou privados (com login e permissões por papel) cujo envio dispara automaticamente uma execução; não tem limite quantitativo próprio — o limite real é governado pela cota de processos do plano, e o Cliente deve projetar os formulários públicos evitando exposição de dados sensíveis ou disparo abusivo.</p>
<h2>6. Limites por plano</h2>
{limits_table}
<h2>7. Segurança, integrações e suporte</h2>
<p>2FA em todos os planos; SSO Google/OAuth em todos os planos e Active Directory no Corporate. O Orquestrador é o provedor único de identidade da Suite. Comunicação TLS, armazenamento cifrado de credenciais de robôs, e criptografia simétrica autenticada (Fernet/AES-128-CBC+HMAC-SHA256) dos passos do robô no repositório, com rotação de chaves via MultiFernet. A API REST permite integração com sistemas do Cliente sob seus próprios controles de autenticação. O suporte é definido em nível de Suite, com primeira resposta em minutos do horário comercial 5×8, atendimento 7×24 com custo adicional e meetup a partir do Standard.</p>
<h2>8. Responsabilidades e limitações</h2>
<p><strong>Do Cliente:</strong> dimensionar infraestrutura e hosts de agentes; em modalidade on-premise, administrar SO, rede e segurança perimetral; gerenciar credenciais e sua rotação; projetar robôs e formulários evitando exposição de dados confidenciais; manter os agentes atualizados; configurar o RBAC com privilégio mínimo; exportar logs quando a retenção do plano for insuficiente. <strong>Do provedor:</strong> disponibilidade conforme o plano; atualizações e patches; aviso de manutenções; suporte técnico; criptografia em trânsito e em repouso conforme a modalidade.</p>
<p>O Orquestrador não fornece nativamente ambientes DEV/QA/PROD separados dentro de uma mesma instância, nem controle de versões tipo Git sobre o código dos robôs; esses controles, quando necessários, devem ser implementados por meio de instâncias separadas ou ferramentas externas sob administração do Cliente.</p>
<p><strong>A versão em espanhol deste documento é a versão oficial</strong>; as traduções existentes têm caráter referencial.</p>
""".format(note=LANG_NOTE['pt'], limits_table=table(PLAN_COLS, limits_pt))

    return {'es': es, 'en': en, 'pt': pt}


def content_ai():
    credit_rows_es = [['Créditos incluidos / año (sin rollover)','25.000.000','50.000.000','100.000.000','250.000.000'],['Modelo interno de AI Studio','Sí','Sí','Sí','Sí'],['Bring Your Own Model','No','Sí','Sí','Sí']]
    credit_rows_en = [['Credits included / year (no rollover)','25,000,000','50,000,000','100,000,000','250,000,000'],['AI Studio internal model','Yes','Yes','Yes','Yes'],['Bring Your Own Model','No','Yes','Yes','Yes']]
    credit_rows_pt = [['Créditos incluídos / ano (sem rollover)','25.000.000','50.000.000','100.000.000','250.000.000'],['Modelo interno do AI Studio','Sim','Sim','Sim','Sim'],['Bring Your Own Model','Não','Sim','Sim','Sim']]
    fmt_rows_es = [['Audio','MP3, WAV','25 MB por archivo'],['Imágenes','PNG, JPEG, JPG, WEBP, GIF (no animado)','10 MB por archivo'],['Documentos','PDF, TXT','25 MB por archivo'],['Correos','Gmail, Outlook, IMAP, POP3','25 MB por mensaje, incl. adjuntos']]
    fmt_rows_en = [['Audio','MP3, WAV','25 MB per file'],['Images','PNG, JPEG, JPG, WEBP, GIF (non-animated)','10 MB per file'],['Documents','PDF, TXT','25 MB per file'],['Emails','Gmail, Outlook, IMAP, POP3','25 MB per message, incl. attachments']]
    fmt_rows_pt = [['Áudio','MP3, WAV','25 MB por arquivo'],['Imagens','PNG, JPEG, JPG, WEBP, GIF (não animado)','10 MB por arquivo'],['Documentos','PDF, TXT','25 MB por arquivo'],['E-mails','Gmail, Outlook, IMAP, POP3','25 MB por mensagem, incl. anexos']]

    es = """
<h2>1. Objeto y alcance</h2>
<p>Este documento describe AI Studio, el componente de la Suite Rocketbot orientado al procesamiento inteligente de contenido no estructurado (correos, documentos, audio, imágenes) y su conversión en datos estructurados accionables mediante IA generativa, NLP y OCR. Se presta exclusivamente en modalidad SaaS: la infraestructura opera en AWS con integración a servicios de IA de Microsoft Azure (incluyendo OpenAI), y el Cliente accede vía navegador con conexión cifrada.</p>
<h2>2. Módulos de procesamiento</h2>
<p><strong>Email GPT</strong> conecta cuentas Gmail, Outlook, IMAP y POP3 (vía OAuth 2.0 para Gmail/Outlook), interpreta el cuerpo del correo por NLP y extrae campos definidos por el Cliente, disparando acciones posteriores. <strong>Documents GPT</strong> convierte PDF y TXT en información estructurada sin necesidad de entrenamiento previo; documentos escaneados sin texto embebido deben procesarse por Image GPT. <strong>Voice GPT</strong> transcribe audio (MP3/WAV, incluyendo notas de WhatsApp, máx. 25 MB) y extrae datos clave de la transcripción. <strong>Image GPT</strong> aplica OCR con IA sobre PNG, JPEG, JPG, WEBP y GIF no animado.</p>
{fmt_table}
<p>La precisión de cada módulo depende de la calidad del contenido fuente (resolución, ruido, estructura del documento). <strong>El contenido procesado por estos módulos es transmitido a los servicios de IA descritos en la sección 1</strong>; el Cliente debe considerar la naturaleza de dicho contenido, especialmente ante datos personales o información regulada, y obtener las autorizaciones necesarias de los titulares.</p>
<h2>3. Acciones y salidas</h2>
<p>Tras la extracción, AI Studio puede ejecutar acciones: visualización en Data View, envío/recepción por WhatsApp, envío de correo, integración con Rocketbot Xperience para disparar automatizaciones, o llamadas a APIs externas del Cliente (CRM, ERP, sistemas propietarios). La disponibilidad efectiva de cada canal depende de que el Cliente tenga contratados los servicios subyacentes (por ejemplo, WhatsApp Business API); AI Studio no responde por la disponibilidad de esos sistemas externos.</p>
<h2>4. Modelo de créditos</h2>
<p>AI Studio no se comercializa como producto independiente: los créditos se asignan como cuota anual dentro de cada plan de la Suite, sin acumulación al ciclo siguiente. Un crédito equivale a un carácter procesado por el modelo de IA (letras, números, símbolos y puntuación). El modelo interno de AI Studio está disponible en todos los planes; desde Standard, el Cliente puede además conectar su propio modelo externo (Bring Your Own Model, por ejemplo Azure OpenAI o Amazon Bedrock).</p>
{credit_table}
<p>El consumo real depende del contenido procesado; los reintentos por errores atribuibles al Cliente (contenido malformado, configuración incorrecta) pueden generar consumo adicional.</p>
<h2>5. Seguridad</h2>
<p>Comunicación HTTPS/TLS 1.2, autenticación JWT, filtrado de tráfico mediante WAF, gestión de credenciales sensibles mediante KMS, persistencia en Amazon RDS y aislamiento lógico entre tenants. Los tokens de acceso a proveedores externos (Gmail, Outlook, Drive) están sujetos a las políticas de seguridad de cada proveedor de identidad. <strong>Cuando el Cliente conecta un modelo de IA externo (Bring Your Own Model), el tratamiento y la seguridad de la información enviada quedan sujetos a los términos de ese proveedor</strong> — el proveedor de la Suite no responde por la seguridad de los datos ya transferidos fuera del entorno Rocketbot. El modelo interno de AI Studio, al operar dentro del entorno Rocketbot, no está alcanzado por esta exclusión.</p>
<h2>6. Soporte y responsabilidades</h2>
<p>El soporte se define a nivel de Suite (primera respuesta en minutos hábiles 5×8, evento 7×24 con costo adicional, meetup desde Standard) y no incluye, salvo pacto expreso, la definición de casos de uso ni el ajuste fino de instrucciones de extracción. <strong>Del Cliente:</strong> evaluar la naturaleza del contenido antes de su carga masiva; obtener consentimientos necesarios; gestionar y rotar credenciales de conexiones; validar la salida de los modelos antes de decisiones automáticas de alto impacto. <strong>Del proveedor:</strong> disponibilidad conforme al SLA; controles de seguridad de la sección 5; notificación de cambios materiales; documentación técnica actualizada.</p>
<h2>7. Limitaciones sobre resultados de IA</h2>
<p>Los resultados de los modelos de IA están sujetos a limitaciones inherentes: posibilidad de error en contenido ambiguo, variabilidad ante entradas similares, sesgos de los datos de entrenamiento y alucinaciones no fundamentadas en el contenido de entrada. El Cliente debe implementar controles de validación proporcionales al impacto de las decisiones automatizadas, incluyendo revisión humana (Human-in-the-Loop) en escenarios críticos. AI Studio no reemplaza sistemas de gestión documental, CRM o ERP, y sus salidas no deben interpretarse como consejo profesional (legal, contable, médico, financiero).</p>
<p><strong>La versión en español de este documento es la versión oficial</strong>; las traducciones existentes tienen carácter referencial.</p>
""".format(fmt_table=table(['Tipo','Formatos soportados','Límite'], fmt_rows_es), credit_table=table(PLAN_COLS, credit_rows_es))

    en = """
<div class="rb-legal-note">{note}</div>
<h2>1. Purpose and scope</h2>
<p>This document describes AI Studio, the Rocketbot Suite component focused on intelligent processing of unstructured content (emails, documents, audio, images) and its conversion into actionable structured data using generative AI, NLP and OCR. It is provided exclusively in SaaS mode: infrastructure runs on AWS with integration to Microsoft Azure AI services (including OpenAI), and the Client accesses it via browser over an encrypted connection.</p>
<h2>2. Processing modules</h2>
<p><strong>Email GPT</strong> connects Gmail, Outlook, IMAP and POP3 accounts (via OAuth 2.0 for Gmail/Outlook), interprets the email body with NLP and extracts Client-defined fields, triggering follow-up actions. <strong>Documents GPT</strong> converts PDF and TXT into structured information without prior training; scanned documents with no embedded text must be processed via Image GPT instead. <strong>Voice GPT</strong> transcribes audio (MP3/WAV, including WhatsApp voice notes, max. 25 MB) and extracts key data from the transcript. <strong>Image GPT</strong> applies AI-powered OCR to PNG, JPEG, JPG, WEBP and non-animated GIF.</p>
{fmt_table}
<p>Each module's accuracy depends on the quality of the source content (resolution, noise, document structure). <strong>Content processed by these modules is sent to the AI services described in section 1</strong>; the Client must consider the nature of that content, especially where personal data or regulated information is involved, and obtain the necessary consents from data subjects.</p>
<h2>3. Actions and outputs</h2>
<p>After extraction, AI Studio can execute actions: display in Data View, sending/receiving via WhatsApp, sending email, integration with Rocketbot Xperience to trigger automations, or calls to the Client's external APIs (CRM, ERP, proprietary systems). The effective availability of each channel depends on the Client having contracted the underlying services (e.g., WhatsApp Business API); AI Studio is not responsible for the availability of those external systems.</p>
<h2>4. Credit model</h2>
<p>AI Studio is not sold as a standalone product: credits are allocated as an annual quota within each Suite plan, with no rollover to the next cycle. One credit equals one character processed by the AI model (letters, numbers, symbols and punctuation). AI Studio's internal model is available on every plan; from Standard up, the Client may also connect its own external model (Bring Your Own Model, e.g. Azure OpenAI or Amazon Bedrock).</p>
{credit_table}
<p>Actual consumption depends on the content processed; retries caused by Client-attributable errors (malformed content, misconfigured tasks) may generate additional consumption.</p>
<h2>5. Security</h2>
<p>HTTPS/TLS 1.2 communication, JWT authentication, traffic filtering via WAF, sensitive-credential management via KMS, persistence on Amazon RDS, and logical tenant isolation. Access tokens for external providers (Gmail, Outlook, Drive) are subject to each identity provider's own security policies. <strong>When the Client connects an external AI model (Bring Your Own Model), the processing and security of the information sent are subject to that provider's terms</strong> — the Suite provider is not responsible for the security of data once transferred outside the Rocketbot environment. AI Studio's internal model, operating within the Rocketbot environment, is not subject to this exclusion.</p>
<h2>6. Support and responsibilities</h2>
<p>Support is defined at the Suite level (first response in business-hour minutes 5×8, 24/7 event coverage at extra cost, meetup support from Standard up) and does not include, absent express agreement, use-case definition or fine-tuning of extraction instructions. <strong>Client:</strong> assess the nature of content before bulk upload; obtain necessary consents; manage and rotate connection credentials; validate model output before high-impact automated decisions. <strong>Provider:</strong> availability per SLA; the security controls in section 5; notice of material changes; up-to-date technical documentation.</p>
<h2>7. Limitations on AI outputs</h2>
<p>AI model outputs are subject to inherent limitations: possible errors on ambiguous content, variability across similar inputs, biases from training data, and hallucinations not grounded in the input content. The Client must implement validation controls proportional to the impact of automated decisions, including human review (Human-in-the-Loop) in critical scenarios. AI Studio does not replace document-management, CRM or ERP systems, and its outputs should not be treated as professional advice (legal, accounting, medical, financial).</p>
<p><strong>The Spanish-language version of this document is the official version</strong>; any existing translations are for reference only.</p>
""".format(note=LANG_NOTE['en'], fmt_table=table(['Type','Supported formats','Limit'], fmt_rows_en), credit_table=table(PLAN_COLS, credit_rows_en))

    pt = """
<div class="rb-legal-note">{note}</div>
<h2>1. Objeto e escopo</h2>
<p>Este documento descreve o AI Studio, o componente da Suite Rocketbot voltado ao processamento inteligente de conteúdo não estruturado (e-mails, documentos, áudio, imagens) e sua conversão em dados estruturados acionáveis por meio de IA generativa, NLP e OCR. É fornecido exclusivamente em modalidade SaaS: a infraestrutura opera na AWS com integração a serviços de IA do Microsoft Azure (incluindo OpenAI), e o Cliente acessa via navegador com conexão criptografada.</p>
<h2>2. Módulos de processamento</h2>
<p>O <strong>Email GPT</strong> conecta contas Gmail, Outlook, IMAP e POP3 (via OAuth 2.0 para Gmail/Outlook), interpreta o corpo do e-mail por NLP e extrai campos definidos pelo Cliente, disparando ações posteriores. O <strong>Documents GPT</strong> converte PDF e TXT em informações estruturadas sem necessidade de treinamento prévio; documentos digitalizados sem texto incorporado devem ser processados pelo Image GPT. O <strong>Voice GPT</strong> transcreve áudio (MP3/WAV, incluindo áudios do WhatsApp, máx. 25 MB) e extrai dados-chave da transcrição. O <strong>Image GPT</strong> aplica OCR com IA em PNG, JPEG, JPG, WEBP e GIF não animado.</p>
{fmt_table}
<p>A precisão de cada módulo depende da qualidade do conteúdo de origem (resolução, ruído, estrutura do documento). <strong>O conteúdo processado por esses módulos é transmitido aos serviços de IA descritos na seção 1</strong>; o Cliente deve considerar a natureza desse conteúdo, especialmente diante de dados pessoais ou informações reguladas, e obter os consentimentos necessários dos titulares.</p>
<h2>3. Ações e saídas</h2>
<p>Após a extração, o AI Studio pode executar ações: visualização no Data View, envio/recebimento por WhatsApp, envio de e-mail, integração com o Rocketbot Xperience para disparar automações, ou chamadas a APIs externas do Cliente (CRM, ERP, sistemas próprios). A disponibilidade efetiva de cada canal depende de o Cliente ter contratado os serviços subjacentes (por exemplo, WhatsApp Business API); o AI Studio não se responsabiliza pela disponibilidade desses sistemas externos.</p>
<h2>4. Modelo de créditos</h2>
<p>O AI Studio não é comercializado como produto independente: os créditos são alocados como cota anual dentro de cada plano da Suite, sem acúmulo para o ciclo seguinte. Um crédito equivale a um caractere processado pelo modelo de IA (letras, números, símbolos e pontuação). O modelo interno do AI Studio está disponível em todos os planos; a partir do Standard, o Cliente também pode conectar seu próprio modelo externo (Bring Your Own Model, por exemplo Azure OpenAI ou Amazon Bedrock).</p>
{credit_table}
<p>O consumo real depende do conteúdo processado; novas tentativas causadas por erros atribuíveis ao Cliente (conteúdo malformado, configuração incorreta) podem gerar consumo adicional.</p>
<h2>5. Segurança</h2>
<p>Comunicação HTTPS/TLS 1.2, autenticação JWT, filtragem de tráfego via WAF, gestão de credenciais sensíveis via KMS, persistência no Amazon RDS e isolamento lógico entre tenants. Os tokens de acesso a provedores externos (Gmail, Outlook, Drive) estão sujeitos às políticas de segurança de cada provedor de identidade. <strong>Quando o Cliente conecta um modelo de IA externo (Bring Your Own Model), o tratamento e a segurança das informações enviadas ficam sujeitos aos termos desse provedor</strong> — o provedor da Suite não se responsabiliza pela segurança dos dados já transferidos para fora do ambiente Rocketbot. O modelo interno do AI Studio, por operar dentro do ambiente Rocketbot, não está sujeito a essa exclusão.</p>
<h2>6. Suporte e responsabilidades</h2>
<p>O suporte é definido em nível de Suite (primeira resposta em minutos do horário comercial 5×8, atendimento 7×24 com custo adicional, meetup a partir do Standard) e não inclui, salvo acordo expresso, a definição de casos de uso nem o ajuste fino de instruções de extração. <strong>Do Cliente:</strong> avaliar a natureza do conteúdo antes do carregamento em massa; obter os consentimentos necessários; gerenciar e rotacionar credenciais de conexões; validar a saída dos modelos antes de decisões automáticas de alto impacto. <strong>Do provedor:</strong> disponibilidade conforme o SLA; os controles de segurança da seção 5; notificação de mudanças materiais; documentação técnica atualizada.</p>
<h2>7. Limitações sobre resultados de IA</h2>
<p>Os resultados dos modelos de IA estão sujeitos a limitações inerentes: possibilidade de erro em conteúdo ambíguo, variabilidade diante de entradas semelhantes, vieses dos dados de treinamento e alucinações não fundamentadas no conteúdo de entrada. O Cliente deve implementar controles de validação proporcionais ao impacto das decisões automatizadas, incluindo revisão humana (Human-in-the-Loop) em cenários críticos. O AI Studio não substitui sistemas de gestão documental, CRM ou ERP, e suas saídas não devem ser interpretadas como aconselhamento profissional (jurídico, contábil, médico, financeiro).</p>
<p><strong>A versão em espanhol deste documento é a versão oficial</strong>; as traduções existentes têm caráter referencial.</p>
""".format(note=LANG_NOTE['pt'], fmt_table=table(['Tipo','Formatos suportados','Limite'], fmt_rows_pt), credit_table=table(PLAN_COLS, credit_rows_pt))

    return {'es': es, 'en': en, 'pt': pt}


def content_nexus():
    limits_es = [['Creators (Makers) incluidos','5','5','15','Ilimitados'],['End Users incluidos','10','25','50','Ilimitados'],['Aplicaciones','5','Ilimitadas','Ilimitadas','Ilimitadas'],['Filas máximas en base interna','50.000','500.000','500.000','Ilimitado'],['Tiempo máx. por Query','30 s','60 s','60 s','Configurable'],['Tiempo máx. por JS Function','10 s','30 s','30 s','Configurable'],['On-Premises Gateway','No','Sí','Sí','Sí'],['Retención de logs de ejecución','7 días','30 días','30 días','365 días']]
    limits_en = [['Creators (Makers) included','5','5','15','Unlimited'],['End Users included','10','25','50','Unlimited'],['Applications','5','Unlimited','Unlimited','Unlimited'],['Max. rows in internal DB','50,000','500,000','500,000','Unlimited'],['Max. time per Query','30 s','60 s','60 s','Configurable'],['Max. time per JS Function','10 s','30 s','30 s','Configurable'],['On-Premises Gateway','No','Yes','Yes','Yes'],['Execution log retention','7 days','30 days','30 days','365 days']]
    limits_pt = [['Creators (Makers) incluídos','5','5','15','Ilimitados'],['End Users incluídos','10','25','50','Ilimitados'],['Aplicações','5','Ilimitadas','Ilimitadas','Ilimitadas'],['Linhas máximas na base interna','50.000','500.000','500.000','Ilimitado'],['Tempo máx. por Query','30 s','60 s','60 s','Configurável'],['Tempo máx. por JS Function','10 s','30 s','30 s','Configurável'],['On-Premises Gateway','Não','Sim','Sim','Sim'],['Retenção de logs de execução','7 dias','30 dias','30 dias','365 dias']]
    action_rows_es = [['Query INSERT/UPDATE/DELETE','1 Action por ejecución'],['Query SELECT/COUNT','No consume'],['JS Function','1 Action por ejecución'],['API Call','1 Action por ejecución'],['MCP tool','1 Action por invocación'],['Acciones de UI (Show, Hide, Navigate, SetValue)','No consume']]
    action_rows_en = [['INSERT/UPDATE/DELETE Query','1 Action per execution'],['SELECT/COUNT Query','No consumption'],['JS Function','1 Action per execution'],['API Call','1 Action per execution'],['MCP tool','1 Action per invocation'],['UI actions (Show, Hide, Navigate, SetValue)','No consumption']]
    action_rows_pt = [['Query INSERT/UPDATE/DELETE','1 Action por execução'],['Query SELECT/COUNT','Não consome'],['JS Function','1 Action por execução'],['API Call','1 Action por execução'],['MCP tool','1 Action por invocação'],['Ações de UI (Show, Hide, Navigate, SetValue)','Não consome']]

    es = """
<h2>1. Objeto y alcance</h2>
<p>Este documento describe Nexus, la plataforma SaaS low-code de aplicaciones internas de la Suite Rocketbot: arquitectura, módulos, ediciones comerciales, límites técnicos y condiciones de uso. Nexus se comercializa como componente SaaS incluido en todos los planes de la Suite.</p>
<h2>2. Arquitectura</h2>
<p>Nexus es una aplicación web cliente-servidor: el frontend es una Single Page Application con el editor visual y el runtime de las apps publicadas; el backend expone una REST API, orquesta la ejecución de queries y funciones, y persiste la metadata en una base de datos relacional. Las entidades principales son: Application, Screen (con historial de versiones), AppTable, DataSource, Query, JsFunction, ApiCall y Action.</p>
<h2>3. Builder visual y catálogo de componentes</h2>
<p>Editor drag-and-drop sobre un grid de 12 columnas (restricción x + w ≤ 12, sin solapamiento), con panel de propiedades, panel de acciones, editor de código embebido y previsualización en tiempo real. El árbol de componentes se serializa como JSON y se versiona automáticamente; la edición simultánea de una misma pantalla sigue política de last-write-wins. Incluye más de 30 componentes preconstruidos (layout, input, display, data, chart, media, upload e invisibles). El componente Div admite HTML y JavaScript libres bajo responsabilidad del Cliente, sujeto a la Content Security Policy estricta de la plataforma.</p>
<h2>4. Data Sources, Queries y JS Functions</h2>
<p>Los Data Sources conectan bases internas, bases externas (MySQL, PostgreSQL, Supabase, Google Sheets, S3) y componentes de la Suite (Orquestador, Saturn Studio, y un Gateway On-Premises para fuentes detrás de firewall corporativo, sin apertura de puertos entrantes). Las credenciales se cifran en reposo y el backend nunca las devuelve en claro al frontend.</p>
<p>Las Queries son operaciones declarativas (SELECT, COUNT, INSERT, UPDATE, DELETE) con filtros parametrizables mediante bindings tipo mustache, ejecutadas siempre con prepared statements (inyección SQL no posible). Las JS Functions ejecutan código del Cliente en un sandbox de servidor con acceso controlado a helpers (params, query.execute, table.list, api.execute, $user, etc.), sin acceso a red directa, filesystem ni componentes del runtime fuera de dichos helpers.</p>
<h2>5. API, MCP Server e integraciones con la Suite</h2>
<p>Nexus expone una REST API completa (/api/v1), endpoints externos autenticados por API Key para integración headless (por ejemplo, con robots del Orquestador) y un servidor <strong>MCP</strong> (/mcp) que permite a clientes de IA (Claude Desktop, Cursor, etc.) crear y modificar aplicaciones mediante un conjunto controlado de tools. <strong>El uso del MCP Server implica que un cliente de IA externo puede modificar aplicaciones del Cliente</strong>; es responsabilidad del Cliente restringir el alcance de las MCP Keys emitidas y revisar las modificaciones antes de publicarlas en producción. Los data sources ROCKETBOT_ORCHESTRATOR y SATURN_STUDIO permiten integración directa con esos productos de la Suite.</p>
<h2>6. Límites por plan</h2>
{limits_table}
<h2>7. Modelo de facturación por Actions</h2>
<p>Nexus factura por Actions: una unidad de trabajo útil ejecutada por el sistema. Las lecturas (SELECT/COUNT) y las acciones puramente de UI no consumen; el consumo se produce solo cuando se ejecuta lógica de negocio.</p>
{action_table}
<p>El límite de Actions por mes es un límite duro: al alcanzarlo, la ejecución de nuevas Actions se suspende hasta la renovación del ciclo o el ascenso de plan — no existe facturación por sobreconsumo. Los reintentos por errores no controlados también consumen Actions, por lo que el Cliente debe diseñar queries y funciones robustas.</p>
<h2>8. Seguridad y responsabilidades</h2>
<p>Autenticación JWT en cookie HttpOnly (Secure, SameSite=Strict), SSO OAuth/OIDC configurable en Business y Enterprise (obligatorio en Enterprise), roles OWNER/ADMIN/MAKER/VIEWER, Content Security Policy estricta y rate limiting en todos los endpoints. <strong>Del Cliente:</strong> dimensionar el plan según Actions, apps y usuarios esperados; gestionar usuarios, roles, API Keys y MCP Keys con mínimo privilegio; custodiar y rotar credenciales de Data Sources; validar las salidas del MCP Server antes de publicarlas. <strong>Del proveedor:</strong> operar la infraestructura SaaS; aplicar los controles de seguridad; notificar cambios materiales; brindar soporte conforme al plan.</p>
<h2>9. Limitaciones</h2>
<p>Nexus <strong>no reemplaza sistemas ERP, CRM, HRIS</strong> ni sistemas transaccionales de misión crítica de alto volumen; <strong>no ofrece de forma nativa reporting avanzado tipo BI</strong> ni separación fuerte de ambientes DEV/QA/PROD dentro de un mismo tenant. El código de JS Functions y el HTML de componentes Div son responsabilidad del Cliente. Las salidas generadas por el MCP Server dependen del cliente de IA utilizado: Nexus no garantiza su corrección semántica.</p>
<p><strong>La versión en español de este documento es la versión oficial</strong>; las traducciones existentes tienen carácter referencial.</p>
""".format(limits_table=table(PLAN_COLS, limits_es), action_table=table(['Operación','Consumo'], action_rows_es))

    en = """
<div class="rb-legal-note">{note}</div>
<h2>1. Purpose and scope</h2>
<p>This document describes Nexus, the Rocketbot Suite's low-code SaaS platform for internal applications: architecture, modules, commercial editions, technical limits and conditions of use. Nexus is sold as a SaaS component included in every Suite plan.</p>
<h2>2. Architecture</h2>
<p>Nexus is a client-server web application: the frontend is a Single Page Application with the visual editor and the runtime for published apps; the backend exposes a REST API, orchestrates query and function execution, and persists metadata in a relational database. The main entities are: Application, Screen (with version history), AppTable, DataSource, Query, JsFunction, ApiCall and Action.</p>
<h2>3. Visual builder and component catalog</h2>
<p>A drag-and-drop editor over a 12-column grid (x + w ≤ 12 constraint, no overlap), with a properties panel, an actions panel, an embedded code editor and real-time preview. The component tree is serialized as JSON and versioned automatically; simultaneous editing of the same screen follows a last-write-wins policy. It includes 30+ prebuilt components (layout, input, display, data, chart, media, upload and invisible). The Div component allows free HTML and JavaScript at the Client's own responsibility, subject to the platform's strict Content Security Policy.</p>
<h2>4. Data Sources, Queries and JS Functions</h2>
<p>Data Sources connect internal databases, external databases (MySQL, PostgreSQL, Supabase, Google Sheets, S3) and Suite components (Orchestrator, Saturn Studio, and an On-Premises Gateway for sources behind a corporate firewall, with no inbound ports required). Credentials are encrypted at rest and the backend never returns them in plain text to the frontend.</p>
<p>Queries are declarative operations (SELECT, COUNT, INSERT, UPDATE, DELETE) with parameterizable filters via mustache-style bindings, always executed with prepared statements (SQL injection is not possible). JS Functions run Client code in a server-side sandbox with controlled access to helpers (params, query.execute, table.list, api.execute, $user, etc.), with no direct network access, filesystem access, or access to server runtime components outside those helpers.</p>
<h2>5. API, MCP Server and Suite integrations</h2>
<p>Nexus exposes a full REST API (/api/v1), API-Key-authenticated external endpoints for headless integration (e.g., with Orchestrator robots), and an <strong>MCP</strong> server (/mcp) that lets AI clients (Claude Desktop, Cursor, etc.) create and modify applications through a controlled set of tools. <strong>Using the MCP Server means an external AI client can modify the Client's applications</strong>; it is the Client's responsibility to restrict the scope of issued MCP Keys and review changes before publishing them to production. The ROCKETBOT_ORCHESTRATOR and SATURN_STUDIO data sources enable direct integration with those Suite products.</p>
<h2>6. Plan limits</h2>
{limits_table}
<h2>7. Actions-based billing model</h2>
<p>Nexus bills by Actions: a unit of useful work executed by the system. Reads (SELECT/COUNT) and purely UI actions do not consume; consumption only occurs when business logic actually runs.</p>
{action_table}
<p>The monthly Actions limit is a hard limit: once reached, execution of new Actions is suspended until the cycle renews or the plan is upgraded — there is no overage billing. Retries from uncontrolled errors also consume Actions, so the Client must design robust queries and functions.</p>
<h2>8. Security and responsibilities</h2>
<p>JWT authentication in an HttpOnly cookie (Secure, SameSite=Strict), configurable OAuth/OIDC SSO on Business and Enterprise (enforced on Enterprise), OWNER/ADMIN/MAKER/VIEWER roles, strict Content Security Policy and rate limiting on every endpoint. <strong>Client:</strong> size the plan to expected Actions, apps and users; manage users, roles, API Keys and MCP Keys under least privilege; safeguard and rotate Data Source credentials; validate MCP Server outputs before publishing them. <strong>Provider:</strong> operate the SaaS infrastructure; apply the security controls; notify material changes; provide support per the plan.</p>
<h2>9. Limitations</h2>
<p>Nexus <strong>does not replace ERP, CRM, HRIS</strong> or high-volume mission-critical transactional systems; <strong>it does not natively offer advanced BI-style reporting</strong> or strong separation of DEV/QA/PROD environments within a single tenant. JS Function code and Div component HTML are the Client's responsibility. Outputs generated by the MCP Server depend on the AI client used: Nexus does not guarantee their semantic correctness.</p>
<p><strong>The Spanish-language version of this document is the official version</strong>; any existing translations are for reference only.</p>
""".format(note=LANG_NOTE['en'], limits_table=table(PLAN_COLS, limits_en), action_table=table(['Operation','Consumption'], action_rows_en))

    pt = """
<div class="rb-legal-note">{note}</div>
<h2>1. Objeto e escopo</h2>
<p>Este documento descreve o Nexus, a plataforma SaaS low-code de aplicações internas da Suite Rocketbot: arquitetura, módulos, edições comerciais, limites técnicos e condições de uso. O Nexus é comercializado como componente SaaS incluído em todos os planos da Suite.</p>
<h2>2. Arquitetura</h2>
<p>O Nexus é uma aplicação web cliente-servidor: o frontend é uma Single Page Application com o editor visual e o runtime das aplicações publicadas; o backend expõe uma REST API, orquestra a execução de queries e funções, e persiste os metadados em um banco de dados relacional. As entidades principais são: Application, Screen (com histórico de versões), AppTable, DataSource, Query, JsFunction, ApiCall e Action.</p>
<h2>3. Builder visual e catálogo de componentes</h2>
<p>Editor drag-and-drop sobre uma grade de 12 colunas (restrição x + w ≤ 12, sem sobreposição), com painel de propriedades, painel de ações, editor de código incorporado e pré-visualização em tempo real. A árvore de componentes é serializada como JSON e versionada automaticamente; a edição simultânea de uma mesma tela segue política de last-write-wins. Inclui mais de 30 componentes pré-construídos (layout, input, display, data, chart, media, upload e invisíveis). O componente Div admite HTML e JavaScript livres sob responsabilidade do Cliente, sujeito à Content Security Policy estrita da plataforma.</p>
<h2>4. Data Sources, Queries e JS Functions</h2>
<p>Os Data Sources conectam bases internas, bases externas (MySQL, PostgreSQL, Supabase, Google Sheets, S3) e componentes da Suite (Orquestrador, Saturn Studio, e um Gateway On-Premises para fontes atrás de firewall corporativo, sem necessidade de abertura de portas de entrada). As credenciais são criptografadas em repouso e o backend nunca as retorna em texto simples ao frontend.</p>
<p>As Queries são operações declarativas (SELECT, COUNT, INSERT, UPDATE, DELETE) com filtros parametrizáveis via bindings estilo mustache, sempre executadas com prepared statements (injeção de SQL não é possível). As JS Functions executam código do Cliente em um sandbox de servidor com acesso controlado a helpers (params, query.execute, table.list, api.execute, $user, etc.), sem acesso direto à rede, ao sistema de arquivos, nem a componentes do runtime do servidor fora desses helpers.</p>
<h2>5. API, MCP Server e integrações com a Suite</h2>
<p>O Nexus expõe uma REST API completa (/api/v1), endpoints externos autenticados por API Key para integração headless (por exemplo, com robôs do Orquestrador) e um servidor <strong>MCP</strong> (/mcp) que permite a clientes de IA (Claude Desktop, Cursor, etc.) criar e modificar aplicações por meio de um conjunto controlado de tools. <strong>O uso do MCP Server implica que um cliente de IA externo pode modificar aplicações do Cliente</strong>; é responsabilidade do Cliente restringir o escopo das MCP Keys emitidas e revisar as modificações antes de publicá-las em produção. Os data sources ROCKETBOT_ORCHESTRATOR e SATURN_STUDIO permitem integração direta com esses produtos da Suite.</p>
<h2>6. Limites por plano</h2>
{limits_table}
<h2>7. Modelo de faturamento por Actions</h2>
<p>O Nexus fatura por Actions: uma unidade de trabalho útil executada pelo sistema. As leituras (SELECT/COUNT) e as ações puramente de UI não consomem; o consumo ocorre apenas quando a lógica de negócio é de fato executada.</p>
{action_table}
<p>O limite de Actions por mês é um limite rígido: ao ser atingido, a execução de novas Actions é suspensa até a renovação do ciclo ou o upgrade de plano — não há faturamento por consumo excedente. Novas tentativas por erros não controlados também consomem Actions, portanto o Cliente deve projetar queries e funções robustas.</p>
<h2>8. Segurança e responsabilidades</h2>
<p>Autenticação JWT em cookie HttpOnly (Secure, SameSite=Strict), SSO OAuth/OIDC configurável no Business e Enterprise (obrigatório no Enterprise), papéis OWNER/ADMIN/MAKER/VIEWER, Content Security Policy estrita e rate limiting em todos os endpoints. <strong>Do Cliente:</strong> dimensionar o plano conforme Actions, apps e usuários esperados; gerenciar usuários, papéis, API Keys e MCP Keys com privilégio mínimo; custodiar e rotacionar credenciais de Data Sources; validar as saídas do MCP Server antes de publicá-las. <strong>Do provedor:</strong> operar a infraestrutura SaaS; aplicar os controles de segurança; notificar mudanças materiais; prestar suporte conforme o plano.</p>
<h2>9. Limitações</h2>
<p>O Nexus <strong>não substitui sistemas ERP, CRM, HRIS</strong> nem sistemas transacionais de missão crítica de alto volume; <strong>não oferece nativamente relatórios avançados tipo BI</strong> nem separação forte de ambientes DEV/QA/PROD dentro de um mesmo tenant. O código das JS Functions e o HTML dos componentes Div são de responsabilidade do Cliente. As saídas geradas pelo MCP Server dependem do cliente de IA utilizado: o Nexus não garante sua correção semântica.</p>
<p><strong>A versão em espanhol deste documento é a versão oficial</strong>; as traduções existentes têm caráter referencial.</p>
""".format(note=LANG_NOTE['pt'], limits_table=table(PLAN_COLS, limits_pt), action_table=table(['Operação','Consumo'], action_rows_pt))

    return {'es': es, 'en': en, 'pt': pt}


CONTENT_FN = {
 'suite': content_suite,
 'saturn': content_saturn,
 'rpa': content_rpa,
 'orquestador': content_orquestador,
 'ai': content_ai,
 'nexus': content_nexus,
}

META_TXT = {
 'es': {'title':'Términos y condiciones técnicas | Rocketbot','desc':'Términos y condiciones técnicas de la Suite Rocketbot y de cada producto: Saturn Studio, RPA Studio, Orquestador, AI Studio y Nexus.'},
 'en': {'title':'Technical Terms & Conditions | Rocketbot','desc':'Technical terms and conditions for the Rocketbot Suite and each product: Saturn Studio, RPA Studio, Orchestrator, AI Studio and Nexus.'},
 'pt': {'title':'Termos e condições técnicas | Rocketbot','desc':'Termos e condições técnicas da Suite Rocketbot e de cada produto: Saturn Studio, RPA Studio, Orquestrador, AI Studio e Nexus.'},
}


def build_tabs(lang):
    out = []
    for i, p in enumerate(PRODUCTS):
        cls = 'rb-tyc-tab active' if i == 0 else 'rb-tyc-tab'
        out.append('      <button class="%s" data-tyc="%s" type="button">%s</button>' % (cls, p, TAB_LABEL[p][lang]))
    return '\n'.join(out)


def build_panels(lang):
    out = []
    contents = {p: CONTENT_FN[p]() for p in PRODUCTS}
    for i, p in enumerate(PRODUCTS):
        cls = 'rb-tyc-panel active' if i == 0 else 'rb-tyc-panel'
        meta = DOC_META[p]
        out.append("""    <div class="{cls}" id="tyc-{p}">
      <div class="rb-tyc-panel__head">
        <span class="rb-tyc-panel__eyebrow">T&amp;C · {name}</span>
        <div class="rb-tyc-panel__meta">{ver_label} {version}</div>
      </div>
      <div class="rb-legal">
{content}
      </div>
    </div>""".format(cls=cls, p=p, name=meta['name'][lang], version=meta['version'],
                      ver_label={'es':'Versión','en':'Version','pt':'Versão'}[lang],
                      content=contents[p][lang]))
    return '\n'.join(out)


def build_main(lang, t):
    return """<!-- CONTACT PAGE -->
<!-- ======================= T&C ======================= -->
<main class="rb-tycpg">

  <section class="rb-tycpg-hero">
    <div class="container">
      <span class="rb-eyebrow"><span class="dot"></span>{eyebrow}</span>
      <h1 class="rb-tycpg-hero__title">{h1}</h1>
      <p class="rb-tycpg-hero__sub">{sub}</p>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="rb-tyc-tabs">
{tabs}
      </div>
{panels}
    </div>
  </section>

</main>

<!-- FOOTER -->""".format(eyebrow=t['eyebrow'], h1=t['h1'], sub=t['sub'], tabs=build_tabs(lang), panels=build_panels(lang))


SECTION_RE = re.compile(r'<!-- CONTACT PAGE -->.*?<!-- FOOTER -->', re.S)
TITLE_RE = re.compile(r'<title>.*?</title>', re.S)


def sub_attr(src, prop, value):
    pat = re.compile(r'(<meta (?:name|property)="' + re.escape(prop) + r'" content=")[^"]*(">)')
    return pat.sub(lambda m: m.group(1) + value + m.group(2), src)


def build(lang, folder):
    src = io.open(os.path.join(folder, 'contacto.html'), encoding='utf-8').read()
    t = META[lang]
    txt = META_TXT[lang]

    src = SECTION_RE.sub(lambda m: build_main(lang, t), src, count=1)

    src = TITLE_RE.sub('<title>' + txt['title'] + '</title>', src, count=1)
    src = sub_attr(src, 'description', txt['desc'])
    src = sub_attr(src, 'og:title', txt['title'])
    src = sub_attr(src, 'og:description', txt['desc'])
    src = sub_attr(src, 'twitter:title', txt['title'])
    src = sub_attr(src, 'twitter:description', txt['desc'])

    src = src.replace('content="noindex, follow"', 'content="index, follow"')

    slug = 'terminos-y-condiciones'
    src = src.replace('rocketbot.com/contacto"', 'rocketbot.com/%s"' % slug)
    src = src.replace('rocketbot.com/en/contacto"', 'rocketbot.com/en/%s"' % slug)
    src = src.replace('rocketbot.com/pt/contacto"', 'rocketbot.com/pt/%s"' % slug)

    src = src.replace('"@type": "ContactPage"', '"@type": "WebPage"')

    src = src.replace("PAGE='contacto.html'", "PAGE='%s.html'" % slug)

    if 'rb-tyc-css' not in src:
        src = src.replace('</head>', TYC_CSS + '</head>', 1)
    if 'rb-tyc-tab[data-tyc]' not in src:
        src = src.replace('</body>', TYC_JS + '</body>', 1)

    out = os.path.join(folder, slug + '.html')
    io.open(out, 'w', encoding='utf-8', newline='\n').write(src)
    print('  escrito %s (%s)' % (out, lang))


def main():
    for lang, folder in (('es', ROOT), ('en', os.path.join(ROOT, 'en')), ('pt', os.path.join(ROOT, 'pt'))):
        build(lang, folder)
    print('listo.')


if __name__ == '__main__':
    main()
