"""Construit le projet Kdenlive de la motion de test en pilotant uniquement le CLI CLI-Anything (cli-anything-kdenlive).

usage: python3 kdenlive_build.py <dossier sfx> <video_sans_son.mp4> <dossier de sortie>
"""
import sys, os, json, subprocess, math
import soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import CUES, T, DUR, FPS
from mix import sync_offset          # même détection de point de synchro que le mixage

SFX, VIDEO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]   # chemins relatifs conservés (projet portable)
os.makedirs(OUT, exist_ok=True)
PROJ = os.path.join(OUT, 'motion_test_sfx.kdenlive-cli.json')
K = 'cli-anything-kdenlive'
LOG = []
MASTER_TRIM_DB = -2.0   # pas de limiteur dans Kdenlive : marge pour éviter la saturation à l'impact


def cli(*args, project=True):
    cmd = [K, '--json'] + (['--project', PROJ] if project else []) + [str(a) for a in args]
    LOG.append(' '.join(f'"{a}"' if ' ' in a else a for a in cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f'{cmd}\n{r.stdout}\n{r.stderr}')
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return r.stdout


fr = lambda s: s / FPS                       # images -> secondes exactes sur la grille
def to_frames(sec): return int(round(sec * FPS))


if os.path.exists(PROJ): os.remove(PROJ)
cli('project', 'new', '-n', 'Motion test SFX', '--width', 1080, '--height', 1920, '--fps-num', FPS, '--fps-den', 1, '-o', PROJ, project=False)
# Contournement d'un défaut du harness : `project new` n'expose pas le rapport d'affichage et garde 16:9
# même pour 1080x1920 (pixels étirés). On le règle à 9:16 dans le JSON du projet => pixels carrés.
_p = json.load(open(PROJ)); _p['profile']['dar_num'], _p['profile']['dar_den'] = 9, 16
json.dump(_p, open(PROJ, 'w'), indent=2, ensure_ascii=False)

# --- média : vidéo + un clip de bin par fichier SFX
vid = cli('bin', 'import', VIDEO, '-n', 'Motion (image seule)', '--type', 'video', '-d', DUR)['id']
bin_ids, durs = {}, {}
for f, *_ in CUES:
    if f in bin_ids: continue
    p = os.path.join(SFX, f); d = sf.info(p).duration
    name = os.path.basename(f).split('_')[1]
    bin_ids[f] = cli('bin', 'import', p, '-n', name, '--type', 'audio', '-d', round(d, 4))['id']
    durs[f] = d

# --- pistes : 1 vidéo + pistes audio par rôle
cli('timeline', 'add-track', '-n', 'Vidéo', '--type', 'video')   # piste 0
ROLES = ['Nappe', 'Whoosh', 'UI', 'Notifications', 'Impacts', 'Magie et logo']
role_of = lambda f: ('Nappe' if 'DSGNDron' in f else
                     'Whoosh' if any(k in f for k in ('SWSH', 'WHSH', 'DSGNWhsh', 'UIMvmt_Card', 'UIMvmt_Slide')) else
                     'Notifications' if any(k in f for k in ('UIAlert', 'UIData')) else
                     'UI' if any(k in f for k in ('UIClick', 'UIMvmt')) else
                     'Magie et logo' if any(k in f for k in ('MAG', 'DSGNStngr')) else 'Impacts')
cli('timeline', 'add-clip', 0, vid, '-p', 0, '--in', 0, '--out', fr(to_frames(DUR)))

# --- placement : calcul des positions (images entières) puis pistes numérotées par rôle, sans chevauchement
plan = []
for f, t, mode, gdb, opt in CUES:
    y, _ = sf.read(os.path.join(SFX, f), always_2d=True)
    off = sync_offset(y, mode)
    d_frames = int(math.floor(durs[f] * FPS))
    if opt.get('loop_to'):                       # nappe bouclée : copies enchaînées
        total = to_frames(opt['loop_to']); pos = 0
        while pos < total:
            n = min(d_frames, total - pos); plan.append((f, t, mode, gdb, opt, off, pos, 0, n)); pos += n
    else:
        n = to_frames(opt['cut']) if opt.get('cut') else d_frames
        start = to_frames(t - off); in_f = 0
        if start < 0: in_f, start = -start, 0
        n = n - in_f
        end_cap = to_frames(DUR) - start                # ne pas dépasser la fin de la vidéo
        if n > end_cap:
            n = end_cap; opt = dict(opt, end_fade=0.3)
        plan.append((f, t, mode, gdb, opt, off, start, in_f, n))

lanes = {r: [] for r in ROLES}                   # rôle -> liste de pistes, chacune = liste d'intervalles
placed = []
for (f, t, mode, gdb, opt, off, pos, in_f, n) in plan:
    role = role_of(f); k = 0
    while k < len(lanes[role]) and any(not (pos >= e or pos + n <= s) for s, e in lanes[role][k]): k += 1
    if k == len(lanes[role]): lanes[role].append([])
    lanes[role][k].append((pos, pos + n))
    placed.append(dict(file=os.path.basename(f), track=f'{role} {k + 1}', cue=t, mode=mode, sync_in_file=round(off, 3),
                       start_s=round(fr(pos), 4), start_frame=pos, in_frame=in_f, frames=n, gain_db=gdb, opt=opt, bin=bin_ids[f]))
name2id = {}
for r in ROLES:
    for k in range(len(lanes[r])):
        nm = f'{r} {k + 1}'
        cli('timeline', 'add-track', '-n', nm, '--type', 'audio')
        tl = cli('timeline', 'list'); tl = tl if isinstance(tl, list) else tl.get('tracks', [])
        name2id[nm] = [x['id'] for x in tl if x['name'] == nm][0]
for pl in placed:
    cli('timeline', 'add-clip', name2id[pl['track']], pl['bin'], '-p', fr(pl['start_frame']), '--in', fr(pl['in_frame']), '--out', fr(pl['in_frame'] + pl['frames']))
ROLES = list(name2id)

# --- filtres : volume (gain linéaire) + fondus ; l'index d'un clip = rang trié par position sur sa piste
for r in ROLES:
    mine = sorted([pl for pl in placed if pl['track'] == r], key=lambda pl: pl['start_frame'])
    for idx, pl in enumerate(mine):
        cli('filter', 'add', name2id[r], idx, 'volume', '-p', f"gain={10 ** ((pl['gain_db'] + MASTER_TRIM_DB) / 20):.4f}")
        o = pl['opt']
        if o.get('fade_in') and pl['start_frame'] == 0:
            cli('filter', 'add', name2id[r], idx, 'fade_in_audio', '-p', f"duration={o['fade_in']}")
        if o.get('fade_out') and idx == len(mine) - 1 and o.get('loop_to'):
            cli('filter', 'add', name2id[r], idx, 'fade_out_audio', '-p', f"duration={o['fade_out']}")
        if o.get('end_fade'):
            cli('filter', 'add', name2id[r], idx, 'fade_out_audio', '-p', f"duration={o['end_fade']}")
        if o.get('cut'):
            cli('filter', 'add', name2id[r], idx, 'fade_out_audio', '-p', 'duration=0.04')

# --- repères (guides) sur les événements visuels
G = [('Logo', T['logo']), ('Glitch', T['glitch']), ('Panneau', T['panel_land']), ('Clic', T['click']),
     ('Notification', T['notif_land']), ('Succès', T['check']), ('Compteur', T['count_start']),
     ('IMPACT', T['hit']), ('Pastilles', T['chips'][0]), ('Logo final', T['outro_logo'])]
for lab, t in G:
    cli('guide', 'add', fr(to_frames(t)), '-l', lab)

kd = os.path.join(OUT, 'motion_test_sfx.kdenlive')
cli('export', 'xml', '-o', kd)
json.dump(placed, open(os.path.join(OUT, 'placement.json'), 'w'), indent=1, ensure_ascii=False)
open(os.path.join(OUT, 'commandes_cli.txt'), 'w').write('\n'.join(LOG) + '\n')
info = cli('project', 'info')
print(json.dumps(info.get('counts', info), indent=1) if isinstance(info, dict) else info)
print('commandes CLI exécutées :', len(LOG))
for pl in placed:
    print('%-50s %-17s repère %5.2f -> image %3d (%.3f s) %+d dB' % (pl['file'][:50], pl['track'], pl['cue'], pl['start_frame'], pl['start_s'], pl['gain_db']))
