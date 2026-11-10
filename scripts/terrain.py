# Mosaics the four 50 m quads to a 2 km height map and a 600 m parchment relief image.
import rasterio, numpy as np, os, glob
from rasterio.merge import merge
from rasterio.enums import Resampling
from PIL import Image, ImageFilter
BASE=os.path.expanduser('~/mnt/Middle Earth'); OUT=BASE+'/Explorer/data'
X0=2527364.22; Y1=3232003.65; W=2352000; H=1932000
bounds=(X0,Y1-H,X0+W,Y1)
srcs=[rasterio.open(p) for p in sorted(glob.glob(BASE+'/Quad*/DEM_50m_Quad*.tif'))]
def mos(res):
    a,t=merge(srcs,bounds=bounds,res=res,nodata=-999,resampling=Resampling.average); return a[0]
def blur(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),np.float32)/255
def unmapped(land):
    # The data set stops at straight lines in the east, north and south-east. Nodata beyond them is unmapped land, not sea.
    hh,ww=land.shape; rows=np.arange(hh); cols=np.arange(ww)
    rsel=[r for r in range(int(hh*.08),int(hh*.97),5) if land[r].any()]
    pe=np.polyfit(rsel,[np.nonzero(land[r])[0].max() for r in rsel],1)
    csel=[c for c in range(int(ww*.33),int(ww*.80),5)]
    pn=np.polyfit(csel,[np.nonzero(land[:,c])[0].min() for c in csel],1)
    csel=[c for c in range(int(ww*.56),int(ww*.97),5)]
    ps=np.polyfit(csel,[np.nonzero(land[:,c])[0].max() for c in csel],1)
    R,C=np.mgrid[0:hh,0:ww]
    u=(C>np.polyval(pe,R)-2)|(R<np.polyval(pn,C)+2)|((R>np.polyval(ps,C)-2)&(C>ww*.47))
    return u&~land
lo=mos(2000); land=lo>-900; un=unmapped(land)
fade=np.clip(1-blur(un,9)*2.0,0,1)
h=np.where(land,np.clip(lo,2,4000),0)*fade
v=np.round(h/4000*65535).astype(np.uint16)
Image.fromarray(np.dstack([(v>>8).astype(np.uint8),(v&255).astype(np.uint8),np.where(land,255,np.where(un,128,0)).astype(np.uint8)]),'RGB').save(OUT+'/height.png',optimize=True)
hi=mos(600); hh,ww=hi.shape
land=hi>-900; un=unmapped(land); ufade=np.clip(blur(un,30)*2.0,0,1)
h=np.where(land,np.clip(hi,2,4000),0).astype(np.float32)
rng=np.random.default_rng(7)
def noise(scale,amp):
    small=rng.random((max(2,hh//scale),max(2,ww//scale))).astype(np.float32)
    return (np.asarray(Image.fromarray(small).resize((ww,hh),Image.BICUBIC))-0.5)*amp
z=5.5
dzdx=np.zeros_like(h); dzdy=np.zeros_like(h)
dzdx[:,1:-1]=(h[:,2:]-h[:,:-2])/1200.0; dzdy[1:-1,:]=(h[:-2,:]-h[2:,:])/1200.0
nx=-z*dzdx; ny=-z*dzdy; nn=np.sqrt(nx*nx+ny*ny+1)
rel=(nx*-0.5+ny*0.5+0.7071)/nn/0.7071
slope=np.sqrt(dzdx*dzdx+dzdy*dzdy)
mult=np.clip(0.30+0.70*rel,0.42,1.16)*(1-0.22*np.clip(slope*9,0,1))
t=np.clip(h/2600,0,1)[...,None]
lowc=np.array([226,213,170],np.float32); midc=np.array([214,192,148],np.float32); topc=np.array([238,229,208],np.float32)
col=np.where(t<0.5,lowc+(midc-lowc)*(t*2),midc+(topc-midc)*((t-0.5)*2))*mult[...,None]
band=np.floor(h/400); edge=np.zeros_like(land)
edge[:,1:]|=band[:,1:]!=band[:,:-1]; edge[1:,:]|=band[1:,:]!=band[:-1,:]
col=np.where((edge&land)[...,None],col*0.90,col)
wet=land|un
b1=blur(wet,7); b2=blur(wet,26)
sea=np.array([194,204,190],np.float32)*(1-0.10*b2[...,None])-np.array([14,10,6],np.float32)*b1[...,None]
q=np.floor(np.power(np.clip(b1,0,1),0.6)*7); we=np.zeros_like(land)
we[:,1:]|=q[:,1:]!=q[:,:-1]; we[1:,:]|=q[1:,:]!=q[:-1,:]
sea=np.where((we&(b1>0.03))[...,None],sea*0.80,sea)
img=np.where(land[...,None],col,sea)
ce=np.zeros_like(land); ce[:,1:]|=land[:,1:]!=land[:,:-1]; ce[1:,:]|=land[1:,:]!=land[:-1,:]; ce[:,:-1]|=land[:,1:]!=land[:,:-1]
img=np.where((ce&(ufade<0.02))[...,None],np.array([84,62,40],np.float32),img)
paper=np.array([224,210,168],np.float32)
img=img*(1-ufade[...,None])+paper*ufade[...,None]
img=img*(1+noise(260,0.10)+noise(60,0.05))[...,None]
yy,xx=np.mgrid[0:hh,0:ww].astype(np.float32); e=np.minimum(np.minimum(xx,ww-1-xx),np.minimum(yy,hh-1-yy))/ww
burn=np.clip(1-(e+noise(90,0.012))/0.022,0,1)**1.5*0.6
img=img*(1-burn[...,None])+np.array([92,66,40],np.float32)*burn[...,None]
out=Image.fromarray(np.clip(img,0,255).astype(np.uint8),'RGB')
out.save(OUT+'/base.jpg',quality=84,optimize=True,subsampling=1)
out.resize((1400,int(1400*hh/ww)),Image.LANCZOS).save(OUT+'/preview.jpg',quality=80)
for f in ['height.png','base.jpg','preview.jpg']: print(f,os.path.getsize(OUT+'/'+f))
