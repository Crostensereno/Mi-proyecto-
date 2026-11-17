#!/bin/bash
# Monta la prueba de anuncio vertical (1080x1920, 30 fps) a partir de fotogramas fijos.
# Uso: montar.sh <carpeta>   (dentro: f1..f4.png, web.mp4, card.png)
set -e
cd "$1"
FPS=30
# duración de cada fotograma (s) y zoom inicial/final: el zoom continúa de uno a otro (efecto cámara que se acerca)
DUR=(0.8 0.8 1.3 1.4)
Z0=(1.00 1.03 1.06 1.10)
Z1=(1.03 1.06 1.10 1.16)
parts=()
for i in 0 1 2 3; do
  n=$((i+1)); frames=$(python3 -c "print(round(${DUR[$i]}*$FPS))")
  ffmpeg -y -loglevel error -loop 1 -i f$n.jpg -vf "scale=2160:3840:flags=lanczos,zoompan=z='${Z0[$i]}+(${Z1[$i]}-${Z0[$i]})*on/$frames':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$frames:s=1080x1920:fps=$FPS,format=yuv420p" \
    -frames:v $frames -c:v libx264 -crf 18 -r $FPS p$n.mp4
  parts+=(p$n.mp4)
done
# Destello blanco corto al pasar del patrón a la tienda
ffmpeg -y -loglevel error -i p4.mp4 -vf "fade=t=out:st=1.25:d=0.15:color=white" -c:v libx264 -crf 18 p4f.mp4
ffmpeg -y -loglevel error -ss 0.9 -i web.mp4 -t 3.2 -vf "fade=t=in:st=0:d=0.2:color=white,fps=$FPS,format=yuv420p" -c:v libx264 -crf 18 pw.mp4
ffmpeg -y -loglevel error -loop 1 -i card.png -t 2.2 -vf "scale=1080:1920,fade=t=in:st=0:d=0.3:color=white,fps=$FPS,format=yuv420p" -c:v libx264 -crf 18 pc.mp4
printf "file 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\nfile 'p4f.mp4'\nfile 'pw.mp4'\nfile 'pc.mp4'\n" > lista.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i lista.txt -c:v libx264 -crf 19 -pix_fmt yuv420p -movflags +faststart prueba_anuncio.mp4
ffprobe -v error -show_entries format=duration:stream=width,height -of default=nw=1 prueba_anuncio.mp4
