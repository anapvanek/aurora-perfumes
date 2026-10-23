function ponerFotos() {
  const SITIO = "https://aurora-perfumes.tiendamendoza.workers.dev/";
  const FOTOS = JSON.parse(UrlFetchApp.fetch(SITIO + "fotos-planilla.json").getContentText());
  const ss = SpreadsheetApp.getActive(), faltan = [];
  Object.keys(FOTOS).forEach(tab => {
    const sh = ss.getSheetByName(tab);
    if (!sh) return;
    sh.getImages().forEach(img => img.remove());
    const vals = sh.getRange(2, 1, sh.getLastRow() - 1, 4).getValues();
    let marca = "";
    const pedidos = [], destinos = [];
    vals.forEach((r, i) => {
      if (r[0]) marca = String(r[0]).trim();
      const nombre = String(r[3]).trim().replace(/\s+\d+\s*ML$/i, "");
      if (!nombre) return;
      const f = FOTOS[tab][marca + "|" + nombre];
      if (!f) { faltan.push(tab + ": " + marca + " " + nombre); return; }
      [0, 1].forEach(k => {
        if (f[k]) { pedidos.push({url: SITIO + "img/" + f[k] + ".jpg", muteHttpExceptions: true}); destinos.push([i + 2, k + 2]); }
      });
    });
    UrlFetchApp.fetchAll(pedidos).forEach((res, j) => {
      const [row, col] = destinos[j];
      if (res.getResponseCode() !== 200) { faltan.push(tab + ": fila " + row + " sin foto"); return; }
      const img = sh.insertImage(res.getBlob(), col, row);
      const rh = sh.getRowHeight(row), cw = sh.getColumnWidth(col);
      const k = Math.min((rh - 6) / img.getHeight(), (cw - 6) / img.getWidth());
      const w = Math.round(img.getWidth() * k), h = Math.round(img.getHeight() * k);
      img.setWidth(w).setHeight(h)
         .setAnchorCellXOffset(Math.round((cw - w) / 2))
         .setAnchorCellYOffset(Math.round((rh - h) / 2));
    });
  });
  Logger.log(faltan.length ? "Revisar:\n" + faltan.join("\n") : "Listo, todas las fotos puestas.");
}
