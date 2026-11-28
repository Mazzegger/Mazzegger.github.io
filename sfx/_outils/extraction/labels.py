import cv2, numpy as np, sys
path,y0,y1,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
cap=cv2.VideoCapture(path); fps=cap.get(cv2.CAP_PROP_FPS); L=[]
while True:
    ok,f=cap.read()
    if not ok: break
    L.append(cv2.cvtColor(f[y0:y1,120:600],cv2.COLOR_BGR2GRAY))
L=np.array(L).astype(np.float32)
d=np.abs(np.diff(L,axis=0)).mean(axis=(1,2))
ch=[0]+[i+1 for i in np.where(d>float(sys.argv[5]))[0]]
# group consecutive change frames
starts=[]
for c in ch:
    if not starts or c-starts[-1]>3: starts.append(c)
crops=[]
for k,s in enumerate(starts):
    e=starts[k+1] if k+1<len(starts) else len(L)
    mid=(s+e)//2
    print('%d  %.3f-%.3f'%(k,s/fps,e/fps))
    im=cv2.cvtColor(L[mid].astype(np.uint8),cv2.COLOR_GRAY2BGR); cv2.putText(im,'%d %.2f'%(k,s/fps),(2,14),0,0.45,(0,0,255),1); crops.append(im)
cv2.imwrite(out,np.vstack(crops))
