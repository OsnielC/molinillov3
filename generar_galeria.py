#!/usr/bin/env python3
"""
generar_galeria.py
==================
Escanea la carpeta ./images/, ordena todas las fotos DSC_XXXX.JPG
y genera galeria.html con las 91 fotos distribuidas automáticamente
en 4 secciones: Espacio, Plantas, Café & Bebidas, Comida.

Uso:
    python generar_galeria.py

Requisitos: solo la librería estándar de Python 3.
"""

import os
import math

# ── Configuración ────────────────────────────────────────────────────────────
IMAGES_DIR   = "./images"          # carpeta con las fotos
OUTPUT_FILE  = "galeria.html"      # archivo de salida
LOGO_FILE    = "logo.jpg"          # logo dentro de images/

# Extensiones reconocidas (case-insensitive)
VALID_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Distribución de fotos por sección (porcentajes aprox.)
SECTION_RATIOS = {
    "espacio": 0.30,   # 30 % — Nuestro Espacio
    "plantas":  0.28,  # 28 % — Plantas
    "cafe":     0.22,  # 22 % — Café & Bebidas
    "comida":   0.20,  # 20 % — Comida
}

# Metadatos por sección
SECTIONS = {
    "espacio": {
        "emoji":    "🏡",
        "titulo":   "Nuestro <span>Espacio</span>",
        "subtitulo":"Ambiente & Decoración",
        "filter":   "espacio",
        "captions": [
            "El corazón de Molinillo 🌿", "Rincones con alma ✨",
            "Cada detalle importa 🍃", "Bienvenido a casa ☕",
            "Espacios que inspiran 🌱", "Luz y plantas 🌸",
            "Nuestro refugio verde 🌿", "Decoración con amor 💚",
        ],
    },
    "plantas": {
        "emoji":    "🌵",
        "titulo":   "Nuestras <span>Plantas</span>",
        "subtitulo":"Selección & Variedades",
        "filter":   "plantas",
        "captions": [
            "Plantas tropicales 🌴", "Cactus & Suculentas 🌵",
            "Arreglos florales 🌸", "De interior 🪴",
            "Tropicales 🌿", "Rodeados de vida 💚",
            "Plantas que enamoran 🌺", "Verde puro 🍃",
        ],
    },
    "cafe": {
        "emoji":    "☕",
        "titulo":   "Café & <span>Bebidas</span>",
        "subtitulo":"Talea de Castro & Más",
        "filter":   "cafe",
        "captions": [
            "Café de Talea de Castro ☕", "Infusiones artesanales 🫖",
            "El mejor café ☕", "Bebidas artesanales 🌿",
            "Tés y más 🍵", "Nuestra selección ✨",
        ],
    },
    "comida": {
        "emoji":    "🍽️",
        "titulo":   "Nuestra <span>Cocina</span>",
        "subtitulo":"Chef Alejandra",
        "filter":   "comida",
        "captions": [
            "Gastronomía con amor 🍽️", "Ingredientes frescos 🌱",
            "Cada detalle importa ✨", "Sabores únicos 🌶️",
            "Recetas del alma 💛", "Mesa lista 🍴",
        ],
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def caption_for(section_key, index):
    caps = SECTIONS[section_key]["captions"]
    return caps[index % len(caps)]


def photo_block(src, caption_text, wide=False):
    cls = "gal-wide" if wide else "gal-photo"
    return (
        f'        <div class="{cls}" data-src="{src}" data-caption="{caption_text}">\n'
        f'          <img src="{src}" alt="{caption_text}" loading="lazy" />\n'
        f'          <div class="gal-photo-caption"><span>{caption_text}</span></div>\n'
        f'        </div>\n'
    )


def render_section(key, photos):
    s = SECTIONS[key]
    lines = []
    lines.append(f'    <!-- SECCIÓN: {key.upper()} -->\n')
    lines.append(f'    <div class="gal-section reveal" data-category="{s["filter"]}">\n')
    lines.append( '      <div class="gal-section-header">\n')
    lines.append(f'        <h2 class="gal-section-title">{s["titulo"]}</h2>\n')
    lines.append( '        <div class="gal-section-line"></div>\n')
    lines.append(f'        <span class="gal-section-count">{s["subtitulo"]}</span>\n')
    lines.append( '      </div>\n\n')

    # Featured row: primeras 2 fotos en grande
    if len(photos) >= 2:
        reverse = "reverse" if key in ("plantas", "comida") else ""
        lines.append(f'      <div class="gal-featured-row {reverse}".strip()>\n'.replace('" >', '">'))
        lines.append(photo_block(photos[0], caption_for(key, 0), wide=True))
        lines.append(photo_block(photos[1], caption_for(key, 1), wide=True))
        lines.append( '      </div>\n\n')
        rest = photos[2:]
    else:
        rest = photos

    # Masonry con el resto
    if rest:
        lines.append('      <div class="gal-masonry">\n')
        for i, src in enumerate(rest):
            lines.append(photo_block(src, caption_for(key, i + 2)))
        lines.append('      </div>\n')

    lines.append('    </div>\n\n')
    return "".join(lines)


# ── Leer imágenes ──────────────────────────────────────────────────────────────

def get_images():
    if not os.path.isdir(IMAGES_DIR):
        raise FileNotFoundError(
            f"No se encontró la carpeta '{IMAGES_DIR}'.\n"
            "Asegúrate de ejecutar este script en el mismo directorio que la carpeta images/."
        )

    files = sorted(
        f for f in os.listdir(IMAGES_DIR)
        if os.path.splitext(f)[1].lower() in VALID_EXT
        and f != LOGO_FILE
    )
    return [f"{IMAGES_DIR}/{f}" for f in files]


def distribute(photos):
    total = len(photos)
    keys  = list(SECTION_RATIOS.keys())
    sizes = {k: max(2, math.floor(total * v)) for k, v in SECTION_RATIOS.items()}

    # Ajustar para que sumen exactamente total
    diff = total - sum(sizes.values())
    for k in keys:
        if diff == 0:
            break
        sizes[k] += 1
        diff -= 1

    result = {}
    idx = 0
    for k in keys:
        result[k] = photos[idx: idx + sizes[k]]
        idx += sizes[k]
    return result


# ── HTML ───────────────────────────────────────────────────────────────────────

CSS = """
    /* ── Variables ── */
    :root {
      --verde-oscuro:  #1a3a1a;
      --verde-musgo:   #3d6b35;
      --verde-lima:    rgb(145, 151, 103);
      --verde-menta:   #a8d89a;
      --cafe-oscuro:   #3b1f0e;
      --cafe-medio:    #7c4a1e;
      --cafe-latte:    #c8935a;
      --crema:         #f5ead7;
      --crema-oscura:  #e8d5b5;
      --terracota:     #c75b3a;
      --amarillo-sol:  #f5c842;
      --blanco:        #ffffff;
      --font-display: 'Playfair Display', serif;
      --font-body:    'Lato', sans-serif;
      --font-accent:  'Caveat', cursive;
      --radius-xl:    100px;
    }

    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font-body);
      background: #0f1a0f;
      color: var(--crema);
      overflow-x: hidden;
      line-height: 1.6;
    }
    img { display: block; max-width: 100%; }
    a   { color: inherit; text-decoration: none; }

    /* ── NAVBAR ── */
    .gal-nav {
      position: fixed; top: 0; width: 100%; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 5%; height: 68px;
      background: rgba(15, 26, 15, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 2px solid var(--verde-lima);
    }
    .gal-nav-logo { display: flex; align-items: center; gap: 10px; }
    .gal-nav-logo img {
      width: 38px; height: 38px; border-radius: 50%;
      object-fit: cover; border: 2px solid var(--verde-lima);
    }
    .gal-nav-logo span {
      font-family: var(--font-display); font-size: 1.3rem;
      font-weight: 900; font-style: italic; color: var(--crema);
    }
    .gal-nav-back {
      display: flex; align-items: center; gap: 8px;
      font-size: 0.8rem; font-weight: 700; letter-spacing: 2px;
      text-transform: uppercase; color: var(--verde-lima);
      border: 1.5px solid rgba(145,151,103,0.4);
      padding: 8px 20px; border-radius: var(--radius-xl);
      transition: background 0.2s, border-color 0.2s;
    }
    .gal-nav-back:hover { background: rgba(145,151,103,0.15); border-color: var(--verde-lima); }

    /* ── HERO ── */
    .gal-hero {
      padding-top: 68px; min-height: 40vh;
      background: linear-gradient(160deg, #1a2a1a 0%, #2a2e1a 50%, var(--cafe-oscuro) 100%);
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; text-align: center;
      position: relative; overflow: hidden;
    }
    .gal-hero::before {
      content: ''; position: absolute; inset: 0;
      background: repeating-linear-gradient(
        -45deg, transparent, transparent 60px,
        rgba(145,151,103,0.04) 60px, rgba(145,151,103,0.04) 120px
      );
    }
    .gal-hero-inner { position: relative; z-index: 1; padding: 60px 20px 50px; }
    .gal-hero-tag {
      display: inline-block; background: var(--verde-lima);
      color: var(--verde-oscuro); font-size: 0.68rem; font-weight: 700;
      letter-spacing: 3px; text-transform: uppercase;
      padding: 6px 18px; border-radius: var(--radius-xl); margin-bottom: 20px;
    }
    .gal-hero-title {
      font-family: var(--font-display);
      font-size: clamp(2.8rem, 7vw, 5.5rem);
      font-weight: 900; line-height: 1.05; color: var(--crema);
    }
    .gal-hero-title em { color: var(--verde-lima); font-style: italic; }
    .gal-hero-sub {
      font-family: var(--font-accent); font-size: 1.3rem;
      color: var(--crema-oscura); opacity: 0.8; margin-top: 14px;
    }
    /* contador de fotos */
    .gal-hero-count {
      margin-top: 18px;
      display: inline-block;
      background: rgba(145,151,103,0.15);
      border: 1px solid rgba(145,151,103,0.35);
      border-radius: var(--radius-xl);
      padding: 6px 22px;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--verde-lima);
    }

    /* ── FILTROS ── */
    .gal-filter {
      position: sticky; top: 68px; z-index: 50;
      background: rgba(15,26,15,0.96);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid rgba(145,151,103,0.2);
      padding: 16px 5%; display: flex; gap: 10px;
      flex-wrap: wrap; justify-content: center;
    }
    .filter-btn {
      font-family: var(--font-body);
      background: transparent; color: rgba(245,234,215,0.55);
      border: 1.5px solid rgba(145,151,103,0.25);
      padding: 8px 22px; border-radius: var(--radius-xl);
      font-size: 0.78rem; font-weight: 700;
      letter-spacing: 1.5px; text-transform: uppercase;
      cursor: pointer; transition: all 0.25s ease;
    }
    .filter-btn:hover { border-color: var(--verde-lima); color: var(--crema); }
    .filter-btn.active {
      background: var(--verde-lima); color: var(--verde-oscuro);
      border-color: var(--verde-lima);
    }

    /* ── GALERÍA ── */
    .gal-main { padding: 48px 4% 80px; max-width: 1400px; margin: 0 auto; }
    .gal-section { margin-bottom: 72px; }
    .gal-section-header {
      display: flex; align-items: center; gap: 18px; margin-bottom: 28px;
    }
    .gal-section-title {
      font-family: var(--font-display); font-size: 1.8rem;
      font-weight: 700; color: var(--crema); white-space: nowrap;
    }
    .gal-section-title span { color: var(--verde-lima); font-style: italic; }
    .gal-section-line { flex: 1; height: 1px; background: rgba(145,151,103,0.25); }
    .gal-section-count {
      font-size: 0.72rem; font-weight: 700; letter-spacing: 2px;
      text-transform: uppercase; color: var(--verde-lima); opacity: 0.7;
      white-space: nowrap;
    }

    /* Masonry */
    .gal-masonry { columns: 3; column-gap: 14px; }
    @media (max-width: 900px) { .gal-masonry { columns: 2; } }
    @media (max-width: 520px) { .gal-masonry { columns: 1; } }

    .gal-photo {
      break-inside: avoid; margin-bottom: 14px; border-radius: 14px;
      overflow: hidden; position: relative; background: #1a2a1a; cursor: pointer;
    }
    .gal-photo img { width: 100%; height: auto; display: block; transition: transform 0.5s ease; }
    .gal-photo:hover img { transform: scale(1.04); }

    .gal-photo-caption {
      position: absolute; bottom: 0; left: 0; right: 0;
      background: linear-gradient(to top, rgba(15,26,15,0.9) 0%, transparent 100%);
      padding: 28px 16px 14px; opacity: 0; transition: opacity 0.3s ease;
    }
    .gal-photo:hover .gal-photo-caption { opacity: 1; }
    .gal-photo-caption span {
      font-family: var(--font-accent); font-size: 1.05rem; color: var(--crema);
    }

    /* Featured row */
    .gal-featured-row {
      display: grid; grid-template-columns: 2fr 1fr;
      gap: 14px; margin-bottom: 14px;
    }
    .gal-featured-row.reverse { grid-template-columns: 1fr 2fr; }
    .gal-wide {
      border-radius: 14px; overflow: hidden;
      position: relative; background: #1a2a1a; cursor: pointer;
    }
    .gal-wide img {
      width: 100%; height: 100%; object-fit: cover;
      display: block; transition: transform 0.5s ease; min-height: 320px;
    }
    .gal-wide:hover img { transform: scale(1.04); }
    .gal-wide .gal-photo-caption { opacity: 0; }
    .gal-wide:hover .gal-photo-caption { opacity: 1; }
    @media (max-width: 700px) {
      .gal-featured-row, .gal-featured-row.reverse { grid-template-columns: 1fr; }
      .gal-wide img { min-height: 200px; }
    }

    /* ── LIGHTBOX ── */
    #lightbox {
      display: none; position: fixed; inset: 0; z-index: 999;
      background: rgba(5,10,5,0.96);
      align-items: center; justify-content: center; cursor: zoom-out;
    }
    #lightbox.open { display: flex; }
    #lightbox img {
      max-width: 90vw; max-height: 90vh;
      border-radius: 10px; box-shadow: 0 30px 80px rgba(0,0,0,0.6);
      cursor: default;
    }
    /* contador en lightbox */
    .lb-counter {
      position: absolute; top: 22px; left: 50%; transform: translateX(-50%);
      font-size: 0.78rem; font-weight: 700; letter-spacing: 2px;
      color: rgba(245,234,215,0.55); text-transform: uppercase;
    }
    .lb-close {
      position: absolute; top: 20px; right: 24px;
      font-size: 2rem; color: var(--crema); opacity: 0.7;
      cursor: pointer; transition: opacity 0.2s;
      background: none; border: none; line-height: 1;
    }
    .lb-close:hover { opacity: 1; }
    .lb-prev, .lb-next {
      position: absolute; top: 50%; transform: translateY(-50%);
      background: rgba(145,151,103,0.2);
      border: 1.5px solid rgba(145,151,103,0.4);
      color: var(--crema); font-size: 1.5rem;
      padding: 14px 18px; border-radius: 50%; cursor: pointer;
      transition: background 0.2s;
    }
    .lb-prev { left: 20px; }
    .lb-next { right: 20px; }
    .lb-prev:hover, .lb-next:hover { background: rgba(145,151,103,0.45); }
    .lb-caption {
      position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
      font-family: var(--font-accent); font-size: 1.2rem;
      color: var(--crema); opacity: 0.8; white-space: nowrap;
    }
    @media (max-width: 600px) {
      .lb-prev { left: 8px; } .lb-next { right: 8px; }
    }

    /* ── Instagram CTA ── */
    .gal-ig-cta {
      text-align: center; padding: 60px 5%;
      background: linear-gradient(160deg, #1a2a1a, #2a2e1a);
      border-top: 1px solid rgba(145,151,103,0.2);
    }
    .gal-ig-cta h3 {
      font-family: var(--font-display); font-size: 2rem;
      font-weight: 700; color: var(--crema); margin-bottom: 12px;
    }
    .gal-ig-cta h3 em { color: var(--verde-lima); font-style: italic; }
    .gal-ig-cta p {
      font-family: var(--font-accent); font-size: 1.2rem;
      color: rgba(245,234,215,0.65); margin-bottom: 28px;
    }
    .btn-ig {
      display: inline-block; background: var(--verde-lima);
      color: var(--verde-oscuro); padding: 14px 36px;
      border-radius: var(--radius-xl); font-weight: 700;
      font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;
      transition: transform 0.2s, box-shadow 0.2s;
      box-shadow: 0 8px 28px rgba(145,151,103,0.4); margin: 0 8px 12px;
    }
    .btn-ig:hover { transform: translateY(-3px); box-shadow: 0 14px 36px rgba(145,151,103,0.55); }
    .btn-back {
      display: inline-block; background: transparent; color: var(--verde-lima);
      padding: 13px 34px; border-radius: var(--radius-xl); font-weight: 700;
      font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;
      border: 2px solid rgba(145,151,103,0.4);
      transition: border-color 0.2s, background 0.2s; margin: 0 8px 12px;
    }
    .btn-back:hover { border-color: var(--verde-lima); background: rgba(145,151,103,0.12); }

    /* ── Footer ── */
    .gal-footer {
      background: #080f08; text-align: center;
      padding: 28px 5%; border-top: 1px solid rgba(255,255,255,0.07);
      font-size: 0.8rem; color: rgba(245,234,215,0.3); letter-spacing: 1px;
    }

    /* ── Reveal ── */
    .reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.7s ease, transform 0.7s ease; }
    .reveal.visible { opacity: 1; transform: translateY(0); }
"""

JS = """
    /* ── Scroll Reveal ── */
    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          setTimeout(() => e.target.classList.add('visible'), i * 100);
          revealObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

    /* ── Lightbox ── */
    const lightbox  = document.getElementById('lightbox');
    const lbImg     = document.getElementById('lbImg');
    const lbCaption = document.getElementById('lbCaption');
    const lbCounter = document.getElementById('lbCounter');
    const lbClose   = document.getElementById('lbClose');
    const lbPrev    = document.getElementById('lbPrev');
    const lbNext    = document.getElementById('lbNext');

    // Solo fotos visibles (respeta el filtro activo)
    let photos = [];
    let currentIndex = 0;

    function buildPhotoList() {
      photos = Array.from(
        document.querySelectorAll('.gal-section:not([style*="display: none"]) .gal-photo[data-src], .gal-section:not([style*="display: none"]) .gal-wide[data-src]')
      );
    }

    function openLightbox(el) {
      buildPhotoList();
      currentIndex = photos.indexOf(el);
      showPhoto();
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    }

    function showPhoto() {
      const el = photos[currentIndex];
      if (!el) return;
      lbImg.src = el.dataset.src;
      lbCaption.textContent = el.dataset.caption || '';
      lbCounter.textContent = (currentIndex + 1) + ' / ' + photos.length;
    }

    function navigate(dir) {
      currentIndex = (currentIndex + dir + photos.length) % photos.length;
      showPhoto();
    }

    document.querySelectorAll('.gal-photo[data-src], .gal-wide[data-src]').forEach(el => {
      el.addEventListener('click', () => openLightbox(el));
    });

    lbClose.addEventListener('click', closeLightbox);
    lbPrev.addEventListener('click',  (e) => { e.stopPropagation(); navigate(-1); });
    lbNext.addEventListener('click',  (e) => { e.stopPropagation(); navigate(+1); });
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox || e.target === lbImg) closeLightbox(); });

    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape')     closeLightbox();
      if (e.key === 'ArrowLeft')  navigate(-1);
      if (e.key === 'ArrowRight') navigate(+1);
    });

    /* Swipe en móvil */
    let touchStartX = 0;
    lightbox.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
    lightbox.addEventListener('touchend',   (e) => {
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 50) navigate(dx < 0 ? 1 : -1);
    });

    /* ── Category Filter ── */
    const filterBtns = document.querySelectorAll('.filter-btn');
    const sections   = document.querySelectorAll('.gal-section');

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.filter;
        sections.forEach(sec => {
          sec.style.display = (cat === 'all' || sec.dataset.category === cat) ? '' : 'none';
        });
      });
    });
"""


def build_html(total_photos, sections_html):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Galería completa de Molinillo — Café, Plantas & Más. Conoce nuestro espacio, platillos y plantas." />
  <title>Galería — Molinillo Café, Plantas & Más</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Lato:wght@300;400;700&family=Caveat:wght@500;700&display=swap" rel="stylesheet" />
  <style>
{CSS}
  </style>
</head>
<body>

  <!-- NAVBAR -->
  <nav class="gal-nav">
    <a href="./index.html" class="gal-nav-logo">
      <img src="./images/logo.jpg" alt="Molinillo" />
      <span>Molinillo</span>
    </a>
    <a href="./index.html" class="gal-nav-back">← Regresar</a>
  </nav>

  <!-- HERO -->
  <div class="gal-hero">
    <div class="gal-hero-inner">
      <div class="gal-hero-tag">📷 Galería completa</div>
      <h1 class="gal-hero-title">Vive la experiencia<br><em>Molinillo</em></h1>
      <p class="gal-hero-sub">Cada imagen cuenta una historia de plantas, café y pasión 🌿</p>
      <span class="gal-hero-count">📸 {total_photos} fotografías</span>
    </div>
  </div>

  <!-- FILTROS -->
  <div class="gal-filter">
    <button class="filter-btn active" data-filter="all">🌿 Todo</button>
    <button class="filter-btn" data-filter="espacio">🏡 Espacio</button>
    <button class="filter-btn" data-filter="plantas">🌵 Plantas</button>
    <button class="filter-btn" data-filter="cafe">☕ Café & Bebidas</button>
    <button class="filter-btn" data-filter="comida">🍽️ Comida</button>
  </div>

  <!-- GALERÍA -->
  <main class="gal-main">

{sections_html}
  </main>

  <!-- INSTAGRAM CTA -->
  <div class="gal-ig-cta">
    <h3>¿Quieres ver <em>más</em>?</h3>
    <p>Síguenos en Instagram para ver nuestras últimas fotos, promociones y novedades 🌿</p>
    <a href="https://www.instagram.com/molinillo_cafeplantas_y_mas/" target="_blank" rel="noopener noreferrer" class="btn-ig">📸 Seguirnos en Instagram</a>
    <a href="./index.html" class="btn-back">← Volver al inicio</a>
  </div>

  <footer class="gal-footer">
    <p>© 2025 Molinillo Café, Plantas & Más · Calicanto 11, San Antonio de la Cal, Oaxaca · 🌿</p>
  </footer>

  <!-- LIGHTBOX -->
  <div id="lightbox">
    <span class="lb-counter" id="lbCounter"></span>
    <button class="lb-close" id="lbClose" aria-label="Cerrar">✕</button>
    <button class="lb-prev"  id="lbPrev"  aria-label="Anterior">‹</button>
    <img id="lbImg" src="" alt="Imagen ampliada" />
    <button class="lb-next"  id="lbNext"  aria-label="Siguiente">›</button>
    <div class="lb-caption"  id="lbCaption"></div>
  </div>

  <script>
{JS}
  </script>
</body>
</html>
"""


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("📂 Leyendo carpeta images/ ...")
    photos = get_images()
    total  = len(photos)
    print(f"✅ {total} fotos encontradas.")

    if total == 0:
        print("❌ No se encontraron imágenes. Verifica la carpeta images/.")
        return

    dist = distribute(photos)
    for k, v in dist.items():
        print(f"   {SECTIONS[k]['emoji']}  {k:<8} → {len(v)} fotos")

    sections_html = ""
    for key in SECTION_RATIOS:
        sections_html += render_section(key, dist[key])

    html = build_html(total, sections_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n🎉 Listo! Archivo generado: {OUTPUT_FILE}")
    print(f"   Abre {OUTPUT_FILE} en tu navegador para verlo.")


if __name__ == "__main__":
    main()