"""
Page generator for Blisniuk & Amanov.
Generates journey detail pages + region pages from data structures.

Usage: python3 tools/build.py
"""
import os, json, html as html_lib

REPO = "/home/user/blisniukamanov"

# Map of stop name → [lat, lng]. Used to render the interactive Leaflet map.
# Add new stops here when adding a new journey.
STOP_COORDS = {
    # África
    "Nairobi": [-1.2921, 36.8219],
    "Aberdares": [-0.3678, 36.7372],
    "Tarangire": [-3.8278, 36.0186],
    "Manyara y Ngorongoro": [-3.2403, 35.4881],
    "Manyara": [-3.6500, 35.7833],
    "Ngorongoro": [-3.2403, 35.4881],
    "Serengeti central": [-2.3333, 34.8333],
    "Kogatende": [-1.6700, 34.9000],
    "Reserva privada Naboisho": [-1.4400, 35.3500],
    "Naboisho": [-1.4400, 35.3500],
    "Masai Mara": [-1.4400, 35.1500],
    "Arusha": [-3.3869, 36.6830],
    "Pejeta": [0.0167, 36.9000],
    "Johannesburgo": [-26.2041, 28.0473],
    "Livingstone": [-17.8419, 25.8543],
    "Cataratas Victoria": [-17.9243, 25.8572],
    "Chobe": [-18.7833, 25.0500],
    "Sabi Sands": [-24.7833, 31.3833],
    "Khwai": [-19.1500, 23.7833],
    "Delta del Okavango": [-19.2833, 22.8000],
    "Maun": [-19.9800, 23.4200],
    # Sudamérica
    "Buenos Aires": [-34.6037, -58.3816],
    "El Calafate": [-50.3403, -72.2647],
    "Perito Moreno": [-50.4861, -73.0306],
    "Torres del Paine": [-51.0000, -73.0000],
    "Puerto Natales": [-51.7236, -72.5167],
    "Ushuaia": [-54.8019, -68.3030],
    "Canal Beagle": [-54.8500, -68.3000],
    "Manaos": [-3.1190, -60.0217],
    "Río Negro": [-3.0000, -60.0000],
    "Anavilhanas": [-2.4500, -60.7500],
    "Cuiabá": [-15.6014, -56.0979],
    "Transpantaneira": [-16.5333, -56.7500],
    "Porto Jofre": [-17.3500, -56.8000],
    "Foz do Iguaçú": [-25.5163, -54.5854],
    "Lima": [-12.0464, -77.0428],
    "Cuzco": [-13.5320, -71.9675],
    "Valle Sagrado": [-13.3167, -72.0833],
    "Ollantaytambo": [-13.2583, -72.2625],
    "Aguas Calientes": [-13.1631, -72.5286],
    "Machu Picchu": [-13.1631, -72.5450],
    # Europa
    "Milán": [45.4642, 9.1900],
    "Turín": [45.0703, 7.6869],
    "Sestri Levante": [44.2733, 9.4000],
    "Portovenere": [44.0489, 9.8389],
    "Parma": [44.8015, 10.3279],
    "Lago di Como": [45.9700, 9.2500],
    "Bolonia": [44.4949, 11.3426],
    "Venecia": [45.4408, 12.3155],
    "Santo Stefano Belbo": [44.7115, 8.2434],
    "Canelli": [44.7222, 8.2933],
    "Barbaresco": [44.7232, 8.0788],
    "Treiso": [44.6843, 8.0530],
    "Alba": [44.7000, 8.0333],
    "Pollenzo": [44.7034, 7.8983],
    "Bra": [44.6989, 7.8589],
    "Barolo": [44.6125, 7.9436],
    "Lisboa": [38.7223, -9.1393],
    "Évora": [38.5667, -7.9000],
    "Sevilla": [37.3886, -5.9823],
    "Granada": [37.1773, -3.5986],
    "Córdoba": [37.8847, -4.7794],
    "Madrid": [40.4168, -3.7038],
    "Toledo": [39.8628, -4.0273],
    "Bilbao": [43.2630, -2.9350],
    "Barcelona": [41.3851, 2.1734],
    # Asia
    "Tokio": [35.6762, 139.6503],
    "Hakone": [35.2329, 139.1058],
    "Kioto": [35.0116, 135.7681],
    "Nara": [34.6851, 135.8048],
    "Osaka": [34.6937, 135.5023],
    "Hanoi": [21.0285, 105.8542],
    "Ha Long Bay": [20.9101, 107.1839],
    "Hai Phong": [20.8449, 106.6881],
    "Ho Chi Minh": [10.8231, 106.6297],
    "Siem Reap": [13.3633, 103.8564],
    "Luang Prabang": [19.8845, 102.1348],
    "Bangkok": [13.7563, 100.5018],
    "Delhi": [28.7041, 77.1025],
    "Agra": [27.1767, 78.0081],
    "Ranthambore": [26.0173, 76.5026],
    "Jaipur": [26.9124, 75.7873],
    "Udaipur": [24.5854, 73.7125],
    # Norte de África / Oriente Medio
    "El Cairo": [30.0444, 31.2357],
    "Saqqara": [29.8714, 31.2167],
    "Luxor": [25.6872, 32.6396],
    "Edfu": [24.9779, 32.8731],
    "Kom Ombo": [24.4658, 32.9281],
    "Asuán": [24.0889, 32.8998],
    "Abu Simbel": [22.3372, 31.6258],
    # Norteamérica
    "Anchorage": [61.2181, -149.9003],
    "Seward": [60.1042, -149.4422],
    "Kenai Fjords": [59.9197, -149.6500],
    "Talkeetna": [62.3208, -150.1078],
    "Denali": [63.0695, -151.0070],
}

# =============================================================================
# COMMON BLOCKS
# =============================================================================
HEAD = lambda title, desc: f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Cormorant+Garamond:ital,wght@0,300;1,300&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>"""

UTILITY_BAR = """  <div class="utility-bar">
    <div class="utility-inner">
      <div class="utility-left">
        <a href="tel:+541161395550" class="speak">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.86 19.86 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.86 19.86 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.91.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7a2 2 0 0 1 1.72 2.03z"/></svg>
          Hablar con un experto · +54 11 6139 5550
        </a>
        <span class="utility-status">· Atendemos hoy de 9:00 a 20:00</span>
      </div>
      <div class="utility-right">
        <a href="#newsletter">Suscribirme</a>
        <span class="dot"></span>
        <a href="catalogos.html">Catálogos</a>
      </div>
    </div>
  </div>"""

HEADER = """  <header class="site-header" id="siteHeader">
    <div class="header-inner">
      <div class="nav-left">
        <button class="menu-trigger" id="menuTrigger" aria-label="Abrir menú">
          <span class="bars"><span></span><span></span><span></span></span> Menú
        </button>
        <a href="destinations.html">Destinos</a>
        <a href="journeys.html">Viajes</a>
        <a href="index.html#sanctuary">Casas B&amp;A</a>
      </div>
      <a href="index.html" class="brand"><span class="brand-wordmark">BLISNIUK <span class="brand-amp">&amp;</span> AMANOV</span></a>
      <div class="nav-right">
        <a href="journeys.html" class="search-trigger">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          Encontrar tu viaje
        </a>
      </div>
    </div>
  </header>

  <aside class="mobile-drawer" id="mobileDrawer" aria-hidden="true">
    <div class="drawer-inner">
      <a href="destinations.html">Destinos</a>
      <a href="journeys.html">Viajes</a>
      <a href="index.html#sanctuary">Casas B&amp;A</a>
      <a href="contact.html" class="btn btn-dark">Contacto</a>
    </div>
  </aside>"""

FOOTER = """  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <div class="footer-brand-row">
          <span class="footer-mark">B&amp;a</span>
          <h3>Blisniuk &amp; Amanov</h3>
        </div>
        <p>Casa de viajes en pequeño grupo y a medida. Casa central en <a href="https://maps.google.com/?q=Manuel+Ugarte+2035+Buenos+Aires" target="_blank" rel="noopener" style="color:rgba(255,255,255,0.85); border-bottom:1px solid rgba(255,255,255,0.3);">Manuel Ugarte 2035, Buenos Aires</a>.</p>
        <div class="socials">
          <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M7 2C4.24 2 2 4.24 2 7v10c0 2.76 2.24 5 5 5h10c2.76 0 5-2.24 5-5V7c0-2.76-2.24-5-5-5H7zm10 2c1.66 0 3 1.34 3 3v10c0 1.66-1.34 3-3 3H7c-1.66 0-3-1.34-3-3V7c0-1.66 1.34-3 3-3h10zm-5 3a5 5 0 100 10 5 5 0 000-10zm0 2a3 3 0 110 6 3 3 0 010-6zm5.5-.5a1 1 0 100 2 1 1 0 000-2z"/></svg></a>
          <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M22 12a10 10 0 10-11.5 9.9v-7H8v-3h2.5V9.5C10.5 7 12 5.7 14.2 5.7c1 0 2.1.2 2.1.2v2.3H15c-1.2 0-1.5.7-1.5 1.5V12H17l-.4 3h-3.1v7A10 10 0 0022 12z"/></svg></a>
        </div>
      </div>
      <div class="footer-col"><h5>Compañía</h5><ul><li><a href="heritage.html">Nuestra historia</a></li><li><a href="filantropia.html">Filantropía B&amp;A</a></li><li><a href="contact.html">Contacto</a></li></ul></div>
      <div class="footer-col"><h5>Servicios</h5><ul><li><a href="catalogos.html">Catálogos</a></li><li><a href="journeys.html">Todos los viajes</a></li></ul></div>
      <div class="footer-col"><h5>Legal</h5><ul><li><a href="terminos.html">Términos y condiciones</a></li><li><a href="privacidad.html">Privacidad</a></li><li><a href="cookies.html">Cookies</a></li></ul></div>
    </div>
    <div class="footer-bottom">© 2026 Blisniuk &amp; Amanov S.A. · RNAV Legajo 20943</div>
  </footer>

  <script src="script.js"></script>
</body>
</html>"""

# =============================================================================
# JOURNEY TEMPLATE
# =============================================================================
def build_journey(j):
    # Coords first (used by days for data-stop-index)
    coords_data = []
    for s in j['stops']:
        if s in STOP_COORDS:
            lat, lng = STOP_COORDS[s]
            coords_data.append({"name": s, "lat": lat, "lng": lng})
    coords_json = json.dumps(coords_data, ensure_ascii=False).replace("'", "&#39;")
    stops_html = "\n".join([f'          <li><span>{i+1}</span> {s}</li>' for i, s in enumerate(j['stops'])])

    days_html_items = []
    n_stops = max(1, len(coords_data))
    for i, d in enumerate(j['days']):
        stop_idx = min(i, n_stops - 1) if coords_data else 0
        days_html_items.append(
            f"""      <article class="day" data-day="{d['n']:02d}" data-stop-index="{stop_idx}">
        <div class="day-text">
          <span class="day-num">{d['label']}</span>
          <h3>{d['title']}</h3>
          <p>{d['body']}</p>
          <p class="day-meta"><strong>Comidas:</strong> {d['meals']} · <strong>Alojamiento:</strong> {d['lodging']}</p>
        </div>
        <div class="day-img"><img src="assets/img/{d['img']}" alt="{d['title']}" /></div>
      </article>"""
        )
    days_html = "\n".join(days_html_items)
    lodges_html = "\n".join([
        f"""        <a href="#" class="lodge-card">
          <img src="assets/img/{l['img']}" alt="{l['name']}" />
          <h4>{l['name']}</h4>
          <p>{l['where']}</p>
        </a>""" for l in j['lodges']
    ])
    exts_html = "\n".join([
        f"""        <a href="#" class="ext-card">
          <img src="assets/img/{e['img']}" alt="{e['title']}" />
          <div class="ext-body">
            <small>{e['meta']}</small>
            <h4>{e['title']}</h4>
            <p>{e['body']}</p>
          </div>
        </a>""" for e in j['extensions']
    ])
    dates_html = "\n".join([
        f"""            <tr><td>{d['date']}</td><td><span class="dot-status {d['status_class']}"></span> {d['status']}</td><td>{d['price']}</td><td><a href="#" class="link-arrow">Reservar →</a></td></tr>"""
        for d in j['dates']
    ])
    similar_html = "\n".join([
        f"""        <a href="{s['href']}" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/{s['img']}" alt="{s['title']}" />
          <span class="label-pill">{s['pill']}</span>
          <div class="img-card-body">
            <small>Pequeño grupo</small>
            <h3>{s['title']}</h3>
          </div>
        </a>""" for s in j['similar']
    ])
    incl_html = "\n".join([f"          <li>{x}</li>" for x in j['includes']])
    excl_html = ""
    if j.get('excludes'):
        items = "\n".join([f"          <li>{x}</li>" for x in j['excludes']])
        excl_html = f"""
        <h3 class="excludes-head">Lo que no incluye</h3>
        <ul class="check-list excludes-list">
{items}
        </ul>"""

    return f"""{HEAD(j['title'] + ' · Blisniuk & Amanov', j['meta_desc'])}

{UTILITY_BAR}
{HEADER}

  <section class="journey-detail-hero">
    <img src="assets/img/{j['hero']}" alt="{j['hero_alt']}" />
    <div class="container journey-hero-inner">
      <nav class="breadcrumb light">
        <a href="journeys.html">Viajes</a>
        <span>/</span>
        <a href="small-group.html">Pequeñas expediciones</a>
        <span>/</span>
        <span class="current">{j['title']}</span>
      </nav>
      <span class="eyebrow light">{j['eyebrow']}</span>
      <h1>{j['headline']}</h1>
      {f'<p class="hero-sub"><em>{j["subtitle"]}</em></p>' if j.get('subtitle') else ''}
      <a href="#fechas" class="btn btn-laurel">Ver fechas y precios</a>
    </div>

    <div class="hero-stats">
      <div class="stat-card"><small>Duración</small><strong>{j['duration']}</strong><span>{j['nights']}</span></div>
      <div class="stat-card"><small>Tipo de viaje</small><strong>Pequeño grupo</strong><span>Hasta {j['max_guests']} viajeros</span></div>
      <div class="stat-card"><small>Salidas</small><strong>{j['window']}</strong><span>2026 · 2027</span></div>
      <div class="stat-card"><small>Desde</small><strong>{j['price_from']}</strong><span>Por persona</span></div>
    </div>
  </section>

  <section class="journey-intro">
    <div class="container">
      <div class="intro-grid">
        <div class="intro-text">
          <h2>{j['intro_h2']}</h2>
          <p>{j['intro_p1']}</p>
          <p>{j['intro_p2']}</p>
        </div>
        <div class="intro-portrait"><img src="assets/img/{j['portrait']}" alt="{j['title']}" /></div>
      </div>

      <div class="highlights">
        <div class="highlight"><span class="hi-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a4 4 0 110 8 4 4 0 010-8zM4 22c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg></span><h4>{j['highlights'][0]['t']}</h4><p>{j['highlights'][0]['b']}</p></div>
        <div class="highlight"><span class="hi-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L4 6v6c0 5 3.5 9.5 8 10 4.5-.5 8-5 8-10V6l-8-4z"/></svg></span><h4>{j['highlights'][1]['t']}</h4><p>{j['highlights'][1]['b']}</p></div>
        <div class="highlight"><span class="hi-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 12h18M12 3a15 15 0 010 18M12 3a15 15 0 000 18"/></svg></span><h4>{j['highlights'][2]['t']}</h4><p>{j['highlights'][2]['b']}</p></div>
      </div>
    </div>
  </section>

  <section class="itinerary-sticky">
    <div class="container itinerary-sticky-grid">
      <aside class="itinerary-aside">
        <h2>Itinerario</h2>
        <p class="itin-lede">{j['itin_intro']}</p>
        <div class="map-frame" data-stops='{coords_json}'>
          <img src="assets/img/route-map.jpg" alt="Mapa de la ruta" />
        </div>
        <ul class="map-stops">
{stops_html}
        </ul>
      </aside>
      <div class="itinerary-days">
{days_html}
      </div>
    </div>
  </section>

  <section class="extensions">
    <div class="container">
      <div class="section-head left">
        <h2>Extensiones</h2>
        <p style="color:var(--ink-mute); margin-top: 6px;">Sumá días al final del viaje, con salidas privadas.</p>
      </div>
      <div class="cards-3 ext-grid">
{exts_html}
      </div>
    </div>
  </section>

  <section class="lodges">
    <div class="container">
      <span class="eyebrow">Alojamientos</span>
      <h2>Casas seleccionadas para esta experiencia</h2>
      <div class="lodge-grid">
{lodges_html}
      </div>
    </div>
  </section>

  <section class="dates-prices">
    <div class="container dates-grid">
      <div class="inclusions">
        <h2>Lo que incluye</h2>
        <ul class="check-list">
{incl_html}
        </ul>{excl_html}
      </div>
      <div class="dates-table" id="fechas">
        <h2>Fechas y precios</h2>
        <table>
          <thead><tr><th>Salida</th><th>Disponibilidad</th><th>Precio desde</th><th></th></tr></thead>
          <tbody>
{dates_html}
          </tbody>
        </table>
        <p class="dates-note">Precios por persona en habitación doble. Suplemento de habitación individual a consultar.</p>
      </div>
    </div>
  </section>

  <section class="similar">
    <div class="container">
      <span class="eyebrow">También podría interesarte</span>
      <h2>Otros viajes en pequeño grupo</h2>
      <div class="cards-4">
{similar_html}
      </div>
    </div>
  </section>

{FOOTER}"""

# =============================================================================
# REGION TEMPLATE
# =============================================================================
def build_region(r):
    countries_html = "\n".join([
        f"""        <a href="#" class="country-card">
          <img src="assets/img/{c['img']}" alt="{c['name']}" />
          <div class="country-body">
            <h3>{c['name']}</h3>
            <p>{c['blurb']}</p>
          </div>
        </a>""" for c in r['countries']
    ])
    return f"""{HEAD('Explorar ' + r['name'] + ' · Blisniuk & Amanov', r['meta_desc'])}

{UTILITY_BAR}
{HEADER}

  <nav class="subnav">
    <div class="subnav-inner">
      <a href="#paises" class="active">{r['nav_label']}</a>
      <a href="#formas">Formas de explorar</a>
    </div>
  </nav>

  <section class="region-hero">
    <div class="region-hero-image">
      <img src="assets/img/{r['hero']}" alt="{r['name']}" />
      <div class="region-hero-overlay">
        <h1>Explorá {r['name']}</h1>
        <a href="#paises" class="btn btn-outline-light">{r['cta']} ↓</a>
      </div>
    </div>
    <div class="region-hero-content">
      <nav class="breadcrumb">
        <a href="index.html">Inicio</a>
        <span>/</span>
        <a href="destinations.html">Todos los destinos</a>
        <span>/</span>
        <span class="current">{r['name']}</span>
      </nav>
      <p class="region-lede"><em>{r['lede']}</em></p>
      <p>{r['body']}</p>
    </div>
  </section>

  <section class="region-countries" id="paises">
    <div class="container">
      <h2>Descubrí dónde podemos llevarte</h2>
      <div class="countries-grid">
{countries_html}
      </div>
    </div>
  </section>

  <section class="section ways-explore" id="formas">
    <div class="container">
      <div class="section-head left">
        <h2>Formas de explorar</h2>
      </div>
      <div class="cards-3" style="grid-template-columns: repeat(4, 1fr);">
        <a href="small-group.html" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-group.jpg" alt="Pequeñas expediciones" />
          <div class="img-card-body"><h3>Pequeñas expediciones</h3><p>Aventuras compartidas con un máximo de dieciséis viajeros.</p></div>
        </a>
        <a href="journeys.html" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-private.jpg" alt="Viaje privado" />
          <div class="img-card-body"><h3>Viaje privado</h3><p>A medida, en exclusiva, desde el primer trayecto hasta la última cena.</p></div>
        </a>
        <a href="#" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-cruise.jpg" alt="Crucero" />
          <div class="img-card-body"><h3>Cruceros</h3><p>Llegar al lugar al ritmo del agua.</p></div>
        </a>
        <a href="#" class="img-card" style="aspect-ratio:4/5;">
          <img src="assets/img/way-jet.jpg" alt="Jet privado" />
          <div class="img-card-body"><h3>Jet privado</h3><p>Vuelo de altura para itinerarios singulares.</p></div>
        </a>
      </div>
    </div>
  </section>

{FOOTER}"""

# =============================================================================
# DATA
# =============================================================================
DEFAULT_INCLUDES = [
    "Todos los traslados internos en avioneta y vehículo privado",
    "Pensión completa o media pensión según el itinerario",
    "Líder de viaje hispanohablante",
    "Guías locales especializados",
    "Tasas de ingreso a parques y reservas",
    "Seguro de asistencia al viajero",
    "Aporte a la fundación local de conservación",
]

JOURNEYS = [
    {
        "slug": "botswana-definitivo",
        "title": "Botswana definitivo",
        "headline": "Botswana definitivo 2026",
        "eyebrow": "Pequeña expedición · África austral",
        "meta_desc": "Once días en el Delta del Okavango, Chobe y las Cataratas Victoria, en pequeño grupo y con guías propios.",
        "hero": "j-botswana.jpg", "hero_alt": "Delta del Okavango al amanecer",
        "portrait": "way-safari.jpg",
        "duration": "11 días", "nights": "10 noches", "max_guests": 16,
        "window": "Mayo–Octubre", "price_from": "$14,500 USD",
        "intro_h2": "El África austral en su versión más íntima, con el agua como hilo conductor.",
        "intro_p1": "El Delta del Okavango es el oasis más grande del planeta y un sistema ecológico único: agua dulce filtrándose por el desierto del Kalahari. Lo recorremos en mokoro tradicional, en jeep abierto y a pie, con guías que llevan más de una década en estas islas.",
        "intro_p2": "Combinamos esa quietud con la potencia de Chobe y el rugido de las Cataratas Victoria, en una progresión cuidadosamente cronometrada para terminar en el momento más intenso de cada paisaje.",
        "highlights": [
            {"t": "Mokoro al amanecer", "b": "Una hora de silencio en canoa antes de cualquier otro grupo, con un guía bayei."},
            {"t": "Vuelo en helicóptero sobre el Delta", "b": "Treinta minutos de cabeza panorámica para entender el sistema completo."},
            {"t": "Tres campos privados", "b": "Acceso a concesiones privadas con baja densidad de vehículos y safaris a pie."}
        ],
        "stops": ["Johannesburgo", "Cataratas Victoria", "Chobe", "Sabi Sands", "Khwai", "Delta del Okavango", "Maun"],
        "itin_intro": "Once días, siete escenarios. Cruzamos del Zambezi al Kalahari siguiendo las rutas de los grandes elefantes, con noches en campamentos remotos y concesiones privadas.",
        "days": [
            {"n": 1, "label": "Día 1 · Llegada", "title": "Llegada a Johannesburgo", "body": "Bienvenida en aeropuerto, traslado privado al hotel de descanso y cena con el líder de viaje.", "meals": "Cena", "lodging": "Saxon Hotel", "img": "day-1.jpg"},
            {"n": 2, "label": "Días 2 · 3", "title": "Cataratas Victoria", "body": "Vuelo a Livingstone y dos noches frente a la cortina de agua. Vuelo en helicóptero al amanecer, paseos por las pasarelas y cena en el Royal Livingstone.", "meals": "Pensión completa", "lodging": "Royal Livingstone", "img": "day-2.jpg"},
            {"n": 4, "label": "Días 4 · 5", "title": "Parque Nacional Chobe", "body": "Crucero por el Chobe a la hora dorada para ver elefantes bañándose por centenas. Safaris a la mañana y a la tarde con biólogos del lodge.", "meals": "Pensión completa", "lodging": "Chobe Chilwero", "img": "day-3.jpg"},
            {"n": 6, "label": "Días 6 · 7", "title": "Reserva Khwai · Comunidad", "body": "Concesión privada gestionada por la comunidad Khwai. Safaris a pie, encuentro con los pobladores y noche en un campamento tipo tienda exclusivo.", "meals": "Pensión completa", "lodging": "Khwai Bush Camp", "img": "day-4.jpg"},
            {"n": 8, "label": "Días 8 · 9 · 10", "title": "Corazón del Delta del Okavango", "body": "Tres noches en una isla privada. Mokoro al amanecer, picnics flotantes, vuelos en avioneta sobre el laberinto de canales y safaris al atardecer.", "meals": "Pensión completa", "lodging": "Sanctuary Baines Camp", "img": "day-6.jpg"},
            {"n": 11, "label": "Día 11 · Salida", "title": "Maun y vuelo de regreso", "body": "Vuelo en avioneta a Maun, almuerzo de despedida y conexión a Johannesburgo para el vuelo internacional.", "meals": "Desayuno y almuerzo", "lodging": "—", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Royal Livingstone", "where": "Cataratas Victoria, Zambia", "img": "lodge-1.jpg"},
            {"name": "Chobe Chilwero", "where": "Chobe, Botswana", "img": "lodge-2.jpg"},
            {"name": "Khwai Bush Camp", "where": "Reserva Khwai, Botswana", "img": "lodge-3.jpg"},
            {"name": "Sanctuary Baines Camp", "where": "Delta del Okavango, Botswana", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $4,200 USD", "title": "Ciudad del Cabo y Stellenbosch", "body": "Cuatro noches entre la cima de Table Mountain y los viñedos de Franschhoek.", "img": "dest-southamerica.jpg"},
            {"meta": "+3 días · desde $3,800 USD", "title": "Madikwe Game Reserve", "body": "Reserva privada sin malaria, ideal para sumar antes o después de Botswana.", "img": "dest-kenya.jpg"},
            {"meta": "+5 días · desde $7,900 USD", "title": "Mozambique · Costa de Bazaruto", "body": "Cinco noches en una isla privada del Índico, ideal para descansar tras el safari.", "img": "dest-indianocean.jpg"},
        ],
        "dates": [
            {"date": "10 mayo 2026", "status": "Abierta", "status_class": "open", "price": "$14,500"},
            {"date": "14 junio 2026", "status": "Abierta", "status_class": "open", "price": "$15,200"},
            {"date": "12 julio 2026", "status": "Pocas plazas", "status_class": "few", "price": "$16,800"},
            {"date": "9 agosto 2026", "status": "Lista de espera", "status_class": "closed", "price": "$16,800"},
            {"date": "20 septiembre 2026", "status": "Abierta", "status_class": "open", "price": "$15,900"},
        ],
        "similar": [
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
            {"href": "amazonas-pantanal.html", "img": "dest-southamerica.jpg", "pill": "12 días", "title": "Amazonas y Pantanal"},
            {"href": "egipto-nilo.html", "img": "j-egypt.jpg", "pill": "10 días", "title": "Egipto y el Nilo"},
            {"href": "india-tigres.html", "img": "dest-india.jpg", "pill": "11 días", "title": "India y los tigres"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "amazonas-pantanal",
        "title": "Amazonas y Pantanal",
        "headline": "Amazonas y Pantanal 2026",
        "eyebrow": "Pequeña expedición · Sudamérica",
        "meta_desc": "Doce días en los dos hábitats con mayor densidad de fauna del continente sudamericano.",
        "hero": "day-6.jpg", "hero_alt": "Río amazónico al atardecer",
        "portrait": "way-honey.jpg",
        "duration": "12 días", "nights": "11 noches", "max_guests": 14,
        "window": "Mayo–Noviembre", "price_from": "$11,800 USD",
        "intro_h2": "Dos vidas salvajes distintas en doce días, leídas por naturalistas brasileños.",
        "intro_p1": "El Amazonas concentra la mayor biodiversidad terrestre del planeta. El Pantanal, en cambio, ofrece la mejor visibilidad de fauna mayor del hemisferio: jaguares, tapires, capibaras, tucanes, hocos. Conectamos los dos hábitats en una secuencia que muestra cómo cambia el ecosistema cuando cruzás dos mil kilómetros al sur.",
        "intro_p2": "Navegamos en embarcaciones pequeñas, dormimos en posadas familiares y descansamos en lodges premiados. El ritmo es contemplativo: amanecer temprano, siesta al mediodía, navegación nocturna cuando el silencio cambia de textura.",
        "highlights": [
            {"t": "Búsqueda de jaguares", "b": "Tres días en Porto Jofre, capital mundial del avistamiento de yaguareté, con guías que conocen a cada individuo."},
            {"t": "Río Negro en barco privado", "b": "Cuatro días en un barco fluvial de doce camarotes, cocina autoral con productos del bosque."},
            {"t": "Comunidades ribereñas", "b": "Encuentro con familias caboclo en el Amazonas y peón pantaneiro en el Pantanal."}
        ],
        "stops": ["Manaos", "Río Negro", "Anavilhanas", "Cuiabá", "Transpantaneira", "Porto Jofre", "Foz do Iguaçú"],
        "itin_intro": "De Manaos a Iguazú, de la selva inundada al humedal más grande del mundo, en doce días con dos noches en barco y siete en posadas seleccionadas.",
        "days": [
            {"n": 1, "label": "Día 1 · Llegada", "title": "Llegada a Manaos", "body": "Bienvenida en el aeropuerto, traslado al hotel boutique en el casco antiguo y cena de orientación.", "meals": "Cena", "lodging": "Villa Amazônia", "img": "day-1.jpg"},
            {"n": 2, "label": "Días 2 · 3 · 4", "title": "Río Negro en barco", "body": "Embarque en el M/Y Tucano. Navegación entre el archipiélago de Anavilhanas, caminatas en selva firme, baños en arroyos negros y avistamiento de delfines rosados.", "meals": "Pensión completa", "lodging": "M/Y Tucano (barco)", "img": "day-6.jpg"},
            {"n": 5, "label": "Días 5 · 6", "title": "Vuelo a Cuiabá", "body": "Vuelo doméstico al sur. Una noche en Cuiabá y traslado por la Transpantaneira hacia el corazón del humedal.", "meals": "Desayuno y cena", "lodging": "Pousada Piuval", "img": "day-3.jpg"},
            {"n": 7, "label": "Días 7 · 8 · 9", "title": "Porto Jofre · En busca de jaguares", "body": "Tres días navegando los ríos Cuiabá y Três Irmãos en lanchas con biólogos. La densidad de jaguar más alta del planeta.", "meals": "Pensión completa", "lodging": "Hotel Pantanal Norte", "img": "day-4.jpg"},
            {"n": 10, "label": "Días 10 · 11", "title": "Cataratas del Iguazú", "body": "Vuelo a Foz do Iguaçú. Visitamos el lado brasileño y el argentino, con paseo en lancha hasta la garganta del Diablo y cena al lado de las cataratas.", "meals": "Pensión completa", "lodging": "Belmond Hotel das Cataratas", "img": "day-2.jpg"},
            {"n": 12, "label": "Día 12 · Salida", "title": "Regreso", "body": "Mañana libre, conexión a São Paulo y vuelo internacional.", "meals": "Desayuno", "lodging": "—", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Villa Amazônia", "where": "Manaos, Brasil", "img": "lodge-1.jpg"},
            {"name": "M/Y Tucano", "where": "Río Negro, Brasil", "img": "lodge-3.jpg"},
            {"name": "Hotel Pantanal Norte", "where": "Porto Jofre, Brasil", "img": "lodge-2.jpg"},
            {"name": "Belmond das Cataratas", "where": "Foz do Iguaçú, Brasil", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $2,900 USD", "title": "Bahía y Salvador", "body": "Tres noches en la capital del candomblé, con cocina baiana y arquitectura colonial.", "img": "dest-spain.jpg"},
            {"meta": "+4 días · desde $4,500 USD", "title": "Río de Janeiro", "body": "Cuatro noches en Ipanema, con vista a Corcovado y cena al pie del Pão de Açúcar.", "img": "dest-southamerica.jpg"},
            {"meta": "+5 días · desde $6,200 USD", "title": "Patagonia chilena", "body": "Cinco noches en Torres del Paine para sumar el polo opuesto del continente.", "img": "dest-patagonia.jpg"},
        ],
        "dates": [
            {"date": "8 mayo 2026", "status": "Abierta", "status_class": "open", "price": "$11,800"},
            {"date": "5 junio 2026", "status": "Abierta", "status_class": "open", "price": "$12,400"},
            {"date": "10 julio 2026", "status": "Pocas plazas", "status_class": "few", "price": "$13,200"},
            {"date": "21 agosto 2026", "status": "Abierta", "status_class": "open", "price": "$13,200"},
            {"date": "25 septiembre 2026", "status": "Abierta", "status_class": "open", "price": "$12,400"},
        ],
        "similar": [
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
            {"href": "botswana-definitivo.html", "img": "j-botswana.jpg", "pill": "11 días", "title": "Botswana definitivo"},
            {"href": "patagonia-circuito.html", "img": "dest-patagonia.jpg", "pill": "10 días", "title": "Patagonia · Circuito completo"},
            {"href": "peru-machu-picchu.html", "img": "j-peru.jpg", "pill": "8 días", "title": "Perú y Machu Picchu"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "piamonte-tartufo",
        "title": "Piamonte",
        "headline": "Piamonte",
        "subtitle": "Tartufo, Nebbiolo y Pavese · Edición octubre 2026",
        "eyebrow": "Pequeño grupo · Italia · Otoño",
        "meta_desc": "Ocho días en las Langhe en el peak de la temporada del tartufo bianco. Bodegas históricas, caza al amanecer y la casa natal de Pavese. La única ventana del año en que todo coincide al mismo tiempo.",
        "hero": "hero-piamonte-tartufo.jpg", "hero_alt": "Viñedos de las Langhe en octubre con niebla baja",
        "portrait": "wildlife-piamonte-tartufo.jpg",
        "duration": "8 días", "nights": "7 noches", "max_guests": 8,
        "window": "Octubre", "price_from": "$8,450 USD",
        "intro_h2": "Ocho días en el Piamonte gastronómico y literario, en la única ventana del año en que todo sucede al mismo tiempo.",
        "intro_p1": "A mediados de octubre, las Langhe entran en su momento más pleno: los grandes domaines terminan la cosecha del Nebbiolo, los trifolau salen al amanecer a buscar el primer tartufo bianco de la temporada, las hojas de las viñas se ponen rojas, y los productores chicos están en el ritmo más fértil del año. Ir tres semanas antes de la subasta de Alba significa producto fresco, productores no saturados de prensa, y el campo todavía respirando a su ritmo humano.",
        "intro_p2": "Nos instalamos en una cascina de uso exclusivo en Santo Stefano Belbo — la casa natal de Cesare Pavese, el escenario de <em>La luna y las hogueras</em>. Desde ahí salimos a Barbaresco, Barolo, Pollenzo, las catedrales subterráneas de Canelli. Pero también volvemos cada noche a casa, donde una cocinera del pueblo nos espera, donde el sommelier abre vinos en el jardín, y donde la sobremesa se vuelve el corazón del viaje.",
        "highlights": [
            {"t": "La trufa, al amanecer", "b": "Caza con un trifolau de linaje en los bosques del Belbo, a las cinco y media de la madrugada, seguida del desayuno con frittata de tartufo en su casa familiar."},
            {"t": "El Nebbiolo en tres voces", "b": "Produttori del Barbaresco con sus nueve cru comparados, una visita extendida a Vajra en Barolo, y una cata vertical histórica (1985, 1996, 2004, 2016) en la cascina, moderada por nuestro sommelier."},
            {"t": "La cena donde somos anfitriones", "b": "La última noche cambia el rol: invitamos a las familias productoras que abrieron sus cantinas durante la semana. Asado al fuego en el jardín de la cascina, vinos que ellos traen, mate al final."}
        ],
        "stops": ["Santo Stefano Belbo", "Canelli", "Barbaresco", "Treiso", "Alba", "Pollenzo", "Bra", "Barolo"],
        "itin_intro": "Ocho días, una sola base, un solo grupo. Empezamos en la cascina con una cena cocinada en casa por una cocinera del pueblo y terminamos siete noches después en el mismo jardín, con los productores que conocimos durante la semana sentados a la mesa como nuestros invitados. En el medio: una caza de trufas a las cinco y media de la madrugada, los nueve cru del Barbaresco comparados en una sola cata, las catedrales subterráneas de Canelli, la casa natal de Pavese, una vertical de Nebbiolo en la cascina iluminada por velas, y una cena estrellada en la única terraza del Piamonte donde el ocaso cae sobre las Langhe.",
        "days": [
            {"n": 1, "label": "Día 1 · Llegada", "title": "Bienvenida en la cascina", "body": "Llegadas escalonadas desde Torino o Milán. Check-in en la casa de Santo Stefano Belbo. Aperitivo en el jardín con vermut local y Moscato d'Asti, cena de bienvenida cocinada por la cocinera del pueblo: tajarin al ragù, brasato al Barolo, bonet. El sommelier presenta el viaje.", "meals": "Cena", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-1.jpg"},
            {"n": 2, "label": "Día 2 · Pavese y Canelli", "title": "La casa del escritor y las catedrales subterráneas", "body": "Caminata por Santo Stefano Belbo y visita a la Fondazione Cesare Pavese y la casa natal. Almuerzo en la Enoteca Regionale di Canelli. Por la tarde, descenso a las Catedrales Subterráneas de Canelli, las antiguas bodegas históricas de espumantes inscriptas por UNESCO. Cata final. Cena ligera en casa.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-2.jpg"},
            {"n": 3, "label": "Día 3 · Barbaresco", "title": "Los nueve cru", "body": "Visita y cata comparativa en Produttori del Barbaresco — los nueve cru Riserva en una sola sesión. Almuerzo en Trattoria Antica Torre, en el corazón del pueblo. Por la tarde, cata íntima en Roagna: Barbaresco artesanal, sin filtración. Vuelta vía el Bricco di Treiso para el ocaso. Cena en casa con sobremesa larga.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-3.jpg"},
            {"n": 4, "label": "Día 4 · La trufa", "title": "Amanecer en el bosque y cena estrellada", "body": "5:30 caza con trifolau y su lagotto romagnolo, seguida del desayuno en su casa familiar. Vuelta a la cascina para una larga siesta. Por la tarde, MUDET — Museo del Tartufo en Alba y paseo por el centro histórico. La cena, en la terraza de La Ciau del Tornavento (1 estrella Michelin), justo cuando el ocaso cae sobre las Langhe.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-4.jpg"},
            {"n": 5, "label": "Día 5 · Pollenzo y Bra", "title": "La idea del Slow Food", "body": "Mañana en la Università di Scienze Gastronomiche de Pollenzo con una sesión sobre el manifiesto del Slow Food, la biodiversidad alimentaria y los Presidi. Almuerzo en el Albergo dell'Agenzia. Tarde en la Banca del Vino (350.000 botellas conservadas) y caminata por Bra, la ciudad donde nació el movimiento en 1986. Aperitivo en Boccondivino, el restaurante fundacional. Cena ligera en casa.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-2.jpg"},
            {"n": 6, "label": "Día 6 · Barolo", "title": "El Nebbiolo y la vertical histórica", "body": "Visita extendida y cata vertical en G.D. Vajra, con almuerzo en cantina junto a la familia Vaira. Por la tarde, WiMu — Museo del Vino en el Castello di Barolo, y mirador de La Morra. Cena en casa preparada por la cocinera, y a las 22:30 la cata histórica vertical: cuatro Nebbiolos de 1985, 1996, 2004 y 2016, moderada por nuestro sommelier.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-3.jpg"},
            {"n": 7, "label": "Día 7 · La noche B&A", "title": "Cuando nosotros somos los anfitriones", "body": "Mañana libre — caminata opcional por el Sentiero Pavesiano o tarde tranquila en el jardín. Visita opcional al productor de avellana Tonda Gentile o al quesero de Castelmagno. A la noche, la cena B&A: las familias productoras que abrieron sus cantinas durante la semana llegan como nuestros invitados. Asado al fuego en el patio de la cascina, vinos que ellos traen, mate y dulce de leche al final. Lectura del último párrafo de <em>La luna y las hogueras</em>.", "meals": "Pensión completa", "lodging": "Cascina privada en Santo Stefano Belbo", "img": "day-piamonte-tartufo-1.jpg"},
            {"n": 8, "label": "Día 8 · Despedida", "title": "Vuelta", "body": "Desayuno tranquilo. Traslados escalonados a Torino Caselle o Milán Malpensa según horarios de vuelo. Parada opcional en Asti o Cherasco camino al aeropuerto.", "meals": "Desayuno", "lodging": "—", "img": "day-piamonte-tartufo-4.jpg"},
        ],
        "lodges": [
            {"name": "Cascina privada Santo Stefano Belbo", "where": "Santo Stefano Belbo, Langa Astigiana, Cuneo", "img": "lodge-piamonte-tartufo-1.jpg"},
            {"name": "Cantine Contratto · Catedrales Subterráneas", "where": "Canelli — Patrimonio UNESCO", "img": "lodge-piamonte-tartufo-2.jpg"},
            {"name": "G.D. Vajra", "where": "Vergne, Barolo", "img": "lodge-piamonte-tartufo-3.jpg"},
            {"name": "La Ciau del Tornavento", "where": "Treiso · 1 estrella Michelin", "img": "lodge-piamonte-tartufo-4.jpg"},
        ],
        "extensions": [
            {"meta": "+2 días · desde $1,450 USD", "title": "Torino antes · capital del Risorgimento", "body": "Caffè reales (Al Bicerin, Mulassano), Museo Egizio (el segundo más grande del mundo), Pinacoteca Agnelli y una cata de vermut en Carpano.", "img": "dest-italy.jpg"},
            {"meta": "+3 días · desde $2,850 USD", "title": "Lago di Como después · descompresión", "body": "Bellagio, Villa Carlotta, Villa del Balbianello y dos noches en Villa d'Este. El descanso después de las Langhe, con el ritmo del lago.", "img": "dest-europe.jpg"},
            {"meta": "+2 días · desde $1,650 USD", "title": "Milán antes · diseño y Triennale", "body": "Triennale di Milano, Fondazione Prada, Bagatti Valsecchi y una cena en Cracco. La precondición urbana al campo.", "img": "j-italy.jpg"},
        ],
        "dates": [
            {"date": "Vie 16 oct – Vie 23 oct 2026", "status": "Abierta", "status_class": "open", "price": "$8,450"},
            {"date": "Vie 15 oct – Vie 22 oct 2027", "status": "Abierta", "status_class": "open", "price": "$9,750"},
        ],
        "similar": [
            {"href": "espana-portugal.html", "img": "j-spainport.jpg", "pill": "14 días", "title": "España y Portugal"},
            {"href": "japon-clasico.html", "img": "j-japan.jpg", "pill": "9 días", "title": "Japón clásico"},
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
            {"href": "angkor-sudeste-asiatico.html", "img": "j-asia.jpg", "pill": "15 días", "title": "Angkor y Sudeste Asiático"},
        ],
        "includes": [
            "7 noches en cascina privada en Santo Stefano Belbo (uso exclusivo del grupo)",
            "Pensión completa: 7 desayunos, 7 almuerzos, 7 cenas",
            "Cocinera local que prepara los desayunos y las cenas en casa",
            "1 cena en restaurante 1 estrella Michelin (La Ciau del Tornavento)",
            "Cata histórica vertical de Nebbiolo (4 añadas: 1985, 1996, 2004, 2016) en la cascina",
            "Caza de tartufo bianco al amanecer con trifolau de linaje + desayuno en su casa",
            "Visitas y catas con productores: Produttori del Barbaresco, Roagna, G.D. Vajra",
            "Visita a las Catedrales Subterráneas de Canelli (Patrimonio UNESCO)",
            "Visita a la Fondazione Cesare Pavese y la casa natal",
            "Sesión académica en Università di Scienze Gastronomiche, Pollenzo",
            "Visita guiada a la Banca del Vino, Pollenzo",
            "MUDET — Museo del Tartufo, Alba",
            "WiMu — Museo del Vino, Castello di Barolo",
            "La cena B&amp;A en la cascina (productores invitados, asado al fuego)",
            "Sommelier italoparlante acompañando al grupo toda la semana",
            "Fotógrafo profesional documentando los 8 días + libro custom impreso para cada pasajero",
            "Kit B&amp;A pre-viaje: 5 libros (incluyendo <em>La luna y las hogueras</em> de Pavese), journal de cuero, mapa de las Langhe, carta de bienvenida",
            "Detalles diarios: flores frescas, cartas manuscritas con el plan del día",
            "Dos furgones privados con chofer durante los 8 días",
            "Traslados aeropuerto-cascina-aeropuerto (Torino Caselle o Milán Malpensa)",
            "Anfitrión B&amp;A en piso durante toda la semana",
            "Aporte a la Fundación B&amp;A (3% del valor del viaje)",
        ],
        "excludes": [
            "Vuelos internacionales desde/hacia Latinoamérica",
            "Seguro de viaje (B&amp;A lo coordina a costo)",
            "Bebidas premium y vinos de cellar fuera del programa",
            "Gastos personales y compras (incluida la trufa que cada pasajero quiera llevar)",
            "Propinas opcionales para el equipo en piso",
            "Extensiones pre y post viaje (cotizadas por separado)",
        ],
    },
    {
        "slug": "japon-clasico",
        "title": "Japón clásico",
        "headline": "Japón clásico 2026",
        "eyebrow": "Pequeña expedición · Asia",
        "meta_desc": "Nueve días entre Tokio, Kioto y los Alpes japoneses, con encuentros con artesanos y maestros del té.",
        "hero": "j-japan.jpg", "hero_alt": "Templo japonés al amanecer",
        "portrait": "dest-japan.jpg",
        "duration": "9 días", "nights": "8 noches", "max_guests": 18,
        "window": "Marzo–Noviembre", "price_from": "$11,800 USD",
        "intro_h2": "Nueve días de Honshu, leído por dentro y por sus oficios.",
        "intro_p1": "Japón no se entiende mirando — se entiende escuchando, cocinando, mirando con paciencia. Por eso este itinerario tiene tan poco de checklist y tanto de encuentros: ceremonia del té con un maestro de la escuela Urasenke, visita al taller de un cuchillero de Sakai, cena con una geiko en un ochaya de Pontochô.",
        "intro_p2": "Combinamos Tokio (tres noches), un par de noches en un ryokan tradicional en Hakone con vista al monte Fuji y cuatro noches en Kioto, capital cultural del país.",
        "highlights": [
            {"t": "Ceremonia del té con maestro Urasenke", "b": "Una hora íntima en una casa de té de Kioto, sólo para nuestro grupo."},
            {"t": "Ryokan con onsen privado", "b": "Dos noches en un ryokan tradicional, con cena kaiseki y onsen privado al aire libre."},
            {"t": "Cena con geiko", "b": "Velada en un ochaya de Pontochô con geiko y maiko (cena kaiseki y juegos tradicionales)."}
        ],
        "stops": ["Tokio", "Hakone", "Kioto", "Nara", "Osaka"],
        "itin_intro": "Nueve días con dos cambios de base. Tokio, ryokan en Hakone, Kioto. El ritmo es contemplativo, las mañanas tempranas, las tardes con espacio para perderse.",
        "days": [
            {"n": 1, "label": "Días 1 · 2 · 3", "title": "Tokio", "body": "Bienvenida en Haneda. Tres noches en Aman Tokyo. Mercado Toyosu al amanecer, paseo por Yanaka y cena privada con chef estrella en un sushi-ya de ocho cubiertos.", "meals": "Pensión completa", "lodging": "Aman Tokyo", "img": "day-1.jpg"},
            {"n": 4, "label": "Días 4 · 5", "title": "Hakone y monte Fuji", "body": "Salida en tren bala. Dos noches en un ryokan tradicional con vista al Fuji. Onsen privado, cena kaiseki y caminata por el lago Ashi.", "meals": "Pensión completa", "lodging": "Gora Kadan", "img": "day-2.jpg"},
            {"n": 6, "label": "Días 6 · 7 · 8", "title": "Kioto", "body": "Cuatro noches en la capital cultural. Templos al amanecer (Fushimi Inari sin gente), bosque de bambú de Arashiyama, ceremonia del té y cena con geiko.", "meals": "Pensión completa", "lodging": "Aman Kyoto", "img": "day-3.jpg"},
            {"n": 9, "label": "Día 9 · Salida", "title": "Vuelo desde Osaka", "body": "Mañana libre, traslado a Kansai y vuelo internacional. Para quienes lo deseen, extensión a Nara con su parque de ciervos.", "meals": "Desayuno", "lodging": "—", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Aman Tokyo", "where": "Tokio, Japón", "img": "lodge-2.jpg"},
            {"name": "Gora Kadan", "where": "Hakone, Japón", "img": "lodge-3.jpg"},
            {"name": "Aman Kyoto", "where": "Kioto, Japón", "img": "lodge-1.jpg"},
            {"name": "Tawaraya Ryokan", "where": "Kioto, Japón", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+3 días · desde $3,900 USD", "title": "Alta cocina y sake", "body": "Tres noches en Niigata con cata privada de tres bodegas de sake.", "img": "dest-japan.jpg"},
            {"meta": "+5 días · desde $7,200 USD", "title": "Hokkaido", "body": "Cinco noches en la isla del norte con onsens en la nieve y mariscos del estrecho.", "img": "dest-arctic.jpg"},
            {"meta": "+4 días · desde $5,400 USD", "title": "Shikoku", "body": "Ruta de los 88 templos en autos privados, dormida en hoteles boutique y aguas termales.", "img": "dest-asia.jpg"},
        ],
        "dates": [
            {"date": "4 abril 2026", "status": "Pocas plazas", "status_class": "few", "price": "$12,400"},
            {"date": "16 mayo 2026", "status": "Abierta", "status_class": "open", "price": "$11,800"},
            {"date": "19 septiembre 2026", "status": "Abierta", "status_class": "open", "price": "$11,800"},
            {"date": "17 octubre 2026", "status": "Pocas plazas", "status_class": "few", "price": "$12,800"},
            {"date": "14 noviembre 2026", "status": "Abierta", "status_class": "open", "price": "$12,400"},
        ],
        "similar": [
            {"href": "angkor-sudeste-asiatico.html", "img": "j-asia.jpg", "pill": "15 días", "title": "Angkor y Sudeste Asiático"},
            {"href": "india-tigres.html", "img": "dest-india.jpg", "pill": "11 días", "title": "India y los tigres"},
            {"href": "piamonte-tartufo.html", "img": "j-italy.jpg", "pill": "8 días", "title": "Piamonte"},
            {"href": "peru-machu-picchu.html", "img": "j-peru.jpg", "pill": "8 días", "title": "Perú y Machu Picchu"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "egipto-nilo",
        "title": "Egipto y el Nilo",
        "headline": "Egipto y el Nilo 2026",
        "eyebrow": "Pequeña expedición · Norte de África",
        "meta_desc": "Diez días entre las pirámides de Giza y el alto Nilo, en pequeño grupo con egiptólogos propios.",
        "hero": "j-egypt.jpg", "hero_alt": "Vista del Nilo al amanecer",
        "portrait": "dest-morocco.jpg",
        "duration": "10 días", "nights": "9 noches", "max_guests": 18,
        "window": "Octubre–Abril", "price_from": "$11,200 USD",
        "intro_h2": "Diez días con tres egiptólogos: uno académico, uno arqueólogo, uno guía.",
        "intro_p1": "Egipto no es un país que se visite — es uno que se lee. Por eso este itinerario está pensado más como un curso intensivo que como un tour. Tres egiptólogos viajan con nosotros y se van alternando según el sitio: en Giza con un arqueólogo del SCA, en Luxor con una académica de Cambridge, en Abu Simbel con un especialista en cultura nubia.",
        "intro_p2": "Combinamos cuatro noches en El Cairo y tres noches a bordo de una dahabiya tradicional navegando del alto Nilo. Cerramos en Asuán y Abu Simbel.",
        "highlights": [
            {"t": "Pirámides al amanecer", "b": "Acceso fuera de horario al recinto de Giza, sin más visitantes."},
            {"t": "Dahabiya tradicional", "b": "Tres noches a bordo de un velero del Nilo, doce camarotes, recorrido lento entre templos."},
            {"t": "Abu Simbel privado", "b": "Visita en privado al templo de Ramsés II y vuelo escénico sobre el lago Nasser."}
        ],
        "stops": ["El Cairo", "Saqqara", "Luxor", "Edfu", "Kom Ombo", "Asuán", "Abu Simbel"],
        "itin_intro": "De Giza a la frontera con Sudán siguiendo la línea verde del Nilo. Diez días, tres bases, un solo país que cambió la idea de tiempo.",
        "days": [
            {"n": 1, "label": "Días 1 · 2 · 3 · 4", "title": "El Cairo y sus pirámides", "body": "Bienvenida en aeropuerto. Cuatro noches en el Marriott Mena House con vista a las pirámides. Saqqara, museo Egipcio, mercado Khan el-Khalili y cena privada al pie de la Esfinge.", "meals": "Pensión completa", "lodging": "Marriott Mena House", "img": "day-1.jpg"},
            {"n": 5, "label": "Día 5", "title": "Vuelo a Luxor", "body": "Vuelo doméstico al alto Nilo. Visita al Valle de los Reyes (incluida la tumba de Tutankamón) y al templo de Hatshepsut.", "meals": "Desayuno y almuerzo", "lodging": "Sofitel Old Winter Palace", "img": "day-2.jpg"},
            {"n": 6, "label": "Días 6 · 7 · 8", "title": "Dahabiya en el Nilo", "body": "Embarque en una dahabiya privada de doce camarotes. Tres noches navegando entre Esna, Edfu, Kom Ombo. Cenas en cubierta, baños en pozas tranquilas.", "meals": "Pensión completa", "lodging": "Dahabiya privada", "img": "day-6.jpg"},
            {"n": 9, "label": "Día 9", "title": "Asuán y Abu Simbel", "body": "Vuelo al sur, visita privada al templo de Ramsés II al amanecer y tarde en Asuán con paseo en faluca.", "meals": "Pensión completa", "lodging": "Old Cataract Aswan", "img": "day-4.jpg"},
            {"n": 10, "label": "Día 10 · Salida", "title": "Regreso", "body": "Vuelo a El Cairo y conexión internacional.", "meals": "Desayuno", "lodging": "—", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Marriott Mena House", "where": "Giza, Egipto", "img": "lodge-2.jpg"},
            {"name": "Sofitel Old Winter Palace", "where": "Luxor, Egipto", "img": "lodge-3.jpg"},
            {"name": "Dahabiya privada", "where": "Río Nilo", "img": "lodge-4.jpg"},
            {"name": "Old Cataract Aswan", "where": "Asuán, Egipto", "img": "lodge-1.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $4,800 USD", "title": "Jordania · Petra y Wadi Rum", "body": "Cuatro noches en Jordania con visita privada a Petra y desierto en Wadi Rum.", "img": "dest-mena.jpg"},
            {"meta": "+3 días · desde $3,200 USD", "title": "Alejandría y el Mediterráneo", "body": "Tres noches en la antigua capital ptolemaica.", "img": "dest-europe.jpg"},
            {"meta": "+5 días · desde $5,900 USD", "title": "Mar Rojo · Hurghada", "body": "Cinco días de snorkel y descanso en la costa egipcia.", "img": "dest-indianocean.jpg"},
        ],
        "dates": [
            {"date": "11 octubre 2026", "status": "Abierta", "status_class": "open", "price": "$11,200"},
            {"date": "8 noviembre 2026", "status": "Pocas plazas", "status_class": "few", "price": "$11,800"},
            {"date": "10 enero 2027", "status": "Abierta", "status_class": "open", "price": "$12,400"},
            {"date": "21 febrero 2027", "status": "Lista de espera", "status_class": "closed", "price": "$12,400"},
            {"date": "14 marzo 2027", "status": "Abierta", "status_class": "open", "price": "$11,800"},
        ],
        "similar": [
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
            {"href": "japon-clasico.html", "img": "j-japan.jpg", "pill": "9 días", "title": "Japón clásico"},
            {"href": "india-tigres.html", "img": "dest-india.jpg", "pill": "11 días", "title": "India y los tigres"},
            {"href": "piamonte-tartufo.html", "img": "j-italy.jpg", "pill": "8 días", "title": "Piamonte"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "patagonia-circuito",
        "title": "Patagonia · Circuito completo",
        "headline": "Patagonia · Circuito completo 2026",
        "eyebrow": "Pequeña expedición · Sudamérica",
        "meta_desc": "Diez días en la Patagonia argentina y chilena: Calafate, Torres del Paine, Ushuaia y la Tierra del Fuego.",
        "hero": "dest-patagonia.jpg", "hero_alt": "Glaciar al amanecer en la Patagonia",
        "portrait": "dest-arctic.jpg",
        "duration": "10 días", "nights": "9 noches", "max_guests": 14,
        "window": "Noviembre–Marzo", "price_from": "$10,800 USD",
        "intro_h2": "Diez días donde el continente se acaba — glaciares vivos, estepa infinita y cielos sin polución.",
        "intro_p1": "La Patagonia es la única región del mundo donde el aire huele a hielo. Empezamos en Calafate frente al Perito Moreno, cruzamos al lado chileno para tres noches en Torres del Paine y bajamos hasta Ushuaia para navegar el Canal Beagle hasta la isla de los lobos marinos.",
        "intro_p2": "Combinamos hotelería de lujo con campamentos seleccionados. Caminamos cada día, leemos a Bruce Chatwin de noche y dormimos cuando el sol decide.",
        "highlights": [
            {"t": "Big Ice en el Perito Moreno", "b": "Travesía de cuatro horas sobre el hielo con guías de montaña certificados."},
            {"t": "Torres del Paine en helicóptero", "b": "Vuelo escénico al amanecer sobre los tres picos icónicos del parque."},
            {"t": "Canal Beagle privado", "b": "Navegación en lancha exclusiva hasta el faro Les Éclaireurs y la isla H."}
        ],
        "stops": ["Buenos Aires", "El Calafate", "Perito Moreno", "Torres del Paine", "Puerto Natales", "Ushuaia", "Canal Beagle"],
        "itin_intro": "Diez días, dos países, tres tipos de paisaje. Empezamos en Buenos Aires y cerramos en el confín del continente.",
        "days": [
            {"n": 1, "label": "Día 1", "title": "Buenos Aires", "body": "Bienvenida en Ezeiza, traslado al hotel boutique en San Telmo y cena de orientación con guía argentino.", "meals": "Cena", "lodging": "Palacio Duhau · Park Hyatt", "img": "day-1.jpg"},
            {"n": 2, "label": "Días 2 · 3", "title": "Calafate y Perito Moreno", "body": "Vuelo doméstico al sur. Dos noches frente al glaciar. Travesía Big Ice (caminata sobre el hielo) y navegación por el frente del glaciar.", "meals": "Pensión completa", "lodging": "Eolo Patagonia", "img": "day-2.jpg"},
            {"n": 4, "label": "Días 4 · 5 · 6", "title": "Torres del Paine", "body": "Cruce de la frontera con Chile. Tres noches en Explora Patagonia. Cabalgatas, trekking suave a la Base de las Torres y vuelo en helicóptero al amanecer.", "meals": "Pensión completa", "lodging": "Explora Patagonia", "img": "day-3.jpg"},
            {"n": 7, "label": "Días 7 · 8 · 9", "title": "Ushuaia y Canal Beagle", "body": "Vuelo a Ushuaia. Tres noches en el Arakur con vista al canal. Navegación privada hasta la isla H, parque nacional Tierra del Fuego y tren del Fin del Mundo.", "meals": "Pensión completa", "lodging": "Arakur Ushuaia", "img": "day-6.jpg"},
            {"n": 10, "label": "Día 10 · Salida", "title": "Regreso a Buenos Aires", "body": "Vuelo del fin del mundo a Buenos Aires y conexión internacional.", "meals": "Desayuno", "lodging": "—", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Palacio Duhau", "where": "Buenos Aires, Argentina", "img": "lodge-2.jpg"},
            {"name": "Eolo Patagonia", "where": "El Calafate, Argentina", "img": "lodge-3.jpg"},
            {"name": "Explora Patagonia", "where": "Torres del Paine, Chile", "img": "lodge-1.jpg"},
            {"name": "Arakur Ushuaia", "where": "Ushuaia, Argentina", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $5,200 USD", "title": "Cataratas del Iguazú", "body": "Cuatro días en el norte de Argentina, con hotel dentro del parque.", "img": "dest-southamerica.jpg"},
            {"meta": "+5 días · desde $6,800 USD", "title": "Antártida en buque chico", "body": "Crucero de cinco días al continente blanco desde Ushuaia.", "img": "dest-arctic.jpg"},
            {"meta": "+3 días · desde $3,600 USD", "title": "Valle de Uco · Mendoza", "body": "Tres noches entre bodegas de altura en el sur mendocino.", "img": "dest-spain.jpg"},
        ],
        "dates": [
            {"date": "10 noviembre 2026", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "5 diciembre 2026", "status": "Pocas plazas", "status_class": "few", "price": "$11,800"},
            {"date": "9 enero 2027", "status": "Abierta", "status_class": "open", "price": "$12,400"},
            {"date": "13 febrero 2027", "status": "Lista de espera", "status_class": "closed", "price": "$12,400"},
            {"date": "13 marzo 2027", "status": "Abierta", "status_class": "open", "price": "$11,200"},
        ],
        "similar": [
            {"href": "amazonas-pantanal.html", "img": "dest-southamerica.jpg", "pill": "12 días", "title": "Amazonas y Pantanal"},
            {"href": "peru-machu-picchu.html", "img": "j-peru.jpg", "pill": "8 días", "title": "Perú y Machu Picchu"},
            {"href": "alaska-familiar.html", "img": "j-alaska.jpg", "pill": "8 días", "title": "Alaska familiar"},
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "espana-portugal",
        "title": "España y Portugal · 10 ciudades extraordinarias",
        "headline": "España y Portugal 2026",
        "eyebrow": "Pequeña expedición · Europa",
        "meta_desc": "Catorce días entre Lisboa, Andalucía y Cataluña — dos países contiguos y dos sensibilidades distintas.",
        "hero": "j-spainport.jpg", "hero_alt": "Plaza ibérica al atardecer",
        "portrait": "dest-spain.jpg",
        "duration": "14 días", "nights": "13 noches", "max_guests": 18,
        "window": "Abril–Octubre", "price_from": "$16,800 USD",
        "intro_h2": "Dos países, diez ciudades, una pregunta: ¿cómo es que la península ibérica se las arregla para sentir tan distinta cada cien kilómetros?",
        "intro_p1": "Comenzamos en Lisboa, donde el azulejo y el fado conviven con la cocina más interesante del Atlántico. Cruzamos el Alentejo hasta Sevilla — capital andaluza, sus bodegas de jerez en sanlúcar, sus plazas y patios. Subimos a Granada (acceso reservado a la Alhambra al amanecer), bajamos a Córdoba, después Madrid en sus mejores tabernas y Barcelona para cerrar.",
        "intro_p2": "Comemos en doce mesas seleccionadas — algunas con estrella, algunas sin pretensión. Dormimos en cuatro paradores históricos y dos hoteles boutique. Caminamos cada día.",
        "highlights": [
            {"t": "Alhambra al amanecer", "b": "Acceso a los Palacios Nazaríes una hora antes de la apertura al público."},
            {"t": "Bodegas con sumiller propio", "b": "Cata vertical de cinco bodegas en el triángulo del jerez."},
            {"t": "Tabernas con historia", "b": "Almuerzos privados en cuatro mesas centenarias en Madrid y Barcelona."}
        ],
        "stops": ["Lisboa", "Évora", "Sevilla", "Granada", "Córdoba", "Madrid", "Toledo", "Bilbao", "Barcelona"],
        "itin_intro": "Catorce días en avance lento del Atlántico al Mediterráneo, pasando por todas las cocinas y todos los climas ibéricos.",
        "days": [
            {"n": 1, "label": "Días 1 · 2 · 3", "title": "Lisboa", "body": "Bienvenida en aeropuerto. Tres noches en el Bairro Alto. Tour privado por los barrios históricos, cena de fado en una casa centenaria y mañana en Belém.", "meals": "Pensión completa", "lodging": "Bairro Alto Hotel", "img": "day-1.jpg"},
            {"n": 4, "label": "Días 4 · 5", "title": "Évora y entrada a Andalucía", "body": "Visita al Templo Romano, cena en una herdade alentejana y traslado a Sevilla. Una tarde por el Real Alcázar.", "meals": "Pensión completa", "lodging": "Hotel Alfonso XIII", "img": "day-3.jpg"},
            {"n": 6, "label": "Días 6 · 7", "title": "Granada y la Alhambra", "body": "Acceso privado a los Palacios Nazaríes al amanecer, sin nadie más. Tarde en el Albaicín y cena de tapas en una bodega del siglo XVIII.", "meals": "Pensión completa", "lodging": "Hotel Alhambra Palace", "img": "day-4.jpg"},
            {"n": 8, "label": "Días 8 · 9 · 10", "title": "Madrid", "body": "Vuelo a Madrid. Tres noches en el Ritz. Mañana en el Prado con curador, mercado de San Miguel y excursión a Toledo.", "meals": "Pensión completa", "lodging": "Mandarin Oriental Ritz", "img": "day-2.jpg"},
            {"n": 11, "label": "Días 11 · 12 · 13 · 14", "title": "Bilbao y Barcelona", "body": "Tren rápido a Bilbao y al día siguiente a Barcelona. Tour Gaudí privado, cena en el Born y mañana libre antes del vuelo internacional.", "meals": "Pensión completa", "lodging": "Mandarin Oriental Barcelona", "img": "day-6.jpg"},
        ],
        "lodges": [
            {"name": "Bairro Alto Hotel", "where": "Lisboa, Portugal", "img": "lodge-2.jpg"},
            {"name": "Hotel Alfonso XIII", "where": "Sevilla, España", "img": "lodge-1.jpg"},
            {"name": "Mandarin Oriental Ritz", "where": "Madrid, España", "img": "lodge-3.jpg"},
            {"name": "Mandarin Oriental Barcelona", "where": "Barcelona, España", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $4,800 USD", "title": "Norte de Portugal · Oporto y el Duero", "body": "Cuatro noches entre Oporto y las quintas del valle del Duero.", "img": "dest-europe.jpg"},
            {"meta": "+5 días · desde $5,400 USD", "title": "Mallorca", "body": "Cinco noches en una finca interior, perfecto para descansar tras el viaje.", "img": "intro-quote.jpg"},
            {"meta": "+3 días · desde $3,600 USD", "title": "Marruecos · Tánger y Fez", "body": "Tres noches del lado africano del estrecho.", "img": "dest-morocco.jpg"},
        ],
        "dates": [
            {"date": "12 abril 2026", "status": "Abierta", "status_class": "open", "price": "$16,800"},
            {"date": "10 mayo 2026", "status": "Pocas plazas", "status_class": "few", "price": "$17,400"},
            {"date": "14 junio 2026", "status": "Abierta", "status_class": "open", "price": "$18,200"},
            {"date": "13 septiembre 2026", "status": "Lista de espera", "status_class": "closed", "price": "$18,200"},
            {"date": "11 octubre 2026", "status": "Abierta", "status_class": "open", "price": "$16,800"},
        ],
        "similar": [
            {"href": "piamonte-tartufo.html", "img": "j-italy.jpg", "pill": "8 días", "title": "Piamonte"},
            {"href": "japon-clasico.html", "img": "j-japan.jpg", "pill": "9 días", "title": "Japón clásico"},
            {"href": "egipto-nilo.html", "img": "j-egypt.jpg", "pill": "10 días", "title": "Egipto y el Nilo"},
            {"href": "india-tigres.html", "img": "dest-india.jpg", "pill": "11 días", "title": "India y los tigres"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "angkor-sudeste-asiatico",
        "title": "Angkor Wat e iconos del Sudeste Asiático",
        "headline": "Sudeste Asiático 2026",
        "eyebrow": "Pequeña expedición · Asia",
        "meta_desc": "Quince días entre Vietnam, Camboya, Laos y Tailandia. Las cuatro caras de la península indochina.",
        "hero": "j-asia.jpg", "hero_alt": "Templo de Angkor al amanecer",
        "portrait": "dest-asia.jpg",
        "duration": "15 días", "nights": "14 noches", "max_guests": 16,
        "window": "Octubre–Marzo", "price_from": "$19,800 USD",
        "intro_h2": "Quince días, cuatro países, una sola península que cambia de idioma, de cocina y de templo cada doscientos kilómetros.",
        "intro_p1": "El Sudeste Asiático es el destino más denso del planeta — en cada valle hay un grupo étnico distinto, un templo distinto, una cocina distinta. Lo recorremos despacio: tres noches en Hanoi y Ha Long Bay, dos en Ho Chi Minh, tres en Siem Reap (con Angkor Wat al amanecer cuatro veces), tres en Luang Prabang y tres de cierre en Bangkok.",
        "intro_p2": "Acompañados por arqueólogos en Camboya, monjes en Laos y chefs en Vietnam — gente que abre puertas que ningún hotel boutique puede abrir.",
        "highlights": [
            {"t": "Angkor Wat al amanecer", "b": "Cuatro madrugadas con un arqueólogo del lugar; cada vez en un templo distinto."},
            {"t": "Ha Long Bay en junco privado", "b": "Dos noches a bordo de un junco tradicional de doce camarotes."},
            {"t": "Cena con monjes en Luang Prabang", "b": "Velada en un monasterio del siglo XIV con cocina laosiana auténtica."}
        ],
        "stops": ["Hanoi", "Ha Long Bay", "Hai Phong", "Ho Chi Minh", "Siem Reap", "Luang Prabang", "Bangkok"],
        "itin_intro": "Quince días en avance hacia el oeste. De los cafés de Hanoi a los mercados de Bangkok, atravesando dos civilizaciones que se conocen poco.",
        "days": [
            {"n": 1, "label": "Días 1 · 2", "title": "Hanoi", "body": "Bienvenida en Noi Bai. Dos noches en el casco antiguo. Café egg, paseo en cyclo y cena con cocina familiar en una casa de barrio.", "meals": "Pensión completa", "lodging": "Sofitel Legend Metropole", "img": "day-1.jpg"},
            {"n": 3, "label": "Días 3 · 4", "title": "Ha Long Bay en junco", "body": "Dos noches a bordo de un junco privado de doce camarotes. Kayak entre las formaciones kársticas, baños al amanecer y cena en cubierta.", "meals": "Pensión completa", "lodging": "Junco Au Co", "img": "day-2.jpg"},
            {"n": 5, "label": "Días 5 · 6", "title": "Ho Chi Minh y el Mekong", "body": "Vuelo doméstico al sur. Visita al Museo de la Guerra, paseo por el Mekong en lancha pequeña y cena en un templo Cao Đài.", "meals": "Pensión completa", "lodging": "The Reverie Saigon", "img": "day-3.jpg"},
            {"n": 7, "label": "Días 7 · 8 · 9", "title": "Camboya · Angkor Wat", "body": "Vuelo a Siem Reap. Tres noches con arqueólogos privados. Madrugadas en Angkor Wat, Ta Prohm, Bayón y Banteay Srei.", "meals": "Pensión completa", "lodging": "Amansara", "img": "day-4.jpg"},
            {"n": 10, "label": "Días 10 · 11 · 12", "title": "Laos · Luang Prabang", "body": "Vuelo al norte del Mekong. Tres noches en la antigua capital real. Ceremonia matinal de los monjes mendicantes y excursión a las cuevas Pak Ou.", "meals": "Pensión completa", "lodging": "Rosewood Luang Prabang", "img": "day-6.jpg"},
            {"n": 13, "label": "Días 13 · 14 · 15", "title": "Bangkok", "body": "Vuelo final a Tailandia. Tres noches en el Mandarin Oriental con clase de cocina, recorrido por canales en long-tail y cena de despedida.", "meals": "Pensión completa", "lodging": "Mandarin Oriental Bangkok", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Sofitel Legend Metropole", "where": "Hanoi, Vietnam", "img": "lodge-2.jpg"},
            {"name": "Junco Au Co", "where": "Ha Long Bay, Vietnam", "img": "lodge-3.jpg"},
            {"name": "Amansara", "where": "Siem Reap, Camboya", "img": "lodge-1.jpg"},
            {"name": "Rosewood Luang Prabang", "where": "Luang Prabang, Laos", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $5,200 USD", "title": "Playas de Phuket", "body": "Cuatro noches en una villa privada en el sur tailandés.", "img": "dest-caribbean.jpg"},
            {"meta": "+5 días · desde $6,800 USD", "title": "Birmania · Bagan y el lago Inle", "body": "Cinco noches en la tierra de los mil templos.", "img": "dest-asia.jpg"},
            {"meta": "+3 días · desde $3,400 USD", "title": "Chiang Mai", "body": "Tres días en el norte tailandés con santuario de elefantes ético.", "img": "way-honey.jpg"},
        ],
        "dates": [
            {"date": "11 octubre 2026", "status": "Abierta", "status_class": "open", "price": "$19,800"},
            {"date": "8 noviembre 2026", "status": "Pocas plazas", "status_class": "few", "price": "$20,400"},
            {"date": "10 enero 2027", "status": "Abierta", "status_class": "open", "price": "$20,800"},
            {"date": "14 febrero 2027", "status": "Lista de espera", "status_class": "closed", "price": "$20,800"},
            {"date": "14 marzo 2027", "status": "Abierta", "status_class": "open", "price": "$19,800"},
        ],
        "similar": [
            {"href": "japon-clasico.html", "img": "j-japan.jpg", "pill": "9 días", "title": "Japón clásico"},
            {"href": "india-tigres.html", "img": "dest-india.jpg", "pill": "11 días", "title": "India y los tigres"},
            {"href": "egipto-nilo.html", "img": "j-egypt.jpg", "pill": "10 días", "title": "Egipto y el Nilo"},
            {"href": "piamonte-tartufo.html", "img": "j-italy.jpg", "pill": "8 días", "title": "Piamonte"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "peru-machu-picchu",
        "title": "Perú · Machu Picchu y el Valle Sagrado",
        "headline": "Perú · Valle Sagrado 2026",
        "eyebrow": "Pequeña expedición · Sudamérica",
        "meta_desc": "Ocho días entre Lima, Cuzco, el Valle Sagrado y Machu Picchu. Tren panorámico y guía arqueológica privada.",
        "hero": "j-peru.jpg", "hero_alt": "Machu Picchu al amanecer",
        "portrait": "dest-southamerica.jpg",
        "duration": "8 días", "nights": "7 noches", "max_guests": 16,
        "window": "Abril–Noviembre", "price_from": "$10,200 USD",
        "intro_h2": "Ocho días en la cuna del imperio inca, leídos por un arqueólogo del Cuzco.",
        "intro_p1": "Perú es el destino que más fácil resulta de presentar y más difícil de leer. Hay capas de civilizaciones superpuestas en cada piedra, contradicciones en cada esquina del Cuzco, y un paisaje que cambia de altura mil veces al día.",
        "intro_p2": "Acompañados por un arqueólogo cusqueño con doctorado en estudios incaicos, recorremos Lima (con su escena culinaria), bajamos al Valle Sagrado para aclimatar a la altura y subimos a Machu Picchu en tren panorámico Hiram Bingham.",
        "highlights": [
            {"t": "Machu Picchu al amanecer", "b": "Acceso al sitio una hora antes de la apertura, con arqueólogo privado."},
            {"t": "Tren Hiram Bingham", "b": "Recorrido a través de la cordillera en el tren más bello del continente."},
            {"t": "Cena con chef estrella en Lima", "b": "Mesa privada en uno de los cincuenta mejores restaurantes del mundo."}
        ],
        "stops": ["Lima", "Cuzco", "Valle Sagrado", "Ollantaytambo", "Aguas Calientes", "Machu Picchu"],
        "itin_intro": "Ocho días de descenso lento por la cordillera. Aclimatamos en el Valle Sagrado antes de subir al santuario.",
        "days": [
            {"n": 1, "label": "Día 1 · Lima", "title": "Llegada", "body": "Bienvenida en Jorge Chávez. Traslado al hotel boutique en Barranco y cena de orientación con chef peruano.", "meals": "Cena", "lodging": "Hotel B Lima", "img": "day-1.jpg"},
            {"n": 2, "label": "Día 2", "title": "Lima cultural", "body": "Visita al Museo Larco, almuerzo en uno de los cincuenta mejores del mundo y tarde libre por Miraflores.", "meals": "Pensión completa", "lodging": "Hotel B Lima", "img": "day-2.jpg"},
            {"n": 3, "label": "Días 3 · 4", "title": "Valle Sagrado", "body": "Vuelo a Cuzco y traslado directo al Valle (menor altitud, ideal para aclimatar). Dos noches en Sol y Luna con cabalgata y visita a Pisac.", "meals": "Pensión completa", "lodging": "Sol y Luna", "img": "day-3.jpg"},
            {"n": 5, "label": "Días 5 · 6", "title": "Machu Picchu", "body": "Tren Hiram Bingham desde Ollantaytambo. Dos noches en Aguas Calientes. Visita al santuario al amanecer con arqueólogo privado y subida opcional a Huayna Picchu.", "meals": "Pensión completa", "lodging": "Sumaq Machu Picchu", "img": "day-4.jpg"},
            {"n": 7, "label": "Días 7 · 8", "title": "Cuzco", "body": "Regreso en tren a Cuzco. Dos noches en el Belmond Monasterio. Plaza de Armas, mercado de San Pedro y cena de despedida.", "meals": "Pensión completa", "lodging": "Belmond Monasterio", "img": "day-6.jpg"},
        ],
        "lodges": [
            {"name": "Hotel B Lima", "where": "Lima, Perú", "img": "lodge-2.jpg"},
            {"name": "Sol y Luna", "where": "Valle Sagrado, Perú", "img": "lodge-3.jpg"},
            {"name": "Sumaq Machu Picchu", "where": "Aguas Calientes, Perú", "img": "lodge-1.jpg"},
            {"name": "Belmond Monasterio", "where": "Cuzco, Perú", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $4,200 USD", "title": "Lago Titicaca", "body": "Cuatro noches entre Puno y las islas flotantes de los uros.", "img": "intro-quote.jpg"},
            {"meta": "+5 días · desde $6,800 USD", "title": "Amazonía peruana", "body": "Cinco noches en el Tambopata con biólogos locales.", "img": "dest-asia.jpg"},
            {"meta": "+3 días · desde $3,600 USD", "title": "Galápagos breve", "body": "Tres días en crucero pequeño por el archipiélago ecuatoriano.", "img": "dest-oceania.jpg"},
        ],
        "dates": [
            {"date": "6 abril 2026", "status": "Abierta", "status_class": "open", "price": "$10,200"},
            {"date": "11 mayo 2026", "status": "Abierta", "status_class": "open", "price": "$10,800"},
            {"date": "8 junio 2026", "status": "Pocas plazas", "status_class": "few", "price": "$11,400"},
            {"date": "14 septiembre 2026", "status": "Abierta", "status_class": "open", "price": "$11,400"},
            {"date": "12 octubre 2026", "status": "Abierta", "status_class": "open", "price": "$10,800"},
        ],
        "similar": [
            {"href": "amazonas-pantanal.html", "img": "dest-southamerica.jpg", "pill": "12 días", "title": "Amazonas y Pantanal"},
            {"href": "patagonia-circuito.html", "img": "dest-patagonia.jpg", "pill": "10 días", "title": "Patagonia"},
            {"href": "alaska-familiar.html", "img": "j-alaska.jpg", "pill": "8 días", "title": "Alaska familiar"},
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "alaska-familiar",
        "title": "Alaska · Aventura familiar",
        "headline": "Alaska familiar 2026",
        "eyebrow": "Pequeña expedición · Norteamérica",
        "meta_desc": "Ocho días entre Anchorage, Kenai Fjords y Denali. Pensado para familias multigeneracionales.",
        "hero": "j-alaska.jpg", "hero_alt": "Fiordos de Alaska al atardecer",
        "portrait": "dest-arctic.jpg",
        "duration": "8 días", "nights": "7 noches", "max_guests": 24,
        "window": "Junio–Septiembre", "price_from": "$12,100 USD",
        "intro_h2": "Ocho días pensados para que tres generaciones lo recuerden igual.",
        "intro_p1": "Alaska es el destino familiar por excelencia: paisaje épico, fauna activa todo el día y actividades para todas las edades sin esfuerzo. Lo recorremos con un naturalista de planta del Parque Nacional Denali, navegando los Kenai Fjords en pequeño grupo y avistando osos pardos en territorio protegido.",
        "intro_p2": "Combinamos cabañas de pesca con un lodge histórico dentro del parque. Caminamos suave, vamos en kayak, en hidroavión y en tren clásico. Hay tiempo libre cada tarde para que los chicos respiren y los grandes descansen.",
        "highlights": [
            {"t": "Kenai Fjords en pequeño grupo", "b": "Catamarán de cuarenta plazas (no de doscientas) con un biólogo a bordo."},
            {"t": "Avistamiento de osos pardos", "b": "Vuelo en hidroavión a Katmai para ver osos pescando salmón en cataratas."},
            {"t": "Tren del Alaska Railroad", "b": "Cinco horas en el GoldStar de cúpula panorámica entre Anchorage y Denali."}
        ],
        "stops": ["Anchorage", "Seward", "Kenai Fjords", "Talkeetna", "Parque Nacional Denali"],
        "itin_intro": "Ocho días con tres bases. Combinamos costa, río y tundra alpina.",
        "days": [
            {"n": 1, "label": "Día 1 · Anchorage", "title": "Llegada", "body": "Bienvenida en aeropuerto y traslado al Captain Cook. Cena de orientación con guía Alaska-based.", "meals": "Cena", "lodging": "Hotel Captain Cook", "img": "day-1.jpg"},
            {"n": 2, "label": "Días 2 · 3", "title": "Seward y Kenai Fjords", "body": "Traslado escénico por la carretera Seward Highway. Dos noches en Seward. Navegación de día completo por los Kenai Fjords en pequeño grupo.", "meals": "Pensión completa", "lodging": "Seward Windsong Lodge", "img": "day-2.jpg"},
            {"n": 4, "label": "Día 4", "title": "Vuelo a Katmai", "body": "Hidroavión a Brooks Falls. Día completo viendo osos pescando salmón al lado del agua, con guarda armado.", "meals": "Pensión completa", "lodging": "Brooks Lodge", "img": "day-4.jpg"},
            {"n": 5, "label": "Días 5 · 6 · 7", "title": "Denali", "body": "Tren panorámico a Talkeetna y traslado al parque. Tres noches en Camp Denali. Recorridos en bus oficial, caminatas guiadas y noche en cabañas con vista al monte.", "meals": "Pensión completa", "lodging": "Camp Denali", "img": "day-6.jpg"},
            {"n": 8, "label": "Día 8 · Salida", "title": "Regreso", "body": "Vuelo desde Fairbanks o regreso por tren a Anchorage para conexión internacional.", "meals": "Desayuno", "lodging": "—", "img": "day-8.jpg"},
        ],
        "lodges": [
            {"name": "Hotel Captain Cook", "where": "Anchorage, Alaska", "img": "lodge-2.jpg"},
            {"name": "Seward Windsong Lodge", "where": "Seward, Alaska", "img": "lodge-3.jpg"},
            {"name": "Brooks Lodge", "where": "Katmai, Alaska", "img": "lodge-1.jpg"},
            {"name": "Camp Denali", "where": "Parque Nacional Denali, Alaska", "img": "lodge-4.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $4,800 USD", "title": "Ferry Inside Passage", "body": "Cuatro días en ferry por el sudeste de Alaska.", "img": "dest-arctic.jpg"},
            {"meta": "+3 días · desde $3,200 USD", "title": "Vancouver y la isla", "body": "Tres noches en Canadá con avistamiento de orcas.", "img": "dest-oceania.jpg"},
            {"meta": "+5 días · desde $5,800 USD", "title": "Yukón canadiense", "body": "Cinco días al norte de Whitehorse con aurora boreal.", "img": "dest-arctic.jpg"},
        ],
        "dates": [
            {"date": "20 junio 2026", "status": "Abierta", "status_class": "open", "price": "$12,100"},
            {"date": "11 julio 2026", "status": "Pocas plazas", "status_class": "few", "price": "$13,200"},
            {"date": "1 agosto 2026", "status": "Lista de espera", "status_class": "closed", "price": "$13,200"},
            {"date": "22 agosto 2026", "status": "Abierta", "status_class": "open", "price": "$12,800"},
            {"date": "12 septiembre 2026", "status": "Abierta", "status_class": "open", "price": "$11,800"},
        ],
        "similar": [
            {"href": "patagonia-circuito.html", "img": "dest-patagonia.jpg", "pill": "10 días", "title": "Patagonia"},
            {"href": "peru-machu-picchu.html", "img": "j-peru.jpg", "pill": "8 días", "title": "Perú y Machu Picchu"},
            {"href": "amazonas-pantanal.html", "img": "dest-southamerica.jpg", "pill": "12 días", "title": "Amazonas y Pantanal"},
            {"href": "japon-clasico.html", "img": "j-japan.jpg", "pill": "9 días", "title": "Japón clásico"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
    {
        "slug": "india-tigres",
        "title": "India · Triángulo de oro y tigres",
        "headline": "India 2026",
        "eyebrow": "Pequeña expedición · Asia",
        "meta_desc": "Once días entre Delhi, Agra, Jaipur y los tigres de Ranthambore.",
        "hero": "dest-india.jpg", "hero_alt": "Templo en India al amanecer",
        "portrait": "way-honey.jpg",
        "duration": "11 días", "nights": "10 noches", "max_guests": 14,
        "window": "Octubre–Marzo", "price_from": "$13,200 USD",
        "intro_h2": "Once días en el corazón mughal, con safaris en Ranthambore en busca del tigre real de Bengala.",
        "intro_p1": "La India es uno de esos pocos países donde la primera visita transforma. El triángulo de oro — Delhi, Agra, Jaipur — concentra mil años de arquitectura mughal en doscientos kilómetros. Lo abordamos con historiadores locales que separan capa por capa.",
        "intro_p2": "Combinamos la cultura con dos días en Ranthambore para safari. La reserva tiene la población de tigre más alta de la India y los guías llevan dos décadas siguiendo familias específicas.",
        "highlights": [
            {"t": "Taj Mahal al amanecer", "b": "Acceso al monumento a la primera hora, antes que abra al público general."},
            {"t": "Safaris en Ranthambore", "b": "Cuatro salidas con guías que rastrean tigres por nombre."},
            {"t": "Audiencia con un maestro de la cocina rajputa", "b": "Velada privada con un chef de Jaipur que cocina recetas de la familia real."}
        ],
        "stops": ["Delhi", "Agra", "Ranthambore", "Jaipur", "Udaipur"],
        "itin_intro": "Once días en el cuadrante del norte, con tres bases y dos vuelos cortos.",
        "days": [
            {"n": 1, "label": "Días 1 · 2", "title": "Delhi", "body": "Bienvenida en Indira Gandhi. Dos noches en el Imperial. Old y New Delhi en cyclo, mezquita Jama Masjid y mercado de especias.", "meals": "Pensión completa", "lodging": "The Imperial", "img": "day-1.jpg"},
            {"n": 3, "label": "Días 3 · 4", "title": "Agra y el Taj", "body": "Vuelo doméstico. Dos noches en el Oberoi Amarvilas con vista al Taj. Acceso al monumento al amanecer y visita al fuerte rojo.", "meals": "Pensión completa", "lodging": "Oberoi Amarvilas", "img": "day-2.jpg"},
            {"n": 5, "label": "Días 5 · 6", "title": "Ranthambore", "body": "Traslado por tren expreso a la reserva. Dos noches en Aman-i-Khás (campamento de lujo). Cuatro safaris en jeep abierto en busca del tigre.", "meals": "Pensión completa", "lodging": "Aman-i-Khás", "img": "day-4.jpg"},
            {"n": 7, "label": "Días 7 · 8 · 9", "title": "Jaipur", "body": "Tren a la ciudad rosa. Tres noches en Rambagh Palace. Fuerte Amber a la mañana, mercado de Johari Bazaar y cena con el chef de la familia real.", "meals": "Pensión completa", "lodging": "Taj Rambagh Palace", "img": "day-3.jpg"},
            {"n": 10, "label": "Días 10 · 11", "title": "Udaipur", "body": "Vuelo a la ciudad del lago. Dos noches en el Taj Lake Palace, dentro del lago Pichola. Templo Jagdish, paseo en bote y vuelo internacional desde Delhi.", "meals": "Pensión completa", "lodging": "Taj Lake Palace", "img": "day-6.jpg"},
        ],
        "lodges": [
            {"name": "The Imperial", "where": "Delhi, India", "img": "lodge-2.jpg"},
            {"name": "Oberoi Amarvilas", "where": "Agra, India", "img": "lodge-3.jpg"},
            {"name": "Aman-i-Khás", "where": "Ranthambore, India", "img": "lodge-4.jpg"},
            {"name": "Taj Lake Palace", "where": "Udaipur, India", "img": "lodge-1.jpg"},
        ],
        "extensions": [
            {"meta": "+4 días · desde $4,800 USD", "title": "Varanasi y el Ganges", "body": "Cuatro noches en la ciudad sagrada hindú con ceremonia del río.", "img": "dest-india.jpg"},
            {"meta": "+5 días · desde $6,200 USD", "title": "Kerala y los backwaters", "body": "Cinco noches en la costa de Malabar con houseboat tradicional.", "img": "dest-asia.jpg"},
            {"meta": "+3 días · desde $3,400 USD", "title": "Bombay", "body": "Tres días en la capital comercial india.", "img": "dest-india.jpg"},
        ],
        "dates": [
            {"date": "11 octubre 2026", "status": "Abierta", "status_class": "open", "price": "$13,200"},
            {"date": "8 noviembre 2026", "status": "Pocas plazas", "status_class": "few", "price": "$13,800"},
            {"date": "10 enero 2027", "status": "Abierta", "status_class": "open", "price": "$14,400"},
            {"date": "21 febrero 2027", "status": "Lista de espera", "status_class": "closed", "price": "$14,400"},
            {"date": "14 marzo 2027", "status": "Abierta", "status_class": "open", "price": "$13,200"},
        ],
        "similar": [
            {"href": "angkor-sudeste-asiatico.html", "img": "j-asia.jpg", "pill": "15 días", "title": "Angkor y Sudeste Asiático"},
            {"href": "japon-clasico.html", "img": "j-japan.jpg", "pill": "9 días", "title": "Japón clásico"},
            {"href": "egipto-nilo.html", "img": "j-egypt.jpg", "pill": "10 días", "title": "Egipto y el Nilo"},
            {"href": "gran-migracion.html", "img": "j-migration.jpg", "pill": "14 días", "title": "La Gran Migración"},
        ],
        "includes": DEFAULT_INCLUDES,
    },
]

REGIONS = [
    {
        "slug": "africa",
        "name": "África",
        "meta_desc": "Safaris, deltas, gorilas y desierto. Doce países africanos con guías propios.",
        "hero": "hero-savannah.jpg",
        "nav_label": "Ver países",
        "cta": "Ver todos los países",
        "lede": "Sabana al amanecer. Aguas del Okavango filtrándose por la arena del Kalahari. Bosque de niebla en Ruanda.",
        "body": "África no es un destino — son diez. La cuna del safari moderno y un continente donde la conservación se hace cara a cara con quienes viven en cada terreno. Trabajamos con guías masai, bayei, samburu y hadza desde hace cuatro décadas. Cada uno cuenta su tierra como sólo se cuenta cuando se nació en ella.",
        "countries": [
            {"name": "Kenia", "blurb": "Tierras altas, gran migración, conservatorios masais. El safari clásico y la cultura viva.", "img": "dest-kenya.jpg"},
            {"name": "Tanzania", "blurb": "El Serengeti, Ngorongoro y Zanzíbar. La esencia del safari acompañada de costa.", "img": "next-up.jpg"},
            {"name": "Botswana", "blurb": "Delta del Okavango. El mejor secreto del África austral, lujo discreto.", "img": "j-botswana.jpg"},
            {"name": "Sudáfrica", "blurb": "De Ciudad del Cabo a los viñedos de Stellenbosch, pasando por Kruger.", "img": "dest-spain.jpg"},
            {"name": "Ruanda", "blurb": "Gorilas de montaña en el Parque Nacional de Volcanes. Una experiencia única.", "img": "dest-asia.jpg"},
            {"name": "Namibia", "blurb": "Sossusvlei, los esqueletos de la costa atlántica y el desierto más antiguo del mundo.", "img": "dest-mena.jpg"},
        ],
    },
    {
        "slug": "asia",
        "name": "Asia",
        "meta_desc": "De Japón a Bután, de la India al Sudeste Asiático. La diversidad cultural más densa del planeta.",
        "hero": "dest-japan.jpg",
        "nav_label": "Ver países",
        "cta": "Ver todos los países",
        "lede": "Templos al amanecer, mercados al alba, ríos que cruzan tres países sin que nadie los corte.",
        "body": "Asia es un continente que cambia cada quinientos kilómetros. Lo recorremos en pequeños grupos con guías locales que conocen no sólo el lugar sino el mejor momento para cada lugar. Trabajamos con artesanos, maestros del té, monjes, naturalistas y chefs que sólo abren sus puertas a quienes vienen con tiempo.",
        "countries": [
            {"name": "Japón", "blurb": "Tokio, Kioto, Hakone. Templos al amanecer y ryokans con onsen.", "img": "dest-japan.jpg"},
            {"name": "India", "blurb": "El triángulo de oro, los tigres de Ranthambore y los palacios de Rajastán.", "img": "dest-india.jpg"},
            {"name": "Bután", "blurb": "El reino donde se mide la felicidad antes que el PIB.", "img": "dest-asia.jpg"},
            {"name": "Vietnam", "blurb": "De Hanoi a Hoi An, pasando por Ha Long Bay.", "img": "j-asia.jpg"},
            {"name": "Camboya", "blurb": "Angkor Wat con egiptólogos del lugar y aldeas flotantes.", "img": "j-asia.jpg"},
            {"name": "Tailandia", "blurb": "Bangkok, Chiang Mai y las islas del sur.", "img": "way-private.jpg"},
        ],
    },
    {
        "slug": "sudamerica",
        "name": "Sudamérica",
        "meta_desc": "Patagonia, Amazonas, Galápagos, Machu Picchu. Doce países con doce escenarios completamente distintos.",
        "hero": "dest-patagonia.jpg",
        "nav_label": "Ver países",
        "cta": "Ver todos los países",
        "lede": "El continente más diverso por kilómetro cuadrado. De la estepa a la selva, del altiplano al hielo.",
        "body": "Como sudamericanos, conocemos este continente de adentro. Hemos viajado en colectivo, en barco, en avioneta, en mula. Esa familiaridad se traduce en itinerarios que no se ven en ningún otro lado — la fiesta a la que sólo los locales van, la cabaña en el bosque que no sale en buscadores, el restaurante con tres meses de espera al que entramos por amistad.",
        "countries": [
            {"name": "Argentina", "blurb": "Patagonia, Buenos Aires, Mendoza, Iguazú. Lo profundo y lo cosmopolita.", "img": "dest-patagonia.jpg"},
            {"name": "Brasil", "blurb": "Río, Pantanal, Amazonas y la costa noreste. El país-continente.", "img": "dest-southamerica.jpg"},
            {"name": "Perú", "blurb": "Machu Picchu, el Valle Sagrado y la Amazonía peruana.", "img": "j-peru.jpg"},
            {"name": "Chile", "blurb": "Patagonia, Atacama, la costa central y la isla de Pascua.", "img": "dest-patagonia.jpg"},
            {"name": "Ecuador", "blurb": "Galápagos en buque pequeño + los Andes y la selva.", "img": "dest-asia.jpg"},
            {"name": "Bolivia", "blurb": "Uyuni, la altura del altiplano y el lago Titicaca.", "img": "intro-quote.jpg"},
        ],
    },
    {
        "slug": "polos",
        "name": "Antártida y polos",
        "meta_desc": "Antártida desde Ushuaia, el Ártico noruego, Groenlandia. Travesías en buques de expedición.",
        "hero": "dest-arctic.jpg",
        "nav_label": "Ver itinerarios",
        "cta": "Ver todos los itinerarios",
        "lede": "El silencio cambia de color cuando pisás el continente blanco.",
        "body": "Los polos son los destinos más exigentes y los más generosos. Trabajamos sólo con buques de expedición de menos de cien pasajeros, con biólogos, fotógrafos y guías polares de experiencia probada. La logística la pensamos nosotros para que vos sólo te dediques a mirar.",
        "countries": [
            {"name": "Antártida desde Ushuaia", "blurb": "Diez a doce días de cruce del Drake, desembarcos diarios en zodiac.", "img": "dest-arctic.jpg"},
            {"name": "Antártida en jet", "blurb": "Cuatro días con vuelo directo a Isla Rey Jorge, ideal para quienes no toleran navegación.", "img": "dest-arctic.jpg"},
            {"name": "Islandia y Groenlandia", "blurb": "Dos semanas circumnavegando Islandia y desembarcando en la costa este de Groenlandia.", "img": "dest-arctic.jpg"},
            {"name": "Svalbard y el Ártico", "blurb": "Diez días en el archipiélago de Spitsbergen, en busca de oso polar y morsa.", "img": "dest-arctic.jpg"},
            {"name": "Patagonia chilena", "blurb": "Glaciares del Pacífico chileno en buque pequeño.", "img": "dest-patagonia.jpg"},
            {"name": "Noruega y los fiordos", "blurb": "Aurora boreal, navegación entre fiordos y los Lofoten.", "img": "dest-arctic.jpg"},
        ],
    },
    {
        "slug": "norteamerica",
        "name": "Norteamérica",
        "meta_desc": "De Alaska al sudoeste americano. Parques nacionales, costas y ciudades.",
        "hero": "dest-northamerica.jpg",
        "nav_label": "Ver países",
        "cta": "Ver todos los países",
        "lede": "Tres países, tres formas distintas de medir el horizonte.",
        "body": "Norteamérica es el continente de los parques nacionales y de los caminos largos. Acompañamos a familias, parejas y viajeros en solitario que buscan tanto la naturaleza salvaje como la cultura urbana. Trabajamos con guías locales en cada estado y cada provincia.",
        "countries": [
            {"name": "Estados Unidos · Oeste", "blurb": "Parques nacionales del sudoeste — Zion, Bryce, Grand Canyon.", "img": "dest-northamerica.jpg"},
            {"name": "Alaska", "blurb": "Denali, Kenai Fjords y el ferry costero del sudeste.", "img": "j-alaska.jpg"},
            {"name": "Canadá · Banff", "blurb": "Rocosas canadienses, lago Louise, oso pardo.", "img": "dest-arctic.jpg"},
            {"name": "Estados Unidos · Este", "blurb": "Costa de Maine, Nueva York y Washington.", "img": "dest-europe.jpg"},
            {"name": "México", "blurb": "Ciudad de México, Oaxaca, Yucatán y la Riviera Maya.", "img": "hero-savannah.jpg"},
            {"name": "Quebec y Montreal", "blurb": "La parte francófona de Canadá, con cocina y arquitectura propias.", "img": "dest-europe.jpg"},
        ],
    },
    {
        "slug": "oceania",
        "name": "Oceanía",
        "meta_desc": "Australia, Nueva Zelanda, Polinesia. Naturaleza extrema y costas sin igual.",
        "hero": "dest-oceania.jpg",
        "nav_label": "Ver países",
        "cta": "Ver todos los países",
        "lede": "El último gran espacio salvaje del planeta y las islas más remotas del Pacífico.",
        "body": "Oceanía es el destino para quienes valoran el tiempo de vuelo. Trabajamos con guías locales que conocen tanto los Outback australianos como los volcanes de Nueva Zelanda y las lagunas polinésicas. Itinerarios siempre por encima de los catorce días, porque distancia + jet lag exige tiempo.",
        "countries": [
            {"name": "Nueva Zelanda", "blurb": "Las dos islas en doce días, con helicóptero a Milford Sound.", "img": "dest-oceania.jpg"},
            {"name": "Australia", "blurb": "Sydney, Outback, Gran Barrera de Coral.", "img": "dest-oceania.jpg"},
            {"name": "Polinesia francesa", "blurb": "Tahití, Moorea, Bora Bora y atolones remotos.", "img": "dest-caribbean.jpg"},
            {"name": "Fiyi", "blurb": "Islas privadas, snorkel y cultura del kava.", "img": "dest-caribbean.jpg"},
            {"name": "Tasmania", "blurb": "Caminata por el Overland Track y el East Coast.", "img": "dest-oceania.jpg"},
            {"name": "Cook Islands", "blurb": "Pequeño archipiélago perfecto para escapar del mundo.", "img": "dest-caribbean.jpg"},
        ],
    },
    {
        "slug": "caribe",
        "name": "Caribe",
        "meta_desc": "Islas privadas, atolones y costa atlántica. Lujo discreto y mar turquesa.",
        "hero": "dest-caribbean.jpg",
        "nav_label": "Ver islas",
        "cta": "Ver todas las islas",
        "lede": "Mar turquesa, islas privadas, ron añejo y arena rosa.",
        "body": "El Caribe es nuestro destino más popular para combinar con safaris africanos o expediciones polares — el contraste funciona. Trabajamos sólo con hoteles boutique, villas privadas e islas pequeñas. Nunca con resorts masivos.",
        "countries": [
            {"name": "San Bartolomé", "blurb": "Punta de la sofisticación caribeña, perfecta para parejas.", "img": "dest-caribbean.jpg"},
            {"name": "Mustique", "blurb": "Isla privada con sólo cien villas. Discreción absoluta.", "img": "dest-caribbean.jpg"},
            {"name": "Cuba", "blurb": "La Habana, Trinidad, Viñales. Cultura viva y música.", "img": "intro-quote.jpg"},
            {"name": "República Dominicana", "blurb": "Costa norte y la sierra interior.", "img": "dest-caribbean.jpg"},
            {"name": "Bahamas", "blurb": "Islas privadas y aguas cristalinas a una hora de Miami.", "img": "dest-caribbean.jpg"},
            {"name": "Granada y las Granadinas", "blurb": "Las islas menos turísticas, ideales para charters de vela.", "img": "dest-caribbean.jpg"},
        ],
    },
    {
        "slug": "oriente-medio",
        "name": "Oriente Medio y Norte de África",
        "meta_desc": "Marruecos, Jordania, Egipto, Omán, Turquía. Cultura milenaria y desiertos imposibles.",
        "hero": "dest-morocco.jpg",
        "nav_label": "Ver países",
        "cta": "Ver todos los países",
        "lede": "Mezquitas al amanecer, dunas que cambian de color cada hora, hammams centenarios.",
        "body": "Esta región concentra algunas de las civilizaciones más antiguas y vivas del planeta. Trabajamos con guías que combinan formación académica con familiaridad cultural — historiadores que también son nativos del lugar. La logística aquí es delicada y la calidad del guía cambia todo.",
        "countries": [
            {"name": "Marruecos", "blurb": "Fez, Marrakech, Sahara. Riads tradicionales y arquitectura imperial.", "img": "dest-morocco.jpg"},
            {"name": "Jordania", "blurb": "Petra, Wadi Rum, Mar Muerto.", "img": "dest-mena.jpg"},
            {"name": "Egipto", "blurb": "Las pirámides, el Nilo en dahabiya, Abu Simbel.", "img": "j-egypt.jpg"},
            {"name": "Omán", "blurb": "Mascate, los wadis del desierto y la cultura beduina.", "img": "dest-mena.jpg"},
            {"name": "Turquía", "blurb": "Estambul, Capadocia, Éfeso y la costa egea.", "img": "dest-mena.jpg"},
            {"name": "Israel y los territorios", "blurb": "Jerusalén, Tel Aviv y el desierto del Néguev.", "img": "dest-mena.jpg"},
        ],
    },
]

# =============================================================================
# RUN
# =============================================================================
def main():
    for j in JOURNEYS:
        path = os.path.join(REPO, j['slug'] + ".html")
        with open(path, "w") as f:
            f.write(build_journey(j))
        print(f"  ✓ {j['slug']}.html")

    for r in REGIONS:
        path = os.path.join(REPO, r['slug'] + ".html")
        with open(path, "w") as f:
            f.write(build_region(r))
        print(f"  ✓ {r['slug']}.html")

if __name__ == "__main__":
    main()
