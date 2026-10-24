// Reseñas de la página. Se publica como "App web" (Implementar → Nueva implementación).
// Cada reseña nueva cae en la pestaña RESEÑAS con PUBLICAR = NO. Poné SI para que aparezca en la página.
const HOJA_RESENAS = "RESEÑAS";

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents || "{}");
    if (d.web) return salida_({ok: true});  // trampa para robots
    const limpio = (t, n) => { t = String(t || "").replace(/\s+/g, " ").trim().slice(0, n); return /^[=+\-@]/.test(t) ? "'" + t : t; };
    const nombre = limpio(d.nombre, 40), comentario = limpio(d.comentario, 600);
    const estrellas = Math.max(1, Math.min(5, parseInt(d.estrellas, 10) || 0));
    if (!nombre || comentario.length < 5 || !d.estrellas) return salida_({ok: false});
    const sh = SpreadsheetApp.getActive().getSheetByName(HOJA_RESENAS);
    sh.appendRow([new Date(), nombre, estrellas, comentario, "NO"]);
    try {
      MailApp.sendEmail(Session.getEffectiveUser().getEmail(), "Nueva reseña en la página: " + "★".repeat(estrellas),
        nombre + " escribió:\n\n" + comentario + "\n\nPara publicarla, en la planilla andá a la pestaña RESEÑAS y poné SI en PUBLICAR.\n" + SpreadsheetApp.getActive().getUrl());
    } catch (err) {}
    return salida_({ok: true});
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  const sh = SpreadsheetApp.getActive().getSheetByName(HOJA_RESENAS);
  const filas = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, 5).getValues() : [];
  const r = filas.filter(x => String(x[4]).trim().toUpperCase() === "SI" && x[1] && x[3])
    .map(x => ({f: x[0] instanceof Date ? Utilities.formatDate(x[0], "America/Argentina/Mendoza", "yyyy-MM-dd") : "",
                n: String(x[1]), e: Number(x[2]) || 5, c: String(x[3])}))
    .reverse();
  return salida_(r);
}

function salida_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
