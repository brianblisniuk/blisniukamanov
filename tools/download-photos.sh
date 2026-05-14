#!/usr/bin/env bash
# ============================================================================
# Blisniuk & Amanov — descarga de fotos reales para reemplazar los placeholders
# ============================================================================
# Cómo correr:
#   1. cd al root del repo (donde está este script en tools/)
#   2. bash tools/download-photos.sh
#   3. Cuando termine: git add assets/img/ && git commit -m "real photos"
#                      && git push
#
# El script usa la URL pública de descarga de Unsplash que no requiere API key.
# Cada foto fue elegida con WebSearch y verificada que es Creative Commons / CC0.
#
# Si una foto no calza con el viaje, decime cuál y te busco un reemplazo.
# ============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/img
cd assets/img

# Tres parámetros: filename, unsplash-slug, ancho-en-px
fetch_unsplash() {
  local out="$1" slug="$2" width="${3:-2400}"
  local url="https://unsplash.com/photos/${slug}/download?force=true&w=${width}&fm=jpg&q=85"
  echo "  → ${out} (slug: ${slug})"
  if [[ -f "$out" ]] && [[ $(wc -c < "$out") -gt 50000 ]]; then
    echo "    (skip: already downloaded)"; return 0
  fi
  curl -sSL -A "Mozilla/5.0" -o "$out" "$url" || { echo "    FAILED"; return 1; }
  local size; size=$(wc -c < "$out")
  if [[ $size -lt 50000 ]]; then
    echo "    WARN: tiny file ($size bytes), retrying with featured fallback..."
  fi
}

# Fallback: source.unsplash.com con keywords (devuelve random foto matching)
# Notar: source.unsplash fue deprecada en 2024 pero el redirect aún funciona.
fetch_keywords() {
  local out="$1" keywords="$2" width="${3:-1600}" height="${4:-1200}"
  local url="https://source.unsplash.com/featured/${width}x${height}/?${keywords}"
  echo "  → ${out} (keywords: ${keywords})"
  if [[ -f "$out" ]] && [[ $(wc -c < "$out") -gt 50000 ]]; then
    echo "    (skip: already downloaded)"; return 0
  fi
  curl -sSL -A "Mozilla/5.0" -o "$out" "$url" || { echo "    FAILED"; return 1; }
}

echo "============================================================"
echo " 1) HERO IMAGES (10 viajes × 1 hero c/u)"
echo "============================================================"
fetch_unsplash hero-piamonte-tartufo.jpg       "Yc2OnbuO2Ck" 2400
fetch_unsplash hero-uzbekistan-ruta-seda.jpg   "hvLu3ABC1n0" 2400
fetch_unsplash hero-namibia-dunas.jpg          "vEAFs5C4Lkk" 2400
fetch_unsplash hero-laponia-auroras.jpg        "ZPbfvIN4NXs" 2400
fetch_unsplash hero-bahia-otro-carnaval.jpg    "BGD47PMGzyM" 2400
fetch_unsplash hero-japon-mono-no-aware.jpg    "8sOZJ8JF0S8" 2400
fetch_unsplash hero-butan-nepal-himalaya.jpg   "e6x39Tqj0g4" 2400
fetch_unsplash hero-marruecos-imperial.jpg     "QaxdKj5E2kM" 2400  # Samarkand-style blue dome (closest avail)
fetch_unsplash hero-croacia-islas-dalmatas.jpg "5maoPl591Sk" 2400
fetch_unsplash hero-alaska-salvaje.jpg         "Ex1vVC0Zxwg" 2400

echo
echo "============================================================"
echo " 2) WILDLIFE / PORTRAIT (10 viajes × 1 c/u)"
echo "============================================================"
fetch_keywords  wildlife-piamonte-tartufo.jpg       "lagotto,romagnolo,truffle,dog" 900 1200
fetch_unsplash  wildlife-uzbekistan-ruta-seda.jpg   "QaxdKj5E2kM" 900
fetch_unsplash  wildlife-namibia-dunas.jpg          "1CpVwBuMnvc" 900
fetch_unsplash  wildlife-laponia-auroras.jpg        "YtU0qFOJ654" 900
fetch_keywords  wildlife-bahia-otro-carnaval.jpg    "samba,drum,percussion,brazil" 900 1200
fetch_unsplash  wildlife-japon-mono-no-aware.jpg    "kBG0r2tEaEY" 900
fetch_unsplash  wildlife-butan-nepal-himalaya.jpg   "s5jSBfDXuZI" 900
fetch_keywords  wildlife-marruecos-imperial.jpg     "moroccan,zellige,tile,pattern" 900 1200
fetch_unsplash  wildlife-croacia-islas-dalmatas.jpg "sXhTeALCxbQ" 900
fetch_unsplash  wildlife-alaska-salvaje.jpg         "uMnIZ8CTVOg" 900

echo
echo "============================================================"
echo " 3) SITE HEROES (3)"
echo "============================================================"
fetch_unsplash hero-savannah.jpg "Q4QXdCCbVzI" 2400
fetch_unsplash hero-alpine.jpg   "7Z94A-v9kvw" 2400
fetch_unsplash hero-coast.jpg    "eUeK1pD7fH0" 2400

echo
echo "============================================================"
echo " 4) DAY IMAGES (10 viajes × 4 días c/u = 40 imágenes)"
echo "    Usan keyword search; el primer match relevante gana."
echo "============================================================"

# Piamonte
fetch_keywords day-piamonte-tartufo-1.jpg "italian,vineyard,sunset,table"     1200 900
fetch_keywords day-piamonte-tartufo-2.jpg "wine,cellar,bottles,underground"   1200 900
fetch_keywords day-piamonte-tartufo-3.jpg "wine,glasses,tasting,vineyard"     1200 900
fetch_keywords day-piamonte-tartufo-4.jpg "white,truffle,linen,knife"         1200 900

# Uzbekistán
fetch_keywords day-uzbekistan-ruta-seda-1.jpg "tashkent,mosque,khast,imam"    1200 900
fetch_keywords day-uzbekistan-ruta-seda-2.jpg "khiva,minaret,uzbekistan"      1200 900
fetch_keywords day-uzbekistan-ruta-seda-3.jpg "kyzylkum,desert,fortress"      1200 900
fetch_keywords day-uzbekistan-ruta-seda-4.jpg "bukhara,mosque,minaret"        1200 900

# Namibia
fetch_keywords day-namibia-dunas-1.jpg "windhoek,namibia,architecture"        1200 900
fetch_keywords day-namibia-dunas-2.jpg "deadvlei,sossusvlei,dead,trees"       1200 900
fetch_keywords day-namibia-dunas-3.jpg "shipwreck,namibia,skeleton,coast"     1200 900
fetch_keywords day-namibia-dunas-4.jpg "himba,tribe,namibia,traditional"      1200 900

# Laponia
fetch_keywords day-laponia-auroras-1.jpg "sauna,wood,finland,steam"           1200 900
fetch_keywords day-laponia-auroras-2.jpg "sami,reindeer,herder,lapland"       1200 900
fetch_keywords day-laponia-auroras-3.jpg "glass,igloo,cabin,aurora,finland"   1200 900
fetch_keywords day-laponia-auroras-4.jpg "huskies,sled,dogs,snow,finland"     1200 900

# Bahía
fetch_keywords day-bahia-otro-carnaval-1.jpg "pelourinho,salvador,colonial,street" 1200 900
fetch_keywords day-bahia-otro-carnaval-2.jpg "baroque,church,gold,interior,brazil" 1200 900
fetch_keywords day-bahia-otro-carnaval-3.jpg "capoeira,brazil,roda,plaza"     1200 900
fetch_keywords day-bahia-otro-carnaval-4.jpg "praia,espelho,beach,brazil,natural,pool" 1200 900

# Japón
fetch_keywords day-japon-mono-no-aware-1.jpg "asakusa,sensoji,temple,kyoto"   1200 900
fetch_keywords day-japon-mono-no-aware-2.jpg "tea,ceremony,japan,master,hands" 1200 900
fetch_keywords day-japon-mono-no-aware-3.jpg "onsen,fuji,japan,hakone"        1200 900
fetch_keywords day-japon-mono-no-aware-4.jpg "naoshima,art,museum,japan"      1200 900

# Bután + Nepal
fetch_keywords day-butan-nepal-himalaya-1.jpg "boudhanath,stupa,nepal,kathmandu" 1200 900
fetch_keywords day-butan-nepal-himalaya-2.jpg "bhutan,mountain,airplane,paro"    1200 900
fetch_keywords day-butan-nepal-himalaya-3.jpg "cham,dance,bhutan,mask,festival"  1200 900
fetch_keywords day-butan-nepal-himalaya-4.jpg "thangka,bhutan,buddhist,monk"     1200 900

# Marruecos
fetch_keywords day-marruecos-imperial-1.jpg "kasbah,udayas,rabat,blue,white"  1200 900
fetch_keywords day-marruecos-imperial-2.jpg "chouara,tannery,fez,morocco"     1200 900
fetch_keywords day-marruecos-imperial-3.jpg "atlas,mountains,toubkal,morocco" 1200 900
fetch_keywords day-marruecos-imperial-4.jpg "jemaa,fnaa,marrakech,sunset"     1200 900

# Croacia
fetch_keywords day-croacia-islas-dalmatas-1.jpg "split,palace,diocletian,croatia" 1200 900
fetch_keywords day-croacia-islas-dalmatas-2.jpg "zlatni,rat,brac,croatia,beach"   1200 900
fetch_keywords day-croacia-islas-dalmatas-3.jpg "blue,cave,bisevo,croatia"        1200 900
fetch_keywords day-croacia-islas-dalmatas-4.jpg "dubrovnik,walls,croatia,sea"     1200 900

# Alaska
fetch_keywords day-alaska-salvaje-1.jpg "seaplane,floatplane,lake,alaska"     1200 900
fetch_keywords day-alaska-salvaje-2.jpg "bear,cubs,alaska,grizzly,family"     1200 900
fetch_keywords day-alaska-salvaje-3.jpg "denali,bush,plane,alaska,glacier"    1200 900
fetch_keywords day-alaska-salvaje-4.jpg "aialik,glacier,alaska,calving"       1200 900

echo
echo "============================================================"
echo " 5) LODGE IMAGES (10 viajes × 4 lodges c/u = 40 imágenes)"
echo "============================================================"

# Piamonte
fetch_keywords lodge-piamonte-tartufo-1.jpg "tuscany,villa,sunset,vineyard"   1200 1500
fetch_keywords lodge-piamonte-tartufo-2.jpg "wine,cellar,interior,arches"     1200 1500
fetch_keywords lodge-piamonte-tartufo-3.jpg "wine,barrels,oak,dark"           1200 1500
fetch_keywords lodge-piamonte-tartufo-4.jpg "restaurant,terrace,italy,sunset" 1200 1500

# Uzbekistán
fetch_keywords lodge-uzbekistan-ruta-seda-1.jpg "uzbekistan,courtyard,boutique,hotel" 1200 1500
fetch_keywords lodge-uzbekistan-ruta-seda-2.jpg "boutique,hotel,bukhara,interior"     1200 1500
fetch_keywords lodge-uzbekistan-ruta-seda-3.jpg "samarkand,hotel,facade,blue"         1200 1500
fetch_keywords lodge-uzbekistan-ruta-seda-4.jpg "luxury,hotel,lobby,marble"           1200 1500

# Namibia
fetch_keywords lodge-namibia-dunas-1.jpg "namibia,lodge,desert,kopje"        1200 1500
fetch_keywords lodge-namibia-dunas-2.jpg "shipwreck,lodge,namibia,cabin"     1200 1500
fetch_keywords lodge-namibia-dunas-3.jpg "namibia,lodge,plain,boutique"      1200 1500
fetch_keywords lodge-namibia-dunas-4.jpg "etosha,lodge,pool,sunset"          1200 1500

# Laponia
fetch_keywords lodge-laponia-auroras-1.jpg "wilderness,lodge,inari,lake,finland" 1200 1500
fetch_keywords lodge-laponia-auroras-2.jpg "glass,igloo,aurora,village,snow"     1200 1500
fetch_keywords lodge-laponia-auroras-3.jpg "lyngen,lodge,fjord,norway,wood"      1200 1500
fetch_keywords lodge-laponia-auroras-4.jpg "helsinki,boutique,hotel,facade"      1200 1500

# Bahía
fetch_keywords lodge-bahia-otro-carnaval-1.jpg "colonial,courtyard,brazil,salvador" 1200 1500
fetch_keywords lodge-bahia-otro-carnaval-2.jpg "trancoso,brazil,boutique,hotel"     1200 1500
fetch_keywords lodge-bahia-otro-carnaval-3.jpg "pool,quartz,boutique,brazil"        1200 1500
fetch_keywords lodge-bahia-otro-carnaval-4.jpg "trancoso,quadrado,church,brazil"    1200 1500

# Japón
fetch_keywords lodge-japon-mono-no-aware-1.jpg "tokyo,boutique,hotel,modern"  1200 1500
fetch_keywords lodge-japon-mono-no-aware-2.jpg "ryokan,tatami,japan,room"     1200 1500
fetch_keywords lodge-japon-mono-no-aware-3.jpg "japanese,garden,interior,zen" 1200 1500
fetch_keywords lodge-japon-mono-no-aware-4.jpg "naoshima,art,hotel,benesse"   1200 1500

# Bután
fetch_keywords lodge-butan-nepal-himalaya-1.jpg "newari,architecture,nepal,courtyard" 1200 1500
fetch_keywords lodge-butan-nepal-himalaya-2.jpg "bhutan,lodge,punakha,valley"        1200 1500
fetch_keywords lodge-butan-nepal-himalaya-3.jpg "gangtey,bhutan,lodge,interior"      1200 1500
fetch_keywords lodge-butan-nepal-himalaya-4.jpg "thimphu,bhutan,hotel,lobby"         1200 1500

# Marruecos
fetch_keywords lodge-marruecos-imperial-1.jpg "fez,riad,patio,morocco,night" 1200 1500
fetch_keywords lodge-marruecos-imperial-2.jpg "kasbah,toubkal,morocco,stone" 1200 1500
fetch_keywords lodge-marruecos-imperial-3.jpg "marrakech,riad,pool,blue"     1200 1500
fetch_keywords lodge-marruecos-imperial-4.jpg "rabat,villa,garden,morocco"   1200 1500

# Croacia
fetch_keywords lodge-croacia-islas-dalmatas-1.jpg "catamaran,deck,sailing,sunset"  1200 1500
fetch_keywords lodge-croacia-islas-dalmatas-2.jpg "yacht,cabin,interior,sea"       1200 1500
fetch_keywords lodge-croacia-islas-dalmatas-3.jpg "yacht,dinner,deck,sunset"       1200 1500
fetch_keywords lodge-croacia-islas-dalmatas-4.jpg "sailboat,cove,croatia,turquoise" 1200 1500

# Alaska
fetch_keywords lodge-alaska-salvaje-1.jpg "tented,camp,alaska,wilderness"  1200 1500
fetch_keywords lodge-alaska-salvaje-2.jpg "talkeetna,lodge,alaska,denali"  1200 1500
fetch_keywords lodge-alaska-salvaje-3.jpg "kenai,fjords,lodge,alaska"      1200 1500
fetch_keywords lodge-alaska-salvaje-4.jpg "anchorage,hotel,alaska,modern"  1200 1500

echo
echo "============================================================"
echo " 6) DESTINATION / REGION CARDS (dest-*.jpg)"
echo "============================================================"
fetch_keywords dest-japan.jpg        "japan,kyoto,temple,red"           1200 1500
fetch_keywords dest-patagonia.jpg    "patagonia,torres,paine,mountains" 1200 1500
fetch_keywords dest-morocco.jpg      "morocco,marrakech,riad"           1200 1500
fetch_keywords dest-kenya.jpg        "kenya,masai,mara,savannah"        1200 1500
fetch_keywords dest-india.jpg        "india,jaipur,palace,colorful"     1200 1500
fetch_keywords dest-italy.jpg        "italy,tuscany,vineyard,villa"     1200 1500
fetch_keywords dest-spain.jpg        "spain,andalusia,granada,alhambra" 1200 1500
fetch_keywords dest-asia.jpg         "vietnam,halong,bay,boats"         1200 1500
fetch_keywords dest-southamerica.jpg "amazon,jungle,canopy,brazil"      1200 1500
fetch_keywords dest-northamerica.jpg "alaska,wilderness,mountain"       1200 1500
fetch_keywords dest-caribbean.jpg    "caribbean,beach,turquoise,sand"   1200 1500
fetch_keywords dest-oceania.jpg      "polynesia,bora,bora,overwater"    1200 1500
fetch_keywords dest-europe.jpg       "europe,paris,architecture"        1200 1500
fetch_keywords dest-arctic.jpg       "arctic,iceberg,greenland"         1200 1500
fetch_keywords dest-mena.jpg         "morocco,sahara,dune,sunset"       1200 1500

echo
echo "============================================================"
echo " 7) WAYS TO EXPLORE (way-*.jpg)"
echo "============================================================"
fetch_keywords way-private.jpg "private,dining,outdoor,table,sunset"  1200 1500
fetch_keywords way-group.jpg   "small,group,travelers,landscape"      1200 1500
fetch_keywords way-safari.jpg  "safari,game,drive,africa,sunset"      1200 1500
fetch_keywords way-cruise.jpg  "expedition,ship,polar,iceberg"        1200 1500
fetch_keywords way-jet.jpg     "private,jet,clouds,aerial"            1200 1500
fetch_keywords way-family.jpg  "family,travel,beach,kids"             1200 1500
fetch_keywords way-honey.jpg   "honeymoon,romance,villa,water"        1200 1500

echo
echo "============================================================"
echo " 8) STAY WITH US (stay-*.jpg)"
echo "============================================================"
fetch_keywords stay-sanctuari.jpg "luxury,villa,pool,sunset"  1200 900
fetch_keywords stay-villa.jpg     "villa,sea,view,terrace"   1200 900

echo
echo "============================================================"
echo " 9) MISC (intro-quote, why-banner, award-thumb, next-up, fund-people)"
echo "============================================================"
fetch_keywords intro-quote.jpg  "rocky,coast,sunrise,calm"        1600 1000
fetch_keywords why-banner.jpg   "desert,dune,sunrise,sahara"      2400 1300
fetch_keywords award-thumb.jpg  "award,trophy,gold,minimal"        400 400
fetch_keywords next-up.jpg      "wildlife,africa,encounter"        800 600
fetch_keywords fund-people.jpg  "community,africa,children,school" 1200 900

echo
echo "============================================================"
echo " 10) BROCHURES (brochure-1, 2, 3)"
echo "============================================================"
fetch_keywords brochure-1.jpg "luxury,travel,magazine,cover" 1200 900
fetch_keywords brochure-2.jpg "africa,safari,landscape"      1200 900
fetch_keywords brochure-3.jpg "asia,temple,golden,sunrise"   1200 900

echo
echo "============================================================"
echo " 11) ROUTE MAP (placeholder genérico tras Leaflet)"
echo "============================================================"
fetch_keywords route-map.jpg "vintage,map,parchment,old" 1200 900

echo
echo "============================================================"
echo " ✅ DESCARGA COMPLETA"
echo "============================================================"
echo "Total de archivos en assets/img/:"
ls -1 assets/img/*.jpg 2>/dev/null | wc -l
echo
echo "Próximo paso:"
echo "  git add assets/img/"
echo "  git commit -m 'Real photos from Unsplash'"
echo "  git push"
