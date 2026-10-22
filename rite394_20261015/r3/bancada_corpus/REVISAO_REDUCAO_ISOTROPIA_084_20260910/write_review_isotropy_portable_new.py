from pathlib import Path
import os, json, hashlib, re
from datetime import datetime, timezone

ROOT=Path(r"C:/IALD/Central de Patentes/Chatgpt")
OUT=ROOT/"REVISAO_REDUCAO_ISOTROPIA_084_20260910"
MAIN=ROOT/"REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md"
MANIFEST=MAIN.with_name("MANIFESTO_REDUCAO_ISOTROPIA_084.json")
SOURCES=[
MAIN,MANIFEST,
ROOT/"COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md",
ROOT/"REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md",
ROOT/"OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md",
ROOT/"REVISAO_OBSTRUCAO_CE_CORRENTE_082_20260910_053437_900535/PARECER_CLASSE_CE_E_CORRENTE_GRADIENTE_082.md",
ROOT/"COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md",
ROOT/"TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md",
ROOT/"TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md",
]
NOTE=r"""# Parecer independente084: eliminação finita da isotropia e canal de Euler

10/09/2026. [DERIVED — revisão matemática escrita independente da nova redução084]. [REAL — custódia documental]. Nenhuma execução matemática, CAS, Lean ou um.py. Todas as fontes anteriores preservadas.

**Parecer favorável no alcance declarado. Não identifiquei erro material** na [redução084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>). A forma normal finita e o critério
\[
J_W\nu\in dC_{\rm nat}^3
\quad\Longleftrightarrow\quad
J_W=\operatorname{div}_0V+K^2f_E,\qquad
f_E\in\mathscr N^{\mathfrak g},
\quad V\in(\mathscr N\otimes V_0)^{\mathfrak h}
\]
estão justificados no mesmo complexo fixado, sem presumir que \(\mathscr N^{\mathfrak g}=0\) ou que exista o par(V,f_E).

Li integralmente a fonte e seu manifesto. Também li as notas necessárias da corrente horizontal082, da transferência080, da redução081 e da transgressão076, e os pareceres independentes das duas entradas082.

**Proveniência.** A identificação CE082 e a redução081 são de minha autoria antecedente. Este parecer não é uma nova aprovação independente dessas provas. A identificação082 foi objeto do [parecer externo de Turing](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md>), aqui lido. A presente revisão avalia a nova eliminação vertical084 e sua composição com essas entradas. Meu controle breve por mensagem antes da escrita também não é contado como revisão integral prévia.

## 1. Módulo, decomposição e sinais de grau

O complexo é \(C^\bullet(\mathfrak g,\mathscr N)^{\mathfrak h}\), com
\(\mathscr N=R_{\rm her}\otimes\operatorname{Sym}^2\mathcal M\),
\(\mathfrak g=\mathfrak h\oplus V_0\), \(\mathfrak h=\mathfrak{so}(1,3)\) e \(\dim V_0=4\).
\(\mathcal M\) conserva suas relações de jatos/EOM. Não foi trocado por uma torre livre, nem o CE invariante pelo relativo.

A separação pelos números de ghosts p e θ tem
\[
d_0:(r,q)\mapsto(r,q+1),\quad
d_1:(r,q)\mapsto(r+1,q),\quad
d_2:(r,q)\mapsto(r+2,q-1).
\]
Os valores nos geradores preservam o sinal082:
\(dp=-\theta p\), \(d\theta=-\theta^2+Kpp^\flat\).
O ghost θ é a parte antissimétrica de ∇C, não o m covariante elevado de sinal oposto.

O diferencial vertical inclui a ação de isotropia nos coeficientes E_r=\(\mathscr N\otimes\Lambda^rV_0^*\), inclusive nos ghosts p. Com o shuffle graduado declarado, é o CE de h nesses coeficientes. Um sinal global dependente de r sob outra ordem de escrita é absorvido nesse shuffle; não altera o cálculo de cohomologia e não autoriza retirar os sinais nas subtrações dR.

As identidades de bigrau extraídas de d²=0 estão completas. Em particular, \(d_1^2\) não é tomado como zero no complexo inteiro: ele é compensado por \(\{d_0,d_2\}\). A nulidade de \(d_{\rm rel}^2\) na linha horizontal invariante usa especificamente d0=0 e d2=0 nessa linha.

## 2. O uso da cohomologia finita de h é legítimo

Um elemento de E_r usa finitíssimos jatos de Weyl e coeficientes escalares. Seu fecho por h está contido num espaço tensorial finito de mesma ordem de jatos. A passagem ao quociente das EOM não aumenta a dimensão desse corte. A extensão por escalares inertes conserva essa afirmação elemento a elemento.

d0 preserva tal corte. Não é necessário que ele seja preservado por transvecções, e a nota não faz essa suposição. Após aplicar d1 numa das subtrações, basta tomar um corte maior, ainda finito. Existem somente três etapas de eliminação vertical.

Conferi diretamente a fonte primária indicada: [Chevalley–Eilenberg1948, teoremas19.1 e24.1](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf). O primeiro identifica a cohomologia trivial com cochains invariantes; o segundo elimina a cohomologia em irreps FINITAS não triviais de uma álgebra semissimples. A decomposição finita em irreps separa o coeficiente trivial. Essa importação é aplicada à h, não a um suposto módulo finito da álgebra g inteira.

Para uma primitiva vertical de um ciclo invariante, há também controle de naturalidade: escolha o corte finito que contém a primitiva e seu ciclo, e projete a primitiva para a parte h-invariante. O diferencial comuta com essa projeção, logo sua imagem continua sendo o ciclo dado. É uma cisão equivarante finita, não integração sobre o grupo Lorentz não compacto.

Como \(\Lambda^q\mathfrak h\) é finita, cochains CE comutam com a união filtrante desses cortes. A cohomologia também comuta com esse limite DIRETO de espaços vetoriais. Assim a igualdade vertical
\[
H^q(C^{r,\bullet},d_0)
=(\mathscr N\otimes\Lambda^rV_0^*)^{\mathfrak h}
 \otimes H^q(\mathfrak h,\mathbb R)
\]
é justificada. Não envolve um limite inverso ou a completação em infinitas derivadas dentro de um coeficiente.

A complexificação de h em dois fatores sl2 fornece duas classes reais de Cartan em grau3, e uma em grau6, além da unidade de grau0. H¹ e H² são zero. Esse passo usa o compacto dual dos dois fatores, ou equivalentemente seus módulos exteriores; não substitui h pelo seu subgrupo compacto máximo so(3), cuja única classe3 daria uma contagem incorreta.

## 3. As cúbicas e o termo de curvatura

Os bilineares \(B_{\rm tr}=\operatorname{tr}(XY)\) e
\(B_E=\varepsilon_{abcd}X^{ab}Y^{cd}/24\)
são invariantes e independentes sobre h. Seus cociclos \(-B(\theta,\theta^2)/3\) dão as duas Cartan verticais. A normalização de B_E está explícita, não é herdada de uma ocorrência homônima de Euler em outra nota.

Revi a identidade
\[
\operatorname{CS}_B=B(\theta,F)-\tfrac13B(\theta,\theta^2),
\quad F=Kpp^\flat,\qquad
d\operatorname{CS}_B=B(F,F).
\]
É a Chern–Simons graduada com \(d\theta=F-\theta^2\). A relação \(dF=F\theta-\theta F\) segue de dp e do abaixamento métrico, e a invariância de B cancela os termos de conexão. Trata-se de um polinômio finito em ghosts; não é uma troca da curvatura de fundo pela curvatura dinâmica.

Para o traço, \(p_bp^b=0\) dá \(\operatorname{tr}(F^2)=0\). Para B_E, \(F^{ab}=Kp^ap^b\) e \(\varepsilon pppp=24\nu\) dão
\[
d\operatorname{CS}_{\rm tr}=0,\qquad
d\operatorname{CS}_E=K^2\nu.
\]
Os sinais e o fatorK² estão corretos. Um coeficiente f somente h-invariante produziria adicionalmente df∧CS; essa parcela é eliminada apenas DEPOIS da condição f∈\(\mathscr N^{\mathfrak g}\) demonstrada no passo seguinte.

## 4. A eliminação vertical não salta a condição sobre os coeficientes

Decompõe-se Q em Q03+Q12+Q21+Q30 e supõe-se que dQ tenha somente bigrau(4,0).

A equação(0,4) permite escrever
\[
Q_{0,3}=f_{\rm tr}\tau_{\rm tr}+f_E\tau_E+d_0R_{0,2},
\qquad f_i\in\mathscr N^{\mathfrak h}.
\]
Subtrair dR02 conserva dQ e remove a peça vertical exata. Os termos de d1R02 e d2R02 permanecem nas outras componentes; não foram apagados.

A equação seguinte, de bigrau(1,3), diz que
\[
\sum_i(d_{\rm rel}f_i)\otimes[\tau_i]=0
\]
na cohomologia vertical. Os \(d_{\rm rel}f_i\) já pertencem ao setor invariante dos coeficientes \(\mathscr N\otimes V_0^*\); não são classes de grau vertical positivo que ainda possam ser anuladas por uma fronteira nesse coeficiente. A independência das duas Cartan força cada um a zero. Isso é precisamente \(\rho_{P_a}f_i=0\) para todos os a. Junto à invariância por h, conclui-se f_i∈\(\mathscr N^{\mathfrak g}\).

Esse é o ponto decisivo: os coeficientes são invariantes sob g por uma equação, não por uma aplicação indevida de Whitehead ou por serem escalares de Lorentz.

Pode-se então subtrair \(\sum_i f_i\operatorname{CS}_i\): dfi=0, e a mudança em dQ é inteiramente horizontal. Q03 fica zero.

A equação(1,3) remanescente torna Q12 verticalmente fechada. Hh²=0 permite Q12=d0R11 com R11 invariante e finita. Subtrair dR11 remove Q12, conservando seus efeitos em Q21/Q30. A equação(2,2) torna Q21 verticalmente fechada; Hh¹=0 fornece R20, e a última subtração deixa Q30. Nenhuma subtração recria uma componente de menor número de p, pois d1 e d2 só aumentam esse número.

Somar os três R dá a forma normal
\[
Q=q_V+f_{\rm tr}\operatorname{CS}_{\rm tr}
      +f_E\operatorname{CS}_E+dR.
\]
O termo fechado de traço é conservado, sem reivindicar unicidade da decomposição ou exaustão de H³ para dQ arbitrário não horizontal.

## 5. Necessidade e suficiência no mesmo módulo

A orientação identifica Q30 com um vetor quadrático natural V:
\(q_V=\varepsilon_{abcd}V^ap^bp^cp^d/3!\).
A [identidade da corrente082](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>) dá \(dq_V=(\operatorname{div}_0V)\nu\), sem passar a um quociente por divergências.

Aplicar d à forma normal prova a necessidade:
\(J_W=\operatorname{div}_0V+K^2f_E\).
A identificação com o coeficiente de ν é injetiva, pois \(\Lambda^4V_0^*\) tem a base não nula ν e estamos no mesmo módulo de coeficientes. A recíproca é a construção explícita \(Q=q_V+f_E\operatorname{CS}_E\). A direção “se” não presume uma primitiva natural maior que a classe usada na direção “somente se”.

A nota conserva \(\mathscr N\) como módulo QUADRÁTICO. A unidade do anel escalar não é automaticamente um elemento desse módulo, e J_W ser um escalar de h não implica que seja invariante por transvecções. Portanto o critério não foi tornado tautológico acrescentando livremente um f de grau zero.

K² permanece visível. Com K real fixo não nulo, multiplicar por K² é uma unidade; num anel restrito em K variável essa substituição exige outra tipagem. Igualmente, restrições suplementares de engenharia ou admissibilidade causal não são dispensadas por uma solução no módulo maior.

## 6. A organização por páginas concorda com a prova finita

A filtração por grau horizontal tem somente r=0,…,4. A página vertical possui linhas q=0,3,6, e d1 induz o complexo horizontal relativo B. Os diferenciais das páginas2 e3 têm alvos em linhas vazias, portanto são nulos.

O único canal que atinge(4,0) é
\[
d_4:E_4^{0,3}=\mathscr N^{\mathfrak g}\otimes\mathbb R^2
\longrightarrow E_4^{4,0}=H^4(B).
\]
Sua realização pela Chern–Simons é zero para traço e \([K^2f\nu]\) para Euler. A nota mantém ainda a possibilidade do canal(0,6)→(4,3); não declara todas as Cartan permanentes. Não há novo diferencial de página superior a4 por falta de posições horizontais.

Essa descrição não usa uma hipótese Mittag–Leffler. A forma normal já provou diretamente a afirmação sobre a imagem em grau4; a sequência espectral finita é uma organização adicional, não uma inferência que esconda uma extensão de cohomologias.

## 7. Limites e conclusão da revisão

Não identifiquei erro material. A redução fornece um critério necessário e suficiente dentro do CE natural fixado e diminui o tipo de ghosts que precisa ser examinado. A obtenção das primitivas verticais é finita e h-invariante, e os coeficientes das Cartan são obrigados a pertencer a \(\mathscr N^{\mathfrak g}\).

Não foi calculado esse último módulo, nem demonstrada sua nulidade. Não foi encontrado V que produza J_W modulo o canal de Euler. Não há classificação total de derivadas, extensão ao fundo físico φ=id, afirmação de regularidade universal em K, admissibilidade Q2, QME ou UV.

Os cálculos083 não são usados nesta prova084 nem incorporados retroativamente na entrega anterior. Este parecer é novo; os controles documentais do recibo não são teoremas Lean, CAS ou execução de um.py.
"""
def pin(p):
    b=p.read_bytes()
    return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def emit(path,data):
    if path.exists():raise FileExistsError(path)
    temp=path.with_name(path.name+".pending")
    with temp.open("xb") as out:
        out.write(data);out.flush();os.fsync(out.fileno())
    if temp.read_bytes()!=data:raise RuntimeError("Temp mismatch")
    temp.rename(path)
    if path.read_bytes()!=data:raise RuntimeError("Final mismatch")
    return pin(path)
OUT.mkdir(parents=True,exist_ok=True)
before=[pin(p) for p in SOURCES]
self_before=pin(Path(__file__).resolve())
m=json.loads(MANIFEST.read_text(encoding="utf-8"))
assert m["all_sources_unchanged"] and m["sources_before"]==m["sources_after"]
refs=[m["note"]]+m["sources_after"]
ref_checks=[{"pin":r,"matches":(actual:=pin(Path(r["path"])))["bytes"]==r["bytes"] and actual["sha256"]==r["sha256"]} for r in refs]
if not all(x["matches"] for x in ref_checks):raise RuntimeError("Manifest reference mismatch")
source_links=re.findall(r"\]\(<(C:/[^>]+)>\)",MAIN.read_text(encoding="utf-8"))
review_links=re.findall(r"\]\(<(C:/[^>]+)>\)",NOTE)
links=[{"path":p,"exists":Path(p).is_file()} for p in source_links+review_links]
if not all(x["exists"] for x in links):raise RuntimeError("Missing link")
note_pin=emit(OUT/"PARECER_ELIMINACAO_FINITA_E_CANAL_EULER_084.md",NOTE.encode("utf-8"))
after=[pin(p) for p in SOURCES]
self_after=pin(Path(__file__).resolve())
if before!=after or self_before!=self_after:raise RuntimeError("Changed input")
record={
"created_utc":datetime.now(timezone.utc).isoformat(),
"verdict":"FAVORABLE_NO_MATERIAL_ERROR_IDENTIFIED_IN_STATED_SCOPE",
"source":pin(MAIN),"artifacts":[note_pin],
"sources_before":before,"sources_after":after,"all_sources_unchanged":before==after,
"script_before":self_before,"script_after":self_after,"script_unchanged":self_before==self_after,
"manifest_reference_checks":ref_checks,"local_link_checks":links,
"documentary_counts":{"preserved_sources":len(before),"reference_pins":len(ref_checks),"reference_pins_pass":sum(x["matches"] for x in ref_checks),"links":len(links),"links_pass":sum(x["exists"] for x in links)},
"primary_read":{"url":"https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf","scope":"Theorems19.1 and24.1 and proof paragraphs, applied to finite h-modules only","ams_fetch":"403; primary paper read through Rochester mirror"},
"new_mathematical_executions":0,"new_lean_runs":0,"um_py_executed_or_imported":False,
"existing_files_modified":False,
"independence":"Reviewer authored antecedents081/082; this review is of the new084 reduction. External082 review was read and not replaced by self-approval."
}
record_pin=emit(OUT/"REGISTRO_REVISAO_REDUCAO_ISOTROPIA_084.json",(json.dumps(record,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"review":note_pin,"record":record_pin,"documentary_counts":record["documentary_counts"]},ensure_ascii=False,indent=2))

