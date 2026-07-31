# -*- coding: utf-8 -*-
"""
Genera politicas-de-privacidad.html y politicas-de-seguridad.html (es/en/pt)
a partir del shell de contacto.html, igual que build_partners.py / build_faq.py.

Contenido extraido y traducido de:
  http://3.148.198.21/es/politicas-de-privacidad/
  http://3.148.198.21/es/politicas-de-seguridad/
(fuente unica en espanol; en/pt son traduccion, no version legal oficial).

    python build_legal.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

LEGAL_CSS = """
<style id="rb-legal-css">
.rb-legalpg{padding-top:72px;}
.rb-legalpg-hero{padding:72px 0 40px;text-align:center;}
.rb-legalpg-hero .container{max-width:760px;}
.rb-legalpg-hero__title{font-size:clamp(28px,4vw,44px);font-weight:900;letter-spacing:-.03em;margin:20px 0 10px;}
.rb-legalpg-hero__meta{font-size:13.5px;opacity:.55;}
.rb-legal{max-width:820px;margin:0 auto;padding:0 0 96px;}
.rb-legal h2{font-size:clamp(20px,2.4vw,26px);font-weight:800;letter-spacing:-.01em;margin:44px 0 16px;color:var(--rb-red);}
.rb-legal h2:first-child{margin-top:0;}
.rb-legal h3{font-size:17px;font-weight:700;margin:28px 0 12px;color:var(--foreground);}
.rb-legal p{font-size:15px;line-height:1.75;color:var(--foreground);opacity:.82;margin:0 0 14px;}
.rb-legal ul{margin:0 0 14px;padding-left:22px;list-style:disc;}
.rb-legal li{font-size:15px;line-height:1.7;color:var(--foreground);opacity:.82;margin-bottom:8px;}
.rb-legal li::marker{color:var(--rb-red);}
.rb-legal strong{color:var(--foreground);opacity:1;}
</style>
"""

# ── PRIVACIDAD ───────────────────────────────────────────────────────────
PRIV = {
'es': """
<h2>I. Política de privacidad y protección de datos personales</h2>
<p>El sitio web WWW.ROCKETBOT.COM, en adelante «ROCKETBOT», «WWW.ROCKETBOT.COM» o «el sitio web» indistintamente, pone en conocimiento de las personas que hagan uso del mismo, en adelante «personas usuarias», la presente política de privacidad y protección de los datos personales.</p>
<p>Esta política de privacidad y protección de los datos personales forma parte de los Términos y Condiciones Generales de Uso del sitio web WWW.ROCKETBOT.COM.</p>
<p>La lectura de la misma le permitirá a las personas usuarias conocer el modo en que ROCKETBOT recolecta, trata y protege sus datos personales. El acceso, uso y permanencia en el sitio web implica la aceptación de la presente política de privacidad.</p>
<p>De particular importancia resultan la aplicación de la Ley N.º 19.628 de Protección de Datos Personales y la Ley N.º 19.496 sobre Derechos del Consumidor. Esta política, en lo que no contraviene la legislación chilena, está adaptada al Reglamento Europeo de Protección de Datos (RGPD).</p>
<h3>1. Definiciones</h3>
<ul>
<li><strong>Almacenamiento de datos:</strong> conservación o custodia de datos en un registro, banco o base de datos.</li>
<li><strong>Dato estadístico:</strong> aquel que en su origen, o como consecuencia de su tratamiento, no puede ser asociado a un titular identificado o identificable.</li>
<li><strong>Datos de carácter personal o datos personales:</strong> aquellos relativos a cualquier información concerniente a personas naturales, identificadas o identificables.</li>
<li><strong>Datos sensibles:</strong> aquellos datos personales que se refieren a las características físicas o morales de las personas o a hechos o circunstancias de su vida privada o intimidad, tales como los hábitos personales, el origen racial, las ideologías y opiniones políticas, las creencias o convicciones religiosas, los estados de salud físicos o psíquicos y la vida sexual.</li>
<li><strong>Registro, banco o base de datos:</strong> conjunto organizado de datos de carácter personal, sea automatizado o no, que permita relacionar los datos entre sí, así como realizar todo tipo de tratamiento de datos.</li>
<li><strong>Responsable del registro, banco o base de datos:</strong> la persona natural o jurídica a quien compete las decisiones relacionadas con el tratamiento de los datos de carácter personal.</li>
<li><strong>Titular de los datos:</strong> persona natural a la que se refieren los datos de carácter personal.</li>
<li><strong>Tratamiento de datos:</strong> cualquier operación o procedimiento técnico, automatizado o no, que permita recolectar, almacenar, grabar, organizar, elaborar, seleccionar, extraer, confrontar, interconectar, disociar, comunicar, ceder, transferir, transmitir o cancelar datos de carácter personal, o utilizarlos en cualquier otra forma.</li>
</ul>
<h3>2. Principios aplicables al tratamiento de los datos personales</h3>
<p>ROCKETBOT trata los datos personales conforme a los principios de licitud, finalidad, proporcionalidad, calidad, seguridad y responsabilidad establecidos en la Ley N.º 19.628, aplicando las definiciones descritas en la sección anterior a cada tratamiento que realiza.</p>
<h3>3. Responsable del registro, banco o base de datos</h3>
<p>La persona responsable del tratamiento de los datos personales recogidos a través del sitio web ROCKETBOT es SOLUCIONES INFORMÁTICAS ROCKET NOT, Rol Único Tributario N.º 76.945.322-9, representada por JUAN JORGE HERRERA WAGENKNECHT, cédula nacional de identidad N.º 10.302.205-3, en adelante, la responsable del tratamiento.</p>
<p>Los datos para tomar contacto con la persona responsable son:</p>
<ul>
<li>Correo electrónico: jjherrera@rocketbot.com</li>
<li>Dirección: Dr. Barros Borgoño 246</li>
</ul>
<h3>4. Recolección y registro de datos de carácter personal y finalidad de su tratamiento</h3>
<p>Los datos personales obtenidos por ROCKETBOT mediante los formularios extendidos en sus páginas quedarán incorporados y serán tratados en nuestras bases de datos con el fin de facilitar, agilizar y cumplir los compromisos establecidos entre ROCKETBOT y las personas usuarias, mantener la relación que se establezca en los formularios que éstas rellenen, o atender una solicitud o consulta de las mismas.</p>
<p>En concreto, los datos de las personas usuarias serán obtenidos por ROCKETBOT a través de las siguientes acciones:</p>
<ul>
<li>Formularios de mensaje o contacto</li>
<li>Descarga de licencias</li>
<li>Cookies de sitios</li>
</ul>
<h3>5. Categoría de datos personales</h3>
<p>Las categorías de datos que se tratan en ROCKETBOT son únicamente datos identificativos. En ningún caso se tratan categorías de datos personales de carácter sensible, como el estado de salud de las personas o sus opiniones políticas o creencias religiosas.</p>
<p>No pueden ser objeto de tratamiento los datos sensibles, salvo cuando la ley lo autorice, exista consentimiento de la persona titular de dichos datos o éstos sean necesarios para la determinación u otorgamiento de beneficios de salud que correspondan a sus titulares.</p>
<h3>6. Base legal para el tratamiento de los datos personales</h3>
<p>El tratamiento de los datos personales solamente puede efectuarse cuando la ley lo autorice o el titular consienta expresamente en ello. ROCKETBOT se compromete a recabar el consentimiento expreso, escrito y verificable de la persona usuaria respecto de los datos personales de los que es titular, para el tratamiento de dichos datos para uno o varios fines específicos, debidamente informados. También se informará de la posible comunicación al público de los datos almacenados y tratados.</p>
<p>No requiere autorización el tratamiento de datos personales que provengan o se recolecten de fuentes accesibles al público, cuando sean de carácter económico, financiero, bancario o comercial, se contengan en listados relativos a una categoría de personas que se limiten a indicar antecedentes tales como la pertenencia del individuo a ese grupo, su profesión o actividad, sus títulos educativos, dirección o fecha de nacimiento, o sean necesarios para comunicaciones comerciales de respuesta directa o comercialización o venta directa de bienes o servicios.</p>
<p>Tampoco requerirá de esta autorización el tratamiento de datos personales que realicen personas jurídicas privadas para el uso exclusivo suyo, de sus asociados y de las entidades a que están afiliadas, con fines estadísticos, de tarificación u otros de beneficio general de aquéllos.</p>
<p>Los datos personales deben utilizarse solamente para los fines para los cuales hubieren sido recolectados, salvo que provengan o se hayan recolectado de fuentes accesibles al público. No pueden ser objeto de tratamiento los datos sensibles, salvo cuando la ley lo autorice, exista consentimiento del titular o sean datos necesarios para la determinación u otorgamiento de beneficios de salud que correspondan a sus titulares.</p>
<p>La persona usuaria tendrá derecho a retirar su consentimiento en cualquier momento. Será tan fácil retirar el consentimiento como darlo. Como regla general, el retiro del consentimiento no condicionará el uso del sitio web.</p>
<p>En las ocasiones en las que la persona usuaria deba o pueda facilitar sus datos a través de formularios para realizar consultas, solicitar información o por motivos relacionados con el contenido del sitio web, se le informará en caso de que la cumplimentación de alguno de ellos sea obligatoria debido a que sean imprescindibles para el correcto desarrollo de la operación realizada.</p>
<h3>7. Período de retención de los datos personales</h3>
<p>Los datos personales solamente serán retenidos durante el tiempo mínimo necesario para los fines de su tratamiento y, en todo caso, únicamente durante el siguiente plazo: 1 año, o hasta que la persona usuaria solicite su supresión.</p>
<p>En el momento en que se obtengan los datos personales se informará a la persona usuaria sobre el plazo durante el cual se conservarán los datos personales o, cuando eso no sea posible, los criterios utilizados para determinar este plazo.</p>
<h3>8. Destinatarios de los datos personales</h3>
<p>Los datos personales de las personas usuarias no serán compartidos, vendidos, cedidos, arrendados, comercializados o transmitidos de modo alguno con terceras personas, salvo en los casos que la ley lo exija.</p>
<h3>9. Datos personales de menores de edad</h3>
<p>Solamente las personas mayores de 14 años podrán otorgar su consentimiento para el tratamiento de sus datos personales de forma lícita por ROCKETBOT.</p>
<p>Si se trata de una persona menor de 14 años será necesario el consentimiento de los padres o representantes legales o de quien tiene a su cargo el cuidado personal del niño o niña, salvo que expresamente lo autorice o mandate la ley.</p>
<p>Los datos sensibles de las personas adolescentes menores de 16 años solamente se podrán tratar con el consentimiento otorgado por sus padres o representantes legales o quien tiene a su cargo el cuidado personal del menor, salvo que expresamente lo autorice o mandate la ley.</p>
<h3>10. Secreto y seguridad de los datos personales</h3>
<p>ROCKETBOT se compromete a adoptar las medidas técnicas y organizativas necesarias, según el nivel de seguridad adecuado al riesgo de los datos recogidos, de forma que se garantice la seguridad de los datos de carácter personal y se evite la destrucción, pérdida o alteración accidental o ilícita de datos personales transmitidos, conservados o tratados de otra forma, o la comunicación o acceso no autorizado a dichos datos.</p>
<p>El sitio web WWW.ROCKETBOT.COM cuenta con un certificado SSL (Secure Socket Layer), que asegura que los datos personales se transmiten de forma segura y confidencial entre el servidor y la persona usuaria, totalmente cifrada o encriptada.</p>
<p>Sin embargo, debido a que ROCKETBOT no puede garantizar la inexpugnabilidad de internet ni la ausencia total de accesos fraudulentos a los datos personales, la persona responsable del tratamiento se compromete a comunicar a las personas usuarias, sin dilación indebida, la ocurrencia de cualquier violación de la seguridad de los datos personales que sea probable que entrañe un alto riesgo para los derechos y libertades de las personas físicas.</p>
<p>Los datos personales serán tratados como confidenciales por la persona responsable del tratamiento, quien se compromete a garantizar, por medio de una obligación legal o contractual, que dicha confidencialidad sea respetada por sus empleados, asociados y toda persona a la cual le haga accesible la información.</p>
<h3>11. Derechos derivados del tratamiento de los datos personales</h3>
<p>La persona usuaria podrá ejercer frente a la persona responsable del tratamiento los siguientes derechos:</p>
<ul>
<li><strong>Derecho de acceso:</strong> obtener confirmación de si ROCKETBOT está tratando o no sus datos personales y, en caso afirmativo, obtener información sobre sus datos concretos y del tratamiento realizado.</li>
<li><strong>Derecho de rectificación:</strong> a que se modifiquen sus datos personales que resulten inexactos o incompletos.</li>
<li><strong>Derecho de supresión (el derecho al olvido):</strong> a obtener la supresión de sus datos personales cuando éstos ya no sean necesarios para los fines para los cuales fueron recogidos, cuando se haya retirado el consentimiento, cuando hayan sido tratados ilícitamente, o cuando deban suprimirse en cumplimiento de una obligación legal.</li>
<li>Si los datos suprimidos o rectificados hubieren sido comunicados previamente a terceros determinados o determinables, la persona responsable deberá avisarles a la brevedad posible la operación efectuada.</li>
<li>No podrá pedirse la rectificación, supresión o bloqueo de datos personales almacenados por mandato legal, fuera de los casos contemplados en la ley respectiva.</li>
<li><strong>Derecho a la limitación del tratamiento:</strong> a limitar el tratamiento de sus datos personales cuando impugne su exactitud, el tratamiento sea ilícito, el responsable ya no los necesite pero la persona usuaria los necesite para reclamaciones, o se haya opuesto al tratamiento.</li>
<li><strong>Derecho a la portabilidad de los datos:</strong> a recibir sus datos personales en un formato estructurado, de uso común y lectura mecánica, y a transmitirlos a otro responsable.</li>
<li><strong>Derecho de oposición:</strong> a que no se lleve a cabo el tratamiento de sus datos personales o se cese el tratamiento de los mismos.</li>
<li><strong>Derecho a no ser objeto de una decisión basada únicamente en el tratamiento automatizado</strong>, incluida la elaboración de perfiles, salvo que la legislación vigente establezca lo contrario.</li>
</ul>
<p>La persona usuaria podrá ejercitar sus derechos mediante comunicación escrita dirigida a la persona responsable del tratamiento, conforme lo establece el artículo 16 de la Ley N.º 19.628.</p>
<h3>12. Reclamaciones ante la autoridad de control</h3>
<p>En caso de que la persona usuaria considere que existe un problema o infracción de la normativa vigente en la forma en la que se están tratando sus datos personales, tendrá derecho a ejercer las acciones que estime pertinentes ante los Tribunales de Justicia.</p>
<h3>13. Datos obtenidos por API</h3>
<p>Las llamadas a API como la API de Google Workspace no se utilizan para desarrollar, mejorar o entrenar modelos generalizados de IA y/o aprendizaje automático.</p>
<h2>II. Política de cookies</h2>
<p>El acceso a este sitio web puede implicar la utilización de cookies. Las cookies son pequeñas cantidades de información que se almacenan en el navegador utilizado por cada persona usuaria para que el servidor recuerde cierta información que posteriormente, y únicamente el servidor que la implementó, leerá. Las cookies facilitan la navegación, la hacen más amigable y no dañan el dispositivo de navegación.</p>
<p>La información recolectada a través de las cookies puede incluir la fecha y hora de visitas del sitio web, las páginas visionadas, el tiempo que se ha estado en el sitio web y los sitios visitados justo antes y después del mismo. Ninguna cookie permite contactar con el número de teléfono de la persona usuaria ni extraer información del disco duro o robar información personal; la única manera de que información privada forme parte de una cookie es que la persona usuaria se la proporcione directamente al servidor.</p>
<p>Las cookies que permiten identificar a una persona se consideran datos personales, por lo que les es aplicable la política de privacidad descrita anteriormente. Para su utilización será necesario el consentimiento de la persona usuaria, comunicado en base a una elección auténtica, ofrecido mediante una afirmación positiva, antes del tratamiento inicial, removible y documentado.</p>
<h3>1. Cookies propias</h3>
<p>Son aquellas cookies que son enviadas al dispositivo de la persona usuaria y gestionadas exclusivamente por ROCKETBOT para el mejor funcionamiento del sitio web. La información recabada se emplea para mejorar la calidad del sitio, su contenido y la experiencia de la persona usuaria, permitiendo reconocerla como visitante recurrente y adaptar el contenido a sus preferencias.</p>
<h3>2. Cookies de terceros</h3>
<p>Son cookies utilizadas y gestionadas por entidades externas que proporcionan a ROCKETBOT servicios solicitados por éste para mejorar su sitio web y la experiencia de navegación. Se utilizan principalmente para obtener estadísticas de accesos y analizar cómo interactúa la persona usuaria con el sitio web: número de páginas visitadas, idioma, ubicación aproximada por dirección IP, frecuencia y reincidencia de las visitas, tiempo de visita, navegador, operador o tipo de dispositivo. La información se recopila de forma anónima y se elaboran informes de tendencias sin identificar a personas usuarias individuales. Las cookies de terceros utilizadas por este sitio web son proporcionadas por:</p>
<ul>
<li>Facebook</li>
<li>LinkedIn</li>
<li>Google</li>
</ul>
<p>Puede obtener más información sobre las cookies y consultar el tipo de cookies utilizadas, sus principales características y período de expiración en los siguientes enlaces: facebook.com/policies/cookies · policies.google.com/privacy · linkedin.com/legal/cookie-policy. Las entidades encargadas del suministro de cookies podrán ceder esta información a terceros cuando lo exija la ley o sea un tercero quien procese esta información para dichas entidades.</p>
<h3>3. Cookies de redes sociales</h3>
<p>ROCKETBOT incorpora plugins de redes sociales que permiten acceder a ellas desde el sitio web, por lo que sus cookies pueden almacenarse en el navegador de la persona usuaria. Las titulares de dichas redes sociales disponen de sus propias políticas de protección de datos y de cookies, siendo ellas mismas responsables de sus propios ficheros y prácticas de privacidad. Se recomienda consultar directamente las políticas de Facebook, X/Twitter, Instagram, YouTube, Google, LinkedIn, Pinterest y TikTok.</p>
<h3>4. Deshabilitar, rechazar y eliminar cookies</h3>
<p>La persona usuaria puede deshabilitar, rechazar y eliminar las cookies, total o parcialmente, instaladas en su dispositivo mediante la configuración de su navegador (Chrome, Firefox, Safari, entre otros). Los procedimientos para rechazar y eliminar cookies pueden diferir de un navegador a otro, por lo que se recomienda acudir a las instrucciones facilitadas por el navegador utilizado. En caso de rechazar el uso de cookies, total o parcialmente, la persona usuaria podrá seguir usando el sitio web, aunque podrá tener limitada la utilización de algunas de sus prestaciones.</p>
<h2>III. Aceptación y cambio de esta política de privacidad</h2>
<p>Es necesario que la persona usuaria haya leído y esté conforme con las condiciones sobre la protección de datos de carácter personal contenidas en esta política de privacidad y de cookies, y que acepte el tratamiento de sus datos personales para que la persona responsable del tratamiento pueda proceder al mismo en la forma, durante los plazos y para las finalidades indicadas. El uso del sitio web implica la aceptación de esta política.</p>
<p>ROCKETBOT se reserva el derecho a modificar su política de privacidad y de cookies de acuerdo a su propio criterio, o motivado por un cambio legislativo o jurisprudencial. Los cambios o actualizaciones serán puestos en conocimiento de la persona usuaria. Se recomienda consultar esta página de forma periódica para estar al tanto de los últimos cambios.</p>
<p>Esta política de privacidad y de cookies fue elaborada el día 1 de octubre de 2021 y se encuentra actualizada para adaptarse a la legislación vigente.</p>
""",
'en': """
<h2>I. Privacy policy and personal data protection</h2>
<p>The website WWW.ROCKETBOT.COM, hereinafter «ROCKETBOT», «WWW.ROCKETBOT.COM» or «the website», informs the people who use it, hereinafter «users», of this privacy and personal data protection policy.</p>
<p>This privacy and personal data protection policy forms part of the General Terms and Conditions of Use of the WWW.ROCKETBOT.COM website.</p>
<p>Reading it allows users to understand how ROCKETBOT collects, processes and protects their personal data. Accessing, using and remaining on the website implies acceptance of this privacy policy.</p>
<p>Of particular importance is the application of Chilean Law No. 19.628 on Personal Data Protection and Law No. 19.496 on Consumer Rights. Insofar as it does not contravene Chilean law, this policy is adapted to the European General Data Protection Regulation (GDPR).</p>
<h3>1. Definitions</h3>
<ul>
<li><strong>Data storage:</strong> the preservation or custody of data in a register, bank or database.</li>
<li><strong>Statistical data:</strong> data that, in its origin or as a result of its processing, cannot be associated with an identified or identifiable data subject.</li>
<li><strong>Personal data:</strong> any information concerning identified or identifiable natural persons.</li>
<li><strong>Sensitive data:</strong> personal data referring to the physical or moral characteristics of individuals, or to facts or circumstances of their private life, such as personal habits, racial origin, political ideologies and opinions, religious beliefs, physical or mental health, and sexual life.</li>
<li><strong>Register, bank or database:</strong> an organized set of personal data, whether automated or not, that allows the data to be related to each other and allows any type of data processing.</li>
<li><strong>Data controller:</strong> the natural or legal person responsible for decisions related to the processing of personal data.</li>
<li><strong>Data subject:</strong> the natural person to whom the personal data refers.</li>
<li><strong>Data processing:</strong> any technical operation or procedure, automated or not, that allows personal data to be collected, stored, recorded, organized, prepared, selected, extracted, compared, interconnected, dissociated, communicated, assigned, transferred, transmitted or deleted, or used in any other way.</li>
</ul>
<h3>2. Principles applicable to the processing of personal data</h3>
<p>ROCKETBOT processes personal data in accordance with the principles of lawfulness, purpose limitation, proportionality, quality, security and accountability established in Law No. 19.628, applying the definitions described in the previous section to every processing activity it carries out.</p>
<h3>3. Data controller</h3>
<p>The party responsible for processing the personal data collected through the ROCKETBOT website is SOLUCIONES INFORMÁTICAS ROCKET NOT, Tax ID No. 76.945.322-9, represented by JUAN JORGE HERRERA WAGENKNECHT, national ID No. 10.302.205-3, hereinafter the data controller.</p>
<p>Contact details for the data controller:</p>
<ul>
<li>Email: jjherrera@rocketbot.com</li>
<li>Address: Dr. Barros Borgoño 246</li>
</ul>
<h3>4. Collection and recording of personal data and purpose of processing</h3>
<p>Personal data obtained by ROCKETBOT through the forms available on its pages will be incorporated into and processed in our databases in order to facilitate, expedite and fulfill the commitments established between ROCKETBOT and users, maintain the relationship established through the forms users fill out, or respond to a request or query.</p>
<p>Specifically, user data is obtained by ROCKETBOT through the following actions:</p>
<ul>
<li>Message or contact forms</li>
<li>License downloads</li>
<li>Site cookies</li>
</ul>
<h3>5. Category of personal data</h3>
<p>The categories of data processed by ROCKETBOT are exclusively identifying data. Sensitive categories of personal data, such as a person's health status or their political opinions or religious beliefs, are never processed.</p>
<p>Sensitive data may not be processed, except when authorized by law, when the data subject has consented, or when such data is necessary to determine or grant health benefits to the data subjects.</p>
<h3>6. Legal basis for processing personal data</h3>
<p>Personal data may only be processed when authorized by law or when the data subject expressly consents. ROCKETBOT undertakes to obtain the express, written and verifiable consent of the user regarding the personal data of which they are the subject, for processing that data for one or more specific, duly informed purposes. Users will also be informed of any possible public disclosure of the data stored and processed.</p>
<p>No authorization is required to process personal data that comes from or is collected from publicly accessible sources, when it is of an economic, financial, banking or commercial nature, is contained in lists relating to a category of persons limited to indicating background information such as the individual's membership in that group, their profession or activity, educational qualifications, address or date of birth, or is necessary for direct-response commercial communications or the direct marketing or sale of goods or services.</p>
<p>Nor is this authorization required for the processing of personal data carried out by private legal entities for their own exclusive use, that of their associates, and of the entities to which they are affiliated, for statistical, billing or other purposes of general benefit to them.</p>
<p>Personal data must be used only for the purposes for which it was collected, unless it came from or was collected from publicly accessible sources. Sensitive data may not be processed except when authorized by law, when the data subject has consented, or when such data is necessary to determine or grant health benefits.</p>
<p>Users have the right to withdraw their consent at any time. Withdrawing consent must be as easy as giving it. As a general rule, withdrawing consent will not condition the use of the website.</p>
<p>Whenever users must or may provide their data through forms to make inquiries, request information, or for reasons related to the content of the website, they will be informed if completing any of the fields is mandatory because it is essential for the correct performance of the operation carried out.</p>
<h3>7. Retention period of personal data</h3>
<p>Personal data will only be retained for the minimum time necessary for the purposes of its processing and, in any case, only for the following period: 1 year, or until the user requests its deletion.</p>
<p>At the time personal data is obtained, users will be informed of the period during which the data will be kept or, when that is not possible, the criteria used to determine that period.</p>
<h3>8. Recipients of personal data</h3>
<p>Users' personal data will not be shared, sold, assigned, leased, marketed or transmitted in any way to third parties, except in cases required by law.</p>
<h3>9. Personal data of minors</h3>
<p>Only persons over 14 years of age may lawfully give their consent for ROCKETBOT to process their personal data.</p>
<p>For persons under 14 years of age, the consent of parents, legal representatives, or whoever is responsible for the child's personal care will be required, unless expressly authorized or mandated by law.</p>
<p>Sensitive data of adolescents under 16 years of age may only be processed with the consent granted by their parents, legal representatives, or whoever is responsible for the minor's personal care, unless expressly authorized or mandated by law.</p>
<h3>10. Confidentiality and security of personal data</h3>
<p>ROCKETBOT undertakes to adopt the necessary technical and organizational measures, according to the level of security appropriate to the risk of the data collected, so as to guarantee the security of personal data and prevent its accidental or unlawful destruction, loss or alteration, whether transmitted, stored or otherwise processed, or unauthorized disclosure of or access to such data.</p>
<p>The WWW.ROCKETBOT.COM website has an SSL (Secure Socket Layer) certificate, which ensures that personal data is transmitted securely and confidentially, fully encrypted, between the server and the user.</p>
<p>However, because ROCKETBOT cannot guarantee the impregnability of the internet or the total absence of fraudulent access to personal data, the data controller undertakes to notify users, without undue delay, of the occurrence of any personal data security breach likely to pose a high risk to the rights and freedoms of natural persons.</p>
<p>Personal data will be treated as confidential by the data controller, who undertakes to guarantee, through a legal or contractual obligation, that such confidentiality is respected by its employees, associates and anyone to whom it makes the information accessible.</p>
<h3>11. Rights arising from the processing of personal data</h3>
<p>Users may exercise the following rights against the data controller:</p>
<ul>
<li><strong>Right of access:</strong> to obtain confirmation of whether or not ROCKETBOT is processing their personal data and, if so, to obtain information about their specific data and the processing carried out.</li>
<li><strong>Right of rectification:</strong> to have inaccurate or incomplete personal data corrected.</li>
<li><strong>Right of erasure (the "right to be forgotten"):</strong> to obtain the deletion of personal data when it is no longer necessary for the purposes for which it was collected, when consent has been withdrawn, when it has been unlawfully processed, or when it must be deleted to comply with a legal obligation.</li>
<li>If deleted or rectified data had previously been disclosed to identified or identifiable third parties, the data controller must notify them of the change as soon as possible.</li>
<li>Rectification, deletion or blocking of personal data stored by legal mandate may not be requested, outside the cases contemplated in the relevant law.</li>
<li><strong>Right to restriction of processing:</strong> to obtain restriction of processing when the accuracy of the data is contested, the processing is unlawful, the controller no longer needs the data but the user needs it for legal claims, or the user has objected to the processing.</li>
<li><strong>Right to data portability:</strong> to receive personal data in a structured, commonly used, machine-readable format and to transmit it to another controller.</li>
<li><strong>Right to object:</strong> to prevent or stop the processing of personal data.</li>
<li><strong>Right not to be subject to a decision based solely on automated processing</strong>, including profiling, unless current legislation provides otherwise.</li>
</ul>
<p>Users may exercise their rights through written communication addressed to the data controller, as established in Article 16 of Law No. 19.628.</p>
<h3>12. Complaints to the supervisory authority</h3>
<p>If users believe there is a problem or a breach of current regulations in the way their personal data is being processed, they have the right to take whatever action they deem appropriate before the Courts of Justice.</p>
<h3>13. Data obtained through APIs</h3>
<p>API calls, such as the Google Workspace API, are not used to develop, improve or train generalized AI and/or machine learning models.</p>
<h2>II. Cookie policy</h2>
<p>Accessing this website may involve the use of cookies. Cookies are small pieces of information stored in the browser used by each user, so that the server can remember certain information which only the server that implemented it will later read. Cookies make browsing easier, more user-friendly, and do not damage the browsing device.</p>
<p>Information collected through cookies may include the date and time of visits to the website, pages viewed, time spent on the website, and sites visited immediately before and after it. No cookie allows contacting a user's phone number, extracting information from their hard drive, or stealing personal information; the only way private information can become part of a cookie is if the user provides it directly to the server.</p>
<p>Cookies that allow a person to be identified are considered personal data, so the privacy policy described above applies to them. Their use requires the user's consent, communicated based on a genuine choice, given through a positive affirmative statement, prior to initial processing, revocable and documented.</p>
<h3>1. First-party cookies</h3>
<p>These are cookies sent to the user's device and managed exclusively by ROCKETBOT for the proper functioning of the website. The information gathered is used to improve the quality of the website, its content and the user's experience, allowing recurring visitors to be recognized and content to be adapted to their preferences.</p>
<h3>2. Third-party cookies</h3>
<p>These are cookies used and managed by external entities that provide ROCKETBOT with services it has requested to improve its website and the browsing experience. They are mainly used to obtain access statistics and analyze how users interact with the website: number of pages visited, language, approximate location based on IP address, frequency and recurrence of visits, time spent, browser, carrier or type of device. Information is collected anonymously and trend reports are produced without identifying individual users. Third-party cookies used by this website are provided by:</p>
<ul>
<li>Facebook</li>
<li>LinkedIn</li>
<li>Google</li>
</ul>
<p>You can find more information about cookies, and review the type of cookies used, their main characteristics and expiration period, at: facebook.com/policies/cookies · policies.google.com/privacy · linkedin.com/legal/cookie-policy. Entities responsible for providing cookies may share this information with third parties when required by law or when a third party processes this information on their behalf.</p>
<h3>3. Social media cookies</h3>
<p>ROCKETBOT includes social media plugins that allow access to those networks from the website, so their cookies may be stored in the user's browser. The owners of those social networks have their own data protection and cookie policies and are themselves responsible for their own files and privacy practices. Users should refer directly to the policies of Facebook, X/Twitter, Instagram, YouTube, Google, LinkedIn, Pinterest and TikTok.</p>
<h3>4. Disabling, rejecting and deleting cookies</h3>
<p>Users can disable, reject and delete cookies installed on their device, wholly or partially, through their browser settings (Chrome, Firefox, Safari, among others). The procedures to reject and delete cookies may differ from one browser to another, so it is recommended to follow the instructions provided by the browser being used. If a user rejects the use of cookies, wholly or partially, they may continue using the website, although the use of some of its features may be limited.</p>
<h2>III. Acceptance and modification of this privacy policy</h2>
<p>Users must have read and agreed to the personal data protection terms contained in this privacy and cookie policy, and must accept the processing of their personal data so that the data controller can carry it out in the manner, for the periods and for the purposes indicated. Use of the website implies acceptance of this policy.</p>
<p>ROCKETBOT reserves the right to modify its privacy and cookie policy according to its own criteria, or motivated by a legislative or case-law change. Changes or updates will be brought to the user's attention. Users are encouraged to periodically check this page to stay informed of the latest changes.</p>
<p>This privacy and cookie policy was drafted on October 1, 2021, and is kept up to date to comply with current legislation.</p>
""",
'pt': """
<h2>I. Política de privacidade e proteção de dados pessoais</h2>
<p>O site WWW.ROCKETBOT.COM, doravante «ROCKETBOT», «WWW.ROCKETBOT.COM» ou «o site», informa às pessoas que o utilizam, doravante «usuários», a presente política de privacidade e proteção de dados pessoais.</p>
<p>Esta política de privacidade e proteção de dados pessoais faz parte dos Termos e Condições Gerais de Uso do site WWW.ROCKETBOT.COM.</p>
<p>A leitura desta política permite aos usuários conhecer como a ROCKETBOT coleta, trata e protege seus dados pessoais. O acesso, uso e permanência no site implicam a aceitação desta política de privacidade.</p>
<p>Destacam-se a aplicação da Lei chilena n.º 19.628 de Proteção de Dados Pessoais e da Lei n.º 19.496 sobre Direitos do Consumidor. Esta política, no que não contraria a legislação chilena, está adaptada ao Regulamento Europeu de Proteção de Dados (RGPD).</p>
<h3>1. Definições</h3>
<ul>
<li><strong>Armazenamento de dados:</strong> conservação ou custódia de dados em um registro, banco ou base de dados.</li>
<li><strong>Dado estatístico:</strong> aquele que, em sua origem ou como consequência de seu tratamento, não pode ser associado a um titular identificado ou identificável.</li>
<li><strong>Dados de caráter pessoal ou dados pessoais:</strong> qualquer informação relativa a pessoas naturais, identificadas ou identificáveis.</li>
<li><strong>Dados sensíveis:</strong> dados pessoais referentes às características físicas ou morais das pessoas, ou a fatos ou circunstâncias de sua vida privada ou intimidade, tais como hábitos pessoais, origem racial, ideologias e opiniões políticas, crenças ou convicções religiosas, estado de saúde física ou psíquica e vida sexual.</li>
<li><strong>Registro, banco ou base de dados:</strong> conjunto organizado de dados de caráter pessoal, automatizado ou não, que permita relacionar os dados entre si e realizar qualquer tipo de tratamento de dados.</li>
<li><strong>Responsável pelo registro, banco ou base de dados:</strong> a pessoa natural ou jurídica a quem cabem as decisões relacionadas ao tratamento dos dados pessoais.</li>
<li><strong>Titular dos dados:</strong> pessoa natural a quem se referem os dados pessoais.</li>
<li><strong>Tratamento de dados:</strong> qualquer operação ou procedimento técnico, automatizado ou não, que permita coletar, armazenar, gravar, organizar, elaborar, selecionar, extrair, confrontar, interconectar, dissociar, comunicar, ceder, transferir, transmitir ou cancelar dados pessoais, ou utilizá-los de qualquer outra forma.</li>
</ul>
<h3>2. Princípios aplicáveis ao tratamento de dados pessoais</h3>
<p>A ROCKETBOT trata os dados pessoais de acordo com os princípios de licitude, finalidade, proporcionalidade, qualidade, segurança e responsabilidade estabelecidos na Lei n.º 19.628, aplicando as definições descritas na seção anterior a cada tratamento realizado.</p>
<h3>3. Responsável pelo registro, banco ou base de dados</h3>
<p>A pessoa responsável pelo tratamento dos dados pessoais coletados através do site ROCKETBOT é SOLUCIONES INFORMÁTICAS ROCKET NOT, CNPJ/RUT n.º 76.945.322-9, representada por JUAN JORGE HERRERA WAGENKNECHT, documento de identidade n.º 10.302.205-3, doravante a responsável pelo tratamento.</p>
<p>Dados de contato da pessoa responsável:</p>
<ul>
<li>E-mail: jjherrera@rocketbot.com</li>
<li>Endereço: Dr. Barros Borgoño 246</li>
</ul>
<h3>4. Coleta e registro de dados pessoais e finalidade do tratamento</h3>
<p>Os dados pessoais obtidos pela ROCKETBOT por meio dos formulários disponíveis em suas páginas serão incorporados e tratados em nossas bases de dados com o objetivo de facilitar, agilizar e cumprir os compromissos estabelecidos entre a ROCKETBOT e os usuários, manter a relação estabelecida nos formulários preenchidos por eles, ou atender a uma solicitação ou consulta.</p>
<p>Especificamente, os dados dos usuários são obtidos pela ROCKETBOT através das seguintes ações:</p>
<ul>
<li>Formulários de mensagem ou contato</li>
<li>Download de licenças</li>
<li>Cookies do site</li>
</ul>
<h3>5. Categoria de dados pessoais</h3>
<p>As categorias de dados tratadas pela ROCKETBOT são unicamente dados identificativos. Em nenhum caso são tratadas categorias de dados pessoais sensíveis, como o estado de saúde das pessoas ou suas opiniões políticas ou crenças religiosas.</p>
<p>Os dados sensíveis não podem ser objeto de tratamento, salvo quando a lei o autorizar, exista consentimento do titular dos dados, ou sejam necessários para a determinação ou concessão de benefícios de saúde aos seus titulares.</p>
<h3>6. Base legal para o tratamento de dados pessoais</h3>
<p>O tratamento de dados pessoais somente pode ser realizado quando a lei o autorizar ou o titular consentir expressamente. A ROCKETBOT compromete-se a obter o consentimento expresso, escrito e verificável do usuário em relação aos dados pessoais dos quais é titular, para o tratamento desses dados para uma ou várias finalidades específicas, devidamente informadas. Também será informada a possível comunicação ao público dos dados armazenados e tratados.</p>
<p>Não é necessária autorização para o tratamento de dados pessoais provenientes ou coletados de fontes acessíveis ao público, quando forem de caráter econômico, financeiro, bancário ou comercial, estiverem contidos em listas relativas a uma categoria de pessoas limitadas a indicar informações como a pertença do indivíduo a esse grupo, sua profissão ou atividade, seus títulos educacionais, endereço ou data de nascimento, ou sejam necessários para comunicações comerciais de resposta direta ou comercialização ou venda direta de bens ou serviços.</p>
<p>Também não será necessária essa autorização para o tratamento de dados pessoais realizado por pessoas jurídicas privadas para uso exclusivo próprio, de seus associados e das entidades às quais estão afiliadas, com fins estatísticos, de tarifação ou outros de benefício geral.</p>
<p>Os dados pessoais devem ser utilizados apenas para os fins para os quais foram coletados, salvo se provierem ou tiverem sido coletados de fontes acessíveis ao público. Os dados sensíveis não podem ser objeto de tratamento, salvo quando a lei o autorizar, exista consentimento do titular, ou sejam necessários para a determinação ou concessão de benefícios de saúde.</p>
<p>O usuário terá direito de retirar seu consentimento a qualquer momento. Será tão fácil retirar o consentimento quanto concedê-lo. Como regra geral, a retirada do consentimento não condicionará o uso do site.</p>
<p>Nas ocasiões em que o usuário deva ou possa fornecer seus dados por meio de formulários para realizar consultas, solicitar informações ou por motivos relacionados ao conteúdo do site, será informado caso o preenchimento de algum campo seja obrigatório por ser imprescindível para o correto desenvolvimento da operação realizada.</p>
<h3>7. Período de retenção dos dados pessoais</h3>
<p>Os dados pessoais serão retidos apenas pelo tempo mínimo necessário para os fins de seu tratamento e, em todo caso, unicamente pelo seguinte prazo: 1 ano, ou até que o usuário solicite sua exclusão.</p>
<p>No momento em que os dados pessoais forem obtidos, o usuário será informado sobre o prazo durante o qual os dados serão conservados ou, quando isso não for possível, os critérios utilizados para determinar esse prazo.</p>
<h3>8. Destinatários dos dados pessoais</h3>
<p>Os dados pessoais dos usuários não serão compartilhados, vendidos, cedidos, alugados, comercializados ou transmitidos de qualquer forma a terceiros, exceto nos casos exigidos por lei.</p>
<h3>9. Dados pessoais de menores de idade</h3>
<p>Somente pessoas maiores de 14 anos poderão dar seu consentimento para o tratamento lícito de seus dados pessoais pela ROCKETBOT.</p>
<p>Tratando-se de pessoa menor de 14 anos, será necessário o consentimento dos pais ou representantes legais, ou de quem tenha a seu cargo o cuidado pessoal da criança, salvo autorização ou determinação expressa da lei.</p>
<p>Os dados sensíveis de adolescentes menores de 16 anos somente poderão ser tratados com o consentimento concedido por seus pais ou representantes legais, ou por quem tenha a seu cargo o cuidado pessoal do menor, salvo autorização ou determinação expressa da lei.</p>
<h3>10. Sigilo e segurança dos dados pessoais</h3>
<p>A ROCKETBOT compromete-se a adotar as medidas técnicas e organizacionais necessárias, de acordo com o nível de segurança adequado ao risco dos dados coletados, de forma a garantir a segurança dos dados pessoais e evitar a destruição, perda ou alteração acidental ou ilícita de dados pessoais transmitidos, conservados ou tratados de outra forma, ou a comunicação ou acesso não autorizado a esses dados.</p>
<p>O site WWW.ROCKETBOT.COM conta com um certificado SSL (Secure Socket Layer), que garante que os dados pessoais sejam transmitidos de forma segura e confidencial, totalmente criptografados, entre o servidor e o usuário.</p>
<p>No entanto, como a ROCKETBOT não pode garantir a inexpugnabilidade da internet nem a ausência total de acessos fraudulentos aos dados pessoais, a responsável pelo tratamento compromete-se a comunicar aos usuários, sem demora indevida, a ocorrência de qualquer violação de segurança de dados pessoais que provavelmente acarrete alto risco para os direitos e liberdades das pessoas físicas.</p>
<p>Os dados pessoais serão tratados como confidenciais pela responsável pelo tratamento, que se compromete a garantir, por meio de obrigação legal ou contratual, que essa confidencialidade seja respeitada por seus funcionários, associados e qualquer pessoa a quem torne a informação acessível.</p>
<h3>11. Direitos decorrentes do tratamento de dados pessoais</h3>
<p>O usuário poderá exercer perante a responsável pelo tratamento os seguintes direitos:</p>
<ul>
<li><strong>Direito de acesso:</strong> obter confirmação sobre se a ROCKETBOT trata ou não seus dados pessoais e, em caso afirmativo, obter informações sobre seus dados específicos e o tratamento realizado.</li>
<li><strong>Direito de retificação:</strong> que sejam modificados seus dados pessoais inexatos ou incompletos.</li>
<li><strong>Direito de exclusão (o "direito ao esquecimento"):</strong> obter a exclusão de seus dados pessoais quando já não forem necessários para os fins para os quais foram coletados, quando o consentimento tiver sido retirado, quando tiverem sido tratados ilicitamente, ou quando devam ser excluídos em cumprimento de uma obrigação legal.</li>
<li>Se os dados excluídos ou retificados tiverem sido previamente comunicados a terceiros determinados ou determináveis, a responsável deverá avisá-los o quanto antes sobre a operação realizada.</li>
<li>Não poderá ser solicitada a retificação, exclusão ou bloqueio de dados pessoais armazenados por determinação legal, fora dos casos previstos na lei respectiva.</li>
<li><strong>Direito à limitação do tratamento:</strong> limitar o tratamento de seus dados pessoais quando contestar sua exatidão, o tratamento for ilícito, a responsável já não precisar dos dados mas o usuário precisar deles para reivindicações, ou tiver se oposto ao tratamento.</li>
<li><strong>Direito à portabilidade dos dados:</strong> receber seus dados pessoais em formato estruturado, de uso comum e leitura mecânica, e transmiti-los a outra responsável.</li>
<li><strong>Direito de oposição:</strong> que não seja realizado o tratamento de seus dados pessoais ou que ele seja interrompido.</li>
<li><strong>Direito de não ser objeto de uma decisão baseada unicamente no tratamento automatizado</strong>, incluindo a elaboração de perfis, salvo se a legislação vigente estabelecer o contrário.</li>
</ul>
<p>O usuário poderá exercer seus direitos mediante comunicação escrita dirigida à responsável pelo tratamento, conforme estabelece o artigo 16 da Lei n.º 19.628.</p>
<h3>12. Reclamações perante a autoridade de controle</h3>
<p>Caso o usuário considere que existe um problema ou infração à normativa vigente na forma como seus dados pessoais estão sendo tratados, terá direito de exercer as ações que julgar pertinentes perante os Tribunais de Justiça.</p>
<h3>13. Dados obtidos por API</h3>
<p>As chamadas a APIs, como a API do Google Workspace, não são utilizadas para desenvolver, aprimorar ou treinar modelos generalizados de IA e/ou aprendizado de máquina.</p>
<h2>II. Política de cookies</h2>
<p>O acesso a este site pode implicar a utilização de cookies. Cookies são pequenas quantidades de informação armazenadas no navegador utilizado por cada usuário, para que o servidor lembre certas informações que, posteriormente, apenas o servidor que as implementou lerá. Os cookies facilitam a navegação, tornam-na mais amigável e não danificam o dispositivo de navegação.</p>
<p>As informações coletadas por meio de cookies podem incluir a data e a hora das visitas ao site, as páginas visualizadas, o tempo de permanência no site e os sites visitados imediatamente antes e depois dele. Nenhum cookie permite contato com o número de telefone do usuário nem extrair informações do disco rígido ou roubar informações pessoais; a única forma de informações privadas fazerem parte de um cookie é o próprio usuário fornecê-las diretamente ao servidor.</p>
<p>Os cookies que permitem identificar uma pessoa são considerados dados pessoais, sendo-lhes aplicável a política de privacidade descrita anteriormente. Para sua utilização, será necessário o consentimento do usuário, comunicado com base em uma escolha autêntica, manifestado por meio de uma afirmação positiva, antes do tratamento inicial, revogável e documentado.</p>
<h3>1. Cookies próprios</h3>
<p>São aqueles cookies enviados ao dispositivo do usuário e gerenciados exclusivamente pela ROCKETBOT para o melhor funcionamento do site. As informações coletadas são utilizadas para melhorar a qualidade do site, seu conteúdo e a experiência do usuário, permitindo reconhecê-lo como visitante recorrente e adaptar o conteúdo às suas preferências.</p>
<h3>2. Cookies de terceiros</h3>
<p>São cookies utilizados e gerenciados por entidades externas que prestam à ROCKETBOT serviços solicitados por ela para melhorar seu site e a experiência de navegação. São utilizados principalmente para obter estatísticas de acesso e analisar como o usuário interage com o site: número de páginas visitadas, idioma, localização aproximada por endereço IP, frequência e recorrência das visitas, tempo de visita, navegador, operadora ou tipo de dispositivo. As informações são coletadas de forma anônima e são elaborados relatórios de tendências sem identificar usuários individuais. Os cookies de terceiros utilizados por este site são fornecidos por:</p>
<ul>
<li>Facebook</li>
<li>LinkedIn</li>
<li>Google</li>
</ul>
<p>Você pode obter mais informações sobre os cookies e consultar o tipo de cookies utilizados, suas principais características e período de expiração em: facebook.com/policies/cookies · policies.google.com/privacy · linkedin.com/legal/cookie-policy. As entidades responsáveis pelo fornecimento de cookies poderão ceder essas informações a terceiros quando exigido por lei ou quando um terceiro processar essas informações em seu nome.</p>
<h3>3. Cookies de redes sociais</h3>
<p>A ROCKETBOT incorpora plugins de redes sociais que permitem acessá-las a partir do site, motivo pelo qual seus cookies podem ser armazenados no navegador do usuário. As titulares dessas redes sociais possuem suas próprias políticas de proteção de dados e cookies, sendo elas mesmas responsáveis por seus próprios arquivos e práticas de privacidade. Recomenda-se consultar diretamente as políticas do Facebook, X/Twitter, Instagram, YouTube, Google, LinkedIn, Pinterest e TikTok.</p>
<h3>4. Desativar, rejeitar e excluir cookies</h3>
<p>O usuário pode desativar, rejeitar e excluir os cookies instalados em seu dispositivo, total ou parcialmente, por meio das configurações de seu navegador (Chrome, Firefox, Safari, entre outros). Os procedimentos para rejeitar e excluir cookies podem variar de um navegador para outro, por isso recomenda-se seguir as instruções fornecidas pelo navegador utilizado. Caso rejeite o uso de cookies, total ou parcialmente, o usuário poderá continuar utilizando o site, embora a utilização de algumas de suas funcionalidades possa ficar limitada.</p>
<h2>III. Aceitação e alteração desta política de privacidade</h2>
<p>É necessário que o usuário tenha lido e esteja de acordo com as condições sobre a proteção de dados pessoais contidas nesta política de privacidade e cookies, e que aceite o tratamento de seus dados pessoais para que a responsável pelo tratamento possa realizá-lo na forma, pelos prazos e para as finalidades indicadas. O uso do site implica a aceitação desta política.</p>
<p>A ROCKETBOT reserva-se o direito de modificar sua política de privacidade e cookies de acordo com seu próprio critério, ou motivada por uma mudança legislativa ou jurisprudencial. As alterações ou atualizações serão levadas ao conhecimento do usuário. Recomenda-se consultar esta página periodicamente para se manter informado sobre as últimas alterações.</p>
<p>Esta política de privacidade e cookies foi elaborada em 1º de outubro de 2021 e é mantida atualizada para se adaptar à legislação vigente.</p>
""",
}

# ── SEGURIDAD ────────────────────────────────────────────────────────────
SEC = {
'es': """
<p>La Seguridad de la Información en Rocketbot es parte fundamental del negocio para así entregar confianza a nuestros clientes y usuarios sobre las tecnologías de la información que operamos. La data, con base en nuestra clasificación de la información, es gestionada con los más altos estándares según las mejores prácticas disponibles en el mercado, lo cual es una base para nuestro crecimiento y sustentabilidad organizacional.</p>
<p>La Seguridad de la Información en Rocketbot es posible dado el compromiso de la alta dirección, que promueve una cultura de mejora continua, facilitando los recursos y herramientas necesarias.</p>
<p>La alta dirección entiende y atiende la importancia y beneficios de mantenerse en cumplimiento, no solo con los requerimientos de ISO 27001 y mejores prácticas de seguridad, sino además con otros requisitos legales, contractuales y gubernamentales relevantes para el contexto de la organización.</p>
<p>Como parte de este compromiso, la alta dirección establece y respalda los siguientes objetivos de seguridad de la información, alineados al SGSI y a la estrategia organizacional:</p>
<ul>
<li>Implementar controles de vigilancia continua que permitan identificar y reportar el 100% de las amenazas críticas detectadas en los sistemas de información.</li>
<li>Fortalecer la configuración segura de los sistemas tecnológicos críticos mediante la implementación de controles de hardening basados en estándares reconocidos.</li>
<li>Impulsar una cultura organizacional orientada a la protección de la información, integrando la seguridad en las prácticas diarias del personal a través de programas de sensibilización, formación continua y refuerzo de las responsabilidades individuales respecto al uso seguro de las tecnologías.</li>
<li>Garantizar el cumplimiento de la normativa de protección de datos personales aplicable (Chile y mercados regionales), asegurando que el 100% de los procesos que involucren datos sensibles cuenten con controles implementados, documentación actualizada y mecanismos de respuesta ante incidentes de privacidad.</li>
<li>Establecer lineamientos y controles para el uso seguro de herramientas de inteligencia artificial, asegurando que su adopción dentro de la organización se realice de forma controlada, minimizando riesgos de fuga de información, uso indebido o exposición de datos sensibles.</li>
</ul>
<p>El cumplimiento de estos objetivos será revisado periódicamente por el Comité de Seguridad, asegurando su seguimiento, medición y mejora continua conforme a los lineamientos del SGSI.</p>
<p>En Rocketbot nuestras políticas y procedimientos en cuanto a la Seguridad de la Información son del conocimiento general de los empleados, cuando se aplican. En la medida de lo posible y con base al Plan de Comunicación del SGSI definido, nuestras partes interesadas clave serán informadas de nuestros lineamientos y mejores prácticas.</p>
""",
'en': """
<p>Information Security at Rocketbot is a fundamental part of our business, allowing us to give our clients and users confidence in the information technologies we operate. Data, based on our information classification, is managed to the highest standards according to the best practices available in the market, which is a foundation for our growth and organizational sustainability.</p>
<p>Information Security at Rocketbot is possible thanks to the commitment of senior management, which promotes a culture of continuous improvement and provides the necessary resources and tools.</p>
<p>Senior management understands and addresses the importance and benefits of remaining in compliance, not only with ISO 27001 requirements and security best practices, but also with other legal, contractual and government requirements relevant to the organization's context.</p>
<p>As part of this commitment, senior management establishes and supports the following information security objectives, aligned with the ISMS and the organizational strategy:</p>
<ul>
<li>Implement continuous monitoring controls that allow 100% of critical threats detected in information systems to be identified and reported.</li>
<li>Strengthen the secure configuration of critical technology systems by implementing hardening controls based on recognized standards.</li>
<li>Foster an organizational culture oriented toward information protection, integrating security into staff's daily practices through awareness programs, continuous training and reinforcement of individual responsibilities regarding the secure use of technology.</li>
<li>Ensure compliance with applicable personal data protection regulations (Chile and regional markets), ensuring that 100% of processes involving sensitive data have implemented controls, up-to-date documentation and privacy incident response mechanisms.</li>
<li>Establish guidelines and controls for the secure use of artificial intelligence tools, ensuring their adoption within the organization is carried out in a controlled manner, minimizing risks of information leakage, misuse or exposure of sensitive data.</li>
</ul>
<p>Compliance with these objectives will be periodically reviewed by the Security Committee, ensuring their monitoring, measurement and continuous improvement in accordance with ISMS guidelines.</p>
<p>At Rocketbot, our Information Security policies and procedures are made known to employees in general, when applicable. As far as possible, and based on the defined ISMS Communication Plan, our key stakeholders will be informed of our guidelines and best practices.</p>
""",
'pt': """
<p>A Segurança da Informação na Rocketbot é parte fundamental do negócio para transmitir confiança aos nossos clientes e usuários sobre as tecnologias da informação que operamos. Os dados, com base em nossa classificação da informação, são gerenciados com os mais altos padrões, de acordo com as melhores práticas disponíveis no mercado, o que é uma base para nosso crescimento e sustentabilidade organizacional.</p>
<p>A Segurança da Informação na Rocketbot é possível graças ao compromisso da alta direção, que promove uma cultura de melhoria contínua, disponibilizando os recursos e ferramentas necessárias.</p>
<p>A alta direção entende e atende à importância e aos benefícios de manter a conformidade, não apenas com os requisitos da ISO 27001 e as melhores práticas de segurança, mas também com outros requisitos legais, contratuais e governamentais relevantes para o contexto da organização.</p>
<p>Como parte desse compromisso, a alta direção estabelece e apoia os seguintes objetivos de segurança da informação, alinhados ao SGSI e à estratégia organizacional:</p>
<ul>
<li>Implementar controles de vigilância contínua que permitam identificar e reportar 100% das ameaças críticas detectadas nos sistemas de informação.</li>
<li>Fortalecer a configuração segura dos sistemas tecnológicos críticos por meio da implementação de controles de hardening baseados em padrões reconhecidos.</li>
<li>Impulsionar uma cultura organizacional voltada à proteção da informação, integrando a segurança às práticas diárias da equipe por meio de programas de conscientização, formação contínua e reforço das responsabilidades individuais quanto ao uso seguro das tecnologias.</li>
<li>Garantir o cumprimento da normativa de proteção de dados pessoais aplicável (Chile e mercados regionais), assegurando que 100% dos processos que envolvem dados sensíveis contem com controles implementados, documentação atualizada e mecanismos de resposta a incidentes de privacidade.</li>
<li>Estabelecer diretrizes e controles para o uso seguro de ferramentas de inteligência artificial, garantindo que sua adoção dentro da organização ocorra de forma controlada, minimizando riscos de vazamento de informações, uso indevido ou exposição de dados sensíveis.</li>
</ul>
<p>O cumprimento desses objetivos será revisado periodicamente pelo Comitê de Segurança, assegurando seu acompanhamento, medição e melhoria contínua conforme as diretrizes do SGSI.</p>
<p>Na Rocketbot, nossas políticas e procedimentos de Segurança da Informação são de conhecimento geral dos colaboradores, quando aplicáveis. Na medida do possível, e com base no Plano de Comunicação do SGSI definido, nossas partes interessadas-chave serão informadas sobre nossas diretrizes e melhores práticas.</p>
""",
}

META = {
 'privacidad': {
  'es': {'title':'Políticas de privacidad | Rocketbot','desc':'Política de privacidad y protección de datos personales de Rocketbot: recolección, tratamiento, derechos ARCO y cookies.','h1':'Políticas de privacidad','eyebrow':'Legal','meta':'Última actualización: 1 de octubre de 2021'},
  'en': {'title':'Privacy Policy | Rocketbot','desc':"Rocketbot's privacy policy and personal data protection: collection, processing, data subject rights and cookies.",'h1':'Privacy policy','eyebrow':'Legal','meta':'Last updated: October 1, 2021'},
  'pt': {'title':'Política de privacidade | Rocketbot','desc':'Política de privacidade e proteção de dados pessoais da Rocketbot: coleta, tratamento, direitos do titular e cookies.','h1':'Política de privacidade','eyebrow':'Legal','meta':'Última atualização: 1 de outubro de 2021'},
  'content': PRIV,
  'slug': 'politicas-de-privacidad',
 },
 'seguridad': {
  'es': {'title':'Políticas de seguridad | Rocketbot','desc':'Política de seguridad de la información de Rocketbot: objetivos del SGSI, compromiso de la dirección y cumplimiento ISO 27001.','h1':'Políticas de seguridad','eyebrow':'Legal','meta':'Alineado a ISO 27001'},
  'en': {'title':'Security Policy | Rocketbot','desc':"Rocketbot's information security policy: ISMS objectives, management commitment and ISO 27001 compliance.",'h1':'Security policy','eyebrow':'Legal','meta':'Aligned with ISO 27001'},
  'pt': {'title':'Política de segurança | Rocketbot','desc':'Política de segurança da informação da Rocketbot: objetivos do SGSI, compromisso da direção e conformidade com a ISO 27001.','h1':'Política de segurança','eyebrow':'Legal','meta':'Alinhado à ISO 27001'},
  'content': SEC,
  'slug': 'politicas-de-seguridad',
 },
}

SECTION_RE = re.compile(r'<!-- CONTACT PAGE -->.*?<!-- FOOTER -->', re.S)
TITLE_RE = re.compile(r'<title>.*?</title>', re.S)


def sub_attr(src, prop, value):
    pat = re.compile(r'(<meta (?:name|property)="' + re.escape(prop) + r'" content=")[^"]*(">)')
    return pat.sub(lambda m: m.group(1) + value + m.group(2), src)


def build_main(t, content):
    return """<!-- CONTACT PAGE -->
<!-- ======================= LEGAL PAGE ======================= -->
<main class="rb-legalpg">

  <section class="rb-legalpg-hero">
    <div class="container">
      <span class="rb-eyebrow"><span class="dot"></span>{eyebrow}</span>
      <h1 class="rb-legalpg-hero__title">{h1}</h1>
      <p class="rb-legalpg-hero__meta">{meta}</p>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="rb-legal">
{content}
      </div>
    </div>
  </section>

</main>

<!-- FOOTER -->""".format(eyebrow=t['eyebrow'], h1=t['h1'], meta=t['meta'], content=content)


def build(page_key, lang, folder):
    cfg = META[page_key]
    src = io.open(os.path.join(folder, 'contacto.html'), encoding='utf-8').read()
    t = cfg[lang]
    content = cfg['content'][lang]

    src = SECTION_RE.sub(lambda m: build_main(t, content), src, count=1)

    src = TITLE_RE.sub('<title>' + t['title'] + '</title>', src, count=1)
    src = sub_attr(src, 'description', t['desc'])
    src = sub_attr(src, 'og:title', t['title'])
    src = sub_attr(src, 'og:description', t['desc'])
    src = sub_attr(src, 'twitter:title', t['title'])
    src = sub_attr(src, 'twitter:description', t['desc'])

    src = src.replace('content="noindex, follow"', 'content="index, follow"')

    slug = cfg['slug']
    src = src.replace('rocketbot.com/contacto"', 'rocketbot.com/%s"' % slug)
    src = src.replace('rocketbot.com/en/contacto"', 'rocketbot.com/en/%s"' % slug)
    src = src.replace('rocketbot.com/pt/contacto"', 'rocketbot.com/pt/%s"' % slug)

    src = src.replace('"@type": "ContactPage"', '"@type": "WebPage"')

    src = src.replace("PAGE='contacto.html'", "PAGE='%s.html'" % slug)

    if 'rb-legal-css' not in src:
        src = src.replace('</head>', LEGAL_CSS + '</head>', 1)

    out = os.path.join(folder, slug + '.html')
    io.open(out, 'w', encoding='utf-8', newline='\n').write(src)
    print('  escrito %s (%s)' % (out, lang))


def main():
    for page_key in ('privacidad', 'seguridad'):
        for lang, folder in (('es', ROOT), ('en', os.path.join(ROOT, 'en')), ('pt', os.path.join(ROOT, 'pt'))):
            build(page_key, lang, folder)
    print('listo.')


if __name__ == '__main__':
    main()
