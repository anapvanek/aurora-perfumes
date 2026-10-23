function arreglarFotos() {
  const ss = SpreadsheetApp.getActive();
  ss.getSheets().forEach(sh => {
    sh.getImages().forEach(img => {
      const a = img.getAnchorCell();
      let row = a.getRow();
      const col = a.getColumn();
      // fila donde está el centro de la foto
      let y = img.getAnchorCellYOffset() + img.getHeight() / 2;
      while (y > sh.getRowHeight(row) && row < sh.getMaxRows()) { y -= sh.getRowHeight(row); row++; }
      // achicar para que entre en la celda, sin deformar
      const rh = sh.getRowHeight(row), cw = sh.getColumnWidth(col);
      const k = Math.min((rh - 6) / img.getHeight(), (cw - 6) / img.getWidth());
      const w = Math.round(img.getWidth() * k), h = Math.round(img.getHeight() * k);
      img.setWidth(w).setHeight(h)
         .setAnchorCell(sh.getRange(row, col))
         .setAnchorCellXOffset(Math.round((cw - w) / 2))
         .setAnchorCellYOffset(Math.round((rh - h) / 2));
    });
  });
}
