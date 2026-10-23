"""Arma site/index.html a partir de src/template.html + src/data.js.
Las fotos viven en site/img/ (nombre = clave usada en data.js).
Uso: python3 src/build.py"""
import json,os,re,shutil
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(R,'src');SITE=os.path.join(R,'site')
URL="https://aurora-perfumes.tiendamendoza.workers.dev/"
data=open(os.path.join(SRC,'data.js'),encoding='utf8').read()
ph={f[:-4]:'img/'+f for f in sorted(os.listdir(os.path.join(SITE,'img'))) if f.endswith('.jpg')}
# Fotos de árabes originales: producto sobre fondo blanco -> se muestran enteras (contain)
m=re.search(r'const DATA=(\[.*?\n\]);',data,re.S)
contain=sorted({k for b,its in json.loads(m.group(1)) for it in its for k in it[4]})
s=open(os.path.join(SRC,'template.html'),encoding='utf8').read()
s=s.replace('{{DATA}}',data).replace('{{PHOTOS}}',json.dumps(ph)).replace('{{CONTAIN}}',json.dumps(contain)).replace('{{SITE}}',URL)
open(os.path.join(SITE,'index.html'),'w',encoding='utf8').write(s)
shutil.copy(os.path.join(SRC,'og.jpg'),os.path.join(SITE,'og.jpg'))
missing=[k for k in re.findall(r'"((?:ext|tub|hog)-[\w-]+)"',data) if k not in ph]
print(f"site/index.html: {len(s)//1024} KB, {len(ph)} fotos", "| FALTAN: "+", ".join(sorted(set(missing))) if missing else "")
# Mapa de fotos para la planilla (lo usa tools/ponerFotos.gs): "MARCA|NOMBRE" -> [foto, ficha]
def _arr(name):
    return json.loads(re.search(r'const '+name+r'=(\[.*?\]);\s*\n',data,re.S).group(1))
def _par(p):
    a=[x for x in p if not x.startswith('fic-')];f=[x for x in p if x.startswith('fic-')]
    return [a[0] if a else '', f[0] if f else (a[1] if len(a)>1 else '')]
fotos={"ÁRABES ORIGINALES":{f"{b}|{it[0]}":_par(it[4]) for b,its in json.loads(m.group(1)) for it in its},
       "TUBITOS ÁRABES 35ML":{f"{b}|{it[0]}":_par(it[1]) for b,its in _arr('TUB') for it in its},
       "EXTRACTOS 60ML":{f"{b}|{it[0]}":_par(it[2]) for b,its in _arr('EXT') for it in its}}
json.dump(fotos,open(os.path.join(SITE,'fotos-planilla.json'),'w',encoding='utf8'),ensure_ascii=False)
# Hogar y auto: una foto general por pestaña, en la primera fila (columnas FOTO y FOTO 2)
_h=json.loads(re.search(r'const HMETA=(\{.*?\});\s*\n',data,re.S).group(1))
for k,tab in [("PERFUMINAS TEXTILES","PERFUMINAS TEXTILES 250ML"),("DIFUSORES DE AMBIENTE","DIFUSORES DE AMBIENTE 125ML"),("DIFUSORES PARA AUTO","DIFUSORES PARA AUTO 10ML")]:
    if k in _h: fotos[tab]={"_fila2":(_h[k]['ph']+['',''])[:2]}
json.dump(fotos,open(os.path.join(SITE,'fotos-planilla.json'),'w',encoding='utf8'),ensure_ascii=False)
