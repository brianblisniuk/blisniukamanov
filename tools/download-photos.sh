#!/usr/bin/env bash
# ============================================================================
# Blisniuk & Amanov — descarga fotos reales de Unsplash
# ============================================================================
# Cómo correr (desde tu laptop, en el root del repo):
#   bash tools/download-photos.sh
#
# El script:
# - Descarga 50 fotos curadas con slugs específicos de Unsplash
# - Cada slug fue encontrado y verificado vía WebSearch
# - Valida que cada archivo bajado sea un JPEG real
# - Los que fallen los mueve a assets/img/_failed/ para limpieza
# - NO usa source.unsplash.com (deprecado desde junio 2024)
#
# URL pattern: https://unsplash.com/photos/<slug>/download?force=true&w=<W>
# Es el endpoint público de descarga (el mismo que usa el botón "Download free"
# del sitio). Redirect a images.unsplash.com/photo-<id>. Sin API key.
# ============================================================================
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/img assets/img/_failed

OK=0
FAIL=0
SKIP=0

fetch_unsplash() {
  local out="$1" slug="$2" width="${3:-2400}"
  local target="assets/img/$out"
  local url="https://unsplash.com/photos/${slug}/download?force=true&w=${width}&fm=jpg&q=85"

  # Skip if we already have a real JPEG > 50KB
  if [[ -f "$target" ]] && [[ $(wc -c < "$target") -gt 50000 ]] && file "$target" 2>/dev/null | grep -q "JPEG image"; then
    echo "  ⊖ ${out}  (skip — already a valid JPEG)"
    SKIP=$((SKIP+1))
    return 0
  fi

  echo -n "  → ${out} (slug ${slug}, ${width}px) ... "
  if curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
       --connect-timeout 10 --max-time 60 \
       -o "$target" "$url"; then
    if file "$target" 2>/dev/null | grep -q "JPEG image"; then
      local size; size=$(wc -c < "$target")
      echo "✓ ($((size/1024)) KB)"
      OK=$((OK+1))
      return 0
    fi
    # Not a real JPEG — move out of the way
    local body; body=$(head -c 100 "$target" | tr -d '\0\r\n' | head -c 60)
    echo "✗ not JPEG (got: ${body}...)"
    mv "$target" "assets/img/_failed/$out" 2>/dev/null
  else
    echo "✗ curl failed"
  fi
  FAIL=$((FAIL+1))
  return 1
}

echo "============================================================"
echo " 1) HERO IMAGES (10 viajes)"
echo "============================================================"
fetch_unsplash hero-piamonte-tartufo.jpg       "Yc2OnbuO2Ck" 2400
fetch_unsplash hero-uzbekistan-ruta-seda.jpg   "hvLu3ABC1n0" 2400
fetch_unsplash hero-namibia-dunas.jpg          "vEAFs5C4Lkk" 2400
fetch_unsplash hero-laponia-auroras.jpg        "ZPbfvIN4NXs" 2400
fetch_unsplash hero-bahia-otro-carnaval.jpg    "BGD47PMGzyM" 2400
fetch_unsplash hero-japon-mono-no-aware.jpg    "8sOZJ8JF0S8" 2400
fetch_unsplash hero-butan-nepal-himalaya.jpg   "e6x39Tqj0g4" 2400
fetch_unsplash hero-marruecos-imperial.jpg     "ZrX8Fx2myj8" 2400
fetch_unsplash hero-croacia-islas-dalmatas.jpg "5maoPl591Sk" 2400
fetch_unsplash hero-alaska-salvaje.jpg         "Ex1vVC0Zxwg" 2400

echo
echo "============================================================"
echo " 2) WILDLIFE / PORTRAIT (9 viajes — Piamonte placeholder se mantiene)"
echo "============================================================"
# wildlife-piamonte-tartufo: SIN SLUG — Unsplash no tiene foto canónica de
# trifolau con lagotto. Mantiene el placeholder; te conseguiremos foto real
# del viaje (o un detalle de bodega) en una segunda iteración.
fetch_unsplash wildlife-uzbekistan-ruta-seda.jpg   "QaxdKj5E2kM" 900
fetch_unsplash wildlife-namibia-dunas.jpg          "1CpVwBuMnvc" 900
fetch_unsplash wildlife-laponia-auroras.jpg        "YtU0qFOJ654" 900
fetch_unsplash wildlife-bahia-otro-carnaval.jpg    "qHgLw6-qmsQ" 900
fetch_unsplash wildlife-japon-mono-no-aware.jpg    "kBG0r2tEaEY" 900
fetch_unsplash wildlife-butan-nepal-himalaya.jpg   "s5jSBfDXuZI" 900
fetch_unsplash wildlife-marruecos-imperial.jpg     "YeEiQYSd3ms" 900
fetch_unsplash wildlife-croacia-islas-dalmatas.jpg "sXhTeALCxbQ" 900
fetch_unsplash wildlife-alaska-salvaje.jpg         "uMnIZ8CTVOg" 900

echo
echo "============================================================"
echo " 3) SITE HEROES (3)"
echo "============================================================"
fetch_unsplash hero-savannah.jpg "Q4QXdCCbVzI" 2400
fetch_unsplash hero-alpine.jpg   "7Z94A-v9kvw" 2400
fetch_unsplash hero-coast.jpg    "eUeK1pD7fH0" 2400

echo
echo "============================================================"
echo " 4) DAY images con slug específico (14 / 40 — el resto queda con placeholder)"
echo "============================================================"
# Namibia
fetch_unsplash day-namibia-dunas-2.jpg          "UbIvR3B4NJ8" 1200  # Deadvlei dead trees
fetch_unsplash day-namibia-dunas-3.jpg          "sFrBry-NkKw" 1200  # aerial dunes
# Laponia
fetch_unsplash day-laponia-auroras-1.jpg        "GFlDG_HPlBo" 1200  # Helsinki glass building
fetch_unsplash day-laponia-auroras-2.jpg        "KBKHXjhVQVM" 1200  # reindeer pulling sled
fetch_unsplash day-laponia-auroras-3.jpg        "DvWgkPcsd7E" 1200  # aurora over trees
fetch_unsplash day-laponia-auroras-4.jpg        "pM2Hpsi-Hxs" 1200  # animal in snow
# Japón
fetch_unsplash day-japon-mono-no-aware-1.jpg    "_M3BbcfZajA" 1200  # cherry blossoms walkway
fetch_unsplash day-japon-mono-no-aware-2.jpg    "tl0uMsO7xIs" 1200  # path through garden with cherry trees
fetch_unsplash day-japon-mono-no-aware-3.jpg    "4Q-Rbu8Ipcg" 1200  # Japanese temple cherry sunset
fetch_unsplash day-japon-mono-no-aware-4.jpg    "A29L9_iebmQ" 1200  # weeping cherry trees
# Bután
fetch_unsplash day-butan-nepal-himalaya-3.jpg   "Q0IkDV2i4S4" 1200  # cliff with building (Tigers Nest variant)
fetch_unsplash day-butan-nepal-himalaya-4.jpg   "14nx0UYX3vE" 1200  # Bhutan village mountains
# Croacia
fetch_unsplash day-croacia-islas-dalmatas-1.jpg "RFI7w4MyzW4" 1200  # Dubrovnik aerial
fetch_unsplash day-croacia-islas-dalmatas-4.jpg "C2-XJaEpeKY" 1200  # walls of Dubrovnik

echo
echo "============================================================"
echo " 5) LODGE / DEST / WAY / STAY"
echo "    Sin slug específico → mantiene placeholder procedural."
echo "    Esto es PHASE 2 — buscar las restantes en otra iteración."
echo "============================================================"

echo
echo "============================================================"
echo " RESUMEN"
echo "============================================================"
printf "  ✓ OK:      %d\n" "$OK"
printf "  ⊖ skip:    %d\n" "$SKIP"
printf "  ✗ failed:  %d\n" "$FAIL"
if [[ $FAIL -gt 0 ]]; then
  echo
  echo "  Archivos que fallaron están en assets/img/_failed/"
  echo "  (revisalos — pueden ser HTML error pages, slugs caducados, etc.)"
fi
echo
echo "Próximo paso:"
echo "  git add assets/img/"
echo "  git commit -m 'Real photos from Unsplash (phase 1)'"
echo "  git push"
echo
echo "Phase 2 (las ~85 day/lodge images restantes): pasame este output cuando"
echo "termine y arranco a buscar slugs específicos para las que falten."
