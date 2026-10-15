# Aurora Perfumes – catálogo web

Catálogo de Aurora Perfumes (Mendoza). Publicado en https://auroraperfumesmza.netlify.app/
(Netlify publica la carpeta `site/` automáticamente con cada push a `main`).

La dueña escribe en español rioplatense; responderle siempre en español.

## Estructura
- `src/data.js` – datos del catálogo (DATA árabes, EXT extractos, TUB tubitos, HOG hogar y auto, HMETA, OUT_A, OUT_T).
- `src/template.html` – diseño y lógica (carrito, pedido por WhatsApp, precios por cantidad).
- `src/build.py` – genera `site/index.html`. Correr `python3 src/build.py` antes de cada commit.
- `site/img/` – fotos (480x600 o 640x640 jpg). La clave en data.js = nombre del archivo sin `.jpg`.
  - árabes: nombre libre (ej. `asad`), fondo blanco.
  - extractos: `ext-<driveId>`, tubitos: `tub-<driveId>`, hogar: `hog-<driveId>` (recorte 4:5).
- `site/fonts/montserrat.woff2` – tipografía (Montserrat, pedida por la dueña; no cambiarla).

## Fuente de datos: Google Sheet
ID `1HM9X4Zg8wNx-NHFNsy_i4lg3ma0UGu1vHTOJr_Tbugg`. Pestañas:
ÁRABES ORIGINALES · TUBITOS ÁRABES 35ML · EXTRACTOS 60ML · PERFUMINAS TEXTILES 250ML ·
DIFUSORES DE AMBIENTE 125ML · DIFUSORES PARA AUTO 10ML.

Cuando la dueña dice **"actualizá"**: leer todas las pestañas, comparar con `src/data.js`
(nombres, precios, stock SI/NO, fotos por ID de Drive), aplicar los cambios, `python3 src/build.py`,
commit y push. Contarle qué cambió.

Reglas de la planilla (si se la edita): filas de producto 62px, separadoras 21px, una fila vacía
entre marcas, bordes completos B:G, columna A coloreada por marca.

## Reglas de negocio
- Árabes: 100% originales; mayorista desde 4 unidades combinadas.
- Extractos 60 ml y tubitos 35 ml: inspirados, NO originales (mantener el aviso). Precio por escala (TIERS en template).
- Tubitos: 1 u $4.000 · 10+ $2.600 · 20+ $2.000 · 60+ $1.900 · 100+ $1.800. No hay producto "caja surtida".
- Hogar y auto: mayorista desde 10 unidades combinadas entre perfuminas y difusores.
- Precios por cantidad: tablas siempre visibles (sin desplegables).
- WhatsApp de pedidos: 5492612420544.
