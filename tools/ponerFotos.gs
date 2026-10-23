function ponerFotos() {
  const SITIO = "https://aurora-perfumes.tiendamendoza.workers.dev/";
  const FOTOS = JSON.parse(UrlFetchApp.fetch(SITIO + "fotos-planilla.json").getContentText());
  const ss = SpreadsheetApp.getActive(), props = PropertiesService.getScriptProperties();
  const inicio = Date.now(), tabs = Object.keys(FOTOS), faltan = [];
  let est = JSON.parse(props.getProperty("estado") || '{"t":0,"j":0}');
  for (let t = est.t; t < tabs.length; t++) {
    const tab = tabs[t], sh = ss.getSheetByName(tab);
    if (!sh) continue;
    const tareas = [];
    if (FOTOS[tab]._fila2) {
      FOTOS[tab]._fila2.forEach((f, k) => { if (f) tareas.push([2, k + 1, f]); });
    } else {
      const vals = sh.getRange(2, 1, sh.getLastRow() - 1, 4).getValues();
      let marca = "";
      vals.forEach((r, i) => {
        if (r[0]) marca = String(r[0]).trim();
        const nombre = String(r[3]).trim().replace(/\s+\d+\s*ML$/i, "");
        if (!nombre) return;
        const f = FOTOS[tab][marca + "|" + nombre];
        if (!f) { faltan.push(tab + ": " + marca + " " + nombre); return; }
        [0, 1].forEach(k => { if (f[k]) tareas.push([i + 2, k + 2, f[k]]); });
      });
    }
    let j = (t === est.t) ? est.j : 0;
    if (j === 0) sh.getImages().forEach(img => img.remove());
    while (j < tareas.length) {
      if (Date.now() - inicio > 270000) {
        props.setProperty("estado", JSON.stringify({t: t, j: j}));
        Logger.log("Todavía faltan fotos (va por " + tab + "). Tocá ▶ Ejecutar otra vez para seguir.");
        return;
      }
      const lote = tareas.slice(j, j + 15);
      const resp = UrlFetchApp.fetchAll(lote.map(x => ({url: SITIO + "img/" + x[2] + ".jpg", muteHttpExceptions: true})));
      resp.forEach((res, n) => {
        const [row, col] = lote[n];
        if (res.getResponseCode() !== 200) { faltan.push(tab + ": fila " + row + " sin foto"); return; }
        const img = sh.insertImage(res.getBlob(), col, row);
        const rh = sh.getRowHeight(row), cw = sh.getColumnWidth(col);
        const k = Math.min((rh - 6) / img.getHeight(), (cw - 6) / img.getWidth());
        const w = Math.round(img.getWidth() * k), h = Math.round(img.getHeight() * k);
        img.setWidth(w).setHeight(h)
           .setAnchorCellXOffset(Math.round((cw - w) / 2))
           .setAnchorCellYOffset(Math.round((rh - h) / 2));
      });
      j += lote.length;
    }
  }
  props.deleteProperty("estado");
  Logger.log(faltan.length ? "Listo. Revisar:\n" + faltan.join("\n") : "Listo, todas las fotos puestas.");
}
