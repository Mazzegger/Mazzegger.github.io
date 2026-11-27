import soundfile as sf, numpy as np, json, sys
from scipy.signal import butter, sosfiltfilt
D=sys.argv[1]; C=json.load(open(f'{D}/catalogue.json'))
for e in C['sounds']:
    p=f'{D}/{e["file"]}'; y,sr=sf.read(p); changed=[]
    if abs(y.mean())>0.005:
        y=sosfiltfilt(butter(2,8,'hp',fs=sr,output='sos'),y,axis=0); changed.append('dc')
    hop=48; n=len(y)//hop; env=20*np.log10(np.sqrt((y.mean(1)[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
    first=int(np.argmax(env>env.max()-50))
    if first>25:
        cut=(first-5)*hop; y=y[cut:].copy(); fi=int(0.003*sr); y[:fi]*=np.linspace(0,1,fi)[:,None]
        e['source']['start_s']=round(e['source']['start_s']+cut/sr,3); changed.append('trim %dms'%(cut/48))
    if changed:
        y*=10**(-1/20)/np.abs(y).max(); sf.write(p,y,sr,subtype='PCM_16')
        e['duration_s']=round(len(y)/sr,3); print(e['file'],changed)
json.dump(C,open(f'{D}/catalogue.json','w'),ensure_ascii=False,indent=1)
