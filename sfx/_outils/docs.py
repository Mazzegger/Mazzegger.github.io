import json, sys, html
D=sys.argv[1]; C=json.load(open(f'{D}/catalogue.json'))
S=C['sounds']; cats=C['categories']
L=[]
L.append('# Bibliothèque SFX pour le motion design\n')
L.append(f'{C["total"]} effets sonores uniques, extraits de 14 vidéos gratuites de créateurs de contenu en motion design '
         '(Suraj Editing Tips, @piero.cesti et une vidéo « 10 Sound Effects Every Editor Must Use » sans créateur indiqué).\n')
L.append('C’est **la** bibliothèque de référence pour les effets sonores de toutes les animations (motions) produites pour ce projet.\n')
L.append('- Écouter : ouvrir [`index.html`](index.html) (lecteur avec recherche et filtres).')
L.append('- Machine : [`catalogue.json`](catalogue.json) (description, durée, source, horodatage d’origine de chaque son).')
L.append(f'- Format : {C["format"]}.\n')
L.append('## Catégories\n')
L.append('| Dossier | Contenu | Usage | Nb |\n|---|---|---|---|')
for k,v in cats.items(): L.append(f'| [`{k}/`]({k}/) | {v["label"]} | {v["usage"]} | {v["count"]} |')
L.append('\n## Règles d’utilisation dans les motions\n')
L.append('''1. **Un son = un événement visuel.** Chaque apparition, déplacement, impact ou changement d’écran important reçoit son SFX ; on n’en met pas sur les micro-mouvements.
2. **Caler l’attaque sur l’image.** Tous les fichiers commencent à l’attaque (pas de silence en tête) : placer le début du fichier sur l’image clé.
   - Exceptions : les `riser/` et `riser_reverse_whoosh` se placent **avant** l’événement, pour que leur fin tombe pile sur l’impact ou la coupe.
   - Les `transition/` combinent montée et impact : caler le pic de l’impact sur la coupe.
3. **Correspondance type d’animation → catégorie :**
   - Texte ou élément qui entre/sort en glissant → `whoosh/` (courts : `micro_swish`, `swish_short`, `zip`, `swipe_short` ; amples : `air_*`).
   - Titre, logo, révélation, drop → `impact/` (souvent précédé d’un `riser/`).
   - Changement de scène → `whoosh/whoosh_transition`, `transition/` ou `glitch/glitch_transition`.
   - Bouton, curseur, carte UI, liste à puces → `ui/` (`click_*`, `pop_*`, `bubble_pops`, `switch`, `open`).
   - Validation, réussite, chiffre clé, prix → `notification/` (`success_ui`, `chime_trending`, `cash_register_*`).
   - Erreur, alerte, style tech/hacker → `glitch/` (`negative_*`, `zap`, `static_*`).
   - Chargement, compteur, données → `ui/ui_data_loading`, `ui/ui_digital_data_up|down`.
   - Écriture/dessin d’un trait → `foley/foley_marker_draw_line` ; frappe → `foley/foley_macbook_keyboard`.
   - Ton léger, humoristique → `cartoon/`.
4. **Mixage.** Les fichiers sont normalisés en crête à −1 dBFS : baisser les SFX de 6 à 12 dB sous la voix off, 3 à 6 dB sous la musique ; jamais deux impacts au même instant.
5. **Varier.** Ne pas réutiliser le même whoosh deux fois de suite : alterner `air_1` … `air_8`, `noise_*`, `swish*`.
''')
L.append('## Catalogue complet\n')
for k,v in cats.items():
    L.append(f'### {v["label"]} — `{k}/` ({v["count"]})\n')
    L.append('| Fichier | Durée | Description | Source |\n|---|---|---|---|')
    for e in S:
        if e['category']!=k: continue
        src=f'{e["source"]["creator"]} — {e["source"]["video"]} @ {e["source"]["start_s"]:.2f} s'
        if e['original_clip_name']: src+=f' (clip « {e["original_clip_name"]} »)'
        d=e['description']+(' ⚠️ '+' '.join(e['notes']) if e['notes'] else '')
        L.append(f'| [`{e["file"].split("/")[1]}`]({e["file"]}) | {e["duration_s"]:.2f} s | {d} | {src} |')
    L.append('')
L.append('## Méthode d’extraction\n')
L.append('''- Chaque vidéo montre une timeline qui défile sous une tête de lecture fixe. La timeline a été reconstruite image par image (panorama « slit-scan » avec mesure du défilement par corrélation de phase) pour identifier chaque clip, sa piste et son nom.
- Les coupes ont ensuite été calées sur l’audio à la milliseconde : début au point le plus calme juste avant l’attaque, fin à l’extinction naturelle du son (ou à la coupe franche quand le son suivant enchaîne).
- Micro-fondus anti-clic (2 ms en entrée, 6 à 12 ms en sortie), fondus plus longs uniquement pour les sons coupés net par le montage ou la fin de la vidéo d’origine (signalés ⚠️).
- Doublons détectés par corrélation croisée des formes d’onde ; la version la plus longue et la plus propre a été conservée.
- La vidéo « 10 Sound Effects » contient une musique de fond sous les SFX : elle a été atténuée d’environ 15 dB par soustraction spectrale (signalé ⚠️ sur ces 10 sons). L’intro et la fin de cette vidéo ne contiennent que de la voix off et n’ont pas été extraites.
- Les noms des clips lus sur les timelines sont indiqués quand ils étaient lisibles ; certains sont tronqués à l’écran (« ... »).
''')
L.append('## Droits\n')
L.append('Ces sons proviennent de vidéos partagées gratuitement par leurs créateurs ; plusieurs portent des noms de banques connues (Mixkit, Epidemic Sound « ES_ », Adobe…). '
         'Vérifier la licence de la banque d’origine avant un usage commercial ou une redistribution publique.\n')
open(f'{D}/README.md','w').write('\n'.join(L))

# ---- index.html ----
J=json.dumps(dict(categories=cats,sounds=S),ensure_ascii=False)
H='''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bibliothèque SFX</title>
<style>
:root{--bg:#0f1115;--card:#181b22;--fg:#e8eaf0;--mut:#9aa1b2;--acc:#7c9cff}
*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
header{position:sticky;top:0;background:rgba(15,17,21,.95);backdrop-filter:blur(6px);padding:14px 18px;border-bottom:1px solid #262a33;z-index:2}
h1{font-size:18px;margin:0 0 10px}input{width:100%;padding:9px 12px;border-radius:8px;border:1px solid #2c313c;background:#11141a;color:var(--fg);font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.chip{padding:5px 10px;border-radius:999px;border:1px solid #2c313c;background:#141821;color:var(--mut);cursor:pointer;font-size:13px}
.chip.on{background:var(--acc);border-color:var(--acc);color:#0b0d12}
main{padding:12px 18px 40px;max-width:1100px;margin:auto}h2{font-size:15px;color:var(--mut);margin:22px 0 8px;text-transform:uppercase;letter-spacing:.06em}
.s{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;background:var(--card);border-radius:10px;padding:10px 12px;margin:6px 0}
.s button{width:38px;height:38px;border-radius:50%;border:0;background:var(--acc);color:#0b0d12;font-size:15px;cursor:pointer}
.s .n{font-weight:600;font-family:ui-monospace,Menlo,monospace;font-size:13.5px}.s .d{color:var(--mut);font-size:13.5px}.s .t{color:var(--mut);font-size:12.5px;white-space:nowrap}
.s .w{color:#e5b45c}.s a{color:var(--mut);font-size:12px}
</style></head><body>
<header><h1>Bibliothèque SFX — <span id="count"></span></h1><input id="q" placeholder="Rechercher (whoosh, clic, impact, papier…)"><div class="chips" id="chips"></div></header>
<main id="list"></main>
<script>
const DATA=__DATA__;let cat=null;const audio=new Audio();let playing=null;
const chips=document.getElementById('chips'),list=document.getElementById('list'),q=document.getElementById('q');
function chip(k,l){const b=document.createElement('button');b.className='chip';b.textContent=l;b.onclick=()=>{cat=(cat===k?null:k);render()};b.dataset.k=k;chips.appendChild(b)}
chip('__all','Tout');for(const[k,v]of Object.entries(DATA.categories))chip(k,v.label+' ('+v.count+')');
function render(){const t=q.value.toLowerCase().trim();list.innerHTML='';let n=0;
 for(const c of chips.children)c.classList.toggle('on',c.dataset.k===(cat||'__all'));
 for(const[k,v]of Object.entries(DATA.categories)){if(cat&&cat!==k&&cat!=='__all')continue;
  const items=DATA.sounds.filter(s=>s.category===k&&(!t||(s.id+' '+s.description+' '+s.original_clip_name).toLowerCase().includes(t)));
  if(!items.length)continue;const h=document.createElement('h2');h.textContent=v.label+' — '+v.usage;list.appendChild(h);
  for(const s of items){n++;const d=document.createElement('div');d.className='s';
   d.innerHTML=`<button aria-label="Écouter">▶</button><div><div class="n">${s.id}</div><div class="d">${s.description}${s.notes.length?' <span class="w">⚠ '+s.notes.join(' ')+'</span>':''}</div></div><div class="t">${s.duration_s.toFixed(2)} s<br><a href="${s.file}" download>télécharger</a></div>`;
   const b=d.querySelector('button');b.onclick=()=>{if(playing===b&&!audio.paused){audio.pause();b.textContent='▶';return}
    if(playing)playing.textContent='▶';audio.src=s.file;audio.currentTime=0;audio.play();b.textContent='■';playing=b};
   list.appendChild(d)}}
 document.getElementById('count').textContent=n+' sons'}
audio.onended=()=>{if(playing)playing.textContent='▶'};q.oninput=render;render();
</script></body></html>'''
open(f'{D}/index.html','w').write(H.replace('__DATA__',J))
print('ok')
