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
