from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
RUN=Path((REV/'right_graph_core_final_latest_run.txt').read_text().strip())
v=load(RUN/'verification.json');m=load(RUN/'manifest.json');c=load(RUN/'compilation.json')
assert v['status']=='SIX_MODULES_57_TARGETS_DEV_VERIFIED' and v['all_six_binaries_equal_independent'] and v['all_axioms_allowed']
assert not v['P0'] and not v['P1'] and not v['P2']
assert hf(RUN/'compilation.json')==v['final_compile_sha256']
for name,s in v['modules'].items():
    assert hf(ROOT/'kernel/TGLV350'/(name+'.lean'))==s['source_sha256'] and hf(ROOT/'build/TGLV350'/(name+'.olean'))==s['binary_sha256']
assert hf(ROOT/'right_graph_core_draft_status.json')==v['draft_sha256']
assert hf(ROOT/'RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F_DEV.md')==v['report_sha256']
assert hf(ROOT/'scalar_vna_custody.json')==v['parent_custody_sha256'] and hf(ROOT/'um.py')==v['working_um_sha256']
assert all(hf(ROOT/name)==d['sha256'] for name,d in v['helpers'].items())
pair=Path((REV/'right_projection_pair_latest_run.txt').read_text().strip());prior=load(pair/'partial_review_pin.json')
p=REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md';assert hf(p)==prior['report_sha256'];old=p.read_bytes()
def link(label,path,line=None):return f'[{label}](<{Path(path).as_posix()}{":"+str(line) if line else ""}>)'
def src(line):return link('ScalarRightGraphCore.lean:'+str(line),ROOT/'kernel/TGLV350/ScalarRightGraphCore.lean',line)
table='\n'.join(f'| {name} | {s["target_count"]} | {s["own_seconds"]} | rc0; bytes iguais |' for name,s in v['modules'].items())
helperpins='\n'.join('- '+link(name,ROOT/name)+f': `{d["sha256"]}`.' for name,d in v['helpers'].items())
hist='; '.join(f'{name}: {s["failed_author_count"]}' for name,s in v['modules'].items())
wrapper=v['modules']['ScalarRightGraphCore'];now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''

## Adendo DEV final — seis módulos/57 alvos

RIGHT_GRAPH_CORE_DEV_REVIEW

{now}. **[REAL — revisão matemática e recompilação independente] Escopo DEV completo, sem P0, P1 ou P2.** Este adendo encerra as pendências dos estratos parciais acima, preservados literalmente. A igualdade `closure (scalarRightPairGraph P) = graph (scalarTomitaAdjoint P)` está conferida para o **F original, no mesmo H_I**, sem hipótese residual de graph-core ou de detecção recebida do usuário.

O wrapper final foi lido integralmente. Em {src(43)}, a densidade é a igualdade do fecho das inscrições auto-adjuntas com Fix F. Em {src(60)}, a conclusão é igualdade dos conjuntos de pares em H_I×H_I; o único parâmetro do enunciado concreto é `P : SiteProfile`. {src(77)} extrai a inclusão inversa entre **esses gráficos**, não uma inclusão inversa entre álgebras comutantes.

Descarte efetivo das hipóteses genéricas nas linhas67–75:

| Obrigação | Prova aplicada ao objeto original |
|---|---|
| Gráfico fechado de F | `scalarTomitaAdjoint_isClosed P` |
| j(a)∈D(F), F(j(a))=j(a*) | `scalarRightPairVector_original_adjoint P a` |
| F preserva seu domínio | `scalarTomitaAdjoint_maps_domain P η` |
| F²η=η no domínio | `scalarTomitaAdjoint_involutive P η` |
| Detecção positiva em Fix F | `scalarRight_selfadjoint_detects_fixed P η hη hn` |

Os dois helpers privados compõem os genéricos já revisados; não redefinem F a partir do fecho procurado. A definição herdada `scalarRightPairGraph` foi conferida como `range (a ↦ (j a,j(a*)))`, com a na álgebra de pares direitos efetivos. A detecção vem do par dos blocos e de seu elemento B+B*, a densidade é **real em Fix F**, e a mistura h+ik/h−ik transporta essa densidade ao gráfico. A geometria complexa do gráfico auxiliar continua distinta do gráfico antilinear real de F. Não é uma inferência de graph-core a partir apenas da antiga densidade Hilbert.

O ideal completo nν participa das identidades de multiplicação e pareamento; não foi identificado com o ideal uniforme I, com a álgebra dos pares direitos ou com todo D(F). Também não se afirma D(F)=j(A_right): o resultado é sobre o **fecho do gráfico**.

[REAL — elaboração final] A fonte usa `refine` com hipóteses em buracos separados, descarregadas em blocos, com `maxHeartbeats=200000`. A mesma versão foi reproduzida sem aumento de limite. Não foi feita a especialização alternativa dos helpers ao tipo `NonUnitalStarSubalgebra`. O sucesso confirma a resolução operacional do problema de elaboração; as suspeitas anteriores sobre o caminho interno das instâncias permanecem diagnóstico, não um teorema sobre o elaborador.

Recompilação própria acumulada, sem repetir os cinco módulos verdes:

| Módulo | Alvos | Segundos na sua execução própria | Resultado |
|---|---:|---:|---|
{table}

Nesta chamada foram executados **somente o wrapper** ({c['records'][0]['seconds']} s) **e o auditor57** ({c['records'][1]['seconds']} s), ambos rc0. {link('Compilação final própria',RUN/'compilation.json')}; {link('tipos/universos e axiomas dos 57',RUN/'logs/RightGraphCoreFinalAudit.stdout.txt')}; {link('manifesto da árvore própria',RUN/'manifest.json')}. Todos os 57 conjuntos de axiomas coincidem com o manifesto autoral e os seis logs finais: somente `propext`, `Classical.choice`, `Quot.sound`. Os auxiliares privados são cobertos transitivamente. Os seis `.olean` próprios coincidem byte a byte com os autorais pinados.

A árvore final fixa {len(m['dependencies'])} dependências de projeto copiadas de árvores próprias revisadas, com origem e hashes por arquivo; a cadeia detalhada permanece nos manifestos dos estratos. O genérico `ClosedAntilinearStandardSubspace` provém da recompilação própria `closed_antilinear_dependency_independent_20260912_095836_800005`. O `LEAN_PATH` contém build próprio e oito pacotes externos readonly; não contém build autoral de projeto. Nenhuma dependência antiga foi recompilada. A preparação anteriormente interrompida por catálogo incompleto continua preservada, separada dos resultados Lean.

[REAL — histórico excluído] **{v['failed_wrapper_count']} tentativas autorais rc1 do wrapper**, não oito, foram medidas no manifesto e nos logs; {v['failed_total_count']} rc1 no lote inteiro ({hist}). Nenhum print desses rc1 foi aceito, inclusive prints vazios, auto-referentes ou com `sorryAx`. {link('Verificação cumulativa e histórico com hashes dos streams',RUN/'verification.json')} contém as contagens e os pins. A versão final rc0 é independente desses prints.

Pins finais lidos:

| Artefato | SHA256 |
|---|---|
| `ScalarRightGraphCore.lean` | `{wrapper['source_sha256']}` |
| `.olean` autoral = próprio | `{wrapper['binary_sha256']}` |
| {link('Log autoral final',wrapper['author_final_log'])} | `{wrapper['author_final_log_sha256']}` |
| Stdout autoral final | `{wrapper['author_stdout_sha256']}` |
| `right_graph_core_draft_status.json` | `{v['draft_sha256']}` |
| `RELATORIO_GRAPH_CORE_ADJUNTO_ORIGINAL_F_DEV.md` | `{v['report_sha256']}` |
| Verificação própria cumulativa | `{hf(RUN/'verification.json')}` |

[REAL — documentos e helpers, somente leitura] O relatório autoral completo e o manifesto6/57 foram conferidos; a igualdade concreta agora tem a composição Lean correspondente. Os cinco helpers foram relidos por conferência de bytes com as cópias integralmente inspecionadas no estrato anterior, sem alteração de conteúdo. A lógica prevê mãe `scalar_vna_custody`, batch625→682, seis módulos, requisito de leitura/revisões antes da preparação e do registro, backups imediatos de bytes/append/troca temporária de 34 superfícies, Audit corrente/histórico e releitura de fontes/binários pelo verifier. Trata-se de **inspeção estática**, sem execução desses helpers por esta revisão. Pins:

{helperpins}

O manifesto autoral registra DEV compilado e integração/revisão pendentes no instante de sua emissão; não foi editado pelo revisor. As afirmações de integração nos templates dos recorders só podem ser usadas após a etapa futura e sua revisão. Não foi inspecionado um build integrado novo nem executado teste autoral ou monólito nesta rodada.

[REAL — preservação] Mãe `scalar_vna_custody.json` `{v['parent_custody_sha256']}`; cópia integrada permanece `{v['working_um_sha256']}`. Foram relidos os pins das **34 memórias**, todos iguais à mãe, e confirmado `gate_extension.py` igual ao pin herdado. As seis flags maiores permanecem falsas nos registros da mãe, sem mudança da cópia ou do gate. As fontes/binários/logs autorais e pareceres selados permanecem intactos; este parecer recebe apenas append com backup exato. Não houve atualização de memória, integração, recorder ou monólito pelo revisor.

**Conclusão delimitada:** graph-core de F original demonstrado no pacote DEV6/57 e revisão independente encerrada, sem análise DEV necessária restante neste escopo. Integração continua pendente. A reconstrução R=Jπ(b)J, inclusão inversa dos comutantes pelo J original, identificação de Δ^it/KMS, traço, consumo de certificados/flags e runtime não são conclusões deste lote.
'''
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');backup=p.with_name(p.name+'.bak_'+stamp)
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old;raw=old+text.encode();tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==old;os.replace(tmp,p)
assert p.read_bytes()==raw and p.read_bytes().startswith(backup.read_bytes())
pin={'timestamp':now,'report':str(p),'report_sha256':hf(p),'backup':str(backup),'backup_sha256':hf(backup),'prefix_preserved':True,'marker':'RIGHT_GRAPH_CORE_DEV_REVIEW','scope':'SIX_MODULES_57_TARGETS_DEV_ONLY','P0':[],'P1':[],'P2':[],'development_review_complete':True,'integration_review_complete':False,'verification_sha256':hf(RUN/'verification.json'),'compilation_sha256':hf(RUN/'compilation.json')}
q=RUN/'final_review_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q);print(json.dumps(pin,ensure_ascii=False))
