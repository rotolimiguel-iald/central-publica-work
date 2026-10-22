from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_vna_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
v=load(RUN/'verification.json');s=load(RUN/'static_verification.json')
assert v['complete'] and not v['P0'] and not v['P1'] and not v['P2']
assert v['all_source_binary_log_stream_pins_match'] and v['audit_all_allowed'] and v['current_Audit_global_hashes_verified']
assert all(hf(ROOT/n)==h for n,h in v['artifact_pins'].items())
assert all(hf(p)==h for p,h in s['surface_pins'].items())
assert hf(ROOT/'um.py')==v['working_sha256']
assert hf(REV/'REVIEW_SCALAR_VNA_DEV.md')==v['own_DEV_review_sha256']
assert not any((ROOT/n).exists() for n in v['new_custody_report_verification_absent'])
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
logs='\n'.join(f'| {x["file"]} | `{x["log_name"]}` | `{x["log_sha256"]}` |' for x in v['new_records'])
artifacts='\n'.join(f'- `{n}`: `{v["artifact_pins"][n]}`.' for n in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json'])
ar=v['final_Audit_record'];stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''

---

{date} — **SCALAR_VNA_INTEGRATED_REVIEW**

[REAL — conferência integrada final concluída] **Nenhum P0, P1 ou P2.** O estrato preliminar acima está preservado; as pendências de evidência nele listadas foram resolvidas nesta leitura. Escopo: quatro módulos/27 alvos já recompilados e revisados no DEV, sua transposição, duas raízes, registros integrados, controles e helpers. Nenhuma recompilação foi repetida nesta rodada.

| Evidência | Resultado conferido | Origem |
|---|---|---|
| Fontes embutidas | **903**; quatro novas, somente imports reescritos; apenas as duas raízes mudaram entre as fontes antigas | Comparação própria de bytes/AST com backup da mãe |
| Compilações integradas | **201 rc0 = 195 registros idênticos à mãe + 6 novos** (4 módulos + TGLExt + Audit) | Execuções autorais; releitura própria de todos os pares fonte/binário, logs e streams |
| Novos alvos | **27**, com os mesmos axiomas do auditor DEV próprio | Prints integrados e mapa atual reparsados |
| Audit completo | **6.982 = 6.955 anteriores preservados + 27 novos**, somente trio lógico permitido | Stdout atual → mapa, confrontado com fonte Audit e evidence |
| Controles | **101/101**, os 100 anteriores preservados e um grupo novo | Resultados autorais relidos, sem reexecutar os testes |
| Memórias | **34** hashes ainda iguais à mãe | Leitura própria; nenhum recorder executado por esta revisão |

Os seis registros novos têm `returncode = lean_returncode = 0`, fonte inalterada durante compilação, binário existente com SHA correto, stderr vazio e nenhum warning. As dependências diretas de projeto desses seis foram relidas e seu frescor conferido; os 195 registros herdados coincidem integralmente com os anteriores, inclusive hashes de fonte, binário, log e streams. Pacotes externos e a cadeia matemática herdada não foram reconstruídos.

| Fonte integrada/raiz | Log autoral final | SHA256 do log lido |
|---|---|---|
{logs}

Audit corrente: **{ar['stdout_bytes']} bytes**, SHA256 `{ar['stdout_sha256']}`; binário `{ar['binary_sha256']}`. `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com esses bytes atuais e apontam para o log Audit acima. `historical_v350_audit_metadata` mantém os hashes da base, sem tratá-los como stream corrente. O mapa reparsado preserva todos os axiomas anteriores e coincide exatamente com `axiom_report`; os 27 novos coincidem com o auditor próprio DEV. Os quatro auxiliares privados do último módulo permanecem cobertos transitivamente.

Controle novo: `{v['added_controls'][0]}`. Confirmada sua exigência de sete nomes-chave presentes, seis flags maiores falsas, gate legado inalterado e `full_plan_complete = false`. `legacy_gate` e todo `frontier` coincidem com a mãe. O rótulo herdado `{v['scope']}` conserva seu alcance de torre-produto; não certifica a inclusão inversa para o J do peso escalar. Nenhuma promoção por este lote.

Helpers relidos estaticamente e pinados: `make_scalar_vna_helpers.py`, `record_scalar_vna_draft.py`, `prepare_scalar_vna_stage.py`, `record_scalar_vna_progress.py`, `verify_scalar_vna_custody.py`. Os diffs efetivos do integrador/compilador/teste correspondem às adições previstas. O recorder exige revisão DEV/integrada lida, mãe, original/cópia, AST externo, pares fonte/binário, transposição, Audit atual/histórico e 34 pins antes de registrar. A gravação prevista usa backup de bytes, prefixo append e troca por temporário; o verifier relê pares e backups. **Esta é inspeção prévia da lógica: recorder, novo relatório autoral integrado e nova custódia ainda não existiam/executaram na evidência conferida.** Não se afirma verificação de uma gravação futura.

[REAL — hashes relidos] Cópia `{v['working_sha256']}`. Original e base `{v['original_sha256']}`. Mãe `right_vector_custody.json`: `{v['parent_custody_sha256']}`. AST Python fora do embutido idêntico ao backup da mãe e `gate_extension.py` byte a byte preservado. As seis flags continuam falsas; `full_runtime = false`. O parecer DEV selado foi relido por hash e não modificado.

Pins finais:

{artifacts}

{link('Verificação própria completa',RUN/'verification.json')} — SHA256 `{hf(RUN/'verification.json')}`. Contém os 201 pares, seis logs novos, dependências diretas, streams, controles e pins. {link('Mapa Audit reparsado',RUN/'axioms.json')}; {link('axiomas dos quatro módulos integrados',RUN/'new_module_axioms.json')}; {link('auditor DEV reutilizado',RUN/'own_DEV_axioms.json')}. As recompilações próprias pertencem ao {link('parecer DEV preservado',REV/'REVIEW_SCALAR_VNA_DEV.md')}; nesta integração houve **zero execuções Lean/testes autorais/monólito/helpers** pelo revisor e zero escrita em memórias.

Alcance confirmado: π(N) igual ao próprio bicomutante no mesmo H_I, mediante levantamento limitado e transporte pela unitária linear V gaussiana. V não substitui J. **Continuam abertos** graph-core de F pela álgebra de pares, reconstrução `R=Jπ(b)J`, inclusão inversa com J original, identificação de Δ^it/KMS, traço/Three Locks, consumo tipado e runtime. Consulta por blocos preservada como proposta. Nenhuma pendência resta na revisão integrada delimitada destes quatro módulos/27 alvos.
'''
p=REV/'REVIEW_SCALAR_VNA_INTEGRATED.md';before=p.read_bytes()
assert b'SCALAR_VNA_INTEGRATED_REVIEW' not in before
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(before)
assert bak.read_bytes()==before
raw=before+text.encode();tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==before
os.replace(tmp,p);assert p.read_bytes()==raw and raw.startswith(bak.read_bytes())
pin={'timestamp':date,'report':str(p),'report_sha256':hf(p),'report_bytes':len(raw),'backup':str(bak),'backup_sha256':hf(bak),'prefix_bytes':len(before),'verification_sha256':hf(RUN/'verification.json'),'scope':'INTEGRATED_FOUR_MODULES_27_TARGETS','P0':[],'P1':[],'P2':[],'memory_written':False,'author_programs_executed':False}
q=RUN/'final_review_pin.json';assert not q.exists();qb=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(qb)
assert qt.read_bytes()==qb;os.replace(qt,q)
print(json.dumps(pin,ensure_ascii=False))
