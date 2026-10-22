from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'right_graph_blocks_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');s=next(iter(m['sources'].values()))
for k in ['complete','all_exit_zero','exact_39_targets','all_axioms_allowed','new_binary_equals_author','inherited_sources_binaries_preserved','author_source_binary_preserved','dependencies_preserved','external_direct_pins_preserved','read_only_artifacts_preserved','author_final_log_streams_preserved']:assert c[k],k
assert len(c['records'])==2 and len(s['declarations'])==17 and len(m['declarations'])==39
assert hf(s['path'])==s['sha256'] and hf(s['author_binary'])==s['author_binary_sha256']
assert hf(s['author_log'])==s['author_log_sha256'] and hf(s['author_stdout'])==s['author_stdout_sha256']
for d in m['inherited_partial_review']['sources'].values():assert hf(d['path'])==d['sha256'] and hf(d['author_binary'])==d['author_binary_sha256']
for d in m['dependencies'].values():assert hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256']
assert all(hf(p)==h for p,h in m['artifacts_readonly'].items())
prior=Path(m['inherited_partial_review']['run']);prior_pin=load(prior/'partial_review_pin.json')
p=REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md';assert hf(p)==prior_pin['report_sha256'];old=p.read_bytes()
def link(label,path,line=None):return f'[{label}](<{Path(path).as_posix()}{":"+str(line) if line else ""}>)'
def src(line):return link('HilbertProjectionBlocks.lean:'+str(line),s['path'],line)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
history=load(RUN/'author_history.json');failed=[x for x in history if x['returncode']!=0]
assert len(failed)==2
text=f'''

## Adendo parcial — terceiro módulo, 17 novos / 39 cumulativos

{now}. **[REAL — inspeção integral e recompilação própria] Nenhum P0, P1 ou P2 em `HilbertProjectionBlocks.lean`.** Concluída a revisão dos três arquivos congelados até aqui. Este adendo continua parcial, sem marcador final de aceite do pacote.

Conferências substantivas:

- {src(13)}–37: os adjuntos das inserções são as coordenadas de `WithLp 2 (H × H)`. Os blocos são exatamente `A=i₁* P i₁`, `B=i₁* P i₂`, `D=i₂* P i₂`, com operadores complexos no mesmo H. As definições aceitam P limitado arbitrário; não escondem idempotência ou positividade.
- {src(39)}: `B* = i₂* P i₁` é afirmado para **P=S.starProjection**, com `[CompleteSpace S]`, usando a autoadjunticidade da projeção. Os lemas de comutação (linhas58–85) transportam a hipótese explícita de comutação com a ação diagonal a A/B/D, sem pressupor T unitário ou auto-adjunto.
- {src(88)} e {src(97)}: de `P(y,−x)=0` resulta **Bx=Ay**; de `P(x,y)=(x,y)` resulta **B* x=y−Dy**. Conferidos os sinais, a orientação das composições e a dependência efetiva da projeção no segundo lema.
- {src(119)}–149: o vetor testemunha é `(A+1−D)v`. Sua energia é exatamente `Re⟨v,(A+1−D)v⟩ = ‖P(v,0)‖² + ‖P⊥(0,v)‖²`, por adjuntos, identidade de projeção e Pitágoras. Usa a geometria complexa de L² do produto; não troca a norma por aquela do produto usual.
- {src(153)}–171: `DenseRange e` basta para que `P(v,0)≠0` quando v≠0: projeção zero daria `⟨e a,v⟩=0` para todo a. Assim a energia é estritamente positiva para cada vetor não nulo. Não há hipótese de continuidade/limitação de f, univalência do fecho ou núcleo de gráfico já denso. **Positividade pontual não é uma cota uniforme positiva nem inversa limitada.**

Os tipos impressos mantêm H/E em universo 0, com as estruturas Hilbert complexa/completude efetivamente recebidas; os resultados de densidade recebem e/f como mapas lineares. O S genérico neste arquivo nomeia um **submódulo de H⊕₂H**, não o operador Tomita. Ainda não foi aplicada esta identidade para produzir o par direito concreto e a densidade real em Fix F.

Evidência própria:

- {link('compilation.json',RUN/'compilation.json')}: somente **duas execuções novas**, o terceiro módulo rc0 ({c['records'][0]['seconds']} s) e o auditor cumulativo39 rc0 ({c['records'][1]['seconds']} s). As duas primeiras recompilações permanecem herdadas do estrato anterior, sem repetição.
- {link('Auditor: tipos/universos e axiomas dos 39',RUN/'logs/RightGraphBlocksAudit.stdout.txt')}: 22 anteriores +17 novos, conjuntos exatos, somente `propext`, `Classical.choice`, `Quot.sound`. O `.olean` novo coincide byte a byte com o binário autoral aceito. Não foram encontrados `sorry`, `axiom`, `unsafe` ou atributos de redutibilidade suspeitos na fonte final.
- {link('Manifesto e dependências',RUN/'manifest.json')}: {len(m['dependencies'])} dependências de projeto pinadas e reaproveitadas de árvores próprias, incluindo os dois módulos deste estrato anterior. A origem imediata das cópias está registrada; `LEAN_PATH` usa só o build próprio e oito pacotes externos readonly. Nenhuma dependência antiga foi recompilada, nenhum build autoral de projeto foi usado na resolução dos imports.
- {link('Histórico autoral capturado',RUN/'author_history.json')}: dois rc1 anteriores (`013045_060190` e `013626_873429`) excluídos integralmente, inclusive seus prints com `sorryAx`. O rc0 final é a única tentativa autoral aceita deste módulo. As falhas permanecem preservadas.

Pins lidos dos arquivos:

| Artefato | SHA256 |
|---|---|
| Fonte final | `{s['sha256']}` |
| `.olean` autoral = próprio | `{s['author_binary_sha256']}` |
| {link('Log final 013823_362131',s['author_log'])} | `{s['author_log_sha256']}` |
| Stdout autoral final | `{s['author_stdout_sha256']}` |
| Compilação própria | `{hf(RUN/'compilation.json')}` |
| Manifesto próprio | `{hf(RUN/'manifest.json')}` |

[REAL — preservação delimitada] Fontes/binários dos três módulos, logs finais, dependências próprias, mãe `scalar_vna_custody.json`, pareceres selados, monólito e gate pinados permaneceram intactos. Não houve execução de monólito, integração, testes autorais, helpers ou atualização de memórias. O prefixo deste parecer é preservado byte a byte com backup imediato.

[OPEN — módulos seguintes] Construção de `ScalarRightProjectionPair`, densidade real dos vetores auto-adjuntos e igualdade com o gráfico do F original permanecem fora deste aceite parcial. Inclusão inversa pelo J original, KMS, traço e flags não foram promovidos. **Escopo concluído aqui: três módulos/39 alvos; pacote completo ainda pendente.**
'''
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');bk=p.with_name(p.name+'.bak_'+stamp)
with bk.open('xb') as f:f.write(old)
assert bk.read_bytes()==old
raw=old+text.encode('utf-8');tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==old
os.replace(tmp,p);assert p.read_bytes()==raw and p.read_bytes().startswith(bk.read_bytes())
pin={'timestamp':now,'report':str(p),'report_sha256':hf(p),'backup':str(bk),'backup_sha256':hf(bk),'prefix_preserved':True,'scope':'PARTIAL_THREE_MODULES_39_TARGETS','new_module_count':1,'new_declaration_count':17,'independent_compilation_sha256':hf(RUN/'compilation.json'),'P0':[],'P1':[],'P2':[],'package_final_approval':False}
q=RUN/'partial_review_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q)
print(json.dumps(pin,ensure_ascii=False))
