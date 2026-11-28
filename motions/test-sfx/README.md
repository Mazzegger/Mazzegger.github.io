# Motion de test — bibliothèque SFX

Vidéo verticale 1080×1920, 30 i/s, 13,2 s, son −13,4 LUFS : [`motion_test_sfx.mp4`](motion_test_sfx.mp4).
Elle présente la bibliothèque `sfx/` et sert de démonstration des règles de calage du son.

## Scènes
1. **Intro logo** (0–2,5 s) : particules aspirées, pop du logo, lettres S-F-X, sous-titre tapé.
2. **Transition glitch** (2,55 s).
3. **Interface** (2,9–7,3 s) : panneau qui glisse, curseur, toggle, 3 lignes qui apparaissent, notification, chargement, coche de succès.
4. **Compteur** 0 → 275 (7,45–8,9 s) avec montée de tension.
5. **Impact** « 275 effets sonores » (9,6 s) avec secousse caméra, puis pastilles et scintillements.
6. **Outro** logo (12 s).

## SFX utilisés (25 repères, 28 sons placés)
| Repère | Fichier (dans `sfx/`) | Calé sur | Gain |
|---|---|---|---|
| 0.00 s | `DSGNDron_Drone Ethereal Loop_MotionSynth_MotionLib` | début | -24 dB |
| 1.00 s | `DSGNStngr_Logo Reveal Corporate_MotionSynth_MotionLib` | impact | -2 dB |
| 1.40 s | `SWSH_Swish Tiny_MotionSynth_MotionLib` | pic | -9 dB |
| 1.50 s | `SWSH_Swish Tiny_MotionSynth_MotionLib` | pic | -9 dB |
| 1.60 s | `SWSH_Swish Tiny_MotionSynth_MotionLib` | pic | -9 dB |
| 1.90 s | `UIData_Text Typing Screen_MotionSynth_MotionLib` | début | -12 dB |
| 2.55 s | `DSGNMorph_Glitch Transition_MotionSynth_MotionLib` | début | -6 dB |
| 3.10 s | `UIMvmt_Slide In Soft_MotionSynth_MotionLib` | pic | -8 dB |
| 3.45 s | `UIClick_Hover Soft_MotionSynth_MotionLib` | début | -16 dB |
| 3.70 s | `UIClick_Click Hard_MotionSynth_MotionLib` | début | -8 dB |
| 3.72 s | `UIClick_Toggle On_MotionSynth_MotionLib` | début | -9 dB |
| 3.95 s | `UIMvmt_Pop Appear_MotionSynth_MotionLib` | début | -9 dB |
| 4.15 s | `UIMvmt_Pop Appear_MotionSynth_MotionLib` | début | -10 dB |
| 4.35 s | `UIMvmt_Pop Appear_MotionSynth_MotionLib` | début | -12 dB |
| 4.80 s | `UIMvmt_Card Swipe Short_SurajET_SurajSFX06` | pic | -10 dB |
| 4.85 s | `UIAlert_Chime Stair Up_SurajET_SurajSFX06` | début | -9 dB |
| 5.30 s | `UIData_Data Chatter_MotionSynth_MotionLib` | début | -15 dB |
| 6.50 s | `UIAlert_Success Arpeggio_MotionSynth_MotionLib` | début | -6 dB |
| 7.30 s | `WHSH_Air Whoosh Medium_MotionSynth_MotionLib` | pic | -6 dB |
| 7.45 s | `UIData_Score Counter Rollup_MotionSynth_MotionLib` | début | -9 dB |
| 9.60 s | `DSGNRise_Noise Riser 2s_MotionSynth_MotionLib` | fin | -9 dB |
| 9.60 s | `DSGNImpt_Cinematic Hit Big_MotionSynth_MotionLib` | impact | -1 dB |
| 9.60 s | `DSGNBass_Sub Drop 2s_MotionSynth_MotionLib` | début | -5 dB |
| 9.60 s | `DSGNBram_Braam Stab Short_MotionSynth_MotionLib` | début | -11 dB |
| 10.25 s | `DSGNWhsh_Fast Pass By_MotionSynth_MotionLib` | pic | -8 dB |
| 10.45 s | `DSGNWhsh_Fast Pass By_MotionSynth_MotionLib` | pic | -8 dB |
| 11.10 s | `MAGShim_Magic Sparkle_MotionSynth_MotionLib` | début | -13 dB |
| 12.00 s | `DSGNStngr_Logo Reveal Minimal_MotionSynth_MotionLib` | début | -4 dB |

**Calé sur** : *début* = le fichier démarre sur l’image clé ; *impact* = son transitoire principal tombe sur l’image ; *pic* = le pic d’un whoosh tombe sur l’arrivée du mouvement ; *fin* = un riser se termine pile sur l’impact.
Vérifié dans le MP4 final : 0–1 ms d’écart entre les attaques audio et les événements visuels.

## Refaire / modifier
Tout part de `timeline.py` (instants des événements + liste des SFX). Depuis ce dossier :
```
python3 mix.py ../../sfx mix.wav                 # bande son (synchro automatique)
python3 build_page.py motion.html page.html      # injecte la timeline dans l’animation
node render.js $PWD/page.html frames 30 13.2     # images (Playwright + Chromium)
ffmpeg -framerate 30 -i frames/f%04d.png -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest motion_test_sfx.mp4
```

## Version Kdenlive (via CLI-Anything)

Le dossier [`kdenlive/`](kdenlive/) contient la même motion sous forme de **projet Kdenlive éditable**, construit entièrement avec le harness [CLI-Anything](https://github.com/HKUDS/CLI-Anything) `cli-anything-kdenlive` (131 commandes, listées dans `commandes_cli.txt`).

| Fichier | Rôle |
|---|---|
| `motion_test_sfx.kdenlive` | Projet à ouvrir dans Kdenlive : 1 piste vidéo + 13 pistes audio rangées par rôle (Nappe, Whoosh, UI, Notifications, Impacts, Magie et logo), 30 clips SFX avec leur volume, fondus, et 10 repères (guides) sur les événements visuels |
| `motion_video_only.mp4` | L’image de la motion, sans son |
| `rendu_melt.mp4` | Rendu du projet par `melt` (le moteur de Kdenlive) |
| `motion_test_sfx.kdenlive-cli.json` | Projet au format du harness (modifiable avec `cli-anything-kdenlive`) |
| `placement.json`, `commandes_cli.txt` | Où est placé chaque SFX, et les commandes exécutées |

Les médias sont référencés en **chemins relatifs** (`../../../sfx/…`) : le projet s’ouvre tel quel depuis une copie du dépôt.

Vérifié : image identique à la source (PSNR 53,6 dB) ; SFX à ±17 ms des événements (Kdenlive place les clips à l’image près, 1/30 s) ; −17 LUFS, crête −0,6 dBFS (gains −2 dB par rapport à la version MP4, car Kdenlive n’a pas de limiteur sur le master).

Reconstruire / rendre :
```
pip install cli-anything-hub && cli-hub install kdenlive && sudo apt install melt
cd kdenlive && python3 ../kdenlive_build.py ../../../sfx motion_video_only.mp4 .
melt motion_test_sfx.kdenlive -consumer avformat:rendu.mp4 vcodec=libx264 crf=18 acodec=aac ab=256k
```

Défauts du harness rencontrés (version 1.0.0) et contournés dans `kdenlive_build.py` :
- `project new` n’expose pas le rapport d’affichage : en 1080×1920 il reste à 16:9 (image étirée). Corrigé à 9:16 dans le JSON du projet.
- `bin import` ne détecte pas la durée des médias (0 s) : durée passée avec `-d`.
- Pas de commande de rendu (seulement `export xml`) : rendu fait directement avec `melt`.
