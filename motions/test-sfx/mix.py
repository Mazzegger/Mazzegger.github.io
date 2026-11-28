"""Mixe la bande son à partir de timeline.CUES (synchro automatique sur l'attaque / le pic / la fin)."""
import sys, os, json
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import CUES, DUR

SR = 48000


def env(y, hop=96):
    m = np.abs(y).max(1)
    n = len(m) // hop
    return np.sqrt((m[:n * hop].reshape(n, hop) ** 2).mean(1)), hop


def sync_offset(y, mode):
    """Instant (s) dans le fichier qui doit tomber sur le repère."""
    if mode == 'start':
        return 0.0
    if mode == 'end':
        return len(y) / SR
    e, hop = env(y)
    if mode == 'peak':
        k = np.convolve(e, np.ones(9) / 9, 'same')
        return int(np.argmax(k)) * hop / SR
    if mode == 'hit':     # transitoire principal : forte montée vers un niveau proche du maximum
        m = np.abs(y).max(1); h = 96; n = len(m) // h          # trames de 2 ms
        db = 20 * np.log10(np.sqrt((m[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
        pad = np.concatenate([np.full(30, -120.0), db])
        best, bi = -1, 0
        for i in range(n - 15):
            nxt = db[i:i + 15].mean(); prev = pad[i:i + 30].max()
            if nxt > db.max() - 8 and nxt - prev > best:
                best, bi = nxt - prev, i
        return bi * h / SR
    raise ValueError(mode)


if __name__ == '__main__':
    SFX, OUT = sys.argv[1], sys.argv[2]
    mixbuf = np.zeros((int((DUR + 4) * SR), 2))
    report = []
    for f, t, mode, gdb, opt in CUES:
        y, sr = sf.read(os.path.join(SFX, f), always_2d=True)
        assert sr == SR, f
        if opt.get('loop_to'):
            reps = int(np.ceil(opt['loop_to'] * SR / len(y)))
            y = np.tile(y, (reps, 1))[:int(opt['loop_to'] * SR)]
        off = sync_offset(y, mode)
        if opt.get('cut'):
            n = int(opt['cut'] * SR); y = y[:n].copy()
            fo = int(0.04 * SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
        if opt.get('fade_in'):
            n = int(opt['fade_in'] * SR); y[:n] *= np.linspace(0, 1, n)[:, None]
        if opt.get('fade_out'):
            n = int(opt['fade_out'] * SR); y[-n:] *= np.linspace(1, 0, n)[:, None]
        start = t - off
        y = y * 10 ** (gdb / 20)
        i = int(round(start * SR))
        if i < 0:
            y = y[-i:]; i = 0
        mixbuf[i:i + len(y)] += y[:len(mixbuf) - i]
        report.append(dict(file=os.path.basename(f), cue=round(t, 3), mode=mode, sync_in_file=round(off, 3), placed_at=round(start, 3), gain_db=gdb))

    mixbuf = mixbuf[:int(DUR * SR)]
    # bus master : limiteur doux puis crête à -1 dBFS
    pk = np.abs(mixbuf).max()
    x = mixbuf / pk * 1.6
    x = np.tanh(x) / np.tanh(1.6)
    x *= 10 ** (-1 / 20) / np.abs(x).max()
    fo = int(0.3 * SR); x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    sf.write(OUT, x, SR, subtype='PCM_24')
    json.dump(report, open(OUT.replace('.wav', '_cues.json'), 'w'), indent=1, ensure_ascii=False)
    for r in report:
        print('%-55s repère %5.2f  %-5s  synchro@%.3f  placé %6.3f  %+d dB' % (r['file'][:55], r['cue'], r['mode'], r['sync_in_file'], r['placed_at'], r['gain_db']))
