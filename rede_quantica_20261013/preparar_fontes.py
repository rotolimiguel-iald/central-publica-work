"""Custody and extract primary scientific sources; no production execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from pypdf import PdfReader
ROOT=Path(r'C:\IALD\Central de Patentes')
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
S=OUT/'sources'; S.mkdir(exist_ok=True)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
paths=[ROOT/'Patentes/Psi_Net_Protocol_PI_INPI.tex',ROOT/'Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex',ROOT/'Patentes/TGL_Tensor_LLM_PI_INPI.tex',ROOT/'Patentes/MQC - Microprocessador Cúbico/mqc_pi_inpi_relatorio descritivo.pdf']
entries=[]
for p in paths:
 item=pin(p)
 if p.suffix=='.pdf':
  reader=PdfReader(p)
  text='\n\n'.join(f'[[PDF_PAGE_{i+1}]]\n'+(page.extract_text() or '') for i,page in enumerate(reader.pages))
  q=S/'MQC_DESCRITIVO_EXTRACT_R1.txt'
  with q.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
  item.update(extraction=pin(q),pages=len(reader.pages),method='pypdf text extraction; equations require visual/source verification')
 entries.append(item)
with (S/'PRIMARY_SOURCES_R1.json').open('x',encoding='utf-8',newline='\n') as f:json.dump({'at':datetime.now(timezone.utc).isoformat(),'sources':entries},f,ensure_ascii=False,indent=2)
print(json.dumps([{'path':x['path'],'bytes':x['bytes'],'pages':x.get('pages')} for x in entries],ensure_ascii=False))
