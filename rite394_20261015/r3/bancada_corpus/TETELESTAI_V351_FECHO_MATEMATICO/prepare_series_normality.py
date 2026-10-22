"""Reuse sheet for order normality of the already constructed series functional."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
ROOT=Path(__file__).absolute().parent
K=ROOT/'kernel/TGLExt'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,s):
    assert not p.exists(),p
    b=s.encode('utf-8') if isinstance(s,str) else s
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    os.replace(t,p)
spec=[('V350RegularNormality.lean','theorem vonNeumann_exists_positive_isLUB'),
 ('V351BaseFunctionalEvaluation.lean','theorem exists_base_series_functional'),
 ('V351BaseFunctionalEvaluation.lean','theorem baseFunctional_hasSum_positive_evaluation'),
 ('V351BaseFunctionalWeightLaws.lean','theorem ennreal_tsum_iSup_directed')]
providers=[]
for file,name in spec:
    p=K/file;lines=p.read_text(encoding='utf-8').splitlines()
    hits=[i for i,l in enumerate(lines) if l.startswith(name) and (len(l)==len(name) or l[len(name)] in ' :({')]
    assert len(hits)==1,(name,hits)
    start=hits[0];part=[]
    for l in lines[start:]:
        part.append(l)
        if ':=' in l:break
    providers.append(dict(file=str(p),line=start+1,sha256=sha(p),declaration=name,statement='\n'.join(part),decision='ADAPTAR' if file.startswith('V350') else 'REUSAR'))
cmd=['rg','-n','series.*[Nn]ormal|[Nn]ormal.*series|[Vv]ector.*[Nn]ormal|[Nn]ormal.*[Vv]ector',str(K),'-g','*.lean']
r=subprocess.run(cmd,capture_output=True);assert r.returncode in (0,1) and not r.stderr
sp=ROOT/'search_A1_series_normality.txt';new(sp,r.stdout)
rec=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO',
 consumer='A1(b): qualificar a imagem de series vetoriais efetivamente construida como cone de funcionais positivos normais; alimenta dominio das avaliacoes m_A.',
 exact_target='HasSum vetorial em todo D da mesma base M implica positividade e preservacao de supremos positivos internos de redes dirigidas arbitrarias por ofReal(Re psi). Fornecer normalidade do funcional vetorial pelo limite forte ja construido, depois trocar supremo/serie. Nao provar nem assumir o converso normal=>serie.',
 decision='ADAPTAR limite forte e REUSAR soma/sup; nao refazer aproximantes nem criar outro funcional.',
 providers=providers,search=dict(command=cmd,path=str(sp),sha256=sha(sp),lines=len(r.stdout.splitlines())),
 inherited_six_modalities={n:sha(ROOT/n) for n in ['REAPROVEITAMENTO_A1.json','BUSCAS_A1.json','OUTRAS_BANCADAS_HASHES.json','ADENDO_REAPROVEITAMENTO_A1.json']},
 distinct_from_previous='baseDualEvaluation_input_normal e normalidade em A no core; este alvo e normalidade de psi em D na base. Tipos diferentes, consumidor comum, nenhum homonimo usado como igualdade.')
new(ROOT/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json',json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
new(ROOT/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.md','# A1 — normalidade por ordem dos funcionais de séries\n\n'+rec['timestamp']+'\n\n[OPEN — ficha anterior ao código]\n\n'+rec['consumer']+'\n\n'+rec['exact_target']+'\n\n'+rec['distinct_from_previous']+'\n\nFontes, enunciados, linhas, hashes lidos e buscas no JSON acompanhante; quatro fornecedores existentes reutilizados. Não é predual completo, não é traço e não move gate.\n')
print(json.dumps(dict(providers=len(providers),source_before_code=True,sha256=sha(ROOT/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json')),indent=2))
