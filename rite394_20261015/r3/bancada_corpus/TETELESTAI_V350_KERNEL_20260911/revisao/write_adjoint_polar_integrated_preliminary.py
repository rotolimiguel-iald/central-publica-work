from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'adjoint_polar_graph_integrated_latest_run.txt').read_text().strip())
s=json.loads((RUN/'static_verification.json').read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not any(s[k] for k in ['P0','P1','P2'])
assert all(hf(ROOT/n)==h for n,h in s['artifact_pins'].items())
assert hf(ROOT/'um.py')==s['working_sha256']
assert hf(REV/'REVIEW_ADJOINT_POLAR_GRAPH_DEV.md')==s['own_DEV_review_sha256']
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
text=f'''# Revisão integrada — adjunto polar e grafos originais

{s['timestamp']}. **PRELIMINAR ESTÁTICO — sem marcador ou veredito integrado final.**

[REAL — inspeção de fontes/bytes/AST] **Sem P0, P1 ou P2 na parte estática concluída.** Compilação e testes aguardam aviso final do autor; os JSONs vivos de build/testes/evidence não foram consumidos como resultados atuais nesta inspeção.

- Cópia `{s['working_sha256']}`, **911 embutidos**. Ambos DEV coincidem com as fontes próprias revisadas e binários pinados. A transposição dos dois TGLExt e embutidos é literal, exclusivamente `import TGLV350.` → `import TGLExt.V350`. Os demais embutidos permanecem iguais à mãe, exceto as duas raízes com imports/prints adicionais.
- Na **fonte** de Audit: **7.056 declarações distintas = 7.039 preservadas +17 do manifesto**, incluindo preservação das multiplicidades anteriores. Ainda não é conclusão sobre o stream compilado novo.
- AST Python fora do dicionário Lean idêntico ao backup materno; `gate_extension.py` idêntico ao pin. Original canônico e base relidos apenas por hash: `{s['original_sha256']}`. Mãe `right_graph_core_custody.json`: `{s['parent_custody_sha256']}`. **34 superfícies e pareceres selados** conferem com os pins da mãe.
- Diffs delimitados: integrador acrescenta dois módulos e batch682→699; compilador insere ambos antes das duas raízes; controle novo exige sete nomes representativos, seis flags falsas, gate/full-plan preservados. A lógica de hashes Audit atual/histórico não mudou. As flags qgf/gpf não são entradas diretas de `evaluate_quantum_gravity_closure`; o AST mantém `formal/physics/experiment` e anexa `kernel_frontier` depois.
- Cinco helpers lidos estaticamente. Preparador exige leitura do parecer DEV e pins da mãe; recorder exige também parecer integrado, valida fontes/binários, metadados e 34 superfícies antes de escrever. Prevê backup imediato dos bytes de cada superfície e append por temporário/troca, preservando prefixos. Verifier relê cada fonte/binário registrado e cada backup/prefixo. Não é transação conjunta das 34 escritas; a garantia é por arquivo. Nenhum helper autoral foi executado pelo revisor. Nova custódia/verificação/relatório integrado autoral estavam ausentes.
- Minuta no recorder mantém F=BJ=JSJ com domínio inteiro e J×J levando graph F a graph S. Não transforma a inscrição conjugado-linear em isomorfismo de álgebras, nem a densidade de gráfico em reconstrução do comutante. A execução futura e a atualização das memórias não foram declaradas concluídas.

{link('Evidência estática e pins',RUN/'static_verification.json')}; {link('fiação por AST',RUN/'gate_wiring.json')}; {link('DEV2/17 preservado',REV/'REVIEW_ADJOINT_POLAR_GRAPH_DEV.md')}, SHA `{s['own_DEV_review_sha256']}`. Nenhuma nova execução Lean, teste autoral ou monólito; escritas somente revisao.

**Pendente:** aviso final; quatro logs novos (dois módulos e raízes), releitura de todos os registros fonte/binário/log/stream e herança; mapa Audit corrente versus 17 próprios e 7.039 anteriores; controles, metadados históricos e flags efetivos. **209 registros =205 herdados+4 novos e 103 controles são expectativas, não resultados aceitos neste estrato.**

[OPEN] Inclusão inversa pelo J original, reconstrução JRJ∈π(N), estimativa dos quadrados, Δ^it/KMS, traço, certificados e runtime. Nenhuma promoção de gate.
'''
p=REV/'REVIEW_ADJOINT_POLAR_GRAPH_INTEGRATED.md'
assert not p.exists()
raw=text.encode();stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;os.replace(tmp,p);assert p.read_bytes()==raw
pin={'report':str(p),'report_sha256':hf(p),'timestamp':s['timestamp'],'status':'PRELIMINARY_STATIC_ONLY','final':False,'static_verification_sha256':hf(RUN/'static_verification.json')}
q=RUN/'preliminary_report_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q);print(json.dumps(pin,ensure_ascii=False))
