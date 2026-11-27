import numpy as np, cv2, soundfile as sf, librosa, sys, json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S=sys.argv[1]; vid=sys.argv[2]; ta=float(sys.argv[3]); tb=float(sys.argv[4]); out=sys.argv[5]
marks=json.loads(sys.argv[6]) if len(sys.argv)>6 else []
y,sr=sf.read(f'{S}/wav/{vid}.wav'); m=y.mean(1)
pp=f'{S}/pano/{vid}.png'
has=os.path.exists(pp)
fig,axs=plt.subplots(3 if has else 2,1,figsize=(20,9 if has else 6),sharex=True,gridspec_kw=dict(height_ratios=[1.3,1.2,0.6] if has else [1.2,0.6]),dpi=100)
k=0
if has:
    P=cv2.cvtColor(cv2.imread(pp),cv2.COLOR_BGR2RGB); T=np.load(f'{S}/pano/{vid}_t.npy')
    axs[0].imshow(P,aspect='auto',extent=[T[0],T[-1],P.shape[0],0],interpolation='bilinear'); axs[0].set_yticks([]); k=1
seg=m[int(ta*sr):int(tb*sr)]
D=librosa.amplitude_to_db(np.abs(librosa.stft(seg,n_fft=2048,hop_length=256))/512,ref=1.0)
fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
axs[k].pcolormesh(ta+np.arange(D.shape[1])*256/sr,fr,D,vmin=-90,vmax=0,cmap='magma',shading='auto'); axs[k].set_yscale('symlog',linthresh=200); axs[k].set_ylim(40,20000)
hop=240; rms=librosa.feature.rms(y=seg,frame_length=960,hop_length=hop)[0]
axs[k+1].plot(ta+np.arange(len(rms))*hop/sr,20*np.log10(rms+1e-9),lw=0.7); axs[k+1].set_ylim(-80,0); axs[k+1].grid(alpha=.3)
on=librosa.onset.onset_detect(y=seg,sr=sr,hop_length=128,backtrack=True,units='time',delta=0.12,wait=4)+ta
for o in on:
    axs[k+1].axvline(o,color='r',lw=0.6,alpha=.7); axs[k+1].text(o,-2,'%.2f'%o,fontsize=7,rotation=90,va='top',color='r')
print('onsets',' '.join('%.3f'%o for o in on))
for mk in marks:
    for a in axs: a.axvline(mk,color='cyan',lw=0.8,alpha=0.8)
axs[-1].set_xlim(ta,tb); axs[-1].set_xticks(np.arange(np.ceil(ta*4)/4,tb,0.25),minor=True); axs[-1].set_xticks(np.arange(np.ceil(ta),tb,0.5))
for a in axs: a.grid(axis='x',which='both',alpha=0.25,color='w' if a is not axs[-1] else 'k')
plt.tight_layout(); plt.savefig(out); print('ok')
