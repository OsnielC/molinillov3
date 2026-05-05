/**
 * Molinillo — Café, Plantas & Más
 * Script principal
 */

/* ═══════════════════════════════════════
   1. NAVBAR — scroll & menú móvil
═══════════════════════════════════════ */
const navbar    = document.getElementById('navbar');
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

navToggle.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', isOpen);
  navToggle.innerHTML = isOpen ? '✕' : '&#9776;';
});

navLinks.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', false);
    navToggle.innerHTML = '&#9776;';
  });
});

/* ═══════════════════════════════════════
   2. SCROLL REVEAL
═══════════════════════════════════════ */
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach((el) => revealObserver.observe(el));

/* ═══════════════════════════════════════
   3. TABS DEL MENÚ
═══════════════════════════════════════ */
const tabButtons = document.querySelectorAll('.tab-btn');
const tabPanels  = document.querySelectorAll('.menu-panel');

tabButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    tabButtons.forEach((b) => {
      b.classList.toggle('active', b === btn);
      b.setAttribute('aria-selected', b === btn);
    });
    tabPanels.forEach((panel) => {
      panel.classList.toggle('active', panel.id === `tab-${target}`);
    });
  });
});

/* ═══════════════════════════════════════
   4. HOJAS FLOTANTES — OPTIMIZADO
   Web Animations API + límite MAX_LEAVES
   + pausa automática en pestaña inactiva.
═══════════════════════════════════════ */
(function initFloatingLeaves() {
  const group      = document.getElementById('leaves-group');
  const leafEmojis = ['🌿', '🍃', '🌱', '🌾', '☕'];
  const MAX_LEAVES  = 7;
  const INTERVAL_MS = 2200;
  let   activeLeaves = 0;
  let   intervalId   = null;

  function createLeaf() {
    if (activeLeaves >= MAX_LEAVES || document.hidden) return;
    activeLeaves++;

    const vw     = window.innerWidth;
    const vh     = window.innerHeight;
    const startX = Math.random() * vw;
    const size   = 16 + Math.random() * 22;
    const dur    = (13 + Math.random() * 14) * 1000;
    const wobble = 25 + Math.random() * 35;
    const emoji  = leafEmojis[Math.floor(Math.random() * leafEmojis.length)];

    const fo = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject');
    fo.setAttribute('x', 0);
    fo.setAttribute('y', 0);
    fo.setAttribute('width',  size * 2);
    fo.setAttribute('height', size * 2);
    fo.style.cssText = `font-size:${size}px;pointer-events:none;will-change:transform,opacity;`;
    fo.innerHTML = `<div xmlns="http://www.w3.org/1999/xhtml">${emoji}</div>`;
    group.appendChild(fo);

    const STEPS = 24;
    const keyframes = [];
    for (let i = 0; i <= STEPS; i++) {
      const p  = i / STEPS;
      const tx = startX + Math.sin(p * Math.PI * 5) * wobble;
      const ty = (vh + size * 2) - (vh + size * 4) * p;
      let opacity;
      if      (p < 0.10) opacity = p * 10 * 0.28;
      else if (p > 0.82) opacity = ((1 - p) / 0.18) * 0.28;
      else               opacity = 0.28;
      keyframes.push({ transform: `translate(${tx}px,${ty}px)`, opacity, offset: p });
    }

    const anim = fo.animate(keyframes, { duration: dur, easing: 'linear', fill: 'forwards' });

    const cleanup = () => {
      fo.remove();
      activeLeaves = Math.max(0, activeLeaves - 1);
    };
    anim.onfinish = cleanup;
    anim.oncancel = cleanup;
  }

  function startInterval() {
    if (intervalId !== null) return;
    intervalId = setInterval(() => { if (!document.hidden) createLeaf(); }, INTERVAL_MS);
  }

  function stopInterval() {
    clearInterval(intervalId);
    intervalId = null;
  }

  document.addEventListener('visibilitychange', () => {
    document.hidden ? stopInterval() : startInterval();
  });

  for (let i = 0; i < 5; i++) setTimeout(createLeaf, i * 500);
  startInterval();
})();

/* ═══════════════════════════════════════
   5. FORMULARIO DE CONTACTO
═══════════════════════════════════════ */
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const nombre  = contactForm.nombre.value.trim();
    const mensaje = contactForm.mensaje.value.trim();
    if (!nombre || !mensaje) { alert('Por favor completa tu nombre y mensaje. 🌿'); return; }

    console.log('Formulario enviado:', {
      nombre,
      telefono: contactForm.telefono.value,
      asunto:   contactForm.asunto.value,
      mensaje,
    });

    const btn = contactForm.querySelector('.form-submit');
    btn.textContent = '✅ ¡Mensaje enviado!';
    btn.style.background = 'linear-gradient(135deg, #5a5e3a, #919767)';
    btn.disabled = true;

    setTimeout(() => {
      contactForm.reset();
      btn.textContent = '🌱 Enviar Mensaje';
      btn.style.background = '';
      btn.disabled = false;
    }, 3500);
  });
}
