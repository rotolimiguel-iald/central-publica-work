from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'right_graph_core_integrated_latest_run.txt').read_text().strip())
s=json.loads((RUN/'static_verification.json').read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not s['P0'] and not s['P1'] and not s['P2']
assert all(hf(ROOT/n)==h for n,h in s['artifact_pins'].items())
assert hf(ROOT/'um.py')==s['working_sha256']
assert hf(REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md')==s['own_DEV_review_sha256']
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
text=f'''# Revisão integrada — graph-core do F original

{s['timestamp']}. **PRELIMINAR ESTÁTICO — sem marcador ou veredito integrado final.**

[REAL — inspeção de fontes/bytes/AST] **Sem P0, P1 ou P2 na parte estática concluída.** Build e testes estão pendentes de aviso final do autor; os JSONs vivos de compilação, testes e evidence não foram consumidos nesta rodada.

- Cópia `{s['working_sha256']}`, **909 embutidos**. Os seis DEV coincidem com as fontes próprias revisadas e os binários DEV pinados; as seis fontes TGLExt e seus embutidos resultam exclusivamente de `import TGLV350.` → `import TGLExt.V350`. Os demais embutidos permanecem iguais à mãe, exceto as duas raízes com os imports/prints acrescentados.
- Na **fonte** de Audit: **7.039 declarações distintas = 6.982 preservadas +57 do manifesto**, mantendo também as multiplicidades anteriores. Esta contagem não é ainda a auditoria do stream integrado novo.
- AST Python fora do dicionário Lean idêntico ao backup da mãe; `gate_extension.py` idêntico ao pin. Original canônico e cópia-base relidos somente por hash: `{s['original_sha256']}`. Mãe `scalar_vna_custody.json`: `{s['parent_custody_sha256']}`. As **34 memórias e os pareceres selados** conferem com os pins maternos.
- Diffs dos scripts: integrador acrescenta seis módulos e batch625→682; compilador os coloca antes das duas raízes; teste acrescenta um grupo de **nove nomes** que exige as seis flags falsas e gate/full-plan preservados. Nenhuma alteração na lógica existente de Audit atual/histórico. A diferença entre flags qgf/gpf e entradas `formal/physics/experiment` do avaliador legado permanece no AST, com `kernel_frontier` anexado depois.
- Os cinco helpers permanecem byte a byte como lidos na revisão DEV. Preparador exige leitura do parecer; recorder exige também revisão integrada; prevê 34 backups imediatos de bytes e append/troca temporária; verifier relê fonte/binário e backup/prefixo. Nenhum deles foi executado pelo revisor. Os artefatos de nova custódia, verificação e relatório integrado autoral estavam ausentes na inspeção.

{link('Evidência estática e pins',RUN/'static_verification.json')}; {link('fiação do gate por AST',RUN/'gate_wiring.json')}; {link('DEV6/57 preservado',REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md')}, SHA `{s['own_DEV_review_sha256']}`. Nenhuma execução Lean, teste autoral, monólito, integrador ou recorder nesta revisão integrada. Escritas somente `revisao/`.

**Pendente para o parecer final:** aviso de build/testes concluídos; leitura dos oito logs novos (seis módulos e duas raízes), todos os registros fonte/binário/log/streams e sua herança, mapa Audit corrente contra os 57 próprios e os 6.982 anteriores, hashes de streams/metadados históricos, controles e flags efetivos. **207 registros, 199 herdados+8 novos e 102 controles são expectativas, não resultados aceitos aqui.**

O resultado matemático herdado é a igualdade do fecho do grafo dos pares direitos com o gráfico do **F original no mesmo H_I**. Inclusão inversa dos comutantes pelo J original, reconstrução R=Jπ(b)J, Δ^it/KMS, traço, consumo de certificados e runtime permanecem fora desse resultado. Nenhuma promoção de gate.
'''
p=REV/'REVIEW_RIGHT_GRAPH_CORE_INTEGRATED.md';old=None;stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');raw=text.encode()
if p.exists():
    old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+stamp)
    with bk.open('xb') as f:f.write(old)
    assert bk.read_bytes()==old;raw=old+b'\n\n'+raw
tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and (old is None or p.read_bytes()==old)
os.replace(tmp,p);assert p.read_bytes()==raw
pin={'report':str(p),'report_sha256':hf(p),'timestamp':s['timestamp'],'status':'PRELIMINARY_STATIC_ONLY','final':False,'static_verification_sha256':hf(RUN/'static_verification.json')}
q=RUN/'preliminary_report_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q);print(json.dumps(pin,ensure_ascii=False))
