"""Monta o prólogo da inscrição e reutiliza a abertura angular do corte anterior."""
from pathlib import Path
import math
import subprocess
import sys

from PIL import Image, ImageDraw

folder = Path(sys.argv[1]).resolve()
evidence = folder.parent/"direcao"
ff = Path("C:/IALD/Central de Patentes/work/mimo26_upgrade_20261020/media_dependency/ffmpeg.exe")
fps, width, height = 30, 1280, 720
prelude_frames = 270
cx, cy = width//2, height//2
scale = 3

def ease(value):
    u = max(0., min(1., value))
    return u*u*(3.-2.*u)

def between(a,b,t):
    return ease((t-a)/(b-a))

def one(draw,x,baseline,h,light):
    """Um mesmo traçado tipográfico em todas as escalas, pé apoiado no eixo."""
    if light<=0 or h<=0:
        return
    color=tuple(round(c*light) for c in (245,224,181))
    def stroke(points,weight):
        draw.line([(round((x+px*h)*scale),round((baseline+py*h)*scale))
                   for px,py in points], fill=color, width=max(1,round(weight*h*scale)),joint="curve")
    stroke([(-.25,-.77),(0,-1.),(0,0)],.091)
    stroke([(-.22,0),(.24,0)],.068)

intro=evidence/"prologo-inscricao.mp4"
args=[str(ff),"-v","error","-n","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{width}x{height}",
      "-framerate",str(fps),"-i","pipe:0","-an","-c:v","libx264","-pix_fmt","yuv420p","-threads","3",
      "-crf","15","-preset","veryfast",str(intro)]
with subprocess.Popen(args,stdin=subprocess.PIPE) as writer:
    for idx in range(prelude_frames):
        t=idx/fps
        # Supersample only the region of the glyphs and of their trace.
        ox, oy = 545, 205
        crop=Image.new("RGB",(470*scale,180*scale))
        draw=ImageDraw.Draw(crop)
        x0,y0=cx-ox,cy-oy
        if 1.15<=t<3.4:
            entering=between(1.55,3.15,t)
            h=77-29*entering
            # The inscribed glyph settles at the isolated point, without a particle trail.
            one(draw,x0,y0-62*(1-entering),h,between(1.15,1.65,t))
        if 3.4<=t<8.42:
            # Seven dyadic subdivisions: only projections become numerous.
            phase=max(0.,min(7.,(t-3.4)/.60))
            level=min(6,int(phase))
            tween=ease(phase-level)
            count=2**level
            h0=48*(.65**level)
            h1=h0*.65
            h=h0+(h1-h0)*tween
            span0=338*(1-math.exp(-.59*level))
            span1=338*(1-math.exp(-.59*(level+1)))
            vanish=1-between(7.6,8.42,t)
            for parent in range(count):
                start=0. if count==1 else span0*parent/(count-1)
                for sister in (0,1):
                    child=2*parent+sister
                    end=span1*child/(2*count-1)
                    x=x0+start+(end-start)*tween
                    # The second image emerges at the same origin, then separates in scale.
                    visibility=(1. if sister==0 else tween)*vanish
                    one(draw,x,y0,h,visibility)
        if t>=6.65:
            built=between(6.65,8.08,t)
            # The baseline is condensed from the feet of the projections, held before theta.
            shade=round(160*built)
            draw.line([(x0*scale,y0*scale),((x0+338*built)*scale,y0*scale)],
                      fill=(round(shade*.81),round(shade*.85),shade),width=3)
        # The point remains fixed throughout. Edge antialiasing keeps the rest truly black.
        point_size=2.6
        draw.ellipse(((x0-point_size)*scale,(y0-point_size)*scale,
                      (x0+point_size)*scale,(y0+point_size)*scale),fill=(244,231,194))
        frame=Image.new("RGB",(width,height))
        frame.paste(crop.resize((470,180),Image.Resampling.LANCZOS),(ox,oy))
        if idx in (22,66,136,176,226,256):
            frame.save(evidence/f"inscricao-{idx:03d}.png")
        writer.stdin.write(frame.tobytes())
    writer.stdin.close()
    if writer.wait():
        raise RuntimeError("Falha no prólogo")
# Resume the original cut at 2.5s, the instant before the angle starts moving.
for previous,current in [("breu-ilhado-global","breu-um-traco-global"),
                         ("breu-ilhado-angulo-de-miguel","breu-um-traco-angulo")]:
    subprocess.run([str(ff),"-v","error","-n","-i",str(intro),"-i",str(folder/(previous+".mp4")),
        "-filter_complex","[0:v]setsar=1,setpts=PTS-STARTPTS[a];[1:v]trim=start_frame=75,setsar=1,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]",
        "-map","[v]","-an","-c:v","libx264","-threads","4","-crf","16","-preset","veryfast","-pix_fmt","yuv420p",
        "-movflags","+faststart",str(folder/(current+".mp4"))],check=True)

