from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'phase_variational_integrated_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
s=load(RUN/'static_verification.json');parent=load(RUN/'adjoint_polar_graph_custody.json')
assert not any(s[k] for k in ['P0','P1','P2'])
assert all(hf(ROOT/n)==h for n,h in s['artifact_pins'].items())
assert all(hf(p)==h for p,h in s['surface_pins'].items())
assert hf(ROOT/'um.py')==s['working_sha256']
assert hf(REV/'REVIEW_PHASE_VARIATIONAL_DEV.md')==s['own_DEV_review_sha256']
assert not any((ROOT/n).exists() for n in s['future_custody_artifacts_absent'])
link=lambda label,p:f'[{label}](<{Path(p).as_posix()}>)'
text=f'''# Revisão integrada — seleção variacional no grafo original

{s['timestamp']}. **PRELIMINAR ESTÁTICO. Sem veredito integrado final.**

[REAL — inspeção própria de fontes, bytes e AST.] **Sem P0–P2 na parte estática concluída.** Os resultados novos de compilação/testes aguardam sinal final do autor. Os JSONs vivos de build/testes/evidence não foram usados como evidência atual nesta inspeção.

- Cópia SHA `{s['working_sha256']}`, **{s['embedded_files']} embutidos** medidos por AST. Dois DEV coincidem com snapshots e binários próprios revisados. Transposição literal nos dois TGLExt: somente `import TGLV350.` → `import TGLExt.V350`; embutidos iguais aos bytes das fontes integradas.
- Entre os embutidos antigos, mudam somente TGLExt.lean e TGL/Audit.lean: imports dos dois módulos e21 prints adicionais. A **fonte** Audit contém **{s['source_Audit_distinct']} nomes distintos = {parent['audit_declarations']} preservados +21**, com multiplicidades antigas mantidas. Ainda não é aceitação do stream de compilação novo.
- AST Python fora do dicionário Lean idêntico ao backup materno. `gate_extension.py` idêntico ao pin; original canônico e base relidos somente por hash, SHA `{s['original_sha256']}`. Mãe adjoint_polar_graph_custody.json SHA `{s['parent_custody_sha256']}`. **34 superfícies e pareceres selados conferidos com os pins maternos**, sem escrita.
- Diffs dos scripts delimitados: integrador acrescenta os dois módulos e batch699→720; compilador insere ambos antes das duas raízes; novo grupo de controle exige cinco nomes representativos e preserva as seis flags falsas, gate e full-plan. A lógica de hashes Audit corrente/histórico não mudou. O AST confirma que as flags qgf/gpf não entram diretamente no avaliador legado: recebe formal/physics/experiment, extraídos de qgc_/qgp_/feed, e kernel_frontier é anexado depois.
- Preparador, recorder e verifier lidos integralmente, sem execução. Preparador exige leitura DEV e pins maternos; recorder exige também parecer integrado, valida transposição, registros fonte/binário rc0, metadados Audit e34 pins antes de escrever. Prevê backup imediato dos bytes e append por temporário/troca. Verifier relê cada fonte/binário registrado e cada backup/prefixo. **Atomicidade por arquivo, sem transação conjunta das34 superfícies.** A nova custódia, sua verificação e o relatório integrado autoral ainda estavam ausentes.
- Minuta distingue o CLM real de seleção e a cota de seu vetor da construção ainda aberta do multiplicador. A identidade complexa mantém ξ∈Fix F e u∈D(S) originais; não atribui pertinência automática aos pares ponderados nem promove KMS/inversa. As consultas CFC continuam DERIVED. Nada nesta inspeção declara executados os futuros append/custódia.

{link('Evidência estática e pins',RUN/'static_verification.json')}; {link('fiação por AST',RUN/'gate_wiring.json')}; {link('DEV21 preservado',REV/'REVIEW_PHASE_VARIATIONAL_DEV.md')}, SHA `{s['own_DEV_review_sha256']}`. A reprodução matemática e os21 tipos/axiomas são herdados do DEV próprio concluído. Nenhuma nova compilação, teste autoral, monólito ou recorder executado; escritas somente revisao.

**Pendente:** sinal final; quatro logs novos (dois módulos e duas raízes), registros fonte/binário/log/stream, herança e frescor; Audit corrente reparseado versus21 próprios e{parent['audit_declarations']} antigos; controles, metadados históricos e flags efetivos. Pela programação lida, a expectativa é **{parent['integrated_records']+2} registros = {parent['integrated_records']-2} herdados +4 novos**, e **{parent['controls']+1} controles**. Essas contagens de build/testes ainda não são resultados aceitos. O parecer final e seu marcador dependem da conferência posterior.

[OPEN] Pertença dos pares ponderados, cota inferior do bloco e multiplicador limitado, inclusão inversa, Δ^it/KMS, traço, certificados/gate/runtime. Nenhuma promoção de escopo.
'''
p=REV/'REVIEW_PHASE_VARIATIONAL_INTEGRATED.md';assert not p.exists()
raw=text.encode();tag=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');tmp=p.with_name(p.name+'.tmp_'+tag)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;os.replace(tmp,p);assert p.read_bytes()==raw
pin={'timestamp':s['timestamp'],'report':str(p),'report_sha256':hf(p),'static_verification_sha256':hf(RUN/'static_verification.json'),'status':'PRELIMINARY_STATIC_ONLY','final':False}
q=RUN/'preliminary_report_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q)
print(json.dumps(pin,ensure_ascii=False))
