# Blisniuk & Amanov

Sitio estático en HTML/CSS/JS vanilla. Tres páginas:

- `index.html` — homepage
- `destinations.html` — mosaico de regiones
- `journeys.html` — listado de viajes con filtros

## Cómo verlo localmente

```bash
python3 -m http.server 8000
# o
npx serve .
```

Y abrí `http://localhost:8000` en el navegador. También funciona abriendo `index.html` directamente con `file://`, pero algunas cosas (anchors, fonts) se ven mejor servidas.

## Capturas de pantalla

Las capturas están en [`_compare/`](./_compare/). Se regeneran con:

```bash
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node tools/screenshot.js
```

(Requiere Chromium de Playwright instalado en `/opt/pw-browsers`.)

## Imágenes

Las imágenes en `assets/img/` son placeholders de paisaje generados proceduralmente con Pillow. Para regenerar:

```bash
python3 tools/gen_images.py
```

## Stack

- Tipografías: Cormorant Garamond (titulares) + Manrope (UI/cuerpo) — Google Fonts
- Paleta: cobre `#AA5432`, crema `#F5F2EB`, tinta `#111111`
- Sin dependencias JS (solo `script.js` propio)
