import numpy as np, soundfile as sf, librosa, json, sys, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
y,sr=sf.read(f'{S}/wav/v12.wav')
segs=[(3.86,4.78,1),(4.79,6.12,2),(6.19,8.00,3),(8.18,8.95,4),(9.00,9.95,5),(10.25,10.60,6),(10.76,11.30,7),(11.41,12.10,8),(12.22,13.25,9),(13.43,13.95,10)]
N=2048;H=256
def stft(x): return librosa.stft(x,n_fft=N,hop_length=H)
rep=[]; fig,axs=plt.subplots(2,len(segs),figsize=(24,6),dpi=90)
for k,(s,e,i) in enumerate(segs):
    pre0=max(s-0.40,0); a=int(pre0*sr); b=int((e+0.05)*sr)
    chunk=y[a:b]; clean=np.zeros_like(chunk)
    npre=int((s-0.03-pre0)*sr/H)
    for c in range(2):
        X=stft(chunk[:,c]); M=np.abs(X)
        prof=np.median(M[:,max(npre-50,1):npre],axis=1,keepdims=True)
        G=np.maximum(1-2.0*prof/(M+1e-9),0.05)
        # smooth gain over time to reduce musical noise
        from scipy.ndimage import uniform_filter
        G=uniform_filter(G,size=(3,5))
        clean[:,c]=librosa.istft(X*G,hop_length=H,length=len(chunk))
    off=int((s-pre0)*sr); x=clean[off:]
    # end: decay on cleaned envelope
    m=x.mean(1); hop=48; n=len(m)//hop
    env=20*np.log10(np.sqrt((m[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
    pk=env.max(); thr=max(-72,pk-40)
    lim=int((e-s)*1000); endi=lim
    for j in range(int(lim*0.3),min(lim+50,n-150)):
        if (env[j:j+150]<thr).all(): endi=j; break
    if i==3: endi=lim
    x=x[:endi*hop].copy()
    fi=int(0.002*sr); fo=int(0.015*sr)
    x[:fi]*=np.linspace(0,1,fi)[:,None]; x[-fo:]*=np.linspace(1,0,fo)[:,None]**2
    g=10**(-1/20)/np.abs(x).max(); x*=g
    fn=f'v12_sfx{i:02d}.wav'; sf.write(f'{out}/{fn}',x,sr,subtype='PCM_16')
    rep.append(dict(file=fn,start=round(s,3),end=round(s+endi/1000,3),dur=round(endi/1000,3),start_how='card+onset',end_how='decay(clean)',gain_db=round(20*np.log10(g),1),note='music bed reduced'))
    for r,sig in enumerate([y[int(s*sr):int((s+endi/1000)*sr)].mean(1),x.mean(1)]):
        D=librosa.amplitude_to_db(np.abs(stft(sig))/512); axs[r,k].imshow(D,origin='lower',aspect='auto',vmin=-90,vmax=0,cmap='magma'); axs[r,k].set_title(f'{i} {"orig" if r==0 else "clean"}',fontsize=8); axs[r,k].set_yticks([]); axs[r,k].set_xticks([])
plt.tight_layout(); plt.savefig(f'{S}/ver/v12_clean.png')
json.dump({'v12':rep},open(f'{S}/cut_report_v12.json','w'),indent=1)
for r in rep: print(r)
