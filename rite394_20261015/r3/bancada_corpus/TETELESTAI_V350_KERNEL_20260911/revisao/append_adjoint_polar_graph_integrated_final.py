from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'adjoint_polar_graph_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
v=load(RUN/'verification.json');s=load(RUN/'static_verification.json')
assert v['complete'] and not any(v[k] for k in ['P0','P1','P2'])
assert all(hf(ROOT/n)==h for n,h in v['artifact_pins'].items())
assert hf(ROOT/'um.py')==v['working_sha256']
assert all(hf(p)==h for p,h in s['surface_pins'].items())
assert hf(REV/'REVIEW_ADJOINT_POLAR_GRAPH_DEV.md')==v['own_DEV_review_sha256']
assert not any((ROOT/n).exists() for n in v['new_custody_report_verification_absent'])
assert len(v['new_records'])==4 and all(not r['warnings'] and not r['stderr_bytes'] for r in v['new_records'])
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
table='\n'.join(f"| {r['file']} | `{r['source_sha256']}` | `{r['binary_sha256']}` |" for r in v['new_records'])
logs='\n'.join(f"- `{r['log_name']}` — SHA `{r['log_sha256']}`." for r in v['new_records'])
a=v['final_Audit_record']
text=f'''

---

{date} — **ADJOINT_POLAR_GRAPH_INTEGRATED_REVIEW**

[REAL — conferência integrada concluída] **Sem P0, P1 ou P2 neste incremento de dois módulos/17 alvos.** O estrato preliminar permanece integralmente como prefixo, com backup imediato de bytes. O aviso final foi seguido de releitura própria dos arquivos, sem nova execução Lean ou de programas autorais.

| Evidência medida | Resultado e alcance |
|---|---|
| Compilação integrada autoral | **209 registros rc0: 205 exatamente herdados +4 novos** (dois módulos e duas raízes). Não são 209 novas execuções. |
| Conferência própria dos registros | 209 fontes/binários/logs/streams relidos; hashes correspondentes e fontes embutidas iguais. Os 205 registros e pins coincidem com o estrato materno. Novos imports diretos com fontes/binários pinados e frescor conferido. |
| Audit atual reparseado | **7.056 distintos =7.039 preservados +17 próprios**, mesmos mapas anteriores e multiplicidades da fonte preservadas; somente `propext`, `Classical.choice`, `Quot.sound`. |
| Controles executados pelo autor | **103/103**, preservando os 102 anteriores; um grupo novo verifica os sete nomes indicados, seis flags falsas e ausência de promoção de gate/full-plan. Resultados relidos, não reexecutados pelo revisor. |
| Transposição e embutidos | **911 arquivos**; exatamente dois novos. Os dois DEV coincidem com snapshots/binários próprios revisados; TGLExt difere apenas no prefixo mecânico dos imports. Só as duas raízes mudaram entre os embutidos antigos. |
| AST/gate/memórias | AST Python fora do dicionário Lean igual à mãe, `gate_extension.py` byte a byte igual; seis flags falsas; **34 superfícies ainda iguais à mãe**, antes do append autoral. |

Cópia atual: `{v['working_sha256']}`. Original canônico e base relidos somente por hash: `{v['original_sha256']}`. Mãe matemática e documental única `right_graph_core_custody.json`: `{v['parent_custody_sha256']}`. Parecer DEV preservado: `{v['own_DEV_review_sha256']}`.

| Arquivo integrado | SHA256 fonte | SHA256 .olean relido |
|---|---|---|
{table}

Logs novos efetivamente conferidos, todos rc0/fonte inalterada, sem warning e stderr vazio:

{logs}

O stream atual é `{a['log_name'].replace('.json','.stdout.txt')}`, **{a['stdout_bytes']} bytes**, SHA `{a['stdout_sha256']}`. Foi reparseado integralmente e confrontado com `axiom_report`, os 17 alvos do auditor DEV próprio e os 7.039 anteriores. `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com esses bytes atuais; `audit_hash_scope` declara o stream incremental atual. Os valores antigos continuam separados em `historical_v350_audit_metadata`, sem serem tratados como hashes atuais.

Os cinco helpers foram lidos, sem execução pelo revisor. Os diffs aplicados acrescentam somente os dois módulos, batch682→699, ordem antes das raízes e um grupo de controle. Recorder exige leitura DEV/integrada, pins maternos, transposição, rc0 e pares fonte/binário, Audit/metadados e os 34 pins antes de escrever; usa backup imediato de bytes e append por troca temporária. Verifier relê os pares e os backups/prefixos. A atomicidade é por arquivo. **Recorder/verifier novos e append das memórias ainda não foram executados**: os artefatos de custódia, verificação e relatório integrado autoral estavam ausentes ao fechar esta leitura. O texto futuro foi avaliado como minuta, sem atribuir execução ou nova custódia.

O escopo matemático é herdado da recompilação independente DEV2/17 e da captura própria de tipos/universos/axiomas: F=BJ=JSJ nos domínios originais, J×J homeomorfismo e closure range(a↦(Jj(a),Jj(a*)))=graph S, no mesmo H_I. A literalidade da transposição e os prints integrados preservam esse escopo. **Não houve recompilação independente da integração nesta rodada**, nem rebuild das dependências herdadas; houve conferência própria das evidências autorais e dos bytes contra o DEV já reproduzido.

[OPEN] Inclusão inversa JRJ∈π(N), estimativa dos quadrados, identificação Δ^it/KMS, traço, Three Locks, consumo físico/por certificados e runtime integral. A inscrição conjugado-linear não foi apresentada como identificação de álgebras. O rótulo herdado de escopo `{v['scope']}` pertence à fronteira PRODUCT_TOWER e não prova a igualdade global dos comutantes nesta construção. Gate legado, full-plan e seis flags permanecem inalterados; não houve promoção.

{link('Verificação própria completa/pins',RUN/'verification.json')} — SHA `{hf(RUN/'verification.json')}`; {link('mapa Audit reparseado',RUN/'axioms.json')}; {link('17 alvos integrados',RUN/'new_module_axioms.json')}; {link('inspeção estática e helpers',RUN/'static_verification.json')}. Evidências de build/testes são autorais relidas; hashes, comparação AST/transposição, mapas e preservação de pins são conferências próprias. Originais, fontes, monólito, memórias e pareceres DEV/anteriores não foram alterados. **Escopo integrado encerrado.**
'''
p=REV/'REVIEW_ADJOINT_POLAR_GRAPH_INTEGRATED.md';old=p.read_bytes()
assert hf(p)==load(RUN/'preliminary_report_pin.json')['report_sha256']
assert b'ADJOINT_POLAR_GRAPH_INTEGRATED_REVIEW' not in old
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(old)
assert bak.read_bytes()==old
raw=old+text.encode();tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==old
os.replace(tmp,p);assert p.read_bytes()==raw and raw.startswith(bak.read_bytes())
pin={'timestamp':date,'report':str(p),'report_sha256':hf(p),'backup':str(bak),'backup_sha256':hf(bak),'prefix_bytes':len(old),'marker':'ADJOINT_POLAR_GRAPH_INTEGRATED_REVIEW','complete':True,'P0':[],'P1':[],'P2':[],'verification_sha256':hf(RUN/'verification.json')}
q=RUN/'final_report_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q);assert q.read_bytes()==b
print(json.dumps(pin,ensure_ascii=False))
