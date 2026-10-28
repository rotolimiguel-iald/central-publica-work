from pathlib import Path
import struct,json,hashlib,datetime,wave,os
R=Path(__file__).resolve().parent.parent;W=R/'cinema_v7'
def boxes(data):
 at=0
 while at+8<=len(data):
  size,kind=struct.unpack_from('>I4s',data,at);head=8
  if size==1:size=struct.unpack_from('>Q',data,at+8)[0];head=16
  if size==0:size=len(data)-at
  if size<head or at+size>len(data):raise ValueError('Malformed box '+repr(kind))
  yield kind.decode('ascii',errors='replace'),data[at+head:at+size];at+=size
def find(data,key):
 for k,v in boxes(data):
  if k==key:return v
 raise KeyError(key)
def mp4(path):
 with path.open('rb') as f:
  moov=None
  while True:
   head=f.read(8)
   if not head:break
   size,kind=struct.unpack('>I4s',head);header=8
   if size==1:size=struct.unpack('>Q',f.read(8))[0];header=16
   if size==0:size=path.stat().st_size-f.tell()+header
   if kind==b'moov':moov=f.read(size-header);break
   f.seek(size-header,1)
 if moov is None:raise ValueError('Missing moov')
 mvhd=find(moov,'mvhd');v=mvhd[0];offset=20 if v else 12;timescale=struct.unpack_from('>I',mvhd,offset)[0];duration=struct.unpack_from('>Q' if v else '>I',mvhd,offset+4)[0]/timescale
 tracks=[]
 for kind,tr in boxes(moov):
  if kind!='trak':continue
  tk=find(tr,'tkhd');mdia=find(tr,'mdia');md=find(mdia,'mdhd');handler=find(mdia,'hdlr')[8:12].decode()
  v=md[0];off=20 if v else 12;scale=struct.unpack_from('>I',md,off)[0];dur=struct.unpack_from('>Q' if v else '>I',md,off+4)[0];loff=off+4+(8 if v else 4);lang=struct.unpack_from('>H',md,loff)[0];language=''.join(chr(((lang>>s)&31)+96) for s in [10,5,0])
  stbl=find(find(mdia,'minf'),'stbl');stsd=find(stbl,'stsd');codec=stsd[12:16].decode()
  stts=find(stbl,'stts');n=struct.unpack_from('>I',stts,4)[0];entries=[struct.unpack_from('>II',stts,8+i*8) for i in range(n)];samples=sum(x[0] for x in entries);ticks=sum(x[0]*x[1] for x in entries)
  track={'type':handler,'codec':codec,'language':language,'duration':dur/scale,'samples':samples,'timescale':scale}
  if handler=='vide':track.update(width=struct.unpack_from('>I',tk,len(tk)-8)[0]>>16,height=struct.unpack_from('>I',tk,len(tk)-4)[0]>>16,fps=samples/(ticks/scale))
  stsz=find(stbl,'stsz');uniform_size,count=struct.unpack_from('>II',stsz,4)
  byte_count=uniform_size*count if uniform_size else sum(struct.unpack_from('>I',stsz,12+i*4)[0] for i in range(count))
  track.update(encoded_bytes=byte_count,bitrate_bps=byte_count*8/(dur/scale))
  tracks.append(track)
 return {'file':path.relative_to(R).as_posix(),'bytes':path.stat().st_size,'duration':duration,'tracks':tracks}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,s):
 b=s.encode('utf-8')
 if p.exists():p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(p.read_bytes())
 tmp=p.with_suffix('.tmp');tmp.write_bytes(b);assert len(b)==tmp.stat().st_size;os.replace(tmp,p)
