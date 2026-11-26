import numpy as np, soundfile as sf, json, sys, os
HOP=48  # 1 ms at 48k
def env_db(m, sr):
    n=len(m)//HOP
    fr=m[:n*HOP].reshape(n,HOP)
    e=np.sqrt((fr**2).mean(1)+1e-12)
    # 3-frame max smoothing
    e=np.maximum.reduce([e,np.roll(e,1),np.roll(e,-1)])
    return 20*np.log10(e+1e-9)
def snap_start(e, s, win=0.06):
    i0=max(int((s-win)*1000),11); i1=min(int((s+win)*1000),len(e)-6)
    best=None;bv=6.0
    for i in range(i0,i1):
        r=e[i+5]-e[i-10:i].min()
        if r>bv: bv=r;best=i
    if best is None:
        # no clear attack: look for a dip (cut point)
        j=i0+int(np.argmin(e[i0:i1])); return j/1000.0,'dip'
    a=max(best-60,0); seg=e[a:best+1]; mn=seg.min()
    if e[best+5]-mn>=10:
        # latest quiet point before the attack
        thr=mn+0.25*(e[best+5]-mn); idx=np.where(seg<=thr)[0][-1]; j=a+idx
        return max(j-1,0)/1000.0,'onset+%.0fdB'%bv
    lo=e[best-10:best].min(); j=best
    while j>best-12 and e[j-1]>lo+3: j-=1
    return max(j-2,0)/1000.0,'onset+%.0fdB'%bv
def find_end(e, s, ge, nxt):
    peak=e[int(s*1000):int(ge*1000)+1].max()
    thr=max(-72.0,peak-62.0)
    a=int(max(s+0.02,ge-0.25)*1000); b=int(min(ge+0.30,(nxt if nxt else 1e9))*1000); b=min(b,len(e)-41)
    for i in range(a,b):
        if (e[i:i+40]<thr).all():
            # back up to last frame above thr
            return i/1000.0,'decay'
    return b/1000.0,'cap'
def process(spec, wav, outdir, report):
    y,sr=sf.read(wav); m=y.mean(1); e=env_db(m,sr)
    segs=spec['segs']; res=[]
    starts=[]
    for k,sg in enumerate(segs):
        s=sg[0]; mode=sg[3] if len(sg)>3 else ''
        if 'fix' in mode: st,how=s,'fixed'
        else: st,how=snap_start(e,s)
        starts.append((st,how))
    for k,sg in enumerate(segs):
        st,how=starts[k]; ge=sg[1]; name=sg[2]; mode=sg[3] if len(sg)>3 else ''
        nxt=starts[k+1][0] if k+1<len(segs) else None
        if 'fixend' in mode: en,eh=ge,'fixed'
        elif nxt is not None and nxt-ge<0.04: en,eh=nxt,'cut'
        else: en,eh=find_end(e,st,ge,nxt)
        a=int(st*sr); b=int(en*sr); x=y[a:b].copy()
        fi=int(0.002*sr)
        mm=np.abs(x).mean(1); pkl=20*np.log10(mm.max()+1e-9)
        tail=20*np.log10(np.sqrt((mm[-int(0.03*sr):]**2).mean())+1e-9)
        note=''
        if eh=='decay': fo=int(0.012*sr)
        elif tail<pkl-40 or 'keepcut' in mode: fo=int(0.006*sr)
        elif 'fixend' in mode and en>len(m)/sr-0.1: fo=int(0.30*sr); note='coupé par la fin de la vidéo source (fondu 300 ms)'
        else: fo=int(0.12*sr); note='coupé par le montage source (fondu 120 ms)'
        fo=min(fo,len(x)//3); fi=min(fi,len(x)//4)
        x[:fi]*=np.linspace(0,1,fi)[:,None]; x[len(x)-fo:]*=np.linspace(1,0,fo)[:,None]**2
        pk=np.abs(x).max(); g=10**(-1/20)/pk if pk>0 else 1
        x=x*g
        fn=f'{name}.wav'; sf.write(os.path.join(outdir,fn),x,sr,subtype='PCM_16')
        res.append(dict(file=fn,start=round(st,3),end=round(en,3),dur=round(en-st,3),start_how=how,end_how=eh,gain_db=round(20*np.log10(g),1),note=note,tail_db=round(tail-pkl,1)))
    report.extend(res); return res
if __name__=='__main__':
    specs=json.load(open(sys.argv[1])); S=sys.argv[2]; out=sys.argv[3]; os.makedirs(out,exist_ok=True)
    only=sys.argv[4:] 
    allr={}
    for vid,spec in specs.items():
        if only and vid not in only: continue
        rep=[]; process(spec,f'{S}/wav/{vid}.wav',out,rep); allr[vid]=rep
        for r in rep: print(vid,'%-40s %6.3f %6.3f %5.2fs %-14s %-6s %+5.1fdB'%(r['file'],r['start'],r['end'],r['dur'],r['start_how'],r['end_how'],r['gain_db']))
    json.dump(allr,open(os.path.join(S,'cut_report_%s.json'%('_'.join(only) or 'all')),'w'),indent=1)
