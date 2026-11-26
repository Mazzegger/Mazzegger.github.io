# Outils d’extraction

Scripts utilisés pour construire la bibliothèque (Python 3 : numpy, scipy, soundfile, librosa, opencv-python-headless, matplotlib ; ffmpeg).

| Script | Rôle |
|---|---|
| `pano2.py` | Reconstruit la timeline d’une vidéo en panorama (slit-scan à la tête de lecture, défilement mesuré par corrélation de phase). |
| `labels.py` | Détecte les changements de texte à l’écran (noms des sons affichés) et leurs horaires. |
| `review.py` | Vue de contrôle : panorama + spectrogramme + enveloppe sur le même axe temporel. |
| `cut.py` + `specs.json` | Découpe : début calé sur l’attaque, fin à l’extinction ou à la coupe, fondus, normalisation à −1 dBFS. |
| `v12.py` | Extraction avec atténuation de musique de fond (soustraction spectrale). |
| `dedupe.py` | Détection des doublons par corrélation croisée. |
| `build.py` + `mapping.py` | Nommage, classement par catégorie, `catalogue.json`. |
| `post.py` | Rognage des débuts silencieux, retrait de composante continue. |
| `qc.py` | Contrôle qualité (crête, saturation, clics, silence en tête). |
| `docs.py` | Génère `README.md` et `index.html` depuis le catalogue. |

Pour ajouter des vidéos : extraire l’audio en WAV 48 kHz, générer panorama + vue de contrôle, noter les segments dans `specs.json`, compléter `mapping.py`, puis relancer `cut.py` → `build.py` → `post.py` → `qc.py` → `docs.py`.
