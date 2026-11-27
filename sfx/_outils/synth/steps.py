# détecte les chutes brutales de niveau (> 18 dB en 5 ms) hors silence
import soundfile as sf, numpy as np, json, sys
d=sys.argv[1]; M=json.load(open(d+'/_meta.json'))
for m in M:
    y,sr=sf.read(d+'/'+m['tmp']); a=y.mean(1); hop=48; n=len(a)//hop
    e=20*np.log10(np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1))+1e-9); e-=e.max()
    drops=[i for i in range(5,n-5) if e[i-5]>-35 and e[i-5]-e[i+5]>18 and e[i+5:i+40].max()<e[i-5]-12]
    if drops: print('%-24s drops at %s'%(m['fx'],[round(i/1000,3) for i in drops[:4]]))
