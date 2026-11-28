#!/usr/bin/env bash
# Télécharge la musique et les effets sonores Mixkit utilisés par la motion (licence Mixkit gratuite :
# utilisables dans la vidéo, mais pas redistribuables seuls — c'est pourquoi ils ne sont pas dans le dépôt).
# Sortie : audio/mixkit/*.wav en 48 kHz stéréo. Nécessite curl et ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p mixkit/_raw
IDS="498 772 784 788 790 890 951 1059 1430 1464 1474 1485 1486 1493 1936 1992 1993 2150 2350 2356 2357 2364 2519 2521 2529 2586 2599 2626 2627 2633 2635 2638 2655 2842 2857 2858 2866 2870 2900 2901 2902 2903 2918 3005 3062 3115 3116 3120"
for id in $IDS; do
  raw="mixkit/_raw/$id"
  if ! curl -sSf -m 60 -A "Mozilla/5.0" -o "$raw.wav" "https://assets.mixkit.co/active_storage/sfx/$id/$id.wav" 2>/dev/null || ! ffprobe -v error "$raw.wav" >/dev/null 2>&1; then
    rm -f "$raw.wav"; curl -sSf -m 60 -A "Mozilla/5.0" -o "$raw.mp3" "https://assets.mixkit.co/active_storage/sfx/$id/$id-preview.mp3"
  fi
  src=$(ls "$raw".* | head -1)
  ffmpeg -nostdin -v error -y -i "$src" -ar 48000 -ac 2 -c:a pcm_s16le "mixkit/$id.wav"
done
curl -sSf -m 120 -A "Mozilla/5.0" -o mixkit/_raw/371.mp3 "https://assets.mixkit.co/music/371/371.mp3"
ffmpeg -nostdin -v error -y -i mixkit/_raw/371.mp3 -ar 48000 -ac 2 -c:a pcm_s16le mixkit/music_371_cat_walk.wav
echo "OK : $(ls mixkit/*.wav | wc -l) fichiers dans audio/mixkit/"
