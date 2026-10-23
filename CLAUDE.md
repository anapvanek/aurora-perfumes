# Aurora Perfumes – catálogo web

Catálogo de Aurora Perfumes (Mendoza). Publicado en https://aurora-perfumes.tiendamendoza.workers.dev/
(Cloudflare Workers publica la carpeta `site/` automáticamente con cada push a `main`; config en wrangler.jsonc). Antes estaba en Netlify (auroraperfumesmza.netlify.app), que cobra créditos por publicación: no usar.

La dueña escribe en español rioplatense; responderle siempre en español.

## Estructura
- `src/data.js` – datos del catálogo (DATA árabes, EXT extractos, TUB tubitos, HOG hogar y auto, HMETA, OUT_A, OUT_T).
- `src/template.html` – diseño y lógica (carrito, pedido por WhatsApp, precios por cantidad).
- `src/build.py` – genera `site/index.html`. Correr `python3 src/build.py` antes de cada commit.
- `site/img/` – fotos (480x600 o 640x640 jpg). La clave en data.js = nombre del archivo sin `.jpg`. Fotos que la dueña manda por chat (sin Drive) usan nombre descriptivo, ej. `ext-goddess`.
  - árabes: nombre libre (ej. `asad`), fondo blanco.
  - extractos: `ext-<driveId>`, tubitos: `tub-<driveId>`, hogar: `hog-<driveId>` (recorte 4:5).
  - fichas de notas (Fragrantica): `fic-<driveId>` (800x800), siempre como foto 2 del perfume en árabes, extractos y tubitos.
    Carpeta Drive `1cqaheS2d4KB78Fg3hr7rDXc0pbsxxCLB`. En la galería se ven enteras (sin recorte) y se abren grandes al tocarlas. La tarjeta nunca muestra la ficha: si el producto no tiene foto propia, muestra las iniciales.
- `site/fonts/montserrat.woff2` – tipografía (Montserrat, pedida por la dueña; no cambiarla).

## Fuente de datos: Google Sheet
ID `1HM9X4Zg8wNx-NHFNsy_i4lg3ma0UGu1vHTOJr_Tbugg`. Pestañas:
ÁRABES ORIGINALES · TUBITOS ÁRABES 35ML · EXTRACTOS 60ML · PERFUMINAS TEXTILES 250ML ·
DIFUSORES DE AMBIENTE 125ML · DIFUSORES PARA AUTO 10ML.

Cuando la dueña dice **"actualizá"**: leer todas las pestañas, comparar con `src/data.js`
(nombres, precios, stock SI/NO/PRÓXIMAMENTE, fotos por ID de Drive), aplicar los cambios, `python3 src/build.py`,
commit y push. Contarle qué cambió.

Reglas de la planilla (si se la edita): todas las filas de producto 62px, SIN filas separadoras entre marcas
(se borraron el 23/10/2026; las marcas se separan por el recuadro de la columna A), bordes completos B:G,
columna A coloreada por marca. Ojo: las tablas de escala de precios están en I1:J8 de tubitos y extractos;
borrar filas enteras las rompe (usar insertRange/deleteRange solo en A:G). Stock de árabes: SI/NO/PRÓXIMAMENTE (desplegable de la tabla).
Las fotos de la planilla son imágenes flotantes (la API no las puede poner ni mover). Para cargarlas/corregirlas la dueña
corre `ponerFotos` (tools/ponerFotos.gs, ya pegado en Extensiones → Apps Script de la planilla): borra las fotos de árabes,
tubitos y extractos y pone las mismas de la página (B = foto, C = ficha), usando `site/fotos-planilla.json` que genera build.py.
Si la dueña corrió `activarAutomatico`, un disparador cada 10 min corre `automatico`: si cambió fotos-planilla.json
rehace las fotos solo (no hace falta pedirle nada). Si no, después de agregar fotos: pedirle que corra `ponerFotos`.

## Reglas de negocio
- Stock en la planilla: SI · NO (sin stock, `OUT_A`/`OUT_T`/ok=0) · PRÓXIMAMENTE (mercadería en camino: `SOON_A` en data.js; la tarjeta se ve en blanco y negro con el cartel "Próximamente" y no se puede agregar al pedido). Cuenta regresiva "Llega en 02:07:36:10" (días:horas:min:seg, sin letras): `SOON_AT` en data.js ({"*": fecha ISO con -03:00} para todos, o por nombre); sin fecha o vencida muestra "Próximamente".
- Precio de árabes desde factura del proveedor: (costo US$ + 2) × 1630, + 21000 minorista / + 16000 mayorista, redondeado para arriba a $1.000 (margen vigente desde 23/10/2026; antes +16000/+11000). Los precios de productos existentes no se tocan hasta que la dueña lo pida.
- Árabes: 100% originales; mayorista desde 4 unidades combinadas.
- Extractos 60 ml y tubitos 35 ml: inspirados, NO originales (mantener el aviso). Precio por escala (TIERS en template).
- Tubitos: 1 u $4.000 · 10+ $2.600 · 20+ $2.000 · 60+ $1.900 · 100+ $1.800. Caja surtida x20 (aromas a elección del local, no se eligen) $36.000: producto aparte (B|BOX en template, foto tub-caja-surtida), no suma a la escala de tubitos.
- Hogar y auto: mayorista desde 10 unidades combinadas entre perfuminas y difusores.
- Precios por cantidad: tablas siempre visibles (sin desplegables).
- Detalle de producto: botón "Compartir" (arriba a la izquierda). Enlace directo `?p=<categoría>-<marca>-<nombre>` (slug en template) abre ese producto.
- WhatsApp de pedidos: 5492612420544.
