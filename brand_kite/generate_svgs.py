import os

def create_svgs():
    os.makedirs("brand_kite", exist_ok=True)

    # 1. Standalone Icon (Icon only)
    icon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="gradCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#0077FE"/>
    </linearGradient>
    <linearGradient id="gradPurple" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7928CA"/>
      <stop offset="100%" stop-color="#FF0080"/>
    </linearGradient>
    <linearGradient id="gradGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#FF8800"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <style>
    .bg { fill: #0B0E14; }
    .crosshair { stroke: #00F0FF; stroke-width: 3; stroke-dasharray: 6 6; opacity: 0.4; }
  </style>
  <rect width="500" height="500" rx="100" class="bg"/>
  
  <!-- Spacing / Range reticle circle -->
  <circle cx="250" cy="250" r="190" fill="none" class="crosshair"/>
  <circle cx="250" cy="250" r="140" fill="none" stroke="#00F0FF" stroke-width="1.5" opacity="0.2"/>
  
  <!-- Targeting tick marks -->
  <line x1="250" y1="40" x2="250" y2="70" stroke="#00F0FF" stroke-width="4" stroke-linecap="round"/>
  <line x1="250" y1="430" x2="250" y2="460" stroke="#00F0FF" stroke-width="4" stroke-linecap="round"/>
  <line x1="40" y1="250" x2="70" y2="250" stroke="#00F0FF" stroke-width="4" stroke-linecap="round"/>
  <line x1="430" y1="250" x2="460" y2="250" stroke="#00F0FF" stroke-width="4" stroke-linecap="round"/>

  <!-- KITE Wing / Arrow Emblem: The aerodynamic stealth kite & crosshair vector -->
  <g filter="url(#glow)">
    <!-- Main Left Wing / Stutter Step Arrow -->
    <path d="M 250 80 L 110 270 L 225 240 L 250 380 Z" fill="url(#gradCyan)"/>
    <!-- Main Right Wing / Forward Thrust -->
    <path d="M 250 80 L 390 270 L 275 240 L 250 380 Z" fill="url(#gradPurple)"/>
    <!-- Center Precision Spine -->
    <polygon points="250,95 260,245 250,360 240,245" fill="#FFFFFF" opacity="0.95"/>
    <!-- Kinetic Attack-Move Core (Center Diamond) -->
    <polygon points="250,215 270,245 250,275 230,245" fill="#0B0E14" stroke="#00F0FF" stroke-width="4"/>
    <circle cx="250" cy="245" r="5" fill="#00F0FF"/>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_icon.svg", "w", encoding="utf-8") as f:
        f.write(icon_svg)

    # 2. Primary Horizontal Logo (Icon + KITE Typography)
    primary_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="100%" height="100%">
  <defs>
    <linearGradient id="pGradCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#0080FF"/>
    </linearGradient>
    <linearGradient id="pGradPurple" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8A2BE2"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
    <filter id="pGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="1000" height="320" rx="30" fill="#090D16"/>

  <!-- Background decorative range grid -->
  <line x1="40" y1="160" x2="960" y2="160" stroke="#00F0FF" stroke-width="1" opacity="0.1"/>
  <circle cx="160" cy="160" r="110" fill="none" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4 6" opacity="0.3"/>
  <circle cx="160" cy="160" r="85" fill="none" stroke="#8A2BE2" stroke-width="1" opacity="0.25"/>

  <!-- Icon Section -->
  <g transform="translate(10, 0)">
    <!-- Wings -->
    <path d="M 150 55 L 70 175 L 138 155 L 150 245 Z" fill="url(#pGradCyan)" filter="url(#pGlow)"/>
    <path d="M 150 55 L 230 175 L 162 155 L 150 245 Z" fill="url(#pGradPurple)" filter="url(#pGlow)"/>
    <!-- Center Spine -->
    <polygon points="150,68 156,160 150,230 144,160" fill="#FFFFFF"/>
    <!-- Core Reticle -->
    <polygon points="150,140 162,158 150,176 138,158" fill="#090D16" stroke="#00F0FF" stroke-width="3"/>
    <circle cx="150" cy="158" r="3.5" fill="#00F0FF"/>
  </g>

  <!-- Typography: KITE -->
  <g transform="translate(300, 195)">
    <!-- Letter K -->
    <polygon points="20,-105 55,-105 55,-40 100,-105 145,-105 90,-25 150,60 105,60 60,-5 55,2 55,60 20,60" fill="#FFFFFF"/>
    <polygon points="100,-105 145,-105 90,-25" fill="url(#pGradCyan)"/>
    <polygon points="90,-25 150,60 105,60 60,-5" fill="url(#pGradPurple)"/>

    <!-- Letter I -->
    <polygon points="180,-105 215,-105 215,60 180,60" fill="#FFFFFF"/>
    <!-- Cyan top indicator pip -->
    <polygon points="180,-122 215,-122 205,-110 180,-110" fill="url(#pGradCyan)"/>

    <!-- Letter T -->
    <polygon points="245,-105 350,-105 350,-75 315,-75 315,60 280,60 280,-75 245,-75" fill="#FFFFFF"/>
    <polygon points="315,-105 350,-105 350,-75 315,-75" fill="url(#pGradCyan)"/>

    <!-- Letter E -->
    <polygon points="380,-105 470,-105 470,-75 415,-75 415,-38 460,-38 460,-10 415,-10 415,30 475,30 475,60 380,60" fill="#FFFFFF"/>
    <polygon points="415,-10 460,-10 460,-38 415,-38" fill="url(#pGradPurple)"/>
  </g>

  <!-- Subtitle Tag / Badge: COACHING -->
  <g transform="translate(805, 110)">
    <rect x="0" y="0" width="150" height="90" rx="12" fill="#131B2E" stroke="#00F0FF" stroke-width="1.5"/>
    <text x="75" y="42" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="20" font-weight="900" fill="#00F0FF" text-anchor="middle" letter-spacing="4">COACH</text>
    <text x="75" y="70" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="#EC4899" text-anchor="middle" letter-spacing="3">ACADEMY</text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_primary.svg", "w", encoding="utf-8") as f:
        f.write(primary_svg)

    # 3. Logo with Slogan (Heslo: OUTSPACE. OUTKITE. OUTCLIMB.)
    slogan_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" width="100%" height="100%">
  <defs>
    <linearGradient id="sGradCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#0080FF"/>
    </linearGradient>
    <linearGradient id="sGradPurple" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8A2BE2"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
    <filter id="sGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="1000" height="400" rx="36" fill="#080C14"/>

  <!-- Ambient light -->
  <circle cx="200" cy="180" r="160" fill="#00F0FF" opacity="0.05" filter="url(#sGlow)"/>
  <circle cx="750" cy="220" r="140" fill="#EC4899" opacity="0.05" filter="url(#sGlow)"/>

  <!-- Icon Section -->
  <g transform="translate(60, 40)">
    <circle cx="120" cy="130" r="95" fill="none" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4 6" opacity="0.35"/>
    <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="url(#sGradCyan)" filter="url(#sGlow)"/>
    <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="url(#sGradPurple)" filter="url(#sGlow)"/>
    <polygon points="120,52 125,130 120,195 115,130" fill="#FFFFFF"/>
    <polygon points="120,115 131,130 120,145 109,130" fill="#080C14" stroke="#00F0FF" stroke-width="2.5"/>
    <circle cx="120" cy="130" r="3" fill="#00F0FF"/>
  </g>

  <!-- Typography: KITE -->
  <g transform="translate(320, 190)">
    <!-- Letter K -->
    <polygon points="10,-95 40,-95 40,-35 80,-95 120,-95 72,-20 125,55 85,55 45,-5 40,2 40,55 10,55" fill="#FFFFFF"/>
    <polygon points="80,-95 120,-95 72,-20" fill="url(#sGradCyan)"/>
    <!-- Letter I -->
    <polygon points="150,-95 180,-95 180,55 150,55" fill="#FFFFFF"/>
    <polygon points="150,-110 180,-110 172,-100 150,-100" fill="url(#sGradCyan)"/>
    <!-- Letter T -->
    <polygon points="210,-95 300,-95 300,-70 270,-70 270,55 240,55 240,-70 210,-70" fill="#FFFFFF"/>
    <!-- Letter E -->
    <polygon points="325,-95 405,-95 405,-70 355,-70 355,-35 395,-35 395,-10 355,-10 355,30 410,30 410,55 325,55" fill="#FFFFFF"/>
    <polygon points="355,-10 395,-10 395,-35 355,-35" fill="url(#sGradPurple)"/>

    <!-- Secondary Word: COACHING -->
    <text x="440" y="-15" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="28" font-weight="900" fill="#00F0FF" letter-spacing="6">COACHING</text>
    <text x="440" y="25" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="14" font-weight="700" fill="#94A3B8" letter-spacing="4">MASTER TIER PLATFORM</text>
  </g>

  <!-- Divider Line -->
  <line x1="120" y1="290" x2="880" y2="290" stroke="#1E293B" stroke-width="2"/>
  <line x1="300" y1="290" x2="700" y2="290" stroke="url(#sGradCyan)" stroke-width="2"/>

  <!-- Slogan / Heslo -->
  <g transform="translate(500, 345)">
    <text x="0" y="0" font-family="'Segoe UI', Montserrat, Arial, sans-serif" font-size="22" font-weight="800" text-anchor="middle" letter-spacing="9">
      <tspan fill="#00F0FF">OUTSPACE.</tspan>
      <tspan fill="#FFFFFF"> OUTKITE.</tspan>
      <tspan fill="#EC4899"> OUTCLIMB.</tspan>
    </text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_with_slogan.svg", "w", encoding="utf-8") as f:
        f.write(slogan_svg)

    # 4. Light Background Logo (Bílé / světlé neutrální pozadí)
    light_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="100%" height="100%">
  <defs>
    <linearGradient id="lGradCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00A3C4"/>
      <stop offset="100%" stop-color="#0052CC"/>
    </linearGradient>
    <linearGradient id="lGradPurple" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6B21A8"/>
      <stop offset="100%" stop-color="#DB2777"/>
    </linearGradient>
  </defs>
  <!-- Neutral Pure White / Light Slate Background -->
  <rect width="1000" height="320" rx="30" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="3"/>

  <!-- Background subtle grid -->
  <line x1="40" y1="160" x2="960" y2="160" stroke="#0F172A" stroke-width="1" opacity="0.08"/>
  <circle cx="160" cy="160" r="105" fill="none" stroke="#00A3C4" stroke-width="1.5" stroke-dasharray="4 6" opacity="0.3"/>

  <!-- Icon Section -->
  <g transform="translate(10, 0)">
    <path d="M 150 55 L 70 175 L 138 155 L 150 245 Z" fill="url(#lGradCyan)"/>
    <path d="M 150 55 L 230 175 L 162 155 L 150 245 Z" fill="url(#lGradPurple)"/>
    <polygon points="150,68 156,160 150,230 144,160" fill="#FFFFFF"/>
    <polygon points="150,140 162,158 150,176 138,158" fill="#FFFFFF" stroke="#00A3C4" stroke-width="3"/>
    <circle cx="150" cy="158" r="3.5" fill="#00A3C4"/>
  </g>

  <!-- Typography: KITE in Dark Slate (#0F172A) -->
  <g transform="translate(300, 195)">
    <!-- Letter K -->
    <polygon points="20,-105 55,-105 55,-40 100,-105 145,-105 90,-25 150,60 105,60 60,-5 55,2 55,60 20,60" fill="#0F172A"/>
    <polygon points="100,-105 145,-105 90,-25" fill="url(#lGradCyan)"/>

    <!-- Letter I -->
    <polygon points="180,-105 215,-105 215,60 180,60" fill="#0F172A"/>
    <polygon points="180,-122 215,-122 205,-110 180,-110" fill="url(#lGradCyan)"/>

    <!-- Letter T -->
    <polygon points="245,-105 350,-105 350,-75 315,-75 315,60 280,60 280,-75 245,-75" fill="#0F172A"/>

    <!-- Letter E -->
    <polygon points="380,-105 470,-105 470,-75 415,-75 415,-38 460,-38 460,-10 415,-10 415,30 475,30 475,60 380,60" fill="#0F172A"/>
    <polygon points="415,-10 460,-10 460,-38 415,-38" fill="url(#lGradPurple)"/>
  </g>

  <!-- Badge: COACHING -->
  <g transform="translate(805, 110)">
    <rect x="0" y="0" width="150" height="90" rx="12" fill="#F1F5F9" stroke="#00A3C4" stroke-width="1.5"/>
    <text x="75" y="42" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="20" font-weight="900" fill="#0077FE" text-anchor="middle" letter-spacing="4">COACH</text>
    <text x="75" y="70" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="#6B21A8" text-anchor="middle" letter-spacing="3">ACADEMY</text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)

    # 5. Monochrome Black (Černobílé - černý tisk)
    mono_black_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="100%" height="100%">
  <rect width="1000" height="320" rx="30" fill="#FFFFFF"/>
  <g transform="translate(10, 0)">
    <path d="M 150 55 L 70 175 L 138 155 L 150 245 Z" fill="#000000"/>
    <path d="M 150 55 L 230 175 L 162 155 L 150 245 Z" fill="#555555"/>
    <polygon points="150,68 156,160 150,230 144,160" fill="#FFFFFF"/>
    <circle cx="150" cy="158" r="5" fill="#000000"/>
  </g>
  <g transform="translate(300, 195)" fill="#000000">
    <polygon points="20,-105 55,-105 55,-40 100,-105 145,-105 90,-25 150,60 105,60 60,-5 55,2 55,60 20,60"/>
    <polygon points="180,-105 215,-105 215,60 180,60"/>
    <polygon points="245,-105 350,-105 350,-75 315,-75 315,60 280,60 280,-75 245,-75"/>
    <polygon points="380,-105 470,-105 470,-75 415,-75 415,-38 460,-38 460,-10 415,-10 415,30 475,30 475,60 380,60"/>
  </g>
  <g transform="translate(805, 110)">
    <rect x="0" y="0" width="150" height="90" rx="12" fill="none" stroke="#000000" stroke-width="2"/>
    <text x="75" y="55" font-family="sans-serif" font-size="20" font-weight="900" fill="#000000" text-anchor="middle" letter-spacing="4">COACH</text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_monochrome_black.svg", "w", encoding="utf-8") as f:
        f.write(mono_black_svg)

    # 6. Monochrome White (Inverzně bílé pro temné pozadí)
    mono_white_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="100%" height="100%">
  <rect width="1000" height="320" rx="30" fill="#000000"/>
  <g transform="translate(10, 0)">
    <path d="M 150 55 L 70 175 L 138 155 L 150 245 Z" fill="#FFFFFF"/>
    <path d="M 150 55 L 230 175 L 162 155 L 150 245 Z" fill="#AAAAAA"/>
    <polygon points="150,68 156,160 150,230 144,160" fill="#000000"/>
    <circle cx="150" cy="158" r="5" fill="#FFFFFF"/>
  </g>
  <g transform="translate(300, 195)" fill="#FFFFFF">
    <polygon points="20,-105 55,-105 55,-40 100,-105 145,-105 90,-25 150,60 105,60 60,-5 55,2 55,60 20,60"/>
    <polygon points="180,-105 215,-105 215,60 180,60"/>
    <polygon points="245,-105 350,-105 350,-75 315,-75 315,60 280,60 280,-75 245,-75"/>
    <polygon points="380,-105 470,-105 470,-75 415,-75 415,-38 460,-38 460,-10 415,-10 415,30 475,30 475,60 380,60"/>
  </g>
  <g transform="translate(805, 110)">
    <rect x="0" y="0" width="150" height="90" rx="12" fill="none" stroke="#FFFFFF" stroke-width="2"/>
    <text x="75" y="55" font-family="sans-serif" font-size="20" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="4">COACH</text>
  </g>
</svg>'''
    with open("brand_kite/kite_logo_monochrome_white.svg", "w", encoding="utf-8") as f:
        f.write(mono_white_svg)

    # 7. Mockup: Vizitka (Business Card)
    mockup_card = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="100%" height="100%">
  <defs>
    <filter id="cardShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="15" stdDeviation="20" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#0B0F19"/>
    </linearGradient>
    <linearGradient id="cardGradCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#7928CA"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="600" fill="#1E293B"/>
  <text x="500" y="50" font-family="'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="800" fill="#94A3B8" text-anchor="middle" letter-spacing="3">MOCKUP A: BUSINESS CARDS (PŘEDNÍ A ZADNÍ STRANA)</text>

  <!-- Front Side of Card -->
  <g transform="translate(60, 100)" filter="url(#cardShadow)">
    <rect width="400" height="240" rx="16" fill="url(#cardGrad)" stroke="#374151" stroke-width="1.5"/>
    <!-- Diagonal cyan laser strip -->
    <path d="M 0 0 L 15 0 L 0 35 Z" fill="#00F0FF"/>
    <path d="M 400 205 L 400 240 L 365 240 Z" fill="#EC4899"/>
    
    <!-- Mini emblem -->
    <g transform="translate(40, 45) scale(0.35)">
      <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#00F0FF"/>
      <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#EC4899"/>
      <circle cx="120" cy="130" r="8" fill="#FFFFFF"/>
    </g>
    <text x="125" y="85" font-family="'Segoe UI', sans-serif" font-size="26" font-weight="900" fill="#FFFFFF" letter-spacing="3">KITE</text>
    <text x="125" y="105" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="700" fill="#00F0FF" letter-spacing="2">ESPORTS COACHING</text>
    
    <!-- Info -->
    <text x="40" y="160" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="800" fill="#F8FAFC">Štěpán „Gajdy“</text>
    <text x="40" y="180" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#A855F7">Master Tier ADC Coach &amp; Analyst</text>
    <line x1="40" y1="192" x2="360" y2="192" stroke="#334155" stroke-width="1"/>
    <text x="40" y="215" font-family="'Segoe UI', sans-serif" font-size="11" fill="#94A3B8">✉ coach@kite-coaching.gg | 🌐 kite-coaching.gg</text>
  </g>

  <!-- Back Side of Card -->
  <g transform="translate(540, 240)" filter="url(#cardShadow)">
    <rect width="400" height="240" rx="16" fill="#080C14" stroke="#00F0FF" stroke-width="2"/>
    <circle cx="200" cy="120" r="70" fill="none" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4 6" opacity="0.4"/>
    <g transform="translate(150, 40) scale(0.42)">
      <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#00F0FF"/>
      <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#EC4899"/>
      <circle cx="120" cy="130" r="10" fill="#FFFFFF"/>
    </g>
    <text x="200" y="165" font-family="'Segoe UI', sans-serif" font-size="20" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="4">KITE</text>
    <text x="200" y="195" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="800" fill="#00F0FF" text-anchor="middle" letter-spacing="4">OUTSPACE. OUTKITE. OUTCLIMB.</text>
  </g>
</svg>'''
    with open("brand_kite/mockup_business_card.svg", "w", encoding="utf-8") as f:
        f.write(mockup_card)

    # 8. Mockup: Web / E-shop Hero
    mockup_web = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="100%" height="100%">
  <defs>
    <linearGradient id="webCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#0077FE"/>
    </linearGradient>
    <linearGradient id="btnGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
  </defs>
  <!-- Browser Window Frame -->
  <rect width="1000" height="650" rx="14" fill="#0B0F17" stroke="#1E293B" stroke-width="2"/>
  
  <!-- Browser top bar -->
  <rect width="1000" height="42" rx="14" fill="#161F30"/>
  <circle cx="25" cy="21" r="6" fill="#EF4444"/>
  <circle cx="45" cy="21" r="6" fill="#F59E0B"/>
  <circle cx="65" cy="21" r="6" fill="#10B981"/>
  <rect x="180" y="10" width="640" height="22" rx="6" fill="#0B0F17"/>
  <text x="500" y="26" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748B" text-anchor="middle">https://kite-coaching.gg/store/master-adc-program</text>

  <!-- Website Header Navigation -->
  <rect y="42" width="1000" height="70" fill="#0E1524" opacity="0.9"/>
  <!-- Mini Logo -->
  <g transform="translate(40, 52) scale(0.28)">
    <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#00F0FF"/>
    <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#EC4899"/>
    <circle cx="120" cy="130" r="10" fill="#FFFFFF"/>
  </g>
  <text x="110" y="85" font-family="'Segoe UI', sans-serif" font-size="24" font-weight="900" fill="#FFFFFF" letter-spacing="2">KITE</text>
  <text x="280" y="83" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="600" fill="#00F0FF">Coaching 1v1</text>
  <text x="410" y="83" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="600" fill="#94A3B8">VOD Reviews</text>
  <text x="530" y="83" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="600" fill="#94A3B8">E-books &amp; Guides</text>
  <text x="680" y="83" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="600" fill="#94A3B8">Merch &amp; Mousepads</text>
  <rect x="850" y="60" width="110" height="34" rx="17" fill="url(#btnGrad)"/>
  <text x="905" y="82" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="800" fill="#0B0F17" text-anchor="middle">BOOK SESSION</text>

  <!-- Hero Section -->
  <g transform="translate(60, 150)">
    <!-- Badge -->
    <rect x="0" y="10" width="220" height="28" rx="14" fill="#132338" stroke="#00F0FF" stroke-width="1"/>
    <text x="110" y="29" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#00F0FF" text-anchor="middle">⚡ MASTER TIER ADC COACHING</text>
    
    <text x="0" y="90" font-family="'Segoe UI', sans-serif" font-size="44" font-weight="900" fill="#FFFFFF">ZASTAV PROHRÁVAT.</text>
    <text x="0" y="145" font-family="'Segoe UI', sans-serif" font-size="44" font-weight="900" fill="#00F0FF">ZAČNI KITOVAT JAKO BŮH.</text>
    
    <text x="0" y="195" font-family="'Segoe UI', sans-serif" font-size="16" fill="#94A3B8">Individuální rozbor chyb, spacing drilly, mechaniky orbwalkingu a macro</text>
    <text x="0" y="220" font-family="'Segoe UI', sans-serif" font-size="16" fill="#94A3B8">pro každého ADC střelce, který míří z Platiny/Diamondu do Masteru.</text>

    <!-- CTAs -->
    <rect x="0" y="260" width="200" height="50" rx="25" fill="url(#btnGrad)"/>
    <text x="100" y="292" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#0B0F17" text-anchor="middle">OBJEDNAT LEKCI</text>

    <rect x="220" y="260" width="180" height="50" rx="25" fill="none" stroke="#334155" stroke-width="2"/>
    <text x="310" y="292" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">ZOBRAZIT GUIDY</text>
  </g>

  <!-- Hero Graphic Card / Master Badge Product Mockup -->
  <g transform="translate(560, 160)">
    <rect width="380" height="310" rx="20" fill="#101726" stroke="#1E293B" stroke-width="2"/>
    <!-- Product preview header -->
    <rect width="380" height="60" rx="20" fill="#162238"/>
    <text x="30" y="38" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="800" fill="#00F0FF">BALÍČEK: ROAD TO MASTER</text>
    <text x="330" y="38" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="900" fill="#EC4899">999 Kč</text>
    
    <!-- Big Logo Emblem in Preview -->
    <g transform="translate(140, 90) scale(0.42)">
      <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#00F0FF"/>
      <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#EC4899"/>
      <circle cx="120" cy="130" r="10" fill="#FFFFFF"/>
    </g>
    <text x="190" y="200" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="900" fill="#FFFFFF" text-anchor="middle">KITE 1-ON-1 INTENSIVE</text>
    <text x="190" y="225" font-family="'Segoe UI', sans-serif" font-size="13" fill="#94A3B8" text-anchor="middle">✓ 2× Live VOD Review + Live Spectate</text>
    <text x="190" y="248" font-family="'Segoe UI', sans-serif" font-size="13" fill="#94A3B8" text-anchor="middle">✓ Kompletní PDF Guide pro Spacing &amp; Macra</text>
    <text x="190" y="271" font-family="'Segoe UI', sans-serif" font-size="13" fill="#00F0FF" text-anchor="middle">✓ Discord VIP Role &amp; Otázky 24/7</text>
  </g>

  <!-- Bottom stats bar -->
  <rect y="540" width="1000" height="110" rx="14" fill="#080C14"/>
  <g transform="translate(100, 580)">
    <text x="0" y="0" font-family="'Segoe UI', sans-serif" font-size="28" font-weight="900" fill="#00F0FF">+350 LP</text>
    <text x="0" y="22" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748B">Průměrný skok studentů</text>
  </g>
  <g transform="translate(420, 580)">
    <text x="0" y="0" font-family="'Segoe UI', sans-serif" font-size="28" font-weight="900" fill="#EC4899">87% WR</text>
    <text x="0" y="22" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748B">Úspěšnost v laning phase</text>
  </g>
  <g transform="translate(720, 580)">
    <text x="0" y="0" font-family="'Segoe UI', sans-serif" font-size="28" font-weight="900" fill="#FFFFFF">MASTER TIER</text>
    <text x="0" y="22" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748B">Ověřená úroveň kouče</text>
  </g>
</svg>'''
    with open("brand_kite/mockup_website_hero.svg", "w", encoding="utf-8") as f:
        f.write(mockup_web)

    # 9. Mockup: Social Media Banner (YouTube / Twitch / Twitter Header)
    mockup_social = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 450" width="100%" height="100%">
  <defs>
    <linearGradient id="socBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B12"/>
      <stop offset="50%" stop-color="#0E1626"/>
      <stop offset="100%" stop-color="#140A20"/>
    </linearGradient>
    <linearGradient id="socCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </linearGradient>
    <linearGradient id="socPink" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EC4899"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="450" rx="20" fill="url(#socBg)"/>
  
  <!-- Reticle Spacing Lines in Background -->
  <circle cx="500" cy="225" r="210" fill="none" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="5 10" opacity="0.25"/>
  <circle cx="500" cy="225" r="160" fill="none" stroke="#EC4899" stroke-width="1" stroke-dasharray="3 6" opacity="0.2"/>
  <line x1="50" y1="225" x2="950" y2="225" stroke="#00F0FF" stroke-width="1" opacity="0.1"/>

  <!-- Center Big Logo -->
  <g transform="translate(425, 40) scale(0.7)">
    <path d="M 110 30 L 30 160 L 100 140 L 110 230 Z" fill="url(#socCyan)"/>
    <path d="M 110 30 L 190 160 L 120 140 L 110 230 Z" fill="url(#socPink)"/>
    <polygon points="110,45 116,145 110,220 104,145" fill="#FFFFFF"/>
    <circle cx="110" cy="142" r="8" fill="#00F0FF"/>
  </g>

  <!-- Typography -->
  <text x="500" y="260" font-family="'Segoe UI', Roboto, sans-serif" font-size="52" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="8">K I T E</text>
  <text x="500" y="295" font-family="'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="800" fill="#00F0FF" text-anchor="middle" letter-spacing="6">MASTER TIER COACHING</text>
  <text x="500" y="340" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#E2E8F0" text-anchor="middle" letter-spacing="4">OUTSPACE  •  OUTKITE  •  OUTCLIMB</text>

  <!-- Social links badges -->
  <g transform="translate(500, 390)">
    <text x="-220" y="0" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="600" fill="#94A3B8" text-anchor="middle">TWITCH.TV/GAJDY_ADC</text>
    <text x="0" y="0" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="600" fill="#94A3B8" text-anchor="middle">YOUTUBE: @KITE_COACHING</text>
    <text x="220" y="0" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="600" fill="#94A3B8" text-anchor="middle">DISCORD.GG/KITE-ESPORTS</text>
  </g>
</svg>'''
    with open("brand_kite/mockup_social_banner.svg", "w", encoding="utf-8") as f:
        f.write(mockup_social)

    # 10. Mockup: Outdoor Board / Esports Arena Roll-Up Banner
    mockup_outdoor = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900" width="100%" height="100%">
  <defs>
    <linearGradient id="outGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#060910"/>
      <stop offset="35%" stop-color="#0F172A"/>
      <stop offset="80%" stop-color="#1E1035"/>
      <stop offset="100%" stop-color="#060910"/>
    </linearGradient>
    <linearGradient id="oNeon" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
  </defs>
  <!-- Rollup Stand Frame -->
  <rect width="600" height="900" fill="#0B0F17"/>
  <!-- Banner Canvas -->
  <rect x="50" y="30" width="500" height="800" rx="12" fill="url(#outGrad)" stroke="#334155" stroke-width="2"/>
  
  <!-- Stand feet -->
  <rect x="30" y="830" width="540" height="20" rx="6" fill="#475569"/>
  <rect x="250" y="850" width="100" height="15" rx="3" fill="#1E293B"/>

  <!-- Banner Content -->
  <g transform="translate(300, 140)">
    <!-- Big Logo -->
    <g transform="translate(-75, -50) scale(0.65)">
      <path d="M 120 40 L 50 145 L 110 128 L 120 205 Z" fill="#00F0FF"/>
      <path d="M 120 40 L 190 145 L 130 128 L 120 205 Z" fill="#EC4899"/>
      <polygon points="120,52 125,130 120,195 115,130" fill="#FFFFFF"/>
      <circle cx="120" cy="130" r="10" fill="#00F0FF"/>
    </g>
    <text x="0" y="150" font-family="'Segoe UI', Roboto, sans-serif" font-size="44" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="6">KITE</text>
    <text x="0" y="185" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="800" fill="#00F0FF" text-anchor="middle" letter-spacing="4">ESPORTS COACHING</text>
  </g>

  <!-- Key Highlights -->
  <g transform="translate(100, 420)">
    <rect x="0" y="0" width="400" height="65" rx="10" fill="#0F172A" stroke="#00F0FF" stroke-width="1.5"/>
    <text x="25" y="40" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="800" fill="#FFFFFF">🎯 MECHANIKY &amp; SPACING DRILLY</text>
  </g>
  <g transform="translate(100, 505)">
    <rect x="0" y="0" width="400" height="65" rx="10" fill="#0F172A" stroke="#EC4899" stroke-width="1.5"/>
    <text x="25" y="40" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="800" fill="#FFFFFF">🏆 HIGH-ELO VOD ANALÝZY</text>
  </g>
  <g transform="translate(100, 590)">
    <rect x="0" y="0" width="400" height="65" rx="10" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="25" y="40" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="800" fill="#FFFFFF">⚡ Z PLATINY AŽ DO MASTERU</text>
  </g>

  <!-- Big Slogan & QR Code Box -->
  <g transform="translate(300, 710)">
    <text x="0" y="0" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="900" fill="url(#oNeon)" text-anchor="middle" letter-spacing="5">OUTSPACE. OUTKITE. OUTCLIMB.</text>
    <rect x="-60" y="20" width="120" height="40" rx="8" fill="#00F0FF"/>
    <text x="0" y="46" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="900" fill="#0B0F17" text-anchor="middle">KITE-COACHING.GG</text>
  </g>
</svg>'''
    with open("brand_kite/mockup_outdoor_board.svg", "w", encoding="utf-8") as f:
        f.write(mockup_outdoor)

create_svgs()
print("SVGs successfully created!")
