import cv2, numpy as np, sys, json
path,out=sys.argv[1],sys.argv[2]
cap=cv2.VideoCapture(path); fps=cap.get(cv2.CAP_PROP_FPS)
F=[]
while True:
    ok,f=cap.read()
    if not ok: break
    F.append(f)
F=np.array(F); n,H,W,_=F.shape
hsv=np.array([cv2.cvtColor(f,cv2.COLOR_BGR2HSV) for f in F[::3]])
blue=((hsv[...,0]>95)&(hsv[...,0]<118)&(hsv[...,1]>120)&(hsv[...,2]>150))
# playhead = narrow column with consistently high blue over many rows
cc=blue.mean(axis=(0,1)); cc2=cc-0.5*(np.roll(cc,6)+np.roll(cc,-6))
px=int(np.argmax(cc2))
rowp=blue[:,:,max(px-1,0):px+2].mean(axis=(0,2))
ys=np.where(rowp>0.4)[0]
y0,y1=(max(ys.min()-10,0),min(ys.max()+10,H)) if len(ys) else (0,H)
if len(sys.argv)>3: px,y0,y1=map(int,sys.argv[3:6])
info=dict(fps=fps,n=n,W=W,H=H,px=px,y0=int(y0),y1=int(y1))
G=[]
for f in F:
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)[y0:y1].astype(np.float32)
    g=np.abs(cv2.Sobel(g,cv2.CV_32F,1,0,ksize=3)); g[:,max(px-8,0):px+9]=0; G.append(g)
win=cv2.createHanningWindow((W,y1-y0),cv2.CV_32F)
dx=[];resp=[]
for a,b in zip(G[:-1],G[1:]):
    (sx,sy),r=cv2.phaseCorrelate(a,b,win); dx.append(sx); resp.append(r)
dx=-np.array(dx); resp=np.array(resp)
# robust clean: median filter 5
from scipy.ndimage import median_filter
dxs=median_filter(dx,5,mode='nearest')
bad=np.abs(dx-dxs)>1.0
dx[bad]=dxs[bad]
cum=np.concatenate([[0],np.cumsum(dx)])  # content scrolled at frame i
t=np.arange(n)/fps
info.update(dx_med=float(np.median(dx)),dx_min=float(dx.min()),dx_max=float(dx.max()),nbad=int(bad.sum()))
o=10
# content coordinate X (px relative to playhead at t=0): screen x in frame i shows X = x-px+cum[i]
X0=int(np.ceil(o+cum[0])); X1=int(np.floor(o+cum[-1]))
cols=[];times=[]
for X in range(X0,X1):
    i=int(np.searchsorted(cum,X-o,side='right')-1); i=min(max(i,0),n-1)
    x=int(round(px+X-cum[i]))
    x=min(max(x,0),W-1)
    cols.append(F[i,y0:y1,x])
    times.append(float(np.interp(X,cum,t)))  # time when content X hits the playhead
P=np.stack(cols,axis=1)
cv2.imwrite(out+'.png',P); np.save(out+'_t.npy',np.array(times)); np.save(out+'_dx.npy',dx)
info['ncols']=P.shape[1]; info['tmin']=times[0]; info['tmax']=times[-1]
json.dump(info,open(out+'.json','w')); print(json.dumps(info))
