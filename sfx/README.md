# Bibliothèque SFX pour le motion design

133 effets sonores uniques, extraits de 14 vidéos gratuites de créateurs de contenu en motion design (Suraj Editing Tips, @piero.cesti et une vidéo « 10 Sound Effects Every Editor Must Use » sans créateur indiqué).

C’est **la** bibliothèque de référence pour les effets sonores de toutes les animations (motions) produites pour ce projet.

- Écouter : ouvrir [`index.html`](index.html) (lecteur avec recherche et filtres).
- Machine : [`catalogue.json`](catalogue.json) (description, durée, source, horodatage d’origine de chaque son).
- Format : WAV PCM 16 bits, 48 kHz, stéréo, crête normalisée à −1 dBFS.

## Catégories

| Dossier | Contenu | Usage | Nb |
|---|---|---|---|
| [`whoosh/`](whoosh/) | Whoosh / swish | Mouvements, glissements, entrées et sorties d’éléments, transitions rapides. | 36 |
| [`transition/`](transition/) | Transitions | Transitions longues et spectaculaires (montée + impact, ralenti, tourbillon). | 7 |
| [`riser/`](riser/) | Risers / montées | Montées de tension avant une révélation, un impact ou une coupe. | 7 |
| [`impact/`](impact/) | Impacts / booms | Chocs, booms, drops : titres, révélations, temps forts. | 12 |
| [`ui/`](ui/) | Interface (UI) | Clics, boutons, pops, bips : interfaces, curseurs, apparitions d’éléments. | 22 |
| [`notification/`](notification/) | Notifications / dings | Dings, carillons, succès, caisse enregistreuse : validation, prix, récompense. | 11 |
| [`glitch/`](glitch/) | Glitch / sci-fi | Glitchs, zaps, statique, erreurs : style tech, erreurs, transitions numériques. | 16 |
| [`foley/`](foley/) | Foley / objets | Sons d’objets réels : papier, chaîne, clavier, engrenages, feutre, obturateur. | 17 |
| [`cartoon/`](cartoon/) | Cartoon / fun | Rebonds, boings, bloops, scintillements : ton léger et ludique. | 5 |

## Règles d’utilisation dans les motions

1. **Un son = un événement visuel.** Chaque apparition, déplacement, impact ou changement d’écran important reçoit son SFX ; on n’en met pas sur les micro-mouvements.
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

## Catalogue complet

### Whoosh / swish — `whoosh/` (36)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`whoosh_air_1.wav`](whoosh/whoosh_air_1.wav) | 1.12 s | Whoosh d’air avec un ton léger. | Suraj Editing Tips — Sound Effects (whoosh) @ 0.05 s (clip « Who... ») |
| [`whoosh_air_2.wav`](whoosh/whoosh_air_2.wav) | 1.10 s | Whoosh d’air ample. | Suraj Editing Tips — Sound Effects (whoosh) @ 1.20 s (clip « Who... ») |
| [`whoosh_air_3.wav`](whoosh/whoosh_air_3.wav) | 1.14 s | Whoosh à attaque franche. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effects (whoosh) @ 2.31 s (clip « Whoo... ») |
| [`whoosh_air_4.wav`](whoosh/whoosh_air_4.wav) | 1.34 s | Whoosh qui gonfle puis retombe. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effects (whoosh) @ 3.44 s (clip « Whoosh... ») |
| [`whoosh_air_5.wav`](whoosh/whoosh_air_5.wav) | 0.96 s | Whoosh puissant et court. | Suraj Editing Tips — Sound Effects (whoosh) @ 4.82 s (clip « W... ») |
| [`whoosh_air_6.wav`](whoosh/whoosh_air_6.wav) | 1.99 s | Whoosh long (2 s). | Suraj Editing Tips — Sound Effects (whoosh) @ 5.78 s (clip « whoosh.mp3 ») |
| [`whoosh_air_7.wav`](whoosh/whoosh_air_7.wav) | 1.46 s | Whoosh doux et large. | Suraj Editing Tips — Sound Effects (whoosh) @ 7.77 s (clip « Woosh 02... ») |
| [`whoosh_air_8.wav`](whoosh/whoosh_air_8.wav) | 1.25 s | Whoosh d’air. | Suraj Editing Tips — Sound Effect Part 14 @ 6.79 s (clip « SSce Woo... ») |
| [`whoosh_burst.wav`](whoosh/whoosh_burst.wav) | 0.46 s | Bouffée de bruit brève. | Suraj Editing Tips — Sound Effect Part 8 @ 5.97 s (clip « Tren... ») |
| [`whoosh_chirp.wav`](whoosh/whoosh_chirp.wav) | 0.74 s | Swoosh avec gazouillis descendant aigu. | Suraj Editing Tips — Sound Effect Part 12 @ 5.73 s |
| [`whoosh_chirp_up.wav`](whoosh/whoosh_chirp_up.wav) | 0.44 s | Swoosh en glissando montant (0,4 s). | Suraj Editing Tips — Sound Effect Part 10 @ 5.06 s (clip « Filler Sw... ») |
| [`whoosh_double_swish.wav`](whoosh/whoosh_double_swish.wav) | 0.79 s | Double swish (aller-retour). | Suraj Editing Tips — Sound Effect Part 6 @ 13.95 s (clip « Trendi... ») |
| [`whoosh_epic_fast.wav`](whoosh/whoosh_epic_fast.wav) | 0.48 s | Whoosh rapide et percutant. | Suraj Editing Tips — Sound Effect Part 10 @ 0.55 s (clip « epic-fast-... ») |
| [`whoosh_fire_burst.wav`](whoosh/whoosh_fire_burst.wav) | 1.41 s | Souffle de flamme / embrasement. | Suraj Editing Tips — Sound Effect Part 6 @ 3.71 s (clip « fire-sfx... ») |
| [`whoosh_heavy.wav`](whoosh/whoosh_heavy.wav) | 1.11 s | Whoosh lourd. | Suraj Editing Tips — Sound Effect Part 14 @ 5.69 s (clip « Sudo... ») |
| [`whoosh_heavy_rumble.wav`](whoosh/whoosh_heavy_rumble.wav) | 1.45 s | Whoosh lourd et grondant (1,5 s). | Suraj Editing Tips — Sound Effect Part 7 @ 1.71 s (clip « Trending Sound Effect For Video Editing ») |
| [`whoosh_micro_swish.wav`](whoosh/whoosh_micro_swish.wav) | 0.16 s | Micro-swish très bref (0,2 s). Petit mouvement rapide. | Suraj Editing Tips — Sound Effect Part 4 @ 7.96 s |
| [`whoosh_noise_1.wav`](whoosh/whoosh_noise_1.wav) | 0.54 s | Souffle bruité court. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 8 @ 0.01 s (clip « Tre... ») |
| [`whoosh_noise_2.wav`](whoosh/whoosh_noise_2.wav) | 0.38 s | Swish bruité court. | Suraj Editing Tips — Sound Effect Part 8 @ 0.56 s |
| [`whoosh_noise_3.wav`](whoosh/whoosh_noise_3.wav) | 0.79 s | Whoosh bruité. | Suraj Editing Tips — Sound Effect Part 12 @ 6.47 s |
| [`whoosh_noise_4.wav`](whoosh/whoosh_noise_4.wav) | 0.67 s | Whoosh bruité. | Suraj Editing Tips — Sound Effects @ 5.30 s |
| [`whoosh_pop.wav`](whoosh/whoosh_pop.wav) | 0.28 s | Swish court avec pop. | Suraj Editing Tips — Sound Effects @ 0.12 s |
| [`whoosh_shimmer.wav`](whoosh/whoosh_shimmer.wav) | 1.79 s | Whoosh scintillant avec note tenue (1,8 s). | Suraj Editing Tips — Sound Effect Part 12 @ 2.00 s |
| [`whoosh_swell_2.wav`](whoosh/whoosh_swell_2.wav) | 0.59 s | Whoosh qui gonfle. | Suraj Editing Tips — Sound Effects @ 8.04 s |
| [`whoosh_swell_short.wav`](whoosh/whoosh_swell_short.wav) | 0.44 s | Whoosh qui gonfle vers un pic (0,5 s). | Suraj Editing Tips — Sound Effect Part 8 @ 3.65 s (clip « striker... ») |
| [`whoosh_swipe_short.wav`](whoosh/whoosh_swipe_short.wav) | 0.49 s | Petits swishs rapides, glissement de carte/UI. | Suraj Editing Tips — Sound Effect Part 6 @ 1.56 s |
| [`whoosh_swish.wav`](whoosh/whoosh_swish.wav) | 0.91 s | Swish net avec pic central. | Suraj Editing Tips — Sound Effect Part 15 @ 1.91 s (clip « whoosh... ») |
| [`whoosh_swish_short.wav`](whoosh/whoosh_swish_short.wav) | 0.39 s | Swish court. | Suraj Editing Tips — Sound Effects @ 5.96 s |
| [`whoosh_swoosh_down.wav`](whoosh/whoosh_swoosh_down.wav) | 0.52 s | Swoosh descendant. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 13.43 s (clip « SFX 10 ») |
| [`whoosh_textured.wav`](whoosh/whoosh_textured.wav) | 0.78 s | Whoosh texturé. | Suraj Editing Tips — Sound Effect Part 8 @ 1.03 s (clip « Trending Sound E... ») |
| [`whoosh_textured_2.wav`](whoosh/whoosh_textured_2.wav) | 0.81 s | Whoosh texturé qui monte. | Suraj Editing Tips — Sound Effect Part 12 @ 1.07 s |
| [`whoosh_tonal_hit.wav`](whoosh/whoosh_tonal_hit.wav) | 0.31 s | Whoosh avec note. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 11.41 s (clip « SFX 8 ») |
| [`whoosh_transition.wav`](whoosh/whoosh_transition.wav) | 1.43 s | Whoosh de transition (1,4 s). | Suraj Editing Tips — Sound Effect Part 14 @ 2.18 s (clip « transition-ex... ») |
| [`whoosh_up.wav`](whoosh/whoosh_up.wav) | 0.67 s | Whoosh montant vers l’aigu. | Suraj Editing Tips — Sound Effect Part 15 @ 6.78 s (clip « whoosh... ») |
| [`whoosh_zip.wav`](whoosh/whoosh_zip.wav) | 0.10 s | Zip bref (balayage montant). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 10.25 s (clip « SFX 6 ») |
| [`whoosh_zoom_high.wav`](whoosh/whoosh_zoom_high.wav) | 1.00 s | « Zoom » très aigu qui monte. Zoom avant, apparition rapide. | Suraj Editing Tips — Sound Effects (whoosh) @ 9.94 s (clip « zoom1... ») |

### Transitions — `transition/` (7)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`transition_cinematic_riser_hit_1.wav`](transition/transition_cinematic_riser_hit_1.wav) | 3.54 s | Montée d’1 s puis impact cinématique et longue queue (3,7 s). ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 11 @ 10.46 s (clip « Cinematic Epic Trailer Hit and Impact ») |
| [`transition_cinematic_riser_hit_2.wav`](transition/transition_cinematic_riser_hit_2.wav) | 4.11 s | Montée puis gros impact de bande-annonce, longue queue (4,1 s). | Suraj Editing Tips — Sound Effect Part 11 @ 14.00 s (clip « Cinematic Epic Trailer Hit and Impact ») |
| [`transition_epic_blockbuster.wav`](transition/transition_epic_blockbuster.wav) | 3.31 s | Montée pulsée puis gros impact orchestral (3,4 s). Transition de bande-annonce. | Suraj Editing Tips — Sound Effect Part 6 @ 5.41 s (clip « mixkit-epic-blockbuster-movie-transition-2 ») |
| [`transition_epic_orchestra.wav`](transition/transition_epic_orchestra.wav) | 3.37 s | Coup orchestral tenu, épique (3,4 s). | Suraj Editing Tips — Sound Effect Part 6 @ 8.75 s (clip « mixkit-epic-orchestra-transition-2290.wav ») |
| [`transition_slow_motion.wav`](transition/transition_slow_motion.wav) | 6.03 s | Effet ralenti : pulsations qui ralentissent puis ré-accélèrent en montant (6 s). | Suraj Editing Tips — Sound Effect Part 8 @ 6.45 s (clip « 1 Slow Motion 1.7.wav ») |
| [`transition_warp_swirl.wav`](transition/transition_warp_swirl.wav) | 2.53 s | Tourbillon / distorsion spatiale sci-fi (2,5 s). ⚠️ Coupé par la fin de la vidéo source (fondu 300 ms). | Suraj Editing Tips — Sound Effect Part 7 @ 6.10 s (clip « Trending Sound Effect For Video Editing ») |
| [`transition_zhiwop_drop.wav`](transition/transition_zhiwop_drop.wav) | 2.09 s | « Zhwoop » : montée grave puis impact et pulsations (2,1 s). | Suraj Editing Tips — Sound Effect Part 14 @ 0.04 s (clip « Zhiwop Sound Effect @aido... ») |

### Risers / montées — `riser/` (7)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`riser_cinematic_swell_1.wav`](riser/riser_cinematic_swell_1.wav) | 4.40 s | Grande montée cinématique qui gonfle puis s’apaise (4,4 s). ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 12 @ 10.22 s |
| [`riser_cinematic_swell_2.wav`](riser/riser_cinematic_swell_2.wav) | 4.09 s | Grande montée cinématique (4,3 s). ⚠️ Coupé par la fin de la vidéo source (fondu 300 ms). | Suraj Editing Tips — Sound Effect Part 12 @ 14.78 s |
| [`riser_fire_riser.wav`](riser/riser_fire_riser.wav) | 0.76 s | Montée courte qui s’arrête net (0,8 s). | Suraj Editing Tips — Sound Effect Part 6 @ 12.12 s (clip « fire-sfx... ») |
| [`riser_harmonic.wav`](riser/riser_harmonic.wav) | 1.76 s | Montée harmonique (hauteur qui monte, 1,8 s). | Suraj Editing Tips — Sound Effect Part 15 @ 7.59 s |
| [`riser_noise_build.wav`](riser/riser_noise_build.wav) | 2.52 s | Montée de bruit (2,5 s) qui culmine puis retombe. | Suraj Editing Tips — Sound Effects @ 9.75 s |
| [`riser_reverse_whoosh.wav`](riser/riser_reverse_whoosh.wav) | 0.60 s | Whoosh inversé qui s’arrête net : à placer juste avant un impact ou une coupe. | Suraj Editing Tips — Sound Effect Part 15 @ 9.42 s |
| [`riser_swell_tonal.wav`](riser/riser_swell_tonal.wav) | 2.03 s | Nappe qui gonfle avec note (2 s). | Suraj Editing Tips — Sound Effect Part 14 @ 3.61 s (clip « SOUND_1.mp3 ») |

### Impacts / booms — `impact/` (12)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`impact_bass_hit.wav`](impact/impact_bass_hit.wav) | 0.81 s | Coup de basse avec ondulation. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 7 @ 5.29 s (clip « Trending Sound Effect Fo... ») |
| [`impact_boom_long.wav`](impact/impact_boom_long.wav) | 3.19 s | Gros boom grave à longue queue (3,2 s). | Suraj Editing Tips — Sound Effect Part 15 @ 10.69 s (clip « SFX 1.mp3 ») |
| [`impact_cinematic_boom_1.wav`](impact/impact_cinematic_boom_1.wav) | 3.09 s | Impact cinématique grave avec débris aigus (3,1 s). | Suraj Editing Tips — Sound Effect Part 11 @ 0.11 s (clip « Cinematic ... Hit ») |
| [`impact_cinematic_boom_2.wav`](impact/impact_cinematic_boom_2.wav) | 2.56 s | Impact cinématique avec résonance tonale descendante (2,6 s). | Suraj Editing Tips — Sound Effect Part 11 @ 3.20 s (clip « Cinematic ... Hit ») |
| [`impact_cinematic_boom_3.wav`](impact/impact_cinematic_boom_3.wav) | 2.10 s | Impact cinématique puissant et soutenu. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 11 @ 5.76 s (clip « Cinematic ... Hit ») |
| [`impact_cinematic_boom_4.wav`](impact/impact_cinematic_boom_4.wav) | 2.11 s | Impact cinématique avec sub-basse. | Suraj Editing Tips — Sound Effect Part 11 @ 8.25 s (clip « Cinematic ... Hit ») |
| [`impact_hard_hit_rumble.wav`](impact/impact_hard_hit_rumble.wav) | 4.78 s | Gros impact grave avec longue queue de grondement (4,8 s). Titre, révélation, drop. | Suraj Editing Tips — Sound Effect Part 4 @ 9.89 s (clip « Hard hit 3.mp3 ») |
| [`impact_pop_thump.wav`](impact/impact_pop_thump.wav) | 0.42 s | Coup sourd tonal (pop grave). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 8.18 s (clip « SFX 4 ») |
| [`impact_reverb_hit.wav`](impact/impact_reverb_hit.wav) | 1.36 s | Impact avec grande réverbération. ⚠️ Coupé par le montage source (fondu 120 ms). | @piero.cesti — Comment "SFX" @ 3.73 s (clip « Reverb Hit ») |
| [`impact_rumble.wav`](impact/impact_rumble.wav) | 1.12 s | Grondement texturé. | Suraj Editing Tips — Sound Effects @ 8.63 s |
| [`impact_shing_drop.wav`](impact/impact_shing_drop.wav) | 3.91 s | Drop de basse avec « shing » brillant tenu (3,9 s). | Suraj Editing Tips — Sound Effect Part 14 @ 8.05 s (clip « Shing Drop @adobebasic.mp3 ») |
| [`impact_soft_boom.wav`](impact/impact_soft_boom.wav) | 1.86 s | Boom grave enveloppé qui gonfle puis s’éteint (1,9 s). | Suraj Editing Tips — Sound Effect Part 15 @ 0.05 s (clip « Paper ... ») |

### Interface (UI) — `ui/` (22)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`ui_bubble_pops.wav`](ui/ui_bubble_pops.wav) | 0.28 s | Trois petits pops rapides (bulles). Apparition de liste/puces. | Suraj Editing Tips — Sound Effects (whoosh) @ 12.08 s |
| [`ui_button_1.wav`](ui/ui_button_1.wav) | 0.88 s | Bouton : déclic qui gonfle. | Suraj Editing Tips — Sound Effect Part 9 @ 0.82 s (clip « 1 Button.wav ») |
| [`ui_button_2.wav`](ui/ui_button_2.wav) | 0.81 s | Bouton : ding doux à deux notes (1 et 2 kHz). | Suraj Editing Tips — Sound Effect Part 9 @ 0.01 s (clip « Button 2.wav ») |
| [`ui_button_3_tonal.wav`](ui/ui_button_3_tonal.wav) | 1.79 s | Bouton à note tenue, harmonique et doux (≈1,8 s). Validation, menu qui s’ouvre. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 4 @ 1.89 s (clip « Button 3.wav ») |
| [`ui_click_double.wav`](ui/ui_click_double.wav) | 0.21 s | Double clic sec. | Suraj Editing Tips — Sound Effects @ 0.51 s |
| [`ui_click_notification.wav`](ui/ui_click_notification.wav) | 1.03 s | Deux clics + tonalités (type notification). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 12.22 s (clip « SFX 9 ») |
| [`ui_click_tone.wav`](ui/ui_click_tone.wav) | 0.64 s | Clic suivi d’une note tenue (≈600 Hz). | Suraj Editing Tips — Sound Effect Part 4 @ 8.12 s (clip « clic... ») |
| [`ui_data_loading.wav`](ui/ui_data_loading.wav) | 1.45 s | Chargement de données : bips réguliers (1,5 s). | @piero.cesti — Comment "SFX" @ 2.19 s (clip « Data Loading ») |
| [`ui_digital_data_down.wav`](ui/ui_digital_data_down.wav) | 0.95 s | Bips numériques descendants. | Suraj Editing Tips — Sound Effect Part 9 @ 7.30 s (clip « digital_data_up_down_17.wav ») |
| [`ui_digital_data_up.wav`](ui/ui_digital_data_up.wav) | 0.93 s | Bips numériques montants (données, compteur qui monte). | Suraj Editing Tips — Sound Effect Part 9 @ 6.25 s (clip « digital_data_up_down_17.wav ») |
| [`ui_hitech_gui_1.wav`](ui/ui_hitech_gui_1.wav) | 0.67 s | Interface high-tech / sci-fi n°1. | Suraj Editing Tips — Sound Effect Part 10 @ 1.08 s (clip « ES_Hitech GUI, Sc... ») |
| [`ui_hitech_gui_2.wav`](ui/ui_hitech_gui_2.wav) | 0.96 s | Interface high-tech / sci-fi n°2 (interaction). | Suraj Editing Tips — Sound Effect Part 10 @ 1.82 s (clip « ES_Hitech GUI, Scifi, Interact... ») |
| [`ui_hitech_gui_3.wav`](ui/ui_hitech_gui_3.wav) | 0.75 s | Interface high-tech / sci-fi n°3. | Suraj Editing Tips — Sound Effect Part 10 @ 2.77 s (clip « ES_Hitech GUI, Sci... ») |
| [`ui_micro_ticks.wav`](ui/ui_micro_ticks.wav) | 0.65 s | Micro-tics rapides. | Suraj Editing Tips — Sound Effect Part 10 @ 3.52 s (clip « ES_Micro, Ticks - Ep... ») |
| [`ui_open.wav`](ui/ui_open.wav) | 0.58 s | Ouverture d’interface / panneau. | @piero.cesti — Comment "SFX" @ 8.82 s (clip « Open UI ») |
| [`ui_pluck_tonal.wav`](ui/ui_pluck_tonal.wav) | 0.86 s | Ton grave avec pincements. Élément qui se pose. | Suraj Editing Tips — Sound Effects (whoosh) @ 11.06 s |
| [`ui_pop_pluck.wav`](ui/ui_pop_pluck.wav) | 0.27 s | Pop pincé court et aigu (≈1,6 kHz). | Suraj Editing Tips — Sound Effect Part 4 @ 8.76 s |
| [`ui_pop_rise.wav`](ui/ui_pop_rise.wav) | 0.72 s | Pop montant avec résonance. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 3.86 s (clip « SFX 1 ») |
| [`ui_pop_tonal_1.wav`](ui/ui_pop_tonal_1.wav) | 0.47 s | Pop tonal avec harmoniques, attaque grave, extinction rapide. | Suraj Editing Tips — Sound Effect Part 4 @ 6.99 s |
| [`ui_switch.wav`](ui/ui_switch.wav) | 0.76 s | Interrupteur / toggle. | @piero.cesti — Comment "SFX" @ 0.57 s (clip « Switch ») |
| [`ui_tap_double.wav`](ui/ui_tap_double.wav) | 0.24 s | Double tapotement léger. | Suraj Editing Tips — Sound Effect Part 4 @ 9.02 s |
| [`ui_tick_short.wav`](ui/ui_tick_short.wav) | 0.14 s | Tic très court et sec avec une petite note (≈800 Hz). Apparition d’un élément minuscule, curseur. | Suraj Editing Tips — Sound Effect Part 4 @ 0.21 s |

### Notifications / dings — `notification/` (11)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`notification_bell_ding.wav`](notification/notification_bell_ding.wav) | 0.82 s | Cloche/ding clair avec harmoniques. | Suraj Editing Tips — Sound Effects (whoosh) @ 12.76 s |
| [`notification_cash_register_1.wav`](notification/notification_cash_register_1.wav) | 0.71 s | Caisse enregistreuse : mécanique + petite sonnette. | Suraj Editing Tips — Sound Effect Part 4 @ 4.50 s (clip « Cash Register... ») |
| [`notification_cash_register_2.wav`](notification/notification_cash_register_2.wav) | 1.78 s | Caisse enregistreuse longue avec tiroir (choc à 1 s) et sonnerie. Prix, argent, vente. | Suraj Editing Tips — Sound Effect Part 4 @ 5.21 s (clip « Cash Register.wav ») |
| [`notification_cash_register_3.wav`](notification/notification_cash_register_3.wav) | 0.81 s | Caisse enregistreuse courte. | Suraj Editing Tips — Sound Effect Part 9 @ 1.70 s (clip « Cash Register 1.wav ») |
| [`notification_cashier_ka_ching.wav`](notification/notification_cashier_ka_ching.wav) | 1.66 s | « Ka-ching » de caisse : mécanique puis cloche tenue. | Suraj Editing Tips — Sound Effect Part 6 @ 2.05 s (clip « cashier... ») |
| [`notification_chime_trending.wav`](notification/notification_chime_trending.wav) | 1.26 s | Carillon ascendant en escalier (1,3→2,6 kHz). Le « ding » réutilisé partout dans ces vidéos. | Suraj Editing Tips — Sound Effect Part 6 @ 14.95 s (clip « Trendi... ») |
| [`notification_ding_bloop.wav`](notification/notification_ding_bloop.wav) | 1.33 s | Ding aigu tenu + bloop. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 4.79 s (clip « SFX 2 ») |
| [`notification_ding_short.wav`](notification/notification_ding_short.wav) | 0.50 s | Petit « ding » harmonique court. | Suraj Editing Tips — Sound Effect Part 4 @ 7.46 s |
| [`notification_ding_triad.wav`](notification/notification_ding_triad.wav) | 1.10 s | Ding à trois notes tenues. ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 12 @ 4.63 s |
| [`notification_ping_bright.wav`](notification/notification_ping_bright.wav) | 1.21 s | Ping aigu cristallin (≈2,6 kHz) qui s’éteint lentement. | Suraj Editing Tips — Sound Effect Part 6 @ 0.02 s |
| [`notification_success_ui.wav`](notification/notification_success_ui.wav) | 1.05 s | Son de succès d’interface (validation). | @piero.cesti — Comment "SFX" @ 9.82 s (clip « Success UI ») |

### Glitch / sci-fi — `glitch/` (16)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`glitch_burst.wav`](glitch/glitch_burst.wav) | 0.48 s | Rafale glitch/clics courte. | Suraj Editing Tips — Sound Effect Part 8 @ 3.08 s (clip « Best Sou... ») |
| [`glitch_clicks.wav`](glitch/glitch_clicks.wav) | 0.54 s | Clics glitchés rapides. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 10.76 s (clip « SFX 7 ») |
| [`glitch_crackle.wav`](glitch/glitch_crackle.wav) | 0.92 s | Crépitement avec petits chocs. | Suraj Editing Tips — Sound Effects @ 0.83 s |
| [`glitch_ea_glitch.wav`](glitch/glitch_ea_glitch.wav) | 0.43 s | Glitch tonal haché. | Suraj Editing Tips — Sound Effect Part 10 @ 0.02 s (clip « EA Glit... ») |
| [`glitch_glitch_01.wav`](glitch/glitch_glitch_01.wav) | 0.80 s | Glitch avec tonalités résiduelles. | Suraj Editing Tips — Sound Effect Part 10 @ 5.50 s (clip « Glitch 01.wav ») |
| [`glitch_laser_zap.wav`](glitch/glitch_laser_zap.wav) | 0.98 s | Laser / tir sci-fi avec balayages croisés. | Suraj Editing Tips — Sound Effect Part 12 @ 9.24 s |
| [`glitch_negative_1.wav`](glitch/glitch_negative_1.wav) | 0.87 s | Glitch « négatif » (erreur) n°1. | @piero.cesti — Comment "SFX" @ 10.86 s (clip « Negative Glitch 1 ») |
| [`glitch_negative_2.wav`](glitch/glitch_negative_2.wav) | 0.76 s | Glitch « négatif » (erreur) n°2. | @piero.cesti — Comment "SFX" @ 11.76 s (clip « Negative Glitch 2 ») |
| [`glitch_negative_3.wav`](glitch/glitch_negative_3.wav) | 1.14 s | Glitch « négatif » (erreur) n°3. | @piero.cesti — Comment "SFX" @ 12.54 s (clip « Negative Glitch 3 ») |
| [`glitch_noise_burst.wav`](glitch/glitch_noise_burst.wav) | 0.98 s | Bouffée de bruit glitchée avec tonalités. | Suraj Editing Tips — Sound Effect Part 12 @ 0.09 s |
| [`glitch_scifi_descend.wav`](glitch/glitch_scifi_descend.wav) | 0.56 s | Tonalités électroniques descendantes, glitch sci-fi. | Suraj Editing Tips — Sound Effect Part 6 @ 12.97 s |
| [`glitch_static_burst.wav`](glitch/glitch_static_burst.wav) | 0.51 s | Bouffée de statique. | Suraj Editing Tips — Sound Effect Part 7 @ 1.20 s (clip « Trending... ») |
| [`glitch_static_texture.wav`](glitch/glitch_static_texture.wav) | 1.72 s | Texture de bruit/statique avec tonalités (1,7 s). | Suraj Editing Tips — Sound Effect Part 8 @ 4.21 s (clip « Trending Sound Effect... ») |
| [`glitch_thump.wav`](glitch/glitch_thump.wav) | 0.61 s | Glitch avec coup sourd grave. | Suraj Editing Tips — Sound Effects @ 1.84 s |
| [`glitch_transition.wav`](glitch/glitch_transition.wav) | 1.84 s | Transition glitch (1,8 s). | @piero.cesti — Comment "SFX" @ 5.09 s (clip « Glitch Transition ») |
| [`glitch_zap.wav`](glitch/glitch_zap.wav) | 0.45 s | Deux décharges électriques « zap ». | @piero.cesti — Comment "SFX" @ 1.57 s (clip « Zap ») |

### Foley / objets — `foley/` (17)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`foley_chain_1.wav`](foley/foley_chain_1.wav) | 1.03 s | Chaîne métallique (1,1 s). | Suraj Editing Tips — Sound Effect Part 9 @ 2.58 s (clip « cchain-6073.mp3 ») |
| [`foley_chain_2.wav`](foley/foley_chain_2.wav) | 0.58 s | Chaîne métallique (0,7 s). | Suraj Editing Tips — Sound Effect Part 9 @ 3.90 s (clip « cchain-6073.mp3 ») |
| [`foley_chain_3.wav`](foley/foley_chain_3.wav) | 0.50 s | Chaîne métallique (0,5 s). | Suraj Editing Tips — Sound Effect Part 9 @ 4.70 s (clip « cchain-6073.mp3 ») |
| [`foley_chain_4.wav`](foley/foley_chain_4.wav) | 0.74 s | Chaîne métallique (0,8 s). | Suraj Editing Tips — Sound Effect Part 9 @ 5.51 s (clip « cchain-6073.mp3 ») |
| [`foley_click_series.wav`](foley/foley_click_series.wav) | 1.05 s | Série de clics/déclics rapides (≈1 s). | Suraj Editing Tips — Sound Effect Part 8 @ 1.81 s (clip « Best Sound Effects... ») |
| [`foley_clock_ticks.wav`](foley/foley_clock_ticks.wav) | 1.81 s | Tic-tac irréguliers (1,8 s). ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 6.19 s (clip « SFX 3 ») |
| [`foley_film_camera_shutter.wav`](foley/foley_film_camera_shutter.wav) | 0.62 s | Obturateur d’appareil photo argentique. | Suraj Editing Tips — Sound Effect Part 10 @ 4.35 s (clip « film-camera-shutter.m... ») |
| [`foley_film_projector.wav`](foley/foley_film_projector.wav) | 0.62 s | Mécanisme de caméra/projecteur film : trois déclics rapides. | Suraj Editing Tips — Sound Effect Part 4 @ 9.26 s (clip « film... ») |
| [`foley_gears.wav`](foley/foley_gears.wav) | 1.70 s | Engrenages / mécanisme qui tourne. | @piero.cesti — Comment "SFX" @ 6.92 s (clip « Gears ») |
| [`foley_macbook_keyboard.wav`](foley/foley_macbook_keyboard.wav) | 2.97 s | Frappe au clavier MacBook (3 s, avec une pause). | @piero.cesti — Comment "SFX" @ 13.68 s (clip « Macbook Keyboard ») |
| [`foley_marker_draw_line.wav`](foley/foley_marker_draw_line.wav) | 1.32 s | Feutre/surligneur qui trace une ligne (1,3 s). Texte ou trait qui se dessine. | Suraj Editing Tips — Sound Effect Part 10 @ 6.29 s (clip « (OB)Write_Marker Pen Highlighter Draw Line Lon... ») |
| [`foley_paper_crumple.wav`](foley/foley_paper_crumple.wav) | 2.31 s | Papier froissé / bruissement (2,4 s). | Suraj Editing Tips — Sound Effect Part 15 @ 2.82 s (clip « Paper ... ») |
| [`foley_paper_flip.wav`](foley/foley_paper_flip.wav) | 0.69 s | Feuille de papier qu’on tourne. | Suraj Editing Tips — Sound Effect Part 15 @ 5.25 s (clip « Paper Flip Sound... ») |
| [`foley_paper_rustle.wav`](foley/foley_paper_rustle.wav) | 0.67 s | Froissement de papier court. | Suraj Editing Tips — Sound Effect Part 15 @ 6.08 s (clip « Paper... ») |
| [`foley_ratchet_ticks.wav`](foley/foley_ratchet_ticks.wav) | 0.62 s | Cliquetis rapide (cliquet / horloge rapide). | Suraj Editing Tips — Sound Effects (whoosh) @ 9.23 s |
| [`foley_ticking_1.wav`](foley/foley_ticking_1.wav) | 1.18 s | Tic-tac / cliquetis rapide aigu (1,1 s). | Suraj Editing Tips — Sound Effect Part 7 @ 0.02 s (clip « Trending Sound Effect For Video Editing ») |
| [`foley_ticking_2.wav`](foley/foley_ticking_2.wav) | 0.90 s | Cliquetis rapide aigu (0,9 s). ⚠️ Coupé par le montage source (fondu 120 ms). | Suraj Editing Tips — Sound Effect Part 7 @ 3.16 s (clip « Trending Sound Effect For Vid... ») |

### Cartoon / fun — `cartoon/` (5)

| Fichier | Durée | Description | Source |
|---|---|---|---|
| [`cartoon_bloop_up.wav`](cartoon/cartoon_bloop_up.wav) | 0.50 s | Bloop montant (glissando vers l’aigu). Apparition, bulle. | Suraj Editing Tips — Sound Effect Part 6 @ 16.21 s |
| [`cartoon_boing.wav`](cartoon/cartoon_boing.wav) | 0.84 s | « Boing » grave tonal avec clic. | Suraj Editing Tips — Sound Effect Part 12 @ 3.79 s |
| [`cartoon_bounce.wav`](cartoon/cartoon_bounce.wav) | 0.90 s | Rebond cartoon : glissandos montants répétés. Objet qui rebondit, logo qui saute. | Suraj Editing Tips — Sound Effect Part 4 @ 0.49 s (clip « bounce 2.MP3 ») |
| [`cartoon_magic_sparkle.wav`](cartoon/cartoon_magic_sparkle.wav) | 1.86 s | Scintillement magique (1,9 s). Paillettes, apparition magique. | Suraj Editing Tips — Sound Effect Part 12 @ 7.38 s |
| [`cartoon_slide_up.wav`](cartoon/cartoon_slide_up.wav) | 0.95 s | Note qui glisse vers le haut. ⚠️ Musique de fond atténuée (≈ −15 dB) par soustraction spectrale : un léger fond musical peut rester. | Créateur non indiqué — 10 Sound Effects Every Editor Must Use @ 9.00 s (clip « SFX 5 ») |

## Méthode d’extraction

- Chaque vidéo montre une timeline qui défile sous une tête de lecture fixe. La timeline a été reconstruite image par image (panorama « slit-scan » avec mesure du défilement par corrélation de phase) pour identifier chaque clip, sa piste et son nom.
- Les coupes ont ensuite été calées sur l’audio à la milliseconde : début au point le plus calme juste avant l’attaque, fin à l’extinction naturelle du son (ou à la coupe franche quand le son suivant enchaîne).
- Micro-fondus anti-clic (2 ms en entrée, 6 à 12 ms en sortie), fondus plus longs uniquement pour les sons coupés net par le montage ou la fin de la vidéo d’origine (signalés ⚠️).
- Doublons détectés par corrélation croisée des formes d’onde ; la version la plus longue et la plus propre a été conservée.
- La vidéo « 10 Sound Effects » contient une musique de fond sous les SFX : elle a été atténuée d’environ 15 dB par soustraction spectrale (signalé ⚠️ sur ces 10 sons). L’intro et la fin de cette vidéo ne contiennent que de la voix off et n’ont pas été extraites.
- Les noms des clips lus sur les timelines sont indiqués quand ils étaient lisibles ; certains sont tronqués à l’écran (« ... »).

## Droits

Ces sons proviennent de vidéos partagées gratuitement par leurs créateurs ; plusieurs portent des noms de banques connues (Mixkit, Epidemic Sound « ES_ », Adobe…). Vérifier la licence de la banque d’origine avant un usage commercial ou une redistribution publique.
