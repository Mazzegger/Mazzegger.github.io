"""Bande son de la motion ResyFlex : musique synthétisée (afro-house / amapiano, 120 BPM) + SFX de la bibliothèque.

usage: python3 build_audio.py <timeline.json> <dossier sfx> <moteur motionsynth.py (dossier)> <sortie.wav>
"""
import sys, os, json
import numpy as np, soundfile as sf

TL, SFX, SYNTH_DIR, OUT = sys.argv[1:5]
sys.path.insert(0, SYNTH_DIR)
from motionsynth import (SR, sine, white, pink, lp, hp, bp, env_perc, env_adsr, expcurve, fm, karplus,
                         reverb, sat, stereo, pan_curve, tailfade)

tl = json.load(open(TL)); E = tl['ev']; DUR = tl['duration']
BEAT = 60 / tl['bpm']; BAR = 4 * BEAT; S16 = BEAT / 4
N = int((DUR + 3) * SR)


def buf(): return np.zeros((N, 2))


def put(dst, sig, t, gain=1.0, pan=0.0):
    s = sig if sig.ndim == 2 else pan_curve(sig, pan)
    i = int(round(t * SR))
    if i >= len(dst): return
    n = min(len(s), len(dst) - i)
    dst[i:i + n] += gain * s[:n]


def note(n):
    names = {'C': -9, 'C#': -8, 'Db': -8, 'D': -7, 'D#': -6, 'Eb': -6, 'E': -5, 'F': -4, 'F#': -3, 'Gb': -3, 'G': -2, 'G#': -1, 'Ab': -1, 'A': 0, 'A#': 1, 'Bb': 1, 'B': 2}
    return 440.0 * 2 ** ((names[n[:-1]] + 12 * (int(n[-1]) - 4)) / 12)


# ------------------------------------------------------------------ instruments
def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    y = sine(48 + 110 * np.exp(-t / 0.035), n) * env_perc(n, 0.001, 0.18)
    y += 0.25 * hp(white(n, 1), 2500) * env_perc(n, 0.0002, 0.004)
    return sat(y, 1.6)


def log_drum(f):
    """Log drum amapiano : note grave avec glissement vers le bas, saturée."""
    n = int(0.55 * SR); t = np.arange(n) / SR
    fr = f * (1 + 0.9 * np.exp(-t / 0.02))
    y = sine(fr, n) * env_perc(n, 0.002, 0.22) + 0.3 * sine(fr * 2, n) * env_perc(n, 0.002, 0.06)
    return lp(sat(y, 2.2), 900)


def shaker(seed, acc=1.0):
    n = int(0.07 * SR)
    return hp(white(n, seed), 7000) * env_perc(n, 0.004, 0.018) * 0.35 * acc


def clap(seed):
    n = int(0.35 * SR); y = np.zeros(n)
    for k, d in enumerate([0, 0.009, 0.018]):
        i = int(d * SR); m = n - i
        y[i:] += bp(white(m, seed + k), 900, 4000) * env_perc(m, 0.0005, 0.012 if k < 2 else 0.09)
    return y * 0.6


def rim(seed):
    n = int(0.12 * SR)
    return (sine(1700, n) * env_perc(n, 0.0005, 0.012) + 0.5 * bp(white(n, seed), 2000, 6000) * env_perc(n, 0.0003, 0.006)) * 0.5


def keys(freqs, dur=0.45):
    """Piano électrique FM, accord."""
    n = int(dur * SR); y = np.zeros(n)
    for i, f in enumerate(freqs):
        y += fm(f, 1.0, 1.6, n, env_perc(n, 0.001, 0.12)) * env_perc(n, 0.002, 0.35) * (0.9 - 0.08 * i)
    return y / len(freqs)


def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for i, f in enumerate(freqs):
        y += sine(f * (1 + 0.003 * np.sin(2 * np.pi * (0.3 + 0.1 * i) * t)), n) + 0.3 * sine(2 * f, n)
    return lp(y / len(freqs), 2200) * env_adsr(n, 0.4, 0.2, dur, 0.6, 0.8)


# Progression (1 accord par mesure) : Ebmaj7 – Cm9 – Abmaj7 – Bb6
CH = [['Eb3', 'G3', 'Bb3', 'D4'], ['C3', 'Eb3', 'G3', 'D4'], ['Ab2', 'C3', 'Eb3', 'G3'], ['Bb2', 'D3', 'F3', 'G3']]
BASS = [['Eb2', 'Eb2', 'Bb1', 'Eb2'], ['C2', 'C2', 'G1', 'Bb1'], ['Ab1', 'Ab1', 'Eb2', 'C2'], ['Bb1', 'Bb1', 'F2', 'D2']]
LOG_POS = [0, 1.5, 2.75, 3.5]           # positions (en temps) du log drum dans la mesure
ARP = ['Bb4', 'Eb5', 'G5', 'D5', 'G5', 'Eb5', 'Bb4', 'G4']

drums, bass, harm, extra = buf(), buf(), buf(), buf()
t_start, drop, t_stop = 4.0, E['ctaHit'], E['ctaHit'] - BEAT  # groove de 4 s à 34,5 s, silence avant l'impact final
K, CL = kick(), [clap(40 + i) for i in range(4)]
bar_i = 0
t = 0.0
while t < drop - 1e-6:
    chord = [note(x) for x in CH[bar_i % 4]]
    groove = t >= t_start
    full = t >= E['chapter']['qr']
    # nappe tout du long (plus présente dans l'intro)
    put(harm, stereo(pad(chord, BAR + 0.6), 0.7), t, 0.55 if not groove else 0.28)
    for b in range(4):
        tb = t + b * BEAT
        if tb >= t_stop: break
        if groove:
            put(drums, K, tb, 0.9 if b in (0, 2) else 0.55)
            if b in (1, 3): put(drums, CL[(bar_i + b) % 4], tb, 0.55, 0.0)
            put(harm, keys(chord), tb + BEAT / 2, 0.42, -0.25 if b % 2 else 0.25)   # accords sur le contretemps
        for s in range(4):
            ts = tb + s * S16
            if ts >= t_stop: break
            acc = 1.0 if s == 2 else 0.55
            if t >= 1.0: put(drums, shaker(1000 + int(ts * 100), acc), ts, 1.0 if groove else 0.6, 0.35)
        if groove and b in (1, 2): put(drums, rim(70 + b), tb + 3 * S16, 0.6, -0.4)
    if groove:
        for k, pos in enumerate(LOG_POS):
            tl_ = t + pos * BEAT
            if tl_ < t_stop: put(bass, log_drum(note(BASS[bar_i % 4][k])), tl_, 0.9)
    if full:
        for k in range(8):
            ta = t + k * BEAT / 2
            if ta < t_stop: put(extra, karplus(note(ARP[k]), 0.4, 300 + k, 0.993, 0.7), ta, 0.22, -0.6 + 1.2 * (k % 2))
    t += BAR; bar_i += 1

# Final : impact tonal + accord tenu
fin = [note(x) for x in ['Eb3', 'Bb3', 'D4', 'G4']]
put(harm, stereo(pad(fin, 4.0), 0.8), drop, 0.6)
put(harm, keys(fin, 1.5), drop, 0.6)
put(bass, log_drum(note('Eb2')), drop, 1.0)
put(drums, K, drop, 1.0)

music = drums * 0.9 + bass * 0.9 + reverb(harm, 0.25, 2.2) [:N] + reverb(extra, 0.3, 1.8)[:N]
music = music[:N]
music /= np.abs(music).max()

# ------------------------------------------------------------------ SFX (repères de la timeline)
def sync_offset(y, mode):
    if mode == 'start': return 0.0
    if mode == 'end': return len(y) / SR
    m = np.abs(y).max(1); h = 96; n = len(m) // h
    db = 20 * np.log10(np.sqrt((m[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    if mode == 'peak':
        k = np.convolve(10 ** (db / 20), np.ones(9) / 9, 'same'); return int(np.argmax(k)) * h / SR
    pad_ = np.concatenate([np.full(30, -120.0), db]); best, bi = -1, 0
    for i in range(n - 15):
        nx = db[i:i + 15].mean(); pv = pad_[i:i + 30].max()
        if nx > db.max() - 8 and nx - pv > best: best, bi = nx - pv, i
    return bi * h / SR


D, U, SW, C, M, G, MC = 'DESIGNED/', 'USER INTERFACE/', 'SWOOSHES/', 'CARTOON/', 'MAGIC/', 'GAMES/', 'MECHANICAL/'
f = lambda d, n, src='MotionSynth_MotionLib': f'{d}{n}_{src}.wav'
CUES = []
add = lambda file, t, mode='start', g=0, **o: CUES.append((file, t, mode, g, o))
for t in E['hookWords']: add(f(C, 'TOONPop_Pop High'), t, 'start', -14)
add(f(D, 'DSGNRise_Noise Riser 2s'), E['logoHit'], 'end', -10)
for t in E['hookPhotos']:
    add(f(D, 'DSGNWhsh_Fast Pass By'), t, 'peak', -11); add(f(D, 'DSGNImpt_Snap Hit Tight'), t, 'hit', -10)
add(f(D, 'DSGNStngr_Whoosh Hit Logo'), E['logoHit'], 'hit', -3)
add(f(D, 'DSGNBoom_Boom Deep Short'), E['logoHit'], 'hit', -7)
add(f(M, 'MAGShim_Twinkle'), E['slogan'], 'start', -12)
for t in E['promise']: add(f(U, 'UIMvmt_Pop Appear'), t, 'start', -9)
for t in E['chapter'].values():
    add(f(SW, 'WHSH_Air Whoosh Short'), t, 'peak', -7); add(f(D, 'DSGNImpt_Snap Hit Tight'), t, 'hit', -12)
add(f(U, 'UIMvmt_Slide In Soft'), E['phoneIn'], 'peak', -10)
add(f(U, 'UIData_Text Typing Screen'), E['typeStart'], 'start', -14, cut=0.72)
for i, t in enumerate(E['chips']): add(f(C, 'TOONPop_Bubble Pop'), t, 'start', -13 - (i % 2))
add(f(U, 'UIClick_Toggle On'), E['nearMe'], 'start', -10)
add(f(SW, 'SWSH_Swish Soft'), E['results'], 'peak', -12)
for t in E['cards']: add(U + 'UIMvmt_Card Swipe Short_SurajET_SurajSFX06.wav', t, 'peak', -9)
add(f(D, 'DSGNImpt_Punch Hit Short'), E['stamp'], 'hit', -6)
add(f(U, 'UIAlert_Notification Ding'), E['stampText'], 'start', -11)
add(f(U, 'UIClick_Click Hard'), E['dayIn'], 'start', -9); add(f(U, 'UIClick_Click Hard'), E['dayOut'], 'start', -9)
add(f(SW, 'SWSH_Swish Short'), E['dayOut'] + 0.05, 'peak', -14)
add(f(U, 'UIAlert_Message Received'), E['sent'], 'start', -9)
add(f(U, 'BEEPTimer_Timer Tick Fast').replace('USER INTERFACE/', 'BEEPS/'), E['timer'][0], 'start', -15)
add(f(U, 'UIAlert_Success Arpeggio'), E['confirmed'], 'start', -7)
add(f(U, 'UIMvmt_Pop Appear'), E['payIn'], 'start', -10)
add(f(U, 'UIData_Score Counter Rollup'), E['countStart'], 'start', -11)
for t in E['methods']: add(f(U, 'UIMvmt_Pop Appear'), t, 'start', -11)
add(f(U, 'UIClick_Toggle On'), E['select'], 'start', -9)
add(G + 'GAMECas_Cashier Ka Ching_SurajET_SurajSFX06.wav', E['kaching'], 'hit', -9)
add(MC + 'MECHSwtch_Switch Toggle_PieroCesti_PieroCestiSFX.wav', E['lock'], 'start', -10)
add(f(U, 'UIData_Data Chatter'), E['qrBuild'][0], 'start', -15, cut=1.0)
add(f(U, 'UIData_Scan Sweep'), E['scan'][0], 'start', -10, cut=0.95)
add(f(U, 'UIBeep_Beep Confirm'), E['scanOk'], 'start', -8)
add(U + 'UIAlert_Success UI_PieroCesti_PieroCestiSFX.wav', E['welcome'], 'start', -8)
add(f(M, 'MAGShim_Magic Sparkle'), E['welcome'] + 0.1, 'start', -16)
for t in E['trust']:
    add(f(SW, 'WHSH_Air Whoosh Short'), t, 'peak', -11); add(f(C, 'TOONPop_Pop Low'), t, 'start', -11)
add(f(SW, 'WHSH_Air Whoosh Medium'), E['ownerIn'], 'peak', -8)
add(f(U, 'UIAlert_Reward Coin'), E['ownerFree'], 'start', -11)
add(f(D, 'DSGNRise_Reverse Cymbal'), E['ctaHit'], 'end', -11)
add(f(D, 'DSGNImpt_Cinematic Hit Big'), E['ctaHit'], 'hit', -5)
add(f(D, 'DSGNBass_Sub Drop 2s'), E['ctaHit'], 'start', -8)
add(f(M, 'MAGShim_Twinkle'), E['ctaTag'], 'start', -13)
add(f(U, 'UIAlert_Notification Ding'), E['ctaUrl'], 'start', -10)
add(f(C, 'TOONPop_Pop High'), E['ctaPhone'], 'start', -12)

sfx = buf(); report = []
for file, t, mode, g, o in CUES:
    p = os.path.join(SFX, file)
    if not os.path.exists(p):
        # BEEPTimer vit dans BEEPS/, Swish dans SWOOSHES/ : recherche par nom
        hits = [os.path.join(dp, x) for dp, _, fs in os.walk(SFX) for x in fs if x == os.path.basename(file)]
        assert hits, file; p = hits[0]
    y, sr = sf.read(p, always_2d=True); assert sr == SR
    off = sync_offset(y, mode)
    if o.get('cut'):
        n = int(o['cut'] * SR); y = y[:n].copy(); fo = int(0.04 * SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    put(sfx, y, max(t - off, 0), 10 ** (g / 20))
    report.append(dict(file=os.path.relpath(p, SFX), cue=t, mode=mode, sync=round(off, 3), placed=round(t - off, 3), gain_db=g))

# ------------------------------------------------------------------ mix + master
mix = music * 10 ** (-10 / 20) + sfx
mix = mix[:int(DUR * SR)]
fo = int(0.6 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
pk = np.abs(mix).max(); x = np.tanh(mix / pk * 1.8) / np.tanh(1.8)
x *= 10 ** (-1 / 20) / np.abs(x).max()
sf.write(OUT, x, SR, subtype='PCM_16')
sf.write(OUT.replace('.wav', '_music.wav'), music[:int(DUR * SR)] * 0.5, SR, subtype='PCM_16')
json.dump(report, open(OUT.replace('.wav', '_cues.json'), 'w'), indent=1, ensure_ascii=False)
print(len(report), 'SFX placés ;', len({r["file"] for r in report}), 'fichiers différents')
