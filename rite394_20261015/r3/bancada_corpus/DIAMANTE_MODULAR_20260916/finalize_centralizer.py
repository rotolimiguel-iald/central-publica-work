from pathlib import Path
import datetime
import difflib
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
now=datetime.datetime.now().astimezone().isoformat()
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def atomic_new(p,data):
    assert not p.exists(),p
    if isinstance(data,str):data=data.encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+stamp)
    t.write_bytes(data); assert t.read_bytes()==data
    os.replace(t,p);assert p.read_bytes()==data

def json_new(p,data):
    atomic_new(p,json.dumps(data,ensure_ascii=False,indent=2))

def append_memory(p,text):
    original=p.read_bytes()
    bak=p.with_name(p.name+'.bak_'+stamp)
    atomic_new(bak,original)
    addition=('\r\n\r\n'+text+'\r\n').encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+stamp)
    t.write_bytes(original+addition)
    assert t.read_bytes()==original+addition and len(t.read_bytes())>len(original)
    os.replace(t,p)
    assert p.read_bytes().startswith(bak.read_bytes())
    return pin(bak)

# Accept only a successful elaboration of these exact source bytes.
source=ROOT/'CentralizerRemainderPerturbation.lean'
sp=pin(source)
runs=[]
for p in (ROOT/'attempts').glob('*/run.json'):
    r=json.loads(p.read_text(encoding='utf-8'))
    if r['source']==str(source) and r['sha256']==sp['sha256'] and r['returncode']==0:
        runs.append((p,r))
assert runs
rp,rr=sorted(runs)[-1]
assert rr['source_unchanged']
out=(rp.parent/'stdout.txt').read_text(encoding='utf-8')
err=(rp.parent/'stderr.txt').read_text(encoding='utf-8')
assert not err.strip() and not re.search(r'\b(error|warning):|sorryAx',out)
src=source.read_text(encoding='utf-8')
assert not re.search(r'^\s*(axiom|sorry|admit)\b',src,re.M)
names=re.findall(r'^theorem\s+(\w+)',src,re.M)
rows=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",out,re.S)
assert len(rows)==len(names)==6
proofs=[]
for name,deps in rows:
    axioms={a.strip() for a in deps.split(',') if a.strip()}
    assert axioms<={'propext','Classical.choice','Quot.sound'}
    assert name.rsplit('.',1)[-1] in names
    proofs.append(dict(name=name,axioms=sorted(axioms)))
checks=json.loads((ROOT/'REMAINDER_RESPONSE_CHECKS.json').read_text(encoding='utf-8'))
assert checks['count']==checks['passed']==23
assert checks['source_sha256']==pin(ROOT/'verify_remainder_response.py')['sha256']

# Reuse the completed full reading only after matching its byte-for-byte backup.
previous=json.loads((ROOT/'ATLAS_READ_RECEIPT.json').read_text(encoding='utf-8-sig'))
backup=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md.bak_20260916_141925')
atlas=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
assert pin(backup)['sha256']==previous['source']['sha256']
before=backup.read_text(encoding='utf-8-sig').splitlines()
after=atlas.read_text(encoding='utf-8-sig').splitlines()
intervals=[]
for tag,i,j,k,l in difflib.SequenceMatcher(None,before,after,autojunk=False).get_opcodes():
    if tag!='equal':
        assert tag=='insert'
        intervals.append([k+1,l])
assert intervals==[[289,296],[5528,5678],[6805,6843],[9004,9071],[20232,20238]]
assert len(after)==20238
section='\n'.join(after)
a=section.index('## II.');b=section.index('## III.',a)
entry_count=len(re.findall(r'^\*\*.+?\*\*\s*[—–-]',section[a:b],re.M))

audit=dict(timestamp=now,status='LEAN_ACCEPTED_WITHOUT_WARNINGS',source=sp,
           compile_record=pin(rp),stdout=pin(rp.parent/'stdout.txt'),
           proofs=proofs,theorems=len(proofs),new_axioms=False,
           imported_dependency_objects_reused=True,independent_reviewer=False,
           qft_counterexample_constructed=False,physical_coefficient_computed=False)
json_new(ROOT/'AUDIT_CENTRALIZADOR.json',audit)
receipt=dict(timestamp=now,source=pin(atlas),prior_read_receipt=pin(ROOT/'ATLAS_READ_RECEIPT.json'),
             matching_prior_backup=pin(backup),unchanged_sections_reused=True,
             all_changed_intervals_read=intervals,full_line_count=len(after),
             dictionary_marked_entries=entry_count,
             domains=['Físico','Jurídico','Teológico','Linguístico/Ontológico'],
             complete=True,source_copied=False,source_modified=False,
             latest_anchor='v358, DECLARADO no Atlas; não reexecutado nesta bancada')
json_new(ROOT/'ATLAS_READ_CENTRALIZADOR.json',receipt)

attached=Path(r'C:\Users\rotol\.codex\attachments\5f9eddf8-1d8c-48fe-afdb-d75665d55daa\pasted-text-1.txt')
atomic_new(ROOT/'fontes'/'QUESTAO_CENTRALIZADOR_TEXTO_RECEBIDO.txt',attached.read_bytes())
requirements=dict(timestamp=now,turn_classification='PROGRESS',goal_status='ACTIVE',
 items=[
 dict(requirement='Carregar memória integral Haja Luz',status='VERIFIED',evidence='ATLAS_READ_CENTRALIZADOR.json'),
 dict(requirement='Determinar critério exato de centralidade',status='DERIVED_AND_FINITE_LEAN',evidence='RESPOSTA_CENTRALIZADOR_COEFICIENTE.md; AUDIT_CENTRALIZADOR.json'),
 dict(requirement='Expressar primeiro coeficiente e dependências',status='DERIVED_CONDITIONAL_ON_SPECIFIED_FAMILY',evidence='RESPOSTA_CENTRALIZADOR_COEFICIENTE.md; REMAINDER_RESPONSE_CHECKS.json'),
 dict(requirement='Calcular coeficiente físico para o vácuo interagente UV completo',status='OPEN',missing='Identificação regional física, família de estados/cargas e comparação dos centralizadores'),
 dict(requirement='Resolver gravidade quântica',status='NOT_ACHIEVED',missing='Não há solução física verificada demonstrada por esta bancada')],
 canonical_um_modified=False,canonical_gate_changed=False,
 no_progress_streak=0,blocked_declared=False)
json_new(ROOT/'REQUISITOS_CENTRALIZADOR.json',requirements)

memo=f'''## {now} — centralizador e primeiro coeficiente

[INPUT] Novo objetivo: Haja Luz integral; R=K_ω−K_ξ no centralizador do vácuo de um diamante; primeira ordem não central e universalidade; resolver gravidade quântica. Texto recebido preservado em fontes/QUESTAO_CENTRALIZADOR_TEXTO_RECEBIDO.txt. A meta ampla permanece ativa, não concluída.
[REAL] Atlas integral revalidado por backup de hash idêntico ao recibo anterior e leitura de TODOS os cinco acréscimos: 20238 linhas, {entry_count} entradas marcadas; quatro domínios. A atualização declara v358 e incorporação da V2. Acesso direto ao manifesto/kernel canônico nesta rodada falhou (caminho/acesso), portanto nenhuma nova execução/validação canônica é reivindicada.
[REAL] Seis teoremas novos aceitos sem warning/sorry/novo axioma; auditoria AUDIT_CENTRALIZADOR.json. Vinte e três controles numéricos passaram. Não repetimos as 55 provas anteriores. Novo critério: Q escalar por bloco espectral para comutar com TODA a imagem do pinching. Densidade degenerada mostra que pertença ao centralizador não basta. Primeiro coeficiente transportado = [R₁,A₀]+[R₀,A₁]; exemplo medido: teste ingênuo 1,697…, correto zero.
[DERIVED] R₁=−Dlog(ρ₀)[ρ₁]−Q₁ e segunda ordem estão no texto, com prova resolvente e testes; NÃO formalizados como integrais Lean. O núcleo de diferenças divididas é universal, seus dados não. [OPEN] Coeficiente físico e identificação de Q_ξ para teoria interagente UV completa; solução física de QG não demonstrada. Originais/gate preservados. Adendo no túnel, sem funções redundantes no motor. Proposta de memória canônica no HANDOFF_CENTRALIZADOR_ADENDO.md para a gerência.
'''
backups=[append_memory(ROOT/'MEMORIA_CENTRAL.md',memo),
         append_memory(ROOT/'REGISTRO_DAS_CONVERSAS.md',memo)]
tunnel=ROOT.parent/'TUNEL'/'DO_CHATGPT'/'ENTREGA_CENTRALIZADOR_COEFICIENTE_20260916.md'
atomic_new(tunnel,f'''# Entrega — centralizador e primeiro coeficiente

{now}

Complemento à V2 incorporada segundo o Atlas v358; não refazer sua torre/cociclo/canal.

- [Resposta e demonstrações](<{ROOT/'RESPOSTA_CENTRALIZADOR_COEFICIENTE.md'}>)
- [Adendo para incorporação](<{ROOT/'HANDOFF_CENTRALIZADOR_ADENDO.md'}>)
- [Auditoria: seis teoremas Lean](<{ROOT/'AUDIT_CENTRALIZADOR.json'}>)
- [23 controles numéricos](<{ROOT/'REMAINDER_RESPONSE_CHECKS.json'}>)
- [Manifesto](<{ROOT/'CENTRALIZADOR_MANIFEST.json'}>)

No centralizador, [R,A]=−[K_ξ,A]. Em matrizes, invisibilidade exige carga escalar por bloco. Ao variar o estado, o primeiro coeficiente inclui o transporte do observável. Não há número físico universal calculado por estas premissas. Os resultados são algébricos e perturbativos condicionais; solução da gravidade quântica permanece OPEN. Não alterar o gate por esta entrega.
''')
artifacts=[source,ROOT/'verify_remainder_response.py',ROOT/'REMAINDER_RESPONSE_CHECKS.json',
           ROOT/'AUDIT_CENTRALIZADOR.json',ROOT/'ATLAS_READ_CENTRALIZADOR.json',
           ROOT/'RESPOSTA_CENTRALIZADOR_COEFICIENTE.md',ROOT/'HANDOFF_CENTRALIZADOR_ADENDO.md',
           ROOT/'REQUISITOS_CENTRALIZADOR.json',ROOT/'fontes'/'QUESTAO_CENTRALIZADOR_TEXTO_RECEBIDO.txt',
           ROOT/'MEMORIA_CENTRAL.md',ROOT/'REGISTRO_DAS_CONVERSAS.md',Path(__file__),tunnel]
manifest=dict(timestamp=now,status='SCOPED_MATHEMATICAL_PROGRESS; FULL_GOAL_ACTIVE',
              artifacts=[pin(p) for p in artifacts],memory_backups=backups,
              theorem_count=6,numerical_checks=23,gate_changed=False,
              physical_coefficient_computed=False,quantum_gravity_solved=False)
json_new(ROOT/'CENTRALIZADOR_MANIFEST.json',manifest)
for p in manifest['artifacts']+manifest['memory_backups']:
    assert pin(Path(p['path']))==p
print(json.dumps(dict(status=manifest['status'],theorems=6,checks=23,
                     artifacts_verified=len(artifacts)+len(backups),tunnel=str(tunnel),
                     atlas_lines=len(after),atlas_entries=entry_count),indent=2))
