import re, os

os.chdir(r'C:\Users\frani\.claude\worktrees\quirky-aryabhata-b7856b')

# ══════════════════════════════════════════════════════════════
# 1. SATURN STUDIO — Orbital rings (dark bg)
# ══════════════════════════════════════════════════════════════
SATURN_CSS = """
/* SATURN HERO VIZ */
.rb-hero__viz{position:absolute;right:4%;top:50%;transform:translateY(-50%);width:420px;height:420px;pointer-events:none;z-index:0;}
.rb-viz-wrap{position:relative;width:100%;height:100%;}
.rb-viz__ring{position:absolute;border-radius:50%;top:50%;left:50%;}
.rb-viz__ring--1{width:380px;height:380px;margin:-190px 0 0 -190px;border:1px solid rgba(188,0,23,.4);animation:rb-viz-spin 30s linear infinite;}
.rb-viz__ring--2{width:270px;height:270px;margin:-135px 0 0 -135px;border:1px dashed rgba(255,255,255,.18);animation:rb-viz-spin 20s linear infinite reverse;}
.rb-viz__ring--3{width:160px;height:160px;margin:-80px 0 0 -80px;border:1px solid rgba(0,212,255,.28);animation:rb-viz-spin 13s linear infinite;}
@keyframes rb-viz-spin{to{transform:rotate(360deg);}}
.rb-viz__orbit{position:absolute;border-radius:50%;top:50%;left:50%;}
.rb-viz__orbit--1{width:380px;height:380px;margin:-190px 0 0 -190px;animation:rb-viz-spin 9s linear infinite;}
.rb-viz__orbit--2{width:270px;height:270px;margin:-135px 0 0 -135px;animation:rb-viz-spin 15s linear infinite reverse;}
.rb-viz__orbit--3{width:160px;height:160px;margin:-80px 0 0 -80px;animation:rb-viz-spin 22s linear infinite;}
.rb-viz__dot{position:absolute;border-radius:50%;top:-5px;left:50%;margin-left:-5px;}
.rb-viz__orbit--1 .rb-viz__dot{width:10px;height:10px;background:var(--rb-red);box-shadow:0 0 16px rgba(188,0,23,.9);}
.rb-viz__orbit--2 .rb-viz__dot{width:7px;height:7px;margin-left:-3.5px;top:-3.5px;background:#2B7FFF;box-shadow:0 0 12px rgba(43,127,255,.9);}
.rb-viz__orbit--3 .rb-viz__dot{width:5px;height:5px;margin-left:-2.5px;top:-2.5px;background:#00D4FF;box-shadow:0 0 10px rgba(0,212,255,.9);}
.rb-viz__core{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;border-radius:50%;background:radial-gradient(circle,rgba(188,0,23,.4),rgba(188,0,23,.1));border:1.5px solid rgba(188,0,23,.5);display:flex;align-items:center;justify-content:center;animation:rb-viz-breathe 4s ease-in-out infinite;}
@keyframes rb-viz-breathe{0%,100%{box-shadow:0 0 20px rgba(188,0,23,.4);}50%{box-shadow:0 0 60px rgba(188,0,23,.7);}}
.rb-viz__star{position:absolute;border-radius:50%;background:rgba(255,255,255,.6);animation:rb-viz-twinkle 3s ease-in-out infinite;}
@keyframes rb-viz-twinkle{0%,100%{opacity:.08;}50%{opacity:.9;}}
@media(max-width:900px){.rb-hero__viz{display:none;}}
"""

SATURN_HTML = """  <div class="rb-hero__viz" aria-hidden="true">
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
  </div>
"""

# ══════════════════════════════════════════════════════════════
# 2. RPA STUDIO — Interlocking gears + process flow
# ══════════════════════════════════════════════════════════════
RPA_CSS = """
/* RPA HERO VIZ */
.rb-hero__viz{position:absolute;right:0;top:50%;transform:translateY(-50%);width:460px;height:460px;pointer-events:none;z-index:0;opacity:.7;}
.rb-rpa-gear--big{transform-origin:170px 200px;animation:rpa-spin-r 16s linear infinite;}
.rb-rpa-gear--small{transform-origin:308px 148px;animation:rpa-spin-r 10s linear infinite reverse;}
@keyframes rpa-spin-r{to{transform:rotate(360deg);}}
.rb-rpa-flow-line{stroke-dasharray:8 5;animation:rpa-flow 2.5s linear infinite;}
@keyframes rpa-flow{to{stroke-dashoffset:-130;}}
.rb-rpa-node-pulse{animation:rpa-np 2s ease-in-out infinite;}
.rb-rpa-node-pulse.d1{animation-delay:.5s;}
.rb-rpa-node-pulse.d2{animation-delay:1s;}
@keyframes rpa-np{0%,100%{opacity:.45;}60%{opacity:1;}}
@media(max-width:900px){.rb-hero__viz{display:none;}}
"""

RPA_HTML = """  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 460 460" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <g class="rb-rpa-gear--big">
        <circle cx="170" cy="200" r="105" fill="none" stroke="rgba(188,0,23,.12)" stroke-width="2" stroke-dasharray="22 8"/>
        <circle cx="170" cy="200" r="80" fill="rgba(188,0,23,.05)" stroke="rgba(188,0,23,.2)" stroke-width="2"/>
        <circle cx="170" cy="200" r="28" fill="rgba(188,0,23,.1)" stroke="rgba(188,0,23,.3)" stroke-width="2"/>
        <line x1="170" y1="120" x2="170" y2="280" stroke="rgba(188,0,23,.12)" stroke-width="2"/>
        <line x1="90" y1="200" x2="250" y2="200" stroke="rgba(188,0,23,.12)" stroke-width="2"/>
        <line x1="114" y1="144" x2="226" y2="256" stroke="rgba(188,0,23,.08)" stroke-width="1.5"/>
        <line x1="226" y1="144" x2="114" y2="256" stroke="rgba(188,0,23,.08)" stroke-width="1.5"/>
      </g>
      <g class="rb-rpa-gear--small">
        <circle cx="308" cy="148" r="66" fill="none" stroke="rgba(43,127,255,.12)" stroke-width="1.5" stroke-dasharray="14 6"/>
        <circle cx="308" cy="148" r="50" fill="rgba(43,127,255,.04)" stroke="rgba(43,127,255,.18)" stroke-width="1.5"/>
        <circle cx="308" cy="148" r="17" fill="rgba(43,127,255,.1)" stroke="rgba(43,127,255,.28)" stroke-width="1.5"/>
        <line x1="308" y1="98" x2="308" y2="198" stroke="rgba(43,127,255,.1)" stroke-width="1.5"/>
        <line x1="258" y1="148" x2="358" y2="148" stroke="rgba(43,127,255,.1)" stroke-width="1.5"/>
        <line x1="272" y1="112" x2="344" y2="184" stroke="rgba(43,127,255,.08)" stroke-width="1"/>
        <line x1="344" y1="112" x2="272" y2="184" stroke="rgba(43,127,255,.08)" stroke-width="1"/>
      </g>
      <path d="M 40 370 L 140 370 L 180 370 L 280 370 L 320 370 L 420 370" fill="none" stroke="rgba(188,0,23,.15)" stroke-width="1.5" class="rb-rpa-flow-line"/>
      <rect x="40" y="350" width="100" height="40" rx="10" fill="rgba(188,0,23,.06)" stroke="rgba(188,0,23,.25)" stroke-width="1.5" class="rb-rpa-node-pulse"/>
      <rect x="180" y="350" width="100" height="40" rx="10" fill="rgba(188,0,23,.06)" stroke="rgba(188,0,23,.25)" stroke-width="1.5" class="rb-rpa-node-pulse d1"/>
      <rect x="320" y="350" width="100" height="40" rx="10" fill="rgba(43,127,255,.06)" stroke="rgba(43,127,255,.25)" stroke-width="1.5" class="rb-rpa-node-pulse d2"/>
      <polyline points="58,370 68,380 88,360" fill="none" stroke="rgba(188,0,23,.55)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="rb-rpa-node-pulse"/>
      <polyline points="198,370 208,380 228,360" fill="none" stroke="rgba(188,0,23,.55)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="rb-rpa-node-pulse d1"/>
      <circle cx="370" cy="370" r="11" fill="none" stroke="rgba(43,127,255,.5)" stroke-width="2.5" stroke-dasharray="20 14" class="rb-rpa-gear--small"/>
    </svg>
  </div>
"""

# ══════════════════════════════════════════════════════════════
# 3. AI STUDIO — Neural network + document cards
# ══════════════════════════════════════════════════════════════
AI_CSS = """
/* AI STUDIO HERO VIZ */
.rb-hero__viz{position:absolute;right:0;top:50%;transform:translateY(-50%);width:460px;height:440px;pointer-events:none;z-index:0;opacity:.7;}
.rb-ai-link{stroke-dasharray:6 5;animation:ai-link-flow 2s linear infinite;}
.rb-ai-link.d1{animation-delay:.4s;}.rb-ai-link.d2{animation-delay:.8s;}.rb-ai-link.d3{animation-delay:1.2s;}.rb-ai-link.d4{animation-delay:1.6s;}
@keyframes ai-link-flow{to{stroke-dashoffset:-110;}}
.rb-ai-node{animation:ai-node-p 2.5s ease-in-out infinite;}
.rb-ai-node.d1{animation-delay:.3s;}.rb-ai-node.d2{animation-delay:.6s;}.rb-ai-node.d3{animation-delay:.9s;}
@keyframes ai-node-p{0%,100%{opacity:.5;}50%{opacity:1;}}
.rb-ai-card{animation:ai-card-fl 4s ease-in-out infinite;}
.rb-ai-card.c2{animation-delay:1.3s;}.rb-ai-card.c3{animation-delay:2.6s;}
@keyframes ai-card-fl{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
.rb-ai-scan{animation:ai-scan 2s ease-in-out infinite;}
@keyframes ai-scan{0%,100%{opacity:.3;}50%{opacity:.9;}}
@media(max-width:900px){.rb-hero__viz{display:none;}}
"""

AI_HTML = """  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 460 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <g class="rb-ai-card">
        <rect x="30" y="60" width="100" height="72" rx="12" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.22)" stroke-width="1.5"/>
        <rect x="42" y="74" width="76" height="6" rx="3" fill="rgba(188,0,23,.2)" class="rb-ai-scan"/>
        <rect x="42" y="86" width="55" height="4" rx="2" fill="rgba(188,0,23,.12)"/>
        <rect x="42" y="96" width="65" height="4" rx="2" fill="rgba(188,0,23,.12)"/>
        <rect x="42" y="106" width="40" height="4" rx="2" fill="rgba(188,0,23,.08)"/>
        <path d="M42 118 h76 v14 h-76 z" fill="none" stroke="rgba(188,0,23,.18)" stroke-width="1"/>
        <path d="M42 118 l38 10 l38-10" fill="none" stroke="rgba(188,0,23,.18)" stroke-width="1"/>
      </g>
      <g class="rb-ai-card c2">
        <rect x="30" y="165" width="100" height="72" rx="12" fill="rgba(43,127,255,.06)" stroke="rgba(43,127,255,.2)" stroke-width="1.5"/>
        <rect x="42" y="178" width="60" height="7" rx="3" fill="rgba(43,127,255,.18)"/>
        <rect x="42" y="205" width="12" height="18" rx="2" fill="rgba(43,127,255,.2)" class="rb-ai-scan"/>
        <rect x="58" y="200" width="12" height="28" rx="2" fill="rgba(43,127,255,.25)" class="rb-ai-scan" style="animation-delay:.3s"/>
        <rect x="74" y="208" width="12" height="12" rx="2" fill="rgba(43,127,255,.2)" class="rb-ai-scan" style="animation-delay:.6s"/>
        <rect x="90" y="203" width="12" height="22" rx="2" fill="rgba(43,127,255,.18)" class="rb-ai-scan" style="animation-delay:.9s"/>
      </g>
      <g class="rb-ai-card c3">
        <rect x="30" y="268" width="100" height="72" rx="12" fill="rgba(0,212,255,.05)" stroke="rgba(0,212,255,.18)" stroke-width="1.5"/>
        <rect x="42" y="280" width="76" height="5" rx="2" fill="rgba(0,212,255,.25)" class="rb-ai-scan"/>
        <rect x="42" y="291" width="60" height="4" rx="2" fill="rgba(0,212,255,.15)"/>
        <rect x="42" y="301" width="72" height="4" rx="2" fill="rgba(0,212,255,.15)"/>
        <rect x="42" y="311" width="50" height="4" rx="2" fill="rgba(0,212,255,.1)"/>
        <rect x="42" y="321" width="66" height="4" rx="2" fill="rgba(0,212,255,.1)"/>
      </g>
      <line x1="130" y1="96" x2="218" y2="185" stroke="rgba(188,0,23,.15)" stroke-width="1.5" class="rb-ai-link"/>
      <line x1="130" y1="201" x2="218" y2="210" stroke="rgba(43,127,255,.15)" stroke-width="1.5" class="rb-ai-link d2"/>
      <line x1="130" y1="304" x2="218" y2="237" stroke="rgba(0,212,255,.12)" stroke-width="1.5" class="rb-ai-link d4"/>
      <circle cx="245" cy="210" r="38" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.28)" stroke-width="2"/>
      <circle cx="245" cy="210" r="24" fill="rgba(188,0,23,.12)" stroke="rgba(188,0,23,.4)" stroke-width="1.5" class="rb-ai-node"/>
      <text x="232" y="216" font-size="16" font-weight="bold" fill="rgba(188,0,23,.7)" font-family="sans-serif">AI</text>
      <circle cx="358" cy="140" r="13" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.22)" stroke-width="1.5" class="rb-ai-node d1"/>
      <text x="349" y="144" font-size="9" fill="rgba(188,0,23,.5)" font-family="monospace">txt</text>
      <circle cx="390" cy="205" r="13" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.22)" stroke-width="1.5" class="rb-ai-node d2"/>
      <text x="378" y="210" font-size="9" fill="rgba(188,0,23,.5)" font-family="monospace">json</text>
      <circle cx="358" cy="268" r="13" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.22)" stroke-width="1.5" class="rb-ai-node d3"/>
      <text x="350" y="272" font-size="9" fill="rgba(188,0,23,.5)" font-family="monospace">csv</text>
      <line x1="280" y1="195" x2="345" y2="148" stroke="rgba(188,0,23,.15)" stroke-width="1.5" class="rb-ai-link d1"/>
      <line x1="283" y1="210" x2="377" y2="210" stroke="rgba(188,0,23,.15)" stroke-width="1.5" class="rb-ai-link d2"/>
      <line x1="280" y1="225" x2="345" y2="260" stroke="rgba(188,0,23,.15)" stroke-width="1.5" class="rb-ai-link d3"/>
    </svg>
  </div>
"""

# ══════════════════════════════════════════════════════════════
# 4. ORQUESTADOR — Pipeline / command center
# ══════════════════════════════════════════════════════════════
ORQ_CSS = """
/* ORQUESTADOR HERO VIZ */
.rb-hero__viz{position:absolute;right:0;top:50%;transform:translateY(-50%);width:460px;height:440px;pointer-events:none;z-index:0;opacity:.65;}
.rb-orq-flow{stroke-dasharray:7 5;animation:orq-flow 2s linear infinite;}
.rb-orq-flow.d1{animation-delay:.5s;}.rb-orq-flow.d2{animation-delay:1s;}
@keyframes orq-flow{to{stroke-dashoffset:-120;}}
.rb-orq-pulse{animation:orq-pulse 2s ease-in-out infinite;}
.rb-orq-pulse.d1{animation-delay:.4s;}.rb-orq-pulse.d2{animation-delay:.8s;}.rb-orq-pulse.d3{animation-delay:1.2s;}
@keyframes orq-pulse{0%,100%{opacity:.35;}55%{opacity:1;}}
@media(max-width:900px){.rb-hero__viz{display:none;}}
"""

ORQ_HTML = """  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 460 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect x="30" y="55" width="110" height="68" rx="14" fill="rgba(188,0,23,.06)" stroke="rgba(188,0,23,.22)" stroke-width="1.5"/>
      <circle cx="50" cy="76" r="7" fill="rgba(188,0,23,.2)" stroke="rgba(188,0,23,.4)" stroke-width="1.5" class="rb-orq-pulse"/>
      <rect x="63" y="72" width="58" height="5" rx="2" fill="rgba(188,0,23,.2)"/>
      <rect x="42" y="88" width="80" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="42" y="98" width="60" height="4" rx="2" fill="rgba(188,0,23,.08)"/>
      <rect x="42" y="108" width="70" height="4" rx="2" fill="rgba(188,0,23,.08)"/>
      <rect x="175" y="55" width="110" height="68" rx="14" fill="rgba(43,127,255,.05)" stroke="rgba(43,127,255,.2)" stroke-width="1.5"/>
      <circle cx="195" cy="76" r="7" fill="rgba(43,127,255,.2)" stroke="rgba(43,127,255,.35)" stroke-width="1.5" class="rb-orq-pulse d1"/>
      <rect x="208" y="72" width="58" height="5" rx="2" fill="rgba(43,127,255,.2)"/>
      <rect x="187" y="88" width="80" height="4" rx="2" fill="rgba(43,127,255,.1)"/>
      <rect x="187" y="98" width="55" height="4" rx="2" fill="rgba(43,127,255,.08)"/>
      <rect x="187" y="108" width="70" height="4" rx="2" fill="rgba(43,127,255,.08)"/>
      <rect x="320" y="55" width="110" height="68" rx="14" fill="rgba(0,212,255,.04)" stroke="rgba(0,212,255,.18)" stroke-width="1.5"/>
      <circle cx="340" cy="76" r="7" fill="rgba(0,212,255,.18)" stroke="rgba(0,212,255,.32)" stroke-width="1.5" class="rb-orq-pulse d2"/>
      <rect x="353" y="72" width="58" height="5" rx="2" fill="rgba(0,212,255,.2)"/>
      <rect x="332" y="88" width="80" height="4" rx="2" fill="rgba(0,212,255,.1)"/>
      <rect x="332" y="98" width="65" height="4" rx="2" fill="rgba(0,212,255,.08)"/>
      <rect x="332" y="108" width="50" height="4" rx="2" fill="rgba(0,212,255,.08)"/>
      <line x1="140" y1="89" x2="175" y2="89" stroke="rgba(188,0,23,.2)" stroke-width="1.5" class="rb-orq-flow"/>
      <line x1="285" y1="89" x2="320" y2="89" stroke="rgba(43,127,255,.2)" stroke-width="1.5" class="rb-orq-flow d1"/>
      <rect x="155" y="178" width="150" height="78" rx="16" fill="rgba(188,0,23,.07)" stroke="rgba(188,0,23,.3)" stroke-width="2"/>
      <rect x="170" y="192" width="120" height="7" rx="3" fill="rgba(188,0,23,.2)" class="rb-orq-pulse"/>
      <rect x="170" y="207" width="50" height="4" rx="2" fill="rgba(188,0,23,.15)" class="rb-orq-pulse d1"/>
      <rect x="228" y="207" width="60" height="4" rx="2" fill="rgba(188,0,23,.12)" class="rb-orq-pulse d2"/>
      <rect x="170" y="218" width="35" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="213" y="218" width="55" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="170" y="232" width="90" height="4" rx="2" fill="rgba(188,0,23,.08)"/>
      <rect x="268" y="232" width="40" height="4" rx="2" fill="rgba(188,0,23,.08)"/>
      <line x1="85" y1="123" x2="185" y2="178" stroke="rgba(188,0,23,.18)" stroke-width="1.5" class="rb-orq-flow"/>
      <line x1="230" y1="123" x2="230" y2="178" stroke="rgba(43,127,255,.18)" stroke-width="1.5" class="rb-orq-flow d1"/>
      <line x1="375" y1="123" x2="275" y2="178" stroke="rgba(0,212,255,.15)" stroke-width="1.5" class="rb-orq-flow d2"/>
      <rect x="70" y="318" width="90" height="50" rx="12" fill="rgba(188,0,23,.05)" stroke="rgba(188,0,23,.18)" stroke-width="1.5"/>
      <circle cx="90" cy="337" r="5" fill="rgba(188,0,23,.3)" class="rb-orq-pulse d1"/>
      <rect x="102" y="333" width="40" height="4" rx="2" fill="rgba(188,0,23,.15)"/>
      <rect x="82" y="348" width="60" height="4" rx="2" fill="rgba(188,0,23,.1)"/>
      <rect x="300" y="318" width="90" height="50" rx="12" fill="rgba(43,127,255,.05)" stroke="rgba(43,127,255,.18)" stroke-width="1.5"/>
      <circle cx="320" cy="337" r="5" fill="rgba(43,127,255,.3)" class="rb-orq-pulse d3"/>
      <rect x="332" y="333" width="40" height="4" rx="2" fill="rgba(43,127,255,.15)"/>
      <rect x="312" y="348" width="55" height="4" rx="2" fill="rgba(43,127,255,.1)"/>
      <line x1="185" y1="256" x2="115" y2="318" stroke="rgba(188,0,23,.15)" stroke-width="1.5" class="rb-orq-flow d2"/>
      <line x1="275" y1="256" x2="345" y2="318" stroke="rgba(43,127,255,.15)" stroke-width="1.5" class="rb-orq-flow"/>
      <rect x="196" y="332" width="14" height="18" rx="3" fill="rgba(188,0,23,.15)" class="rb-orq-pulse"/>
      <rect x="216" y="324" width="14" height="26" rx="3" fill="rgba(188,0,23,.2)" class="rb-orq-pulse d1"/>
      <rect x="236" y="328" width="14" height="22" rx="3" fill="rgba(188,0,23,.15)" class="rb-orq-pulse d2"/>
    </svg>
  </div>
"""

# ══════════════════════════════════════════════════════════════
# 5. XPERIENCE — Animated form builder
# ══════════════════════════════════════════════════════════════
XPR_CSS = """
/* XPERIENCE HERO VIZ */
.rb-hero__viz{position:absolute;right:0;top:50%;transform:translateY(-50%);width:440px;height:440px;pointer-events:none;z-index:0;opacity:.72;}
.rb-xpr-field{animation:xpr-appear 7s ease-in-out infinite;}
.rb-xpr-field.f2{animation-delay:1s;}.rb-xpr-field.f3{animation-delay:2s;}.rb-xpr-field.f4{animation-delay:3s;}
@keyframes xpr-appear{0%,95%,100%{opacity:0;transform:translateX(10px);}15%,80%{opacity:1;transform:translateX(0);}}
.rb-xpr-btn-glow{animation:xpr-btn 3s ease-in-out infinite;}
@keyframes xpr-btn{0%,100%{fill:rgba(188,0,23,.1);}50%{fill:rgba(188,0,23,.22);}}
.rb-xpr-check{animation:xpr-check 3s ease-in-out infinite;}
.rb-xpr-check.ck2{animation-delay:1.5s;}
@keyframes xpr-check{0%,100%{opacity:.4;}50%{opacity:1;}}
.rb-xpr-float{animation:xpr-float 4s ease-in-out infinite;}
.rb-xpr-float.fl2{animation-delay:2s;}
@keyframes xpr-float{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@media(max-width:900px){.rb-hero__viz{display:none;}}
"""

XPR_HTML = """  <div class="rb-hero__viz" aria-hidden="true">
    <svg viewBox="0 0 440 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect x="80" y="55" width="280" height="326" rx="20" fill="rgba(255,255,255,.85)" stroke="rgba(188,0,23,.15)" stroke-width="2" class="rb-xpr-float"/>
      <rect x="80" y="55" width="280" height="44" rx="20" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.12)" stroke-width="1"/>
      <rect x="80" y="75" width="280" height="24" fill="rgba(188,0,23,.08)"/>
      <circle cx="106" cy="77" r="6" fill="rgba(188,0,23,.3)"/>
      <circle cx="126" cy="77" r="6" fill="rgba(255,180,0,.3)"/>
      <circle cx="146" cy="77" r="6" fill="rgba(0,200,80,.3)"/>
      <rect x="168" y="73" width="100" height="8" rx="4" fill="rgba(188,0,23,.15)"/>
      <rect x="104" y="122" width="150" height="9" rx="4" fill="rgba(188,0,23,.25)"/>
      <rect x="104" y="138" width="100" height="6" rx="3" fill="rgba(0,0,0,.08)"/>
      <g class="rb-xpr-field">
        <rect x="104" y="162" width="232" height="36" rx="8" fill="rgba(255,255,255,.9)" stroke="rgba(188,0,23,.3)" stroke-width="1.5"/>
        <rect x="116" y="177" width="60" height="6" rx="3" fill="rgba(0,0,0,.12)"/>
      </g>
      <g class="rb-xpr-field f2">
        <rect x="104" y="210" width="232" height="36" rx="8" fill="rgba(255,255,255,.9)" stroke="rgba(188,0,23,.2)" stroke-width="1.5"/>
        <rect x="116" y="225" width="80" height="6" rx="3" fill="rgba(0,0,0,.1)"/>
      </g>
      <g class="rb-xpr-field f3">
        <rect x="104" y="260" width="14" height="14" rx="3" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.3)" stroke-width="1.5"/>
        <polyline points="107,267 111,271 117,263" fill="none" stroke="rgba(188,0,23,.7)" stroke-width="2" stroke-linecap="round" class="rb-xpr-check"/>
        <rect x="126" y="263" width="70" height="6" rx="3" fill="rgba(0,0,0,.1)"/>
        <rect x="104" y="282" width="14" height="14" rx="3" fill="rgba(188,0,23,.08)" stroke="rgba(188,0,23,.3)" stroke-width="1.5"/>
        <polyline points="107,289 111,293 117,285" fill="none" stroke="rgba(188,0,23,.5)" stroke-width="2" stroke-linecap="round" class="rb-xpr-check ck2"/>
        <rect x="126" y="285" width="55" height="6" rx="3" fill="rgba(0,0,0,.08)"/>
      </g>
      <g class="rb-xpr-field f4">
        <rect x="104" y="314" width="232" height="42" rx="10" class="rb-xpr-btn-glow" stroke="rgba(188,0,23,.35)" stroke-width="1.5"/>
        <rect x="158" y="328" width="84" height="8" rx="4" fill="rgba(188,0,23,.45)"/>
      </g>
      <g class="rb-xpr-float fl2">
        <rect x="292" y="26" width="100" height="26" rx="13" fill="rgba(0,200,80,.1)" stroke="rgba(0,200,80,.28)" stroke-width="1.5"/>
        <circle cx="312" cy="39" r="5" fill="rgba(0,200,80,.4)" class="rb-xpr-check"/>
        <rect x="324" y="36" width="50" height="5" rx="2" fill="rgba(0,150,60,.3)"/>
      </g>
      <g class="rb-xpr-float">
        <rect x="42" y="294" width="26" height="26" rx="8" fill="rgba(43,127,255,.1)" stroke="rgba(43,127,255,.25)" stroke-width="1.5"/>
        <path d="M 50 302 L 55 312 L 60 302" fill="none" stroke="rgba(43,127,255,.5)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </svg>
  </div>
"""

# ══════════════════════════════════════════════════════════════
# PATCHER
# ══════════════════════════════════════════════════════════════
patches = [
    ('saturn-studio.html', SATURN_CSS, SATURN_HTML),
    ('rpa-studio.html',    RPA_CSS,    RPA_HTML),
    ('ai-studio.html',     AI_CSS,     AI_HTML),
    ('orquestador.html',   ORQ_CSS,    ORQ_HTML),
    ('xperience.html',     XPR_CSS,    XPR_HTML),
]

for fname, css, html in patches:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS before </style>
    if 'rb-hero__viz' not in content:
        content = content.replace('</style>', css + '\n</style>', 1)
    else:
        print(f'{fname}: CSS already present')

    # Inject HTML after particles div
    marker = '<div class="rb-hero__particles"></div>'
    if 'rb-hero__viz' not in content and marker in content:
        content = content.replace(marker, marker + '\n' + html.rstrip(), 1)
    elif marker in content and 'rb-hero__viz' not in content:
        content = content.replace(marker, marker + '\n' + html.rstrip(), 1)
    elif 'rb-hero__viz' in content and 'rb-viz-wrap' not in content and 'rb-rpa-gear' not in content:
        # CSS was already there but we need to check the HTML too
        pass

    # Re-check: if viz HTML not present, inject it
    if 'rb-hero__viz' not in content:
        if marker in content:
            content = content.replace(marker, marker + '\n' + html.rstrip(), 1)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'{fname}: done (viz present: {"rb-hero__viz" in content})')

print('\nAll files patched.')
