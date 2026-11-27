import soundfile as sf, numpy as np, glob, sys, os
bad=0; rows=[]
for f in sorted(glob.glob(sys.argv[1]+'/*/*.wav')):
    y,sr=sf.read(f); i=sf.info(f); m=np.abs(y).max(1)
    pk=20*np.log10(np.abs(y).max()); clip=(np.abs(y)>0.999).sum()
    s0=np.abs(y[0]).max(); s1=np.abs(y[-1]).max()
    hop=48; n=len(y)//hop; e=20*np.log10(np.sqrt((y.mean(1)[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
    lead=int(np.argmax(e>e.max()-40))  # ms of leading near-silence
    dc=abs(y.mean())
    issues=[]
    if not (-1.2<pk<-0.8): issues.append('peak %.2f'%pk)
    if clip: issues.append('clip %d'%clip)
    if s0>0.01 or s1>0.01: issues.append('edge %.3f/%.3f'%(s0,s1))
    if lead>40: issues.append('lead %dms'%lead)
    if dc>0.01: issues.append('dc %.3f'%dc)
    if i.samplerate!=48000 or i.channels!=2 or i.subtype!='PCM_16': issues.append('fmt')
    if np.isnan(y).any(): issues.append('nan')
    if issues: bad+=1; print(os.path.relpath(f,sys.argv[1]),'%.2fs'%i.duration,issues)
print('files with issues:',bad)
