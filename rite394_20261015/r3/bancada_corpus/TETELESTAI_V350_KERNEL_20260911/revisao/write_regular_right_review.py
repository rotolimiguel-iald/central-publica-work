"""Create the delimited DEV report from independently measured evidence."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=Path((REV/'regular_right_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
m=load(RUN/'manifest.json'); c=load(RUN/'compilation.json')
assert all(v is True for k,v in c.items() if k!='records')
assert len(m['sources'])==3 and len(m['declarations'])==36 and len(c['records'])==4
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
    bt+='| '+link(r['stdout'],Path(r['module']).stem)+' | '+str(r['returncode'])+' | `'+r['output_sha256']+'` | '+('idêntico ao autor' if r.get('binary_equals_author') else 'auditor 36/36')+' |\n'
pins='| Artefato lido | SHA-256 |\n|---|---|\n'
for n,h in m['artifact_pins'].items():pins+='| '+link(ROOT/n)+' | `'+h+'` |\n'
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''Parecer DEV — direita unitária regular e domínio do mesmo S†S

REGULAR_RIGHT_DEV_REVIEW

{stamp}. **Sem achados P0–P2. Escopo DEV concluído: três módulos, 36 alvos (17 + 10 + 9).** [REAL — leitura integral das fontes, manifesto e relatório; recompilações e auditor próprios.] A família direita construída é unitária no mesmo `ScalarGNSHilbert P` e preserva o domínio completo de `scalarTomitaSquare P`, com comutação nesse domínio. Não se certifica integração deste lote.

{table}
Em {line('ScalarRegularRightGNS',12)}, `λ_t` é o `regularUnitary P t` pertencente à mesma álgebra `N`. As linhas 20–36 provam `ν((aλ_t)*aλ_t)=ν(a*a)` e constroem o produto dentro de `scalarWeightLeftIdeal P=nν`. A invariância herdada usa `λ_t* a λ_t`, com a orientação correta; ela decorre da comutação das translações com `N`, da lei bimodular da integral e do vetor fixado pelo fluxo da fibra, sem hipótese KMS. A igualdade vale em ENNReal; a finitude do produto segue da finitude recebida de `a`, sem converter infinito por `toReal`.

Em {line('ScalarRegularRightGNS',40)}, o ambiente é literalmente `L²(ℝ,L²(ℝ,TowerHilbert P))`, com Lebesgue em ambas as coordenadas. Para parâmetro `t`, o caráter exterior é `exp(-i*t*s)` e a translação interior tem convenção `f(x-t)`. `characterPhase_comm` troca os fatores reais `t,s`, sem inverter o sinal. `fibre (shift t)` e o caráter exterior comutam porque atuam em coordenadas distintas; a prova não aplica indevidamente a relação de Weyl da mesma coordenada. Nas linhas 70–84, o entrelaçamento usa exatamente `scalarOrbit_right_regular`, o mesmo `regularVacuum P` e o mesmo fator `sqrt(dualHaarFactor)`; são quatro igualdades a.e. para `a,t` fixados, sem uniformização a.e. não enumerável.

Em {line('ScalarRegularRightGNS',86)}, a imagem do domínio escalar completo é preservada e a continuidade do operador limitado transporta seu fecho. A igualdade herdada `scalarWeight_completion_eq` identifica esse fecho com o `H_I` anterior; não afirma `I=nν`. A restrição da linha 95 atua nesse mesmo subespaço. As linhas 103–128 provam composição, adjunto `R_t*=R_(-t)` e as duas identidades de inversa; a igualdade do adjunto é verificada por pareamentos no Hilbert restrito, não presumida pela notação. Não se introduz hipótese adicional sobre `P`.

Em {line('ScalarRegularRightTomita',12)}, `aλ_t` preserva `nν∩nν*`: a finitude da estrela usa `(aλ_t)*=λ_t* a*` e a propriedade de ideal esquerdo. As linhas 27–38 identificam a segunda coordenada com `π(λ_t*)Λ(a*)`. O mapa de pares `(x,z)↦(R_t x,π(λ_t*)z)` é contínuo, preserva o gráfico algébrico do peso e, pelas linhas 59–64, o fecho do gráfico original. Assim as linhas 66–84 fornecem pertinência real a `D(S)` e **`S R_t x=π(λ_t*) Sx` para todo `x∈D(S)`**, usando univalência do fecho. Não se pressupõe continuidade de `S`, nem que todo seu domínio seja imagem algébrica de `nν∩nν*`.

Em {line('ScalarRegularRightSquare',16)}, o pareamento complexo é quantificado sobre todo `D(S)` e usa a identidade de adjunto da mesma representação `π`. A maximalidade já construída de `F=S†` fornece **`π(λ_t)z∈D(F)` e `Fπ(λ_t)z=R_t*Fz`**. A escolha na linha 52 escolhe a prova de pertinência do vetor já determinado; não troca esse vetor nem escolhe outro adjunto. A orientação dos produtos internos coincide com a convenção antilinear do primeiro argumento e com `⟨Sx,z⟩=⟨Fz,x⟩`.

Em {line('ScalarRegularRightSquare',70)}, o domínio herdado é exatamente **`x∈D(S)` e `Sx∈D(F)`**, e `A=scalarTomitaSquare P` é a composição efetiva `FS`. As duas pertinências de `R_t x` são provadas; a segunda aplica a lei do adjunto em `-t`, pois `λ_t*=λ_(-t)`. As linhas 85–102 identificam por `Subtype.ext` as entradas no mesmo `F` e obtêm **`A R_t x=R_t Ax` em todo `D(A)`**, usando `R_(-t)*=R_t`. A equivalência da linha 105 vale para qualquer vetor ambiente: a direção inversa aplica a inclusão já provada a `R_(-t)` e cancela `R_(-t)R_t=I`. Não há premissa residual de invariância de domínio ou de comutação, nem restrição oculta ao núcleo algébrico.

**Evidência própria e proveniência.**

{bt}
Executados somente os três módulos e {link(RUN/'sources/RegularRightAudit.lean','o auditor próprio')}. Os **36 `#check` com universos e 36 `#print axioms`** foram conferidos, incluindo as definições: nomes exatos, tipos/domínios acima e somente `propext`, `Classical.choice`, `Quot.sound`. Os três binários coincidem byte a byte com os autorais. Nenhum `sorry`, `axiom`, `unsafe` ou alteração de redutibilidade nas novas fontes. O warning de deprecação de `ContinuousLinearMap.one_apply` na linha 113 do terceiro módulo é benigno e está preservado no stdout.

Foram relidos os três JSONs finais autorais indicados no manifesto, seus streams e os pares fonte/binário: rc0, fonte inalterada durante compilação, saída existente e todos os hashes coincidentes. O histórico delimitado encontrado contém somente essas tentativas Lean finais, sem rc1. A falha auxiliar de impressão cp1252 mencionada no relatório não foi tomada como evidência de compilação; a aceitação se apoia nos bytes e logs lidos e nas execuções próprias.

{link(RUN/'manifest.json')} SHA-256 `{hf(RUN/'manifest.json')}`; {link(RUN/'compilation.json')} SHA-256 `{hf(RUN/'compilation.json')}`. Foram reutilizadas **{len(m['dependencies'])} dependências de projeto** alcançáveis a partir das três fontes, com fontes/binários congelados provenientes da árvore própria `right_square_independent_20260912_164053_083979`; os hashes da origem estão no manifesto. O grafo de imports foi percorrido sem ciclo. Preservada a errata exclusivamente documental, já revisada e pinada, de `DualSemifiniteIdeal`. O `LEAN_PATH` contém somente o build desta revisão e oito diretórios de pacotes externos readonly, sem build autoral de projeto. Pacotes e dependências não foram recompilados; a evidência binária anterior é herdada. Compilador Lean 4.31.0, SHA-256 `{m['compiler_sha256']}`. Todas as saídas próprias estão em `revisao/`.

**Pins documentais e fronteira.**

{pins}
O relatório autoral foi lido integralmente e descreve corretamente a família `λ_t`, o domínio composto completo e as limitações. O manifesto mantém `integrated=false`, KMS/identificação do fluxo/gate falsos e revisão pendente na data de sua emissão; não foi alterado por esta revisão. A mãe integrada é `right_square_custody.json`. Seus números **162 registros / 91 controles / 6717 Audit / 864 embutidos** pertencem ao estágio anterior: não houve nova revisão integrada nem repetição de testes autorais nesta tarefa.

Os **34 arquivos de memória e seus 34 backups imediatos** foram relidos, com hashes e prefixos byte a byte preservados. Fontes/binários do autor, dependências congeladas, pareceres anteriores, artefatos pinados, gate e cópia integrada permaneceram inalterados. Hash lido da cópia: `{m['working_sha256']}`. As seis flags maiores continuam falsas na evidência lida. A preservação canônica do estágio mãe é herdada da custódia/verificação lida; nenhum monólito, integrador, recorder ou teste autoral foi executado nesta revisão, e nenhuma memória foi escrita.

**Conclusão delimitada:** DEV 3/36 encerrado sem P0–P2 ou análise necessária pendente. [OPEN] Identificação de `A^it` com o fluxo candidato, KMS global, extensão da direita a toda `N`, traço e consumo pelos contratos/flags. Este pacote também não prova nova continuidade forte em `t`; continuidade dos mapas de gráfico em seus vetores é uma afirmação diferente. As fronteiras são limites esperados, não defeitos destas provas. Integração e registro deste lote permanecem fora desta conclusão.
'''
p=REV/'REVIEW_REGULAR_RIGHT_DEV.md'; b=text.encode('utf-8')
assert not p.exists(), 'Existing review must be preserved; use a byte backup and explicit addendum.'
q=p.with_name(p.name+'.tmp')
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b; q.replace(p); assert p.read_bytes()==b
assert text.count('REGULAR_RIGHT_DEV_REVIEW')==1
v={'timestamp':stamp,'report':str(p),'report_sha256':hf(p),'report_bytes':len(b),'report_lines':len(text.splitlines()),
   'modules':3,'targets':36,'own_executions_rc0':4,'three_binaries_identical':True,'only_trio':True,
   'manifest_sha256':hf(RUN/'manifest.json'),'compilation_sha256':hf(RUN/'compilation.json'),
   'P0':[],'P1':[],'P2':[],'memory_pairs_preserved':34,'integrated':False,'pending_analysis':False}
q=RUN/'verification.json'; assert not q.exists(); tmp=q.with_name(q.name+'.tmp'); raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw; tmp.replace(q)
print(json.dumps(v,ensure_ascii=False,indent=2))
