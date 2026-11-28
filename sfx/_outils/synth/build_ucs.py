"""Assemble la bibliothèque : dossiers UCS, noms UCS, familles motion, métadonnées WAV, catalogue."""
import sys, os, json, shutil, re, csv
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from ucs_map_extracted import X

UCS_JSON, OLD, SYN, DST = sys.argv[1:5]
UCS = json.load(open(UCS_JSON))
FR_FIX = {'OBJFash': 'MODE', 'OBJFurn': 'MEUBLE', 'OBJGrdn': 'JARDIN', 'OBJGym': 'GYM'}
for r in UCS:
    if r['catid'] in FR_FIX: r['subcategory_fr'] = FR_FIX[r['catid']]
BYID = {r['catid']: r for r in UCS}
CATS = []
for r in UCS:
    if r['category'] not in CATS: CATS.append(r['category'])

FAMILIES = [
 ('Whoosh', 'Entrées/sorties d’éléments, mouvements de caméra, passages.'),
 ('Swish / swipe', 'Petits mouvements rapides, cartes et panneaux qui glissent.'),
 ('Riser / montée', 'Monter la tension avant une révélation ; caler la FIN sur l’impact.'),
 ('Impact / hit', 'Temps forts : titre qui tombe, coupe, révélation.'),
 ('Boom / sub drop', 'Renfort grave sous un impact ou un drop.'),
 ('Braam', 'Gros son cuivré de bande-annonce : moment dramatique.'),
 ('Stinger / logo reveal', 'Signature sonore complète pour un logo ou une fin de vidéo.'),
 ('Transition', 'Changement de scène (montée + impact, tape stop, glitch, ralenti).'),
 ('Drone / nappe', 'Fond sonore tenu (bouclable) : tension, mystère, technologie.'),
 ('Ambiance', 'Fond d’ambiance bouclable : pièce, vent, salle high-tech, sci-fi.'),
 ('UI clic / tap', 'Boutons, curseur, toggles, sélections.'),
 ('Pop / bulle', 'Apparition/disparition d’éléments, bulles, puces.'),
 ('UI bip / données', 'Bips, chargement, données, interfaces high-tech, texte qui s’écrit.'),
 ('Notification / alerte', 'Succès, erreur, notification, récompense, argent.'),
 ('Glitch / numérique', 'Glitchs, statique, corruption : style tech, erreurs.'),
 ('Électrique / laser / énergie', 'Zaps, étincelles, lasers, charges d’énergie, téléportation.'),
 ('Magie / scintillement', 'Paillettes, poufs magiques, glissandos féeriques.'),
 ('Cartoon / fun', 'Boings, sifflets, couinements, bonks : ton léger.'),
 ('Tonal / musical', 'Accents musicaux : accords, cloches, marimba, petites phrases.'),
 ('Horloge / compteur', 'Tic-tac, comptes à rebours, compteurs de score.'),
 ('Battement / pulsation', 'Battements de cœur : suspense, émotion.'),
 ('Power up / down', 'Mise sous/hors tension, servos, mécanismes robotiques.'),
 ('Foley / objets', 'Sons d’objets réels : papier, chaîne, clavier, engrenages, feutre, obturateur.'),
]
FAM_NAMES = [f for f, _ in FAMILIES]

CREATORS = {'Suraj Editing Tips': 'SurajET', '@piero.cesti': 'PieroCesti', 'Créateur non indiqué': 'Unknown'}
def src_id(video):
    m = re.search(r'Part (\d+)', video)
    if m: return 'SurajSFX%02d' % int(m.group(1))
    if 'whoosh' in video: return 'SurajSFXWhoosh'
    if video == 'Sound Effects': return 'SurajSFX'
    if 'Comment' in video: return 'PieroCestiSFX'
    return 'TenSFXEditors'

def clean_fx(s):
    s = re.sub(r'[_\-]', ' ', s); s = re.sub(r'\s+', ' ', s).strip(); return s

if os.path.exists(DST): shutil.rmtree(DST)
os.makedirs(DST)
old = json.load(open(os.path.join(OLD, 'catalogue.json')))
syn = json.load(open(os.path.join(SYN, '_meta.json')))
items = []
for e in old['sounds']:
    catid, fx, fam = X[e['id']]
    cr = CREATORS[e['source']['creator']]
    items.append(dict(src=os.path.join(OLD, e['file']), catid=catid, fx=fx, family=fam, creator=cr, creator_full=e['source']['creator'],
                      source=src_id(e['source']['video']), desc=e['description'], notes=e['notes'], loop=False,
                      origin='extrait', origin_detail=dict(video=e['source']['video'], start_s=e['source']['start_s'], end_s=e['source']['end_s'],
                      clip_name=e['original_clip_name'], old_id=e['id'])))
for m in syn:
    items.append(dict(src=os.path.join(SYN, m['tmp']), catid=m['catid'], fx=m['fx'], family=m['family'], creator='MotionSynth',
                      creator_full='Synthèse sonore (code, ce dépôt)', source='MotionLib', desc=m['desc'], notes=[], loop=m['loop'],
                      origin='synthétisé', origin_detail=dict(recipe=m['fx'])))
assert all(i['family'] in FAM_NAMES for i in items), {i['family'] for i in items} - set(FAM_NAMES)
assert all(i['catid'] in BYID for i in items)

seen = set(); sounds = []
for it in items:
    r = BYID[it['catid']]; fx = clean_fx(it['fx'])
    if it['loop'] and 'Loop' not in fx: fx += ' Loop'
    base = f"{it['catid']}_{fx}_{it['creator']}_{it['source']}"
    k = 2
    while base.lower() in seen:
        base = f"{it['catid']}_{fx} {k}_{it['creator']}_{it['source']}"; k += 1
    seen.add(base.lower())
    folder = r['category']; os.makedirs(os.path.join(DST, folder), exist_ok=True)
    rel = f'{folder}/{base}.wav'
    y, sr = sf.read(it['src'], always_2d=True)
    with sf.SoundFile(os.path.join(DST, rel), 'w', sr, y.shape[1], 'PCM_16') as f:
        f.title = fx; f.artist = it['creator_full']; f.album = it['source']
        f.genre = f"{r['category']}-{r['subcategory']}"
        f.comment = f"{it['desc']} | Famille motion : {it['family']} | UCS {it['catid']}"
        f.software = 'Bibliothèque SFX motion design'
        f.write(y)
    sounds.append(dict(id=base, file=rel, catid=it['catid'], category=r['category'], subcategory=r['subcategory'],
        category_fr=r['category_fr'], subcategory_fr=r['subcategory_fr'], fx_name=fx, creator_id=it['creator'], source_id=it['source'],
        motion_family=it['family'], description=it['desc'], duration_s=round(len(y) / sr, 3), loop=it['loop'],
        origin=it['origin'], origin_detail=it['origin_detail'], notes=it['notes']))

# dossiers UCS vides : fiche des sous-catégories
used = {s['category'] for s in sounds}
for c in CATS:
    d = os.path.join(DST, c); os.makedirs(d, exist_ok=True)
    rows = [r for r in UCS if r['category'] == c]
    n = sum(s['category'] == c for s in sounds)
    lines = [f'UCS v8.2.1 — {c}  ({rows[0]["category_fr"]})   CatShort : {rows[0]["catshort"]}',
             f'Sons dans ce dossier : {n}', '',
             'Nommer chaque fichier : CatID_Nom court_CreatorID_SourceID.wav  (ex. ' + rows[0]['catid'] + '_Mon Son_MonNom_MaLib.wav)', '',
             'Sous-catégories (CatID | anglais | français | définition officielle) :', '']
    for r in rows:
        lines.append(f"{r['catid']:<11}| {r['subcategory']:<22}| {r['subcategory_fr']:<22}| {r['explanation']}")
    open(os.path.join(d, '_UCS_' + c.replace(' ', '_').replace('&', 'et') + '.txt'), 'w').write('\n'.join(lines) + '\n')

order_f = {f: i for i, f in enumerate(FAM_NAMES)}
sounds.sort(key=lambda s: (CATS.index(s['category']), s['catid'], s['fx_name']))
cat_meta = []
for c in CATS:
    rows = [r for r in UCS if r['category'] == c]
    cat_meta.append(dict(category=c, category_fr=rows[0]['category_fr'], catshort=rows[0]['catshort'], subcategories=len(rows),
                         count=sum(s['category'] == c for s in sounds)))
fam_meta = [dict(family=f, usage=u, count=sum(s['motion_family'] == f for s in sounds)) for f, u in FAMILIES]
json.dump(dict(version=2, standard='Universal Category System (UCS) v8.2.1 — https://universalcategorysystem.com',
               naming='CatID_FXName_CreatorID_SourceID.wav', format='WAV PCM 16 bits, 48 kHz, stéréo, crête à −1 dBFS',
               total=len(sounds), extracted=sum(s['origin'] == 'extrait' for s in sounds), synthesized=sum(s['origin'] == 'synthétisé' for s in sounds),
               motion_families=fam_meta, ucs_categories=cat_meta, sounds=sounds,
               excluded_duplicates=old.get('excluded_duplicates', [])),
          open(os.path.join(DST, 'catalogue.json'), 'w'), ensure_ascii=False, indent=1)

# liste UCS complète (référence pour classer de futurs sons)
os.makedirs(os.path.join(DST, '_ucs'), exist_ok=True)
with open(os.path.join(DST, '_ucs', 'UCS_v8.2.1_liste_complete.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['CatID', 'Category', 'SubCategory', 'Catégorie_FR', 'SousCatégorie_FR', 'CatShort', 'Explanation', 'Synonyms'])
    for r in UCS: w.writerow([r['catid'], r['category'], r['subcategory'], r['category_fr'], r['subcategory_fr'], r['catshort'], r['explanation'], r['synonyms']])
print(len(sounds), 'sons ;', len(used), 'catégories UCS utilisées /', len(CATS))
for fm in fam_meta: print('  %-30s %d' % (fm['family'], fm['count']))
