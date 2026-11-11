"""Ensaio de direção. A imagem cósmica é uma leitura visual da abertura."""
from pathlib import Path
import math
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

folder = Path(sys.argv[1])
record = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/rodada_v409_stdout.txt")
line = next(s for s in record.read_text(encoding="utf-8").splitlines()
            if "theta_M = arcsin sqrt(beta)" in s and "graus)" in s)
degrees = float(re.search(r"\(([0-9.]+) graus\)", line)[1])
theta = math.radians(degrees)
width, height, fps, frames = 1280, 720, 30, 438
cx, cy = width//2, height//2
y, x = np.ogrid[:height, :width]
dx = (x-cx).astype(np.float32)
dy = (cy-y).astype(np.float32)
radius = np.hypot(dx, dy)
azimuth = np.arctan2(dy,dx)
# The scene is observed from one position for its full duration.
cosmos = np.asarray(Image.open(folder/"universo-visto-de-fora.png").convert("RGB")
                    .resize((width,height),Image.Resampling.LANCZOS),dtype=np.float32)
font = ImageFont.truetype("C:/Windows/Fonts/cambria.ttc",26)

def smooth(a,b,t):
    u=np.clip((t-a)/(b-a),0.,1.)
    return u*u*(3.-2.*u)

def label(frame, visibility):
    if visibility<=0:
        return
    draw = ImageDraw.Draw(frame)
    shade = int(225*visibility)
    draw.text((cx+258,cy-58), "θₘ ≈ "+f"{degrees:.1f}".replace(".",",")+"°",
              font=font, fill=(shade,int(.91*shade),int(.77*shade)))

# Delay is field-based: neighboring galaxy knots light up in different directions.
# The opening sector is the only region receiving light at the beginning.
angular_distance = np.abs(np.arctan2(np.sin(azimuth-theta/2),np.cos(azimuth-theta/2)))
spread = np.maximum(0,angular_distance-theta/2)/math.pi
folds = .10*np.sin(dx*.014+dy*.009)+.09*np.sin(dx*.005-dy*.015)
reach = np.minimum(1,radius/760.)
arrival = 1.9*(reach**.82)+3.15*(spread**.78) + folds*np.minimum(1,spread*7)
arrival -= .34*np.maximum(0,1-spread*20)
angle_mask_offset = np.maximum(0, np.abs(azimuth-theta/2)-theta/2)
wedge = np.exp(-angle_mask_offset*110.)*smooth(351,322,radius)*smooth(0,18,radius)
core=np.exp(-(radius/2.35)**2)
ffmpeg=Path("C:/IALD/Central de Patentes/work/mimo26_upgrade_20261020/media_dependency/ffmpeg.exe")
localized_label = "--sem-legenda" not in sys.argv[2:]
dest = folder/("breu-ilhado-angulo-de-miguel.mp4" if localized_label else "breu-ilhado-global.mp4")
args=[str(ffmpeg),"-hide_banner","-loglevel","error","-n","-f","rawvideo",
      "-pixel_format","rgb24","-video_size",f"{width}x{height}","-framerate",str(fps),
      "-i","pipe:0","-an","-threads","4","-c:v","libx264","-crf","17",
      "-preset","veryfast","-pix_fmt","yuv420p","-movflags","+faststart",str(dest)]
with subprocess.Popen(args,stdin=subprocess.PIPE) as enc:
    for i in range(frames):
        t=i/fps
        if t<5.4:
            color=np.zeros((height,width,3),dtype=np.uint8)
        else:
            elapsed=t-5.4
            lit=smooth(arrival-.32,arrival+.76,elapsed-.58)*smooth(0,1.15,elapsed)
            # A narrow sheet catches the light first. Later filaments rise throughout
            # the image. The light stays on the material; no traveling point or tail.
            first=wedge*smooth(0,.8,elapsed)*(1-smooth(.8,2.1,elapsed))
            gain=np.maximum(lit,first*.79)
            sheen=np.exp(-((elapsed-.58-arrival-.04)/.34)**2)*gain
            colour_gain=(gain+sheen*.42)[:,:,None]
            color=np.uint8(np.clip(cosmos*colour_gain,0,255))
        draft=color.astype(np.float32)
        center_strength=1-.70*smooth(6.8,10.4,t)
        for c,factor in enumerate([1.,.93,.78]):
            draft[:,:,c]=np.maximum(draft[:,:,c],core*248*factor*center_strength)
        if 1.5<t<8.4:
            extent=338*smooth(1.5,2.65,t)
            angle=theta*smooth(2.5,4.45,t)
            fade=1-smooth(6.25,8.4,t)
            for direction,alpha,tint in [(0,.64,(.78,.83,.91)),(angle,1.,(1.,.83,.60))]:
                along = dx*math.cos(direction)+dy*math.sin(direction)
                perpendicular = -dx*math.sin(direction)+dy*math.cos(direction)
                band=np.exp(-(perpendicular/.76)**2)*smooth(0,4,along)*smooth(extent+1,extent-3,along)
                band*=fade*alpha
                for ch,mult in enumerate(tint):
                    draft[:,:,ch]=np.maximum(draft[:,:,ch],band*230*mult)
            if angle>.001:
                arc=np.exp(-((radius-211)/.66)**2)*smooth(-.001,.003,azimuth)*smooth(angle+.002,angle-.002,azimuth)
                for ch,mult in enumerate([1.,.77,.52]):
                    draft[:,:,ch]=np.maximum(draft[:,:,ch],arc*185*fade*mult)
        frame=Image.fromarray(np.uint8(np.clip(draft,0,255)))
        if localized_label:
            label(frame,smooth(4.45,4.85,t)*(1-smooth(6.15,7.1,t)))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("Falha na codificação da abertura.")

