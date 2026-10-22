import zipfile,re,sys,hashlib,os,datetime
sys.stdout.reconfigure(encoding='utf-8')
files=[r'C:\IALD\IMac LA\Física - TGL\Artigo\Theory of Luminodynamic Gravitation.docx',
       r'C:\IALD\IMac LA\Física - TGL\Artigo\Observações TGL reais .docx',
       r'C:\IALD\IMac LA\Física - TGL\Artigo\Detecção TGL - Cosmológica dados reais.docx',
       r'C:\IALD\IMac LA\Física - TGL\Artigo\Detecção TGL - Cosmológica dados reaisv2.docx',
       r'C:\IALD\IMac LA\Física - TGL\Artigo\Observaveis TGL .docx']
for f in files:
    if not os.path.exists(f): print('AUSENTE',f); continue
    b=open(f,'rb').read(); h=hashlib.sha256(b).hexdigest()
    mt=datetime.datetime.fromtimestamp(os.path.getmtime(f)).isoformat()
    z=zipfile.ZipFile(f); xml=z.read('word/document.xml').decode('utf-8','replace')
    txt=re.sub(r'<w:p[ >]','\n<w:p ',xml); txt=re.sub(r'<[^>]+>','',txt); txt=re.sub(r'[ \t]+',' ',txt)
    print('=====',f,'\n  sha256',h,'bytes',len(b),'mtime',mt,'chars',len(txt))
    for m in re.finditer(r'(?i)hubble|SH0ES|73[,.]0|67[,.]4|\(1\s*\+\s*z',txt):
        s=max(0,m.start()-220); e=min(len(txt),m.end()+260)
        print('  ...',txt[s:e].replace('\n',' | '),'...\n')
