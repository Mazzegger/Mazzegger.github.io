import sys, os, json, shutil, soundfile as sf, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from mapping import M, DROP, VIDEOS
S, DST = sys.argv[1], sys.argv[2]
R = json.load(open(f'{S}/cut_report_all.json')); R.update(json.load(open(f'{S}/cut_report_v12.json')))
vidfile = dict(l.split() for l in open(f'{S}/map.txt'))
CAT = {
 'whoosh': ('Whoosh / swish', 'Mouvements, glissements, entrées et sorties d’éléments, transitions rapides.'),
 'transition': ('Transitions', 'Transitions longues et spectaculaires (montée + impact, ralenti, tourbillon).'),
 'riser': ('Risers / montées', 'Montées de tension avant une révélation, un impact ou une coupe.'),
 'impact': ('Impacts / booms', 'Chocs, booms, drops : titres, révélations, temps forts.'),
 'ui': ('Interface (UI)', 'Clics, boutons, pops, bips : interfaces, curseurs, apparitions d’éléments.'),
 'notification': ('Notifications / dings', 'Dings, carillons, succès, caisse enregistreuse : validation, prix, récompense.'),
 'glitch': ('Glitch / sci-fi', 'Glitchs, zaps, statique, erreurs : style tech, erreurs, transitions numériques.'),
 'foley': ('Foley / objets', 'Sons d’objets réels : papier, chaîne, clavier, engrenages, feutre, obturateur.'),
 'cartoon': ('Cartoon / fun', 'Rebonds, boings, bloops, scintillements : ton léger et ludique.'),
}
if os.path.exists(DST): shutil.rmtree(DST)
entries = []
for vid, reps in R.items():
    for r in reps:
        src = r['file'][:-4]
        if src in DROP: continue
        cat, name, desc, orig = M[src]
        fn = f'{cat}_{name}.wav'; os.makedirs(f'{DST}/{cat}', exist_ok=True)
        sd = f'{S}/out12' if vid == 'v12' else f'{S}/out1'
        shutil.copy(f'{sd}/{r["file"]}', f'{DST}/{cat}/{fn}')
        info = sf.info(f'{DST}/{cat}/{fn}')
        notes = []
        if r.get('note') == 'music bed reduced': notes.append('Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester.')
        elif r.get('note'): notes.append(r['note'][0].upper() + r['note'][1:] + '.')
        creator, video = VIDEOS[vid]
        entries.append(dict(id=f'{cat}_{name}', file=f'{cat}/{fn}', category=cat, description=desc,
            duration_s=round(info.duration, 3), original_clip_name=orig, notes=notes,
            source=dict(creator=creator, video=video, upload_id=vidfile[vid], start_s=r['start'], end_s=r['end'], ref=src)))
order = list(CAT)
entries.sort(key=lambda e: (order.index(e['category']), e['id']))
cat_meta = {k: dict(label=v[0], usage=v[1], count=sum(e['category'] == k for e in entries)) for k, v in CAT.items()}
json.dump(dict(version=1, format='WAV PCM 16 bits, 48 kHz, stéréo, crête normalisée à −1 dBFS',
               total=len(entries), categories=cat_meta, sounds=entries,
               excluded_duplicates=[dict(ref=k, reason=v) for k, v in DROP.items()]),
          open(f'{DST}/catalogue.json', 'w'), ensure_ascii=False, indent=1)
print(len(entries), 'sons ;', sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(DST) for f in fs) / 1e6, 'Mo')
