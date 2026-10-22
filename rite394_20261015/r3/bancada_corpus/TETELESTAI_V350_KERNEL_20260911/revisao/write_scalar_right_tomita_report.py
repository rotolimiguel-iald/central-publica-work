"""Publish the reviewed 12-target stratum, then byte-backup and append the five-target addendum."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def link(p,label=None):
    p=Path(p);return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def line(rel,n):return '['+Path(rel).name+':'+str(n)+'](<'+(ROOT/rel).as_posix()+':'+str(n)+'>)'
def atomic(p,b):
    assert p.resolve().is_relative_to(REV)
    temp=p.with_name(p.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with temp.open('xb') as f:f.write(b)
    assert temp.read_bytes()==b;temp.replace(p);assert p.read_bytes()==b
r1=Path((REV/'scalar_right_tomita_latest_run.txt').read_text().strip())
r2=Path((REV/'scalar_right_adjoint_latest_run.txt').read_text().strip())
m1=load(r1/'manifest.json');c1=load(r1/'compilation.json')
m2=load(r2/'manifest.json');c2=load(r2/'compilation.json')
for m,c in [(m1,c1),(m2,c2)]:
    assert all(v is True for k,v in c.items() if k!='records')
    assert all(hf(ROOT/n)==h for n,h in m['artifact_pins'].items())
    assert hf(ROOT/'um.py')==m['working_sha256'] and hf(ROOT/'gate_extension.py')==m['gate_sha256']
    for p,r in m['memory_surfaces'].items():
        b=Path(r['backup']).read_bytes();v=Path(p).read_bytes()
        assert sha(v)==r['sha256'] and sha(b)==r['before_sha256'] and v.startswith(b)
    for p,h in m['previous_reviews'].items():assert hf(p)==h
    for rel,s in m['sources'].items():
        assert hf(s['path'])==hf(s['snapshot'])==s['sha256']
        assert hf(s['author_binary'])==s['author_binary_sha256'] and hf(s['author_log'])==s['author_log_sha256']
        a=load(s['author_log']);assert hf(a['stdout'])==s['author_stdout_sha256']
    for row in c['records']:
        assert row['returncode']==0 and row['axioms_allowed'] and row['exact_targets']
        assert hf(row['command'][2])==row['output_sha256']
        assert hf(row['stdout'])==row['stdout_sha256'] and hf(row['stderr'])==row['stderr_sha256']
    audit=c['records'][-1];text=Path(audit['stdout']).read_text(encoding='utf-8')
    assert all(len(re.findall(r'^'+re.escape(n)+r'(?=\s|\{|\.)',text,re.M))==1 for n in m['declarations'])
assert len(m1['declarations'])==12 and len(m2['declarations'])==5
assert set(m1['declarations']).isdisjoint(m2['declarations'])
assert m2['initial_12_manifest_sha256']==hf(r1/'manifest.json')
assert m2['initial_12_compilation_sha256']==hf(r1/'compilation.json')
assert m1['memory_surfaces']==m2['memory_surfaces'] and len(m1['memory_surfaces'])==34
E=load(ROOT/'kernel_incremental_evidence.json');assert all(E[k] is False for k in m1['six_flags'])
def source_table(m):
    t='| Fonte DEV | Alvos | SHA-256 da fonte |\n|---|---:|---|\n'
    for rel,s in m['sources'].items():t+='| '+link(s['path'])+' | '+str(len(s['declarations']))+' | `'+s['sha256']+'` |\n'
    return t
def compile_table(c):
    t='| Execução própria | rc | SHA-256 do .olean próprio | Comparação autoral |\n|---|---:|---|---|\n'
    for row in c['records']:
        t+='| '+link(row['stdout'],Path(row['module']).stem)+' | '+str(row['returncode'])+' | `'+row['output_sha256']+'` | '+('idêntico byte a byte' if row.get('binary_equals_author') else 'auditor próprio')+' |\n'
    return t
def evidence(r):
    return link(r/'manifest.json')+' — SHA-256 `'+hf(r/'manifest.json')+'`; '+link(r/'compilation.json')+' — SHA-256 `'+hf(r/'compilation.json')+'`.'
def artifact_table(m,names):
    t='| Artefato lido | SHA-256 |\n|---|---|\n'
    for n in names:t+='| '+link(ROOT/n)+' | `'+m['artifact_pins'][n]+'` |\n'
    return t
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
initial=f'''Parecer independente DEV — transporte da direita pelo Tomita fechado

SCALAR_RIGHT_CLOSED_TOMITA_DEV_REVIEW

Estrato inicial: {stamp}. **Dois módulos, 12 alvos (7 + 5). Sem achados P0–P2 neste escopo.** [REAL — inspeção integral de fontes/documentação, hashes medidos e recompilação independente.] O adendo abaixo trata separadamente o terceiro módulo; o manifesto inicial permanece com seus 12 alvos.

{source_table(m1)}
Em {line('kernel/TGLV350/ScalarRightStarGraph.lean',12)}, o elemento esquerdo é efetivamente `fibre d.left` na mesma `regularCoreAlgebra P`, usando `d.left_mem`. `HomogeneousRightData P` recebe explicitamente pertinência do operador direito ao comutante da base, pertinência do esquerdo à base, homogeneidade e igualdade dos vetores de vácuo; não recebe KMS. A instância `matrixUnitRightData P N i j` descarrega esses campos na torre anterior. O resultado genérico permanece condicionado a esses dados explícitos e não quantifica sobre qualquer multiplicador sem tais condições.

Em {line('kernel/TGLV350/ScalarRightStarGraph.lean',16)}, `scalarWeightStarRightProduct` pertence ao mesmo `scalarWeightStarCore P`: a finitude de `Ay` usa a lei homogênea anterior; a de `(Ay)* = y* A*` usa o ideal à esquerda aplicado a `A*`. Trata-se de `nν ∩ nν*`, sem substituí-lo pelo ideal uniforme `I`. As duas identidades de inscrição, nas linhas 26 e 32, dão precisamente `(Λ(Ay), Λ((Ay)*)) = (R_y Λ(A), π(y*) Λ(A*))`. A estrela no segundo componente é a estrela algébrica real de `homogeneousRightCoreElement d`, não `modTwist(y)`.

Em {line('kernel/TGLV350/ScalarRightStarGraph.lean',48)} e {line('kernel/TGLV350/ScalarRightClosedTomita.lean',11)}, o mapa do produto é `(x,z) ↦ (R_y x, π(y*)z)`, contínuo porque seus dois componentes são operadores limitados no mesmo `ScalarGNSHilbert P`. A preservação do gráfico do peso passa ao fecho por `MapsTo.closure`; `scalarWeightTomitaGraph_closure_eq` identifica esse fecho com o do gráfico original `scalarTomitaGraph P`. Não se presume continuidade de `S`, nem se troca inclusão por igualdade de imagens.

Em {line('kernel/TGLV350/ScalarRightClosedTomita.lean',19)}, o segundo componente fornece a testemunha de pertinência a `scalarClosedTomitaDomain P`, definido por existência no fecho. Na linha 31, a univalência desse mesmo gráfico identifica o valor escolhido. O enunciado é, para **todo** `x : scalarClosedTomitaDomain P`, `R_y x ∈ D(S)` e `S(R_y x) = π(y*) Sx`. A linha 40 é a especialização matricial. Não há hipótese de que o domínio seja todo o Hilbert ou apenas a imagem algébrica.

**Recompilação própria e proveniência.**

{compile_table(c1)}
Foram compilados exatamente os dois módulos e {link(r1/'sources/ScalarRightTomitaAudit.lean','o auditor próprio dos 12 alvos')}; todos rc0. Os `#check` com universos e `#print axioms` foram lidos integralmente: nomes exatos, 12 distintos, todos somente `propext`, `Classical.choice`, `Quot.sound`. A enumeração cobre as definições e teoremas declarados pelas duas fontes; não foram encontrados `sorry`, `admit`, `axiom`, `unsafe` ou novos atributos de redutibilidade. Os dois binários reproduzem os bytes autorais.

{evidence(r1)}

O `LEAN_PATH` contém somente o build desta árvore e oito diretórios de pacotes externos em leitura. As **{len(m1['dependencies'])} dependências de projeto** foram congeladas a partir das árvores próprias anteriormente revisadas `scalar_weight_gns_independent_20260912_143728_407700` e `homogeneous_right_independent_20260912_153308_891913`, com hashes de fonte/binário/origem no manifesto. Nenhum build autoral de projeto entrou nesse caminho e nenhuma dependência de projeto foi recompilada neste estrato. Conservou-se a exceção documental herdada de `DualSemifiniteIdeal`: diferença literal de comentário já revisada, com ambas as formas e hashes registrados. Pacotes/biblioteca e validação anterior das dependências são herança, não novo rebuild integral. Compilador lido: `{m1['lean_version']}`; SHA-256 `{m1['compiler_sha256']}`. A execução escalada serviu para ler as dependências externas; as saídas próprias ficaram em `revisao/`.

Os logs autorais aceitos foram `ScalarRightStarGraph_20260912_155335_539760.json` e `ScalarRightClosedTomita_20260912_155522_693230.json`. Foram relidos fonte, .olean, JSON, stdout e stderr; rc0, fonte inalterada e saída existente conferem. Cópias dos logs/streams e respectivos hashes estão em {link(r1/'author_history.json')}. A busca delimitada encontrou um log final por módulo; não se usou tentativa fracassada como evidência.

**Manifesto, recorder e 34 superfícies.**

{artifact_table(m1,['scalar_right_tomita_draft_status.json','scalar_right_tomita_draft_memory.json','RELATORIO_DIREITA_TOMITA_FECHADO_DEV.md','record_scalar_right_tomita_draft.py','homogeneous_right_custody.json','homogeneous_right_custody_verification.json'])}
O relatório, o manifesto e `record_scalar_right_tomita_draft.py` foram lidos integralmente; o script foi apenas analisado, sem execução. Seu fluxo confere a mãe integrada e os pins do DEV, registra fonte/binário/log e mantém explicitamente revisão e integração pendentes. Para cada superfície exige o estado da mãe, grava backup imediato de **bytes** na mesma pasta e escreve por temporário verificado → substituição, preservando o prefixo. Essa atomicidade é por arquivo, não uma transação indivisível das 34 superfícies.

[REAL — leitura independente] Foram relidos os **34 arquivos atuais e seus 34 backups** indicados em `scalar_right_tomita_draft_memory.json`: hashes antes/depois corretos, backup no mesmo diretório, prefixo byte a byte preservado, crescimento e marcador DEV pendente presentes. A mãe documental imediata deste DEV é esse registro; sua mãe integrada é `homogeneous_right_custody.json`. Não foram atualizadas memórias por esta revisão. A verificação materna relida registra 157 pares/34 backups; seus 157 binários integrados não foram reaud itados nesta tarefa.

A cópia experimental foi apenas lida para hash: `{m1['working_sha256']}`. `gate_extension.py` conservou o hash `{m1['gate_sha256']}` e a evidência lida mantém as seis flags maiores falsas. As contagens integradas 157/86/6687 e `full_runtime=false` pertencem à mãe anterior; os dois novos módulos não estão integrados. Os pareceres anteriores, fontes/binários autorais e pins documentais permaneceram intactos.

**Limites.** [OPEN] Este estrato não prova KMS global, identificação de `S†S` com o fluxo candidato, traço ou promoção de gate. Também não prova igualdade de ideais `I=nν`, inversibilidade de `R_y` ou invariância bijetiva do domínio. A identificação prévia dos fechos dos gráficos é a ponte usada, sem nova pressuposição sobre o domínio máximo. Nenhuma execução/importação do monólito, recorder ou integrador foi realizada. A revisão DEV dos 12 alvos está concluída; o terceiro módulo tem avaliação separada a seguir.
'''.replace('reaud itados','reauditados')
report=REV/'REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md'
assert not report.exists(),'Do not overwrite an existing review.'
atomic(report,initial.encode('utf-8'))
original=report.read_bytes();backup=report.with_name(report.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f:f.write(original)
assert backup.read_bytes()==original
stamp2=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
addendum=f'''
---

Adendo separado — adjunto máximo, {stamp2}.

**Um módulo adicional, cinco alvos; acumulado três módulos/17 alvos = 12 do manifesto inicial + 5 do manifesto separado. Sem achados P0–P2.** [REAL — inspeção integral e recompilação independente.] O estrato anterior foi preservado por backup imediato de bytes: {link(backup)}, SHA-256 `{hf(backup)}`; o conteúdo final mantém esse prefixo exato.

{source_table(m2)}
Em {line('kernel/TGLV350/ScalarRightTomitaAdjoint.lean',15)}, o pareamento usa a convenção complexa existente `⟨Sx,z⟩ = ⟨S†z,x⟩`. A cadeia é `⟨Sx,π(y)z⟩ = ⟨π(y*)Sx,z⟩ = ⟨S(R_y x),z⟩ = ⟨S†z,R_y x⟩ = ⟨R_y* S†z,x⟩`. As duas passagens por adjuntos limitados têm a orientação correta; não falta conjugação adicional. `x` percorre **todo** `scalarClosedTomitaDomain P`, conforme o tipo impresso, e `R_y x` tem a pertinência já provada no estrato inicial.

Em {line('kernel/TGLV350/ScalarRightTomitaAdjoint.lean',44)}, `scalarTomitaAdjoint_maximal` converte esse pareamento universal em pertinência de `π(y)z` ao domínio e igualdade com `R_y* S†z`. Conferida a dependência {line('kernel/TGLV350/ScalarTomitaAdjoint.lean',13)}: trata-se do adjunto antilinear **máximo do mesmo S em H_I**, cuja unicidade usa a densidade anterior de `D(S)`. Nas linhas 53–63 do novo módulo, `choose` seleciona a prova de pertinência do vetor fixo `π(y)z`; não escolhe outro operador, vetor ou domínio. Não se pressupõe a invariância buscada, a continuidade de `S` ou a de `S†`.

Em {line('kernel/TGLV350/ScalarRightTomitaAdjoint.lean',65)}, a instância matricial substitui legitimamente `R_y*` por `homogeneousRightGNS (matrixUnitTwistedRightData ...)`, usando `matrixUnitRightGNS_adjoint` herdado. É aqui que aparece `modTwist(y)`, no multiplicador direito adjunto; continua distinto do `y*` em `S R_y = π(y*)S`. Não houve nova hipótese sobre `P` nem campo KMS introduzido.

{compile_table(c2)}
O módulo e {link(r2/'sources/ScalarRightAdjointAudit.lean','o auditor próprio dos cinco alvos')} passaram rc0. Foram lidos os cinco tipos com universos e todos os axiomas; nomes exatos e somente o trio. Alvos: `scalarRightTomitaAdjoint_pairing`, `scalarRightTomitaAdjoint_maximal`, `scalarRightTomitaAdjointInput`, `scalarTomitaAdjoint_left_intertwines` e `matrixUnit_TomitaAdjoint_left_intertwines`, no namespace `TGLV350.Regular`. O binário é idêntico ao autoral; nenhuma recompilação dos dois módulos já verdes foi repetida.

{evidence(r2)}

O fecho de imports possui **{len(m2['dependencies'])} dependências pinadas**: reutiliza o estrato próprio dos 12 alvos e a árvore própria `scalar_tomita_involution_independent_20260912_133836_401235` para o adjunto já revisto, conferindo igualdade de hashes nas dependências compartilhadas. O build autoral continuou fora do `LEAN_PATH`; pacotes e provas herdadas não foram recompilados. Fonte, binário e streams do log final `ScalarRightTomitaAdjoint_20260912_160610_026235.json` foram relidos e preservados em {link(r2/'author_history.json')}; rc0/fonte inalterada/saída existente conferem. Só esse log autoral foi encontrado para o módulo.

{artifact_table(m2,['scalar_right_adjoint_draft_status.json','record_scalar_right_adjoint_draft.py'])}
O manifesto adicional fixa o manifesto inicial em `{m2['artifact_pins']['scalar_right_tomita_draft_status.json']}` e a memória imediata em `{m2['artifact_pins']['scalar_right_tomita_draft_memory.json']}`; ambos foram relidos sem alteração. `record_scalar_right_adjoint_draft.py`, lido integralmente e apenas parseado, cria somente o manifesto adicional por temporário verificado, recusa sobrescrevê-lo e não escreve nas 34 memórias. Mantém `memory_update_pending_review_in_this_turn=true`, `integrated=false` e `KMS_proved=false`. Os 34 pares foram conferidos novamente e continuam iguais aos do primeiro estrato.

**Conclusão DEV delimitada: revisão dos três módulos/17 alvos encerrada, sem achados P0–P2 e sem análise necessária pendente nesse escopo.** As cinco execuções próprias (três módulos + auditores 12 e 5) foram rc0; os três binários coincidem com os autorais. [OPEN] KMS, ligação do operador modular ao fluxo, traço, consumo por contrato/gate e runtime continuam fora da conclusão. A integração dos 17 alvos não foi revista nem declarada realizada. Os três helpers de integração futuros e a proposta de atualização dos hashes globais de Audit ficam para solicitação posterior; nenhuma execução deles, registro de custódia ou escrita de memória é atribuída a esta revisão.
'''
atomic(report,original+addendum.encode('utf-8'))
assert report.read_bytes().startswith(backup.read_bytes())
assert report.read_text(encoding='utf-8').count('SCALAR_RIGHT_CLOSED_TOMITA_DEV_REVIEW')==1
v={'timestamp':stamp2,'report':str(report),'report_sha256':hf(report),'bytes':report.stat().st_size,
 'initial_prefix_backup':str(backup),'initial_prefix_sha256':hf(backup),'exact_prefix_preserved':True,
 'initial_targets':12,'addendum_targets':5,'cumulative_targets':17,'modules':3,'own_executions_rc0':5,
 'source_binaries_equal_author':3,'axioms_only_trio':True,'P0':[],'P1':[],'P2':[],
 'compilation_jsons':{str(r/'compilation.json'):hf(r/'compilation.json') for r in [r1,r2]},
 'memory_pairs_rechecked':34,'integration_reviewed':False,'new_helpers_executed':False,'memory_written':False}
verification=REV/'scalar_right_tomita_report_verification.json';assert not verification.exists()
atomic(verification,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(v,ensure_ascii=False,indent=2))
