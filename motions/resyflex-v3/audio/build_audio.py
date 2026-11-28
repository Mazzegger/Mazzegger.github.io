"""Bande son v3 : vraie musique (Mixkit « Cat Walk » d'Arulo, 2 drops + break) + vrais effets sonores Mixkit.

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
gate = np.ones(N)
f0, f1 = MU['fadeOut']
gate *= np.clip((f1 - t) / (f1 - f0), 0, 1) ** 1.5
music *= gate[:, None]

# ------------------------------------------------------------------ effets sonores (id Mixkit, instant, synchro, gain dB, options)
C = []
add = lambda i, tt, mode='start', g=0, **o: C.append((str(i), tt, mode, g, o))
# intro 3D : grondement qui monte, pièces qui arrivent et se verrouillent
add(784, E['slam'], 'end', -8)
add(3120, E['introText'][0], 'start', -12); add(3005, E['introText'][1], 'start', -12)
for tt in E['lock']:
    add(1493, tt - 0.12, 'peak', -9); add(2858, tt, 'start', -6); add(1485, tt, 'hit', -10)
add(790, E['slam'], 'end', -6); add(1486, E['slam'] - 0.1, 'peak', -12)
add(2900, E['slam'], 'hit', -2); add(2599, E['slam'], 'hit', -8); add(788, E['slam'], 'hit', -10)
add(2586, E['sweep'] + 0.5, 'peak', -9); add(2635, E['wordmark'], 'start', -11); add(3062, E['slogan'], 'start', -12)
add(2627, E['heroOut'] + 0.17, 'peak', -7)
for k, tt in enumerate(E['cutBeats']):
    if k in (0, 2, 4): add(772, tt, 'hit', -8)
    elif k in (1, 3, 5): add(1430, tt, 'start', -10); add(3115, tt, 'peak', -12)
    else: add(2364, tt, 'start', -10)
add(2635, E['mapRise'], 'start', -9); add(2902, E['mapRise'], 'hit', -9)
for k, tt in enumerate(E['pillars']): add(2626, tt, 'start', -13); add([2521, 2866, 2519][k % 3], tt, 'start', -14)
add(2655, E['mapCount'], 'hit', -8)
add(1493, E['carIn'], 'start', -8); add(2633, E['carIn'] + 0.2, 'start', -12)
add(2150, E['carStamp'], 'hit', -4); add(2870, E['carStamp'] + 0.15, 'start', -10); add(2356, E['carSub'], 'start', -13)
add(1059, E['tick'][0], 'start', -11, cut=E['tick'][1] - E['tick'][0])
for tt in E['heart']: add(498, tt, 'hit', -6)
add(2918, E['confirmed'], 'hit', -4); add(951, E['confirmed'] + 0.1, 'start', -6)
add(2655, E['payNum'], 'hit', -6); add(2529, E['fill'][0], 'start', -12, cut=0.9)
for tt in E['chips']: add(2364, tt, 'start', -10)
add(1936, E['coins'], 'start', -8); add(1993, E['coins'] + 0.05, 'start', -12)
add(2638, E['qrIn'], 'start', -9); add(890, E['qrBuild'][0], 'start', -10)
add(2529, E['scan'][0], 'start', -10, cut=E['scan'][1] - E['scan'][0])
add(3116, E['scanOk'], 'start', -5); add(2842, E['key'], 'start', -9); add(2350, E['welcome'], 'start', -8)
for tt in E['trust']: add(1464, tt, 'peak', -8); add(772, tt, 'hit', -12)
add(1474, E['owner'][0], 'peak', -8); add(2357, E['owner'][1], 'start', -11); add(1992, E['owner'][2], 'start', -8)
add(2903, E['outroBurst'], 'hit', -6)
for tt in E['outroLock']: add(2857, tt, 'start', -8); add(1485, tt, 'hit', -12)
add(2901, E['outroSlam'], 'hit', -3); add(2599, E['outroSlam'], 'hit', -10); add(2586, E['outroSlam'] + 1.0, 'peak', -10)
add(3062, E['ctaTag'], 'start', -11); add(2357, E['ctaUrl'], 'start', -9); add(2356, E['ctaPhone'], 'start', -11)

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
