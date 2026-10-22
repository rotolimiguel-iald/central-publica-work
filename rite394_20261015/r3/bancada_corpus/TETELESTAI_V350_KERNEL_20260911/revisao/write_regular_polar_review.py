"""Create the delimited DEV report from independently measured evidence."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=Path((REV/'regular_polar_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
m=load(RUN/'manifest.json'); c=load(RUN/'compilation.json')
assert all(v is True for k,v in c.items() if k!='records')
assert len(m['sources'])==3 and len(m['declarations'])==16 and len(c['records'])==4
for n,h in m['artifact_pins'].items():assert hf(ROOT/n)==h
for r in c['records']:
    assert r['returncode']==0 and r['exact_targets'] and r['axioms_allowed']
    assert hf(r['command'][2])==r['output_sha256']
    assert hf(r['stdout'])==r['stdout_sha256'] and hf(r['stderr'])==r['stderr_sha256']
for rel,s in m['sources'].items():
    assert hf(s['path'])==hf(s['snapshot'])==s['sha256']
    assert hf(s['author_binary'])==s['author_binary_sha256'] and hf(s['author_log'])==s['author_log_sha256']
for p,r in m['memory_surfaces'].items():
    assert hf(p)==r['sha256'] and hf(r['backup'])==r['before_sha256']
for p,h in m['previous_reviews'].items():assert hf(p)==h
assert hf(ROOT/'um.py')==m['working_sha256'] and hf(ROOT/'gate_extension.py')==m['gate_sha256']
audit=Path(c['records'][-1]['stdout']).read_text(encoding='utf-8')
assert all(len(re.findall(r'^'+re.escape(n)+r'(?=\s|\{|\.)',audit,re.M))==1 for n in m['declarations'])
def link(p,label=None):
    p=Path(p);return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def line(name,n):
    return '['+name+'.lean:'+str(n)+'](<'+(ROOT/'kernel/TGLV350'/f'{name}.lean').as_posix()+':'+str(n)+'>)'
table='| Fonte DEV | Alvos | SHA-256 lido |\n|---|---:|---|\n'
for rel,s in m['sources'].items():
    table+='| '+link(s['path'])+' | '+str(len(s['declarations']))+' | `'+s['sha256']+'` |\n'
bt='| Compilação própria / stdout | rc | SHA-256 do .olean próprio | Comparação |\n|---|---:|---|---|\n'
for r in c['records']:
    bt+='| '+link(r['stdout'],Path(r['module']).stem)+' | '+str(r['returncode'])+' | `'+r['output_sha256']+'` | '+('idêntico ao autor' if r.get('binary_equals_author') else 'auditor 16/16')+' |\n'
pins='| Artefato lido | SHA-256 |\n|---|---|\n'
for n,h in m['artifact_pins'].items():pins+='| '+link(ROOT/n)+' | `'+h+'` |\n'
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')

H=load(RUN/'author_history.json')
for x in H:
    for b in x.get('failed_source_backups',[]):assert hf(b['path'])==b['sha256']
text=f'''Parecer DEV — conjugação polar e continuidade da direita regular

REGULAR_POLAR_DEV_REVIEW

{stamp}. **Sem achados P0–P2. Revisão DEV 3/16 concluída (9 + 4 + 3).** [REAL — leitura integral das três fontes, manifesto e relatório, recompilação independente e auditor próprio.] Foram conferidos os mesmos objetos `A=S†S`, `T=(I+A)⁻¹`, `B=scalarTomitaPositiveRoot P` e `J=scalarTomitaPolarFactor P` no `ScalarGNSHilbert P` anterior. Não é identificação do fluxo modular/KMS.

{table}
Em {line('ScalarRegularRightPolar',14)}, **`T R_t=R_t T`** é deduzido das duas equações da inversa efetiva `T`: para cada `z`, toma-se `x∈D(A)` com `x+Ax=z` e `x=Tz`; usa-se a pertinência já provada de `R_t x` a `D(A)` e `A R_t x=R_t Ax`. Aplicar `T` a `R_t x+A R_t x` devolve `R_t x`. Não há inversa formal sem domínio, hipótese residual de comutação com `T`, nem suposição de domínio total de `A`.

Em {line('ScalarRegularRightPolar',31)}, o transporte genérico é especializado ao **grafo da mesma raiz construída por CFC do resolvente**. Ele transporta os dois componentes do grafo parametrizado por `sqrt(T)` e `sqrt(1-T)`; comutação com essas funções decorre de comutação com `T`. Positividade e injetividade são as já provadas para `scalarTomitaResolvent P`, não campos novos. As linhas 40–61 extraem do grafo a pertinência real e a igualdade de valores de `B`; não se assume `B` limitado ou contínuo. A linha 63 usa `R_(-t)R_t=I` para provar **`R_t x∈D(B) ↔ x∈D(B)`** em todo o Hilbert, além de `B R_t x=R_t Bx` em todo `D(B)`.

Em {line('ScalarRegularRightPolar',78)}, a extensão por densidade usa **a imagem de B**, cuja densidade já foi provada para essa raiz positiva auto-adjunta de núcleo trivial. Sobre `z=Bx`, a cadeia é `J R_t Bx=J B R_t x=S R_t x=π(λ_t*)Sx=π(λ_t*)JBx`. A igualdade de subtipos da linha 86 mantém os mesmos vetores nas inclusões de `D(B)` em `D(S)`. A extensão ao Hilbert inteiro usa a continuidade de `J`, `R_t` e `π(λ_t*)`; não presume continuidade do operador não limitado `S` ou de `B`, nem sobrejetividade ou inversa limitada de `B`.

As linhas 105–121 usam `antiunitaryConjugate J C = J ∘ C ∘ J.symm`. **J é o fator polar efetivo de S**, construído anteriormente por extensão antilinear com `JBx=Sx`; não é `TowerJ` nem um antiunitário escolhido para satisfazer a fórmula. A primeira conjugação dá `J R_t J⁻¹=π(λ_t*)`. A volta usa explicitamente `scalarTomitaPolarFactor_involutive`, já provado nos ancestrais, sem tomar involutividade como propriedade automática de antiunitários. Em {line('ScalarRegularPolarCommutation',50)}, a substituição `t↦-t` e `λ_t*=λ_(-t)` dão **`Jπ(λ_t)J⁻¹=R_(-t)`**, com sinal correto. A conjugação por dois mapas antilineares é complexo-linear como operador sobre o Hilbert; não se afirma linearidade complexa da operação em C.

Em {line('ScalarRegularPolarCommutation',13)}, **`R_t` comuta com todo `π(a)`, para `a∈N`**, não só com a família regular. A prova calcula na imagem densa do domínio escalar completo `nν`: ambos os produtos permanecem em `nν`, e a igualdade é `(a b)λ_t=a(bλ_t)`. As linhas 24–37 identificam os produtos como elementos do mesmo submódulo e usam os dois entrelaçamentos existentes. A continuidade dos operadores limitados estende a igualdade ao mesmo `H_I`. Não se troca `nν` pelo ideal uniforme `I`, não se exige `I=nν`, nem se escolhe outro completamento. A linha 57 conclui a comutação de cada gerador regular conjugado por J com todo `π(N)`; não conclui a igualdade de toda a álgebra com seu comutante.

Em {line('ScalarRegularRightContinuity',13)}, a cota **`‖λ_t‖≤1` para todo t** vem das isometrias da translação e do fluxo da fibra. A linha 20 aplica `scalarGNSRepresentation_tendsto_of_uniformly_bounded` a `λ_t`, com limite já conhecido na representação regular e cota 1 explicitamente descarregada. Obtém continuidade vetorial de `π(λ_t)` em cada `z∈H_I`. A linha 30 escreve `R_t z=Jπ(λ_(-t))Jz` e usa continuidade de J e da negação. Portanto a nova continuidade é **forte**, sem assumir continuidade na norma de operadores, continuidade geral do adjunto na SOT ou KMS. Não há ciclo: o transporte SOT herdado depende da representação e da fatoração ambiente, e a involução de J antecede estes módulos.

**Recompilação e evidência própria.**

{bt}
Executados apenas os três módulos novos e {link(RUN/'sources/RegularPolarAudit.lean','auditor próprio dos 16 alvos')}. Os **16 `#check` com universos e 16 `#print axioms`** foram lidos: tipos e domínios conferem, sem nova hipótese sobre `P : SiteProfile`; todos usam exatamente `propext`, `Classical.choice`, `Quot.sound`. A definição auxiliar de entrada no domínio também foi auditada. Os três `.olean` próprios são byte a byte iguais aos autorais. Não há `sorry`, `axiom`, `unsafe` ou alteração de redutibilidade nas fontes finais.

Foram relidos os pins de fonte/binário/JSON/streams dos logs finais `ScalarRegularRightPolar_20260912_172640_709275.json`, `ScalarRegularPolarCommutation_20260912_173018_646315.json` e `ScalarRegularRightContinuity_20260912_173508_422734.json`: rc0, fonte inalterada e saída existente. As tentativas **rc1** `172521_827544` e `172754_613488` foram lidas e preservadas, juntamente com backups de fonte cujo hash coincide com a fonte de cada tentativa. A primeira contém erros de coerção/rewrite/simplificação e `sorryAx` derivado da elaboração falha. A segunda contém timeout em `whnf`, constante desconhecida e impressões inválidas, inclusive ausência aparente de axiomas. **Nenhuma impressão dessas tentativas conta como aprovação.** Somente os rc0 dos bytes finais e os rc0 próprios sustentam este parecer; detalhes em {link(RUN/'author_history.json')} e capturas em `author_history/` e `author_source_history/`.

{link(RUN/'compilation.json')} SHA-256 `{hf(RUN/'compilation.json')}`; {link(RUN/'manifest.json')} SHA-256 `{hf(RUN/'manifest.json')}`. As **{len(m['dependencies'])} dependências de projeto** foram congeladas a partir das árvores próprias anteriores da direita regular e da involução de Tomita, com hashes das origens e dos pares fonte/binário. O grafo de imports foi conferido sem ciclos e as dependências compartilhadas coincidem. Reutilizada a errata somente de comentário já revisada de `DualSemifiniteIdeal`, explicitamente pinada. O `LEAN_PATH` contém apenas o build próprio e oito diretórios de pacotes externos readonly; nenhum build autoral de projeto. Compilador Lean 4.31.0, SHA-256 `{m['compiler_sha256']}`. Não se recompilaram biblioteca ou dependências antigas; sua validação matemática/binária anterior permanece herdada.

**Manifesto, documentação e preservação.**

{pins}
O relatório autoral foi lido integralmente e conserva corretamente o alcance acima, inclusive continuidade forte nova, identidade de J e limitação à conjugação dos geradores regulares. Suas frentes físicas e próximos passos são rotas abertas, não novas provas deste lote. A distinção documental `qgc_/qgp_/feed` versus anexo `kernel_frontier` é herdada da inspeção AST anterior; não houve nova auditoria do runtime. Os flags positivos do draft foram confrontados com os teoremas, não usados como prova por si mesmos.

A mãe é `regular_right_custody.json`, com os pins da tabela. As contagens **165 registros / 92 controles / 6753 Audit / 867 embutidos** pertencem ao estágio integrado anterior e não foram reapresentadas como nova execução deste DEV. Os 34 arquivos de memória e seus 34 backups foram apenas relidos, com hashes e prefixos preservados. Fontes/binários autorais, pareceres anteriores, dependências congeladas, manifesto/relatório e gate permaneceram intactos; cópia integrada SHA-256 `{m['working_sha256']}`. As seis flags maiores continuam falsas na evidência lida. A preservação do original é herdada da custódia/verificação materna; nenhum monólito, integrador ou recorder foi executado/importado por esta revisão, e toda escrita ficou em `revisao/`.

**Escopo DEV 3/16 encerrado sem P0–P2 ou análise necessária pendente.** [OPEN] Conjugação dos geradores da base e igualdade global `Jπ(N)J=π(N)'`, identificação de `A^it`/fluxo/KMS, traço e consumo pelos contratos/flags. A comutação nova de `R_t` com todo `π(N)` não supre essas obrigações. Integração e registro deste lote continuam pendentes e fora deste parecer; não há promoção de gate nem aprovação de runtime/QG.
'''
p=REV/'REVIEW_REGULAR_POLAR_DEV.md';assert not p.exists()
b=text.encode('utf-8');q=p.with_name(p.name+'.tmp')
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b;q.replace(p);assert p.read_bytes()==b
assert text.count('REGULAR_POLAR_DEV_REVIEW')==1
v={'timestamp':stamp,'report':str(p),'report_sha256':hf(p),'report_bytes':len(b),'report_lines':len(text.splitlines()),
   'modules':3,'targets':16,'own_executions_rc0':4,'three_binaries_identical':True,'only_trio':True,
   'manifest_sha256':hf(RUN/'manifest.json'),'compilation_sha256':hf(RUN/'compilation.json'),
   'P0':[],'P1':[],'P2':[],'memory_pairs_preserved':34,'integrated':False,'pending_analysis':False}
q=RUN/'verification.json';assert not q.exists();tmp=q.with_name(q.name+'.tmp');raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(q)
print(json.dumps(v,ensure_ascii=False,indent=2))
