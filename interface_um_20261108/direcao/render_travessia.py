from pathlib import Path
import sys, subprocess
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image

root = Path(sys.argv[1])
width, height, fps = 1280, 720, 30
seconds = 8.5
rng = np.random.default_rng(318)
def ramp(a, b, x):
    u = np.clip((x-a)/(b-a),0,1)
    return u*u*(3-2*u)
def center(z):
    return np.array([0.7*np.sin(z*.18)+0.13*np.sin(z*.62), 0.48*np.sin(.29*z-.4),z]).T
def basis(z):
    f = center(z+.01)-center(z-.01)
    f /= np.linalg.norm(f)
    r = np.cross(np.array([0.,1.,0.]), f)
    r /= np.linalg.norm(r)
    return r, np.cross(f,r), f
def wires(n):
    z = rng.uniform(-4,43,n)
    lane = rng.integers(0,27,n)
    # Elongated strands weave along an asymmetric, breathing membrane.
    a = lane*2.39996 + .15*z + .75*np.sin(z*.3+lane*.08)
    edge = 1 + .23*np.cos(z*.51 + a*2) + .12*np.sin(z*.95+a)
    fuzz = np.abs(rng.normal(0,.024,n)) + .006
    rad = (1.7+lane%6*.092)*edge
    x = np.cos(a)*rad+rng.normal(size=n)*fuzz
    y = np.sin(a)*rad*.74+rng.normal(size=n)*fuzz
    return center(z)+np.array([x,y,np.zeros(n)]).T,lane
pts,lane=wires(230000)
energy = (0.07 + rng.random(len(pts))**6*.52)[:,None]
cool = (lane%5==1) | (lane%5==3)
tones = np.where(cool[:,None], [0.31,0.56,1.0], [1.0,.69,.38])*energy
# Sparse intrafilament dust gives parallax while leaving clear dark volume.
dust = rng.uniform([-4,-3,-4],[4,3,43],size=(13500,3))
pts = np.concatenate([pts,dust])
tones = np.concatenate([tones, np.tile([.18,.23,.30],(len(dust),1))*(rng.random(len(dust))**5)[:,None]])
xx,yy=np.meshgrid(np.arange(width,dtype=np.float32),np.arange(height,dtype=np.float32))
background=np.zeros((height,width,3),dtype=np.float32)+np.array([.004,.009,.018],dtype=np.float32)
plate=Image.open(root/'primeira-dobra.png').convert('RGB')
art=plate.resize((width,height),Image.Resampling.LANCZOS)
enc=Path('C:/IALD/Central de Patentes/work/mimo26_upgrade_20261020/media_dependency/ffmpeg.exe')
dest=root/'travessia-da-dobra.mp4'
with subprocess.Popen([str(enc),'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{width}x{height}','-framerate',str(fps),'-i','pipe:0','-an','-vcodec','libx264','-threads','4','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE) as writer:
    for frame in range(round(seconds*fps)):
        t=frame/fps
        advance=27*ramp(.25,7.2,t)
        z=-2+advance
        cam=center(z); right,up,forward=basis(z+.48)
        rel=pts-cam
        depth=rel@forward
        valid=(depth>.36)&(depth<34)
        depth=depth[valid]
        focal=685+55*ramp(.2,2,t)
        px=((rel[valid]@right)/depth*focal+width/2).astype(int)
        py=(-(rel[valid]@up)/depth*focal+height/2).astype(int)
        visible=(px>=0)&(px<width)&(py>=0)&(py<height)
        pix=px[visible]+py[visible]*width
        d=depth[visible]
        light = np.minimum(1.4, 2.1/(.70+d*.17))*np.exp(-d*.10)
        # An inscription illuminates the wall as the light front travels on.
        light*=ramp(.30,2.70,t)
        e=tones[valid][visible]*light[:,None]
        layer=np.stack([np.bincount(pix,weights=e[:,c],minlength=width*height).reshape(height,width) for c in range(3)],axis=-1).astype(np.float32)
        small=layer.reshape(height//4,4,width//4,4,3).mean(axis=(1,3))
        halo=gaussian_filter(small,sigma=(1.4,1.4,0))
        glow=np.repeat(np.repeat(halo,4,axis=0),4,axis=1)
        dist=4.6+2.4*ramp(.6,6,t)
        photon=center(z+dist)-cam
        u=width/2+focal*(photon@right)/(photon@forward)
        v=height/2-focal*(photon@up)/(photon@forward)
        rad=((xx-u)**2+(yy-v)**2)
        beam=np.exp(-rad/10)*2.6+np.exp(-rad/160)*.47+np.exp(-rad/1600)*.13
        linear=background+layer*.91+glow*4.2+beam[:,:,None]*np.array([1.0,.78,.52])
        encoded=np.uint8(np.clip(1-np.exp(-linear*1.60),0,1)**.77*255)
        if t>5.55:
            blend=float(ramp(5.55,7.95,t))
            zoom=1+.55*(1-blend)
            w,h=width/zoom,height/zoom
            ax=width*.46; ay=height*.50
            focus=art.transform((width,height),Image.Transform.EXTENT,(ax*(1-w/width),ay*(1-h/height),ax*(1-w/width)+w,ay*(1-h/height)+h),Image.Resampling.BICUBIC)
            encoded=np.asarray(Image.blend(Image.fromarray(encoded),focus,blend))
        writer.stdin.write(encoded.tobytes())
    writer.stdin.close()
    if writer.wait()!=0:
        raise RuntimeError('Video encoding failed')

