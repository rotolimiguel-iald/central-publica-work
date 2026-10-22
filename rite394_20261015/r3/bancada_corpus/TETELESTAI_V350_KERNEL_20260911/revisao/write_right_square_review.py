"""Write the bounded DEV review from independent compilation and measured pins."""
from pathlib import Path
import datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'right_square_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');D=load(RUN/'right_square_draft_status.json')
assert all(v is True for k,v in c.items() if k!='records')
assert len(m['sources'])==2 and len(m['declarations'])==13 and len(c['records'])==3
for n,h in m['artifact_pins'].items():assert hf(ROOT/n)==h
for r in c['records']:
    assert r['returncode']==0 and r['exact_targets'] and r['axioms_allowed']
    assert hf(r['command'][2])==r['output_sha256'] and hf(r['stdout'])==r['stdout_sha256'] and hf(r['stderr'])==r['stderr_sha256']
for rel,s in m['sources'].items():
    assert hf(s['path'])==hf(s['snapshot'])==s['sha256']
    assert hf(s['author_binary'])==s['author_binary_sha256'] and hf(s['author_log'])==s['author_log_sha256']
for p,r in m['memory_surfaces'].items():
    assert hf(p)==r['sha256'] and hf(r['backup'])==r['before_sha256']
for p,h in m['previous_reviews'].items():assert hf(p)==h
assert hf(ROOT/'um.py')==m['working_sha256'] and hf(ROOT/'gate_extension.py')==m['gate_sha256']
t=Path(c['records'][-1]['stdout']).read_text(encoding='utf-8')
assert all(len(re.findall(r'^'+re.escape(n)+r'(?=\s|\{|\.)',t,re.M))==1 for n in m['declarations'])
def link(p,label=None):
    p=Path(p);return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def line(rel,n):return '['+Path(rel).name+':'+str(n)+'](<'+(ROOT/rel).as_posix()+':'+str(n)+'>)'
table='| Fonte DEV | Alvos | SHA-256 da fonte |\n|---|---:|---|\n'
for rel,s in m['sources'].items():table+='| '+link(s['path'])+' | '+str(len(s['declarations']))+' | `'+s['sha256']+'` |\n'
buildtable='| Execução própria | rc | SHA-256 do .olean próprio | Resultado |\n|---|---:|---|---|\n'
for r in c['records']:
    buildtable+='| '+link(r['stdout'],Path(r['module']).stem)+' | '+str(r['returncode'])+' | `'+r['output_sha256']+'` | '+('idêntico ao autor' if r.get('binary_equals_author') else 'auditor 13/13')+' |\n'
pins='| Artefato lido | SHA-256 |\n|---|---|\n'
for n,h in m['artifact_pins'].items():pins+='| '+link(ROOT/n)+' | `'+h+'` |\n'
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''Parecer DEV — escala da direita no domínio do mesmo S†S

RIGHT_SQUARE_DEV_REVIEW

{stamp}. **Sem achados P0–P2. Revisão dos dois módulos/13 alvos (4 + 9) concluída.** [REAL — leitura integral das fontes, manifesto, relatório e recorder; recompilação independente e auditor próprio.] O resultado é a inclusão de domínio e a relação local de escala para o `scalarTomitaSquare P` já construído. Não é identificação do fluxo nem KMS.

{table}
Em {line('kernel/TGLV350/HomogeneousRightSquareDomain.lean',12)}, a hipótese genérica explícita é `homogeneousRightCoreElement e = star (homogeneousRightCoreElement d)`, com `d,e : HomogeneousRightData P`. Ela transforma `S R_d x` em `π(core e) Sx`. Em {line('kernel/TGLV350/ScalarTomitaSquare.lean',14)}, o domínio herdado é exatamente `x∈D(S)` e `Sx∈D(S†)`; a definição da linha 35 é a composição efetiva dos mesmos operadores no mesmo `ScalarGNSHilbert P`, não outro operador escolhido por satisfazer uma relação.

Em {line('kernel/TGLV350/HomogeneousRightSquareDomain.lean',24)}, as duas pertinências de `R_d x` são provadas: a primeira pelo transporte anterior de `D(S)`; a segunda pela invariância de `D(S†)` por `π(core e)` aplicada ao vetor `Sx` que já pertence ao domínio adjunto. Na linha 42, `Subtype.ext` identifica os vetores de entrada no adjunto e a lei anterior fornece **`A R_d x = R_e* A x` para todo `x : scalarTomitaSquareDomain P`**. Não se supõe domínio total, continuidade de `S`/`S†` ou invariância do domínio composto. As duas antilinearidades compõem-se no mapa complexo-linear `A=S†S`; os subtipos guardam as pertinências reais, sem domínio fictício.

Em {line('kernel/TGLV350/MatrixUnitRightSquare.lean',11)}, `localEigenvalue P N i j` é o real `towerW P N i / towerW P N j`. As duas ponderações são positivas por `towerW_pos`; portanto **r=w_i/w_j>0** e os logaritmos não usam valores degenerados. A identidade é `−log(w_j/w_i)=log(w_i/w_j)`. Nas linhas 18–22, a transposta conjugada troca `e_ji` por `e_ij`, e `deltaLevel_single` fornece `modTwist(e_ji)=r e_ij`. Nenhum sinal ou razão foi invertido inadvertidamente.

Em {line('kernel/TGLV350/MatrixUnitRightSquare.lean',24)}, a igualdade `R_e=c R_d` decorre da igualdade **do operador direito na fibra e da frequência**: `fibre(fibre e.right) * shift e.frequency` é comparado como CLM ambiente, e `ext1`/`Subtype.ext` transportam a igualdade à restrição no mesmo `H_I`. Não basta igualdade no vácuo, nem se encadeiam homônimos. A prova herdada de `rTowerPi_parameter_smul` usa adicionalmente comutação e densidade para justificar sua igualdade global.

As linhas 36–49 combinam a torção e a frequência correta para obter **`R_(e_ji)* = (r:ℂ) R_(e_ij)`**. A linha 51 prova a hipótese algébrica `core(e_ji)=core(e_ij)*`, distinta da torção do adjunto direito. Logo a especialização da linha 71 é **`A R_(e_ij)x = (r:ℂ) • R_(e_ij)(Ax)` em todo `D(A)`**, com pertinência provada nas linhas 59–67. O escalar é a inclusão canônica do real positivo em ℂ; ele entra pela igualdade entre operadores direitos limitados depois da composição, sem ser puxado através de um mapa antilinear sem conjugação. A hipótese genérica `he` é efetivamente descarregada para as instâncias ij/ji, sem premissa adicional sobre `P`.

**Evidência própria.**

{buildtable}
Foram executadas somente essas duas compilações e {link(RUN/'sources/RightSquareAudit.lean','o auditor próprio dos 13 alvos')}. Os 13 `#check` com universos e os 13 `#print axioms` foram lidos: nomes exatos, somente `propext`, `Classical.choice`, `Quot.sound`, sem `sorry`, `axiom`, `unsafe` ou alteração de redutibilidade nas novas fontes. As definições também estão auditadas. Os dois binários próprios coincidem byte a byte com os autorais. Logs autorais finais relidos: `HomogeneousRightSquareDomain_20260912_163333_058477.json` e `MatrixUnitRightSquare_20260912_163525_790535.json`; fonte/binário/JSON/streams conferem com o manifesto, rc0, fonte inalterada e saída existente. O histórico delimitado encontrou apenas essas primeiras tentativas, sem rc1.

{link(RUN/'compilation.json')} SHA-256 `{hf(RUN/'compilation.json')}`; {link(RUN/'manifest.json')} SHA-256 `{hf(RUN/'manifest.json')}`. As **{len(m['dependencies'])} dependências de projeto** vieram das árvores próprias do adjunto direito e da involução de Tomita, com hashes das origens e fontes/binários congelados; dependências compartilhadas coincidem. O `LEAN_PATH` usa apenas o build próprio e oito diretórios de pacotes externos readonly, sem build autoral de projeto. Não se recompilaram biblioteca/dependências; permanece a errata de comentário herdada e pinada de `DualSemifiniteIdeal`. Compilador Lean 4.31.0, SHA-256 `{m['compiler_sha256']}`. A leitura externa autorizada serviu ao compilador; todas as saídas ficaram em `revisao/`.

**Manifesto e estatuto.**

{pins}
`record_right_square_draft.py` foi apenas inspecionado. Ele confere a mãe integrada, seus artefatos/superfícies e os pins das compilações aceitas; cria somente relatório e manifesto por temporário verificado, recusando sobrescrita. Não grava nas 34 memórias. O texto distingue inclusão de domínio de bijetividade e marca explicitamente a ligação ao fluxo como aberta. O nome e os flags positivos do manifesto não foram tomados como prova: foram confrontados com os tipos e compilações acima.

Os **34 arquivos e seus 34 backups** da mãe foram relidos, com hashes e prefixos byte a byte preservados. Os pareceres anteriores e a cópia integrada permanecem intactos; hash da cópia lido `{m['working_sha256']}`. As contagens **160/90/6704** e a verificação materna são evidência herdada, não nova auditoria integrada nesta tarefa. As seis flags continuam falsas na evidência lida. Nenhum original canônico, monólito ou recorder foi executado; nenhuma fonte autoral ou memória foi modificada. Os helpers futuros não foram examinados nem executados.

**Conclusão delimitada:** DEV 2/13 encerrado, sem P0–P2 ou análise necessária pendente. [OPEN] A relação para unidades matriciais não prova identificação de `A^it` com o fluxo, KMS global, bijetividade de `R_y`, lacuna espectral, traço, Three Locks ou consumo pelas seis flags. Não se presume `I=nν`. Essas fronteiras são limites esperados, não defeitos das provas. Integração e registro de memória deste lote permanecem pendentes.
'''
p=REV/'REVIEW_RIGHT_SQUARE_DEV.md';assert not p.exists()
b=text.encode('utf-8');q=p.with_name(p.name+'.tmp')
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b;q.replace(p);assert p.read_bytes()==b
assert p.read_text(encoding='utf-8').count('RIGHT_SQUARE_DEV_REVIEW')==1
v={'timestamp':stamp,'report':str(p),'report_sha256':hf(p),'report_bytes':len(b),'report_lines':len(text.splitlines()),
 'modules':2,'targets':13,'own_executions_rc0':3,'both_binaries_identical':True,'only_trio':True,
 'manifest_sha256':hf(RUN/'manifest.json'),'compilation_sha256':hf(RUN/'compilation.json'),
 'P0':[],'P1':[],'P2':[],'memory_pairs_preserved':34,'integrated':False,'pending_analysis':False}
q=RUN/'verification.json';assert not q.exists();tmp=q.with_name(q.name+'.tmp');raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(q)
print(json.dumps(v,ensure_ascii=False,indent=2))
