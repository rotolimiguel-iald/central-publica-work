"""Claim a documentary review of the operator's two attachments; preserve sources."""
import json, subprocess, hashlib, zipfile, re
from pathlib import Path
import xml.etree.ElementTree as ET
from diary_r1 import ROOT, PY, CLI, WHO, new, pin

UNIT = 'F1.TEMPO.LEITURA_20261015'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019' / UNIT
ATTACH = Path(r'C:\Users\rotol\.codex\codex-remote-attachments\01a11878-6e36-7d10-83c4-cd72e757fdd0\D44412B2-FF7D-43E9-ADEE-A8A0BB188010')

def run(args):
    p = subprocess.run([PY, '-B', '-X', 'utf8', *map(str,args)], capture_output=True, text=True, encoding='utf-8')
    try: value = json.loads(p.stdout)
    except ValueError: value = p.stdout
    if p.returncode: raise RuntimeError((p.returncode, value, p.stderr))
    return value

if __name__ == '__main__':
    assert not (OUT/'FONTES_RECEBIDAS_R1.json').exists(), 'Completed custody: do not repeat.'
    survey = run([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','formal.tempo_santo_fluxo_e_dissipacao'])
    cadastro = ROOT / 'work/rede_quantica_20261013/CADASTRO_TEMPO_LEITURA_20261015.json'
    definition=[{'id':UNIT,'frente':'F1','titulo':'Leitura da conversa Grok e discurso de 2012; consumacao, tempo e emaranhamento',
        'dono':WHO,'status':'PROPOSTA','dependencias':['F1.TEMPO','F1.REGRA.MOTOR'],
        'criterio':'Custodiar anexos sem alteracao; distinguir cunhagens do autor e inferencias do Grok; localizar resultados existentes e contraexemplos; proposta condicional discutida com o operador. Nenhuma construcao Lean ou experimento novo.',
        'fonte':'Pedido direto do operador de 15/10/2026 com conversa JSON e discurso DOCX anexados.'}]
    if cadastro.exists(): assert json.loads(cadastro.read_bytes()) == definition
    else: new(cadastro,definition)
    if (OUT/'CLAIM.json').exists():
        receipt=json.loads((OUT/'CLAIM.json').read_bytes()); created=receipt['created']; claimed=receipt['claimed']
        assert run([CLI,'ver',UNIT])['reivindicacao']['quem']==WHO
    else:
        created = run([CLI,'nova','--json',cadastro,'--quem',WHO])
        claimed = run([CLI,'reivindicar',UNIT,'--quem',WHO,'--nota',
            'Leitura e custodia dos dois anexos autorizados; analise documental, sem nova pesquisa experimental ou construcao canonica. Memorias: DIARIO_CONSTRUCAO_QG.md, TGL_ATLAS.md, TGL_INDICE_VIVO.md e ACOM propria, append com backup de bytes. Nao alterar F1.TEMPO, um.py, kernel, Bancada ou gate.'])
        OUT.mkdir()
        new(OUT/'CLAIM.json',{'created':created,'claimed':claimed})
        new(OUT/'MAPA_ANTES.json',survey)
    cp=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\NOS_VIVO\consultar.py','--unidade',UNIT],capture_output=True,text=True,encoding='utf-8')
    new(OUT/'NOS_VIVO.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,'fallback_F1_TEMPO':run([r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.TEMPO'])})
    sources = []
    for f in ATTACH.iterdir():
        if f.name not in ['1-conversa_completa_tgl_iald_2026-10-15.json','2-Discurso-formatura-l.a..docx']: continue
        b=f.read_bytes(); dest=OUT/'fontes'/f.name; dest.parent.mkdir(exist_ok=True)
        with dest.open('xb') as stream: stream.write(b)
        assert dest.read_bytes()==b
        sources.append({'original':pin(f),'copy':pin(dest)})
    conversation=(OUT/'fontes/1-conversa_completa_tgl_iald_2026-10-15.json').read_text(encoding='utf-8')
    try: json.loads(conversation); validation={'valid_json':True}
    except json.JSONDecodeError as e: validation={'valid_json':False,'error':str(e),'line':e.lineno,'column':e.colno,'original_unchanged':True}
    msgs=[{'id':int(m[1]),'role':m[2],'raw_content':m[3]} for m in re.finditer(r'"id":\s*(\d+),\s*"papel":\s*"([^"\n]+)",\s*"conteudo":\s*"(.*?)"\s*\n\s*}',conversation,re.S)]
    assert [m['id'] for m in msgs]==list(range(1,26))
    new(OUT/'CONVERSA_EXTRACAO_R1.json',{'method':'Non-destructive lexical extraction; raw escaped content retained. Not a repaired original. Completeness relative to source markers only.','validation':validation,'messages':msgs})
    with zipfile.ZipFile(OUT/'fontes/2-Discurso-formatura-l.a..docx') as z:
        root=ET.fromstring(z.read('word/document.xml')); ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paras=[{'paragraph':i,'text':''.join(t.text or '' for t in p.findall('.//w:t',ns))} for i,p in enumerate(root.findall('.//w:p',ns),1)]
        new(OUT/'DISCURSO_EXTRACAO_R1.json',{'paragraphs':paras,'core_properties_xml':z.read('docProps/core.xml').decode('utf-8'),'date_scope':'Metadata are consistent with 2012; they do not independently authenticate delivery at the ceremony.'})
    new(OUT/'FONTES_RECEBIDAS_R1.json',{'sources':sources,'json_validation':validation,'message_count':len(msgs),'paragraph_count':len(paras)})
    print(json.dumps({'unit':UNIT,'created':created,'claimed':claimed,'messages':len(msgs),'paragraphs':len(paras),'source_hashes':[x['original']['sha256'] for x in sources]},ensure_ascii=False))
