# EasyHmongDev — assets for "Easy Hmong Dev" crayon explainer videos
Folder for AI video generation. Read ONLY what the task needs (saves tokens).

## Layout
- `sprites/`  44 mascot PNGs (transparent) + `meta.js`/`meta.json` (sizes). THE character: never redraw him.
  turnaround front/side/back/three_quarter; faces face_*; poses wave thumbs_up pointing jump sit working walk;
  props laptop reading code coffee idea celebrate; lip-sync busts mouth_* (12); speaking poses say_* (7).
- `icons/`    100 crayon tech icons (512px PNG) + `icons.json` ([{file,label,category}]) + Tabler MIT licence.
- `fonts/`    nl-lao, nl-latin (subtitles/Lao), ns-lao (titles), ph (Latin crayon labels). PH has NO Lao glyphs.
- `engine/`   template_en.html / template_lao.html (full working video pages), lipsync.js, sprite_hero.js, motifs.js,
              env.py (audio -> loudness envelope), render.py, shot.py, cut_*.py, build_icons.py
- `sheets/`   original character sheets (only needed to re-cut sprites)
- `paper.png` 1080x1920 paper background

## Make a video (9:16, 1080x1920, 30fps)
1. New job folder; copy `engine/template_*.html` -> `index.html`, `engine/render.py`, and copy/link `sprites/ icons/ fonts/ paper.png` into it.
2. `python3 engine/env.py narration.wav > env.js` (lip-sync loudness).
3. Edit scenes + subtitles in index.html (keep `render(t)` deterministic in t). Test stills with `shot.py`.
4. `python3 render.py START END frames index.html` (15 fps; split ranges in parallel), then
   `ffmpeg -y -framerate 15 -i frames/f%05d.jpg -i AUDIO -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 -c:a aac -movflags +faststart out.mp4`.
5. Deliver mp4 + post pack (Lao title/caption/hashtags). Say lip-sync and subtitle timing come from loudness, not ASR.

## Rules
- ONE character only (the boy). Several copies at different sizes are OK. Never mix say_* bodies and mouth_* busts in one frame.
- Thank-you bubble follows narration language: English "Thank you!" / Lao "ຂອບໃຈ!" (font NL).
- Lao text: render with real fonts (NL/NS), never AI-generated. Suggest a native Lao check before posting.
- ICONS: use `icons/` ONLY for objects in `icons.json` (computer, phone, server, Wi-Fi, lock, code, AI ...).
  If an object is not in icons.json, or the topic is not tech: DO NOT force this icon style and do not use a "nearest" icon.
  Draw a new prop in code (crayon shapes, topic-fitting style). Mixed videos are fine. Tell the user which props are icons vs new.
- Extra tech icon in the same style: `npm i @tabler/icons` then `python3 build_icons.py file:Label:Category` (see engine/build_icons.py).
- Layout (1080x1920): talking head bust bottom y=1330 h=800 + red band at y=1320; title y~215; subtitles box y~1585; keep bottom 240px free.
- Scripts: do not force a restaurant/stock analogy; explain from the content itself.
