import os

def create_monochrome_pack():
    os.makedirs("brand_kite", exist_ok=True)

    # 1. Monochromatické primární logo - ČERNÉ (transparentní pozadí)
    # Využívá precizní negativní prostor (řezy), aby křídla vynikla i v 1 jediné barvě!
    mono_primary_black = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="100%" height="100%">
  <!-- Monochrome Black (Transparent Background) -->
  <!-- Target reticle circles -->
  <circle cx="160" cy="160" r="110" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="6 8" opacity="0.4"/>
  <circle cx="160" cy="160" r="85" fill="none" stroke="#000000" stroke-width="1.5" opacity="0.3"/>

  <!-- Icon Section with Negative Space & Hatching/Tone -->
  <g transform="translate(10, 0)">
    <!-- Left Wing (Solid Black) -->
    <path d="M 150 55 L 70 175 L 138 155 L 150 245 Z" fill="#000000"/>
    <!-- Right Wing (Toned / 45% black tint for facet depth) -->
    <path d="M 150 55 L 230 175 L 162 155 L 150 245 Z" fill="#000000" opacity="0.55"/>
    <!-- Center Spine (White / Cutout line) -->
    <polygon points="150,68 155,160 150,230 145,160" fill="#FFFFFF"/>
    <!-- Center Reticle Ring -->
    <polygon points="150,140 162,158 150,176 138,158" fill="#FFFFFF" stroke="#000000" stroke-width="3"/>
    <circle cx="150" cy="158" r="4" fill="#000000"/>
  </g>

  <!-- Typography: KITE (Solid Black) -->
  <g transform="translate(300, 195)" fill="#000000">
    <!-- Letter K -->
    <polygon points="20,-105 55,-105 55,-40 100,-105 145,-105 90,-25 150,60 105,60 60,-5 55,2 55,60 20,60"/>
    <!-- Letter I -->
    <polygon points="180,-105 215,-105 215,60 180,60"/>
    <polygon points="180,-122 215,-122 205,-110 180,-110"/>
    <!-- Letter T -->
    <polygon points="245,-105 350,-105 350,-75 315,-75 315,60 280,60 280,-75 245,-75"/>
    <!-- Letter E -->
    <polygon points="380,-105 470,-105 470,-75 415,-75 415,-38 460,-38 460,-10 415,-10 415,30 475,30 475,60 380,60"/>
  </g>

  <!-- Badge: COACHING (Black Outline & Text) -->
  <g transform="translate(805, 110)">
    <rect x="0" y="0" width="150" height="90" rx="12" fill="none" stroke="#000000" stroke-width="2.5"/>
    <text x="75" y="42" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="20" font-weight="900" fill="#000000" text-anchor="middle" letter-spacing="4">COACH</text>
    <text x="75" y="70" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="13" font-weight="700" fill="#000000" text-anchor="middle" letter-spacing="3">ACADEMY</text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_monochrome_black.svg", "w", encoding="utf-8") as f:
        f.write(mono_primary_black)

    # 2. Monochromatické primární logo - BÍLÉ (transparentní pozadí pro tmavá pozadí)
    mono_primary_white = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="100%" height="100%">
  <!-- Monochrome White (Transparent Background) -->
  <circle cx="160" cy="160" r="110" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="6 8" opacity="0.4"/>
  <circle cx="160" cy="160" r="85" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.3"/>

  <g transform="translate(10, 0)">
    <!-- Left Wing (Solid White) -->
    <path d="M 150 55 L 70 175 L 138 155 L 150 245 Z" fill="#FFFFFF"/>
    <!-- Right Wing (Toned White / 60% opacity) -->
    <path d="M 150 55 L 230 175 L 162 155 L 150 245 Z" fill="#FFFFFF" opacity="0.6"/>
    <!-- Center Spine (Cutout) -->
    <polygon points="150,68 155,160 150,230 145,160" fill="#000000"/>
    <!-- Center Reticle -->
    <polygon points="150,140 162,158 150,176 138,158" fill="#000000" stroke="#FFFFFF" stroke-width="3"/>
    <circle cx="150" cy="158" r="4" fill="#FFFFFF"/>
  </g>

  <!-- Typography: KITE (Solid White) -->
  <g transform="translate(300, 195)" fill="#FFFFFF">
    <polygon points="20,-105 55,-105 55,-40 100,-105 145,-105 90,-25 150,60 105,60 60,-5 55,2 55,60 20,60"/>
    <polygon points="180,-105 215,-105 215,60 180,60"/>
    <polygon points="180,-122 215,-122 205,-110 180,-110"/>
    <polygon points="245,-105 350,-105 350,-75 315,-75 315,60 280,60 280,-75 245,-75"/>
    <polygon points="380,-105 470,-105 470,-75 415,-75 415,-38 460,-38 460,-10 415,-10 415,30 475,30 475,60 380,60"/>
  </g>

  <g transform="translate(805, 110)">
    <rect x="0" y="0" width="150" height="90" rx="12" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
    <text x="75" y="42" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="20" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="4">COACH</text>
    <text x="75" y="70" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">ACADEMY</text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_monochrome_white.svg", "w", encoding="utf-8") as f:
        f.write(mono_primary_white)

    # 3. Monochromatické logo S HESLEM - ČERNÉ (Transparent background)
    mono_slogan_black = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" width="100%" height="100%">
  <!-- Icon Section -->
  <g transform="translate(60, 40)">
    <circle cx="120" cy="130" r="95" fill="none" stroke="#000000" stroke-width="2" stroke-dasharray="4 6" opacity="0.35"/>
    <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#000000"/>
    <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#000000" opacity="0.55"/>
    <polygon points="120,52 125,130 120,195 115,130" fill="#FFFFFF"/>
    <polygon points="120,115 131,130 120,145 109,130" fill="#FFFFFF" stroke="#000000" stroke-width="2.5"/>
    <circle cx="120" cy="130" r="3.5" fill="#000000"/>
  </g>

  <!-- Typography: KITE -->
  <g transform="translate(320, 190)" fill="#000000">
    <polygon points="10,-95 40,-95 40,-35 80,-95 120,-95 72,-20 125,55 85,55 45,-5 40,2 40,55 10,55"/>
    <polygon points="150,-95 180,-95 180,55 150,55"/>
    <polygon points="150,-110 180,-110 172,-100 150,-100"/>
    <polygon points="210,-95 300,-95 300,-70 270,-70 270,55 240,55 240,-70 210,-70"/>
    <polygon points="325,-95 405,-95 405,-70 355,-70 355,-35 395,-35 395,-10 355,-10 355,30 410,30 410,55 325,55"/>

    <text x="440" y="-15" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="28" font-weight="900" fill="#000000" letter-spacing="6">COACHING</text>
    <text x="440" y="25" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="14" font-weight="700" fill="#000000" opacity="0.6" letter-spacing="4">MASTER TIER PLATFORM</text>
  </g>

  <!-- Divider Line -->
  <line x1="120" y1="290" x2="880" y2="290" stroke="#000000" stroke-width="2" opacity="0.3"/>

  <!-- Slogan / Heslo -->
  <g transform="translate(500, 345)">
    <text x="0" y="0" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="22" font-weight="900" fill="#000000" text-anchor="middle" letter-spacing="9">
      OUTSPACE. OUTKITE. OUTCLIMB.
    </text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_monochrome_with_slogan_black.svg", "w", encoding="utf-8") as f:
        f.write(mono_slogan_black)

    # 4. Monochromatické logo S HESLEM - BÍLÉ (Transparent background)
    mono_slogan_white = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" width="100%" height="100%">
  <!-- Icon Section -->
  <g transform="translate(60, 40)">
    <circle cx="120" cy="130" r="95" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="4 6" opacity="0.4"/>
    <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#FFFFFF"/>
    <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#FFFFFF" opacity="0.6"/>
    <polygon points="120,52 125,130 120,195 115,130" fill="#000000"/>
    <polygon points="120,115 131,130 120,145 109,130" fill="#000000" stroke="#FFFFFF" stroke-width="2.5"/>
    <circle cx="120" cy="130" r="3.5" fill="#FFFFFF"/>
  </g>

  <!-- Typography: KITE -->
  <g transform="translate(320, 190)" fill="#FFFFFF">
    <polygon points="10,-95 40,-95 40,-35 80,-95 120,-95 72,-20 125,55 85,55 45,-5 40,2 40,55 10,55"/>
    <polygon points="150,-95 180,-95 180,55 150,55"/>
    <polygon points="150,-110 180,-110 172,-100 150,-100"/>
    <polygon points="210,-95 300,-95 300,-70 270,-70 270,55 240,55 240,-70 210,-70"/>
    <polygon points="325,-95 405,-95 405,-70 355,-70 355,-35 395,-35 395,-10 355,-10 355,30 410,30 410,55 325,55"/>

    <text x="440" y="-15" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="28" font-weight="900" fill="#FFFFFF" letter-spacing="6">COACHING</text>
    <text x="440" y="25" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" opacity="0.7" letter-spacing="4">MASTER TIER PLATFORM</text>
  </g>

  <!-- Divider Line -->
  <line x1="120" y1="290" x2="880" y2="290" stroke="#FFFFFF" stroke-width="2" opacity="0.3"/>

  <!-- Slogan / Heslo -->
  <g transform="translate(500, 345)">
    <text x="0" y="0" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="22" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="9">
      OUTSPACE. OUTKITE. OUTCLIMB.
    </text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_monochrome_with_slogan_white.svg", "w", encoding="utf-8") as f:
        f.write(mono_slogan_white)

    # 5. Monochromatická standalone IKONA - ČERNÁ (Transparent)
    mono_icon_black = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <!-- Reticle -->
  <circle cx="250" cy="250" r="190" fill="none" stroke="#000000" stroke-width="3" stroke-dasharray="8 8" opacity="0.35"/>
  <circle cx="250" cy="250" r="140" fill="none" stroke="#000000" stroke-width="2" opacity="0.25"/>
  <line x1="250" y1="40" x2="250" y2="70" stroke="#000000" stroke-width="4" stroke-linecap="round"/>
  <line x1="250" y1="430" x2="250" y2="460" stroke="#000000" stroke-width="4" stroke-linecap="round"/>
  <line x1="40" y1="250" x2="70" y2="250" stroke="#000000" stroke-width="4" stroke-linecap="round"/>
  <line x1="430" y1="250" x2="460" y2="250" stroke="#000000" stroke-width="4" stroke-linecap="round"/>

  <!-- Wings -->
  <path d="M 250 80 L 110 270 L 225 240 L 250 380 Z" fill="#000000"/>
  <path d="M 250 80 L 390 270 L 275 240 L 250 380 Z" fill="#000000" opacity="0.55"/>
  <polygon points="250,95 260,245 250,360 240,245" fill="#FFFFFF"/>
  <polygon points="250,215 270,245 250,275 230,245" fill="#FFFFFF" stroke="#000000" stroke-width="4"/>
  <circle cx="250" cy="245" r="5" fill="#000000"/>
</svg>'''
    with open("brand_kite/kite_logo_icon_monochrome_black.svg", "w", encoding="utf-8") as f:
        f.write(mono_icon_black)

    # 6. Monochromatická standalone IKONA - BÍLÁ (Transparent)
    mono_icon_white = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <!-- Reticle -->
  <circle cx="250" cy="250" r="190" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="8 8" opacity="0.4"/>
  <circle cx="250" cy="250" r="140" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.3"/>
  <line x1="250" y1="40" x2="250" y2="70" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <line x1="250" y1="430" x2="250" y2="460" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <line x1="40" y1="250" x2="70" y2="250" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <line x1="430" y1="250" x2="460" y2="250" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>

  <!-- Wings -->
  <path d="M 250 80 L 110 270 L 225 240 L 250 380 Z" fill="#FFFFFF"/>
  <path d="M 250 80 L 390 270 L 275 240 L 250 380 Z" fill="#FFFFFF" opacity="0.6"/>
  <polygon points="250,95 260,245 250,360 240,245" fill="#000000"/>
  <polygon points="250,215 270,245 250,275 230,245" fill="#000000" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="250" cy="245" r="5" fill="#FFFFFF"/>
</svg>'''
    with open("brand_kite/kite_logo_icon_monochrome_white.svg", "w", encoding="utf-8") as f:
        f.write(mono_icon_white)

create_monochrome_pack()
print("All Monochrome variants created successfully!")
