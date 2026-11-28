# Motion ResyFlex v3 — logo 3D

Vidéo verticale **42,5 s**, 1080×1920, 30 i/s : [`ResyFlex_motion_v3.mp4`](ResyFlex_motion_v3.mp4). Réalisée avec **Remotion + Three.js** (vrai rendu 3D WebGL), une vraie musique et de vrais effets sonores (Mixkit).

Contenu tiré uniquement de **resy-flex.com** (relevé le 28/11/2026). Aucun avis, chiffre ou témoignage inventé.

## Le logo en 3D
Le symbole ResyFlex est **reconstruit en vrai volume** à partir du fichier officiel `logo-full.png` : ses 4 formes sont vectorisées (`src/logo_mark_shapes.json`, 99,9 % de recouvrement avec l’original), puis extrudées avec biseaux, matière orange métallisée vernie, reflets d’environnement, lumière balayante, faisceaux et particules.
- **Ouverture (0–9,7 s)** : les 4 pièces arrivent en tournoyant depuis la profondeur, se verrouillent une à une sur la montée, puis **claquent ensemble sur le drop** (6,0 s) avec flash, onde de choc et secousse ; la caméra tourne autour du symbole.
- **Final (35,5–42,5 s)** : le symbole se reforme sous un autre angle, puis l’appel à l’action.
- Le nom « ResyFlex » et le slogan sont le **fichier officiel** (non redessinés), posés sur un cartouche crème pour rester lisibles sur fond sombre.

## Montage sur la musique
« Cat Walk » d’Arulo (130 BPM), démarrée à 23,52 s : le **1er drop** tombe sur l’assemblage du logo (6,0 s), le **break** devient un moment de suspense (« Le propriétaire confirme… », cadran 10 MIN, battements de cœur, une seconde de quasi-silence) et le **2e drop** (22,6 s) déclenche « Disponibilité confirmée ».

| Temps | Scène |
|---|---|
| 0–6 s | Assemblage 3D du symbole + « Votre prochain séjour commence ici. » |
| 6–9,7 s | Drop : logo 3D, nom officiel, « Résidences meublées en Côte d’Ivoire » |
| 9,7–13,4 s | Rafale sur chaque demi-mesure : vraies photos, TROUVEZ / RÉSERVEZ / SÉJOURNEZ, villes, slogan |
| 13,4–17,1 s | **Carte 3D** de la Côte d’Ivoire qui s’élève, 7 colonnes lumineuses sur les villes disponibles |
| 17,1–20,5 s | **Carrousel 3D** de 8 vraies résidences, tampon « 100 % vérifiées » |
| 20,5–22,6 s | Break : 10 MIN, suspense |
| 22,6–26,3 s | 2e drop : disponibilité confirmée, acompte 30 % (Mobile Money / Portefeuille ResyFlex) |
| 26,3–30 s | QR Code scanné à l’arrivée, « Bienvenue chez vous » |
| 30–33,7 s | 4 engagements |
| 33,7–35,5 s | Propriétaires : inscription gratuite |
| 35,5–42,5 s | Logo 3D, resy-flex.com, +225 01 01 01 46 04 |

## Son
100 effets sonores réels (48 sons Mixkit différents), placés automatiquement sur les événements de `src/timeline.json` ; liste dans `audio/placement_sfx.json`. Normalisation EBU R128 à −14 LUFS, crête −1 dBTP.

## Licences et crédits
- **Musique** : « Cat Walk », Arulo — Mixkit, *Stock Music Free License* (réseaux sociaux et publicité en ligne autorisés ; pas TV/radio, CD/DVD, jeux vidéo).
- **Effets sonores** : Mixkit, *Sound Effects Free License*.
- Les fichiers Mixkit ne sont **pas** dans le dépôt (redistribution interdite) : `npm run sounds` les retélécharge à l’identique.
- **Carte** : Natural Earth (domaine public). **Polices** : Poppins, Inter (OFL). Logo, photos : resy-flex.com.

## Refaire / modifier
```
npm install
npm run sounds && npm run audio
npm run studio
npm run render      # sur une machine sans GPU : remplacer --gl=angle par --gl=swangle
```
`src/three3d.tsx` contient les scènes 3D (logo, carte, carrousel) ; `src/ResyFlex3.tsx` le montage ; `src/kit.tsx` les éléments communs.
