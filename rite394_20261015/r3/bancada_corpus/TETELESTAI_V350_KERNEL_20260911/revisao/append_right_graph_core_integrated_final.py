from pathlib import Path
import datetime, hashlib, json, os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV / 'right_graph_core_integrated_latest_run.txt').read_text().strip())
hf = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_bytes())
v = load(RUN / 'verification.json')
s = load(RUN / 'static_verification.json')
assert v['complete'] and not any(v[k] for k in ('P0', 'P1', 'P2'))
assert v['all_source_binary_log_stream_pins_match'] and v['audit_all_allowed']
assert v['current_Audit_global_hashes_verified']
assert all(hf(ROOT / n) == h for n, h in v['artifact_pins'].items())
assert all(hf(p) == h for p, h in s['surface_pins'].items())
assert hf(ROOT / 'um.py') == v['working_sha256']
assert hf(REV / 'REVIEW_RIGHT_GRAPH_CORE_DEV.md') == v['own_DEV_review_sha256']
assert not any((ROOT / n).exists() for n in v['new_custody_report_verification_absent'])
assert all(not r['warnings'] and r['stderr_bytes'] == 0 for r in v['new_records'])

def link(label, p):
    return f'[{label}](<{Path(p).as_posix()}>)'

logs = '\n'.join(f'| {x["file"]} | `{x["log_name"]}` |' for x in v['new_records'])
artifacts = '\n'.join(f'- `{n}`: `{v["artifact_pins"][n]}`.' for n in ['integration.json', 'integrated_compile.json', 'gate_tests.json', 'kernel_incremental_evidence.json'])
a = v['final_Audit_record']
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
date = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text = f'''

---

{date} — **RIGHT_GRAPH_CORE_INTEGRATED_REVIEW**

[REAL — inspeção integrada concluída] **Nenhum achado P0, P1 ou P2.** As pendências do estrato preliminar foram resolvidas pela leitura dos artefatos finais. Escopo: seis módulos/57 alvos do DEV preservado, transposição, duas raízes, evidências e helpers. As recompilações independentes são as documentadas no DEV; nesta rodada não houve execução Lean nem de programas autorais.

| Evidência conferida | Resultado | Proveniência |
|---|---|---|
| Embutidos | **909**; seis adições, somente imports reescritos; entre os antigos, apenas duas raízes alteradas | Comparação própria de bytes/AST com a mãe |
| Registros Lean | **207 rc0 = 199 herdados idênticos + 8 novos** (seis módulos + duas raízes) | Compilações autorais; fonte/binário/log/streams relidos pelo revisor |
| Alvos novos | **57**, tipos preservados pela transposição literal e axiomas iguais ao auditor DEV próprio | Fontes, prints integrados e auditor próprio anterior |
| Audit corrente | **7.039 = 6.982 preservados +57**, apenas `propext`, `Classical.choice`, `Quot.sound` | Mapa reparsado do stdout atual, igual ao `axiom_report` |
| Controles | **102/102**, preservados os 101 anteriores e acrescido um grupo | Resultados autorais inspecionados, sem reexecução |
| Memórias | **34 hashes iguais à mãe** | Leitura própria, nenhuma escrita |

Os oito registros novos têm `returncode = lean_returncode = 0`, fonte inalterada durante a compilação, binário pinado, stderr vazio e nenhum warning. Dependências diretas de projeto e frescor foram conferidos. Os 199 herdados mantêm os mesmos registros e hashes de fonte, binário, log e streams. A biblioteca e a cadeia herdada não foram reconstruídas; a evidência própria de tipos/universos e axiomas continua no DEV6/57.

| Fonte/raiz | Log autoral final, relido e pinado |
|---|---|
{logs}

Audit atual: **{a['stdout_bytes']} bytes**, SHA256 `{a['stdout_sha256']}`; log SHA256 `{a['log_sha256']}`. Os dois campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com os bytes atuais, sob `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`. Os valores de `historical_v350_audit_metadata` permanecem iguais aos da mãe e não foram usados como stream atual. Nomes, axiomas e multiplicidades anteriores foram preservados; o acréscimo é exatamente o manifesto57, incluindo cobertura transitiva dos auxiliares privados.

Controle novo: `{v['added_controls'][0]}`. Sua lógica exige nove nomes-chave, as seis flags maiores falsas e ausência de promoção do gate/full-plan. AST Python fora do dicionário Lean e `gate_extension.py` permanecem iguais à mãe. `legacy_gate` e `frontier` também são idênticos. O rótulo herdado `{v['scope']}` continua referido à torre-produto; não certifica a inclusão inversa pelo J original do peso. As entradas diretas do avaliador legado e o anexo `kernel_frontier` continuam distintos.

Os cinco helpers `make/record_draft/prepare_stage/record_progress/verify_custody` de `right_graph_core` foram lidos estaticamente e seus pins finais reconferidos. O recorder exige leitura dos pareceres, mãe e pins antes dos 34 backups imediatos de bytes, append e troca por temporário; o verifier relê pares fonte/binário e backups/prefixos. Os diffs efetivos do integrador/compilador/teste correspondem às adições previstas. **Isto verifica a lógica prévia à gravação:** nova custódia, verificação e relatório integrado autoral estavam ausentes; nenhuma execução futura desses scripts está certificada aqui.

[REAL — hashes lidos] Cópia `{v['working_sha256']}`; original e base `{v['original_sha256']}`; mãe `scalar_vna_custody.json`, `{v['parent_custody_sha256']}`. DEV selado e pareceres maternos preservados.

{artifacts}

{link('Verificação própria completa', RUN / 'verification.json')} — SHA256 `{hf(RUN / 'verification.json')}`: contém os 207 pares, logs, streams, dependências, controles e pins. {link('Audit reparsado', RUN / 'axioms.json')}; {link('57 alvos integrados por módulo', RUN / 'new_module_axioms.json')}; {link('auditor DEV reutilizado', RUN / 'own_DEV_axioms.json')}; {link('parecer DEV imutável', REV / 'REVIEW_RIGHT_GRAPH_CORE_DEV.md')}.

Alcance confirmado pela transposição: **o fecho do grafo dos pares direitos é o gráfico de F original, no mesmo H_I**, com densidade real dos auto-adjuntos em Fix F. Não se afirma igualdade algébrica de domínios, continuidade de F, troca de J ou igualdade I=nν. [OPEN] Reconstrução `R=Jπ(b)J`, inclusão inversa dos comutantes pelo J original, identificação de Δ^it/KMS, traço, consumo das obrigações físicas e runtime não decorrem deste lote. As seis flags e `full_plan_complete` permanecem falsas. **Não resta pendência nesta revisão integrada delimitada.**
'''
p = REV / 'REVIEW_RIGHT_GRAPH_CORE_INTEGRATED.md'
before = p.read_bytes()
assert b'RIGHT_GRAPH_CORE_INTEGRATED_REVIEW' not in before
bak = p.with_name(p.name + '.bak_' + stamp)
with bak.open('xb') as f:
    f.write(before)
assert bak.read_bytes() == before
raw = before + text.encode()
tmp = p.with_name(p.name + '.tmp_' + stamp)
with tmp.open('xb') as f:
    f.write(raw)
assert tmp.read_bytes() == raw and p.read_bytes() == before
os.replace(tmp, p)
assert p.read_bytes() == raw and raw.startswith(bak.read_bytes())
pin = {'timestamp': date, 'report': str(p), 'report_sha256': hf(p), 'report_bytes': len(raw), 'backup': str(bak), 'backup_sha256': hf(bak), 'prefix_bytes': len(before), 'verification_sha256': hf(RUN / 'verification.json'), 'scope': 'INTEGRATED_SIX_MODULES_57_TARGETS', 'P0': [], 'P1': [], 'P2': [], 'memory_written': False, 'author_programs_executed': False}
q = RUN / 'final_review_pin.json'
assert not q.exists()
qb = (json.dumps(pin, ensure_ascii=False, indent=2) + '\n').encode()
qt = q.with_name(q.name + '.tmp')
with qt.open('xb') as f:
    f.write(qb)
assert qt.read_bytes() == qb
os.replace(qt, q)
print(json.dumps(pin, ensure_ascii=False))
