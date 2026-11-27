# Bibliothèque SFX — motion design × UCS

**275 effets sonores** rangés selon le standard professionnel **UCS v8.2.1** (Universal Category System) et regroupés en **23 familles motion design** :

- **133 sons extraits** de 14 vidéos gratuites de créateurs de motion design (Suraj Editing Tips, @piero.cesti, « 10 Sound Effects Every Editor Must Use ») ;
- **142 sons synthétisés** par code pour couvrir toutes les familles motion (risers, braams, drones, logo reveals, UI, glitch, magie…).

C’est la bibliothèque de référence pour les effets sonores de toutes les motions de ce projet.

- **Écouter / chercher** : ouvrir [`index.html`](index.html) (filtres par famille motion, par catégorie UCS et par origine).
- **Données** : [`catalogue.json`](catalogue.json) — CatID, catégorie/sous-catégorie (EN + FR), famille motion, description, durée, origine.
- **Référence UCS complète** : [`_ucs/UCS_v8.2.1_liste_complete.csv`](_ucs/UCS_v8.2.1_liste_complete.csv) — les 82 catégories et 753 sous-catégories avec traductions FR, définitions et synonymes, pour classer de futurs sons.
- **Format** : WAV PCM 16 bits, 48 kHz, stéréo, crête à −1 dBFS. Métadonnées intégrées dans chaque WAV (titre, auteur, catégorie UCS, description).

## Organisation

```
sfx/
├── <CATÉGORIE UCS>/            82 dossiers officiels (DESIGNED, SWOOSHES, USER INTERFACE, …)
│   ├── _UCS_<CATÉGORIE>.txt     fiche : sous-catégories, CatID, traductions, définitions
│   └── CatID_FXName_CreatorID_SourceID.wav
├── _ucs/                       liste UCS complète (CSV)
├── _outils/                    scripts : extraction depuis vidéos + moteur de synthèse
├── catalogue.json · index.html · README.md
```
Les 22 catégories UCS utilisées aujourd’hui contiennent des sons ; les 60 autres sont prêtes à recevoir de vrais enregistrements (animaux, véhicules, portes, eau, foules…), chacune avec sa fiche de sous-catégories.

### Convention de nommage UCS

`CatID_FXName_CreatorID_SourceID.wav` — ex. `DSGNRise_Synth Riser_MotionSynth_MotionLib.wav`

| Bloc | Rôle | Valeurs ici |
|---|---|---|
| **CatID** | catégorie + sous-catégorie UCS (code officiel, casse respectée) | `WHSH`, `DSGNImpt`, `UIClick`… |
| **FXName** | titre court (≤ 25 caractères), sans `_` ni `-` | `Air Whoosh Long` |
| **CreatorID** | auteur | `MotionSynth` (synthèse), `SurajET`, `PieroCesti`, `Unknown` |
| **SourceID** | bibliothèque / projet d’origine | `MotionLib`, `SurajSFX04`, `PieroCestiSFX`, `TenSFXEditors` |

Les outils compatibles UCS (Soundminer, BaseHead, Reaper + UCS Toolkit, Audio Category Clipper…) lisent la catégorie directement depuis le nom.

## Les familles motion design

| Famille | Usage | Nb |
|---|---|---|
| [Whoosh](#whoosh) | Entrées/sorties d’éléments, mouvements de caméra, passages. | 37 |
| [Swish / swipe](#swish--swipe) | Petits mouvements rapides, cartes et panneaux qui glissent. | 16 |
| [Riser / montée](#riser--montée) | Monter la tension avant une révélation ; caler la FIN sur l’impact. | 15 |
| [Impact / hit](#impact--hit) | Temps forts : titre qui tombe, coupe, révélation. | 15 |
| [Boom / sub drop](#boom--sub-drop) | Renfort grave sous un impact ou un drop. | 11 |
| [Braam](#braam) | Gros son cuivré de bande-annonce : moment dramatique. | 4 |
| [Stinger / logo reveal](#stinger--logo-reveal) | Signature sonore complète pour un logo ou une fin de vidéo. | 6 |
| [Transition](#transition) | Changement de scène (montée + impact, tape stop, glitch, ralenti). | 15 |
| [Drone / nappe](#drone--nappe) | Fond sonore tenu (bouclable) : tension, mystère, technologie. | 4 |
| [Ambiance](#ambiance) | Fond d’ambiance bouclable : pièce, vent, salle high-tech, sci-fi. | 4 |
| [UI clic / tap](#ui-clic--tap) | Boutons, curseur, toggles, sélections. | 20 |
| [Pop / bulle](#pop--bulle) | Apparition/disparition d’éléments, bulles, puces. | 12 |
| [UI bip / données](#ui-bip--données) | Bips, chargement, données, interfaces high-tech, texte qui s’écrit. | 15 |
| [Notification / alerte](#notification--alerte) | Succès, erreur, notification, récompense, argent. | 20 |
| [Glitch / numérique](#glitch--numérique) | Glitchs, statique, corruption : style tech, erreurs. | 21 |
| [Électrique / laser / énergie](#électrique--laser--énergie) | Zaps, étincelles, lasers, charges d’énergie, téléportation. | 9 |
| [Magie / scintillement](#magie--scintillement) | Paillettes, poufs magiques, glissandos féeriques. | 7 |
| [Cartoon / fun](#cartoon--fun) | Boings, sifflets, couinements, bonks : ton léger. | 11 |
| [Tonal / musical](#tonal--musical) | Accents musicaux : accords, cloches, marimba, petites phrases. | 6 |
| [Horloge / compteur](#horloge--compteur) | Tic-tac, comptes à rebours, compteurs de score. | 9 |
| [Battement / pulsation](#battement--pulsation) | Battements de cœur : suspense, émotion. | 2 |
| [Power up / down](#power-up--down) | Mise sous/hors tension, servos, mécanismes robotiques. | 3 |
| [Foley / objets](#foley--objets) | Sons d’objets réels : papier, chaîne, clavier, engrenages, feutre, obturateur. | 13 |

## Les catégories UCS utilisées

| Dossier UCS | Français | Sous-catégories UCS | Sons |
|---|---|---|---|
| [`AMBIENCE/`](AMBIENCE/) | AMBIANCE | 47 | 3 |
| [`BEEPS/`](BEEPS/) | BIPS | 6 | 2 |
| [`CARTOON/`](CARTOON/) | CARTOON | 22 | 23 |
| [`CHAINS/`](CHAINS/) | CHAÎNES | 5 | 4 |
| [`CLOCKS/`](CLOCKS/) | HORLOGES | 4 | 4 |
| [`COMMUNICATIONS/`](COMMUNICATIONS/) | COMMUNICATIONS | 13 | 4 |
| [`COMPUTERS/`](COMPUTERS/) | ORDINATEURS | 3 | 1 |
| [`DESIGNED/`](DESIGNED/) | DESIGN | 20 | 84 |
| [`ELECTRICITY/`](ELECTRICITY/) | ÉLECTRICITÉ | 6 | 3 |
| [`FIRE/`](FIRE/) | FEU | 10 | 1 |
| [`GAMES/`](GAMES/) | JEUX | 5 | 4 |
| [`HUMAN/`](HUMAN/) | HUMAIN | 14 | 2 |
| [`LASERS/`](LASERS/) | LASERS | 4 | 3 |
| [`MAGIC/`](MAGIC/) | MAGIE | 7 | 7 |
| [`MECHANICAL/`](MECHANICAL/) | MÉCANISMES | 12 | 5 |
| [`MUSICAL/`](MUSICAL/) | MUSICAL | 21 | 6 |
| [`OBJECTS/`](OBJECTS/) | OBJETS | 21 | 1 |
| [`PAPER/`](PAPER/) | PAPIER | 7 | 3 |
| [`SCIFI/`](SCIFI/) | SCIFI | 12 | 11 |
| [`SWOOSHES/`](SWOOSHES/) | SWOOSHES | 2 | 32 |
| [`USER INTERFACE/`](USER%20INTERFACE/) | INTERFACE | 7 | 71 |
| [`WIND/`](WIND/) | VENT | 7 | 1 |

Toutes les autres catégories (sur 82) existent en dossier vide avec leur fiche ; la liste complète est dans `_ucs/`.

## Règles d’utilisation dans les motions

1. **Un son = un événement visuel important** (apparition, impact, changement de scène). Pas de SFX sur les micro-mouvements.
2. **Caler l’attaque sur l’image clé** : les fichiers démarrent à l’attaque, sans silence en tête.
   - Exceptions : **risers**, **reverse** et **montées** se placent *avant* l’événement pour que leur **fin** tombe sur l’impact ou la coupe (elles s’arrêtent net exprès).
   - **Stingers / logo reveals** et **transitions** : caler le **pic de l’impact** sur l’apparition du logo ou la coupe.
3. **Choisir par famille** (tableau ci-dessus), puis varier : ne jamais enchaîner deux fois le même whoosh.
4. **Superposer** pour un temps fort : riser → impact + boom/sub drop (+ braam pour le dramatique).
5. **Boucles** (`Loop` dans le nom : drones, ambiances, chargement, tic-tac) : bouclables sans clic, à étirer sous toute une scène, 15–25 dB sous la voix.
6. **Mixage** : crêtes à −1 dBFS ; baisser les SFX de 6 à 12 dB sous la voix off, 3 à 6 dB sous la musique ; jamais deux impacts au même instant.

## Catalogue complet (par famille motion)

### Whoosh

Entrées/sorties d’éléments, mouvements de caméra, passages.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Double Whoosh`](DESIGNED/DSGNWhsh_Double%20Whoosh_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.42 s | Double whoosh aller-retour. | synthèse |
| [`Fast Pass By`](DESIGNED/DSGNWhsh_Fast%20Pass%20By_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 0.92 s | Passage très rapide (0,25 s), mouvement éclair. | synthèse |
| [`Heavy Whoosh Low`](DESIGNED/DSGNWhsh_Heavy%20Whoosh%20Low_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.81 s | Whoosh lourd et grave avec sub, pour gros éléments ou caméra. | synthèse |
| [`Tonal Whoosh`](DESIGNED/DSGNWhsh_Tonal%20Whoosh_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.50 s | Whoosh avec sifflement tonal, futuriste. | synthèse |
| [`Whoosh Cinematic`](DESIGNED/DSGNWhsh_Whoosh%20Cinematic_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 2.65 s | Whoosh cinématique large, grave + aigus, longue queue. | synthèse |
| [`Whoosh Swell Slow`](DESIGNED/DSGNWhsh_Whoosh%20Swell%20Slow_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 2.12 s | Whoosh qui gonfle lentement (pic tardif), avant une révélation. | synthèse |
| [`Air Whoosh Long`](SWOOSHES/WHSH_Air%20Whoosh%20Long_MotionSynth_MotionLib.wav) | `WHSH` SWOOSHES › WHOOSH | 2.12 s | Whoosh d’air long et ample (1,4 s). | synthèse |
| [`Air Whoosh Medium`](SWOOSHES/WHSH_Air%20Whoosh%20Medium_MotionSynth_MotionLib.wav) | `WHSH` SWOOSHES › WHOOSH | 1.52 s | Whoosh d’air moyen (0,7 s), polyvalent pour entrées/sorties. | synthèse |
| [`Air Whoosh Short`](SWOOSHES/WHSH_Air%20Whoosh%20Short_MotionSynth_MotionLib.wav) | `WHSH` SWOOSHES › WHOOSH | 1.22 s | Whoosh d’air court (0,35 s), passage gauche→droite. | synthèse |
| [`Airy Whoosh Bright`](SWOOSHES/WHSH_Airy%20Whoosh%20Bright_MotionSynth_MotionLib.wav) | `WHSH` SWOOSHES › WHOOSH | 1.17 s | Whoosh aérien et brillant (aigus), élégant pour du texte. | synthèse |
| [`Epic Fast Whoosh`](DESIGNED/DSGNWhsh_Epic%20Fast%20Whoosh_SurajET_SurajSFX10.wav) | `DSGNWhsh` DESIGN › WHOOSH | 0.48 s | Whoosh rapide et percutant. | SurajET — Sound Effect Part 10 @ 0.55 s |
| [`Heavy Rumble Whoosh`](DESIGNED/DSGNWhsh_Heavy%20Rumble%20Whoosh_SurajET_SurajSFX07.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.45 s | Whoosh lourd et grondant (1,5 s). | SurajET — Sound Effect Part 7 @ 1.71 s |
| [`Heavy Whoosh`](DESIGNED/DSGNWhsh_Heavy%20Whoosh_SurajET_SurajSFX14.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.11 s | Whoosh lourd. | SurajET — Sound Effect Part 14 @ 5.69 s |
| [`Shimmer Whoosh Tonal`](DESIGNED/DSGNWhsh_Shimmer%20Whoosh%20Tonal_SurajET_SurajSFX12.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.79 s | Whoosh scintillant avec note tenue (1,8 s). | SurajET — Sound Effect Part 12 @ 2.00 s |
| [`Swoosh Chirp Down`](DESIGNED/DSGNWhsh_Swoosh%20Chirp%20Down_SurajET_SurajSFX12.wav) | `DSGNWhsh` DESIGN › WHOOSH | 0.74 s | Swoosh avec gazouillis descendant aigu. | SurajET — Sound Effect Part 12 @ 5.73 s |
| [`Swoosh Chirp Up`](DESIGNED/DSGNWhsh_Swoosh%20Chirp%20Up_SurajET_SurajSFX10.wav) | `DSGNWhsh` DESIGN › WHOOSH | 0.44 s | Swoosh en glissando montant (0,4 s). | SurajET — Sound Effect Part 10 @ 5.06 s |
| [`Whoosh Tonal Hit`](DESIGNED/DSGNWhsh_Whoosh%20Tonal%20Hit_Unknown_TenSFXEditors.wav) | `DSGNWhsh` DESIGN › WHOOSH | 0.31 s | Whoosh avec note. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 11.41 s |
| [`Zoom In High`](DESIGNED/DSGNWhsh_Zoom%20In%20High_SurajET_SurajSFXWhoosh.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.00 s | « Zoom » très aigu qui monte. Zoom avant, apparition rapide. | SurajET — Sound Effects (whoosh) @ 9.94 s |
| [`Fire Burst Whoosh`](FIRE/FIREWhsh_Fire%20Burst%20Whoosh_SurajET_SurajSFX06.wav) | `FIREWhsh` FEU › WHOOSH | 1.41 s | Souffle de flamme / embrasement. | SurajET — Sound Effect Part 6 @ 3.71 s |
| [`Air Whoosh`](SWOOSHES/WHSH_Air%20Whoosh_SurajET_SurajSFX14.wav) | `WHSH` SWOOSHES › WHOOSH | 1.25 s | Whoosh d’air. | SurajET — Sound Effect Part 14 @ 6.79 s |
| [`Air Whoosh Long`](SWOOSHES/WHSH_Air%20Whoosh%20Long_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 1.99 s | Whoosh long (2 s). | SurajET — Sound Effects (whoosh) @ 5.78 s |
| [`Air Whoosh Punchy`](SWOOSHES/WHSH_Air%20Whoosh%20Punchy_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 0.96 s | Whoosh puissant et court. | SurajET — Sound Effects (whoosh) @ 4.82 s |
| [`Air Whoosh Sharp Attack`](SWOOSHES/WHSH_Air%20Whoosh%20Sharp%20Attack_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 1.14 s | Whoosh à attaque franche. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effects (whoosh) @ 2.31 s |
| [`Air Whoosh Soft Wide`](SWOOSHES/WHSH_Air%20Whoosh%20Soft%20Wide_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 1.46 s | Whoosh doux et large. | SurajET — Sound Effects (whoosh) @ 7.77 s |
| [`Air Whoosh Swell`](SWOOSHES/WHSH_Air%20Whoosh%20Swell_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 1.34 s | Whoosh qui gonfle puis retombe. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effects (whoosh) @ 3.44 s |
| [`Air Whoosh Tonal`](SWOOSHES/WHSH_Air%20Whoosh%20Tonal_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 1.12 s | Whoosh d’air avec un ton léger. | SurajET — Sound Effects (whoosh) @ 0.05 s |
| [`Air Whoosh Wide`](SWOOSHES/WHSH_Air%20Whoosh%20Wide_SurajET_SurajSFXWhoosh.wav) | `WHSH` SWOOSHES › WHOOSH | 1.10 s | Whoosh d’air ample. | SurajET — Sound Effects (whoosh) @ 1.20 s |
| [`Noise Burst Whoosh`](SWOOSHES/WHSH_Noise%20Burst%20Whoosh_SurajET_SurajSFX08.wav) | `WHSH` SWOOSHES › WHOOSH | 0.46 s | Bouffée de bruit brève. | SurajET — Sound Effect Part 8 @ 5.97 s |
| [`Noise Whoosh A`](SWOOSHES/WHSH_Noise%20Whoosh%20A_SurajET_SurajSFX12.wav) | `WHSH` SWOOSHES › WHOOSH | 0.79 s | Whoosh bruité. | SurajET — Sound Effect Part 12 @ 6.47 s |
| [`Noise Whoosh B`](SWOOSHES/WHSH_Noise%20Whoosh%20B_SurajET_SurajSFX.wav) | `WHSH` SWOOSHES › WHOOSH | 0.67 s | Whoosh bruité. | SurajET — Sound Effects @ 5.30 s |
| [`Noise Whoosh Short`](SWOOSHES/WHSH_Noise%20Whoosh%20Short_SurajET_SurajSFX08.wav) | `WHSH` SWOOSHES › WHOOSH | 0.54 s | Souffle bruité court. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 8 @ 0.01 s |
| [`Swoosh Down`](SWOOSHES/WHSH_Swoosh%20Down_Unknown_TenSFXEditors.wav) | `WHSH` SWOOSHES › WHOOSH | 0.52 s | Swoosh descendant. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 13.43 s |
| [`Textured Whoosh`](SWOOSHES/WHSH_Textured%20Whoosh_SurajET_SurajSFX08.wav) | `WHSH` SWOOSHES › WHOOSH | 0.78 s | Whoosh texturé. | SurajET — Sound Effect Part 8 @ 1.03 s |
| [`Textured Whoosh Rising`](SWOOSHES/WHSH_Textured%20Whoosh%20Rising_SurajET_SurajSFX12.wav) | `WHSH` SWOOSHES › WHOOSH | 0.81 s | Whoosh texturé qui monte. | SurajET — Sound Effect Part 12 @ 1.07 s |
| [`Whoosh Swell B`](SWOOSHES/WHSH_Whoosh%20Swell%20B_SurajET_SurajSFX.wav) | `WHSH` SWOOSHES › WHOOSH | 0.59 s | Whoosh qui gonfle. | SurajET — Sound Effects @ 8.04 s |
| [`Whoosh Swell Short`](SWOOSHES/WHSH_Whoosh%20Swell%20Short_SurajET_SurajSFX08.wav) | `WHSH` SWOOSHES › WHOOSH | 0.44 s | Whoosh qui gonfle vers un pic (0,5 s). | SurajET — Sound Effect Part 8 @ 3.65 s |
| [`Whoosh Up`](SWOOSHES/WHSH_Whoosh%20Up_SurajET_SurajSFX15.wav) | `WHSH` SWOOSHES › WHOOSH | 0.67 s | Whoosh montant vers l’aigu. | SurajET — Sound Effect Part 15 @ 6.78 s |

### Swish / swipe

Petits mouvements rapides, cartes et panneaux qui glissent.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Swish Sharp`](SWOOSHES/SWSH_Swish%20Sharp_MotionSynth_MotionLib.wav) | `SWSH` SWOOSHES › SWISH | 0.20 s | Swish tranchant (aigus). | synthèse |
| [`Swish Short`](SWOOSHES/SWSH_Swish%20Short_MotionSynth_MotionLib.wav) | `SWSH` SWOOSHES › SWISH | 0.22 s | Swish court et net (0,22 s). | synthèse |
| [`Swish Soft`](SWOOSHES/SWSH_Swish%20Soft_MotionSynth_MotionLib.wav) | `SWSH` SWOOSHES › SWISH | 0.30 s | Swish doux et feutré. | synthèse |
| [`Swish Tiny`](SWOOSHES/SWSH_Swish%20Tiny_MotionSynth_MotionLib.wav) | `SWSH` SWOOSHES › SWISH | 0.15 s | Micro-swish (0,15 s) : petit élément, icône. | synthèse |
| [`Zip Up`](CARTOON/TOONZip_Zip%20Up_MotionSynth_MotionLib.wav) | `TOONZip` CARTOON › ZIP | 0.14 s | Zip rapide montant (0,12 s). | synthèse |
| [`Slide In Soft`](USER%20INTERFACE/UIMvmt_Slide%20In%20Soft_MotionSynth_MotionLib.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.45 s | Entrée glissée douce d’un panneau. | synthèse |
| [`Swipe Left`](USER%20INTERFACE/UIMvmt_Swipe%20Left_MotionSynth_MotionLib.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.28 s | Glissement d’interface vers la gauche (carte, slide). | synthèse |
| [`Swipe Right`](USER%20INTERFACE/UIMvmt_Swipe%20Right_MotionSynth_MotionLib.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.28 s | Glissement d’interface vers la droite. | synthèse |
| [`Double Swish`](SWOOSHES/SWSH_Double%20Swish_SurajET_SurajSFX06.wav) | `SWSH` SWOOSHES › SWISH | 0.79 s | Double swish (aller-retour). | SurajET — Sound Effect Part 6 @ 13.95 s |
| [`Micro Swish`](SWOOSHES/SWSH_Micro%20Swish_SurajET_SurajSFX04.wav) | `SWSH` SWOOSHES › SWISH | 0.16 s | Micro-swish très bref (0,2 s). Petit mouvement rapide. | SurajET — Sound Effect Part 4 @ 7.96 s |
| [`Noise Swish Short`](SWOOSHES/SWSH_Noise%20Swish%20Short_SurajET_SurajSFX08.wav) | `SWSH` SWOOSHES › SWISH | 0.38 s | Swish bruité court. | SurajET — Sound Effect Part 8 @ 0.56 s |
| [`Swish Center Peak`](SWOOSHES/SWSH_Swish%20Center%20Peak_SurajET_SurajSFX15.wav) | `SWSH` SWOOSHES › SWISH | 0.91 s | Swish net avec pic central. | SurajET — Sound Effect Part 15 @ 1.91 s |
| [`Swish Short B`](SWOOSHES/SWSH_Swish%20Short%20B_SurajET_SurajSFX.wav) | `SWSH` SWOOSHES › SWISH | 0.39 s | Swish court. | SurajET — Sound Effects @ 5.96 s |
| [`Swish With Pop`](SWOOSHES/SWSH_Swish%20With%20Pop_SurajET_SurajSFX.wav) | `SWSH` SWOOSHES › SWISH | 0.28 s | Swish court avec pop. | SurajET — Sound Effects @ 0.12 s |
| [`Zip Sweep Up`](CARTOON/TOONZip_Zip%20Sweep%20Up_Unknown_TenSFXEditors.wav) | `TOONZip` CARTOON › ZIP | 0.10 s | Zip bref (balayage montant). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 10.25 s |
| [`Card Swipe Short`](USER%20INTERFACE/UIMvmt_Card%20Swipe%20Short_SurajET_SurajSFX06.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.49 s | Petits swishs rapides, glissement de carte/UI. | SurajET — Sound Effect Part 6 @ 1.56 s |

### Riser / montée

Monter la tension avant une révélation ; caler la FIN sur l’impact.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Noise Riser 2s`](DESIGNED/DSGNRise_Noise%20Riser%202s_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 2.00 s | Montée de bruit (2 s) qui s’arrête net : à caler pour finir sur l’impact. | synthèse |
| [`Noise Riser 4s`](DESIGNED/DSGNRise_Noise%20Riser%204s_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 4.00 s | Montée de bruit longue (4 s). | synthèse |
| [`Reverse Cymbal`](DESIGNED/DSGNRise_Reverse%20Cymbal_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 1.80 s | Cymbale inversée (1,8 s) : se termine sur le temps fort. | synthèse |
| [`Reverse Whoosh Suck`](DESIGNED/DSGNRise_Reverse%20Whoosh%20Suck_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 1.20 s | Aspiration inversée (impact + réverb à l’envers), 1,2 s. | synthèse |
| [`Shepard Riser`](DESIGNED/DSGNRise_Shepard%20Riser_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 5.42 s | Montée « infinie » (illusion de Shepard), 4 s : tension continue. | synthèse |
| [`Synth Riser`](DESIGNED/DSGNRise_Synth%20Riser_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 3.00 s | Montée synthé (supersaw qui monte de 2 octaves + filtre qui s’ouvre), 3 s. | synthèse |
| [`Tension Riser`](DESIGNED/DSGNRise_Tension%20Riser_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 3.00 s | Montée de tension : cluster de sons qui monte avec tremolo qui accélère (3 s). | synthèse |
| [`Uplifter Short`](DESIGNED/DSGNRise_Uplifter%20Short_MotionSynth_MotionLib.wav) | `DSGNRise` DESIGN › RISER | 1.00 s | Petite montée courte (1 s) pour un changement de plan. | synthèse |
| [`Cinematic Swell A`](DESIGNED/DSGNRise_Cinematic%20Swell%20A_SurajET_SurajSFX12.wav) | `DSGNRise` DESIGN › RISER | 4.40 s | Grande montée cinématique qui gonfle puis s’apaise (4,4 s). ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 12 @ 10.22 s |
| [`Cinematic Swell B`](DESIGNED/DSGNRise_Cinematic%20Swell%20B_SurajET_SurajSFX12.wav) | `DSGNRise` DESIGN › RISER | 4.09 s | Grande montée cinématique (4,3 s). ⚠️ Coupé par la fin de la vidéo source (fondu 300 ms). | SurajET — Sound Effect Part 12 @ 14.78 s |
| [`Harmonic Riser`](DESIGNED/DSGNRise_Harmonic%20Riser_SurajET_SurajSFX15.wav) | `DSGNRise` DESIGN › RISER | 1.76 s | Montée harmonique (hauteur qui monte, 1,8 s). | SurajET — Sound Effect Part 15 @ 7.59 s |
| [`Noise Build`](DESIGNED/DSGNRise_Noise%20Build_SurajET_SurajSFX.wav) | `DSGNRise` DESIGN › RISER | 2.52 s | Montée de bruit (2,5 s) qui culmine puis retombe. | SurajET — Sound Effects @ 9.75 s |
| [`Reverse Whoosh Stop`](DESIGNED/DSGNRise_Reverse%20Whoosh%20Stop_SurajET_SurajSFX15.wav) | `DSGNRise` DESIGN › RISER | 0.60 s | Whoosh inversé qui s’arrête net : à placer juste avant un impact ou une coupe. | SurajET — Sound Effect Part 15 @ 9.42 s |
| [`Short Riser Hard Stop`](DESIGNED/DSGNRise_Short%20Riser%20Hard%20Stop_SurajET_SurajSFX06.wav) | `DSGNRise` DESIGN › RISER | 0.76 s | Montée courte qui s’arrête net (0,8 s). | SurajET — Sound Effect Part 6 @ 12.12 s |
| [`Tonal Swell`](DESIGNED/DSGNRise_Tonal%20Swell_SurajET_SurajSFX14.wav) | `DSGNRise` DESIGN › RISER | 2.03 s | Nappe qui gonfle avec note (2 s). | SurajET — Sound Effect Part 14 @ 3.61 s |

### Impact / hit

Temps forts : titre qui tombe, coupe, révélation.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Bright Glass Hit`](DESIGNED/DSGNImpt_Bright%20Glass%20Hit_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 2.20 s | Impact brillant/cristallin. | synthèse |
| [`Cinematic Hit Big`](DESIGNED/DSGNImpt_Cinematic%20Hit%20Big_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 4.53 s | Gros impact cinématique avec longue queue (3 s). | synthèse |
| [`Deep Hit Reverb`](DESIGNED/DSGNImpt_Deep%20Hit%20Reverb_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 4.60 s | Impact profond avec grande réverbération. | synthèse |
| [`Metallic Hit`](DESIGNED/DSGNImpt_Metallic%20Hit_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 2.67 s | Impact métallique qui résonne. | synthèse |
| [`Punch Hit Short`](DESIGNED/DSGNImpt_Punch%20Hit%20Short_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 1.04 s | Impact sec et punchy, court : texte qui tombe, cut. | synthèse |
| [`Snap Hit Tight`](DESIGNED/DSGNImpt_Snap%20Hit%20Tight_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 0.54 s | Impact très serré (snap), pour les coupes rythmées. | synthèse |
| [`Soft Pillow Hit`](DESIGNED/DSGNImpt_Soft%20Pillow%20Hit_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 1.72 s | Impact doux et feutré, sans attaque agressive. | synthèse |
| [`Trailer Hit Distorted`](DESIGNED/DSGNImpt_Trailer%20Hit%20Distorted_MotionSynth_MotionLib.wav) | `DSGNImpt` DESIGN › IMPACT | 4.30 s | Impact de bande-annonce saturé et massif. | synthèse |
| [`Cinematic Boom Debris`](DESIGNED/DSGNImpt_Cinematic%20Boom%20Debris_SurajET_SurajSFX11.wav) | `DSGNImpt` DESIGN › IMPACT | 3.09 s | Impact cinématique grave avec débris aigus (3,1 s). | SurajET — Sound Effect Part 11 @ 0.11 s |
| [`Cinematic Boom Sub`](DESIGNED/DSGNImpt_Cinematic%20Boom%20Sub_SurajET_SurajSFX11.wav) | `DSGNImpt` DESIGN › IMPACT | 2.11 s | Impact cinématique avec sub-basse. | SurajET — Sound Effect Part 11 @ 8.25 s |
| [`Cinematic Boom Sustain`](DESIGNED/DSGNImpt_Cinematic%20Boom%20Sustain_SurajET_SurajSFX11.wav) | `DSGNImpt` DESIGN › IMPACT | 2.10 s | Impact cinématique puissant et soutenu. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 11 @ 5.76 s |
| [`Cinematic Boom Tonal`](DESIGNED/DSGNImpt_Cinematic%20Boom%20Tonal_SurajET_SurajSFX11.wav) | `DSGNImpt` DESIGN › IMPACT | 2.56 s | Impact cinématique avec résonance tonale descendante (2,6 s). | SurajET — Sound Effect Part 11 @ 3.20 s |
| [`Hard Hit Rumble Tail`](DESIGNED/DSGNImpt_Hard%20Hit%20Rumble%20Tail_SurajET_SurajSFX04.wav) | `DSGNImpt` DESIGN › IMPACT | 4.78 s | Gros impact grave avec longue queue de grondement (4,8 s). Titre, révélation, drop. | SurajET — Sound Effect Part 4 @ 9.89 s |
| [`Reverb Hit`](DESIGNED/DSGNImpt_Reverb%20Hit_PieroCesti_PieroCestiSFX.wav) | `DSGNImpt` DESIGN › IMPACT | 1.36 s | Impact avec grande réverbération. ⚠️ Coupé par le montage source (fondu 120 ms). | PieroCesti — Comment "SFX" @ 3.73 s |
| [`Tonal Thump`](DESIGNED/DSGNImpt_Tonal%20Thump_Unknown_TenSFXEditors.wav) | `DSGNImpt` DESIGN › IMPACT | 0.42 s | Coup sourd tonal (pop grave). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 8.18 s |

### Boom / sub drop

Renfort grave sous un impact ou un drop.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Bass Dive`](DESIGNED/DSGNBass_Bass%20Dive_MotionSynth_MotionLib.wav) | `DSGNBass` DESIGN › BASS DIVE | 1.59 s | Plongée de basse rapide 220→30 Hz. | synthèse |
| [`Sub Drop 2s`](DESIGNED/DSGNBass_Sub%20Drop%202s_MotionSynth_MotionLib.wav) | `DSGNBass` DESIGN › BASS DIVE | 2.39 s | Sub drop : basse qui plonge 90→28 Hz (2 s). | synthèse |
| [`Sub Drop Long`](DESIGNED/DSGNBass_Sub%20Drop%20Long_MotionSynth_MotionLib.wav) | `DSGNBass` DESIGN › BASS DIVE | 3.59 s | Sub drop long (3,5 s) pour une grosse révélation. | synthèse |
| [`Boom Deep Short`](DESIGNED/DSGNBoom_Boom%20Deep%20Short_MotionSynth_MotionLib.wav) | `DSGNBoom` DESIGN › BOOM | 1.96 s | Boom grave court, renfort de basse pour un temps fort. | synthèse |
| [`Boom Trailer`](DESIGNED/DSGNBoom_Boom%20Trailer_MotionSynth_MotionLib.wav) | `DSGNBoom` DESIGN › BOOM | 4.04 s | Boom de bande-annonce long et profond. | synthèse |
| [`Rumble Swell`](DESIGNED/DSGNRmbl_Rumble%20Swell_MotionSynth_MotionLib.wav) | `DSGNRmbl` DESIGN › RUMBLE | 3.00 s | Grondement qui monte puis s’éteint (3 s). | synthèse |
| [`Shing Drop`](DESIGNED/DSGNBass_Shing%20Drop_SurajET_SurajSFX14.wav) | `DSGNBass` DESIGN › BASS DIVE | 3.91 s | Drop de basse avec « shing » brillant tenu (3,9 s). | SurajET — Sound Effect Part 14 @ 8.05 s |
| [`Bass Hit Wobble`](DESIGNED/DSGNBoom_Bass%20Hit%20Wobble_SurajET_SurajSFX07.wav) | `DSGNBoom` DESIGN › BOOM | 0.81 s | Coup de basse avec ondulation. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 7 @ 5.29 s |
| [`Boom Long Tail`](DESIGNED/DSGNBoom_Boom%20Long%20Tail_SurajET_SurajSFX15.wav) | `DSGNBoom` DESIGN › BOOM | 3.19 s | Gros boom grave à longue queue (3,2 s). | SurajET — Sound Effect Part 15 @ 10.69 s |
| [`Soft Boom Swell`](DESIGNED/DSGNBoom_Soft%20Boom%20Swell_SurajET_SurajSFX15.wav) | `DSGNBoom` DESIGN › BOOM | 1.86 s | Boom grave enveloppé qui gonfle puis s’éteint (1,9 s). | SurajET — Sound Effect Part 15 @ 0.05 s |
| [`Textured Rumble`](DESIGNED/DSGNRmbl_Textured%20Rumble_SurajET_SurajSFX.wav) | `DSGNRmbl` DESIGN › RUMBLE | 1.12 s | Grondement texturé. | SurajET — Sound Effects @ 8.63 s |

### Braam

Gros son cuivré de bande-annonce : moment dramatique.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Braam Bright`](DESIGNED/DSGNBram_Braam%20Bright_MotionSynth_MotionLib.wav) | `DSGNBram` DESIGN › BRAAM | 5.36 s | Braam cuivré plus brillant. | synthèse |
| [`Braam Dark`](DESIGNED/DSGNBram_Braam%20Dark_MotionSynth_MotionLib.wav) | `DSGNBram` DESIGN › BRAAM | 5.59 s | Braam sombre et massif (3 s), façon bande-annonce. | synthèse |
| [`Braam Rising`](DESIGNED/DSGNBram_Braam%20Rising_MotionSynth_MotionLib.wav) | `DSGNBram` DESIGN › BRAAM | 5.99 s | Braam qui monte d’un ton (3,5 s) : tension grandissante. | synthèse |
| [`Braam Stab Short`](DESIGNED/DSGNBram_Braam%20Stab%20Short_MotionSynth_MotionLib.wav) | `DSGNBram` DESIGN › BRAAM | 3.73 s | Braam court (1 s), coup de poing sonore. | synthèse |

### Stinger / logo reveal

Signature sonore complète pour un logo ou une fin de vidéo.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Logo Reveal Corporate`](DESIGNED/DSGNStngr_Logo%20Reveal%20Corporate_MotionSynth_MotionLib.wav) | `DSGNStngr` DESIGN › STINGER | 5.73 s | Révélation de logo « corporate » : aspiration inversée → impact doux + accord cristallin. | synthèse |
| [`Logo Reveal Epic`](DESIGNED/DSGNStngr_Logo%20Reveal%20Epic_MotionSynth_MotionLib.wav) | `DSGNStngr` DESIGN › STINGER | 6.30 s | Révélation épique : montée → impact bande-annonce + braam. | synthèse |
| [`Logo Reveal Minimal`](DESIGNED/DSGNStngr_Logo%20Reveal%20Minimal_MotionSynth_MotionLib.wav) | `DSGNStngr` DESIGN › STINGER | 2.38 s | Révélation minimaliste : pop + ding propre. | synthèse |
| [`Logo Reveal Sparkle`](DESIGNED/DSGNStngr_Logo%20Reveal%20Sparkle_MotionSynth_MotionLib.wav) | `DSGNStngr` DESIGN › STINGER | 5.61 s | Révélation magique : glissando scintillant → accord brillant. | synthèse |
| [`Logo Reveal Tech`](DESIGNED/DSGNStngr_Logo%20Reveal%20Tech_MotionSynth_MotionLib.wav) | `DSGNStngr` DESIGN › STINGER | 2.31 s | Révélation de logo tech : glitch → impact numérique + bips. | synthèse |
| [`Whoosh Hit Logo`](DESIGNED/DSGNStngr_Whoosh%20Hit%20Logo_MotionSynth_MotionLib.wav) | `DSGNStngr` DESIGN › STINGER | 2.02 s | Whoosh + impact serré : apparition de logo dynamique. | synthèse |

### Transition

Changement de scène (montée + impact, tape stop, glitch, ralenti).

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Glitch Transition`](DESIGNED/DSGNMorph_Glitch%20Transition_MotionSynth_MotionLib.wav) | `DSGNMorph` DESIGN › TRANSFORMATION | 1.05 s | Transition glitch : hachures qui accélèrent + bitcrush (1 s). | synthèse |
| [`Swirl Morph`](DESIGNED/DSGNMorph_Swirl%20Morph_MotionSynth_MotionLib.wav) | `DSGNMorph` DESIGN › TRANSFORMATION | 2.68 s | Tourbillon spatial (son qui tourne autour de l’auditeur), 1,8 s. | synthèse |
| [`Tape Start`](DESIGNED/DSGNMorph_Tape%20Start_MotionSynth_MotionLib.wav) | `DSGNMorph` DESIGN › TRANSFORMATION | 1.60 s | Démarrage de bande (le son accélère jusqu’à la vitesse normale). | synthèse |
| [`Tape Stop`](DESIGNED/DSGNMorph_Tape%20Stop_MotionSynth_MotionLib.wav) | `DSGNMorph` DESIGN › TRANSFORMATION | 1.40 s | Arrêt de bande (le son ralentit jusqu’à l’arrêt). | synthèse |
| [`Filter Sweep Transition`](DESIGNED/DSGNWhsh_Filter%20Sweep%20Transition_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 2.00 s | Balayage de filtre montant puis descendant (2 s). | synthèse |
| [`Riser To Hit`](DESIGNED/DSGNWhsh_Riser%20To%20Hit_MotionSynth_MotionLib.wav) | `DSGNWhsh` DESIGN › WHOOSH | 4.09 s | Montée (1,5 s) qui débouche sur un impact : changement de scène fort. | synthèse |
| [`Zhwoop Drop`](DESIGNED/DSGNBass_Zhwoop%20Drop_SurajET_SurajSFX14.wav) | `DSGNBass` DESIGN › BASS DIVE | 2.09 s | « Zhwoop » : montée grave puis impact et pulsations (2,1 s). | SurajET — Sound Effect Part 14 @ 0.04 s |
| [`Slow Motion Effect`](DESIGNED/DSGNMorph_Slow%20Motion%20Effect_SurajET_SurajSFX08.wav) | `DSGNMorph` DESIGN › TRANSFORMATION | 6.03 s | Effet ralenti : pulsations qui ralentissent puis ré-accélèrent en montant (6 s). | SurajET — Sound Effect Part 8 @ 6.45 s |
| [`Cinematic Riser Hit A`](DESIGNED/DSGNStngr_Cinematic%20Riser%20Hit%20A_SurajET_SurajSFX11.wav) | `DSGNStngr` DESIGN › STINGER | 3.54 s | Montée d’1 s puis impact cinématique et longue queue (3,7 s). ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 11 @ 10.46 s |
| [`Cinematic Riser Hit B`](DESIGNED/DSGNStngr_Cinematic%20Riser%20Hit%20B_SurajET_SurajSFX11.wav) | `DSGNStngr` DESIGN › STINGER | 4.11 s | Montée puis gros impact de bande-annonce, longue queue (4,1 s). | SurajET — Sound Effect Part 11 @ 14.00 s |
| [`Epic Blockbuster Hit`](DESIGNED/DSGNStngr_Epic%20Blockbuster%20Hit_SurajET_SurajSFX06.wav) | `DSGNStngr` DESIGN › STINGER | 3.31 s | Montée pulsée puis gros impact orchestral (3,4 s). Transition de bande-annonce. | SurajET — Sound Effect Part 6 @ 5.41 s |
| [`Transition Whoosh`](DESIGNED/DSGNWhsh_Transition%20Whoosh_SurajET_SurajSFX14.wav) | `DSGNWhsh` DESIGN › WHOOSH | 1.43 s | Whoosh de transition (1,4 s). | SurajET — Sound Effect Part 14 @ 2.18 s |
| [`Epic Orchestra Hit`](MUSICAL/MUSCStngr_Epic%20Orchestra%20Hit_SurajET_SurajSFX06.wav) | `MUSCStngr` MUSICAL › STINGER | 3.37 s | Coup orchestral tenu, épique (3,4 s). | SurajET — Sound Effect Part 6 @ 8.75 s |
| [`Warp Swirl`](SCIFI/SCIEnrg_Warp%20Swirl_SurajET_SurajSFX07.wav) | `SCIEnrg` SCIFI › ÉNERGIE | 2.53 s | Tourbillon / distorsion spatiale sci-fi (2,5 s). ⚠️ Coupé par la fin de la vidéo source (fondu 300 ms). | SurajET — Sound Effect Part 7 @ 6.10 s |
| [`Glitch Transition Long`](USER%20INTERFACE/UIGlitch_Glitch%20Transition%20Long_PieroCesti_PieroCestiSFX.wav) | `UIGlitch` INTERFACE › GLITCH | 1.84 s | Transition glitch (1,8 s). | PieroCesti — Comment "SFX" @ 5.09 s |

### Drone / nappe

Fond sonore tenu (bouclable) : tension, mystère, technologie.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Drone Dark Loop`](DESIGNED/DSGNDron_Drone%20Dark%20Loop_MotionSynth_MotionLib.wav) | `DSGNDron` DESIGN › DRONE | 10.00 s | Nappe sombre et grave, bouclable (10 s). 🔁 bouclable | synthèse |
| [`Drone Ethereal Loop`](DESIGNED/DSGNDron_Drone%20Ethereal%20Loop_MotionSynth_MotionLib.wav) | `DSGNDron` DESIGN › DRONE | 10.00 s | Nappe éthérée et lumineuse, bouclable (10 s). 🔁 bouclable | synthèse |
| [`Drone Tech Hum Loop`](DESIGNED/DSGNDron_Drone%20Tech%20Hum%20Loop_MotionSynth_MotionLib.wav) | `DSGNDron` DESIGN › DRONE | 10.00 s | Bourdonnement technologique, bouclable (10 s). 🔁 bouclable | synthèse |
| [`Drone Tense Loop`](DESIGNED/DSGNDron_Drone%20Tense%20Loop_MotionSynth_MotionLib.wav) | `DSGNDron` DESIGN › DRONE | 10.00 s | Nappe tendue (battements dissonants), bouclable (10 s). 🔁 bouclable | synthèse |

### Ambiance

Fond d’ambiance bouclable : pièce, vent, salle high-tech, sci-fi.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Room Tone Loop`](AMBIENCE/AMBRoom_Room%20Tone%20Loop_MotionSynth_MotionLib.wav) | `AMBRoom` AMBIANCE › FOND D’AIR | 10.00 s | Ambiance de pièce calme (fond neutre), bouclable (10 s). 🔁 bouclable | synthèse |
| [`SciFi Ambience Loop`](AMBIENCE/AMBSci_SciFi%20Ambience%20Loop_MotionSynth_MotionLib.wav) | `AMBSci` AMBIANCE › SCIFI | 10.00 s | Ambiance science-fiction : drone + gazouillis électroniques, bouclable (10 s). 🔁 bouclable | synthèse |
| [`HiTech Room Loop`](AMBIENCE/AMBTech_HiTech%20Room%20Loop_MotionSynth_MotionLib.wav) | `AMBTech` AMBIANCE › HIGH TECH | 10.00 s | Salle high-tech : ventilation, bourdonnement, petits bips, bouclable (10 s). 🔁 bouclable | synthèse |
| [`Wind Designed Loop`](WIND/WINDDsgn_Wind%20Designed%20Loop_MotionSynth_MotionLib.wav) | `WINDDsgn` VENT › DESIGN | 10.00 s | Vent synthétique avec rafales, bouclable (10 s). 🔁 bouclable | synthèse |

### UI clic / tap

Boutons, curseur, toggles, sélections.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Click Double`](USER%20INTERFACE/UIClick_Click%20Double_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.12 s | Double clic de souris. | synthèse |
| [`Click Hard`](USER%20INTERFACE/UIClick_Click%20Hard_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.04 s | Clic sec et net. | synthèse |
| [`Click Soft Tap`](USER%20INTERFACE/UIClick_Click%20Soft%20Tap_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.09 s | Tapotement doux (bouton, sélection discrète). | synthèse |
| [`Glass Tick`](USER%20INTERFACE/UIClick_Glass%20Tick_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.12 s | Tic cristallin. | synthèse |
| [`Hover Soft`](USER%20INTERFACE/UIClick_Hover%20Soft_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.06 s | Survol très léger (hover). | synthèse |
| [`Keypress`](USER%20INTERFACE/UIClick_Keypress_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.05 s | Touche de clavier synthétique (« thock »). | synthèse |
| [`Scroll Tick`](USER%20INTERFACE/UIClick_Scroll%20Tick_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.03 s | Petit tic de défilement (molette, liste). | synthèse |
| [`Select Confirm`](USER%20INTERFACE/UIClick_Select%20Confirm_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.07 s | Sélection confirmée (clic + note brève). | synthèse |
| [`Toggle Off`](USER%20INTERFACE/UIClick_Toggle%20Off_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.10 s | Interrupteur OFF (clic + petite note descendante). | synthèse |
| [`Toggle On`](USER%20INTERFACE/UIClick_Toggle%20On_MotionSynth_MotionLib.wav) | `UIClick` INTERFACE › CLIC | 0.10 s | Interrupteur ON (clic + petite note montante). | synthèse |
| [`Switch Toggle`](MECHANICAL/MECHSwtch_Switch%20Toggle_PieroCesti_PieroCestiSFX.wav) | `MECHSwtch` MÉCANISMES › INTERRUPTEUR | 0.76 s | Interrupteur / toggle. | PieroCesti — Comment "SFX" @ 0.57 s |
| [`Button Swell Click`](USER%20INTERFACE/UIClick_Button%20Swell%20Click_SurajET_SurajSFX09.wav) | `UIClick` INTERFACE › CLIC | 0.88 s | Bouton : déclic qui gonfle. | SurajET — Sound Effect Part 9 @ 0.82 s |
| [`Button Tonal Long`](USER%20INTERFACE/UIClick_Button%20Tonal%20Long_SurajET_SurajSFX04.wav) | `UIClick` INTERFACE › CLIC | 1.79 s | Bouton à note tenue, harmonique et doux (≈1,8 s). Validation, menu qui s’ouvre. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 4 @ 1.89 s |
| [`Button Two Tone Ding`](USER%20INTERFACE/UIClick_Button%20Two%20Tone%20Ding_SurajET_SurajSFX09.wav) | `UIClick` INTERFACE › CLIC | 0.81 s | Bouton : ding doux à deux notes (1 et 2 kHz). | SurajET — Sound Effect Part 9 @ 0.01 s |
| [`Click Double Dry`](USER%20INTERFACE/UIClick_Click%20Double%20Dry_SurajET_SurajSFX.wav) | `UIClick` INTERFACE › CLIC | 0.21 s | Double clic sec. | SurajET — Sound Effects @ 0.51 s |
| [`Click With Tone`](USER%20INTERFACE/UIClick_Click%20With%20Tone_SurajET_SurajSFX04.wav) | `UIClick` INTERFACE › CLIC | 0.64 s | Clic suivi d’une note tenue (≈600 Hz). | SurajET — Sound Effect Part 4 @ 8.12 s |
| [`Tap Double Light`](USER%20INTERFACE/UIClick_Tap%20Double%20Light_SurajET_SurajSFX04.wav) | `UIClick` INTERFACE › CLIC | 0.24 s | Double tapotement léger. | SurajET — Sound Effect Part 4 @ 9.02 s |
| [`Tick Short Tonal`](USER%20INTERFACE/UIClick_Tick%20Short%20Tonal_SurajET_SurajSFX04.wav) | `UIClick` INTERFACE › CLIC | 0.14 s | Tic très court et sec avec une petite note (≈800 Hz). Apparition d’un élément minuscule, curseur. | SurajET — Sound Effect Part 4 @ 0.21 s |
| [`Low Tone Plucks`](USER%20INTERFACE/UIMisc_Low%20Tone%20Plucks_SurajET_SurajSFXWhoosh.wav) | `UIMisc` INTERFACE › DIVERS | 0.86 s | Ton grave avec pincements. Élément qui se pose. | SurajET — Sound Effects (whoosh) @ 11.06 s |
| [`Open UI Panel`](USER%20INTERFACE/UIMvmt_Open%20UI%20Panel_PieroCesti_PieroCestiSFX.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.58 s | Ouverture d’interface / panneau. | PieroCesti — Comment "SFX" @ 8.82 s |

### Pop / bulle

Apparition/disparition d’éléments, bulles, puces.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Bubble Cluster`](CARTOON/TOONPop_Bubble%20Cluster_MotionSynth_MotionLib.wav) | `TOONPop` CARTOON › POP | 0.94 s | Grappe de bulles (apparition de plusieurs éléments). | synthèse |
| [`Bubble Pop`](CARTOON/TOONPop_Bubble%20Pop_MotionSynth_MotionLib.wav) | `TOONPop` CARTOON › POP | 0.07 s | Pop de bulle classique. | synthèse |
| [`Mouth Pop`](CARTOON/TOONPop_Mouth%20Pop_MotionSynth_MotionLib.wav) | `TOONPop` CARTOON › POP | 0.06 s | Pop de bouche (feutré). | synthèse |
| [`Plop`](CARTOON/TOONPop_Plop_MotionSynth_MotionLib.wav) | `TOONPop` CARTOON › POP | 0.15 s | Plop descendant (goutte, élément qui tombe). | synthèse |
| [`Pop High`](CARTOON/TOONPop_Pop%20High_MotionSynth_MotionLib.wav) | `TOONPop` CARTOON › POP | 0.06 s | Pop aigu et vif. | synthèse |
| [`Pop Low`](CARTOON/TOONPop_Pop%20Low_MotionSynth_MotionLib.wav) | `TOONPop` CARTOON › POP | 0.09 s | Pop grave et rond. | synthèse |
| [`Pop Appear`](USER%20INTERFACE/UIMvmt_Pop%20Appear_MotionSynth_MotionLib.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.64 s | Apparition d’élément (pop montant avec petite réverb). | synthèse |
| [`Pop Disappear`](USER%20INTERFACE/UIMvmt_Pop%20Disappear_MotionSynth_MotionLib.wav) | `UIMvmt` INTERFACE › MOUVEMENT | 0.65 s | Disparition d’élément (pop descendant). | synthèse |
| [`Bubble Pops Triple`](CARTOON/TOONPop_Bubble%20Pops%20Triple_SurajET_SurajSFXWhoosh.wav) | `TOONPop` CARTOON › POP | 0.28 s | Trois petits pops rapides (bulles). Apparition de liste/puces. | SurajET — Sound Effects (whoosh) @ 12.08 s |
| [`Pop Pluck High`](CARTOON/TOONPop_Pop%20Pluck%20High_SurajET_SurajSFX04.wav) | `TOONPop` CARTOON › POP | 0.27 s | Pop pincé court et aigu (≈1,6 kHz). | SurajET — Sound Effect Part 4 @ 8.76 s |
| [`Pop Rise Resonant`](CARTOON/TOONPop_Pop%20Rise%20Resonant_Unknown_TenSFXEditors.wav) | `TOONPop` CARTOON › POP | 0.72 s | Pop montant avec résonance. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 3.86 s |
| [`Pop Tonal Harmonic`](CARTOON/TOONPop_Pop%20Tonal%20Harmonic_SurajET_SurajSFX04.wav) | `TOONPop` CARTOON › POP | 0.47 s | Pop tonal avec harmoniques, attaque grave, extinction rapide. | SurajET — Sound Effect Part 4 @ 6.99 s |

### UI bip / données

Bips, chargement, données, interfaces high-tech, texte qui s’écrit.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Beep Confirm`](USER%20INTERFACE/UIBeep_Beep%20Confirm_MotionSynth_MotionLib.wav) | `UIBeep` INTERFACE › BIP | 0.09 s | Bip de confirmation doux. | synthèse |
| [`Beep Double`](USER%20INTERFACE/UIBeep_Beep%20Double_MotionSynth_MotionLib.wav) | `UIBeep` INTERFACE › BIP | 0.18 s | Double bip. | synthèse |
| [`HUD Beep`](USER%20INTERFACE/UIBeep_HUD%20Beep_MotionSynth_MotionLib.wav) | `UIBeep` INTERFACE › BIP | 0.49 s | Bip d’interface HUD/hologramme (FM). | synthèse |
| [`Computing Process`](USER%20INTERFACE/UIData_Computing%20Process_MotionSynth_MotionLib.wav) | `UIData` INTERFACE › DONNÉES | 2.02 s | Ordinateur qui calcule : séquence de bips FM (2 s). | synthèse |
| [`Data Chatter`](USER%20INTERFACE/UIData_Data%20Chatter_MotionSynth_MotionLib.wav) | `UIData` INTERFACE › DONNÉES | 1.20 s | Traitement de données : bips aléatoires rapides (1,2 s). | synthèse |
| [`Loading Loop`](USER%20INTERFACE/UIData_Loading%20Loop_MotionSynth_MotionLib.wav) | `UIData` INTERFACE › DONNÉES | 2.00 s | Chargement : motif de 3 notes en boucle (2 s). 🔁 bouclable | synthèse |
| [`Scan Sweep`](USER%20INTERFACE/UIData_Scan%20Sweep_MotionSynth_MotionLib.wav) | `UIData` INTERFACE › DONNÉES | 1.82 s | Balayage de scan (montée-descente avec trémolo), 1,2 s. | synthèse |
| [`Text Typing Screen`](USER%20INTERFACE/UIData_Text%20Typing%20Screen_MotionSynth_MotionLib.wav) | `UIData` INTERFACE › DONNÉES | 1.47 s | Texte qui s’écrit à l’écran : tics rapides (1,5 s). | synthèse |
| [`HiTech GUI A`](SCIFI/SCICmpt_HiTech%20GUI%20A_SurajET_SurajSFX10.wav) | `SCICmpt` SCIFI › ORDINATEUR | 0.67 s | Interface high-tech / sci-fi n°1. | SurajET — Sound Effect Part 10 @ 1.08 s |
| [`HiTech GUI B`](SCIFI/SCICmpt_HiTech%20GUI%20B_SurajET_SurajSFX10.wav) | `SCICmpt` SCIFI › ORDINATEUR | 0.75 s | Interface high-tech / sci-fi n°3. | SurajET — Sound Effect Part 10 @ 2.77 s |
| [`HiTech GUI Interact`](SCIFI/SCICmpt_HiTech%20GUI%20Interact_SurajET_SurajSFX10.wav) | `SCICmpt` SCIFI › ORDINATEUR | 0.96 s | Interface high-tech / sci-fi n°2 (interaction). | SurajET — Sound Effect Part 10 @ 1.82 s |
| [`Data Loading Beeps`](USER%20INTERFACE/UIData_Data%20Loading%20Beeps_PieroCesti_PieroCestiSFX.wav) | `UIData` INTERFACE › DONNÉES | 1.45 s | Chargement de données : bips réguliers (1,5 s). | PieroCesti — Comment "SFX" @ 2.19 s |
| [`Digital Data Down`](USER%20INTERFACE/UIData_Digital%20Data%20Down_SurajET_SurajSFX09.wav) | `UIData` INTERFACE › DONNÉES | 0.95 s | Bips numériques descendants. | SurajET — Sound Effect Part 9 @ 7.30 s |
| [`Digital Data Up`](USER%20INTERFACE/UIData_Digital%20Data%20Up_SurajET_SurajSFX09.wav) | `UIData` INTERFACE › DONNÉES | 0.93 s | Bips numériques montants (données, compteur qui monte). | SurajET — Sound Effect Part 9 @ 6.25 s |
| [`Micro Ticks`](USER%20INTERFACE/UIData_Micro%20Ticks_SurajET_SurajSFX10.wav) | `UIData` INTERFACE › DONNÉES | 0.65 s | Micro-tics rapides. | SurajET — Sound Effect Part 10 @ 3.52 s |

### Notification / alerte

Succès, erreur, notification, récompense, argent.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Error Buzz`](USER%20INTERFACE/UIAlert_Error%20Buzz_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 0.39 s | Erreur : deux notes graves descendantes (refus, mauvaise réponse). | synthèse |
| [`Level Up`](USER%20INTERFACE/UIAlert_Level%20Up_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.47 s | Niveau supérieur : arpège rapide montant + scintillement. | synthèse |
| [`Like Heart`](USER%20INTERFACE/UIAlert_Like%20Heart_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.34 s | Like / cœur : petite note qui glisse vers le haut + cloche douce. | synthèse |
| [`Message Received`](USER%20INTERFACE/UIAlert_Message%20Received_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 0.96 s | Message reçu : deux notes pincées montantes. | synthèse |
| [`Notification Ding`](USER%20INTERFACE/UIAlert_Notification%20Ding_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 2.08 s | Ding de notification clair. | synthèse |
| [`Reward Coin`](USER%20INTERFACE/UIAlert_Reward%20Coin_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 0.37 s | Récompense / pièce : deux notes vives. | synthèse |
| [`Success Arpeggio`](USER%20INTERFACE/UIAlert_Success%20Arpeggio_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 2.15 s | Succès : arpège majeur cristallin (validation, objectif atteint). | synthèse |
| [`Warning Triple`](USER%20INTERFACE/UIAlert_Warning%20Triple_MotionSynth_MotionLib.wav) | `UIAlert` INTERFACE › NOTIFICATION | 0.46 s | Avertissement : trois bips médium. | synthèse |
| [`Cash Register Bell`](GAMES/GAMECas_Cash%20Register%20Bell_SurajET_SurajSFX04.wav) | `GAMECas` JEUX › CASINO | 0.71 s | Caisse enregistreuse : mécanique + petite sonnette. | SurajET — Sound Effect Part 4 @ 4.50 s |
| [`Cash Register Drawer`](GAMES/GAMECas_Cash%20Register%20Drawer_SurajET_SurajSFX04.wav) | `GAMECas` JEUX › CASINO | 1.78 s | Caisse enregistreuse longue avec tiroir (choc à 1 s) et sonnerie. Prix, argent, vente. | SurajET — Sound Effect Part 4 @ 5.21 s |
| [`Cash Register Short`](GAMES/GAMECas_Cash%20Register%20Short_SurajET_SurajSFX09.wav) | `GAMECas` JEUX › CASINO | 0.81 s | Caisse enregistreuse courte. | SurajET — Sound Effect Part 9 @ 1.70 s |
| [`Cashier Ka Ching`](GAMES/GAMECas_Cashier%20Ka%20Ching_SurajET_SurajSFX06.wav) | `GAMECas` JEUX › CASINO | 1.66 s | « Ka-ching » de caisse : mécanique puis cloche tenue. | SurajET — Sound Effect Part 6 @ 2.05 s |
| [`Bell Ding Clear`](USER%20INTERFACE/UIAlert_Bell%20Ding%20Clear_SurajET_SurajSFXWhoosh.wav) | `UIAlert` INTERFACE › NOTIFICATION | 0.82 s | Cloche/ding clair avec harmoniques. | SurajET — Sound Effects (whoosh) @ 12.76 s |
| [`Chime Stair Up`](USER%20INTERFACE/UIAlert_Chime%20Stair%20Up_SurajET_SurajSFX06.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.26 s | Carillon ascendant en escalier (1,3→2,6 kHz). Le « ding » réutilisé partout dans ces vidéos. | SurajET — Sound Effect Part 6 @ 14.95 s |
| [`Clicks And Tones`](USER%20INTERFACE/UIAlert_Clicks%20And%20Tones_Unknown_TenSFXEditors.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.03 s | Deux clics + tonalités (type notification). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 12.22 s |
| [`Ding And Bloop`](USER%20INTERFACE/UIAlert_Ding%20And%20Bloop_Unknown_TenSFXEditors.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.33 s | Ding aigu tenu + bloop. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 4.79 s |
| [`Ding Short Harmonic`](USER%20INTERFACE/UIAlert_Ding%20Short%20Harmonic_SurajET_SurajSFX04.wav) | `UIAlert` INTERFACE › NOTIFICATION | 0.50 s | Petit « ding » harmonique court. | SurajET — Sound Effect Part 4 @ 7.46 s |
| [`Ding Triad`](USER%20INTERFACE/UIAlert_Ding%20Triad_SurajET_SurajSFX12.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.10 s | Ding à trois notes tenues. ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 12 @ 4.63 s |
| [`Ping Bright Crystal`](USER%20INTERFACE/UIAlert_Ping%20Bright%20Crystal_SurajET_SurajSFX06.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.21 s | Ping aigu cristallin (≈2,6 kHz) qui s’éteint lentement. | SurajET — Sound Effect Part 6 @ 0.02 s |
| [`Success UI`](USER%20INTERFACE/UIAlert_Success%20UI_PieroCesti_PieroCestiSFX.wav) | `UIAlert` INTERFACE › NOTIFICATION | 1.05 s | Son de succès d’interface (validation). | PieroCesti — Comment "SFX" @ 9.82 s |

### Glitch / numérique

Glitchs, statique, corruption : style tech, erreurs.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Buzz Glitch`](DESIGNED/DSGNDist_Buzz%20Glitch_MotionSynth_MotionLib.wav) | `DSGNDist` DESIGN › DISTORSION | 0.50 s | Bourdonnement électrique haché (0,5 s). | synthèse |
| [`Rhythmic Glitch Loop`](DESIGNED/DSGNRythm_Rhythmic%20Glitch%20Loop_MotionSynth_MotionLib.wav) | `DSGNRythm` DESIGN › RYTHMIQUE | 2.00 s | Boucle de glitchs rythmés (120 BPM, 2 s). 🔁 bouclable | synthèse |
| [`Data Corruption`](USER%20INTERFACE/UIGlitch_Data%20Corruption_MotionSynth_MotionLib.wav) | `UIGlitch` INTERFACE › GLITCH | 0.80 s | Corruption de données : échantillonnage aléatoire changeant (0,8 s). | synthèse |
| [`Digital Burst`](USER%20INTERFACE/UIGlitch_Digital%20Burst_MotionSynth_MotionLib.wav) | `UIGlitch` INTERFACE › GLITCH | 0.30 s | Rafale numérique courte (0,3 s). | synthèse |
| [`Glitch Hit`](USER%20INTERFACE/UIGlitch_Glitch%20Hit_MotionSynth_MotionLib.wav) | `UIGlitch` INTERFACE › GLITCH | 0.41 s | Impact glitché (0,3 s). | synthèse |
| [`Glitch Stutter`](USER%20INTERFACE/UIGlitch_Glitch%20Stutter_MotionSynth_MotionLib.wav) | `UIGlitch` INTERFACE › GLITCH | 0.56 s | Glitch haché (bégaiement numérique), 0,6 s. | synthèse |
| [`Screen Static`](USER%20INTERFACE/UIGlitch_Screen%20Static_MotionSynth_MotionLib.wav) | `UIGlitch` INTERFACE › GLITCH | 0.80 s | Statique d’écran avec coupures (0,8 s). | synthèse |
| [`VHS Wobble Glitch`](USER%20INTERFACE/UIGlitch_VHS%20Wobble%20Glitch_MotionSynth_MotionLib.wav) | `UIGlitch` INTERFACE › GLITCH | 1.00 s | Glitch VHS : note qui tangue + bruit + décrochages (1 s). | synthèse |
| [`Static Burst`](COMMUNICATIONS/COMStatic_Static%20Burst_SurajET_SurajSFX07.wav) | `COMStatic` COMMUNICATIONS › PARASITES | 0.51 s | Bouffée de statique. | SurajET — Sound Effect Part 7 @ 1.20 s |
| [`Static Texture Tonal`](COMMUNICATIONS/COMStatic_Static%20Texture%20Tonal_SurajET_SurajSFX08.wav) | `COMStatic` COMMUNICATIONS › PARASITES | 1.72 s | Texture de bruit/statique avec tonalités (1,7 s). | SurajET — Sound Effect Part 8 @ 4.21 s |
| [`SciFi Tones Descend`](SCIFI/SCIRetro_SciFi%20Tones%20Descend_SurajET_SurajSFX06.wav) | `SCIRetro` SCIFI › RÉTRO | 0.56 s | Tonalités électroniques descendantes, glitch sci-fi. | SurajET — Sound Effect Part 6 @ 12.97 s |
| [`Glitch Burst Clicks`](USER%20INTERFACE/UIGlitch_Glitch%20Burst%20Clicks_SurajET_SurajSFX08.wav) | `UIGlitch` INTERFACE › GLITCH | 0.48 s | Rafale glitch/clics courte. | SurajET — Sound Effect Part 8 @ 3.08 s |
| [`Glitch Clicks Fast`](USER%20INTERFACE/UIGlitch_Glitch%20Clicks%20Fast_Unknown_TenSFXEditors.wav) | `UIGlitch` INTERFACE › GLITCH | 0.54 s | Clics glitchés rapides. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 10.76 s |
| [`Glitch Crackle`](USER%20INTERFACE/UIGlitch_Glitch%20Crackle_SurajET_SurajSFX.wav) | `UIGlitch` INTERFACE › GLITCH | 0.92 s | Crépitement avec petits chocs. | SurajET — Sound Effects @ 0.83 s |
| [`Glitch Noise Burst`](USER%20INTERFACE/UIGlitch_Glitch%20Noise%20Burst_SurajET_SurajSFX12.wav) | `UIGlitch` INTERFACE › GLITCH | 0.98 s | Bouffée de bruit glitchée avec tonalités. | SurajET — Sound Effect Part 12 @ 0.09 s |
| [`Glitch Thump`](USER%20INTERFACE/UIGlitch_Glitch%20Thump_SurajET_SurajSFX.wav) | `UIGlitch` INTERFACE › GLITCH | 0.61 s | Glitch avec coup sourd grave. | SurajET — Sound Effects @ 1.84 s |
| [`Glitch Tonal Residue`](USER%20INTERFACE/UIGlitch_Glitch%20Tonal%20Residue_SurajET_SurajSFX10.wav) | `UIGlitch` INTERFACE › GLITCH | 0.80 s | Glitch avec tonalités résiduelles. | SurajET — Sound Effect Part 10 @ 5.50 s |
| [`Negative Glitch A`](USER%20INTERFACE/UIGlitch_Negative%20Glitch%20A_PieroCesti_PieroCestiSFX.wav) | `UIGlitch` INTERFACE › GLITCH | 0.87 s | Glitch « négatif » (erreur) n°1. | PieroCesti — Comment "SFX" @ 10.86 s |
| [`Negative Glitch B`](USER%20INTERFACE/UIGlitch_Negative%20Glitch%20B_PieroCesti_PieroCestiSFX.wav) | `UIGlitch` INTERFACE › GLITCH | 0.76 s | Glitch « négatif » (erreur) n°2. | PieroCesti — Comment "SFX" @ 11.76 s |
| [`Negative Glitch C`](USER%20INTERFACE/UIGlitch_Negative%20Glitch%20C_PieroCesti_PieroCestiSFX.wav) | `UIGlitch` INTERFACE › GLITCH | 1.14 s | Glitch « négatif » (erreur) n°3. | PieroCesti — Comment "SFX" @ 12.54 s |
| [`Tonal Chopped Glitch`](USER%20INTERFACE/UIGlitch_Tonal%20Chopped%20Glitch_SurajET_SurajSFX10.wav) | `UIGlitch` INTERFACE › GLITCH | 0.43 s | Glitch tonal haché. | SurajET — Sound Effect Part 10 @ 0.02 s |

### Électrique / laser / énergie

Zaps, étincelles, lasers, charges d’énergie, téléportation.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Spark Crackle`](ELECTRICITY/ELECSprk_Spark%20Crackle_MotionSynth_MotionLib.wav) | `ELECSprk` ÉLECTRICITÉ › ÉTINCELLES | 1.20 s | Crépitement d’étincelles (1,2 s). | synthèse |
| [`Electric Zap`](ELECTRICITY/ELECZap_Electric%20Zap_MotionSynth_MotionLib.wav) | `ELECZap` ÉLECTRICITÉ › ZAP | 0.25 s | Décharge électrique « zap » (0,25 s). | synthèse |
| [`Laser Double`](LASERS/LASRGun_Laser%20Double_MotionSynth_MotionLib.wav) | `LASRGun` LASERS › ARME | 0.70 s | Double tir laser. | synthèse |
| [`Laser Pew`](LASERS/LASRGun_Laser%20Pew_MotionSynth_MotionLib.wav) | `LASRGun` LASERS › ARME | 0.69 s | Tir laser « pew » (0,2 s). | synthèse |
| [`Energy Charge`](SCIFI/SCIEnrg_Energy%20Charge_MotionSynth_MotionLib.wav) | `SCIEnrg` SCIFI › ÉNERGIE | 1.50 s | Charge d’énergie : sifflement qui monte (1,5 s). | synthèse |
| [`Force Field Hum Loop`](SCIFI/SCIEnrg_Force%20Field%20Hum%20Loop_MotionSynth_MotionLib.wav) | `SCIEnrg` SCIFI › ÉNERGIE | 3.00 s | Champ de force : bourdonnement modulé, bouclable (3 s). 🔁 bouclable | synthèse |
| [`Teleport`](SCIFI/SCIEnrg_Teleport_MotionSynth_MotionLib.wav) | `SCIEnrg` SCIFI › ÉNERGIE | 2.05 s | Téléportation : balayage scintillant montant-descendant (1,2 s). | synthèse |
| [`Double Zap`](ELECTRICITY/ELECZap_Double%20Zap_PieroCesti_PieroCestiSFX.wav) | `ELECZap` ÉLECTRICITÉ › ZAP | 0.45 s | Deux décharges électriques « zap ». | PieroCesti — Comment "SFX" @ 1.57 s |
| [`Laser Zap Sweep`](LASERS/LASRGun_Laser%20Zap%20Sweep_SurajET_SurajSFX12.wav) | `LASRGun` LASERS › ARME | 0.98 s | Laser / tir sci-fi avec balayages croisés. | SurajET — Sound Effect Part 12 @ 9.24 s |

### Magie / scintillement

Paillettes, poufs magiques, glissandos féeriques.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Angelic Swell`](MAGIC/MAGAngl_Angelic%20Swell_MotionSynth_MotionLib.wav) | `MAGAngl` MAGIE › BLANCHE | 5.05 s | Nappe angélique qui gonfle (2,5 s). | synthèse |
| [`Wand Swish`](MAGIC/MAGMisc_Wand%20Swish_MotionSynth_MotionLib.wav) | `MAGMisc` MAGIE › DIVERS | 2.14 s | Coup de baguette magique : swish + scintillement. | synthèse |
| [`Magic Poof`](MAGIC/MAGPoof_Magic%20Poof_MotionSynth_MotionLib.wav) | `MAGPoof` MAGIE › POUF | 2.21 s | Pouf magique : bouffée + scintillement (apparition/disparition). | synthèse |
| [`Fairy Glissando`](MAGIC/MAGShim_Fairy%20Glissando_MotionSynth_MotionLib.wav) | `MAGShim` MAGIE › SCINTILLEMENT | 2.63 s | Glissando féerique montant (0,7 s). | synthèse |
| [`Magic Sparkle`](MAGIC/MAGShim_Magic%20Sparkle_MotionSynth_MotionLib.wav) | `MAGShim` MAGIE › SCINTILLEMENT | 3.41 s | Scintillement magique (1,5 s) : paillettes, étoiles. | synthèse |
| [`Twinkle`](MAGIC/MAGShim_Twinkle_MotionSynth_MotionLib.wav) | `MAGShim` MAGIE › SCINTILLEMENT | 2.53 s | Trois notes scintillantes isolées. | synthèse |
| [`Magic Sparkle Long`](MAGIC/MAGShim_Magic%20Sparkle%20Long_SurajET_SurajSFX12.wav) | `MAGShim` MAGIE › SCINTILLEMENT | 1.86 s | Scintillement magique (1,9 s). Paillettes, apparition magique. | SurajET — Sound Effect Part 12 @ 7.38 s |

### Cartoon / fun

Boings, sifflets, couinements, bonks : ton léger.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Boing Spring`](CARTOON/TOONBoing_Boing%20Spring_MotionSynth_MotionLib.wav) | `TOONBoing` CARTOON › BOING | 0.70 s | Boing de ressort (rebond cartoon). | synthèse |
| [`Bonk`](CARTOON/TOONImpt_Bonk_MotionSynth_MotionLib.wav) | `TOONImpt` CARTOON › IMPACT | 0.25 s | Bonk cartoon (coup sur la tête, objet qui tape). | synthèse |
| [`Pluck Cartoon`](CARTOON/TOONPluk_Pluck%20Cartoon_MotionSynth_MotionLib.wav) | `TOONPluk` CARTOON › PLUCK | 0.60 s | Corde pincée cartoon (petit pas furtif). | synthèse |
| [`Squeak`](CARTOON/TOONSqk_Squeak_MotionSynth_MotionLib.wav) | `TOONSqk` CARTOON › SQUEAK | 0.21 s | Couinement (jouet, petit personnage). | synthèse |
| [`Twang Ruler`](CARTOON/TOONTwang_Twang%20Ruler_MotionSynth_MotionLib.wav) | `TOONTwang` CARTOON › TWANG | 1.20 s | Twang de règle qui vibre. | synthèse |
| [`Slide Whistle Down`](CARTOON/TOONWhis_Slide%20Whistle%20Down_MotionSynth_MotionLib.wav) | `TOONWhis` CARTOON › SIFFLET | 0.80 s | Sifflet à coulisse descendant (chute). | synthèse |
| [`Slide Whistle Up`](CARTOON/TOONWhis_Slide%20Whistle%20Up_MotionSynth_MotionLib.wav) | `TOONWhis` CARTOON › SIFFLET | 0.70 s | Sifflet à coulisse montant. | synthèse |
| [`Boing Low Tonal`](CARTOON/TOONBoing_Boing%20Low%20Tonal_SurajET_SurajSFX12.wav) | `TOONBoing` CARTOON › BOING | 0.84 s | « Boing » grave tonal avec clic. | SurajET — Sound Effect Part 12 @ 3.79 s |
| [`Bounce Glissandos`](CARTOON/TOONBoing_Bounce%20Glissandos_SurajET_SurajSFX04.wav) | `TOONBoing` CARTOON › BOING | 0.90 s | Rebond cartoon : glissandos montants répétés. Objet qui rebondit, logo qui saute. | SurajET — Sound Effect Part 4 @ 0.49 s |
| [`Bloop Up`](CARTOON/TOONPop_Bloop%20Up_SurajET_SurajSFX06.wav) | `TOONPop` CARTOON › POP | 0.50 s | Bloop montant (glissando vers l’aigu). Apparition, bulle. | SurajET — Sound Effect Part 6 @ 16.21 s |
| [`Note Slide Up`](CARTOON/TOONWhis_Note%20Slide%20Up_Unknown_TenSFXEditors.wav) | `TOONWhis` CARTOON › SIFFLET | 0.95 s | Note qui glisse vers le haut. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 9.00 s |

### Tonal / musical

Accents musicaux : accords, cloches, marimba, petites phrases.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Tonal Sub Hit`](DESIGNED/DSGNTonl_Tonal%20Sub%20Hit_MotionSynth_MotionLib.wav) | `DSGNTonl` DESIGN › TONAL | 4.10 s | Impact tonal : basse + harmoniques de cloche qui résonnent. | synthèse |
| [`Bell Hit`](MUSICAL/MUSCBell_Bell%20Hit_MotionSynth_MotionLib.wav) | `MUSCBell` MUSICAL › CLOCHES | 4.43 s | Coup de cloche tonale (3 s). | synthèse |
| [`Wind Chimes`](MUSICAL/MUSCChim_Wind%20Chimes_MotionSynth_MotionLib.wav) | `MUSCChim` MUSICAL › CHIME | 4.20 s | Carillon à vent (2,5 s). | synthèse |
| [`Musical Sting Up`](MUSICAL/MUSCStngr_Musical%20Sting%20Up_MotionSynth_MotionLib.wav) | `MUSCStngr` MUSICAL › STINGER | 1.84 s | Petite phrase musicale montante (3 notes), ponctuation positive. | synthèse |
| [`Synth Stab Chord`](MUSICAL/MUSCSynth_Synth%20Stab%20Chord_MotionSynth_MotionLib.wav) | `MUSCSynth` MUSICAL › SYNTHÉTISÉ | 1.74 s | Accord synthé court (stab), accent musical. | synthèse |
| [`Marimba Note`](MUSICAL/MUSCTnprc_Marimba%20Note_MotionSynth_MotionLib.wav) | `MUSCTnprc` MUSICAL › PERCUSSION MÉLODIQUE | 1.41 s | Note de marimba (mallet doux). | synthèse |

### Horloge / compteur

Tic-tac, comptes à rebours, compteurs de score.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Countdown 3 2 1`](BEEPS/BEEPTimer_Countdown%203%202%201_MotionSynth_MotionLib.wav) | `BEEPTimer` BIPS › MINUTERIE | 3.60 s | Compte à rebours : 3 bips + bip long (départ). | synthèse |
| [`Timer Tick Fast`](BEEPS/BEEPTimer_Timer%20Tick%20Fast_MotionSynth_MotionLib.wav) | `BEEPTimer` BIPS › MINUTERIE | 1.10 s | Minuteur : tics rapides (10 tics). | synthèse |
| [`Clock Tick Loop`](CLOCKS/CLOCKTick_Clock%20Tick%20Loop_MotionSynth_MotionLib.wav) | `CLOCKTick` HORLOGES › TIC TAC | 4.00 s | Tic-tac d’horloge, bouclable (4 s). 🔁 bouclable | synthèse |
| [`Stopwatch Click`](MECHANICAL/MECHClik_Stopwatch%20Click_MotionSynth_MotionLib.wav) | `MECHClik` MÉCANISMES › CLIC | 0.08 s | Chronomètre : déclic mécanique double. | synthèse |
| [`Score Counter Rollup`](USER%20INTERFACE/UIData_Score%20Counter%20Rollup_MotionSynth_MotionLib.wav) | `UIData` INTERFACE › DONNÉES | 3.26 s | Compteur de score qui défile (accélère, monte) puis ding final. | synthèse |
| [`Clock Ticks Irregular`](CLOCKS/CLOCKTick_Clock%20Ticks%20Irregular_Unknown_TenSFXEditors.wav) | `CLOCKTick` HORLOGES › TIC TAC | 1.81 s | Tic-tac irréguliers (1,8 s). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Unknown — 10 Sound Effects Every Editor Must Use @ 6.19 s |
| [`Fast Ticking A`](CLOCKS/CLOCKTick_Fast%20Ticking%20A_SurajET_SurajSFX07.wav) | `CLOCKTick` HORLOGES › TIC TAC | 1.18 s | Tic-tac / cliquetis rapide aigu (1,1 s). | SurajET — Sound Effect Part 7 @ 0.02 s |
| [`Fast Ticking B`](CLOCKS/CLOCKTick_Fast%20Ticking%20B_SurajET_SurajSFX07.wav) | `CLOCKTick` HORLOGES › TIC TAC | 0.90 s | Cliquetis rapide aigu (0,9 s). ⚠️ Coupé par le montage source (fondu 120 ms). | SurajET — Sound Effect Part 7 @ 3.16 s |
| [`Ratchet Ticks`](MECHANICAL/MECHRtch_Ratchet%20Ticks_SurajET_SurajSFXWhoosh.wav) | `MECHRtch` MÉCANISMES › CLIQUET | 0.62 s | Cliquetis rapide (cliquet / horloge rapide). | SurajET — Sound Effects (whoosh) @ 9.23 s |

### Battement / pulsation

Battements de cœur : suspense, émotion.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Heartbeat Calm`](HUMAN/HMNHart_Heartbeat%20Calm_MotionSynth_MotionLib.wav) | `HMNHart` HUMAIN › PULSATION | 3.29 s | Battement de cœur calme (70 BPM, 4 battements). | synthèse |
| [`Heartbeat Fast`](HUMAN/HMNHart_Heartbeat%20Fast_MotionSynth_MotionLib.wav) | `HMNHart` HUMAIN › PULSATION | 3.02 s | Battement de cœur rapide (130 BPM), suspense. | synthèse |

### Power up / down

Mise sous/hors tension, servos, mécanismes robotiques.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Power Down`](SCIFI/SCIMach_Power%20Down_MotionSynth_MotionLib.wav) | `SCIMach` SCIFI › MACHINE | 1.60 s | Mise hors tension : descente qui s’éteint (1,6 s). | synthèse |
| [`Power Up`](SCIFI/SCIMach_Power%20Up_MotionSynth_MotionLib.wav) | `SCIMach` SCIFI › MACHINE | 1.54 s | Mise sous tension : montée + sifflement + déclic (1,6 s). | synthèse |
| [`Servo Motion`](SCIFI/SCIMach_Servo%20Motion_MotionSynth_MotionLib.wav) | `SCIMach` SCIFI › MACHINE | 0.60 s | Petit servo / mécanisme robotique (0,6 s). | synthèse |

### Foley / objets

Sons d’objets réels : papier, chaîne, clavier, engrenages, feutre, obturateur.

| Fichier | UCS | Durée | Description | Origine |
|---|---|---|---|---|
| [`Chain Rattle A`](CHAINS/CHAINMvmt_Chain%20Rattle%20A_SurajET_SurajSFX09.wav) | `CHAINMvmt` CHAÎNES › MOUVEMENT | 1.03 s | Chaîne métallique (1,1 s). | SurajET — Sound Effect Part 9 @ 2.58 s |
| [`Chain Rattle B`](CHAINS/CHAINMvmt_Chain%20Rattle%20B_SurajET_SurajSFX09.wav) | `CHAINMvmt` CHAÎNES › MOUVEMENT | 0.58 s | Chaîne métallique (0,7 s). | SurajET — Sound Effect Part 9 @ 3.90 s |
| [`Chain Rattle C`](CHAINS/CHAINMvmt_Chain%20Rattle%20C_SurajET_SurajSFX09.wav) | `CHAINMvmt` CHAÎNES › MOUVEMENT | 0.50 s | Chaîne métallique (0,5 s). | SurajET — Sound Effect Part 9 @ 4.70 s |
| [`Chain Rattle D`](CHAINS/CHAINMvmt_Chain%20Rattle%20D_SurajET_SurajSFX09.wav) | `CHAINMvmt` CHAÎNES › MOUVEMENT | 0.74 s | Chaîne métallique (0,8 s). | SurajET — Sound Effect Part 9 @ 5.51 s |
| [`Laptop Keyboard Typing`](COMPUTERS/CMPTKey_Laptop%20Keyboard%20Typing_PieroCesti_PieroCestiSFX.wav) | `CMPTKey` ORDINATEURS › CLAVIER & SOURIS | 2.97 s | Frappe au clavier MacBook (3 s, avec une pause). | PieroCesti — Comment "SFX" @ 13.68 s |
| [`Film Projector Clicks`](COMMUNICATIONS/COMAv_Film%20Projector%20Clicks_SurajET_SurajSFX04.wav) | `COMAv` COMMUNICATIONS › AUDIOVISUEL | 0.62 s | Mécanisme de caméra/projecteur film : trois déclics rapides. | SurajET — Sound Effect Part 4 @ 9.26 s |
| [`Film Camera Shutter`](COMMUNICATIONS/COMCam_Film%20Camera%20Shutter_SurajET_SurajSFX10.wav) | `COMCam` COMMUNICATIONS › APPAREIL PHOTO | 0.62 s | Obturateur d’appareil photo argentique. | SurajET — Sound Effect Part 10 @ 4.35 s |
| [`Click Series Fast`](MECHANICAL/MECHClik_Click%20Series%20Fast_SurajET_SurajSFX08.wav) | `MECHClik` MÉCANISMES › CLIC | 1.05 s | Série de clics/déclics rapides (≈1 s). | SurajET — Sound Effect Part 8 @ 1.81 s |
| [`Gears Turning`](MECHANICAL/MECHGear_Gears%20Turning_PieroCesti_PieroCestiSFX.wav) | `MECHGear` MÉCANISMES › ENGRENAGE | 1.70 s | Engrenages / mécanisme qui tourne. | PieroCesti — Comment "SFX" @ 6.92 s |
| [`Marker Draw Line`](OBJECTS/OBJWrite_Marker%20Draw%20Line_SurajET_SurajSFX10.wav) | `OBJWrite` OBJETS › ÉCRITURE | 1.32 s | Feutre/surligneur qui trace une ligne (1,3 s). Texte ou trait qui se dessine. | SurajET — Sound Effect Part 10 @ 6.29 s |
| [`Paper Crumple`](PAPER/PAPRHndl_Paper%20Crumple_SurajET_SurajSFX15.wav) | `PAPRHndl` PAPIER › MANIPULATION | 2.31 s | Papier froissé / bruissement (2,4 s). | SurajET — Sound Effect Part 15 @ 2.82 s |
| [`Paper Page Flip`](PAPER/PAPRHndl_Paper%20Page%20Flip_SurajET_SurajSFX15.wav) | `PAPRHndl` PAPIER › MANIPULATION | 0.69 s | Feuille de papier qu’on tourne. | SurajET — Sound Effect Part 15 @ 5.25 s |
| [`Paper Rustle Short`](PAPER/PAPRHndl_Paper%20Rustle%20Short_SurajET_SurajSFX15.wav) | `PAPRHndl` PAPIER › MANIPULATION | 0.67 s | Froissement de papier court. | SurajET — Sound Effect Part 15 @ 6.08 s |

## Origine des sons

**Sons extraits** — les vidéos montrent une timeline qui défile ; elle a été reconstruite image par image pour identifier chaque clip et son nom, puis les coupes ont été calées sur l’audio à la milliseconde (fondus anti-clic, doublons retirés par corrélation). La vidéo « 10 Sound Effects » avait une musique de fond, atténuée d’environ 15 dB (signalé ⚠️). Les sons coupés net par le montage d’origine sont aussi signalés ⚠️.

**Sons synthétisés** — générés par le moteur `_outils/synth/` (Python : bruit filtré, oscillateurs, FM, synthèse additive de cloches, Karplus-Strong, réverbération à convolution synthétique). Chaque son est contrôlé : spectrogramme, fins sans coupure, boucles sans clic au raccord. Pour en créer d’autres : ajouter une recette dans `families.py` puis relancer `render.py` et `build_ucs.py`.

**Pourquoi certaines catégories UCS sont vides** : les sons du monde réel (animaux, voix, véhicules, armes, foules, eau…) ne se synthétisent pas de façon crédible ; ils demandent de vrais enregistrements, à déposer dans le dossier UCS correspondant en suivant sa fiche.

## Droits

- **Sons synthétisés** : créés pour ce projet, utilisables librement.
- **Sons extraits** : issus de vidéos partagées gratuitement ; plusieurs portent des noms de banques connues (Mixkit, Epidemic Sound « ES_ », Adobe…). Vérifier la licence d’origine avant un usage commercial ou une redistribution.
- **UCS** : système libre créé par Tim Nielsen, Justin Drury, Kai Paquin et contributeurs — https://universalcategorysystem.com. Traduction française officielle utilisée, avec 4 corrections dans OBJECTS (FASHION/FURNITURE/GARDEN/GYM étaient intervertis).
