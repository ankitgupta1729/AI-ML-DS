#!/usr/bin/env bash
# =============================================================================
# Income Tax Evaluation System · build-video.sh — assembles the narrated demo MP4.
# Pipeline:  say (TTS) -> per-slide audio -> ffmpeg image+audio segment -> concat
# Each slide is shown for exactly its narration length (+0.8s), so audio and
# video stay perfectly in sync. Run from the demo-video/ folder.
#   ./build-video.sh
# Requires: macOS `say`, `ffmpeg`, `ffprobe`.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"

VOICE="${VOICE:-Samantha}"          # macOS voice; try "Daniel" for UK English
RATE="${RATE:-172}"                 # words per minute
BUILD="build"
AUDIO="audio"
OUT="Income-Tax-Evaluation-System-Demo.mp4"
mkdir -p "$BUILD" "$AUDIO"

# Narration — one entry per slide (must match slides.html order).
NARR=(
"Welcome to the Income Tax Evaluation System. In this short walkthrough, you will see what the project does, the modules it offers, and how your team can use it from any device."
"Tax practitioners traditionally maintain client records, income tax returns, and firm accounts by hand. This is slow, error prone, and hard to search. This system replaces that paperwork with a single, secure, computerised system."
"The system maintains a record for every client. Based on the client's category, it files their original return for a fiscal year, and lets you file a revised return to correct mistakes. For firms, it maintains the trading account, profit and loss account, and balance sheet. And it generates ready to print reports."
"The production system is built with Visual Basic dot NET and an Oracle database, exactly as required. To let anyone try it instantly, we also ship a live web version, with the same modules and the same tax engine, deployed online with no installation needed."
"Access is protected. Every user signs in with a user id and password. Passwords are stored only as secure hashes, and every change to the data is recorded in an audit log."
"After signing in, the dashboard gives a live overview. Total clients, returns filed, revised returns, and the net tax recorded, along with recent activity, so you always know where things stand."
"The Client Information module is the master record. You can add, edit, and delete clients. The PAN is validated and used as the unique key, and deleting a client safely removes all of their linked returns and accounts."
"Filing a return is the heart of the system. Enter the income under each head, and the system computes the tax live, applying the slab rates, rebate, surcharge, and cess, and shows the final balance payable or refund instantly."
"For firm clients, the system maintains the trading account, profit and loss account, and balance sheet. Each has two sides that are totalled automatically, and the system tells you at a glance whether they balance."
"The Reports module generates the four statutory reports. A client's return history, all returns in a fiscal year, and revised returns by a client. Each report can be printed, or saved as a P D F for the client file."
"The application is fully responsive. It works on a laptop, a tablet, or a mobile phone, and includes a polished light and dark theme, so your team gets a great experience on any device."
"That is the Income Tax Evaluation System. A complete, modern income tax workspace. Open the live link, sign in with the demo credentials shown here, and explore every feature yourself. Thank you for watching."
)

echo "== 1/3  Synthesizing narration (voice: $VOICE) =="
CONCAT="$BUILD/concat.txt"; : > "$CONCAT"
for i in "${!NARR[@]}"; do
  n=$((i+1)); nn=$(printf '%02d' "$n")
  slide="$BUILD/slide-$nn.png"
  aiff="$AUDIO/slide-$nn.aiff"
  seg="$BUILD/seg-$nn.mp4"
  [ -f "$slide" ] || { echo "Missing $slide"; exit 1; }
  say -v "$VOICE" -r "$RATE" -o "$aiff" "${NARR[$i]}"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$aiff")
  total=$(awk "BEGIN{printf \"%.2f\", $dur + 0.8}")
  echo "   slide $nn : ${dur}s narration -> ${total}s segment"
  ffmpeg -y -loglevel error -loop 1 -i "$slide" -i "$aiff" -t "$total" \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=25,format=yuv420p" \
    -af "apad" -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -ar 44100 "$seg"
  echo "file 'seg-$nn.mp4'" >> "$CONCAT"
done

echo "== 2/3  Concatenating segments =="
ffmpeg -y -loglevel error -f concat -safe 0 -i "$CONCAT" -c copy "$BUILD/joined.mp4"

echo "== 3/3  Finalizing $OUT =="
ffmpeg -y -loglevel error -i "$BUILD/joined.mp4" -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
echo "Done -> $OUT  (${dur}s)"
