import os
os.chdir(r'C:\Users\frani\.claude\worktrees\quirky-aryabhata-b7856b')

MARKER = '<div class="rb-hero__particles"></div>'

HTMLS = {}

HTMLS['saturn-studio.html'] = '''\
  <div class="rb-hero__viz" aria-hidden="true">
    <div class="rb-viz-wrap">
      <div class="rb-viz__ring rb-viz__ring--1"></div>
      <div class="rb-viz__ring rb-viz__ring--2"></div>
      <div class="rb-viz__ring rb-viz__ring--3"></div>
      <div class="rb-viz__orbit rb-viz__orbit--1"><div class="rb-viz__dot"></div></div>
      <div class="rb-viz__orbit rb-viz__orbit--2"><div class="rb-viz__dot"></div></div>
      <div class="rb-viz__orbit rb-viz__orbit--3"><div class="rb-viz__dot"></div></div>
      <div class="rb-viz__core">
        <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2m-7.07-14.07 1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2m-4.93-7.07-1.41 1.41M6.34 17.66l-1.41 1.41"/></svg>
      </div>
      <div class="rb-viz__star" style="width:2px;height:2px;top:8%;left:15%;animation-delay:.2s;"></div>
      <div class="rb-viz__star" style="width:3px;height:3px;top:18%;left:80%;animation-delay:.9s;"></div>
      <div class="rb-viz__star" style="width:2px;height:2px;top:75%;left:85%;animation-delay:1.6s;"></div>
      <div class="rb-viz__star" style="width:2px;height:2px;top:82%;left:20%;animation-delay:2.2s;"></div>
      <div class="rb-viz__star" style="width:1px;height:1px;top:42%;left:92%;animation-delay:.5s;"></div>
    </div>
  </div>'''

HTMLS['rpa-studio.html'] = '''\
  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 460 460" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <g class="rb-rpa-gear--big">
        <circle cx="170" cy="200" r="105" fill="none" stroke="rgba(188,0,23,.15)" stroke-width="2" stroke-dasharray="22 8"/>
        <circle cx="170" cy="200" r="80" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.25)" stroke-width="2"/>
        <circle cx="170" cy="200" r="28" fill="rgba(188,0,23,.12)" stroke="rgba(188,0,23,.35)" stroke-width="2"/>
        <line x1="170" y1="120" x2="170" y2="280" stroke="rgba(188,0,23,.15)" stroke-width="2"/>
        <line x1="90" y1="200" x2="250" y2="200" stroke="rgba(188,0,23,.15)" stroke-width="2"/>
        <line x1="114" y1="144" x2="226" y2="256" stroke="rgba(188,0,23,.1)" stroke-width="1.5"/>
        <line x1="226" y1="144" x2="114" y2="256" stroke="rgba(188,0,23,.1)" stroke-width="1.5"/>
      </g>
      <g class="rb-rpa-gear--small">
        <circle cx="308" cy="148" r="66" fill="none" stroke="rgba(43,127,255,.15)" stroke-width="1.5" stroke-dasharray="14 6"/>
        <circle cx="308" cy="148" r="50" fill="rgba(43,127,255,.06)" stroke="rgba(43,127,255,.22)" stroke-width="1.5"/>
        <circle cx="308" cy="148" r="17" fill="rgba(43,127,255,.12)" stroke="rgba(43,127,255,.32)" stroke-width="1.5"/>
        <line x1="308" y1="98" x2="308" y2="198" stroke="rgba(43,127,255,.12)" stroke-width="1.5"/>
        <line x1="258" y1="148" x2="358" y2="148" stroke="rgba(43,127,255,.12)" stroke-width="1.5"/>
        <line x1="272" y1="112" x2="344" y2="184" stroke="rgba(43,127,255,.1)" stroke-width="1"/>
        <line x1="344" y1="112" x2="272" y2="184" stroke="rgba(43,127,255,.1)" stroke-width="1"/>
      </g>
      <path d="M 40 380 L 140 380 L 180 380 L 280 380 L 320 380 L 420 380" fill="none" stroke="rgba(188,0,23,.18)" stroke-width="1.5" class="rb-rpa-flow-line"/>
      <rect x="40" y="358" width="100" height="42" rx="10" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.28)" stroke-width="1.5" class="rb-rpa-node-pulse"/>
      <rect x="180" y="358" width="100" height="42" rx="10" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.28)" stroke-width="1.5" class="rb-rpa-node-pulse d1"/>
      <rect x="320" y="358" width="100" height="42" rx="10" fill="rgba(43,127,255,.07)" stroke="rgba(43,127,255,.28)" stroke-width="1.5" class="rb-rpa-node-pulse d2"/>
      <polyline points="58,380 68,390 88,368" fill="none" stroke="rgba(188,0,23,.65)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="rb-rpa-node-pulse"/>
      <polyline points="198,380 208,390 228,368" fill="none" stroke="rgba(188,0,23,.65)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="rb-rpa-node-pulse d1"/>
      <circle cx="370" cy="379" r="11" fill="none" stroke="rgba(43,127,255,.6)" stroke-width="2.5" stroke-dasharray="20 14" class="rb-rpa-gear--small"/>
    </svg>
  </div>'''

HTMLS['ai-studio.html'] = '''\
  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 460 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <g class="rb-ai-card">
        <rect x="30" y="60" width="100" height="72" rx="12" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.25)" stroke-width="1.5"/>
        <rect x="42" y="74" width="76" height="6" rx="3" fill="rgba(188,0,23,.25)" class="rb-ai-scan"/>
        <rect x="42" y="86" width="55" height="4" rx="2" fill="rgba(188,0,23,.15)"/>
        <rect x="42" y="96" width="65" height="4" rx="2" fill="rgba(188,0,23,.15)"/>
        <rect x="42" y="106" width="40" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
        <path d="M42 118 h76 v14 h-76 z" fill="none" stroke="rgba(188,0,23,.2)" stroke-width="1"/>
        <path d="M42 118 l38 10 l38-10" fill="none" stroke="rgba(188,0,23,.2)" stroke-width="1"/>
      </g>
      <g class="rb-ai-card c2">
        <rect x="30" y="165" width="100" height="72" rx="12" fill="rgba(43,127,255,.07)" stroke="rgba(43,127,255,.25)" stroke-width="1.5"/>
        <rect x="42" y="178" width="60" height="7" rx="3" fill="rgba(43,127,255,.22)"/>
        <rect x="42" y="205" width="12" height="18" rx="2" fill="rgba(43,127,255,.25)" class="rb-ai-scan"/>
        <rect x="58" y="200" width="12" height="28" rx="2" fill="rgba(43,127,255,.3)" class="rb-ai-scan" style="animation-delay:.3s"/>
        <rect x="74" y="208" width="12" height="12" rx="2" fill="rgba(43,127,255,.22)" class="rb-ai-scan" style="animation-delay:.6s"/>
        <rect x="90" y="203" width="12" height="22" rx="2" fill="rgba(43,127,255,.2)" class="rb-ai-scan" style="animation-delay:.9s"/>
      </g>
      <g class="rb-ai-card c3">
        <rect x="30" y="268" width="100" height="72" rx="12" fill="rgba(0,180,220,.06)" stroke="rgba(0,180,220,.22)" stroke-width="1.5"/>
        <rect x="42" y="280" width="76" height="5" rx="2" fill="rgba(0,180,220,.3)" class="rb-ai-scan"/>
        <rect x="42" y="291" width="60" height="4" rx="2" fill="rgba(0,180,220,.18)"/>
        <rect x="42" y="301" width="72" height="4" rx="2" fill="rgba(0,180,220,.18)"/>
        <rect x="42" y="311" width="50" height="4" rx="2" fill="rgba(0,180,220,.12)"/>
        <rect x="42" y="321" width="66" height="4" rx="2" fill="rgba(0,180,220,.12)"/>
      </g>
      <line x1="130" y1="96" x2="218" y2="185" stroke="rgba(188,0,23,.2)" stroke-width="1.5" class="rb-ai-link"/>
      <line x1="130" y1="201" x2="218" y2="210" stroke="rgba(43,127,255,.2)" stroke-width="1.5" class="rb-ai-link d2"/>
      <line x1="130" y1="304" x2="218" y2="237" stroke="rgba(0,180,220,.18)" stroke-width="1.5" class="rb-ai-link d4"/>
      <circle cx="245" cy="210" r="38" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.32)" stroke-width="2"/>
      <circle cx="245" cy="210" r="24" fill="rgba(188,0,23,.15)" stroke="rgba(188,0,23,.45)" stroke-width="1.5" class="rb-ai-node"/>
      <text x="232" y="216" font-size="16" font-weight="bold" fill="rgba(188,0,23,.75)" font-family="sans-serif">AI</text>
      <circle cx="358" cy="140" r="13" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.28)" stroke-width="1.5" class="rb-ai-node d1"/>
      <text x="349" y="144" font-size="9" fill="rgba(188,0,23,.6)" font-family="monospace">txt</text>
      <circle cx="390" cy="205" r="13" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.28)" stroke-width="1.5" class="rb-ai-node d2"/>
      <text x="378" y="210" font-size="9" fill="rgba(188,0,23,.6)" font-family="monospace">json</text>
      <circle cx="358" cy="268" r="13" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.28)" stroke-width="1.5" class="rb-ai-node d3"/>
      <text x="350" y="272" font-size="9" fill="rgba(188,0,23,.6)" font-family="monospace">csv</text>
      <line x1="280" y1="195" x2="345" y2="148" stroke="rgba(188,0,23,.2)" stroke-width="1.5" class="rb-ai-link d1"/>
      <line x1="283" y1="210" x2="377" y2="210" stroke="rgba(188,0,23,.2)" stroke-width="1.5" class="rb-ai-link d2"/>
      <line x1="280" y1="225" x2="345" y2="260" stroke="rgba(188,0,23,.2)" stroke-width="1.5" class="rb-ai-link d3"/>
    </svg>
  </div>'''

HTMLS['orquestador.html'] = '''\
  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 460 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect x="30" y="55" width="110" height="68" rx="14" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.28)" stroke-width="1.5"/>
      <circle cx="50" cy="76" r="7" fill="rgba(188,0,23,.25)" stroke="rgba(188,0,23,.5)" stroke-width="1.5" class="rb-orq-pulse"/>
      <rect x="63" y="72" width="58" height="5" rx="2" fill="rgba(188,0,23,.25)"/>
      <rect x="42" y="88" width="80" height="4" rx="2" fill="rgba(188,0,23,.15)"/>
      <rect x="42" y="98" width="60" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="42" y="108" width="70" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="175" y="55" width="110" height="68" rx="14" fill="rgba(43,127,255,.06)" stroke="rgba(43,127,255,.25)" stroke-width="1.5"/>
      <circle cx="195" cy="76" r="7" fill="rgba(43,127,255,.25)" stroke="rgba(43,127,255,.45)" stroke-width="1.5" class="rb-orq-pulse d1"/>
      <rect x="208" y="72" width="58" height="5" rx="2" fill="rgba(43,127,255,.25)"/>
      <rect x="187" y="88" width="80" height="4" rx="2" fill="rgba(43,127,255,.12)"/>
      <rect x="187" y="98" width="55" height="4" rx="2" fill="rgba(43,127,255,.1)"/>
      <rect x="187" y="108" width="70" height="4" rx="2" fill="rgba(43,127,255,.1)"/>
      <rect x="320" y="55" width="110" height="68" rx="14" fill="rgba(0,180,220,.05)" stroke="rgba(0,180,220,.22)" stroke-width="1.5"/>
      <circle cx="340" cy="76" r="7" fill="rgba(0,180,220,.22)" stroke="rgba(0,180,220,.4)" stroke-width="1.5" class="rb-orq-pulse d2"/>
      <rect x="353" y="72" width="58" height="5" rx="2" fill="rgba(0,180,220,.25)"/>
      <rect x="332" y="88" width="80" height="4" rx="2" fill="rgba(0,180,220,.12)"/>
      <rect x="332" y="98" width="65" height="4" rx="2" fill="rgba(0,180,220,.1)"/>
      <rect x="332" y="108" width="50" height="4" rx="2" fill="rgba(0,180,220,.1)"/>
      <line x1="140" y1="89" x2="175" y2="89" stroke="rgba(188,0,23,.25)" stroke-width="1.5" class="rb-orq-flow"/>
      <line x1="285" y1="89" x2="320" y2="89" stroke="rgba(43,127,255,.25)" stroke-width="1.5" class="rb-orq-flow d1"/>
      <rect x="155" y="178" width="150" height="78" rx="16" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.35)" stroke-width="2"/>
      <rect x="170" y="192" width="120" height="7" rx="3" fill="rgba(188,0,23,.25)" class="rb-orq-pulse"/>
      <rect x="170" y="207" width="50" height="4" rx="2" fill="rgba(188,0,23,.18)" class="rb-orq-pulse d1"/>
      <rect x="228" y="207" width="60" height="4" rx="2" fill="rgba(188,0,23,.15)" class="rb-orq-pulse d2"/>
      <rect x="170" y="218" width="35" height="4" rx="2" fill="rgba(188,0,23,.12)"/>
      <rect x="213" y="218" width="55" height="4" rx="2" fill="rgba(188,0,23,.12)"/>
      <rect x="170" y="232" width="90" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="268" y="232" width="40" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <line x1="85" y1="123" x2="185" y2="178" stroke="rgba(188,0,23,.22)" stroke-width="1.5" class="rb-orq-flow"/>
      <line x1="230" y1="123" x2="230" y2="178" stroke="rgba(43,127,255,.22)" stroke-width="1.5" class="rb-orq-flow d1"/>
      <line x1="375" y1="123" x2="275" y2="178" stroke="rgba(0,180,220,.18)" stroke-width="1.5" class="rb-orq-flow d2"/>
      <rect x="70" y="318" width="90" height="50" rx="12" fill="rgba(188,0,23,.06)" stroke="rgba(188,0,23,.22)" stroke-width="1.5"/>
      <circle cx="90" cy="337" r="5" fill="rgba(188,0,23,.35)" class="rb-orq-pulse d1"/>
      <rect x="102" y="333" width="40" height="4" rx="2" fill="rgba(188,0,23,.2)"/>
      <rect x="82" y="348" width="60" height="4" rx="2" fill="rgba(188,0,23,.12)"/>
      <rect x="300" y="318" width="90" height="50" rx="12" fill="rgba(43,127,255,.06)" stroke="rgba(43,127,255,.22)" stroke-width="1.5"/>
      <circle cx="320" cy="337" r="5" fill="rgba(43,127,255,.35)" class="rb-orq-pulse d3"/>
      <rect x="332" y="333" width="40" height="4" rx="2" fill="rgba(43,127,255,.2)"/>
      <rect x="312" y="348" width="55" height="4" rx="2" fill="rgba(43,127,255,.12)"/>
      <line x1="185" y1="256" x2="115" y2="318" stroke="rgba(188,0,23,.18)" stroke-width="1.5" class="rb-orq-flow d2"/>
      <line x1="275" y1="256" x2="345" y2="318" stroke="rgba(43,127,255,.18)" stroke-width="1.5" class="rb-orq-flow"/>
      <rect x="196" y="332" width="14" height="18" rx="3" fill="rgba(188,0,23,.18)" class="rb-orq-pulse"/>
      <rect x="216" y="324" width="14" height="26" rx="3" fill="rgba(188,0,23,.25)" class="rb-orq-pulse d1"/>
      <rect x="236" y="328" width="14" height="22" rx="3" fill="rgba(188,0,23,.18)" class="rb-orq-pulse d2"/>
    </svg>
  </div>'''

HTMLS['xperience.html'] = '''\
  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 440 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect x="80" y="55" width="280" height="326" rx="20" fill="rgba(255,255,255,.92)" stroke="rgba(188,0,23,.2)" stroke-width="2" class="rb-xpr-float"/>
      <rect x="80" y="55" width="280" height="44" rx="20" fill="rgba(188,0,23,.1)" stroke="rgba(188,0,23,.15)" stroke-width="1"/>
      <rect x="80" y="75" width="280" height="24" fill="rgba(188,0,23,.1)"/>
      <circle cx="106" cy="77" r="6" fill="rgba(188,0,23,.4)"/>
      <circle cx="126" cy="77" r="6" fill="rgba(255,180,0,.4)"/>
      <circle cx="146" cy="77" r="6" fill="rgba(0,200,80,.4)"/>
      <rect x="168" y="73" width="100" height="8" rx="4" fill="rgba(188,0,23,.2)"/>
      <rect x="104" y="122" width="150" height="9" rx="4" fill="rgba(188,0,23,.3)"/>
      <rect x="104" y="138" width="100" height="6" rx="3" fill="rgba(0,0,0,.1)"/>
      <g class="rb-xpr-field">
        <rect x="104" y="162" width="232" height="36" rx="8" fill="rgba(255,255,255,.95)" stroke="rgba(188,0,23,.35)" stroke-width="1.5"/>
        <rect x="116" y="177" width="60" height="6" rx="3" fill="rgba(0,0,0,.15)"/>
      </g>
      <g class="rb-xpr-field f2">
        <rect x="104" y="210" width="232" height="36" rx="8" fill="rgba(255,255,255,.95)" stroke="rgba(188,0,23,.25)" stroke-width="1.5"/>
        <rect x="116" y="225" width="80" height="6" rx="3" fill="rgba(0,0,0,.12)"/>
      </g>
      <g class="rb-xpr-field f3">
        <rect x="104" y="260" width="14" height="14" rx="3" fill="rgba(188,0,23,.1)" stroke="rgba(188,0,23,.4)" stroke-width="1.5"/>
        <polyline points="107,267 111,271 117,263" fill="none" stroke="rgba(188,0,23,.8)" stroke-width="2" stroke-linecap="round" class="rb-xpr-check"/>
        <rect x="126" y="263" width="70" height="6" rx="3" fill="rgba(0,0,0,.12)"/>
        <rect x="104" y="282" width="14" height="14" rx="3" fill="rgba(188,0,23,.1)" stroke="rgba(188,0,23,.4)" stroke-width="1.5"/>
        <polyline points="107,289 111,293 117,285" fill="none" stroke="rgba(188,0,23,.6)" stroke-width="2" stroke-linecap="round" class="rb-xpr-check ck2"/>
        <rect x="126" y="285" width="55" height="6" rx="3" fill="rgba(0,0,0,.1)"/>
      </g>
      <g class="rb-xpr-field f4">
        <rect x="104" y="314" width="232" height="42" rx="10" class="rb-xpr-btn-glow" stroke="rgba(188,0,23,.4)" stroke-width="1.5"/>
        <rect x="158" y="328" width="84" height="8" rx="4" fill="rgba(188,0,23,.55)"/>
      </g>
      <g class="rb-xpr-float fl2">
        <rect x="292" y="26" width="100" height="26" rx="13" fill="rgba(0,200,80,.12)" stroke="rgba(0,200,80,.32)" stroke-width="1.5"/>
        <circle cx="312" cy="39" r="5" fill="rgba(0,200,80,.5)" class="rb-xpr-check"/>
        <rect x="324" y="36" width="50" height="5" rx="2" fill="rgba(0,150,60,.35)"/>
      </g>
      <g class="rb-xpr-float">
        <rect x="42" y="294" width="26" height="26" rx="8" fill="rgba(43,127,255,.12)" stroke="rgba(43,127,255,.3)" stroke-width="1.5"/>
        <path d="M 50 302 L 55 312 L 60 302" fill="none" stroke="rgba(43,127,255,.6)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </svg>
  </div>'''

for fname, html in HTMLS.items():
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'class="rb-hero__viz"' in content:
        print(f'{fname}: HTML already present, skipping')
        continue

    if MARKER in content:
        content = content.replace(MARKER, MARKER + '\n' + html, 1)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        ok = 'class="rb-hero__viz"' in content
        print(f'{fname}: injected OK={ok}')
    else:
        print(f'{fname}: WARNING - marker not found!')

print('Done.')
