from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'phase_variational_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
v=load(RUN/'verification.json');s=load(RUN/'static_verification.json')
assert v['complete'] and not any(v[k] for k in ['P0','P1','P2'])
assert all(hf(ROOT/n)==h for n,h in v['artifact_pins'].items())
assert hf(ROOT/'um.py')==v['working_sha256']
assert all(hf(p)==h for p,h in s['surface_pins'].items())
assert hf(REV/'REVIEW_PHASE_VARIATIONAL_DEV.md')==v['own_DEV_review_sha256']
assert not any((ROOT/n).exists() for n in v['new_custody_report_verification_absent'])
assert len(v['new_records'])==4 and all(not r['warnings'] and not r['stderr_bytes'] for r in v['new_records'])
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
link=lambda label,p:f'[{label}](<{Path(p).as_posix()}>)'
table='\n'.join(f"| {r['file']} | `{r['source_sha256']}` | `{r['binary_sha256']}` |" for r in v['new_records'])
logs='\n'.join(f"- `{r['log_name']}` — SHA `{r['log_sha256']}`." for r in v['new_records'])
a=v['final_Audit_record']
text=f'''

---

## Adendo integrado final — seleção variacional e grafo original

{date} — **PHASE_VARIATIONAL_INTEGRATED_REVIEW**

[REAL — conferência própria dos artefatos finais.] **Sem P0, P1 ou P2 neste incremento de dois módulos/21 alvos. Escopo integrado encerrado.** O estrato preliminar permanece integralmente como prefixo, com backup imediato de bytes. O aviso final foi seguido de releitura dos registros, sem executar Lean, testes ou programas autorais.

| Evidência medida | Resultado e alcance |
|---|---|
| Build integrado autoral | **211 registros rc0 =207 exatamente herdados +4 novos**, dois módulos e duas raízes. Não são211 novas execuções. |
| Conferência própria |211 fontes/binários/logs/stdout/stderr relidos; hashes e embutidos correspondentes. Os207 registros e seus pins coincidem com a mãe. Imports diretos dos quatro alterados com fontes/binários pinados e frescor conferido. |
| Audit atual | **7077 distintos =7056 preservados +21**, com mapas de axiomas anteriores preservados e os novos iguais ao auditor DEV próprio; somente propext/Classical.choice/Quot.sound. |
| Testes autorais relidos | **104/104**; os103 anteriores preservados e um grupo novo, sem reexecução pelo revisor. |
| Transposição | **913 embutidos**, somente dois novos; entre os antigos, apenas as duas raízes mudaram. DEV→TGLExt literal, exclusivamente prefixo dos imports. |
| AST/gate/memórias | AST Python fora do dicionário Lean idêntico à mãe; gate_extension.py idêntico; seis flags falsas; **34 superfícies ainda iguais aos pins maternos**, antes do append autoral. |

Cópia atual: `{v['working_sha256']}`. Original canônico e base relidos somente por hash: `{v['original_sha256']}`. Mãe matemática/documental única adjoint_polar_graph_custody.json: `{v['parent_custody_sha256']}`. Parecer DEV preservado: `{v['own_DEV_review_sha256']}`.

| Arquivo integrado | SHA256 fonte | SHA256 .olean relido |
|---|---|---|
{table}

Quatro logs finais conferidos, rc0/fonte inalterada, sem warning e stderr vazio:

{logs}

Audit corrente: `{a['log_name'].replace('.json','.stdout.txt')}`, **{a['stdout_bytes']} bytes**, SHA `{a['stdout_sha256']}`. O stream foi integralmente reparseado e confrontado com axiom_report, os21 alvos próprios e os7056 anteriores. `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com os bytes atuais; `audit_hash_scope` permanece CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES. `historical_v350_audit_metadata` preserva separadamente os valores antigos; não foi usado como hash do stream atual. As multiplicidades anteriores dos prints na fonte de Audit também permanecem.

O novo controle é `original_phase_variational_graph_does_not_discharge_KMS_trace_or_physical_frontier`: verifica os cinco nomes representativos previstos, as seis flags falsas e ausência de mudança de gate/full-plan. A cobertura dos21 nomes e axiomas vem adicionalmente da conferência própria integral do Audit e dos dois streams dos módulos. Gate legado e objeto frontier coincidem com os maternos. A fiação permanece formal/physics/experiment, obtidos de qgc_/qgp_/feed; as seis flags qgf/gpf não são entradas diretas desse avaliador e kernel_frontier é anexado depois. O rótulo herdado `{v['scope']}` não é prova da inclusão inversa desta construção.

**Helpers e custódia futura:** prepare_phase_variational_stage.py, record_phase_variational_progress.py e verify_phase_variational_custody.py foram lidos integralmente e inspecionados estaticamente. Diffs aplicados: dois módulos, batch699→720, ordem antes das raízes e um novo grupo de controle; lógica dos hashes Audit corrente/histórico inalterada. Recorder exige leitura dos pareceres DEV/integrado, pins da mãe, transposição e pares fonte/binário rc0, Audit/metadados e os34 pins antes de escrever. Prevê backup imediato de bytes e append com temporário/troca. Verifier relê todos os pares fonte/binário registrados e backups/prefixos. A atomicidade é por arquivo, sem transação conjunta das34 superfícies. A minuta mantém os domínios e as obrigações abertas corretamente.

**Recorder/verifier novos, atualização das memórias e nova custódia ainda não executados neste snapshot:** phase_variational_custody.json, sua verificação e o relatório integrado autoral estavam ausentes ao fechar a leitura. Esta revisão não declara esses atos realizados. O preparador/integrador e build/testes são atos autorais cuja evidência foi inspecionada; o revisor não os executou.

**Alcance matemático herdado:** o DEV próprio recompilou os dois módulos em estratos sucessivos e executou auditor21 separado, com tipos/universos e axiomas conferidos. A transposição conserva a seleção real-linear contínua em Fix S original, sua unicidade/cota e, para ξ∈Fix F e TODO u∈D(S), a identidade **2⟨ξ,Su⟩=z⟨η,Su⟩+conj(z)⟨u,η⟩**, Re(z)>0. Não supõe simetria da forma nem continuidade de S. Nesta rodada integrada não houve recompilação própria: fontes/termos transpostos e evidências autorais foram confrontados com o DEV já reproduzido. Binários integrados são pinados aos seus próprios logs; a mudança de nome do módulo não exige igualdade de .olean DEV→TGLExt.

[OPEN] Pertinência dos pares ponderados a D(S), (V)/(P), cota inferior do bloco e multiplicador limitado, inclusão inversa pelo J original, identificação Δ^it/KMS, traço e consumo por certificados/gate/runtime. O CLM da seleção não é o multiplicador associado ao vetor. As consultas CFC/quadrados permanecem DERIVED e fora dos21. Nenhuma promoção de gate, full-plan ou seis flags.

{link('Verificação própria completa/pins',RUN/'verification.json')} — SHA `{hf(RUN/'verification.json')}`; {link('Audit reparseado',RUN/'axioms.json')}; {link('21 alvos integrados',RUN/'new_module_axioms.json')}; {link('inspeção estática e helpers',RUN/'static_verification.json')}. Recompilação matemática própria herdada do DEV; build/testes integrados autorais relidos; hashes, AST, transposição e mapas são conferências próprias. Fontes, monólito, originais, memórias e pareceres DEV/anteriores não foram alterados. **Nenhuma verificação necessária deste escopo integrado permanece pendente.**
'''
p=REV/'REVIEW_PHASE_VARIATIONAL_INTEGRATED.md';old=p.read_bytes()
assert hf(p)==load(RUN/'preliminary_report_pin.json')['report_sha256']
assert b'PHASE_VARIATIONAL_INTEGRATED_REVIEW' not in old
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(old)
assert bak.read_bytes()==old
raw=old+text.encode();tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==old
os.replace(tmp,p);assert p.read_bytes()==raw and raw.startswith(bak.read_bytes())
pin={'timestamp':date,'report':str(p),'report_sha256':hf(p),'backup':str(bak),'backup_sha256':hf(bak),'prefix_bytes':len(old),'marker':'PHASE_VARIATIONAL_INTEGRATED_REVIEW','complete':True,'P0':[],'P1':[],'P2':[],'verification_sha256':hf(RUN/'verification.json')}
q=RUN/'final_report_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q);assert q.read_bytes()==b
print(json.dumps(pin,ensure_ascii=False))
