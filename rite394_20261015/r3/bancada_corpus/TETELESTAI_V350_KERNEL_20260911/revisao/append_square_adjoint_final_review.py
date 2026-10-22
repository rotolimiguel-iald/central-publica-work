from pathlib import Path
import datetime, hashlib, json, os, re
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=Path((REV/'square_adjoint_final_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');hist=load(RUN/'author_history.json')
for k in ['complete','all_exit_zero','exact_5_and_20_targets','all_axioms_allowed','all_axioms_match_author','new_binary_equal_author','inherited_two_binaries_preserved','source_snapshots_preserved','readonly_artifacts_preserved','dependencies_preserved','external_direct_pins_preserved']:assert c[k],k
report=REV/'REVIEW_SQUARE_RESOLVENT_DEV.md';old=report.read_bytes();assert sha(old)==m['readonly_pins'][str(report)]
for p,h in m['readonly_pins'].items():assert hf(p)==h,p
third=m['sources']['TGLV350/ScalarSquareAdjointTest.lean'];raw=Path(third['snapshot']).read_bytes();lines=raw.decode().splitlines()
assert '600000' not in raw.decode()
def ln(n):return next(i+1 for i,l in enumerate(lines) if re.match(r'(?:private )?(?:theorem|def) '+re.escape(n)+r'\b',l))
tables='\n'.join('| '+Path(rel).stem+' | `'+d['sha256']+'` | `'+d['author_binary_sha256']+'` |' for rel,d in m['sources'].items())
targets='\n'.join('- `'+n+'`' for n in third['declarations'])
failed=[h for h in hist if h['module']=='ScalarSquareAdjointTest' and h['returncode']!=0];assert len(failed)==5
failure_names=', '.join('`'+Path(h['log']).stem.removeprefix('ScalarSquareAdjointTest_20260913_')+'`' for h in failed)
new,audit=c['records'];stamp=datetime.datetime.now().astimezone().isoformat();suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
probe=REV/'square_adjoint_probe_20260913_053747_825645';diag=load(probe/'SubalgebraBridgeV1.json');assert diag['returncode']==0 and diag['all_five_trio']
text=f'''

## Adendo DEV FINAL 20 = 6 + 9 + 5 — {stamp}

SQUARE_RESOLVENT_DEV_REVIEW

[REAL — fontes lidas e reproduzidas em árvore independente.] **Nenhum P0–P2 identificado nos três módulos/20 alvos finais.** Este adendo encerra o pacote DEV completo; preserva os estratos6/15, que isoladamente não autorizavam o terceiro módulo. A fonte autoral final `ScalarSquareAdjointTest.lean` foi lida INTEIRA e recompilada sem modificações, com maxHeartbeats=200000 e synthInstance.maxHeartbeats=200000, sem opções locais600000.

**O que o terceiro módulo prova e como as hipóteses são descarregadas:**

- `{ln('differencePairing')}`–`{ln('scalarSelfadjointPairing_of_squarePairing')}`: a igualdade de pareamentos é estável sob diferença e escala REAL ¼, pois a conjugação complexa fixa esse coeficiente. Os dois testes usados são em (a+d_n)² e (a−d_n)²; a auto-adjunticidade de a±d_n vem de ha e do corte auto-adjunto já construído. O `let d` do teorema anterior é o mesmo d_n, sem novo parâmetro livre. A convergência de j(c_n) é a versão final do módulo9, não a variante de diagnóstico.
- Linha `{ln('scalarFixedPairing_of_squarePairing')}`: passa-se ao conjunto fechado {{v | ⟨v,y⟩=⟨z,v⟩}} e usa-se explicitamente `scalarRightSelfadjointVectors_closure`. A igualdade desse fecho com Fix F é um resultado herdado de `ScalarRightGraphCore.lean:50`, com F=`scalarTomitaAdjoint P` ORIGINAL. Não se substitui densidade em Fix F por mera densidade Hilbert de j(E), nem se presume que o conjunto de pareamento seja subespaço complexo.
- Linhas `{ln('pairingViaFixedDecomposition')}`–`{ln('scalarClosedTomita_of_squarePairing')}`: a decomposição compilada `domain_fixed_decomposition` dá x=h+ik e Fx=h−ik, com h,k∈Fix F. A conjugação na primeira entrada do produto interno é essencial: o sinal de −ik na esquerda vira +i. Assim os testes dão ⟨Fx,y⟩=⟨z,x⟩ para TODO x∈D(F). As hipóteses genéricas de preservação do domínio e involução são descarregadas por `scalarTomitaAdjoint_maps_domain` e `scalarTomitaAdjoint_involutive`. `scalarClosedTomita_bidual_maximal` conclui y∈D(S), Sy=z para o S original, sem postular a conclusão como campo.
- Linha `{ln('scalarClosedTomita_squarePairing_iff')}`: o sentido inverso usa o pareamento bidual já provado e a pertinência efetiva de j(b²) a D(F), fornecida por `scalarRightPairVector_original_adjoint`. Como b=b*, b² é auto-adjunto e F j(b²)=j(b²). O wrapper semilinear trabalha no Hilbert/subálgebra abstratos; suas hipóteses são satisfeitas separadamente por refine no P concreto. Não há troca de S, F, J ou domínio.
- Linhas `{ln('boundedActionSquarePairing')}`–`{ln('scalarClosedTomita_of_boundedPairAction')}`: K é dado como CLM limitado em TODO H_I. As DUAS hipóteses, K j(a)=a.val y e K* j(a)=a.val z, valem para TODO a∈E e permanecem explícitas. Para a=a*, auto-adjunticidade de a.val e a identidade de adjunto de K produzem o teste sobre j(a²)=a.val j(a). Isso coloca (y,z) no grafo do S original. O teorema não constrói K nem demonstra essas duas ações para um candidato futuro. Não exige continuidade do operador não limitado S/F ou continuidade geral de star na SOT.

Os testes são complexos, sem substituir igualdade por igualdade apenas da parte real. O critério público caracteriza exatamente o grafo de S por testes nos quadrados auto-adjuntos. Não pressupõe densidade dos quadrados como hipótese nova, e não afirma que o cone positivo sozinho seja denso em todo H. O P, o mapa j, E e H_I são os mesmos herdados; não se identifica I com nν nem D(S) com uma imagem algébrica.

**Recompilação e auditoria próprias concluídas:**

| Execução desta ampliação | rc | segundos |
|---|---:|---:|
| ScalarSquareAdjointTest AUTORAL FINAL, arquivo completo5 | {new['returncode']} | {new['seconds']} |
| Auditor20, tipos com universos + axiomas | {audit['returncode']} | {audit['seconds']} |

Os vinte nomes e mapas de axiomas coincidem exatamente com o manifesto e com os três stdouts finais autorais: somente `propext`, `Classical.choice`, `Quot.sound`. Os dez auxiliares privados do terceiro estão cobertos transitivamente; a fonte não contém sorry/admit/axiom novo/unsafe ou alteração de redutibilidade. O novo .olean próprio é byte a byte igual ao autoral. Os primeiros dois módulos conservam suas recompilações próprias anteriores e binários conferidos; não foram recompilados nesta ampliação.

**Pins cumulativos, relidos dos bytes (fonte e .olean próprio=autoral):**

| Módulo | SHA256 fonte | SHA256 .olean |
|---|---|---|
{tables}

- Log aceito do terceiro: `{Path(third['author_log']).name}`, SHA `{third['author_log_sha256']}`.
- Stdout final autoral do terceiro: `{third['author_stdout_sha256']}`; stderr vazio.
- `square_resolvent_draft_status.json`: `{m['draft_sha256']}`.
- `RELATORIO_RESOLVENTES_QUADRADOS_TESTE_ORIGINAL_DEV.md`: `{m['report_sha256']}`.
- Auditor20 próprio .olean: `{audit['output_sha256']}`.
- `compilation.json` próprio: `{hf(RUN/'compilation.json')}`.

Evidências em `{RUN.relative_to(ROOT)}/`: manifesto próprio, fontes congeladas, registros de compilação, captura dos tipos/axiomas, stdouts e histórico. {len(m['dependencies'])} dependências de projeto foram reutilizadas com hashes preservados; origens próprias imediatas: `square_approximation_independent_20260913_052356_708074`, `bidual_support_final_independent_20260913_042239_895782` e `right_graph_core_final_independent_20260913_021030_429982`, além da proveniência transitiva registrada. A pasta de diagnóstico forneceu somente cópias dessas dependências, NUNCA o binário experimental do terceiro. LEAN_PATH: uma raiz própria de projeto e oito pacotes externos readonly; {len(m['external_direct_pins'])} pins externos diretos relidos. Sem build autoral na resolução de imports, sem reconstruir dependências/biblioteca e sem repetir auditoria binária integral da Mathlib.

**Histórico autoral do terceiro recusado:** {failure_names}. São exatamente cinco rc1, confrontados com o manifesto e preservados com seus streams. Incluem erros de posição docstring/set_option e timeouts de elaboração. A quinta falha foi localizada no obtain de `original_adjoint`, não na composição hf.trans seguinte. Nenhum print parcialmente verde ou com sorryAx dessas execuções conta como prova. Somadas às anteriores, são 1+8+5=14 tentativas autorais rc1 excluídas deste pacote.

**Separação do diagnóstico e autoria.** O probe próprio `SubalgebraBridgeV1` sobre o backup da quarta tentativa passou cinco alvos a 600000 locais ({diag['seconds']} s); conservava F:D→H. Ele não certificava a versão autoral posterior nem passagem a 200000. A fonte agora aceita é a autoral, com wrappers de subálgebra e F SEMILINEAR, recompilada a 200000 nesta chamada. [DECLARADO pelo agente principal] Essa variante foi criada antes da leitura do patch do revisor e não foi copiada dele. A remoção isolada das classes e a ponte concreta por rfl falharam no histórico; a causa interna única do gargalo não foi demonstrada. As falhas próprias de preparação diagnóstica também não são evidência matemática e permaneceram separadas da execução final verde.

**Documento e preparação, somente leitura.** O relatório DEV foi lido integralmente: distingue o critério provado de sua aplicação futura aos blocos, que ainda exige as duas ações, cota inferior e multiplicador limitado. Os gráficos mencionados na rota posterior são explicitamente objetos distintos; não se promove a consulta a prova. `prepare_square_resolvent_stage.py` (SHA `{m['prepare_helper_sha256']}`) exige --review-read, marcador, os TRÊS pares de hashes no parecer, manifesto3/20 e pins de fontes/binários/mãe; portanto o estrato15 sozinho não satisfazia sua guarda. Foi apenas inspecionado, não executado; essa leitura não equivale a revisão de integração ou execução de custódia.

**Cinco novos alvos auditados:**

{targets}

**Conclusão e fronteira.** DEV20 completo, sem análise necessária pendente neste escopo e sem P0–P2. Mãe `bidual_right_support_custody.json`, SHA `{m['parent_custody_sha256']}`, cópia/gate e arquivos pinados permaneceram iguais durante a execução. Nenhuma escrita em fontes, originais, integração ou memórias; não houve execução de monólito, helper autoral, recorder, integrador ou controle autoral. As 34 memórias não foram reauditadas integralmente nesta rodada. Não há aceite integrado. Permanecem fora desta conclusão: aplicação aos pares ponderados/candidato dos blocos, multiplicador limitado correspondente, inclusão inversa por J, identificação Δ^it/KMS, traço, flags maiores, contrato de consumo e runtime integral. O teste agora provado é uma ponte concreta para essas obrigações, não sua quitação automática.
'''
graph_lines=Path(m['dependencies']['TGLV350.ScalarRightGraphCore']['frozen_source']).read_text(encoding='utf-8').splitlines()
graph_line=next(i+1 for i,l in enumerate(graph_lines) if l.startswith('theorem scalarRightSelfadjointVectors_closure'))
text=text.replace('ScalarRightGraphCore.lean:50',f'ScalarRightGraphCore.lean:{graph_line}')
b=text.encode();backup=report.with_name(report.name+'.bak_'+suffix)
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old
tmp=report.with_name(report.name+'.tmp_'+suffix)
with tmp.open('xb') as f:f.write(old+b)
assert tmp.read_bytes()==old+b and tmp.stat().st_size>len(old)
os.replace(tmp,report);assert report.read_bytes().startswith(old)
pin={'timestamp':stamp,'report':str(report),'report_sha256':hf(report),'backup':str(backup),'backup_sha256':hf(backup),'preserved_prefix_bytes':len(old),'size':report.stat().st_size,'marker':'SQUARE_RESOLVENT_DEV_REVIEW','scope':'FINAL_DEV20_ONLY','findings':[],'compilation_sha256':hf(RUN/'compilation.json')}
p=RUN/'review_pin.json';t=p.with_suffix('.json.tmp');assert not p.exists();t.write_bytes((json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode());os.replace(t,p)
print(json.dumps(pin,ensure_ascii=False))
