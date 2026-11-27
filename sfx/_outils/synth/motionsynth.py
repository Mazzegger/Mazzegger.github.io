"""Petit moteur de synthèse sonore pour effets de motion design (numpy/scipy)."""
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt, sosfiltfilt, resample_poly

SR = 48000
N_FFT = 2048
HOP = 256


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def rng(seed):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------- courbes
def curve(points, n):
    """points: liste (temps_normalisé 0..1, valeur) -> courbe de n échantillons (interp. linéaire)."""
    p = np.array(points, dtype=float)
    return np.interp(np.linspace(0, 1, n), p[:, 0], p[:, 1])


def expcurve(v0, v1, n, shape=1.0):
    """Interpolation exponentielle (utile pour les fréquences)."""
    x = np.linspace(0, 1, n) ** shape
    return v0 * (v1 / v0) ** x


def env_adsr(n, a, d, s, r, sustain_level=0.7):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    s_len = max(n - a - d - r, 0)
    e = np.concatenate([np.linspace(0, 1, a, endpoint=False) if a else [],
                        np.linspace(1, sustain_level, d, endpoint=False) if d else [],
                        np.full(s_len, sustain_level),
                        np.linspace(sustain_level, 0, r) if r else []])
    return np.pad(e, (0, max(0, n - len(e))))[:n]


def env_perc(n, attack=0.002, decay=0.3, curve_pow=1.0):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-5), 0, 1)
    d = np.exp(-np.maximum(t - attack, 0) / max(decay, 1e-5)) ** curve_pow
    e = a * d
    k = max(int(n * 0.2), 1)                      # fin garantie à zéro
    e[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2
    return e


def env_swell(n, peak=0.6, a_pow=2.0, r_pow=1.5):
    """Montée puis descente, pic à `peak` (0..1)."""
    x = np.linspace(0, 1, n)
    up = np.clip(x / peak, 0, 1) ** a_pow
    down = np.clip((1 - x) / (1 - peak), 0, 1) ** r_pow
    return np.where(x <= peak, up, down)


# ---------------------------------------------------------------- bruits
def white(n, seed=0):
    return rng(seed).standard_normal(n)


def pink(n, seed=0):
    X = np.fft.rfft(white(n, seed))
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = f[1]
    y = np.fft.irfft(X / np.sqrt(f), n)
    return y / (np.abs(y).max() + 1e-12)


def brown(n, seed=0):
    X = np.fft.rfft(white(n, seed))
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = f[1]
    y = np.fft.irfft(X / f, n)
    y = sosfilt(butter(1, 15, 'hp', fs=SR, output='sos'), y)
    return y / (np.abs(y).max() + 1e-12)


# ---------------------------------------------------------------- filtres
def _stft(x):
    import librosa
    return librosa.stft(x, n_fft=N_FFT, hop_length=HOP)


def _istft(X, n):
    import librosa
    return librosa.istft(X, hop_length=HOP, length=n)


def spectral_band(x, fc, bw_oct, gain=None, shape='gauss'):
    """Filtre passe-bande variable dans le temps (fc, bw_oct: scalaires ou courbes de len(x))."""
    n = len(x)
    X = _stft(x)
    nf, nt = X.shape
    freqs = np.fft.rfftfreq(N_FFT, 1 / SR)[:, None]
    freqs[0] = 1.0
    tf = np.clip(np.arange(nt) * HOP, 0, n - 1)
    fc_t = (np.interp(tf, np.arange(n), fc) if np.ndim(fc) else np.full(nt, fc))[None, :]
    bw_t = (np.interp(tf, np.arange(n), bw_oct) if np.ndim(bw_oct) else np.full(nt, bw_oct))[None, :]
    d = np.log2(freqs / fc_t) / (bw_t / 2)
    M = np.exp(-0.5 * d ** 2 * 2.77) if shape == 'gauss' else 1 / (1 + d ** 4)
    if gain is not None:
        M = M * (np.interp(tf, np.arange(n), gain)[None, :])
    return _istft(X * M, n)


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR / 2 - 100), 'lp', fs=SR, output='sos'), x, axis=0)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'hp', fs=SR, output='sos'), x, axis=0)


def bp(x, f1, f2, order=2):
    return sosfilt(butter(order, [f1, min(f2, SR / 2 - 100)], 'bp', fs=SR, output='sos'), x, axis=0)


def lp_sweep(x, fc_curve, res=0.0):
    """Passe-bas variable (via masque spectral, pente 24 dB/oct + bosse de résonance optionnelle)."""
    n = len(x)
    X = _stft(x)
    nf, nt = X.shape
    freqs = np.fft.rfftfreq(N_FFT, 1 / SR)[:, None]
    tf = np.clip(np.arange(nt) * HOP, 0, n - 1)
    fc_t = np.interp(tf, np.arange(n), fc_curve)[None, :]
    r = freqs / fc_t
    M = 1 / np.sqrt(1 + r ** 8)
    if res > 0:
        M = M * (1 + res * np.exp(-0.5 * (np.log2(r + 1e-9) / 0.15) ** 2))
    return _istft(X * M, n)


# ---------------------------------------------------------------- oscillateurs
def phase_from_freq(freq):
    return 2 * np.pi * np.cumsum(freq) / SR


def sine(freq, n=None, phase0=0.0):
    if np.ndim(freq) == 0:
        freq = np.full(n, float(freq))
    return np.sin(phase_from_freq(freq) + phase0)


def _naive(kind, freq, os=4):
    f = np.repeat(freq, os) if np.ndim(freq) else freq
    ph = np.cumsum(f) / (SR * os)
    ph = ph - np.floor(ph)
    if kind == 'saw':
        y = 2 * ph - 1
    elif kind == 'square':
        y = np.where(ph < 0.5, 1.0, -1.0)
    elif kind == 'tri':
        y = 4 * np.abs(ph - 0.5) - 1
    return resample_poly(y, 1, os)


def saw(freq, n=None):
    if np.ndim(freq) == 0:
        freq = np.full(n, float(freq))
    return _naive('saw', freq)[:len(freq)]


def square(freq, n=None):
    if np.ndim(freq) == 0:
        freq = np.full(n, float(freq))
    return _naive('square', freq)[:len(freq)]


def tri(freq, n=None):
    if np.ndim(freq) == 0:
        freq = np.full(n, float(freq))
    return _naive('tri', freq)[:len(freq)]


def supersaw(freq, n, voices=7, detune_cents=18, seed=0, stereo=True):
    r = rng(seed)
    base = np.full(n, float(freq)) if np.ndim(freq) == 0 else freq
    L = np.zeros(n); R = np.zeros(n)
    for v in range(voices):
        c = (v - (voices - 1) / 2) / ((voices - 1) / 2 + 1e-9) * detune_cents
        y = np.roll(saw(base * 2 ** (c / 1200)), r.integers(0, 2000))
        pan = 0.5 + 0.45 * (v / (voices - 1) - 0.5) * 2 if stereo else 0.5
        L += y * np.cos(pan * np.pi / 2); R += y * np.sin(pan * np.pi / 2)
    return np.stack([L, R], 1) / voices


def fm(carrier, ratio, index, n, index_env=None):
    """FM 2 opérateurs. carrier: Hz (scalaire ou courbe)."""
    fc = np.full(n, float(carrier)) if np.ndim(carrier) == 0 else carrier
    mod = np.sin(phase_from_freq(fc * ratio))
    I = index * (index_env if index_env is not None else 1.0)
    return np.sin(phase_from_freq(fc) + I * mod)


def bell(freq, dur, seed=0, bright=1.0, decay=1.2, partials=None):
    """Cloche additive inharmonique."""
    n = int(dur * SR)
    partials = partials or [(0.56, 1.0, 1.0), (0.92, 0.6, 0.8), (1.0, 1.0, 1.0), (1.19, 0.5, 0.6),
                            (1.71, 0.45, 0.5), (2.0, 0.6, 0.45), (2.74, 0.35 * bright, 0.35),
                            (3.0, 0.3 * bright, 0.3), (3.76, 0.25 * bright, 0.22), (4.07, 0.2 * bright, 0.2)]
    y = np.zeros(n)
    r = rng(seed)
    for ratio, amp, dec in partials:
        y += amp * sine(freq * ratio * (1 + r.normal(0, 0.0007)), n, r.uniform(0, 6.28)) * env_perc(n, 0.001, decay * dec)
    return tailfade(y / (np.abs(y).max() + 1e-12))


def karplus(freq, dur, seed=0, damp=0.996, bright=0.5):
    n = int(dur * SR)
    p = max(int(SR / freq), 2)
    buf = rng(seed).uniform(-1, 1, p)
    buf = lp(buf, 800 + 9000 * bright, 1)
    y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % p]
        buf[i % p] = damp * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return tailfade(y)


# ---------------------------------------------------------------- effets
def stereo(x, width=0.0, seed=0):
    """Mono -> stéréo, avec élargissement par décorrélation (all-pass approx. par léger délai filtré)."""
    if x.ndim == 2:
        return x
    if width <= 0:
        return np.stack([x, x], 1)
    d = int(0.0004 * SR + 0.012 * SR * width * 0.5)
    side = np.concatenate([np.zeros(d), x[:-d]]) - x
    side = hp(side, 300)
    return np.stack([x + width * 0.5 * side, x - width * 0.5 * side], 1)


def pan_curve(x, pan):
    """x mono, pan: -1..1 (scalaire ou courbe) -> stéréo loi à puissance constante."""
    p = (np.asarray(pan) + 1) / 2 * np.pi / 2
    return np.stack([x * np.cos(p), x * np.sin(p)], 1)


def doppler(x, pan_path, max_delay_ms=1.2):
    """Déplacement gauche->droite avec décalage interaural."""
    n = len(x)
    p = np.asarray(pan_path) if np.ndim(pan_path) else np.full(n, pan_path)
    L = x * np.cos((p + 1) / 2 * np.pi / 2)
    R = x * np.sin((p + 1) / 2 * np.pi / 2)
    dl = np.clip(p, 0, 1) * max_delay_ms * SR / 1000   # source à droite => gauche retardée
    dr = np.clip(-p, 0, 1) * max_delay_ms * SR / 1000
    idx = np.arange(n)
    L = np.interp(idx - dl, idx, L, left=0)
    R = np.interp(idx - dr, idx, R, left=0)
    return np.stack([L, R], 1)


def make_ir(dur=2.0, seed=0, damp_hz=6000, predelay=0.01, decay_lo=None):
    """Réponse impulsionnelle synthétique stéréo : bruit à décroissance exponentielle,
    plus sombre avec le temps."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = []
    for c in range(2):
        nz = white(n, seed + 31 * c)
        e = np.exp(-t * 6.9 / dur)
        y = nz * e
        # assombrissement progressif : mélange passe-bas croissant
        dark = lp(y, damp_hz * 0.25, 2)
        mix = np.clip(t / dur * 1.5, 0, 1)
        y = (1 - mix) * lp(y, damp_hz, 2) + mix * dark
        y = np.concatenate([np.zeros(int(predelay * SR)), y])
        out.append(y)
    ir = np.stack(out, 1)
    return ir / np.sqrt((ir ** 2).sum(0)).max()


def reverb(x, wet=0.3, dur=2.0, seed=7, damp_hz=6000, predelay=0.012, tail=True):
    xs = stereo(x) if x.ndim == 1 else x
    ir = make_ir(dur, seed, damp_hz, predelay)
    pad = int(dur * SR) if tail else 0
    xs = np.pad(xs, ((0, pad), (0, 0)))
    w = np.stack([fftconvolve(xs[:, c], ir[:, c])[:len(xs)] for c in range(2)], 1)
    w *= np.sqrt((xs ** 2).mean() / ((w ** 2).mean() + 1e-12))
    return (1 - wet) * xs + wet * w


def tailfade(y, frac=0.25):
    """Fondu cos² sur la dernière fraction : garantit une fin à zéro."""
    y = np.array(y, dtype=float)
    k = max(int(len(y) * frac), 1)
    w = np.cos(np.linspace(0, np.pi / 2, k)) ** 2
    y[-k:] *= w[:, None] if y.ndim == 2 else w
    return y


def sat(x, drive=2.0):
    return np.tanh(drive * x) / np.tanh(drive)


def bitcrush(x, bits=6, down=8):
    q = 2 ** (bits - 1)
    y = np.round(x * q) / q
    idx = (np.arange(len(y)) // down) * down
    return y[idx]


def delay(x, time=0.25, fb=0.35, mix=0.3, n_rep=6):
    xs = stereo(x) if x.ndim == 1 else x
    d = int(time * SR)
    out = np.pad(xs, ((0, d * n_rep), (0, 0)))
    acc = out.copy()
    for k in range(1, n_rep + 1):
        sh = np.zeros_like(out)
        sh[d * k:] = out[:len(out) - d * k] * (fb ** k)
        if k % 2:
            sh = sh[:, ::-1]  # ping-pong
        acc += mix * sh
    return acc


def place(dst, src, at):
    """Ajoute src dans dst à l'instant `at` (s), en agrandissant si besoin."""
    i = int(at * SR)
    src = stereo(src) if src.ndim == 1 else src
    dst = stereo(dst) if dst.ndim == 1 else dst
    need = i + len(src)
    if need > len(dst):
        dst = np.pad(dst, ((0, need - len(dst)), (0, 0)))
    dst[i:i + len(src)] += src
    return dst


def silence(dur):
    return np.zeros((int(dur * SR), 2))


def loopify(x, xfade=0.5):
    """Rend un son bouclable : fondu enchaîné fin->début."""
    xs = stereo(x) if x.ndim == 1 else x
    f = int(xfade * SR)
    head, body, tail = xs[:f], xs[f:-f] if f else xs, xs[-f:]
    w = np.sin(np.linspace(0, np.pi / 2, f))[:, None]
    mixed = tail * np.cos(np.linspace(0, np.pi / 2, f))[:, None] + head * w
    return np.concatenate([mixed, xs[f:-f]], 0)


def finalize(x, peak_db=-1.0, fade_in=0.002, fade_out=0.02, trim_db=-70, loop=False):
    xs = stereo(x) if x.ndim == 1 else x.copy()
    sos = butter(2, 20, 'hp', fs=SR, output='sos')
    if loop:   # filtrage circulaire : préserve la continuité du bouclage
        n0 = len(xs)
        xs = sosfiltfilt(sos, np.concatenate([xs, xs, xs], 0), axis=0)[n0:2 * n0]
    else:
        xs = sosfiltfilt(sos, xs, axis=0)
    if not loop:
        # rogner la fin silencieuse
        e = np.abs(xs).max(1)
        thr = e.max() * 10 ** (trim_db / 20)
        last = np.where(e > thr)[0]
        if len(last):
            xs = xs[:min(len(xs), last[-1] + int(0.01 * SR))]
        if fade_out >= 0.01:
            m = np.abs(xs).max(1)
            tail = m[-int(0.05 * SR):].max() / (m.max() + 1e-12)
            if tail > 10 ** (-45 / 20):
                xs = tailfade(xs, 0.25)
        fi, fo = int(fade_in * SR), int(fade_out * SR)
        if fi:
            xs[:fi] *= np.linspace(0, 1, fi)[:, None]
        if fo:
            xs[-fo:] *= (np.linspace(1, 0, fo) ** 2)[:, None]
    xs *= 10 ** (peak_db / 20) / (np.abs(xs).max() + 1e-12)
    return xs.astype(np.float32)
