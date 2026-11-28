import json, sys
D = sys.argv[1]
C = json.load(open(f'{D}/catalogue.json'))
S, F, K = C['sounds'], C['motion_families'], C['ucs_categories']
used = [k for k in K if k['count']]
L = []
A = L.append
A('# Bibliothèque SFX — motion design × UCS\n')
A(f'**{C["total"]} effets sonores** rangés selon le standard professionnel **UCS v8.2.1** (Universal Category System) '
  f'et regroupés en **{len(F)} familles motion design** :\n')
A(f'- **{C["extracted"]} sons extraits** de 14 vidéos gratuites de créateurs de motion design (Suraj Editing Tips, @piero.cesti, « 10 Sound Effects Every Editor Must Use ») ;')
A(f'- **{C["synthesized"]} sons synthétisés** par code pour couvrir toutes les familles motion (risers, braams, drones, logo reveals, UI, glitch, magie…).\n')
A('C’est la bibliothèque de référence pour les effets sonores de toutes les motions de ce projet.\n')
A('- **Écouter / chercher** : ouvrir [`index.html`](index.html) (filtres par famille motion, par catégorie UCS et par origine).')
A('- **Données** : [`catalogue.json`](catalogue.json) — CatID, catégorie/sous-catégorie (EN + FR), famille motion, description, durée, origine.')
A('- **Référence UCS complète** : [`_ucs/UCS_v8.2.1_liste_complete.csv`](_ucs/UCS_v8.2.1_liste_complete.csv) — les 82 catégories et 753 sous-catégories avec traductions FR, définitions et synonymes, pour classer de futurs sons.')
A(f'- **Format** : {C["format"]}. Métadonnées intégrées dans chaque WAV (titre, auteur, catégorie UCS, description).\n')

A('## Organisation\n')
A('```')
A('sfx/')
A('├── <CATÉGORIE UCS>/            82 dossiers officiels (DESIGNED, SWOOSHES, USER INTERFACE, …)')
A('│   ├── _UCS_<CATÉGORIE>.txt     fiche : sous-catégories, CatID, traductions, définitions')
A('│   └── CatID_FXName_CreatorID_SourceID.wav')
A('├── _ucs/                       liste UCS complète (CSV)')
A('├── _outils/                    scripts : extraction depuis vidéos + moteur de synthèse')
A('├── catalogue.json · index.html · README.md')
A('```')
A(f'Les {len(used)} catégories UCS utilisées aujourd’hui contiennent des sons ; les {82 - len(used)} autres sont prêtes à recevoir de vrais enregistrements '
  '(animaux, véhicules, portes, eau, foules…), chacune avec sa fiche de sous-catégories.\n')
A('### Convention de nommage UCS\n')
A('`CatID_FXName_CreatorID_SourceID.wav` — ex. `DSGNRise_Synth Riser_MotionSynth_MotionLib.wav`\n')
A('| Bloc | Rôle | Valeurs ici |\n|---|---|---|')
A('| **CatID** | catégorie + sous-catégorie UCS (code officiel, casse respectée) | `WHSH`, `DSGNImpt`, `UIClick`… |')
A('| **FXName** | titre court (≤ 25 caractères), sans `_` ni `-` | `Air Whoosh Long` |')
A('| **CreatorID** | auteur | `MotionSynth` (synthèse), `SurajET`, `PieroCesti`, `Unknown` |')
A('| **SourceID** | bibliothèque / projet d’origine | `MotionLib`, `SurajSFX04`, `PieroCestiSFX`, `TenSFXEditors` |')
A('\nLes outils compatibles UCS (Soundminer, BaseHead, Reaper + UCS Toolkit, Audio Category Clipper…) lisent la catégorie directement depuis le nom.\n')

A('## Les familles motion design\n')
A('| Famille | Usage | Nb |\n|---|---|---|')
for f in F: A(f'| [{f["family"]}](#{f["family"].lower().replace(" / ", "--").replace(" ", "-").replace("’", "")}) | {f["usage"]} | {f["count"]} |')
A('\n## Les catégories UCS utilisées\n')
A('| Dossier UCS | Français | Sous-catégories UCS | Sons |\n|---|---|---|---|')
for k in used: A(f'| [`{k["category"]}/`]({k["category"].replace(" ", "%20").replace("&", "%26")}/) | {k["category_fr"]} | {k["subcategories"]} | {k["count"]} |')
A(f'\nToutes les autres catégories (sur 82) existent en dossier vide avec leur fiche ; la liste complète est dans `_ucs/`.\n')

A('## Règles d’utilisation dans les motions\n')
A('''1. **Un son = un événement visuel important** (apparition, impact, changement de scène). Pas de SFX sur les micro-mouvements.
2. **Caler l’attaque sur l’image clé** : les fichiers démarrent à l’attaque, sans silence en tête.
   - Exceptions : **risers**, **reverse** et **montées** se placent *avant* l’événement pour que leur **fin** tombe sur l’impact ou la coupe (elles s’arrêtent net exprès).
   - **Stingers / logo reveals** et **transitions** : caler le **pic de l’impact** sur l’apparition du logo ou la coupe.
3. **Choisir par famille** (tableau ci-dessus), puis varier : ne jamais enchaîner deux fois le même whoosh.
4. **Superposer** pour un temps fort : riser → impact + boom/sub drop (+ braam pour le dramatique).
5. **Boucles** (`Loop` dans le nom : drones, ambiances, chargement, tic-tac) : bouclables sans clic, à étirer sous toute une scène, 15–25 dB sous la voix.
6. **Mixage** : crêtes à −1 dBFS ; baisser les SFX de 6 à 12 dB sous la voix off, 3 à 6 dB sous la musique ; jamais deux impacts au même instant.
''')

A('## Catalogue complet (par famille motion)\n')
for f in F:
    A(f'### {f["family"]}\n')
    A(f'{f["usage"]}\n')
    A('| Fichier | UCS | Durée | Description | Origine |\n|---|---|---|---|---|')
    for s in sorted([s for s in S if s['motion_family'] == f['family']], key=lambda s: (s['origin'] != 'synthétisé', s['catid'], s['fx_name'])):
        o = s['origin_detail']
        orig = 'synthèse' if s['origin'] == 'synthétisé' else f'{s["creator_id"]} — {o["video"]} @ {o["start_s"]:.2f} s'
        d = s['description'] + (' ⚠️ ' + ' '.join(s['notes']) if s['notes'] else '') + (' 🔁 bouclable' if s['loop'] else '')
        path = s['file'].replace(' ', '%20').replace('&', '%26')
        A(f'| [`{s["fx_name"]}`]({path}) | `{s["catid"]}` {s["category_fr"]} › {s["subcategory_fr"]} | {s["duration_s"]:.2f} s | {d} | {orig} |')
    A('')

A('## Origine des sons\n')
A('''**Sons extraits** — les vidéos montrent une timeline qui défile ; elle a été reconstruite image par image pour identifier chaque clip et son nom, puis les coupes ont été calées sur l’audio à la milliseconde (fondus anti-clic, doublons retirés par corrélation). La vidéo « 10 Sound Effects » avait une musique de fond, atténuée d’environ 15 dB (signalé ⚠️). Les sons coupés net par le montage d’origine sont aussi signalés ⚠️.

**Sons synthétisés** — générés par le moteur `_outils/synth/` (Python : bruit filtré, oscillateurs, FM, synthèse additive de cloches, Karplus-Strong, réverbération à convolution synthétique). Chaque son est contrôlé : spectrogramme, fins sans coupure, boucles sans clic au raccord. Pour en créer d’autres : ajouter une recette dans `families.py` puis relancer `render.py` et `build_ucs.py`.

**Pourquoi certaines catégories UCS sont vides** : les sons du monde réel (animaux, voix, véhicules, armes, foules, eau…) ne se synthétisent pas de façon crédible ; ils demandent de vrais enregistrements, à déposer dans le dossier UCS correspondant en suivant sa fiche.
''')
A('## Droits\n')
A('- **Sons synthétisés** : créés pour ce projet, utilisables librement.\n'
  '- **Sons extraits** : issus de vidéos partagées gratuitement ; plusieurs portent des noms de banques connues (Mixkit, Epidemic Sound « ES_ », Adobe…). Vérifier la licence d’origine avant un usage commercial ou une redistribution.\n'
  '- **UCS** : système libre créé par Tim Nielsen, Justin Drury, Kai Paquin et contributeurs — https://universalcategorysystem.com. '
  'Traduction française officielle utilisée, avec 4 corrections dans OBJECTS (FASHION/FURNITURE/GARDEN/GYM étaient intervertis).\n')
open(f'{D}/README.md', 'w').write('\n'.join(L))

J = json.dumps(dict(families=F, cats=used, sounds=[{k: s[k] for k in ('id', 'file', 'catid', 'category', 'category_fr', 'subcategory_fr', 'fx_name', 'motion_family', 'description', 'duration_s', 'loop', 'origin', 'notes')} for s in S]), ensure_ascii=False)
H = '''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bibliothèque SFX — motion design × UCS</title>
<style>
:root{--bg:#0f1115;--card:#181b22;--fg:#e8eaf0;--mut:#9aa1b2;--acc:#7c9cff;--syn:#5fd4a0;--ext:#e5b45c}
*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
header{position:sticky;top:0;background:rgba(15,17,21,.96);backdrop-filter:blur(6px);padding:12px 18px;border-bottom:1px solid #262a33;z-index:2}
h1{font-size:18px;margin:0 0 8px}.row{display:flex;gap:8px;flex-wrap:wrap}input,select{padding:8px 10px;border-radius:8px;border:1px solid #2c313c;background:#11141a;color:var(--fg);font-size:14px}
input{flex:1;min-width:200px}.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.chip{padding:4px 9px;border-radius:999px;border:1px solid #2c313c;background:#141821;color:var(--mut);cursor:pointer;font-size:12.5px}.chip.on{background:var(--acc);border-color:var(--acc);color:#0b0d12}
main{padding:10px 18px 40px;max-width:1150px;margin:auto}h2{font-size:14px;color:var(--mut);margin:20px 0 6px;text-transform:uppercase;letter-spacing:.05em}
.s{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;background:var(--card);border-radius:10px;padding:9px 12px;margin:5px 0}
.s button{width:36px;height:36px;border-radius:50%;border:0;background:var(--acc);color:#0b0d12;font-size:14px;cursor:pointer}
.n{font-weight:600;font-size:14px}.u{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--mut)}.d{color:var(--mut);font-size:13px}
.t{color:var(--mut);font-size:12px;text-align:right;white-space:nowrap}.t a{color:var(--mut)}.tag{font-size:11px;padding:1px 6px;border-radius:5px;margin-left:6px}
.syn{background:#163a2c;color:var(--syn)}.ext{background:#3a2d16;color:var(--ext)}.w{color:var(--ext)}
</style></head><body>
<header><h1>Bibliothèque SFX — <span id="count"></span></h1>
<div class="row"><input id="q" placeholder="Rechercher (whoosh, clic, riser, logo, papier, DSGNImpt…)">
<select id="cat"><option value="">Toutes les catégories UCS</option></select>
<select id="org"><option value="">Toutes origines</option><option value="synthétisé">Synthétisés</option><option value="extrait">Extraits des vidéos</option></select></div>
<div class="chips" id="chips"></div></header>
<main id="list"></main>
<script>
const DATA=__DATA__;let fam=null;const audio=new Audio();let playing=null;
const $=id=>document.getElementById(id);
for(const c of DATA.cats){const o=document.createElement('option');o.value=c.category;o.textContent=c.category+' — '+c.category_fr+' ('+c.count+')';$('cat').appendChild(o)}
function chip(k,l){const b=document.createElement('button');b.className='chip';b.textContent=l;b.dataset.k=k;b.onclick=()=>{fam=(fam===k||k==='__all')?null:k;render()};$('chips').appendChild(b)}
chip('__all','Toutes les familles');for(const f of DATA.families)chip(f.family,f.family+' ('+f.count+')');
function render(){const t=$('q').value.toLowerCase().trim(),c=$('cat').value,o=$('org').value;$('list').innerHTML='';let n=0;
 for(const b of $('chips').children)b.classList.toggle('on',b.dataset.k===(fam||'__all'));
 for(const f of DATA.families){if(fam&&fam!==f.family)continue;
  const it=DATA.sounds.filter(s=>s.motion_family===f.family&&(!c||s.category===c)&&(!o||s.origin===o)&&(!t||(s.id+' '+s.description+' '+s.category_fr+' '+s.subcategory_fr).toLowerCase().includes(t)));
  if(!it.length)continue;const h=document.createElement('h2');h.textContent=f.family+' — '+f.usage;$('list').appendChild(h);
  for(const s of it){n++;const d=document.createElement('div');d.className='s';
   d.innerHTML=`<button aria-label="Écouter">▶</button><div><div class="n">${s.fx_name}<span class="tag ${s.origin==='synthétisé'?'syn':'ext'}">${s.origin}</span>${s.loop?'<span class="tag syn">🔁 boucle</span>':''}</div><div class="u">${s.catid} · ${s.category_fr} › ${s.subcategory_fr}</div><div class="d">${s.description}${s.notes.length?' <span class="w">⚠ '+s.notes.join(' ')+'</span>':''}</div></div><div class="t">${s.duration_s.toFixed(2)} s<br><a href="${encodeURI(s.file).replace(/&/g,'%26')}" download>télécharger</a></div>`;
   const b=d.querySelector('button');b.onclick=()=>{if(playing===b&&!audio.paused){audio.pause();b.textContent='▶';return}
    if(playing)playing.textContent='▶';audio.src=encodeURI(s.file).replace(/&/g,'%26');audio.loop=s.loop;audio.currentTime=0;audio.play();b.textContent='■';playing=b};
   $('list').appendChild(d)}}
 $('count').textContent=n+' sons'}
audio.onended=()=>{if(playing)playing.textContent='▶'};$('q').oninput=render;$('cat').onchange=render;$('org').onchange=render;render();
</script></body></html>'''
open(f'{D}/index.html', 'w').write(H.replace('__DATA__', J))
print('ok', len(L), 'lignes README')
