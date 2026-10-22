from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import uuid

WORK = Path("C:/IALD/Central de Patentes/Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
if not OUT.is_relative_to(WORK):
    raise RuntimeError("Unauthorized output")
FILES = {
    "criterion": "NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md",
    "normal": "HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md",
    "frame": "HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md",
    "rees": "COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md",
    "q2": "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md",
    "admissible": "COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md",
    "ward": "COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md",
    "smooth071": "COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md",
    "spectator073": "COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md",
    "descent": "DESCIDA_NATURAL_SIMBOLOS_075_20260910/DESCIDA_NATURAL_POR_OPERADORES.md",
    "first_descent": "DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md",
    "descent_application": "APLICACAO_DESCIDA_OFFSHELL_075_20260910_022420_157704/APLICACAO_OFFSHELL_E_FONTES_CENTRAIS.md",
    "page085": "PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md",
    "corollaries086": "COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/COHOMOLOGIA_CE3_E_IMAGEM_CUBICA_ZERO_APOS_C6.md",
    "review086": "REVISAO_COROLARIOS_CE_LIDER_086_20260910/PARECER_COROLARIOS_CE_E_IMAGEM_CUBICA_086.md",
    "review085": "REVISAO_PRIMEIRA_PAGINA_085_20260910_062843_679705/PARECER_TODAS_VALENCIAS_E_INVARIANTES_085.md",
}

def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    st = path.stat()
    return {
        "path": path.as_posix(), "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(), "mtime_ns": st.st_mtime_ns,
    }, data

def publish(path, data):
    path = Path(path).resolve()
    if not path.is_relative_to(OUT) or path.exists():
        raise RuntimeError("Output must be new inside review folder")
    temp = path.with_name(path.name + ".pending_" + uuid.uuid4().hex)
    with temp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError("Temporary verification failed")
    if path.exists():
        raise FileExistsError(str(path))
    os.rename(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError("Final verification failed")
    return pin(path)[0]

def publish_json(path, value):
    return publish(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

before, content = {}, {}
for key, relative in FILES.items():
    before[key], data = pin(WORK / relative)
    content[key] = data.decode("utf-8-sig")
before["helper"], _ = pin(__file__)
anchors = {}
def loc(key, needle, label, anchor_name):
    hits = [(n, text) for n, text in enumerate(content[key].splitlines(), 1) if needle in text]
    if len(hits) != 1:
        raise RuntimeError("Anchor not unique: " + anchor_name + " " + str(hits))
    n, fragment = hits[0]
    target = before[key]["path"] + ":" + str(n)
    anchors[anchor_name] = {"source": key, "path": before[key]["path"], "line": n, "fragment": fragment}
    return "[" + label + "](<" + target + ">)"

LINKS = {
    "@CRITERION": loc("criterion", "## 6. Critério suficiente", "critério074, seção6", "criterion_section"),
    "@ZEROS": loc("criterion", "H^1(s)=H^2(s)=H^5(s)=0", "nulidades074, equação6.2", "criterion_zeros"),
    "@GROUPS": loc("criterion", r"E_2^{4,1}=H^1", "grupos074, equação6.3", "criterion_groups"),
    "@S_TRANSPORT": loc("criterion", "**Limite da entrada073:**", "limite do transporte de primitivas073→074", "ordinary_to_formal"),
    "@EULER": loc("criterion", "## 3. Contraexemplo relativo", "controle Euler074", "euler_counterexample"),
    "@Q_RECURRENCE": loc("normal", r"sT_q+E_NT_{q-1}+C_NT_{q-2}", "recorrência074, equação17", "normal_recurrence"),
    "@FORM_FILTER": loc("normal", "## 7. Filtração natural correta", "filtração por formas074", "form_filtration"),
    "@BACKGROUND": loc("normal", r"boxed{E_N B_{0,I}", "ação de E_N nos jatos de B0", "background_horizontal"),
    "@FRAME": loc("frame", "## 2. Teorema que permanece", "precisão métrica074", "metric_presentation"),
    "@REES_DEF": loc("rees", "## 2. Convenções e classe formal", "classe Rees074", "rees_definition"),
    "@REES_B": loc("rees", "## 4. Teorema da translação", "continuidade da translação074", "rees_translation"),
    "@REES_LIMIT": loc("rees", "Essa equivalência não afirma que o complexo", "limite das homotopias074", "rees_other_homotopies"),
    "@Q2_DOMAIN": loc("q2", r"Trabalhe em \(M=", "domínio físico Q2_069", "physical_domain"),
    "@Q2_ANOMALY": loc("q2", "## 6. A anomalia existe", "Ward e consistência Q2_069", "q2_anomaly"),
    "@Q2_REMOVE": loc("q2", r"Para remover \(a_N\)", "obrigação de remoção Q2_069", "q2_removal"),
    "@ADMISSIBLE": loc("admissible", "## 3. A primitiva precisa", "contrato de normalização072", "normalization_class"),
    "@REGULARITY": loc("admissible", "## 4. Suave e analítico", "precisão de regularidade072", "regularity"),
    "@CONTACTS": loc("admissible", "## 5. Escala, pernas e contatos", "escala e contatos072", "contacts"),
    "@SPLIT": loc("admissible", "## 6. A obrigação adicional", "comparação entre fundos072", "split_background"),
    "@ORDINARY": loc("spectator073", "## 4. As entradas", "nulidades ordinárias073", "ordinary_cohomology"),
    "@REFERENCE_DOMAINS": loc("spectator073", "## 7. Três sentidos", "três domínios de B0 na073", "reference_domains"),
    "@SMOOTH": loc("smooth071", "## 4. Por que o qualificador", "diferença suave/racional071", "smooth_rational"),
    "@DESCENT": loc("descent", "## 8. Completação perturbativa", "controle Rees da descida075", "descent_rees"),
    "@FIRST_DESCENT": loc("first_descent", "## 2. A descida completa", "primeiro descendente075", "first_descent"),
    "@DESCENT_APPLICATION": loc("descent_application", "## 7. Resultado e contrato", "aplicação off-shell075", "descent_application"),
    "@DESCENT_COEFS": loc("descent_application", "## 4. Por que B0 on-shell", "quociente diferencial apenas de coeficientes075", "coefficient_quotient"),
    "@CENTRAL": loc("descent_application", "## 5. Fontes centrais", "fontes centrais e três projeções075", "central_sources"),
    "@PAGE085": loc("page085", "H^q(s0)|_E =", "fórmula de primeira página085", "valence_page"),
    "@CE085": loc("page085", "## 3. O primeiro diferencial", "identificação CE085", "first_ce_differential"),
    "@INVARIANTS": loc("page085", "## 4. Invariantes de qualquer", "invariantes positivos085", "positive_invariants"),
    "@COROLLARY086": loc("corollaries086", "## 2. H³ do complexo", "H³ CE quadrático086", "ce3_vanishes"),
    "@PONTRYAGIN086": loc("corollaries086", "## 3. A linha de Pontryagin", "linha CE Pontryagin086", "ce4_pontryagin"),
    "@CUBIC086": loc("corollaries086", "## 4. A imagem em", "destino da imagem cúbica086", "cubic_image"),
    "@FORMAL086": loc("corollaries086", "## 5. Projeção formal", "projeção formal086", "formal_projection"),
}

note = r"""# Critério de anomalias074: contrato exato e contribuição dos resultados085–086

10/09/2026. Etapa087, independente de novos cálculos de N₁/N₂ em andamento. [DERIVED — auditoria de composição e tipagem]. [REAL — leitura, linhas e pins medidos no manifesto]. Zero execução matemática, CAS ou Lean; nenhum um.py executado/importado; nenhum original alterado.

**Resultado:** a074 fornece um critério SUFICIENTE para eliminar o grau total cinco de um complexo natural de formas. Ele usa H(s) do BRST clássico COMPLETO, e não H(s₀) ou CE da primeira página por valência. A descida075 satisfaz um antecedente importante desse critério no domínio de aplicação declarado. Os resultados085/086 fornecem cálculos efetivos numa referência espaço-forma com sigma constante, mas não satisfazem automaticamente as cinco hipóteses de nulidade do critério na classe causal física.

Em particular, a074 NÃO exige H³(s)=0 nem H⁴(s)=0. Exige dois grupos horizontais com esses módulos de coeficientes. Uma classe não nula de H⁴(s), caso venha a ser demonstrada, não é por isso uma anomalia ou uma refutação desse critério.

## 1. Fontes da afirmação e definição do diferencial

O enunciado está em @CRITERION, equações6.1–6.3. A conjugação e seus limites estão em @FORM_FILTER e @FRAME. A fonte original que admitia também vielbein deve ser lida com a precisão: o operador que anula o ghost Lorentz convencional não é natural sob frames LOCAIS. A apresentação MÉTRICA mínima usada por Q2 permanece no alcance. Uma comparação prévia com vielbein exige o domínio formal e o transporte canônico explicitados na070; não cria a extensão de frame do operador antigo.

Depois de desfazer o gauge e contrair pares não mínimos no domínio apropriado, escreva

    Q_N = e^(−b_N)(s+d_H)e^(b_N) = s + E_N + C_N,
    bideg(s)=(1,0), bideg(E_N)=(0,1), bideg(C_N)=(−1,2).

Os pares nesta nota são (ghost g, forma q). A álgebra inclui os campos completos mínimos e antifields, e B0 como espectador de ghost zero. sB0=0, mas @BACKGROUND mostra E_N B0=d_HB0. Portanto não se pode trocar E_N pela derivada exterior somente em coordenadas, ou zerar derivadas de coeficientes de fundo.

As identidades são

    s²=0, {s,E_N}=0, E_N²=−{s,C_N},
    {E_N,C_N}=0, C_N²=0.

E_N é diferencial apenas depois de passar a H(s). C_N participa dos passos posteriores. O termo explícito C_N(∇̄c)=−R̄ impede ignorá-lo até no fundo físico FRW da construção Q2. A covariância conjunta/passiva dos campos e B0 é distinta do gauge dinâmico s, que fixa B0.

## 2. Os cinco grupos: notação sem ambiguidade de índices

Seja C_nat^(g,q) a classe de formas naturais efetivamente escolhida, com seus coeficientes, completação e grau de regularidade. Para não ocultar o grau de forma, escreva

    H_s^(g,q) := H^g(C_nat^(•,q),s).

Filtrando Q_N pelo grau de forma, denote a primeira página por E_F,1^(g,q)=H_s^(g,q). O próximo diferencial é Ebar_N induzido por E_N. O critério da fonte usa @ZEROS e @GROUPS para eliminar todos os canais g+q=5.

| Canal (ghost, forma) | Hipótese suficiente precisamente tipada | Página em que desaparece |
|---|---|---|
| (5,0) | H_s^(5,0)=0 | Primeira |
| (4,1) | ker[Ebar:H_s^(4,1)→H_s^(4,2)] / im[Ebar:H_s^(4,0)→H_s^(4,1)] = 0 | Segunda |
| (3,2) | ker[Ebar:H_s^(3,2)→H_s^(3,3)] / im[Ebar:H_s^(3,1)→H_s^(3,2)] = 0 | Segunda |
| (2,3) | H_s^(2,3)=0 | Primeira |
| (1,4) | H_s^(1,4)=0 | Primeira |

A abreviação H¹(s)=H²(s)=H⁵(s)=0 da074 é uma condição uniforme mais forte que as três componentes mostradas. Para consumo basta controlar as componentes pertinentes, mas não se deve identificar H_s^(g,q) com um grupo de zeroformas multiplicado por formas arbitrárias sem demonstrar o mapa na categoria natural com B0. O grau q das duas cohomologias horizontais também é parte do contrato.

As expressões H¹(Ebar;H⁴(s)) e H²(Ebar;H³(s)) são, respectivamente, os quocientes da segunda e terceira linhas. O primeiro número é FORMA HORIZONTAL, não ghost físico nem laço. Não se substituem por H¹_dR(S³) e H²_dR(S³): os coeficientes são a cohomologia DINÂMICA, e Ebar deriva os dados externos remanescentes.

Há cinco níveis de forma, q=0,…,4. Se os cinco termos indicados são zero, os subquocientes posteriores continuam zero e H⁵(Q_N)=0. A filtração por forma é finita; essa inferência não precisa de Mittag-Leffler ou de um limite inverso em forma.

A recíproca não foi afirmada e é falsa como princípio de sequências espectrais: uma entrada não nula na primeira ou segunda página pode ser eliminada por um diferencial posterior. Também basta, para uma quebra concreta, que SUA classe seja exata, mesmo que outros elementos de H⁵(Q_N) não o sejam. O critério suficiente evita calcular essas alternativas; não as exclui.

## 3. O que é preciso construir se não forem provadas as nulidades inteiras

A @Q_RECURRENCE oferece uma obrigação mais localizada. Para um cociclo total Ω de grau cinco e uma primitiva candidata T de grau quatro,

    sT_q + E_N T_(q−1) + C_N T_(q−2) = Ω_q,
    T_(−1)=T_(−2)=0, 0≤q≤4.

Aqui Ω_q tem ghost 5−q e T_q tem ghost 4−q. Se as equações anteriores valem, U_q=Ω_q−E_NT_(q−1)−C_NT_(q−2) é s-fechado. Pode-se resolver cada classe concreta de U_q em vez de provar uma nulidade global desnecessariamente forte. Nas etapas q=1/2, mudar primitivas anteriores é precisamente o mecanismo codificado pelos quocientes horizontais do §2.

Para orientação dos próximos mapas por FORMAS: se a é s-fechado e E_N a=−sb, o segundo diferencial é representado por

    C_N a + E_N b,

de bidegrau (ghost−1, forma+2), módulo os ajustes da página pertinente. A igualdade s(C_Na+E_Nb)=0 segue de E_N²=−{s,C_N} e {s,E_N}=0. Este é um controle de sinais e graus, não o cálculo de sua classe. Em geral o r-ésimo diferencial por formas tem bidegrau (1−r,r). Ele não é o s_r da expansão por valência.

Se a solução T existir na classe correta, e^(b_N)T fornece a primitiva para s+d_H; sua componente de ghost zero/forma quatro é o contratermo, e a componente ghost um/forma três fornece a divergência. Isso constrói uma densidade candidata, ainda sujeita ao contrato de normalização causal do §7.

## 4. O que073 e074 realmente forneciam sobre H(s)

A @ORDINARY registra H¹,H²,H⁵ do BRST completo na classe local COORDENADA, suave nos valores dos campos completos e de ordem finita/polinomial nos jatos diferenciados, consumindo071. A extensão por espectadores mantém d_HB0. O teorema tem duas versões universais: jatos externos livres, ou quociente pelo ideal diferencial COMPLETO das EOM de B0, com as hipóteses horizontais correspondentes. A @REFERENCE_DOMAINS separa ambas da mera igualdade numa solução FRW particular.

Isso é um antecedente útil, não uma prova automaticamente disponível em qualquer completação. A @S_TRANSPORT afirma: se uma primitiva ordinária já pertence à mesma álgebra formal, normalizar jatos de B0 e projetar tipos Lorentz transporta essa primitiva para H(s) natural. A hipótese de pertença da primitiva é explícita. Uma série formal arbitrária com ordens de jatos crescendo em cada valência não é automaticamente o Taylor de uma expressão suave de ordem finita; não se aplica Borel ou uma ressoma sem novo teorema.

A @SMOOTH também impede trocar C∞ em vielbein por funções racionais sem demonstrar a comparação. Do mesmo modo, a retração natural que comuta com s não comuta com d_H. O @EULER fornece o defeito concreto no grau total quatro. Esse controle não é uma anomalia de ghost um; ele invalida apenas uma importação automática de exatidão relativa.

Portanto os enunciados ordinários071/073 não devem voltar à lista como inexistentes, mas seu consumo como as nulidades naturais/completadas do §2 continua condicionado ao transporte de CLASSE. O que falta não é simplesmente citar de novo H⁵(s)=0 da073.

## 5. Descida075: antecedente já satisfeito no seu domínio

O critério074 exigia que a quebra natural consistente tivesse descida natural. A @FIRST_DESCENT e a @DESCENT_APPLICATION satisfazem essa obrigação sob as hipóteses indicadas: a primeira quebra não removida é consistente como funcional local off-shell nos campos, ghosts e antifields DINÂMICOS; B0 permanece na categoria em que a Ward foi construída.

A primeira variação covariante naturaliza o primeiro descendente, porque o termo s a₄¹ tem operadores de Euler em Z nulos. A homotopia por símbolos resolve os graus de forma abaixo de quatro quando os jatos de todos os geradores de ghost não zero são livres. No final obtém-se Ω=a₄¹+a₃²+a₂³+a₁⁴+a₀⁵ com (s+d_H)Ω=0. Isso é uma descida, não uma primitiva de Ω.

A @DESCENT_COEFS demonstra que um ideal diferencial APENAS de coeficientes de ghost zero, por exemplo relações de B0, não destrói essa prova. Ela não passa a um quociente por EOM dos ghosts/antifields. Na classe perturbativa, os fibrados e suas conexões são os de B0, e a @DESCENT conserva valência, grau Euler positivo, laço e peso t^(E+2L−2), coeficiente a coeficiente.

A @CENTRAL distingue três rotas: incluir os jatos livres da fonte central ω em Z; restringir θ=ω=0 com todos os jatos; ou usar a projeção relativa correta Ω=sΦ após desfazer o gauge. Não se coloca Ω=0 na terceira rota e não se introduzem conjugados de fundo fora do domínio de inserções. Centralidade quântica não significa constância horizontal. Uma constante ímpar sem jatos livres seria outra álgebra.

Logo, no domínio de aplicação075, a descida deixou de ser uma obrigação genericamente aberta. O que permanece é resolver a classe TOTAL e conferir a admissibilidade do contratermo resultante. Tampouco a descida promove a família de referência on-shell a todos os jatos livres de B0.

## 6. O que085/086 acrescentam — e a segunda sequência espectral

A @PAGE085 descreve todas as valências FINITAS do BRST linear no teste métrico de espaço-forma orientada com K>0 fixado, κ≠0, sigma constante projetado e anel escalar herdado inerte Rher:

    H^g(s₀)|_E = Rher ⊗ [Sym^(E−g) M ⊗ Λ^g G]^h,
    0≤g≤min(E,10).

M é o módulo efetivo Weyl/EOM e G os dez jatos de Killing. Esta é a primeira página de OUTRA filtração, a de VALÊNCIA. Pela @CE085, d_V,1 induzido por s₁ é o CE em N_m=Rher⊗Sym^mM, com m=E−g fixo. A @INVARIANTS dá (N_m)^gKilling=0 para m>0; o expoente aqui significa invariância sob a álgebra de Killing, não número de ghost. m=0 conserva constantes.

Para evitar quatro usos do mesmo símbolo, a tabela fixa as duas estruturas:

| Estrutura | Página inicial após cohomologia | Próximo diferencial | Graus mantidos/finitude |
|---|---|---|---|
| Filtração por formas074 de Q_N | H do s COMPLETO em cada forma q | Ebar_N | q∈{0,…,4}; grau total ghost+q |
| Filtração por valência085 de s=Σs_j | H(s₀) em cada E | d_V,1=CE nos N_m | d_V,1 aumenta E e ghost em1; m=E−ghost |
| Próximo r por formas | subquocientes de H(s) | grau (ghost,forma)=(1−r,r) | curvatura C_N entra |
| Próximo r por valência | subquocientes da página CE | (E,ghost)↦(E+r,ghost+1) | m aumenta r−1 |

Os resultados selados086 são:

- @COROLLARY086: H³_CE(gKilling,N₂)^h=0. Isto anula a peça de SEGUNDA PÁGINA POR VALÊNCIA em (E=5,ghost=3). Não anula H³(s) inteiro nem H²(Ebar_N;H³(s)).
- @PONTRYAGIN086: λ↦λ[J_Wν] injeta Rher em H⁴_CE(gKilling,N₂)^h. A peça tem (E=6,ghost=4,m=2). Sua não nulidade nessa página não é sobrevivência em H⁴(s), e não é uma anomalia física de ghost um.
- @CUBIC086: im[H³(C_N)→H³(C₃)]=0 para N≥6. Todas as escolhas de correções permitidas no teste foram abrangidas. Classes de H³(C_N) que começam mais tarde não são anuladas.
- @FORMAL086: a imagem correspondente da completação no alvo C₃ também é zero por fatorização via C₆, sem permutar H e lim. Não se demonstrou ML em todos os alvos nem se calculou H³ da completação.

A tipagem do próximo diferencial por VALÊNCIA pode ser registrada sem calculá-lo: uma seta de ghost três/E3/m0 para ghost quatro/E6/m2 tem comprimento r=3. A existência do ciclo T≤5 e sua obstrução em C₆ tornam esse o índice relevante para a linha cúbica, depois de controlar os quocientes intermediários. A conta explícita dessa seta e os novos resultados N₁/N₂ são tarefas087 separadas; esta nota não os antecipa nem os certifica.

Em particular, mesmo uma futura classe não nula de H⁴(s) não contradiz o critério074, pois ele só exige H¹(Ebar_N;H⁴(s))=0. Seria preciso calcular a ação de Ebar_N e o quociente horizontal sobre essa classe, no domínio pertinente.

## 7. Q2, regularidade e contratermos: condições que não desaparecem com a cohomologia

A @Q2_DOMAIN fixa M=(0,π)×S³, ḡ=dr²−4cos²(r/2)γ e φ̄=id, com suportes compactos interiores e expansão geométrica φ=Exp_φ̄(tξ). Isso é diferente do teste com sigma constante de085/086. Os campos dinâmicos são h, ξ no fibrado tangente pullback, ghosts difeomórficos, setor não mínimo e antifields externos sem propagador. Não se substitui o mapa físico por uma constante para concluir sobre a anomalia desse domínio.

A @Q2_ANOMALY constrói uma quebra local consistente na álgebra auxiliar. A @Q2_REMOVE exige, na primeira ordem não removida, a_N=sB_N+dD_N com B_N real, covariante e ADMISSÍVEL. Não é necessário demonstrar que todas as cohomologias sejam nulas para remover um coeficiente específico; é necessário que a classe desse coeficiente seja removível na normalização autorizada.

O @ADMISSIBLE fornece a lista que ainda deve acompanhar B_N e sua polarização multilinear:

1. Localidade e suporte na diagonal, tipos/ghost/paridade e naturalidade conjunta na categoria de fundos e de alvo.
2. Regularidade declarada, incluindo T4/T5 quando invocados, e ordem de jatos finita em cada coeficiente.
3. Cotas de escala por laço, aridade e inserção, contando acoplamentos, curvaturas, campos, ghosts, antifields e fontes; preservar apenas um peso total não substitui a cota transversal de extensão.
4. Realidade graduada, simetria, independência funcional dos campos e identidade da ação por partes.
5. Compatibilidade dos mapas D_n entre inserções/submonômios, normalização de campos lineares e contatos de EOM; termos de derivadas dos cutoffs permanecem fora da região constante.

A @REGULARITY não declara analiticidade conjunta arbitrária em todo mapa de fundo. Uma homotopia C∞ não fornece automaticamente a versão analítica forte; escolher uma classe suave alternativa exige seu próprio teorema de normalização. A exponencial analítica da esfera não torna analítico um coeficiente C∞ inicial. A @CONTACTS conserva os contatos P_gr G_gr^F=Id e os termos df de uma igualdade modulo d testada por f.

O contratermo não precisa nem deve ser imposto, sem motivo, como uma densidade antifield-free natural SÓ dos campos completos: tal funcional já é s-fechado modulo d e não remove genericamente uma quebra não nula. O espaço BV e a possível dependência relativa em B0 precisam ser tipados antes da busca. Tampouco a média O(4) transforma uma primitiva fora dessa classe em admissível.

[KNOWN — conferência primária limitada] O Teorema2 de Hollands, §3.6 e equações255–259/263, relaciona prescrições T1–T11 a uma HIERARQUIA de contratermos D_n com restrições, e dá a recíproca para essa hierarquia. Isso não é autorização para qualquer densidade s-exata isolada. A extensão tensorial/Grassmann é tratada em §3.5; a remoção Yang–Mills não foi importada para o sigma gravitacional. [Hollands, 0705.3340v4](https://arxiv.org/pdf/0705.3340v4).

[KNOWN — conferência primária limitada] Fröb, Teorema3, parte de uma derivação verdadeira local/covariante da álgebra livre; a equação154 e o Teorema7 dão a Ward e sua consistência, conservando inserções e a interpretação local da ação. A nulidade da quebra é hipótese adicional nos resultados posteriores que constroem o diferencial quântico físico. [Fröb, 1803.10235v3](https://arxiv.org/pdf/1803.10235v3).

A @SPLIT registra ainda a obrigação adicional de acordo perturbativo/contatos quando se pretende COMPARAR fundos. Ela não é T11, nem consequência automática de cohomologia numa referência fixa. Esta auditoria não reabre a existência Q2 já construída: delimita o passo de sua normalização sem anomalia.

## 8. Completação e preservação: precisamente o que os operadores pagam

A @REES_DEF usa

    R_L^q = ∏_(E≥0) t^(E+2L−2) P_E^q,

com E finito e finitos jatos em cada coeficiente, embora a ordem possa crescer com E. t é formal e não é o tempo r. Na @REES_B, b_N=t⁻¹B_N retira uma perna ghost e acrescenta uma forma, conservando R_L. Cada coeficiente de e^(±b_N) recebe no máximo E,…,E+4; para L≥1 não aparecem potências negativas. A derivada horizontal e o antibracket com a ação clássica pertinente conservam a organização.

O @REES_LIMIT é explícito: nada disso prova continuidade de uma futura homotopia de s ou de Ebar_N. A descida075 acrescenta o controle de seus próprios operadores horizontais, mas não de todos os operadores necessários ao §3. Uma solução meramente elemento a elemento numa álgebra suave de ordem finita não fornece uma solução de uma série completada sem compatibilidade coeficiente a coeficiente.

Nas fontes estendidas072, tadpoles t⁻¹θ têm graduação externa própria e dão séries Laurent com parte negativa limitada no grau externo fixado. Não se recategorizam como R_L por nome. O setor sem fontes, a extensão inteira e a projeção relativa são rotas distintas e suas operações devem conservar os graus realmente usados.

Os cortes C_N de085/086 truncam VALÊNCIA, não ordem de jatos. A prova da imagem cúbica zero não precisa ML; obter toda H(s) completada por uma sucessão de escolhas de primitivas pode exigir construir uma compatibilidade que essa única projeção não fornece.

## 9. Próximos requisitos concretos e verificáveis

Para aplicar a074 à quebra física, sem ampliar o objetivo:

- Fixar a álgebra de inserções/referências efetivamente usada: teoria original sem fontes ou projeção/estensão072, regularidade, pesos e graus externos. Transportar o cociclo consistente para essa mesma classe; não usar uma avaliação pontual como identidade universal.
- Utilizar a descida075 já disponível no domínio off-shell relativo apropriado e obter Ω, conservando cutoffs e as conexões de B0.
- Pela rota suficiente074, demonstrar as três nulidades H_s^(5,0), H_s^(2,3), H_s^(1,4), e os dois quocientes horizontais da tabela; pela rota mais localizada, resolver as classes U_q concretas da recorrência. Uma linha sobrevivente em H³(s)/H⁴(s) exige calcular Ebar_N, não declarar fracasso.
- Se a filtração por valência for usada para fornecer H(s), controlar os diferenciais posteriores e a compatibilidade das primitivas na completação, e demonstrar a comparação com o fundo físico e os coeficientes efetivos. Os cálculos085/086 são entradas precisas para o teste fixado, não esse mapa de comparação.
- Construir os B_N como parte de uma normalização multilinear que satisfaça as condições do §7 e conserve as ordens já corrigidas. A existência da classe cohomológica potencial não calcula seu coeficiente de anomalia; sua exatidão tampouco implementa sozinha a hierarquia.

Esses requisitos são alternativas organizadas para a remoção local formal; não são uma lista de hipóteses necessárias para toda possível teoria quântica. Nenhum resultado N₁/N₂ ou novo representante H⁴(s) ainda em investigação087 foi consumido aqui.

## 10. Estatuto e custódia

[DERIVED] A auditoria identifica a fonte, todos os graus e a fronteira lógica do critério074, conserva a contribuição positiva da descida075 e posiciona exatamente085/086 em sua própria filtração. Não recomputa a cohomologia dos módulos N₁/N₂.

[OPEN] A remoção admissível da quebra/QME no domínio físico, a comparação entre fundos quando exigida, o estado/quociente físico interagente, as demais questões globais e UV permanecem distintos. Nada foi deduzido sobre falsificação, confirmação ou reconstrução gravitacional geral. Fase/ramo do registro e o H3 interno do programa não são alterados.

[REAL — documental] As linhas dos vínculos foram extraídas dos bytes lidos nesta emissão. O manifesto mede as fontes antes/depois e o novo helper. As importações primárias foram consultadas pela web; não há hash local inventado de PDF. A descoberta inicial por nomes teve acesso negado a uma dependência de pacotes sem relação com o alvo; a consulta foi então restrita aos diretórios pertinentes074–086, com leitura completa das fontes necessárias. Não se alegou varredura exaustiva do computador ou auditoria recursiva dos antecedentes.

Somente arquivos novos desta pasta foram escritos por temporário exclusivo, fsync, verificação e rename sem sobrescrita. Nenhum arquivo canônico, memória, Atlas, índice, selo ou fonte congelada foi escrito, nem um.py executado/importado.
"""
for token, value in sorted(LINKS.items(), key=lambda item: -len(item[0])):
    if token not in note:
        raise RuntimeError("Unused reference token: " + token)
    note = note.replace(token, value)
unresolved = re.findall(r"@[A-Z_]+", note)
if unresolved:
    raise RuntimeError("Unresolved reference " + str(unresolved))

checks = []
def check(name, condition, detail=None):
    checks.append({"name": name, "passed": bool(condition), "detail": detail})
for name, anchor in anchors.items():
    actual_line = content[anchor["source"]].splitlines()[anchor["line"] - 1]
    check("anchor_exact:" + name, actual_line == anchor["fragment"], anchor)

links = list(dict.fromkeys(re.findall(r"\]\(<(C:/[^>]+)>\)", note)))
for link in links:
    path = re.sub(r":\d+$", "", link)
    check("local_link_exists:" + Path(path).name, Path(path).is_file(), link)

if not all(item["passed"] for item in checks):
    publish_json(OUT / "FALHA_DOCUMENTAL_PRE_EMISSAO_087.json", {"checks": checks, "sources_before": before})
    raise RuntimeError("Pre-emission documentary failure")

note_pin = publish(OUT / "CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md", note.encode("utf-8"))
after = {}
for key, relative in FILES.items():
    after[key], _ = pin(WORK / relative)
after["helper"], _ = pin(__file__)
for key in before:
    check("input_preserved:" + key,
          before[key]["bytes"] == after[key]["bytes"] and
          before[key]["sha256"] == after[key]["sha256"] and
          before[key]["mtime_ns"] == after[key]["mtime_ns"])
check("note_roundtrip", (OUT / Path(note_pin["path"]).name).read_bytes() == note.encode("utf-8"))
passed = all(item["passed"] for item in checks)
record = {
    "status": "WRITTEN_CONTRACT_AUDIT_DOCUMENTARY_PASS_PENDING_REVIEW" if passed else "FAIL_DOCUMENTARY",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author": "/root/prepare_integration_83",
    "scope": "Exact sufficient criterion074, two distinct spectral-sequence gradings, completed descent075, mapped results085/086, and causal admissibility; no new N1/N2 computation or claim of QME.",
    "note": note_pin,
    "sources_before": before, "sources_after": after, "anchors": anchors,
    "checks": checks,
    "documentary_checks_total": len(checks),
    "documentary_checks_passed": sum(item["passed"] for item in checks),
    "failed_checks": [item for item in checks if not item["passed"]],
    "sources_preserved": len(before) if passed else None,
    "primary_sources_consulted": [
        {"url": "https://arxiv.org/pdf/0705.3340v4", "scope": "Section3.5, theorem2/section3.6 equations255-259 and263; T4/T5; source viewed via web, not downloaded."},
        {"url": "https://arxiv.org/pdf/1803.10235v3", "scope": "Theorem3 and equation154/theorem7: derivation hypothesis, anomaly and consistency; viewed via web."},
    ],
    "discovery_limit": "Initial rg file listing was partial due denied package dependencies unrelated to task; exact relevant directories then read successfully.",
    "new_mathematical_executions": 0, "new_cas_executions": 0, "new_lean_compilations": 0,
    "um_executed_or_imported": False, "existing_files_modified": False, "originals_written": False,
    "canonical_reopened": False,
    "new_N1_N2_results_consumed": False,
    "external_approval_claimed": False,
}
record_pin = publish_json(OUT / "MANIFESTO_CONTRATO_CRITERIO_087.json", record)
print(json.dumps({"status": record["status"], "note": note_pin, "manifest": record_pin,
                  "checks": [record["documentary_checks_passed"], record["documentary_checks_total"]],
                  "preserved": record["sources_preserved"], "failed": record["failed_checks"]},
                 ensure_ascii=False, indent=2))
if not passed:
    raise RuntimeError("Preservation failure recorded")

