# Inventario de imágenes — Blisniuk & Amanov

Cada slot del sitio que necesita una foto, listado con:
- **Nombre del archivo** (así tiene que llamarse cuando lo subas)
- **Ruta exacta** donde va dentro del repo
- **Dimensión recomendada** (siempre subí la versión más grande que tengas; el CSS la reduce)
- **Proporción de aspecto** (importante respetarla para que no se deforme)
- **Qué representa** (para que sepas qué buscar / tomar)
- **Sección/página** donde aparece

> 📍 **Cómo identificar cada placeholder hoy**: en el repo, los archivos están en `assets/img/` con un nombre descriptivo. Por ejemplo `dest-japan.jpg` es el placeholder de la card de Japón. Para reemplazarlo, simplemente subí una imagen JPG con el mismo nombre y misma ruta y reemplaza la versión actual.
>
> 🎨 **Formato preferido**: JPG con compresión calidad 80 (Lightroom: "Calidad 80"). Si tenés versión .webp lista, mejor todavía — pesa 30% menos.
>
> 📏 **Tip de proporción**: si la foto original es 4000×3000 (4:3) y el slot es 4:5 (vertical), recortala antes de subir, o yo defino un `object-fit: cover` que la centra y recorta. Pero si me pasás la foto ya en proporción, queda mejor compuesta.

---

## 1. Homepage (`index.html`)

### Hero spotlight (rotativo, 3 imágenes a sangre)
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `hero-savannah.jpg` | `assets/img/` | 2400×1500 | 16:10 | Suite, lodge o paisaje **al atardecer** (cálido). Foto editorial, sensación de "primer momento del viaje". |
| `hero-alpine.jpg` | `assets/img/` | 2400×1500 | 16:10 | Salón, sala o interior con vista a **paisaje frío** (alpes, lago, montaña). |
| `hero-coast.jpg` | `assets/img/` | 2400×1500 | 16:10 | Habitación, terraza o paisaje **mar / costa** (tono azul). |

### Tarjeta de premio (vertical, esquina del hero)
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `award-thumb.jpg` | `assets/img/` | 400×500 | 4:5 | Foto vertical, podría ser portada de revista que destacó la casa o foto editorial premiada. |

### Strip "A continuación"
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `next-up.jpg` | `assets/img/` | 400×280 | 10:7 | Foto chica de teaser de la próxima novedad (ej. vida salvaje, nuevo destino). |

### Cards "¿A dónde te llevamos?" — destinos destacados
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `dest-japan.jpg` | `assets/img/` | 1200×1500 | 4:5 | Foto representativa de Japón (templo, calle de Kioto, geisha, monte Fuji…). |
| `dest-patagonia.jpg` | `assets/img/` | 1200×1500 | 4:5 | Patagonia: Torres del Paine, Perito Moreno, fauna estepa. |
| `dest-morocco.jpg` | `assets/img/` | 1200×1500 | 4:5 | Marruecos: riad, medina, dunas del desierto. |

### Cards "¿Qué tipo de viaje?" — estilos
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `way-honey.jpg` | `assets/img/` | 1000×1250 | 4:5 | Refugio remoto. Lodge solitario en naturaleza. |
| `way-family.jpg` | `assets/img/` | 1000×1250 | 4:5 | Familia compartiendo experiencia (safari, naturaleza). |
| `dest-arctic.jpg` *(reusada)* | `assets/img/` | 1000×1250 | 4:5 | Viajar solo. Paisaje contemplativo, una sola figura. |

### Cards "Stay with us" — casas propias
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `stay-sanctuari.jpg` | `assets/img/` | 1400×1750 | 4:5 | Suite o piscina infinita al atardecer. Lujo discreto. |
| `stay-villa.jpg` | `assets/img/` | 1400×1750 | 4:5 | Villa privada con vista a la costa, vista aérea o exterior. |

### Cards "¿Cómo prefieres viajar?" — 5 modalidades
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `way-private.jpg` | `assets/img/` | 1200×1500 | 4:5 | Cena privada al aire libre / experiencia exclusiva. |
| `way-group.jpg` | `assets/img/` | 1200×1500 | 4:5 | Pequeño grupo en exterior, con guía. |
| `way-safari.jpg` | `assets/img/` | 1200×1500 | 4:5 | Safari: jeep abierto y fauna africana. |
| `way-cruise.jpg` | `assets/img/` | 1600×900 | 16:9 | Crucero pequeño, río o mar, al atardecer. |
| `way-jet.jpg` | `assets/img/` | 1600×900 | 16:9 | Jet privado sobre nubes o pista. |

### Cita band a sangre
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `intro-quote.jpg` | `assets/img/` | 2400×1200 | 2:1 | Paisaje épico para fondo de cita (costa, montaña, sabana al atardecer). Debe tener zonas oscuras donde superponer texto blanco. |

### Filantropía split
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `fund-people.jpg` | `assets/img/` | 1400×1050 | 4:3 | Foto humana: niños, comunidad local, proyecto educativo. Sonrisa o naturalidad. |

### Banner "¿Por qué viajar con…?"
| Archivo | Ruta | Dimensión | Ratio | Qué |
|---|---|---|---|---|
| `why-banner.jpg` | `assets/img/` | 2400×900 | 8:3 | Foto panorámica con espacio negativo en izquierda (texto sobre overlay oscuro). Dunas, sabana, costa funcionan bien. |

---

## 2. Destinos (`destinations.html`)

Mosaico de regiones (10 cards mixtas).

| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `next-up.jpg` *(reuse)* | 1200×1200 | 1:1 | África (cebra, sabana). |
| `dest-arctic.jpg` | 1200×2400 | 1:2 (vertical) | Antártida y el Ártico. Iceberg, pingüinos. |
| `dest-japan.jpg` | 1200×1200 | 1:1 | Asia (puede ser Japón, Bali, Vietnam). |
| `dest-oceania.jpg` | 1200×2400 | 1:2 (vertical) | Oceanía. Ola, costa Australia, Bora Bora. |
| `dest-italy.jpg` | 1200×2400 | 1:2 (vertical) | Europa (Amalfi, Toscana, Provenza). |
| `dest-southamerica.jpg` | 1200×1200 | 1:1 | Sudamérica (Lago Titicaca, Galápagos, Iguazú). |
| `hero-savannah.jpg` *(reuse)* | 1200×1200 | 1:1 | Centroamérica (jungla maya, Costa Rica). |
| `dest-northamerica.jpg` | 1200×1200 | 1:1 | Norteamérica (Monument Valley, Banff). |
| `intro-quote.jpg` *(reuse)* | 1200×1200 | 1:1 | Caribe. Aguas turquesa, isla privada. |
| `dest-morocco.jpg` *(reuse)* | 1200×1200 | 1:1 | Oriente Próximo y Norte de África. Petra, Cairo, dunas. |

---

## 3. Europa (`europe.html`)

### Hero de región (image left a sangre + texto right)
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `dest-italy.jpg` *(reuse)* | 1600×1200 | 4:3 | Hero panorámico de Europa: costa amalfitana, viñedos, ciudad antigua. |

### Carrusel "Mejores formas de viajar" (3 cards chicas)
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `dest-europe.jpg` | 600×450 | 4:3 | Budapest / Viena / Praga (capital centroeuropea). |
| `dest-italy.jpg` *(reuse)* | 600×450 | 4:3 | Sur de Italia (Sicilia, Apulia). |
| `intro-quote.jpg` *(reuse)* | 600×450 | 4:3 | Costa dálmata (Croacia). |

### Grid de países (10 países, tarjetas cuadradas)
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `dest-italy.jpg` *(reuse)* | 1000×1000 | 1:1 | Italia. |
| `dest-europe.jpg` *(reuse)* | 1000×1000 | 1:1 | Francia. |
| `dest-northamerica.jpg` *(reuse)* | 1000×1000 | 1:1 | Reino Unido. Castillos, costas. |
| `intro-quote.jpg` *(reuse)* | 1000×1000 | 1:1 | Grecia. Islas blancas y azules. |
| `dest-spain.jpg` | 1000×1000 | 1:1 | Portugal (Lisboa, Oporto). |
| `dest-spain.jpg` *(reuse)* | 1000×1000 | 1:1 | España (Sevilla, Barcelona). |
| `dest-arctic.jpg` *(reuse)* | 1000×1000 | 1:1 | Noruega. Fiordos, aurora. |
| `dest-europe.jpg` *(reuse)* | 1000×1000 | 1:1 | Escocia. Highlands. |
| `dest-mena.jpg` | 1000×1000 | 1:1 | Turquía. Estambul, Capadocia. |
| `dest-arctic.jpg` *(reuse)* | 1000×1000 | 1:1 | Islandia. |

---

## 4. Detalle de viaje — La Gran Migración (`gran-migracion.html`)

Estructura general que **se va a repetir** en los 11 otros detalles cuando me pases la lista. Lo más importante.

### Hero del viaje
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `hero-savannah.jpg` *(reuse, o ideal una específica)* | 2400×1300 | 16:9 | Foto a sangre del destino al amanecer/atardecer. **Espacio negativo a la izquierda** porque ahí va el título. |

### Retrato vertical de fauna
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `wildlife-portrait.jpg` | 900×1200 | 3:4 | Foto vertical de animal o paisaje cercano. Guepardo, león, elefante. Foto editorial. |

### Mapa de ruta
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `route-map.jpg` | 1200×900 | 4:3 | Idealmente un mapa estilizado de la ruta. Si no, ilustración o foto de mapa antiguo. Si me pasás un track GPX o coordenadas, te genero el mapa con SVG. |

### Día por día (8 imágenes — una por entrada de día)
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `day-1.jpg` | 1000×750 | 4:3 | Día 1 — llegada al destino (aeropuerto, primer lodge). |
| `day-2.jpg` | 1000×750 | 4:3 | Día 2/3 — Aberdares (rinos, bosque). |
| `day-3.jpg` | 1000×750 | 4:3 | Día 4/5 — Tarangire (elefantes, baobabs). |
| `day-4.jpg` | 1000×750 | 4:3 | Día 6 — Manyara + Ngorongoro (leones, cráter). |
| `day-5.jpg` | 1000×750 | 4:3 | Día 7 — vuelo en globo sobre el Serengeti. |
| `day-6.jpg` | 1000×750 | 4:3 | Días 8–10 — río Mara (cruces, migración). |
| `day-7.jpg` | 1000×750 | 4:3 | Días 11–13 — Naboisho (masais, safari a pie). |
| `day-8.jpg` | 1000×750 | 4:3 | Día 14 — salida desde Nairobi (orfanato de elefantes, despedida). |

### Lodges seleccionados (4)
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `lodge-1.jpg` | 1200×1500 | 4:5 | Sanctuary Swala Camp (Tarangire). |
| `lodge-2.jpg` | 1200×1500 | 4:5 | Ngorongoro Crater Lodge. |
| `lodge-3.jpg` | 1200×1500 | 4:5 | Kogatende Tented Camp. |
| `lodge-4.jpg` | 1200×1500 | 4:5 | Naboisho Camp. |

### Extensiones (3 cards) — *reuse imágenes de destinos*
- Zanjíbar → `dest-indianocean.jpg`
- Gorilas de Ruanda → `dest-asia.jpg` *(o foto específica de gorila)*
- Cataratas Victoria → `intro-quote.jpg` *(o foto específica)*

### Reseñas (avatares circulares 56×56px)
| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `review-1.jpg` | 200×200 | 1:1 | Avatar/retrato cabeza de reseña 1 (puede ser foto en redondo). |
| `review-2.jpg` | 200×200 | 1:1 | Avatar/retrato cabeza de reseña 2. |

---

## 5. Pequeñas expediciones (`small-group.html`)

| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `way-group.jpg` *(reuse)* | 1600×1200 | 4:3 | Hero side image — grupo en exterior. |
| Cards horizontales grandes | varias | ver detalles | Reusan los `j-*.jpg` |

---

## 6. Catálogos (`catalogos.html`) *— pendiente*

12 tarjetas de catálogo, cada una con una "tapa" vertical (estilo libro).

| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `brochure-1.jpg` … `brochure-12.jpg` | 600×800 | 3:4 | Tapa simulada de cada catálogo. Foto destacada del destino + título superpuesto. |

---

## 7. Contacto (`contact.html`)

| Archivo | Dimensión | Ratio | Qué |
|---|---|---|---|
| `way-private.jpg` *(reuse)* | 1200×1500 | 4:5 | Imagen izquierda — paisaje editorial. |

---

## Resumen de prioridades

Cuando tengas tiempo de subir fotos, **prioridad alta** son las que más impactan:

1. **`hero-savannah.jpg`** (homepage hero principal) — la primera impresión
2. **3 cards de destinos en homepage** (`dest-japan`, `dest-patagonia`, `dest-morocco`)
3. **2 cards de "stay with"** (`stay-sanctuari`, `stay-villa`)
4. **`why-banner.jpg`** (banner cobre con CTA)
5. **`fund-people.jpg`** (filantropía)
6. **Los 10 países de Europa** + **10 regiones del mosaico**

Eso son **~20 fotos** que cubren el 80% del impacto visual. Cuando las subas, el sitio salta de "demo" a "realista" en un commit.

---

## Cómo subir las imágenes

1. Asegurate de que el nombre del archivo coincida exactamente con la lista de arriba (incluyendo `.jpg` en minúscula y guiones).
2. Subilas a la carpeta `assets/img/` del repo en GitHub.
3. Hacé commit (Netlify redespliega automáticamente).
4. En 60 segundos las ves online.

Si querés que las pase yo (vos me las pasás por mail/WhatsApp y yo las commiteo), también funciona.

## Si te falta una foto

Subí solo las que tengas. Las que falten siguen mostrando el placeholder procedual hasta que tengas la real. Sin romper el sitio.
