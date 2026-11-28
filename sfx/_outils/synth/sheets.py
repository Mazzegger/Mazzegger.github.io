import json, sys, os, numpy as np, soundfile as sf, librosa
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = sys.argv[1]; outp = sys.argv[2]; M = json.load(open(f'{d}/_meta.json'))
per = 12
for k in range(0, len(M), per):
    chunk = M[k:k + per]
    fig, axs = plt.subplots(3, 4, figsize=(20, 11), dpi=100)
    for ax, m in zip(axs.flat, chunk):
        y, sr = sf.read(f'{d}/{m["tmp"]}'); mo = y.mean(1)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(mo, n_fft=1024, hop_length=128)) / 256)
        fr = librosa.fft_frequencies(sr=sr, n_fft=1024); tt = np.arange(D.shape[1]) * 128 / sr
        ax.pcolormesh(tt, fr, D, vmin=-90, vmax=0, cmap='magma', shading='auto'); ax.set_yscale('symlog', linthresh=200); ax.set_ylim(40, 20000)
        hop = 48; n = len(mo) // hop
        e = 20 * np.log10(np.sqrt((mo[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
        ax2 = ax.twinx(); ax2.plot(np.arange(n) * hop / sr, e, color='cyan', lw=0.7); ax2.set_ylim(-80, 0); ax2.set_yticks([])
        corr = np.corrcoef(y[:, 0], y[:, 1])[0, 1] if y[:, 0].std() > 0 else 1
        ax.set_title(f'{m["fx"]} [{m["catid"]}] {m["dur"]:.2f}s  LR={corr:.2f}', fontsize=9)
        ax.tick_params(labelsize=7)
    for ax in axs.flat[len(chunk):]: ax.axis('off')
    plt.tight_layout(); plt.savefig(f'{outp}_{k // per:02d}.png'); plt.close()
print('ok')
