#!/usr/bin/env bash
# Télécharge la musique et les effets sonores Mixkit utilisés par la motion (licence Mixkit gratuite :
# utilisables dans la vidéo, mais pas redistribuables seuls — c'est pourquoi ils ne sont pas dans le dépôt).
# Sortie : audio/mixkit/*.wav en 48 kHz stéréo. Nécessite curl et ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p mixkit/_raw
IDS="3115 1433 2364 3120 790 1486 2900 788 772 2627 2608 2568 166 2356 2357 1492 2635 2521 2866 2519 2655 3005 1481 2633 1430 2150 2870 2909 1063 951 2529 1936 1993 2638 890 3116 2842 2350 1464 1474 1992 2918 2901 3062"
for id in $IDS; do
  raw="mixkit/_raw/$id"
  if ! curl -sSf -m 60 -A "Mozilla/5.0" -o "$raw.wav" "https://assets.mixkit.co/active_storage/sfx/$id/$id.wav" 2>/dev/null || ! ffprobe -v error "$raw.wav" >/dev/null 2>&1; then
    rm -f "$raw.wav"; curl -sSf -m 60 -A "Mozilla/5.0" -o "$raw.mp3" "https://assets.mixkit.co/active_storage/sfx/$id/$id-preview.mp3"
  fi
  src=$(ls "$raw".* | head -1)
  ffmpeg -nostdin -v error -y -i "$src" -ar 48000 -ac 2 -c:a pcm_s16le "mixkit/$id.wav"
done
curl -sSf -m 120 -A "Mozilla/5.0" -o mixkit/_raw/836.mp3 "https://assets.mixkit.co/music/836/836.mp3"
ffmpeg -nostdin -v error -y -i mixkit/_raw/836.mp3 -ar 48000 -ac 2 -c:a pcm_s16le mixkit/music_836_lets_move.wav
echo "OK : $(ls mixkit/*.wav | wc -l) fichiers dans audio/mixkit/"
