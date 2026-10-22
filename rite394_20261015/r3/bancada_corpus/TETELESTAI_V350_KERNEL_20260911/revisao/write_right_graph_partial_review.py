from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'right_graph_partial_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');history=load(RUN/'author_history.json')
assert c['complete'] and c['all_exit_zero'] and c['exact_22_targets'] and c['all_axioms_allowed'] and c['two_binaries_equal_author']
for k in ['author_source_binary_preserved','dependencies_preserved','external_direct_pins_preserved','read_only_artifacts_preserved','author_final_log_streams_preserved']:assert c[k],k
assert all(hf(p)==h for p,h in m['artifacts_readonly'].items())
assert all(hf(x['path'])==x['sha256'] and hf(x['author_binary'])==x['author_binary_sha256'] and hf(x['author_log'])==x['author_log_sha256'] for x in m['sources'].values())
def link(label,p,line=None):return f'[{label}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
def src(n,line):return link(n+'.lean',ROOT/'kernel/TGLV350'/(n+'.lean'),line)
table='\n'.join(f'| {Path(n).stem} | {len(x["declarations"])} | `{x["sha256"]}` | `{x["author_binary_sha256"]}` |' for n,x in m['sources'].items())
logs='\n'.join('- '+link(Path(x['author_log']).name,x['author_log'])+f'; SHA256 `{x["author_log_sha256"]}`, stdout `{x["author_stdout_sha256"]}`.' for x in m['sources'].values())
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds');parent=load(ROOT/'scalar_vna_custody.json')
text=f'''# Revisão DEV — graph-core direito, estrato parcial

{date}. **PARCIAL: dois módulos/22 alvos. Sem marcador final de aprovação do pacote.**

[REAL — leitura e recompilação independente] **Nenhum P0, P1 ou P2 nestes dois módulos.** Fontes lidas integralmente, tipos com universos e axiomas transitivos conferidos. As duas recompilações e o auditor próprio22 passaram rc0; os dois `.olean` são idênticos aos autorais dos logs finais. Blocos, densidade real e igualdade final dos gráficos ainda não são certificados por este estrato.

Conferências substantivas:

- {src('ComplexGraphProjection',14)}: inserções e ação diagonal são CLM complexos no `WithLp 2 (H × H)`. A igualdade do adjunto diagonal é demonstrada pelo produto interno de L²; não depende de tratar a equivalência com o produto usual como uma isometria.
- {src('ComplexGraphProjection',37)}: `complexGraphClosure` é o fecho da imagem de uma aplicação **ℂ-linear**, com completude herdada do fecho. Não pressupõe univalência da relação, continuidade de e/f ou limitação de uma operação em norma de e(a). A hipótese de transporte dos geradores dá invariância do fecho por continuidade da ação limitada.
- {src('ComplexGraphProjection',65)}: a simetria complexa com ordem exata `⟨f a,e b⟩=⟨e a,f b⟩` produz `(f a,−e a)` no ortogonal e projeção zero. A comutação da projeção recebe invariância para T **e T.adjoint**, satisfazendo a redução; nenhuma continuidade geral do adjunto na topologia forte é usada.
- {src('ScalarRightMultiplicationGraph',24)}: `scalarWeightPairProduct` tipa a*b em `scalarWeightStarCore P` usando a finitude de b e a de a para o adjunto b*a. São elementos do **ideal escalar completo nν**, sem substituir pelo ideal uniforme I nem supor nν fechado pela estrela. O lema de estrela troca a,b e a inscrição coincide com π(a*)Λ(b).
- {src('ScalarRightMultiplicationGraph',44)}: a simetria usa η∈`scalarTomitaAdjointDomain P` e **Fη=η**, a extensão já provada de S à estrela do domínio completo, e `scalarTomitaAdjoint_pairing` para o mesmo F. Conferidas as orientações dos produtos internos e dos adjuntos de π(a),π(b). Não recebe KMS, graph-core de F ou limitação de a↦π(a)η em ‖Λ(a)‖.
- {src('ScalarRightMultiplicationGraph',83)}: o gráfico auxiliar é o mesmo fecho complexo de `(Λ(a),π(a)η)`. Invariância e comutação da projeção valem para **todo η** e todo c∈N, usando `scalarWeightLeftProduct` e depois `star c`. A condição Fη=η entra somente na simetria e em `scalarRightMultiplicationGraph_rotated_zero` (linha112). Nenhuma hipótese de redução fica residual na aplicação concreta.

Os genéricos usam `H E : Type`, conforme os tipos impressos (universo 0); não é afirmada generalização adicional. A definição do gráfico não constrói por si só um operador direito limitado, auto-adjunto ou densamente definido no domínio máximo. Tampouco identifica esse gráfico complexo com o gráfico real de F.

Evidência e proveniência:

- {link('Compilação própria',RUN/'compilation.json')} — três execuções rc0: dois módulos e auditor22. {link('Tipos e axiomas próprios',RUN/'logs/RightGraphPartialAudit.stdout.txt')}. Conjunto exato de 22 alvos; todos somente `propext`, `Classical.choice`, `Quot.sound`. Não há `sorry`, `axiom`, `unsafe` nem marcador de redutibilidade suspeito nas fontes finais lidas.
- {link('Manifesto próprio',RUN/'manifest.json')} fixa **{len(m['dependencies'])} dependências de projeto** copiadas de árvores independentes já revisadas. O catálogo usa as árvores CorePolar, GaussianPolar, RightVector e ScalarVNA, com origem e hashes imediatos por dependência; nenhuma dependência antiga foi recompilada. `LEAN_PATH` contém somente build próprio e oito pacotes externos readonly, nunca build autoral de projeto.
- Compilador `{m['lean_version']}`, SHA `{m['compiler_sha256']}`. Pins externos diretos herdados relidos; acrescentado o import direto `Mathlib.Analysis.InnerProductSpace.ProdL2`. Não é uma reauditoria integral da Mathlib ou da cadeia custodiada.
- Uma tentativa autoral rc1 de `ComplexGraphProjection` foi capturada e excluída, inclusive o print com `sorryAx`; o segundo módulo tem a tentativa final rc0 capturada. Somente bytes dos dois logs aceitos e correspondentes às fontes/binários atuais são usados como evidência autoral.

| Módulo | Alvos | SHA256 fonte | SHA256 binário autoral = próprio |
|---|---:|---|---|
{table}

Logs finais autorais, distintos dos próprios:

{logs}

Mãe `scalar_vna_custody.json`: `{hf(ROOT/'scalar_vna_custody.json')}`; sua verificação registrada confere com o pin. Cópia integrada ainda `{parent['working_sha256']}`. Os pareceres ScalarVNA, fontes/binários autorais, logs finais, dependências copiadas, monólito e gate pinados permaneceram inalterados. Esta rodada não refez a auditoria dos 201 registros nem das 34 memórias da mãe. Não executou monólito, integrador, recorder ou testes autorais; não escreveu em memórias.

[OPEN — restante do pacote] Faltam revisar os módulos futuros que construam os blocos, o par auto-adjunto e a identidade positiva, deduzam densidade real em Fix F e concluam `closure (scalarRightPairGraph P) = graph F` original. Não há aceite desses resultados por antecipação. A consulta por blocos continua proposta fora dos 22 alvos. Inclusão inversa com J, KMS, traço e promoção de flags/gate não são resultados deste estrato. **A revisão dos dois arquivos congelados está concluída; o parecer cumulativo do pacote permanece aberto.**
'''
p=REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md';raw=text.encode();old=None;stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
if p.exists():
 old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+stamp)
 with bk.open('xb') as f:f.write(old)
 assert bk.read_bytes()==old;raw=old+b'\n\n'+raw
tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and (old is None or p.read_bytes()==old)
os.replace(tmp,p);assert p.read_bytes()==raw
pin={'timestamp':date,'report':str(p),'report_sha256':hf(p),'bytes':len(raw),'scope':'PARTIAL_TWO_MODULES_22_TARGETS','compilation_sha256':hf(RUN/'compilation.json'),'manifest_sha256':hf(RUN/'manifest.json'),'P0':[],'P1':[],'P2':[],'package_final_approval':False}
q=RUN/'partial_review_pin.json';qb=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();assert not q.exists();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(qb)
assert qt.read_bytes()==qb;os.replace(qt,q)
print(json.dumps(pin,ensure_ascii=False))
