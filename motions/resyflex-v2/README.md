# Motion ResyFlex v2 — version cinématique

Vidéo verticale **40 s**, 1080×1920, 30 i/s : [`ResyFlex_motion_v2.mp4`](ResyFlex_motion_v2.mp4). Réalisée avec **Remotion**, une **vraie musique** et de **vrais effets sonores** (Mixkit), montée sur le tempo du morceau.

Contenu tiré uniquement de **resy-flex.com** (relevé le 28/11/2026) : logo officiel, photos et prix publiés, villes disponibles, fonctionnement (10 min max., acompte 30 %, QR Code), engagements, contact. Les captures d’écran du téléphone sont celles du vrai site.

## Montage
Musique « Let’s Move » à 120 BPM, démarrée à 12,035 s : son **drop tombe sur l’ouverture du logo (4,0 s)**, les phrases suivantes sur « Réservez » (20 s) et sur l’appel à l’action (36 s), avec un temps de silence juste avant. Chaque coup de grosse caisse fait pulser la caméra.

| Temps | Scène |
|---|---|
| 0–2 s | Villes en rafale sur de vraies photos (Abidjan, Korhogo, San-Pedro, Grand-Lahou) |
| 2–4 s | « Votre résidence meublée, partout en Côte d’Ivoire » + riser |
| 4–8 s | **Drop** : l’écran s’ouvre en forme du symbole ResyFlex → logo → TROUVEZ / RÉSERVEZ / SÉJOURNEZ → zoom traversant |
| 8–12 s | 01 · Trouvez — vrai site dans un téléphone 3D (accueil → liste qui défile) + fonctions réelles |
| 12–16 s | Carte de Côte d’Ivoire qui se dessine, 7 villes disponibles, compteur |
| 16–20 s | Annonces réelles en éventail 3D, flash photo, tampon « 100 % vérifiées » |
| 20–24 s | 02 · Réservez — cadran « 10 MIN », notification « Disponibilité confirmée » |
| 24–28 s | « 30 % » qui se remplit, Mobile Money / Portefeuille ResyFlex, pièces |
| 28–32 s | 03 · Séjournez — QR Code construit puis scanné, rayons de lumière, « Bienvenue chez vous » |
| 32–34 s | 4 engagements en rafale |
| 34–36 s | Propriétaires : inscription gratuite |
| 36–40 s | Logo, resy-flex.com, +225 01 01 01 46 04 |

Effets visuels : caméra pulsée et secousses sur les impacts, typographie cinétique lettre par lettre, masque en forme du logo, zoom traversant, mouvement filé avec flou, téléphones 3D avec reflet, grain de film, fuites de lumière, reflets anamorphiques, ondes de choc, particules.

## Son
- **84 effets sonores réels** (44 sons Mixkit différents : impacts de bande-annonce, risers, whooshes cinématiques, obturateurs photo, tic-tac, pièces, clé dans la serrure, sons d’interface…) placés automatiquement sur les événements de `src/timeline.json` (synchro sur l’attaque, le pic ou la fin). Liste : `audio/placement_sfx.json`.
- Vérifié dans le MP4 : −8 à +2 ms d’écart entre les impacts sonores et les images. −13,9 LUFS, crête −1 dBFS (normalisation EBU R128).

## Licences et crédits
- **Musique** : « Let’s Move », Mixkit — *Mixkit Stock Music Free License* (autorisée pour les réseaux sociaux et la publicité en ligne ; pas pour la TV/radio, les CD/DVD ni les jeux vidéo).
- **Effets sonores** : Mixkit — *Mixkit Sound Effects Free License*.
- Les fichiers Mixkit **ne sont pas dans le dépôt** (la licence interdit de les redistribuer seuls) : `npm run sounds` les retélécharge.
- **Carte** : contour de la Côte d’Ivoire d’après Natural Earth (domaine public).
- **Polices** : Poppins, Inter (licence OFL). Logo, photos et captures : resy-flex.com.

## Refaire / modifier
```
npm install
npm run sounds     # télécharge musique + effets Mixkit (audio/mixkit/)
npm run audio      # bande son → public/audio/mix.wav
npm run studio     # aperçu
npm run render     # MP4
```
