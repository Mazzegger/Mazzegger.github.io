import numpy as np, soundfile as sf, glob, os, sys, librosa
from scipy.signal import fftconvolve
fs=sorted(glob.glob(sys.argv[1]+'/*.wav'))
X={}
for f in fs:
    y,sr=sf.read(f); m=librosa.resample(y.mean(1),orig_sr=sr,target_sr=8000)
    X[os.path.basename(f)]=m/np.sqrt((m**2).sum()+1e-12)
names=list(X); res=[]
for i,a in enumerate(names):
    for b in names[i+1:]:
        A,B=X[a],X[b]
        # normalized xcorr against the shorter; use local energy normalization on the longer
        if len(A)>len(B): A,B=B,A; aa,bb=b,a
        else: aa,bb=a,b
        c=fftconvolve(B,A[::-1],mode='valid') if len(B)>=len(A) else None
        # local energy of B windows
        e=np.sqrt(np.convolve(B**2,np.ones(len(A)),mode='valid')+1e-12)
        r=np.max(np.abs(c)/e)
        if r>0.6: res.append((r,aa,len(A)/8000,bb,len(B)/8000))
for r in sorted(res,reverse=True): print('%.3f  %-42s (%.2fs) in %-42s (%.2fs)'%tuple(r))
