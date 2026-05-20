import re, os
os.chdir(r'C:\Users\frani\.claude\worktrees\quirky-aryabhata-b7856b')

# CSS compartido para el nuevo hero con video
SHARED_HERO_CSS = """
/* HERO VIDEO LAYOUT */
.rb-hero__grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center;position:relative;z-index:1;width:100%;}
.rb-hero__copy{display:flex;flex-direction:column;gap:0;}
.rb-hero__video-wrap{display:flex;align-items:center;justify-content:center;}
.rb-hero__video-wrap video{width:100%;max-width:520px;border-radius:20px;display:block;}
@media(max-width:900px){
  .rb-hero__grid{grid-template-columns:1fr;gap:32px;}
  .rb-hero__video-wrap{display:none;}
}
"""

# CSS a ELIMINAR (regex patterns)
REMOVE_CSS_PATTERNS = [
    r'/\* SATURN HERO VIZ \*/.*?@media\(max-width:900px\)\{\.rb-hero__viz\{display:none;\}\}',
    r'/\* RPA HERO VIZ \*/.*?@media\(max-width:900px\)\{\.rb-hero__viz\{display:none;\}\}',
    r'/\* AI STUDIO HERO VIZ \*/.*?@media\(max-width:900px\)\{\.rb-hero__viz\{display:none;\}\}',
    r'/\* ORQUESTADOR HERO VIZ \*/.*?@media\(max-width:900px\)\{\.rb-hero__viz\{display:none;\}\}',
    r'/\* XPERIENCE HERO VIZ \*/.*?@media\(max-width:900px\)\{\.rb-hero__viz\{display:none;\}\}',
]

VIDEO_SRC = {
    'saturn-studio.html': 'assets/images/anims/saturn.mp4',
    'rpa-studio.html':    'assets/images/anims/rpa.mp4',
    'ai-studio.html':     'assets/images/anims/ai.mp4',
    'orquestador.html':   'assets/images/anims/orquestador.mp4',
    'xperience.html':     'assets/images/anims/xperience.mp4',
}

files = list(VIDEO_SRC.keys())

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove old viz CSS
    for pat in REMOVE_CSS_PATTERNS:
        content = re.sub(pat, '', content, flags=re.DOTALL)

    # 2. Remove old viz HTML div
    content = re.sub(
        r'\s*<div class="rb-hero__viz"[^>]*>.*?</div>\s*(?=\n\s*<div class="container">)',
        '\n',
        content,
        flags=re.DOTALL
    )

    # 3. Inject shared CSS if not present
    if 'rb-hero__grid' not in content:
        content = content.replace('</style>', SHARED_HERO_CSS + '\n</style>', 1)

    # 4. Wrap hero content in 2-column grid + add video
    vid = VIDEO_SRC[fname]
    video_html = f'''<div class="rb-hero__video-wrap">
        <video autoplay loop muted playsinline>
          <source src="{vid}" type="video/mp4">
        </video>
      </div>'''

    # Find the hero content div and wrap it
    # Pattern: <div class="rb-hero__content"> ... </div>\n  </div>\n</section> (last </div> of container, then section)
    def wrap_hero(m):
        inner = m.group(0)
        # Replace <div class="rb-hero__content"> wrapper with grid
        inner = re.sub(
            r'<div class="rb-hero__content">(.*?)</div>(\s*</div>\s*</section>)',
            lambda m2: (
                '<div class="rb-hero__grid">\n      '
                '<div class="rb-hero__copy">' + m2.group(1) + '</div>\n      '
                + video_html + '\n    </div>'
                + m2.group(2)
            ),
            inner,
            flags=re.DOTALL
        )
        return inner

    # Apply the transformation to the hero section
    content = re.sub(
        r'<!-- HERO -->.*?</section>',
        wrap_hero,
        content,
        count=1,
        flags=re.DOTALL
    )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

    has_grid  = 'rb-hero__grid' in content
    has_video = 'rb-hero__video-wrap' in content
    has_viz   = 'class="rb-hero__viz"' in content
    print(f'{fname}: grid={has_grid} video={has_video} old_viz={has_viz}')

print('Done.')
