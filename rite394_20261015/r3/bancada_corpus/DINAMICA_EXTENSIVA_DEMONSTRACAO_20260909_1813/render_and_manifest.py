import os, re, json, hashlib, datetime, io, html, sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent
MD = ROOT / 'DEMONSTRACAO_DINAMICA_EXTENSIVA.md'
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def save(path, data):
    if isinstance(data, str): data = data.encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_bytes()
        bak = path.with_name(path.name + '.bak_' + stamp)
        with bak.open('xb') as f:
            f.write(old); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes() == data and len(data) > 0
    os.replace(temp, path)
    assert path.read_bytes() == data

def pin(path):
    p = Path(path); data = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

for name, file in [('Body','cambria.ttc'),('Bold','cambriab.ttf'),('Italic','cambriai.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts')/file), subfontIndex=0))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Italic', boldItalic='Bold')
styles = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=10.5, leading=15, spaceAfter=8, textColor=colors.HexColor('#1b2834'), allowWidows=0, allowOrphans=0),
    'title': ParagraphStyle('title', fontName='Bold', fontSize=23, leading=27, spaceAfter=15, textColor=colors.HexColor('#12344a')),
    'heading': ParagraphStyle('heading', fontName='Bold', fontSize=13.3, leading=17, spaceBefore=16, spaceAfter=9, keepWithNext=True, textColor=colors.HexColor('#12344a')),
    'eq': ParagraphStyle('eq', fontName='Body', fontSize=10.4, leading=17, leftIndent=12, rightIndent=8, spaceBefore=4, spaceAfter=10, backColor=colors.HexColor('#f1f5f7'), borderPadding=9),
    'bullet': ParagraphStyle('bullet', fontName='Body', fontSize=10.2, leading=14.5, leftIndent=12, firstLineIndent=-9, spaceAfter=7),
    'ref': ParagraphStyle('ref', fontName='Body', fontSize=9.3, leading=12.7, leftIndent=12, firstLineIndent=-9, spaceAfter=6),
}

def inline(s, ref=False):
    links = []
    def take(m):
        label, target = m.group(1), m.group(2).strip('<>')
        if target.startswith('C:/'):
            base, _, line = target.rpartition(':')
            short = Path(base).name + (':' + line if line.isdigit() else '')
            return label + ' — ' + short
        token='ZZLINK'+str(len(links))+'ZZ'
        links.append('<link href="'+html.escape(target,quote=True)+'" color="#175a78">'+html.escape(label)+'</link>')
        return token
    s=re.sub(r'\[([^\]]+)\]\((<[^>]+>|[^)]+)\)',take,s)
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<i>\1</i>',s)
    s=s.replace('*On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian*','<i>On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian</i>')
    # Preserve other literal mathematical stars.
    for n,x in enumerate(links):s=s.replace('ZZLINK'+str(n)+'ZZ',x)
    # Explicit typographic replacements, preserving the mathematical text.
    s=s.replace('ᴺ','<super>N</super>').replace('ᴹ','<super>M</super>').replace('⁰','<super>0</super>')
    s=s.replace('H_N','H<sub>N</sub>').replace('K_N','K<sub>N</sub>').replace('M_N','M<sub>N</sub>')
    s=s.replace('U_N','U<sub>N</sub>').replace('B_N','B<sub>N</sub>').replace('h_j','h<sub>j</sub>').replace('Z_j','Z<sub>j</sub>').replace('X_j','X<sub>j</sub>')
    return s

text=MD.read_text(encoding='utf-8')
story=[]
inrefs=False
for block in re.split(r'\n\s*\n',text.strip()):
    if block.startswith('# '):story.append(Paragraph(inline(block[2:]),styles['title']))
    elif block.startswith('## '):
        if block.startswith('## 11.'):inrefs=True
        story.append(Paragraph(inline(block[3:]),styles['heading']))
    elif block.startswith('>'):
        rows=[line.lstrip('> ').strip() for line in block.splitlines() if line.strip('> ').strip()]
        story.append(KeepTogether([Paragraph('<br/>'.join(inline(x) for x in rows),styles['eq'])]))
    elif block.startswith('- '):
        for line in block.splitlines():
            if line.startswith('- '):story.append(Paragraph('• '+inline(line[2:],inrefs),styles['ref' if inrefs else 'bullet']))
    else:story.append(Paragraph(inline(block.replace('\n',' ')),styles['body']))

missing=sorted({c for c in text if ord(c)>127 and ord(c) not in pdfmetrics.getFont('Body').face.charWidths})
# Superscript N/M are deliberately rendered with Paragraph markup above.
missing=[c for c in missing if c not in 'ᴺᴹ']
if missing:raise RuntimeError('Font missing characters: '+repr(missing))

def decorate(c,doc):
    c.saveState()
    width,height=doc.pagesize
    c.setStrokeColor(colors.HexColor('#bed0da')); c.setLineWidth(0.5)
    c.line(49,height-38,width-49,height-38)
    c.setFont('Body',8);c.setFillColor(colors.HexColor('#466274'))
    c.drawString(49,height-30,'BANCADA CHATGPT  /  DEMONSTRAÇÃO MATEMÁTICA ESCRITA')
    c.line(49,39,width-49,39)
    c.drawString(49,26,'09.09.2026  •  Dinâmica extensiva e alcance da representação')
    c.drawRightString(width-49,26,str(doc.page))
    c.restoreState()

buffer=io.BytesIO()
doc=SimpleDocTemplate(buffer,pagesize=(595.2756,841.8898),rightMargin=49,leftMargin=49,topMargin=56,bottomMargin=54,
    title='Existência da dinâmica extensiva na álgebra quase local canônica',author='Bancada Chatgpt — demonstração para revisão científica',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
pdf=ROOT/'output/pdf/DEMONSTRACAO_DINAMICA_EXTENSIVA.pdf'
save(pdf,buffer.getvalue())

paths=[]
for p in re.findall(r'\]\(<(C:/[^>]+)>\)',text):
    path,line=p.rsplit(':',1)
    if line.isdigit():paths.append(path)
pins=[pin(p) for p in sorted(set(paths))]
receipt=Path('C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BUILD_20260909_173338_542415/BUILD_RESULT.json')
rec=json.loads(receipt.read_bytes())
pins.append({**pin(receipt),'status':rec['status'],'theorems':rec['theorems'],'definitions':rec['definitions']})
sources={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':pins,
    'external':[{'url':'https://arxiv.org/pdf/1410.8174','title':'On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian','authors':['Bruno Nachtergaele','Robert Sims'],'year':2014,'theorem':'4.1','pages_consulted':[7,8,11,12]}]}
save(ROOT/'FONTES_CONSULTADAS.json',json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
manifest={'status':'WRITTEN_PROOF_RENDERED_PENDING_VISUAL_REVIEW','mathematical_status':'DERIVED + KNOWN; not an infinite-limit Lean compilation',
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originals_read_only':True,'um_py_executed_or_imported':False,
    'outputs':[pin(MD),pin(pdf),pin(ROOT/'FONTES_CONSULTADAS.json')],'authoring_script':pin(__file__),
    'font_missing_characters':missing,'pdf_visual_review':'PENDING','independent_review':'PENDING'}
save(ROOT/'MANIFESTO_DEMONSTRACAO.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':manifest['status'],'pdf':pdf.as_posix(),'pdf_bytes':pdf.stat().st_size,'missing':missing},ensure_ascii=False))
