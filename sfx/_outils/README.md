# Outils

Python 3 : numpy, scipy, soundfile, librosa (+ opencv-python-headless, matplotlib, ffmpeg pour l’extraction).

## `synth/` — moteur de synthèse
| Fichier | Rôle |
|---|---|
| `motionsynth.py` | Briques : bruits, filtres variables, oscillateurs (saw/square/supersaw, FM, cloches additives, Karplus-Strong), enveloppes, doppler, réverbération, bouclage, finalisation (−1 dBFS, fin propre). |
| `families.py` | Les recettes : un son = une fonction décorée par `@add(famille, CatID, FXName, description)`. |
| `render.py` | Rend toutes les recettes en WAV (vérifie les CatID contre la liste UCS). |
| `ucs_map_extracted.py` | CatID / nom anglais / famille des sons extraits des vidéos. |
| `build_ucs.py` | Assemble la bibliothèque : dossiers UCS, noms UCS, métadonnées WAV, `catalogue.json`, fiches des catégories, CSV UCS. |
| `docs2.py` | Génère `README.md` et `index.html`. |
| `sheets.py`, `steps.py` | Contrôle : planches de spectrogrammes, détection de coupures brutales. |

Ajouter un son : écrire une recette dans `families.py` (CatID choisi dans `../_ucs/UCS_v8.2.1_liste_complete.csv`), puis `render.py` → `build_ucs.py` → `docs2.py`.

## `extraction/` — extraction depuis des vidéos
Reconstruction de la timeline (`pano2.py`), lecture des noms affichés (`labels.py`), vue de contrôle (`review.py`), découpe calée sur l’audio (`cut.py` + `specs.json`), atténuation de musique de fond (`v12.py`), doublons (`dedupe.py`), contrôle qualité (`qc.py`).
