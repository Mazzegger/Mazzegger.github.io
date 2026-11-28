"""Bande son v2 : vraie musique (Mixkit « Let's Move », drop calé sur le logo) + vrais effets sonores Mixkit.

usage: python3 build_audio.py <timeline.json> <dossier des sons Mixkit en WAV 48 kHz> <sortie.wav>
Les fichiers Mixkit ne sont pas redistribués : ils se téléchargent avec fetch_mixkit.sh.
"""
import sys, os, json
import numpy as np, soundfile as sf

TL, SND, OUT = sys.argv[1:4]
tl = json.load(open(TL)); E = tl['ev']; MU = tl['music']; DUR = tl['duration']
SR = 48000; N = int((DUR + 2) * SR)


def load(name):
    y, sr = sf.read(os.path.join(SND, f'{name}.wav'), always_2d=True); assert sr == SR, name
    return y[:, :2] if y.shape[1] >= 2 else np.repeat(y, 2, 1)


def sync_offset(y, mode):
    if mode == 'start': return 0.0
    if mode == 'end': return len(y) / SR
    m = np.abs(y).max(1); h = 96; n = len(m) // h
    db = 20 * np.log10(np.sqrt((m[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    if mode == 'peak':
        k = np.convolve(10 ** (db / 20), np.ones(9) / 9, 'same'); return int(np.argmax(k)) * h / SR
    pad = np.concatenate([np.full(30, -120.0), db]); best, bi = -1, 0
    for i in range(n - 15):
        nx = db[i:i + 15].mean(); pv = pad[i:i + 30].max()
        if nx > db.max() - 8 and nx - pv > best: best, bi = nx - pv, i
    return bi * h / SR


def put(dst, y, t, g):
    i = int(round(t * SR))
    if i < 0: y = y[-i:]; i = 0
    n = min(len(y), len(dst) - i)
    if n > 0: dst[i:i + n] += y[:n] * g


# ------------------------------------------------------------------ musique
mus = load(MU['file'].replace('.wav', ''))
a = int(MU['start'] * SR)
music = np.zeros((N, 2)); seg = mus[a:a + N]; music[:len(seg)] = seg
t = np.arange(N) / SR
c0, c1 = MU['cut']
gate = np.ones(N)                                     # coupure d'un temps avant l'appel à l'action
gate[(t >= c0) & (t < c1)] = 0.0
k = int(0.03 * SR); i0, i1 = int(c0 * SR), int(c1 * SR)
gate[i0 - k:i0] = np.linspace(1, 0, k); gate[i1:i1 + k] = np.linspace(0, 1, k)
f0, f1 = MU['fadeOut']
gate *= np.clip((f1 - t) / (f1 - f0), 0, 1) ** 1.5
music *= gate[:, None]

# ------------------------------------------------------------------ effets sonores (id Mixkit, instant, synchro, gain dB, options)
C = []
add = lambda i, tt, mode='start', g=0, **o: C.append((str(i), tt, mode, g, o))
for k_, tt in enumerate(E['cityCuts']):
    add(3115, tt, 'peak', -8); add(1433, tt, 'start', -15)
add(2364, E['hookLine'][0], 'start', -9); add(3120, E['hookLine'][1], 'start', -9)
add(790, E['drop'], 'end', -5); add(1486, E['drop'] - 0.05, 'peak', -11)
add(2900, E['drop'], 'hit', -2); add(788, E['drop'], 'hit', -9)
for tt in E['words']: add(772, tt, 'hit', -7)
add(2627, E['zoomThrough'] + 0.25, 'peak', -6); add(2608, E['zoomThrough'] + 0.4, 'peak', -11)
add(3120, E['phoneIn'], 'start', -9); add(2568, E['listIn'], 'start', -10); add(166, E['listIn'] + 0.3, 'peak', -13)
for k_, tt in enumerate(E['callouts']): add(2356 if k_ % 2 == 0 else 2357, tt, 'start', -11)
add(1492, E['whip'] + 0.1, 'peak', -7)
add(2635, E['mapDraw'], 'start', -8)
for k_, tt in enumerate(E['pins']): add([2521, 2866, 2519][k_ % 3], tt, 'start', -12)
add(2655, E['cities'], 'hit', -7); add(3005, E['soon'], 'start', -10); add(1481, E['toVerify'] + 0.1, 'peak', -8)
add(2633, E['fan'], 'start', -10)
for tt in E['shots']: add(1430, tt, 'start', -9)
add(2150, E['stamp'], 'hit', -4); add(2870, E['stamp'] + 0.15, 'start', -10); add(2356, E['stampSub'], 'start', -13)
add(3115, E['toAvail'] + 0.1, 'peak', -8)
add(2909, E['ten'], 'hit', -4); add(772, E['min'], 'hit', -9)
add(1063, E['tick'][0], 'start', -11, cut=E['tick'][1] - E['tick'][0])
add(951, E['confirmed'], 'start', -6); add(2356, E['availSub'], 'start', -13)
add(2627, E['toPay'] + 0.1, 'peak', -8)
add(2655, E['thirty'], 'hit', -5); add(2529, E['fill'][0], 'start', -12, cut=1.0)
add(3005, E['deposit'], 'start', -10)
for tt in E['chips']: add(2364, tt, 'start', -10)
add(1936, E['coins'], 'start', -8); add(1993, E['coins'] + 0.05, 'start', -12)
add(1492, E['toStay'] + 0.1, 'peak', -8)
add(2638, E['stayIn'], 'start', -9); add(890, E['qrBuild'][0], 'start', -10)
add(2529, E['scan'][0], 'start', -10, cut=E['scan'][1] - E['scan'][0])
add(3116, E['scanOk'], 'start', -5); add(2842, E['key'], 'start', -9); add(2350, E['welcome'], 'start', -8)
add(3115, E['toTrust'] + 0.1, 'peak', -8)
for tt in E['trust']: add(1464, tt, 'peak', -8); add(772, tt, 'hit', -12)
add(1474, E['owner'][0], 'peak', -8); add(2357, E['owner'][1], 'start', -11); add(1992, E['owner'][2], 'start', -8)
add(790, E['ctaHit'], 'end', -6)
add(2918, E['ctaHit'], 'hit', -3); add(2901, E['ctaHit'], 'hit', -10)
add(3062, E['ctaTag'], 'start', -10); add(2357, E['ctaUrl'], 'start', -9); add(2356, E['ctaPhone'], 'start', -11)

sfx = np.zeros((N, 2)); rep = []
for i, tt, mode, g, o in C:
    y = load(i); off = sync_offset(y, mode)
    if o.get('cut'):
        n = int(o['cut'] * SR); y = y[:n].copy(); fo = min(int(0.05 * SR), n // 3); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    put(sfx, y, tt - off, 10 ** (g / 20))
    rep.append(dict(mixkit_id=i, cue=tt, mode=mode, sync=round(off, 3), placed=round(tt - off, 3), gain_db=g))

mix = music * 10 ** (-7 / 20) + sfx
mix = mix[:int(DUR * SR)]
pk = np.abs(mix).max(); x = np.tanh(mix / pk * 1.3) / np.tanh(1.3)      # écrêtage doux léger
x *= 10 ** (-3 / 20) / np.abs(x).max()
tmp = OUT.replace('.wav', '_pre.wav'); sf.write(tmp, x, SR, subtype='FLOAT')
# normalisation EBU R128 en deux passes : -14 LUFS, crête vraie -1 dBTP
import subprocess, re
r = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', str(SR), '-c:a', 'pcm_s16le', OUT], check=True)
os.remove(tmp)
json.dump(rep, open(OUT.replace('.wav', '_cues.json'), 'w'), indent=1)
print(len(rep), 'effets placés ;', len({r['mixkit_id'] for r in rep}), 'sons Mixkit différents')
