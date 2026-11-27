"""Définition des sons synthétisés : famille motion, CatID UCS, nom, description, recette."""
import numpy as np
from motionsynth import *

S = []  # liste des specs


def add(family, catid, fx, desc, loop=False, fade_out=0.02, trim_db=-70):
    def deco(fn):
        S.append(dict(family=family, catid=catid, fx=fx, desc=desc, fn=fn, loop=loop, fade_out=fade_out, trim_db=trim_db))
        return fn
    return deco


def note(n):  # 'A4' -> Hz
    names = {'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5, 'F': -4, 'F#': -3, 'G': -2, 'G#': -1, 'A': 0, 'A#': 1, 'B': 2}
    return 440.0 * 2 ** ((names[n[:-1]] + 12 * (int(n[-1]) - 4)) / 12)


def mix(*xs):
    n = max(len(x) for x in xs)
    return sum(np.pad(x, [(0, n - len(x))] + [(0, 0)] * (x.ndim - 1)) for x in xs)


def smooth(x):
    return x * x * (3 - 2 * x)


# =================================================================== briques réutilisables
def whoosh(dur, f_lo, f_hi, peak=0.55, bw_edge=1.8, bw_peak=1.0, tone=0.0, pan=(-0.8, 0.8), seed=0,
           sub=0.0, wet=0.12, a_pow=2.0, r_pow=1.6):
    n = int(dur * SR)
    nz = 0.6 * pink(n, seed) + 0.4 * white(n, seed + 1) / 3
    lf = curve([(0, np.log(f_lo)), (peak, np.log(f_hi)), (1, np.log(f_lo * 1.6))], n)
    fc = np.exp(lf)
    bw = curve([(0, bw_edge), (peak, bw_peak), (1, bw_edge)], n)
    g = env_swell(n, peak, a_pow, r_pow)
    y = spectral_band(nz, fc, bw, g)
    if tone:
        y += tone * spectral_band(white(n, seed + 2), fc * 1.2, 0.12, g) * 3
    if sub:
        y += sub * sine(fc * 0.08 + 40, n) * g ** 1.5
    y /= np.abs(y).max() + 1e-12
    path = pan[0] + (pan[1] - pan[0]) * smooth(np.linspace(0, 1, n))
    st = doppler(y, path)
    return reverb(st, wet, 1.2, seed + 5, 7000) if wet else st


def swish(dur, f0=1500, f1=6500, seed=0, peak=0.35, bw=1.2, pan=(-0.3, 0.3)):
    n = int(dur * SR)
    lf = curve([(0, np.log(f0)), (peak, np.log(f1)), (1, np.log(f1 * 0.6))], n)
    y = spectral_band(white(n, seed), np.exp(lf), bw, env_swell(n, peak, 1.5, 2.2))
    y /= np.abs(y).max()
    return doppler(y, np.linspace(pan[0], pan[1], n), 0.6)


def click(f=2400, dec=0.006, noise=0.6, nlo=2000, nhi=9000, seed=0, body=0.0, body_f=180):
    n = int(max(dec * 8, 0.03) * SR)
    y = (1 - noise) * sine(f, n) * env_perc(n, 0.0003, dec)
    y += noise * bp(white(n, seed), nlo, nhi) * env_perc(n, 0.0002, dec * 0.6) * 0.5
    if body:
        y += body * sine(body_f, n) * env_perc(n, 0.0005, dec * 2.5)
    return tailfade(y, 0.3)


def pop(f0, f1, dur=0.06, dec=0.03, shape=0.5, seed=0, noise=0.05):
    n = int(dur * 3 * SR)
    fr = np.concatenate([expcurve(f0, f1, int(dur * SR), shape), np.full(n - int(dur * SR), f1)])
    y = sine(fr, n) * env_perc(n, 0.0008, dec)
    y += noise * hp(white(n, seed), 2000) * env_perc(n, 0.0003, 0.004)
    return tailfade(y, 0.5)


def impact(seed=0, f0=110, f1=38, body_dec=0.45, click_amt=1.0, mid=0.6, tail=1.5, wet=0.25,
           metal=0.0, dist=1.6, bright=1.0, sub_len=1.0):
    n = int((body_dec * 5 * sub_len + 0.2) * SR)
    t = np.arange(n) / SR
    fr = f1 + (f0 - f1) * np.exp(-t / 0.06)
    body = sine(fr, n) * env_perc(n, 0.001, body_dec * sub_len)
    cl = hp(white(n, seed), 1800) * env_perc(n, 0.0003, 0.004) * click_amt
    md = bp(white(n, seed + 1), 120, 1800 * bright) * env_perc(n, 0.001, 0.07) * mid
    y = body + 0.6 * cl + md
    if metal:
        y += metal * 0.5 * bell(320 * bright, n / SR, seed, bright=1.4, decay=0.9)
    y = tailfade(sat(y / np.abs(y).max(), dist), 0.3)
    return reverb(y, wet, tail, seed + 3, 5000 * bright) if wet else stereo(y)


def noise_riser(dur, f0=250, f1=9000, seed=0, shape=1.6, end_cut=True):
    n = int(dur * SR)
    fc = expcurve(f0, f1, n, shape)
    g = np.linspace(0, 1, n) ** 2.2
    y = spectral_band(0.7 * pink(n, seed) + 0.3 * white(n, seed + 1) / 3, fc, curve([(0, 1.6), (1, 0.8)], n), g)
    y += 0.25 * hp(white(n, seed + 2), 6000) * np.linspace(0, 1, n) ** 3
    return stereo(y / np.abs(y).max(), 0.8)


def pad_chord(freqs, dur, seed=0, kind='saw', lp_hz=2500, vib=0.0):
    n = int(dur * SR)
    acc = np.zeros((n, 2))
    for i, f in enumerate(freqs):
        if kind == 'saw':
            acc += supersaw(f, n, 5, 12, seed + i)
        else:
            fr = f * (1 + vib * np.sin(2 * np.pi * (4.5 + 0.3 * i) * np.arange(n) / SR))
            acc += pan_curve(sine(fr, n), (i / max(len(freqs) - 1, 1) - 0.5) * 1.2)
    if kind == 'saw':
        acc = lp(acc, lp_hz, 2)
    return acc / (np.abs(acc).max() + 1e-12)


def tape_warp(x, rate_curve):
    """Lecture à vitesse variable (rate 1 = normal) ; x stéréo."""
    pos = np.cumsum(rate_curve)
    pos = pos[pos < len(x) - 1]
    i0 = np.floor(pos).astype(int); fr = (pos - i0)[:, None]
    return x[i0] * (1 - fr) + x[i0 + 1] * fr


def sparkle_grains(dur, count, seed=0, lo='C6', hi='C8', dec=0.12, scale=(0, 2, 4, 7, 9)):
    r = rng(seed)
    out = silence(dur + 0.5)
    base = note(lo)
    octs = int(np.log2(note(hi) / base))
    for k in range(count):
        st = r.choice(scale) + 12 * r.integers(0, max(octs, 1))
        f = base * 2 ** (st / 12)
        g = sine(f, int(0.4 * SR)) * env_perc(int(0.4 * SR), 0.001, dec * r.uniform(0.6, 1.4))
        g += 0.3 * sine(f * 2.76, int(0.4 * SR)) * env_perc(int(0.4 * SR), 0.001, dec * 0.4)
        out = place(out, pan_curve(g * r.uniform(0.4, 1.0), r.uniform(-0.8, 0.8)), r.uniform(0, dur))
    return out


def blip(f, dur=0.08, wave='sine', a=0.003, r_=0.02, lp_hz=5000):
    n = int(dur * SR)
    osc = {'sine': sine, 'square': square, 'tri': tri}[wave](f, n)
    y = osc * env_adsr(n, a, 0.01, dur, r_, 0.8)
    return lp(y, lp_hz, 2) if wave != 'sine' else y


def fm_bell(f, dur=1.2, ratio=1.4, index=2.5, dec=0.5):
    n = int(dur * SR)
    e = env_perc(n, 0.001, dec)
    return tailfade(fm(f, ratio, index, n, env_perc(n, 0.001, dec * 0.5)) * e, 0.35)


def seq(events, total=None):
    """events: liste (t, signal)"""
    out = silence(total or 0.01)
    for t0, s in events:
        out = place(out, s, t0)
    return out


# =================================================================== 1. WHOOSH (WHSH / DSGNWhsh)
F = 'Whoosh'
@add(F, 'WHSH', 'Air Whoosh Short', 'Whoosh d’air court (0,35 s), passage gauche→droite.')
def _(): return whoosh(0.35, 400, 3500, 0.5, seed=1)
@add(F, 'WHSH', 'Air Whoosh Medium', 'Whoosh d’air moyen (0,7 s), polyvalent pour entrées/sorties.')
def _(): return whoosh(0.7, 300, 3000, 0.55, seed=2)
@add(F, 'WHSH', 'Air Whoosh Long', 'Whoosh d’air long et ample (1,4 s).')
def _(): return whoosh(1.4, 200, 2500, 0.6, seed=3, wet=0.2)
@add(F, 'WHSH', 'Airy Whoosh Bright', 'Whoosh aérien et brillant (aigus), élégant pour du texte.')
def _(): return whoosh(0.6, 1500, 9000, 0.5, bw_edge=1.4, bw_peak=0.9, seed=4)
@add(F, 'DSGNWhsh', 'Heavy Whoosh Low', 'Whoosh lourd et grave avec sub, pour gros éléments ou caméra.')
def _(): return whoosh(1.0, 90, 900, 0.55, seed=5, sub=0.5, wet=0.2)
@add(F, 'DSGNWhsh', 'Tonal Whoosh', 'Whoosh avec sifflement tonal, futuriste.')
def _(): return whoosh(0.8, 300, 4000, 0.5, tone=0.5, seed=6)
@add(F, 'DSGNWhsh', 'Fast Pass By', 'Passage très rapide (0,25 s), mouvement éclair.')
def _(): return whoosh(0.25, 600, 6000, 0.45, seed=7, a_pow=1.5, r_pow=2.5)
@add(F, 'DSGNWhsh', 'Double Whoosh', 'Double whoosh aller-retour.')
def _():
    a = whoosh(0.4, 400, 4000, 0.5, seed=8, pan=(-0.8, 0.8), wet=0)
    b = whoosh(0.45, 350, 3500, 0.5, seed=9, pan=(0.8, -0.8), wet=0)
    return reverb(seq([(0, a), (0.32, b)]), 0.12, 1.0)
@add(F, 'DSGNWhsh', 'Whoosh Swell Slow', 'Whoosh qui gonfle lentement (pic tardif), avant une révélation.')
def _(): return whoosh(1.2, 150, 2800, 0.82, seed=10, a_pow=2.5, r_pow=1.2, wet=0.18)
@add(F, 'DSGNWhsh', 'Whoosh Cinematic', 'Whoosh cinématique large, grave + aigus, longue queue.')
def _():
    a = whoosh(1.1, 120, 1500, 0.55, seed=11, sub=0.35, wet=0)
    b = whoosh(1.1, 1200, 8000, 0.55, seed=12, wet=0) * 0.5
    return reverb(a + b, 0.25, 2.0)

# =================================================================== 2. SWISH / SWIPE (SWSH / UIMvmt / TOONZip)
F = 'Swish / swipe'
@add(F, 'SWSH', 'Swish Tiny', 'Micro-swish (0,15 s) : petit élément, icône.')
def _(): return swish(0.15, seed=21)
@add(F, 'SWSH', 'Swish Short', 'Swish court et net (0,22 s).')
def _(): return swish(0.22, 1200, 7000, seed=22)
@add(F, 'SWSH', 'Swish Soft', 'Swish doux et feutré.')
def _(): return lp(swish(0.3, 800, 4000, seed=23, bw=1.5), 5000)
@add(F, 'SWSH', 'Swish Sharp', 'Swish tranchant (aigus).')
def _(): return swish(0.2, 3000, 11000, seed=24, bw=0.9)
@add(F, 'UIMvmt', 'Swipe Left', 'Glissement d’interface vers la gauche (carte, slide).')
def _(): return lp(swish(0.28, 900, 3500, seed=25, pan=(0.6, -0.6)), 6000)
@add(F, 'UIMvmt', 'Swipe Right', 'Glissement d’interface vers la droite.')
def _(): return lp(swish(0.28, 900, 3500, seed=26, pan=(-0.6, 0.6)), 6000)
@add(F, 'UIMvmt', 'Slide In Soft', 'Entrée glissée douce d’un panneau.')
def _(): return lp(swish(0.45, 400, 2500, seed=27, peak=0.6, bw=1.6), 4000)
@add(F, 'TOONZip', 'Zip Up', 'Zip rapide montant (0,12 s).')
def _():
    n = int(0.14 * SR)
    fr = expcurve(400, 4000, n, 1.0)
    y = 0.6 * sine(fr, n) * env_swell(n, 0.7, 1, 2) + 0.4 * swish(0.14, 1500, 9000, seed=28)[:, 0]
    return stereo(y)

# =================================================================== 3. RISERS (DSGNRise)
F = 'Riser / montée'
@add(F, 'DSGNRise', 'Noise Riser 2s', 'Montée de bruit (2 s) qui s’arrête net : à caler pour finir sur l’impact.', fade_out=0.004)
def _(): return noise_riser(2.0, seed=31)
@add(F, 'DSGNRise', 'Noise Riser 4s', 'Montée de bruit longue (4 s).', fade_out=0.004)
def _(): return noise_riser(4.0, 180, 10000, seed=32, shape=1.8)
@add(F, 'DSGNRise', 'Synth Riser', 'Montée synthé (supersaw qui monte de 2 octaves + filtre qui s’ouvre), 3 s.', fade_out=0.004)
def _():
    n = int(3 * SR)
    f = expcurve(110, 440, n, 1.3)
    s = supersaw(f, n, 7, 20, 33)
    s = np.stack([lp_sweep(s[:, c], expcurve(300, 12000, n, 1.5), 0.5) for c in range(2)], 1)
    trem = 1 - 0.3 * (0.5 + 0.5 * np.sin(phase_from_freq(expcurve(4, 24, n))))
    s *= (np.linspace(0, 1, n) ** 1.8 * trem)[:, None]
    return s / np.abs(s).max() + 0.4 * noise_riser(3.0, seed=34)
@add(F, 'DSGNRise', 'Shepard Riser', 'Montée « infinie » (illusion de Shepard), 4 s : tension continue.', fade_out=0.15)
def _():
    n = int(4 * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(8):
        pos = (k + t / 4) % 8
        f = 40 * 2 ** pos
        amp = np.exp(-0.5 * ((pos - 4) / 1.5) ** 2)
        y += amp * sine(f, n)
    y *= np.clip(t / 0.5, 0, 1)
    return reverb(y / np.abs(y).max(), 0.2, 1.5)
@add(F, 'DSGNRise', 'Tension Riser', 'Montée de tension : cluster de sons qui monte avec tremolo qui accélère (3 s).', fade_out=0.004)
def _():
    n = int(3 * SR)
    y = np.zeros(n)
    for i, st in enumerate([0, 1, 7]):
        y += sine(expcurve(220 * 2 ** (st / 12), 440 * 2 ** (st / 12), n, 1.2), n)
    trem = 0.5 + 0.5 * np.sin(phase_from_freq(expcurve(3, 30, n)))
    y = y * trem * np.linspace(0.1, 1, n) ** 1.5
    return reverb(y / np.abs(y).max(), 0.2, 1.2, tail=False)
@add(F, 'DSGNRise', 'Uplifter Short', 'Petite montée courte (1 s) pour un changement de plan.', fade_out=0.004)
def _(): return noise_riser(1.0, 600, 12000, seed=36, shape=1.2)
@add(F, 'DSGNRise', 'Reverse Cymbal', 'Cymbale inversée (1,8 s) : se termine sur le temps fort.', fade_out=0.003)
def _():
    n = int(1.8 * SR)
    cy = hp(white(n, 37), 4500) * env_perc(n, 0.001, 0.6)
    cy += 0.4 * bell(4200, 1.8, 37, bright=1.5, decay=0.8) * env_perc(n, 0.001, 0.5)
    st = reverb(cy, 0.3, 1.0, tail=False)
    return st[::-1]
@add(F, 'DSGNRise', 'Reverse Whoosh Suck', 'Aspiration inversée (impact + réverb à l’envers), 1,2 s.', fade_out=0.003)
def _():
    h = impact(38, 160, 60, 0.25, 1.0, 0.8, tail=1.2, wet=0.6)
    h = h[:int(1.2 * SR)]
    return h[::-1]

# =================================================================== 4. IMPACTS (DSGNImpt)
F = 'Impact / hit'
@add(F, 'DSGNImpt', 'Punch Hit Short', 'Impact sec et punchy, court : texte qui tombe, cut.')
def _(): return impact(41, 140, 45, 0.18, 1.0, 0.8, tail=0.6, wet=0.12)
@add(F, 'DSGNImpt', 'Cinematic Hit Big', 'Gros impact cinématique avec longue queue (3 s).')
def _(): return impact(42, 120, 34, 0.6, 1.0, 0.7, tail=3.0, wet=0.35, dist=2.2)
@add(F, 'DSGNImpt', 'Trailer Hit Distorted', 'Impact de bande-annonce saturé et massif.')
def _():
    y = impact(43, 150, 32, 0.7, 1.2, 1.0, tail=2.5, wet=0.3, dist=4.0)
    n = len(y); nz = lp(white(n, 43), 3000) * env_perc(n, 0.001, 0.25)
    return y + 0.25 * stereo(nz, 0.8)
@add(F, 'DSGNImpt', 'Metallic Hit', 'Impact métallique qui résonne.')
def _(): return impact(44, 130, 50, 0.3, 1.0, 0.5, tail=2.0, wet=0.3, metal=0.8)
@add(F, 'DSGNImpt', 'Soft Pillow Hit', 'Impact doux et feutré, sans attaque agressive.')
def _(): return lp(impact(45, 100, 45, 0.3, 0.1, 0.4, tail=1.0, wet=0.2, dist=1.1), 1500)
@add(F, 'DSGNImpt', 'Bright Glass Hit', 'Impact brillant/cristallin.')
def _(): return impact(46, 180, 70, 0.2, 1.3, 0.6, tail=1.8, wet=0.35, metal=0.6, bright=2.2)
@add(F, 'DSGNImpt', 'Snap Hit Tight', 'Impact très serré (snap), pour les coupes rythmées.')
def _(): return impact(47, 200, 60, 0.08, 1.4, 1.0, tail=0.4, wet=0.08, dist=2.0)
@add(F, 'DSGNImpt', 'Deep Hit Reverb', 'Impact profond avec grande réverbération.')
def _(): return impact(48, 90, 30, 0.5, 0.6, 0.5, tail=3.5, wet=0.5)

# =================================================================== 5. BOOM / SUB DROP / RUMBLE (DSGNBoom / DSGNBass / DSGNRmbl)
F = 'Boom / sub drop'
@add(F, 'DSGNBoom', 'Boom Deep Short', 'Boom grave court, renfort de basse pour un temps fort.')
def _():
    n = int(1.5 * SR); t = np.arange(n) / SR
    y = sine(32 + 40 * np.exp(-t / 0.08), n) * env_perc(n, 0.002, 0.35)
    return reverb(mix(sat(y, 2.5), 0.2 * click(1500, 0.004, 0.8)), 0.15, 1.2)
@add(F, 'DSGNBoom', 'Boom Trailer', 'Boom de bande-annonce long et profond.')
def _():
    n = int(3 * SR); t = np.arange(n) / SR
    y = sine(28 + 50 * np.exp(-t / 0.12), n) * env_perc(n, 0.003, 0.9)
    y = sat(y, 3.0) + 0.3 * lp(brown(n, 52), 200) * env_perc(n, 0.01, 0.6)
    return reverb(y, 0.25, 2.5, damp_hz=2000)
@add(F, 'DSGNBass', 'Sub Drop 2s', 'Sub drop : basse qui plonge 90→28 Hz (2 s).')
def _():
    n = int(2.4 * SR)
    y = sine(expcurve(90, 28, n, 0.6), n) * env_perc(n, 0.002, 0.9)
    return stereo(sat(y, 1.8))
@add(F, 'DSGNBass', 'Sub Drop Long', 'Sub drop long (3,5 s) pour une grosse révélation.')
def _():
    n = int(3.6 * SR)
    y = sine(expcurve(110, 25, n, 0.5), n) * env_perc(n, 0.002, 1.4)
    return stereo(sat(y, 2.2) + 0.15 * saw(expcurve(110, 25, n, 0.5), n) * env_perc(n, 0.002, 0.3))
@add(F, 'DSGNBass', 'Bass Dive', 'Plongée de basse rapide 220→30 Hz.')
def _():
    n = int(1.6 * SR)
    f = expcurve(220, 30, n, 0.7)
    y = lp_sweep(saw(f, n), f * 4, 0.6) * env_perc(n, 0.003, 0.6)
    return stereo(sat(y / np.abs(y).max(), 2.0))
@add(F, 'DSGNRmbl', 'Rumble Swell', 'Grondement qui monte puis s’éteint (3 s).')
def _():
    n = int(3 * SR)
    y = lp(brown(n, 56), 140, 4) * env_swell(n, 0.45, 1.5, 1.3)
    return stereo(y / np.abs(y).max(), 0.5)

# =================================================================== 6. BRAAM (DSGNBram)
F = 'Braam'
def braam(dur, root=55.0, lp_peak=1800, rise=0.0, seed=0, att=0.08):
    n = int(dur * SR)
    f = root * (expcurve(1, 2 ** (rise / 12), n) if rise else np.ones(n))
    s = sum(supersaw(f * m, n, 6, 14, seed + i) * a for i, (m, a) in enumerate([(1, 1.0), (1.5, 0.6), (2, 0.5), (0.5, 0.7)]))
    fc = curve([(0, 150), (0.12, lp_peak), (0.6, lp_peak * 0.5), (1, 200)], n)
    s = np.stack([lp_sweep(s[:, c], fc, 0.8) for c in range(2)], 1)
    s *= env_adsr(n, att, 0.3, dur, dur * 0.35, 0.75)[:, None]
    s = sat(s / np.abs(s).max(), 2.5)
    return reverb(s, 0.3, 3.0, seed + 9, 3000)
@add(F, 'DSGNBram', 'Braam Dark', 'Braam sombre et massif (3 s), façon bande-annonce.')
def _(): return braam(3.0, 55, 1400, seed=61)
@add(F, 'DSGNBram', 'Braam Bright', 'Braam cuivré plus brillant.')
def _(): return braam(3.0, 55, 3500, seed=62)
@add(F, 'DSGNBram', 'Braam Stab Short', 'Braam court (1 s), coup de poing sonore.')
def _(): return braam(1.0, 55, 2500, seed=63, att=0.02)
@add(F, 'DSGNBram', 'Braam Rising', 'Braam qui monte d’un ton (3,5 s) : tension grandissante.')
def _(): return braam(3.5, 49, 2200, rise=2, seed=64, att=0.4)

# =================================================================== 7. STINGERS / LOGO REVEAL (DSGNStngr)
F = 'Stinger / logo reveal'
def shimmer_chord(notes, dur=2.5, seed=0, wet=0.45):
    acc = silence(dur)
    for i, nn in enumerate(notes):
        b = bell(note(nn), dur, seed + i, bright=0.8, decay=1.4) * 0.6
        acc = place(acc, pan_curve(b, (i / max(len(notes) - 1, 1) - 0.5)), 0.012 * i)
    return reverb(acc, wet, 3.0, seed)
@add(F, 'DSGNStngr', 'Logo Reveal Corporate', 'Révélation de logo « corporate » : aspiration inversée → impact doux + accord cristallin.')
def _():
    sw = whoosh(0.9, 200, 3000, 0.95, seed=71, a_pow=2.5, wet=0)
    return seq([(0, sw * 0.7), (0.85, impact(71, 110, 45, 0.3, 0.3, 0.4, tail=1.0, wet=0.2) * 0.8),
                (0.85, shimmer_chord(['C5', 'E5', 'G5', 'B5', 'D6'], 3.0, 71))])
@add(F, 'DSGNStngr', 'Logo Reveal Tech', 'Révélation de logo tech : glitch → impact numérique + bips.')
def _():
    r = rng(72); g = silence(0.6)
    for k in range(10):
        d = r.uniform(0.01, 0.05)
        b = bitcrush(square(r.uniform(300, 2500), int(d * SR)) * 0.5, 5, 6)
        g = place(g, pan_curve(b, r.uniform(-0.7, 0.7)), k * 0.055)
    hit = impact(72, 160, 50, 0.25, 1.2, 0.7, tail=1.2, wet=0.25, dist=2.5)
    tail = seq([(0.05 * i, pan_curve(blip(note(nn), 0.06), 0.3 * (-1) ** i) * 0.25) for i, nn in enumerate(['E6', 'B6', 'E7', 'B6'])])
    return seq([(0, g * 0.6), (0.6, hit), (0.75, tail)])
@add(F, 'DSGNStngr', 'Logo Reveal Epic', 'Révélation épique : montée → impact bande-annonce + braam.')
def _():
    return seq([(0, noise_riser(1.5, seed=73) * 0.6), (1.5, impact(73, 130, 32, 0.6, 1.0, 0.8, tail=2.5, wet=0.3, dist=3)),
                (1.5, braam(2.5, 55, 1800, seed=73) * 0.6)])
@add(F, 'DSGNStngr', 'Logo Reveal Minimal', 'Révélation minimaliste : pop + ding propre.')
def _():
    return seq([(0, stereo(pop(300, 1200, 0.04, 0.03)) * 0.8),
                (0.06, reverb(fm_bell(note('E6'), 1.5, 1.4, 1.8, 0.5), 0.3, 1.5) * 0.7)])
@add(F, 'DSGNStngr', 'Logo Reveal Sparkle', 'Révélation magique : glissando scintillant → accord brillant.')
def _():
    gl = silence(0.6)
    sc = ['C6', 'D6', 'E6', 'G6', 'A6', 'C7', 'D7', 'E7', 'G7']
    for i, nn in enumerate(sc):
        gl = place(gl, pan_curve(bell(note(nn), 0.5, i, decay=0.25) * 0.4, -0.8 + 1.6 * i / len(sc)), 0.06 * i)
    return seq([(0, reverb(gl, 0.4, 2)), (0.55, shimmer_chord(['C5', 'G5', 'E6', 'G6'], 3.0, 75))])
@add(F, 'DSGNStngr', 'Whoosh Hit Logo', 'Whoosh + impact serré : apparition de logo dynamique.')
def _():
    return seq([(0, whoosh(0.5, 300, 4000, 0.85, seed=76, wet=0)), (0.45, impact(76, 150, 45, 0.25, 1.0, 0.8, tail=1.2, wet=0.2))])

# =================================================================== 8. TRANSITIONS (DSGNMorph / DSGNWhsh)
F = 'Transition'
@add(F, 'DSGNMorph', 'Tape Stop', 'Arrêt de bande (le son ralentit jusqu’à l’arrêt).', fade_out=0.05)
def _():
    pad = pad_chord([note('C3'), note('G3'), note('C4'), note('E4')], 2.0, 81, lp_hz=3000)
    n = int(1.2 * SR)
    rate = np.concatenate([np.ones(int(0.2 * SR)), np.linspace(1, 0.02, n) ** 1.5])
    return tape_warp(pad, rate)
@add(F, 'DSGNMorph', 'Tape Start', 'Démarrage de bande (le son accélère jusqu’à la vitesse normale).', fade_out=0.05)
def _():
    pad = pad_chord([note('C3'), note('G3'), note('C4'), note('E4')], 2.5, 82, lp_hz=3000)
    rate = np.concatenate([np.linspace(0.02, 1, int(1.0 * SR)) ** 1.5, np.ones(int(0.6 * SR))])
    return tape_warp(pad, rate)
@add(F, 'DSGNMorph', 'Glitch Transition', 'Transition glitch : hachures qui accélèrent + bitcrush (1 s).')
def _():
    r = rng(83); base = stereo(0.6 * saw(110, int(1.2 * SR)) + 0.4 * white(int(1.2 * SR), 83) / 3)
    out = silence(1.1); t0 = 0.0; k = 0
    while t0 < 1.0:
        L = max(0.012, 0.09 * (1 - t0)); st = r.integers(0, len(base) - int(L * SR) - 1)
        g = base[st:st + int(L * SR)] * (0.5 + 0.5 * r.random())
        g = np.stack([bitcrush(g[:, c], r.integers(3, 8), r.integers(2, 20)) for c in range(2)], 1)
        out = place(out, g, t0); t0 += L * r.uniform(1.0, 1.6); k += 1
    return lp(out, 9000)
@add(F, 'DSGNWhsh', 'Riser To Hit', 'Montée (1,5 s) qui débouche sur un impact : changement de scène fort.')
def _(): return seq([(0, noise_riser(1.5, seed=84) * 0.7), (1.5, impact(84, 130, 40, 0.4, 1.0, 0.7, tail=2.0, wet=0.3))])
@add(F, 'DSGNWhsh', 'Filter Sweep Transition', 'Balayage de filtre montant puis descendant (2 s).')
def _():
    n = int(2 * SR)
    s = pad_chord([note('A2'), note('E3'), note('A3'), note('C4')], 2.0, 85, lp_hz=20000) + stereo(0.3 * white(n, 85) / 3)
    fc = np.exp(curve([(0, np.log(200)), (0.55, np.log(9000)), (1, np.log(200))], n))
    s = np.stack([lp_sweep(s[:, c], fc, 1.0) for c in range(2)], 1)
    return s * env_swell(n, 0.55, 1.2, 1.2)[:, None]
@add(F, 'DSGNMorph', 'Swirl Morph', 'Tourbillon spatial (son qui tourne autour de l’auditeur), 1,8 s.')
def _():
    n = int(1.8 * SR); t = np.arange(n) / SR
    fc = 800 * 2 ** (1.5 * np.sin(2 * np.pi * 1.2 * t))
    y = spectral_band(pink(n, 86), fc, 0.6, env_swell(n, 0.5, 1.5, 1.5))
    return reverb(pan_curve(y / np.abs(y).max(), 0.9 * np.sin(2 * np.pi * 1.6 * t)), 0.25, 1.5)

# =================================================================== 9. DRONES (DSGNDron) — bouclables
F = 'Drone / nappe'
@add(F, 'DSGNDron', 'Drone Dark Loop', 'Nappe sombre et grave, bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); t = np.arange(n) / SR
    s = supersaw(41.2, n, 6, 10, 91) + 0.5 * supersaw(61.7, n, 4, 8, 92)
    fc = 250 + 150 * np.sin(2 * np.pi * 0.07 * t)
    s = np.stack([lp_sweep(s[:, c], fc, 0.5) for c in range(2)], 1) + 0.3 * stereo(lp(brown(n, 93), 180), 0.8)
    return loopify(reverb(s, 0.3, 3, tail=False), 0.5)
@add(F, 'DSGNDron', 'Drone Tense Loop', 'Nappe tendue (battements dissonants), bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); t = np.arange(n) / SR
    y = sine(220, n) + sine(233.1, n) + 0.6 * sine(330, n) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.2 * t))
    y += 0.4 * spectral_band(white(n, 94), 2000 * 2 ** (0.5 * np.sin(2 * np.pi * 0.05 * t)), 0.5)
    return loopify(reverb(stereo(y / np.abs(y).max(), 0.7), 0.35, 3, tail=False), 0.5)
@add(F, 'DSGNDron', 'Drone Ethereal Loop', 'Nappe éthérée et lumineuse, bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); t = np.arange(n) / SR
    acc = np.zeros((n, 2))
    for i, nn in enumerate(['A3', 'C#4', 'E4', 'B4', 'E5']):
        a = 0.6 + 0.4 * np.sin(2 * np.pi * (0.05 + 0.03 * i) * t + i)
        acc += pan_curve(sine(note(nn) * (1 + 0.002 * np.sin(2 * np.pi * 0.3 * t)), n) * a, -0.6 + 0.3 * i)
    return loopify(reverb(acc, 0.55, 4, tail=False), 0.5)
@add(F, 'DSGNDron', 'Drone Tech Hum Loop', 'Bourdonnement technologique, bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); t = np.arange(n) / SR
    y = sum(sine(50 * k, n) / k for k in range(1, 8)) * 0.5
    y += 0.5 * spectral_band(pink(n, 95), 700 * (1 + 0.2 * np.sin(2 * np.pi * 0.11 * t)), 1.0)
    return loopify(stereo(y / np.abs(y).max(), 0.6), 0.5)

# =================================================================== 10. AMBIANCES (AMBDsgn / AMBRoom / WINDDsgn / AMBTech / AMBSci)
F = 'Ambiance'
@add(F, 'AMBRoom', 'Room Tone Loop', 'Ambiance de pièce calme (fond neutre), bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR)
    y = lp(0.7 * brown(n, 101) + 0.3 * pink(n, 102), 900, 2) + 0.02 * (sine(50, n) + 0.5 * sine(100, n))
    return loopify(stereo(y / np.abs(y).max(), 1.0), 0.5)
@add(F, 'WINDDsgn', 'Wind Designed Loop', 'Vent synthétique avec rafales, bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); r = rng(103)
    walk = np.cumsum(r.normal(0, 1, 60)); walk = (walk - walk.min()) / (np.ptp(walk) + 1e-9)
    fc = np.exp(np.interp(np.linspace(0, 59, n), np.arange(60), np.log(300) + walk * np.log(4)))
    g = np.interp(np.linspace(0, 59, n), np.arange(60), 0.4 + 0.6 * np.roll(walk, 7))
    y = spectral_band(pink(n, 103), fc, 1.4, g) + 0.3 * spectral_band(pink(n, 104), fc * 2.5, 0.25, g ** 2)
    return loopify(stereo(y / np.abs(y).max(), 1.0), 0.5)
@add(F, 'AMBTech', 'HiTech Room Loop', 'Salle high-tech : ventilation, bourdonnement, petits bips, bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); r = rng(105)
    y = stereo(0.5 * lp(pink(n, 105), 2500) + 0.15 * sum(sine(60 * k, n) / k for k in range(1, 6)), 0.8)
    for k in range(9):
        y = place(y, pan_curve(blip(r.uniform(1500, 3500), 0.05) * 0.08, r.uniform(-0.8, 0.8)), r.uniform(0.3, 9.8))
    return loopify(y[:n], 0.5)
@add(F, 'AMBSci', 'SciFi Ambience Loop', 'Ambiance science-fiction : drone + gazouillis électroniques, bouclable (10 s).', loop=True)
def _():
    n = int(10.5 * SR); r = rng(106); t = np.arange(n) / SR
    y = stereo(0.6 * sine(55, n) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t)) + 0.4 * spectral_band(pink(n, 106), 400, 1.0), 0.8)
    for k in range(12):
        d = r.uniform(0.1, 0.4); m = int(d * SR)
        ch = fm(expcurve(r.uniform(800, 2000), r.uniform(800, 3000), m), 2.01, 2.0, m) * env_perc(m, 0.005, d / 3)
        y = place(y, pan_curve(ch * 0.12, r.uniform(-0.9, 0.9)), r.uniform(0.2, 9.8))
    return loopify(reverb(y[:n], 0.4, 3, tail=False), 0.5)

# =================================================================== 11. UI CLICKS (UIClick)
F = 'UI clic / tap'
@add(F, 'UIClick', 'Click Soft Tap', 'Tapotement doux (bouton, sélection discrète).')
def _(): return stereo(lp(click(900, 0.012, 0.4, 1500, 6000, 111), 7000))
@add(F, 'UIClick', 'Click Hard', 'Clic sec et net.')
def _(): return stereo(click(2400, 0.005, 0.7, 3000, 12000, 112))
@add(F, 'UIClick', 'Click Double', 'Double clic de souris.')
def _():
    c = click(2000, 0.005, 0.7, 2500, 10000, 113)
    return seq([(0, stereo(c)), (0.075, stereo(c * 0.8))])
@add(F, 'UIClick', 'Toggle On', 'Interrupteur ON (clic + petite note montante).')
def _(): return seq([(0, stereo(click(1800, 0.004, 0.6, seed=114))), (0.008, stereo(pop(700, 1300, 0.03, 0.03) * 0.5))])
@add(F, 'UIClick', 'Toggle Off', 'Interrupteur OFF (clic + petite note descendante).')
def _(): return seq([(0, stereo(click(1500, 0.004, 0.6, seed=115))), (0.008, stereo(pop(1200, 650, 0.03, 0.03) * 0.5))])
@add(F, 'UIClick', 'Hover Soft', 'Survol très léger (hover).')
def _(): return stereo(lp(sine(1500, int(0.06 * SR)) * env_adsr(int(0.06 * SR), 0.008, 0.01, 0.06, 0.04, 0.6), 4000) * 0.6)
@add(F, 'UIClick', 'Select Confirm', 'Sélection confirmée (clic + note brève).')
def _(): return seq([(0, stereo(click(2200, 0.004, 0.6, seed=117))), (0.005, stereo(blip(2093, 0.07) * 0.5))])
@add(F, 'UIClick', 'Keypress', 'Touche de clavier synthétique (« thock »).')
def _(): return stereo(click(3000, 0.006, 0.8, 1000, 5000, 118, body=0.6, body_f=180))
@add(F, 'UIClick', 'Scroll Tick', 'Petit tic de défilement (molette, liste).')
def _(): return stereo(click(4500, 0.002, 0.5, 4000, 12000, 119) * 0.8)
@add(F, 'UIClick', 'Glass Tick', 'Tic cristallin.')
def _():
    n = int(0.12 * SR)
    return stereo(mix((sine(4200, n) + 0.6 * sine(6810, n)) * env_perc(n, 0.0005, 0.03), 0.3 * click(5000, 0.002, 1.0, 5000, 14000, 120)))

# =================================================================== 12. POPS (TOONPop / UIMvmt)
F = 'Pop / bulle'
@add(F, 'TOONPop', 'Bubble Pop', 'Pop de bulle classique.')
def _(): return stereo(pop(300, 1100, 0.025, 0.035, seed=121))
@add(F, 'TOONPop', 'Pop Low', 'Pop grave et rond.')
def _(): return stereo(pop(140, 450, 0.03, 0.05, seed=122))
@add(F, 'TOONPop', 'Pop High', 'Pop aigu et vif.')
def _(): return stereo(pop(700, 2600, 0.02, 0.025, seed=123))
@add(F, 'TOONPop', 'Mouth Pop', 'Pop de bouche (feutré).')
def _(): return stereo(lp(pop(250, 700, 0.02, 0.03, seed=124, noise=0.15), 2500))
@add(F, 'UIMvmt', 'Pop Appear', 'Apparition d’élément (pop montant avec petite réverb).')
def _(): return reverb(pop(400, 1600, 0.07, 0.06, 0.6, 125), 0.2, 0.6)
@add(F, 'UIMvmt', 'Pop Disappear', 'Disparition d’élément (pop descendant).')
def _(): return reverb(pop(1400, 350, 0.07, 0.06, 0.6, 126), 0.2, 0.6)
@add(F, 'TOONPop', 'Bubble Cluster', 'Grappe de bulles (apparition de plusieurs éléments).')
def _():
    r = rng(127)
    return reverb(seq([(r.uniform(0, 0.45), pan_curve(pop(r.uniform(250, 600), r.uniform(900, 2200), 0.02, 0.03), r.uniform(-0.7, 0.7)) * r.uniform(0.5, 1)) for _ in range(7)]), 0.15, 0.6)
@add(F, 'TOONPop', 'Plop', 'Plop descendant (goutte, élément qui tombe).')
def _(): return stereo(pop(900, 250, 0.05, 0.04, 0.4, 128))

# =================================================================== 13. UI BEEPS / DATA (UIBeep / UIData)
F = 'UI bip / données'
@add(F, 'UIBeep', 'Beep Confirm', 'Bip de confirmation doux.')
def _(): return stereo(blip(1318.5, 0.09))
@add(F, 'UIBeep', 'Beep Double', 'Double bip.')
def _(): return seq([(0, stereo(blip(1046.5, 0.07))), (0.11, stereo(blip(1046.5, 0.07)))])
@add(F, 'UIBeep', 'HUD Beep', 'Bip d’interface HUD/hologramme (FM).')
def _(): return reverb(fm(2000, 3.5, 2.0, int(0.15 * SR), env_perc(int(0.15 * SR), 0.001, 0.03)) * env_perc(int(0.15 * SR), 0.002, 0.05), 0.15, 0.5)
@add(F, 'UIData', 'Data Chatter', 'Traitement de données : bips aléatoires rapides (1,2 s).')
def _():
    r = rng(134)
    return seq([(i / 40, pan_curve(blip(r.uniform(800, 3000), 0.022, 'square', 0.001, 0.005, 4000) * r.uniform(0.3, 0.8), r.uniform(-0.5, 0.5))) for i in range(48)])
@add(F, 'UIData', 'Computing Process', 'Ordinateur qui calcule : séquence de bips FM (2 s).')
def _():
    r = rng(135)
    ev = []
    for i in range(24):
        f = r.choice([1200, 1500, 1800, 2400]); m = int(0.06 * SR)
        ev.append((i * 0.085, pan_curve(fm(f, 2, 1.5, m) * env_perc(m, 0.001, 0.025) * 0.6, r.uniform(-0.4, 0.4))))
    return seq(ev)
@add(F, 'UIData', 'Scan Sweep', 'Balayage de scan (montée-descente avec trémolo), 1,2 s.')
def _():
    n = int(1.2 * SR); t = np.arange(n) / SR
    f = np.exp(curve([(0, np.log(500)), (0.5, np.log(3000)), (1, np.log(500))], n))
    y = sine(f, n) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * t)) * env_swell(n, 0.5, 0.8, 0.8)
    return reverb(stereo(y * 0.6), 0.2, 0.8)
@add(F, 'UIData', 'Text Typing Screen', 'Texte qui s’écrit à l’écran : tics rapides (1,5 s).')
def _():
    r = rng(137)
    return seq([(i / 18 + r.uniform(-0.01, 0.01), stereo(click(r.uniform(1500, 3000), 0.004, 0.5, seed=i) * r.uniform(0.5, 1))) for i in range(27)])
@add(F, 'UIData', 'Loading Loop', 'Chargement : motif de 3 notes en boucle (2 s).', loop=True)
def _():
    ev = [(i * 0.1667, stereo(blip(note(['E6', 'G6', 'B6'][i % 3]), 0.08) * 0.6)) for i in range(12)]
    return seq(ev, 2.0)[:int(2.0 * SR)]

# =================================================================== 14. NOTIFICATIONS / ALERTES (UIAlert)
F = 'Notification / alerte'
@add(F, 'UIAlert', 'Success Arpeggio', 'Succès : arpège majeur cristallin (validation, objectif atteint).')
def _(): return reverb(seq([(i * 0.08, stereo(fm_bell(note(nn), 1.2, 1.0, 1.2, 0.35) * 0.7)) for i, nn in enumerate(['C5', 'E5', 'G5', 'C6'])]), 0.3, 1.5)
@add(F, 'UIAlert', 'Error Buzz', 'Erreur : deux notes graves descendantes (refus, mauvaise réponse).')
def _(): return seq([(0, stereo(blip(330, 0.14, 'square', 0.002, 0.02, 1800) * 0.7)), (0.17, stereo(blip(262, 0.22, 'square', 0.002, 0.05, 1800) * 0.7))])
@add(F, 'UIAlert', 'Notification Ding', 'Ding de notification clair.')
def _(): return reverb(stereo(fm_bell(note('G6'), 1.5, 1.4, 2.0, 0.5)), 0.25, 1.2)
@add(F, 'UIAlert', 'Message Received', 'Message reçu : deux notes pincées montantes.')
def _(): return reverb(seq([(0, stereo(karplus(note('A5'), 0.5, 141, 0.993, 0.8))), (0.1, stereo(karplus(note('E6'), 0.6, 142, 0.993, 0.8)))]), 0.2, 1.0)
@add(F, 'UIAlert', 'Warning Triple', 'Avertissement : trois bips médium.')
def _(): return seq([(i * 0.18, stereo(blip(740, 0.1, 'square', 0.002, 0.02, 2500) * 0.6)) for i in range(3)])
@add(F, 'UIAlert', 'Level Up', 'Niveau supérieur : arpège rapide montant + scintillement.')
def _():
    a = seq([(i * 0.055, stereo(blip(note(nn), 0.07, 'tri', 0.002, 0.02, 6000) * 0.6)) for i, nn in enumerate(['C5', 'E5', 'G5', 'C6', 'E6', 'G6', 'C7'])])
    return place(reverb(a, 0.25, 1.2), sparkle_grains(0.6, 10, 145) * 0.4, 0.35)
@add(F, 'UIAlert', 'Reward Coin', 'Récompense / pièce : deux notes vives.')
def _(): return seq([(0, stereo(blip(note('G5'), 0.07, 'tri', 0.001, 0.01, 8000))), (0.07, stereo(blip(note('D6'), 0.3, 'tri', 0.001, 0.2, 8000)))])
@add(F, 'UIAlert', 'Like Heart', 'Like / cœur : petite note qui glisse vers le haut + cloche douce.')
def _(): return reverb(seq([(0, stereo(pop(500, 1000, 0.05, 0.05) * 0.6)), (0.05, stereo(fm_bell(note('C7'), 0.8, 2.0, 1.0, 0.3) * 0.4))]), 0.3, 1.0)

# =================================================================== 15. GLITCH (UIGlitch / DSGNRythm / DSGNDist)
F = 'Glitch / numérique'
@add(F, 'UIGlitch', 'Glitch Stutter', 'Glitch haché (bégaiement numérique), 0,6 s.')
def _():
    r = rng(151); g = 0.6 * saw(220, int(0.03 * SR)) + 0.4 * white(int(0.03 * SR), 151) / 3
    ev = []
    t0 = 0
    while t0 < 0.55:
        L = r.choice([0.015, 0.03, 0.045]); seg = np.resize(g, int(L * SR))
        ev.append((t0, pan_curve(bitcrush(seg, r.integers(4, 8), r.integers(2, 12)) * r.uniform(0.5, 1), r.uniform(-0.6, 0.6))))
        t0 += L * r.choice([1, 1, 1.5])
    return seq(ev)
@add(F, 'UIGlitch', 'Digital Burst', 'Rafale numérique courte (0,3 s).')
def _():
    n = int(0.3 * SR); r = rng(152)
    sh = np.repeat(r.uniform(-1, 1, n // 40 + 1), 40)[:n]
    y = bitcrush(0.5 * sh + 0.5 * white(n, 152) / 3, 4, 3) * env_perc(n, 0.001, 0.12)
    return stereo(lp(y, 10000), 0.8)
@add(F, 'UIGlitch', 'Data Corruption', 'Corruption de données : échantillonnage aléatoire changeant (0,8 s).')
def _():
    n = int(0.8 * SR); r = rng(153); out = np.zeros(n); i = 0
    while i < n:
        L = int(r.uniform(0.02, 0.08) * SR); step = r.integers(8, 120)
        vals = np.repeat(r.uniform(-1, 1, L // step + 1), step)[:L]
        out[i:i + L] = vals[:max(0, min(L, n - i))] * r.uniform(0.3, 1)
        i += L
    return stereo(bp(out, 200, 9000) * env_adsr(n, 0.005, 0.05, 0.8, 0.1, 0.8), 0.7)
@add(F, 'UIGlitch', 'Glitch Hit', 'Impact glitché (0,3 s).')
def _():
    h = impact(154, 160, 50, 0.12, 1.2, 0.8, tail=0.3, wet=0.0)
    return np.stack([bitcrush(h[:, c], 5, 10) for c in range(2)], 1)
@add(F, 'DSGNDist', 'Buzz Glitch', 'Bourdonnement électrique haché (0,5 s).')
def _():
    n = int(0.5 * SR); r = rng(155)
    gate = np.repeat(r.random(n // 600 + 1) > 0.35, 600)[:n].astype(float)
    y = sat(saw(60, n) + 0.5 * square(120, n), 3) * lp(gate, 300)
    return stereo(lp(y, 6000) * 0.8, 0.5)
@add(F, 'DSGNRythm', 'Rhythmic Glitch Loop', 'Boucle de glitchs rythmés (120 BPM, 2 s).', loop=True)
def _():
    r = rng(156); ev = []
    for i in range(32):
        if r.random() < 0.6:
            L = r.choice([0.02, 0.04, 0.06]); m = int(L * SR)
            kind = r.integers(0, 3)
            s = [click(r.uniform(1000, 5000), 0.006, 0.8, seed=i), bitcrush(square(r.uniform(200, 1500), m), 4, 6) * env_perc(m, 0.001, L / 2), hp(white(m, i), 3000) * env_perc(m, 0.001, 0.01)][kind]
            ev.append((i * 0.0625, pan_curve(s * 0.6, r.uniform(-0.7, 0.7))))
    return seq(ev, 2.0)[:int(2.0 * SR)]
@add(F, 'UIGlitch', 'Screen Static', 'Statique d’écran avec coupures (0,8 s).')
def _():
    n = int(0.8 * SR); r = rng(157)
    gate = lp(np.repeat(r.random(n // 900 + 1) > 0.25, 900)[:n].astype(float), 500)
    y = (white(n, 157) / 3 + 0.2 * sine(60, n)) * gate
    return stereo(bp(y, 300, 10000), 0.9)
@add(F, 'UIGlitch', 'VHS Wobble Glitch', 'Glitch VHS : note qui tangue + bruit + décrochages (1 s).')
def _():
    n = int(1.0 * SR); t = np.arange(n) / SR; r = rng(158)
    f = 440 * (1 + 0.03 * np.sin(2 * np.pi * 5 * t) + 0.02 * np.sin(2 * np.pi * 0.7 * t))
    gate = lp(np.repeat(r.random(n // 2400 + 1) > 0.15, 2400)[:n].astype(float), 200)
    y = (tri(f, n) * 0.6 + 0.25 * white(n, 158) / 3) * gate
    return stereo(lp(y, 5000), 0.6)

# =================================================================== 16. ÉLECTRIQUE / LASER / ÉNERGIE
F = 'Électrique / laser / énergie'
@add(F, 'ELECZap', 'Electric Zap', 'Décharge électrique « zap » (0,25 s).')
def _():
    n = int(0.25 * SR); r = rng(161)
    imp = (r.random(n) > 0.985) * r.uniform(-1, 1, n)
    y = bp(imp, 1500, 12000) * 2 + 0.6 * sine(expcurve(3000, 500, n, 0.5), n) + 0.4 * bp(white(n, 161), 2000, 8000) / 3
    return stereo(y * env_perc(n, 0.001, 0.08), 0.6)
@add(F, 'ELECSprk', 'Spark Crackle', 'Crépitement d’étincelles (1,2 s).')
def _():
    n = int(1.2 * SR); r = rng(162)
    imp = (r.random(n) > 0.995) * r.uniform(-1, 1, n) * (0.4 + 0.6 * r.random(n))
    y = hp(imp, 2000) + 0.1 * hp(white(n, 162), 6000) / 3
    return stereo(y * env_adsr(n, 0.01, 0.1, 1.2, 0.3, 0.7), 0.9)
@add(F, 'LASRGun', 'Laser Pew', 'Tir laser « pew » (0,2 s).')
def _():
    n = int(0.22 * SR)
    return reverb(fm(expcurve(2500, 250, n, 0.6), 0.5, 3.0, n, env_perc(n, 0.001, 0.08)) * env_perc(n, 0.001, 0.09), 0.15, 0.6)
@add(F, 'LASRGun', 'Laser Double', 'Double tir laser.')
def _():
    n = int(0.15 * SR)
    p = fm(expcurve(3200, 400, n, 0.6), 0.5, 2.5, n) * env_perc(n, 0.001, 0.06)
    return reverb(seq([(0, pan_curve(p, -0.4)), (0.12, pan_curve(p * 0.85, 0.4))]), 0.15, 0.6)
@add(F, 'SCIEnrg', 'Energy Charge', 'Charge d’énergie : sifflement qui monte (1,5 s).', fade_out=0.004)
def _():
    n = int(1.5 * SR)
    f = expcurve(200, 2200, n, 1.3)
    y = sine(f, n) + 0.4 * sine(f * 1.5, n)
    y *= (0.6 + 0.4 * np.sin(phase_from_freq(expcurve(5, 40, n)))) * np.linspace(0.1, 1, n) ** 1.5
    return reverb(stereo(y / np.abs(y).max() + 0.15 * hp(white(n, 165), 5000) / 3 * np.linspace(0, 1, n), 0.6), 0.2, 0.8, tail=False)
@add(F, 'SCIEnrg', 'Force Field Hum', 'Champ de force : bourdonnement modulé, bouclable (3 s).', loop=True)
def _():
    n = int(3.3 * SR); t = np.arange(n) / SR
    y = lp(saw(60 * (1 + 0.01 * np.sin(2 * np.pi * 3 * t)), n), 800) + 0.4 * sine(120, n) * (0.7 + 0.3 * np.sin(2 * np.pi * 6 * t))
    return loopify(stereo(y / np.abs(y).max(), 0.7), 0.3)
@add(F, 'SCIEnrg', 'Teleport', 'Téléportation : balayage scintillant montant-descendant (1,2 s).')
def _():
    n = int(1.2 * SR)
    f = np.exp(curve([(0, np.log(300)), (0.6, np.log(4000)), (1, np.log(1500))], n))
    y = fm(f, 1.5, 2.0, n) * env_swell(n, 0.6, 1.2, 1.5)
    return place(reverb(stereo(y * 0.6, 0.6), 0.3, 1.2), sparkle_grains(0.8, 14, 167) * 0.5, 0.3)

# =================================================================== 17. MAGIE (MAG*)
F = 'Magie / scintillement'
@add(F, 'MAGShim', 'Magic Sparkle', 'Scintillement magique (1,5 s) : paillettes, étoiles.')
def _(): return reverb(sparkle_grains(1.5, 40, 171), 0.45, 2.0)
@add(F, 'MAGPoof', 'Magic Poof', 'Pouf magique : bouffée + scintillement (apparition/disparition).')
def _():
    n = int(0.4 * SR)
    pf = spectral_band(white(n, 172), 3500, 1.5, env_swell(n, 0.2, 1, 2))
    return reverb(place(stereo(pf / np.abs(pf).max(), 0.8), sparkle_grains(0.7, 18, 172) * 0.6, 0.05), 0.4, 1.5)
@add(F, 'MAGShim', 'Fairy Glissando', 'Glissando féerique montant (0,7 s).')
def _():
    sc = ['C6', 'D6', 'E6', 'G6', 'A6', 'C7', 'D7', 'E7', 'G7', 'A7', 'C8']
    return reverb(seq([(0.06 * i, pan_curve(bell(note(nn), 0.6, i, decay=0.2) * 0.5, -0.8 + 1.6 * i / len(sc))) for i, nn in enumerate(sc)]), 0.45, 2.0)
@add(F, 'MAGShim', 'Twinkle', 'Trois notes scintillantes isolées.')
def _(): return reverb(seq([(0.18 * i, pan_curve(bell(note(nn), 0.8, i, decay=0.3) * 0.6, [-0.5, 0.5, 0][i])) for i, nn in enumerate(['E7', 'B7', 'G7'])]), 0.45, 2.0)
@add(F, 'MAGMisc', 'Wand Swish', 'Coup de baguette magique : swish + scintillement.')
def _(): return reverb(place(swish(0.3, 2000, 9000, seed=175), sparkle_grains(0.6, 15, 175) * 0.6, 0.12), 0.35, 1.5)
@add(F, 'MAGAngl', 'Angelic Swell', 'Nappe angélique qui gonfle (2,5 s).')
def _():
    p = pad_chord([note(n) for n in ['C4', 'G4', 'C5', 'E5', 'G5']], 2.5, 176, kind='sine', vib=0.004)
    return reverb(p * env_swell(len(p), 0.6, 1.5, 1.2)[:, None], 0.55, 3.0)

# =================================================================== 18. CARTOON (TOON*)
F = 'Cartoon / fun'
@add(F, 'TOONBoing', 'Boing Spring', 'Boing de ressort (rebond cartoon).')
def _():
    n = int(0.7 * SR); t = np.arange(n) / SR
    f = 160 + 110 * np.exp(-t / 0.25) * np.sin(2 * np.pi * 9 * t)
    y = sat(sine(f, n) + 0.4 * sine(f * 2, n), 1.5) * env_perc(n, 0.002, 0.25)
    return stereo(y)
@add(F, 'TOONWhis', 'Slide Whistle Up', 'Sifflet à coulisse montant.')
def _():
    n = int(0.7 * SR); t = np.arange(n) / SR
    f = expcurve(500, 1800, n, 1.0) * (1 + 0.015 * np.sin(2 * np.pi * 6 * t))
    y = sine(f, n) * env_adsr(n, 0.03, 0.05, 0.7, 0.08, 0.85) + 0.05 * bp(white(n, 182), 1500, 5000)
    return stereo(y)
@add(F, 'TOONWhis', 'Slide Whistle Down', 'Sifflet à coulisse descendant (chute).')
def _():
    n = int(0.8 * SR); t = np.arange(n) / SR
    f = expcurve(1800, 400, n, 1.0) * (1 + 0.015 * np.sin(2 * np.pi * 6 * t))
    return stereo(sine(f, n) * env_adsr(n, 0.03, 0.05, 0.8, 0.1, 0.85))
@add(F, 'TOONPluk', 'Pluck Cartoon', 'Corde pincée cartoon (petit pas furtif).')
def _(): return stereo(karplus(note('E4'), 0.6, 184, 0.992, 0.6))
@add(F, 'TOONTwang', 'Twang Ruler', 'Twang de règle qui vibre.')
def _():
    k = karplus(98, 1.2, 185, 0.998, 0.7)
    t = np.arange(len(k)) / SR
    rate = 1 + 0.05 * np.exp(-t / 0.5) * np.sin(2 * np.pi * 7 * t)
    return tape_warp(stereo(k), rate)
@add(F, 'TOONSqk', 'Squeak', 'Couinement (jouet, petit personnage).')
def _():
    n = int(0.09 * SR)
    f = np.exp(curve([(0, np.log(2500)), (0.4, np.log(3600)), (1, np.log(2800))], n))
    s = sine(f, n) * env_swell(n, 0.3, 1, 1.5)
    return seq([(0, stereo(s)), (0.12, stereo(s * 0.8))])
@add(F, 'TOONImpt', 'Bonk', 'Bonk cartoon (coup sur la tête, objet qui tape).')
def _():
    n = int(0.25 * SR); t = np.arange(n) / SR
    y = sine(600 * np.exp(-t / 0.08) + 300, n) * env_perc(n, 0.001, 0.05) + 0.6 * spectral_band(white(n, 187), 900, 0.3) * env_perc(n, 0.0005, 0.03) * 4
    return stereo(y)

# =================================================================== 19. TONAL / MUSICAL (MUSC* / DSGNTonl)
F = 'Tonal / musical'
@add(F, 'MUSCSynth', 'Synth Stab Chord', 'Accord synthé court (stab), accent musical.')
def _():
    n = int(0.6 * SR)
    s = sum(supersaw(note(nn), n, 5, 12, i) for i, nn in enumerate(['C4', 'E4', 'G4', 'B4']))
    s = np.stack([lp_sweep(s[:, c], expcurve(6000, 600, n, 0.5), 0.5) for c in range(2)], 1)
    return reverb(s * env_perc(n, 0.002, 0.25)[:, None], 0.3, 1.5)
@add(F, 'MUSCBell', 'Bell Hit', 'Coup de cloche tonale (3 s).')
def _(): return reverb(stereo(bell(note('C5'), 3.0, 192, decay=1.5)), 0.3, 2.5)
@add(F, 'MUSCTnprc', 'Marimba Note', 'Note de marimba (mallet doux).')
def _():
    n = int(1.0 * SR); f = note('G4')
    y = sine(f, n) * env_perc(n, 0.001, 0.35) + 0.4 * sine(f * 3.93, n) * env_perc(n, 0.001, 0.08) + 0.15 * sine(f * 9.2, n) * env_perc(n, 0.001, 0.02)
    return reverb(stereo(y), 0.2, 1.0)
@add(F, 'MUSCChim', 'Wind Chimes', 'Carillon à vent (2,5 s).')
def _():
    r = rng(194)
    return reverb(seq([(r.uniform(0, 1.2), pan_curve(bell(note(r.choice(['C6', 'D6', 'E6', 'G6', 'A6', 'C7'])), 1.5, i, decay=0.8) * r.uniform(0.3, 0.7), r.uniform(-0.8, 0.8))) for i in range(12)]), 0.4, 2.5)
@add(F, 'MUSCStngr', 'Musical Sting Up', 'Petite phrase musicale montante (3 notes), ponctuation positive.')
def _(): return reverb(seq([(0, stereo(karplus(note('G4'), 0.5, 195, 0.995, 0.7))), (0.14, stereo(karplus(note('C5'), 0.5, 196, 0.995, 0.7))), (0.28, stereo(karplus(note('E5'), 1.4, 197, 0.997, 0.7)))]), 0.25, 1.5)
@add(F, 'DSGNTonl', 'Tonal Sub Hit', 'Impact tonal : basse + harmoniques de cloche qui résonnent.')
def _():
    n = int(2.5 * SR)
    y = sine(note('C2'), n) * env_perc(n, 0.002, 0.8) + 0.5 * bell(note('C4'), 2.5, 198, decay=1.2)
    return reverb(stereo(sat(y / np.abs(y).max(), 1.5)), 0.3, 2.5)

# =================================================================== 20. TEMPS / COMPTEURS (CLOCKTick / BEEPTimer / UIData)
F = 'Horloge / compteur'
@add(F, 'CLOCKTick', 'Clock Tick Loop', 'Tic-tac d’horloge, bouclable (4 s).', loop=True)
def _():
    return seq([(i * 0.5, stereo(click(3000 if i % 2 == 0 else 2400, 0.004, 0.6, 1500, 8000, i, body=0.3, body_f=900) * 0.8)) for i in range(8)], 4.0)[:int(4 * SR)]
@add(F, 'BEEPTimer', 'Countdown 3 2 1', 'Compte à rebours : 3 bips + bip long (départ).')
def _(): return seq([(i, stereo(blip(880, 0.12) * 0.7)) for i in range(3)] + [(3.0, stereo(blip(1760, 0.6, 'sine', 0.003, 0.15) * 0.8))])
@add(F, 'UIData', 'Score Counter Rollup', 'Compteur de score qui défile (accélère, monte) puis ding final.')
def _():
    ev = []; t0 = 0.0; i = 0
    while t0 < 1.4:
        rate = 8 + 40 * (t0 / 1.4); f = 1500 + 1500 * t0 / 1.4
        ev.append((t0, stereo(click(f, 0.003, 0.4, seed=i) * 0.6))); t0 += 1 / rate; i += 1
    ev.append((1.45, reverb(stereo(fm_bell(note('C7'), 1.2, 1.4, 1.5, 0.4)), 0.3, 1.2)))
    return seq(ev)
@add(F, 'BEEPTimer', 'Timer Tick Fast', 'Minuteur : tics rapides (10 tics).')
def _(): return seq([(i * 0.12, stereo(blip(2000, 0.02, 'square', 0.001, 0.005, 6000) * 0.5)) for i in range(10)])
@add(F, 'MECHClik', 'Stopwatch Click', 'Chronomètre : déclic mécanique double.')
def _(): return seq([(0, stereo(click(3500, 0.003, 0.9, 2000, 10000, 205, body=0.4, body_f=1200))), (0.05, stereo(click(2800, 0.003, 0.9, 2000, 10000, 206) * 0.6))])

# =================================================================== 21. CŒUR / PULSATIONS (HMNHart)
F = 'Battement / pulsation'
def heartbeat(bpm, beats, seed=0):
    lub = lp(sine(expcurve(65, 40, int(0.2 * SR), 0.5), int(0.2 * SR)) * env_perc(int(0.2 * SR), 0.004, 0.06), 200)
    return reverb(seq([(i * 60 / bpm + d, stereo(lub * a)) for i in range(beats) for d, a in [(0, 1.0), (0.17, 0.7)]]), 0.1, 0.6)
@add(F, 'HMNHart', 'Heartbeat Calm', 'Battement de cœur calme (70 BPM, 4 battements).')
def _(): return heartbeat(70, 4, 211)
@add(F, 'HMNHart', 'Heartbeat Fast', 'Battement de cœur rapide (130 BPM), suspense.')
def _(): return heartbeat(130, 6, 212)

# =================================================================== 22. ÉNERGIE / MACHINE (SCIMach)
F = 'Power up / down'
@add(F, 'SCIMach', 'Power Up', 'Mise sous tension : montée + sifflement + déclic (1,6 s).')
def _():
    n = int(1.5 * SR)
    f = expcurve(40, 400, n, 1.2)
    y = lp_sweep(saw(f, n), f * 6, 0.5) * np.linspace(0.2, 1, n) + 0.3 * sine(f * 7.5, n) * np.linspace(0, 1, n) ** 2
    y = stereo(y / np.abs(y).max(), 0.5)
    return place(y, stereo(click(2500, 0.005, 0.8, body=0.5, body_f=150)), 1.5)
@add(F, 'SCIMach', 'Power Down', 'Mise hors tension : descente qui s’éteint (1,6 s).')
def _():
    n = int(1.6 * SR)
    f = expcurve(400, 25, n, 0.7)
    y = lp_sweep(saw(f, n), f * 6, 0.5) * np.linspace(1, 0, n) ** 1.2 + 0.3 * sine(f * 7.5, n) * np.linspace(1, 0, n) ** 2
    return stereo(y / np.abs(y).max(), 0.5)
@add(F, 'SCIMach', 'Servo Motion', 'Petit servo / mécanisme robotique (0,6 s).')
def _():
    n = int(0.6 * SR); t = np.arange(n) / SR
    f = curve([(0, 600), (0.2, 900), (0.8, 900), (1, 500)], n)
    y = lp(square(f, n), 3000) * env_adsr(n, 0.02, 0.02, 0.6, 0.08, 0.8) * (0.8 + 0.2 * np.sin(2 * np.pi * 40 * t))
    return stereo(y * 0.6, 0.4)
