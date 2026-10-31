import json,re,sys
F=sys.argv[1];d=json.load(open(F))
s=open('/home/claude/aurora-perfumes/src/data.js').read()
J=lambda n,o='[':json.loads(re.search(r'const '+n+r'=('+re.escape(o)+r'.*?'+(r'\]' if o=='[' else r'\}')+r');\s*(//[^\n]*)?\n',s,re.S).group(1))
DATA=json.loads(re.search(r'const DATA=(\[.*?\n\]);',s,re.S).group(1))
EXT,TUB,HOG,OUT_A,OUT_T,SOON_A=J('EXT'),J('TUB'),J('HOG'),J('OUT_A'),J('OUT_T'),J('SOON_A');HMETA=J('HMETA','{')
def rows(title):
  sh=[x for x in d['sheets'] if x['properties']['title']==title][0]
  return [[c.get('formattedValue','') for c in r.get('values',[])]+['']*10 for r in sh['data'][0].get('rowData',[])]
num=lambda t:int(re.sub(r'[^\d]','',t.split('.')[0] if re.search(r'\.\d\d$',t) else t) or 0)
did=lambda u:(re.search(r'/d/([\w-]+)',u) or re.search(r'id=([\w-]+)',u) or [None,None])[1] if u else None
out=[]
# ÁRABES
R=rows('ÁRABES ORIGINALES');b='';seen=set()
web={(B,it[0]):it for B,its in DATA for it in its}
for r in R[1:]:
  if r[0].strip():b=r[0].strip()
  if not r[3].strip():continue
  m=re.match(r'(.*?)\s+(\d+)\s*ML$',r[3].strip(),re.I);n,ml=(m.group(1),int(m.group(2))) if m else (r[3].strip(),None)
  st=r[6].strip().upper();k=(b,n);seen.add(k)
  if k not in web:out.append(f"A NUEVO {b} {n} {ml} {r[4]} {r[5]} {st} foto={did(r[1])}");continue
  it=web[k];pm,pM=num(r[4]),num(r[5])
  if (pm,pM)!=(it[2],it[3]):out.append(f"A PRECIO {b} {n}: {it[2]}/{it[3]} -> {pm}/{pM}")
  if ml and ml!=it[1]:out.append(f"A ML {b} {n}: {it[1]} -> {ml}")
  cur='PRÓXIMAMENTE' if n in SOON_A else 'NO' if n in OUT_A else 'SI'
  if st!=cur:out.append(f"A STOCK {b} {n}: {cur} -> {st}")
for k in web:
  if k not in seen:out.append(f"A BORRADO {k}")
# EXTRACTOS
R=rows('EXTRACTOS 60ML');b='';seen=set();web={(B,it[0]):it for B,its in EXT for it in its}
for r in R[1:]:
  if r[0].strip():b=r[0].strip()
  n=r[3].strip()
  if not n:continue
  st=r[6].strip().upper();k=(b,n);seen.add(k)
  if k not in web:out.append(f"E NUEVO {b} {n} {st} foto={did(r[1])}");continue
  it=web[k];cur='SI' if it[1] else 'NO'
  if st!=cur:out.append(f"E STOCK {b} {n}: {cur} -> {st}")
  i=did(r[1])
  if i and not any(i in x for x in it[2]):out.append(f"E FOTO {b} {n}: {i} no está ({it[2]})")
for k in web:
  if k not in seen:out.append(f"E BORRADO {k}")
print('E tiers:',[(r[8],r[9]) for r in R[:8]])
# TUBITOS
R=rows('TUBITOS ÁRABES 35ML');b='';seen=set();web={(B,it[0]):it for B,its in TUB for it in its}
for r in R[1:]:
  if r[0].strip():b=r[0].strip()
  n=re.sub(r'\s+35\s*ML$','',r[3].strip(),flags=re.I)
  if not n:continue
  st=r[6].strip().upper();k=(b,n);seen.add(k)
  if k not in web:out.append(f"T NUEVO {b} {n} {st} foto={did(r[1])}");continue
  cur='NO' if n in OUT_T else 'SI'
  if st!=cur:out.append(f"T STOCK {b} {n}: {cur} -> {st}")
  i=did(r[1]);it=web[k]
  if i and not any(i in x for x in it[1]):out.append(f"T FOTO {b} {n}: {i} no está ({it[1]})")
  if r[4].strip() and num(r[4])!=4000:out.append(f"T PRECIO {n}: {r[4]}")
for k in web:
  if k not in seen:out.append(f"T BORRADO {k}")
print('T tiers:',[(r[8],r[9]) for r in R[:8]])
# HOGAR
for tab,cat in [("PERFUMINAS TEXTILES 250ML","PERFUMINAS TEXTILES"),("DIFUSORES DE AMBIENTE 125ML","DIFUSORES DE AMBIENTE"),("DIFUSORES PARA AUTO 10ML","DIFUSORES PARA AUTO")]:
  R=rows(tab);web=dict(dict(HOG)[cat]);M=HMETA[cat];seen=set()
  for r in R[1:]:
    n=r[2].strip()
    if not n:continue
    seen.add(n);st=r[5].strip().upper()
    if n not in web:out.append(f"H NUEVO {cat} {n} {r[3]} {r[4]} {st}");continue
    if st!=('SI' if web[n] else 'NO'):out.append(f"H STOCK {cat} {n}: -> {st}")
    if r[3].strip() and (num(r[3]),num(r[4]))!=(M['pm'],M['pM']):out.append(f"H PRECIO {cat} {n}: {M['pm']}/{M['pM']} -> {r[3]}/{r[4]}")
  for n in web:
    if n not in seen:out.append(f"H BORRADO {cat} {n}")
print('\n'.join(out) or 'SIN CAMBIOS')
