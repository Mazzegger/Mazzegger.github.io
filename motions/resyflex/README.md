# Motion ResyFlex — « Trouvez · Réservez · Séjournez »

Vidéo verticale **39 s**, 1080×1920, 30 i/s : [`ResyFlex_motion.mp4`](ResyFlex_motion.mp4). Réalisée avec **Remotion** (React), la bibliothèque [`sfx/`](../../sfx/) et une musique synthétisée. Script et légendes : [`SCRIPT.md`](SCRIPT.md).

Contenu tiré uniquement de **resy-flex.com** (relevé le 28/11/2026) : logo officiel, 6 photos de résidences publiées sur le site, prix affichés, fonctionnement en 3 étapes (page À propos), politique d’annulation, villes disponibles, contact. Aucun avis, chiffre ou témoignage inventé.

## Déroulé
| Temps | Scène |
|---|---|
| 0–4 s | Accroche « Tu cherches une résidence meublée en Côte d’Ivoire ? » + photos en rafale |
| 4–7,5 s | Logo, « Résidences meublées en Côte d’Ivoire », Trouvez · Réservez · Séjournez |
| 7,5–12 s | **01 TROUVEZ** — recherche « Abidjan », villes disponibles, « Autour de moi » |
| 12–16 s | Annonces réelles (prix /nuit) + tampon « Vérifiée » |
| 16–20,5 s | **02 RÉSERVEZ** — calendrier, demande, confirmation en 10 min max. |
| 20,5–25 s | Acompte 30 % (exemple : 3 nuits × 40 000 = 36 000 FCFA), Mobile Money / Portefeuille ResyFlex |
| 25–29 s | **03 SÉJOURNEZ** — QR Code scanné à l’arrivée |
| 29–33 s | 4 engagements |
| 33–35 s | Propriétaires : inscription gratuite |
| 35–39 s | Logo, resy-flex.com, +225 01 01 01 46 04 |

## Son
- **Musique** originale synthétisée : groove afro-house / amapiano à 120 BPM (log drum, shaker, clap, piano électrique, arpège au chapitre 3), arrêt d’un temps avant l’impact final. Toutes les coupes tombent sur le temps (1 temps = 15 images).
- **73 SFX** (36 sons différents de `sfx/`, synthétisés et extraits des vidéos), placés automatiquement sur les événements de `src/timeline.json` (synchro sur l’attaque, le pic ou la fin du son). Vérifié dans le MP4 : 0 à 3 ms d’écart entre les attaques audio et les événements visuels.
- −15 LUFS, crête −1 dBFS.

## Fichiers
| Fichier | Rôle |
|---|---|
| `src/timeline.json` | Source unique : instants des scènes et des événements (image ET son) |
| `src/ResyFlex.tsx` | La composition Remotion (10 scènes, icônes, typo Poppins/Inter, couleurs ResyFlex) |
| `audio/build_audio.py` | Musique + placement des SFX + mastering → `public/audio/mix.wav` |
| `public/` | Logo, photos, polices (Poppins, Inter — licence OFL), bande son |

## Modifier / refaire
```
npm install
npm run audio      # régénère la bande son (après modification de timeline.json ou des SFX)
npm run studio     # aperçu interactif dans le navigateur
npm run render     # rendu MP4
```
Pour changer un texte, un prix ou une photo : `src/ResyFlex.tsx` (constantes `CARDS`, `CITIES`, `TRUST`) et `public/img/`. Pour décaler une scène : `src/timeline.json`, puis `npm run audio` et `npm run render`.
