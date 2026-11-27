import sys, os, json, time, re, traceback
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, soundfile as sf
from families import S
from motionsynth import finalize, SR
ucs = {r['catid']: r for r in json.load(open(sys.argv[1]))}
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
only = sys.argv[3:]
bad = [s['catid'] for s in S if s['catid'] not in ucs]
print('specs', len(S), 'invalid catids', bad)
names = [s['fx'] for s in S]; dup = {x for x in names if names.count(x) > 1}
print('dup fx', dup, 'too long', [x for x in names if len(x) > 25], 'underscore', [x for x in names if '_' in x])
meta = []
for i, s in enumerate(S):
    if only and s['fx'] not in only: continue
    t0 = time.time()
    try:
        y = s['fn']()
        y = finalize(np.asarray(y, dtype=np.float64), fade_out=s['fade_out'], loop=s['loop'])
    except Exception:
        print('FAIL', s['fx']); traceback.print_exc(); continue
    fn = re.sub(r'[^A-Za-z0-9]+', '', s['fx']) + '.wav'
    sf.write(os.path.join(out, fn), y, SR, subtype='PCM_16')
    meta.append(dict(tmp=fn, family=s['family'], catid=s['catid'], fx=s['fx'], desc=s['desc'], loop=s['loop'], dur=round(len(y) / SR, 3)))
    print('%-26s %-10s %5.2fs  %.1fs' % (s['fx'], s['catid'], len(y) / SR, time.time() - t0), flush=True)
if not only: json.dump(meta, open(os.path.join(out, '_meta.json'), 'w'), ensure_ascii=False, indent=1)
