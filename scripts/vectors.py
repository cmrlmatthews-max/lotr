# Converts the William & Mary shapefile layers to compact JSON (km coordinates, origin at the south-west corner).
import struct, glob, os, json, math, re
BASE=os.path.expanduser('~/mnt/Middle Earth'); SRC=BASE+'/Vector_Shapefiles'; OUT=BASE+'/Explorer/data'
X0=2527364.22; Y1=3232003.65; WKM=2352.0; HKM=1932.0; Y0=Y1-HKM*1000
def kx(x): return (x-X0)/1000.0
def ky(y): return (y-Y0)/1000.0
def dbf(path):
    f=open(path,'rb'); h=f.read(32); n,hl,rl=struct.unpack('<IHH',h[4:12]); fields=[]
    while True:
        d=f.read(32)
        if d[0]==0x0D: break
        fields.append((d[:11].split(b'\0')[0].decode(),d[16]))
    f.seek(hl); rows=[]
    for i in range(n):
        r=f.read(rl); o=1; row={}
        for nm,l in fields:
            v=r[o:o+l].decode('utf-8','replace').strip(); o+=l
            if v: row[nm]=v
        rows.append(row)
    return rows
def shp(path):
    f=open(path,'rb'); f.seek(100); out=[]
    while True:
        rh=f.read(8)
        if len(rh)<8: break
        _,ln=struct.unpack('>ii',rh); c=f.read(ln*2); st=struct.unpack('<i',c[:4])[0]
        if st==0: out.append(None); continue
        if st in(1,11,21):
            x,y=struct.unpack('<2d',c[4:20]); out.append(('pt',[(kx(x),ky(y))]))
        else:
            npart,npt=struct.unpack('<2i',c[36:44]); parts=struct.unpack('<%di'%npart,c[44:44+4*npart]); o=44+4*npart
            pts=struct.unpack('<%dd'%(2*npt),c[o:o+16*npt]); P=[(kx(pts[2*i]),ky(pts[2*i+1])) for i in range(npt)]
            idx=list(parts)+[npt]; out.append(('poly' if st in(5,15,25) else 'line',[P[idx[i]:idx[i+1]] for i in range(npart)]))
    return out
def dp(pts,tol):
    if len(pts)<3: return pts
    keep=[False]*len(pts); keep[0]=keep[-1]=True; stack=[(0,len(pts)-1)]
    while stack:
        a,b=stack.pop(); ax,ay=pts[a]; bx,by=pts[b]; dx,dy=bx-ax,by-ay; L=math.hypot(dx,dy); md=0; mi=-1
        for i in range(a+1,b):
            px,py=pts[i]
            d=abs((px-ax)*dy-(py-ay)*dx)/L if L>1e-9 else math.hypot(px-ax,py-ay)
            if d>md: md=d; mi=i
        if md>tol: keep[mi]=True; stack.append((a,mi)); stack.append((mi,b))
    return [p for p,k in zip(pts,keep) if k]
def area(r): return 0.5*sum(r[i][0]*r[(i+1)%len(r)][1]-r[(i+1)%len(r)][0]*r[i][1] for i in range(len(r)))
def inside(x,y,r):
    c=False; n=len(r); j=n-1
    for i in range(n):
        xi,yi=r[i]; xj,yj=r[j]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi: c=not c
        j=i
    return c
def dseg(x,y,r):
    m=1e18; n=len(r)
    for i in range(n):
        ax,ay=r[i]; bx,by=r[(i+1)%n]; dx,dy=bx-ax,by-ay; L2=dx*dx+dy*dy
        t=0 if L2==0 else max(0,min(1,((x-ax)*dx+(y-ay)*dy)/L2)); d=math.hypot(x-ax-t*dx,y-ay-t*dy)
        if d<m: m=d
    return m
def polepoint(r):
    r=dp(r,max(0.3,math.sqrt(abs(area(r)))/40)) if len(r)>60 else r
    xs=[p[0] for p in r]; ys=[p[1] for p in r]; best=None; N=28
    for i in range(N):
        for j in range(N):
            x=min(xs)+(i+.5)*(max(xs)-min(xs))/N; y=min(ys)+(j+.5)*(max(ys)-min(ys))/N
            if inside(x,y,r):
                d=dseg(x,y,r)
                if best is None or d>best[0]: best=(d,x,y)
    return (best[1],best[2]) if best else (sum(xs)/len(xs),sum(ys)/len(ys))
def linemid(p):
    L=[0]
    for i in range(1,len(p)): L.append(L[-1]+math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]))
    h=L[-1]/2
    for i in range(1,len(p)):
        if L[i]>=h:
            t=(h-L[i-1])/max(1e-9,L[i]-L[i-1]); return (p[i-1][0]+t*(p[i][0]-p[i-1][0]),p[i-1][1]+t*(p[i][1]-p[i-1][1]))
    return p[0]
def flat(p): 
    o=[]
    for x,y in p: o+= [round(x,1),round(y,1)]
    return o
ORDER=['Towns','Fortresses','Harbors','Buildings','Doors_Gates','Bridges','Fords','Cave_entrances','Falls','Graves_Tombs','Mountains_of_Moria','Mountains','Hills','Forests','Swamps','Lakes','Islands','Bays','Fields','Valleys','Rivers','Roads','Walls','Realms','Place_Boundaries','Frodo_Route']
TOL={'Mountains':0.7,'Bays':0.8,'Realms':0.8,'Place_Boundaries':0.8,'Rivers':0.25,'Roads':0.2,'Frodo_Route':0.25,'Walls':0.02}
KEEP=['Type','Location','Realm','Inhabitant','Owner','Maker','Occupant','Created','Range','Trees','Outflow','Tributary','Comments','English','Westron','Quenya','Sindarin','Khuzdul','Rohirric','Other','Name_1']
feats=[]
for lay in ORDER:
    rows=dbf(f'{SRC}/{lay}.dbf'); geo=shp(f'{SRC}/{lay}.shp'); merged={}
    for i,(r,g) in enumerate(zip(rows,geo)):
        if g is None: continue
        if lay=='Mountains_of_Moria' and r.get('Status')!='Current': continue
        name=r.get('Name') or {'Frodo_Route':"Frodo's route"}.get(lay,'')
        code=r.get('Code') or r.get('Code_1') or f'{lay[:2].upper()}X{i:02d}'
        if lay=='Buildings' and name.startswith('Warning beacons'): code=f'{code}_{i}'
        if lay=='Roads' and (name.lower().startswith('unnamed') or name=='Causeway'): code=f'{code}_{i}' if code.startswith('RD') else code
        key=code
        if key in merged and g[0]=='pt': continue
        if key not in merged:
            merged[key]={'id':code,'layer':lay,'name':name,'kind':g[0],'attrs':{k:r[k] for k in KEEP if k in r},'geom':[]}
        merged[key]['geom']+=g[1]
    for f in merged.values():
        tol=TOL.get(lay,0.35); k=f['kind']
        if k=='pt':
            f['x'],f['y']=f['geom'][0]; f['geom']=None
        elif k=='line':
            parts=[dp(p,tol) for p in f['geom'] if len(p)>1]; parts.sort(key=lambda p:-sum(math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]) for i in range(1,len(p))))
            f['x'],f['y']=linemid(parts[0]); f['geom']=[flat(p) for p in parts]
        else:
            rings=sorted(f['geom'],key=lambda r:-abs(area(r))); big=rings[0]; A=abs(area(big))
            f['x'],f['y']=polepoint(big); f['area']=round(sum(abs(area(r)) for r in rings if area(r)*area(big)>0),1)
            out=[]
            for r in rings:
                if abs(area(r))<max(0.02,A*0.0005) and r is not big: continue
                s=dp(r,min(tol,max(0.01,math.sqrt(abs(area(r)))/25)))
                if len(s)>=4: out.append(flat(s))
            f['geom']=out
        f['x']=round(f['x'],1); f['y']=round(f['y'],1); feats.append(f)
# de-duplicate places that appear in several layers: same name within 25 km -> one card
def norm(n): return re.sub(r'\s*\(.*?\)','',n).strip().lower()
prim={}
for f in feats:
    if not f['name'] or f['layer'] in('Realms','Place_Boundaries','Frodo_Route') or f['name'].lower().startswith('unnamed'): f['card']=None; continue
    hit=None
    for g in prim.get(norm(f['name']),[]):
        if math.hypot(g['x']-f['x'],g['y']-f['y'])<25 or (f['layer']==g['layer'] and f['kind']!='pt'): hit=g; break
    if hit: f['card']=hit['id']; hit.setdefault('also',[]).append(f['layer'])
    else: f['card']=f['id']; prim.setdefault(norm(f['name']),[]).append(f)
ids=[f['id'] for f in feats]; assert len(ids)==len(set(ids)),[i for i in ids if ids.count(i)>1]
json.dump({'wkm':WKM,'hkm':HKM,'features':feats},open(OUT+'/vectors.json','w'),ensure_ascii=False,separators=(',',':'))
gaz=[{k:f[k] for k in('id','layer','name','x','y','attrs') if k in f}|({'also':f['also']} if 'also' in f else {})|({'area_km2':f['area']} if 'area' in f else {}) for f in feats if f.get('card')==f['id']]
json.dump(gaz,open(OUT+'/gazetteer.json','w'),ensure_ascii=False,indent=0)
print('features',len(feats),'cards',len(gaz),'vectors.json',os.path.getsize(OUT+'/vectors.json'),'gaz',os.path.getsize(OUT+'/gazetteer.json'))
from collections import Counter; print(Counter(g['layer'] for g in gaz))
for n in ['Hobbiton','Minas Tirith','Rivendell','Edoras','Lonely Mountain','Mount Doom','Misty Mountains','Anduin','Mirkwood']:
    print(n,[(g['id'],g['layer'],g['x'],g['y']) for g in gaz if g['name']==n])
