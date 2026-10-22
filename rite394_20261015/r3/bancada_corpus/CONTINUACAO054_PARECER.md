# Continuação054 — custo modular pelo polarizador global

[REAL — alcance das declarações compiladas e auditadas] Emissão UTC: 2026-09-07T07:04:26.733096+00:00

A054 constrói um custo não negativo estendido a partir do mesmo polarizador real global D da053. Prova o domínio de custo finito, sua densidade no setor real pertinente, a semicontinuidade inferior e a covariância por todos os TowerHorizon do mesmo perfil. Nos vetores locais autoadjuntos, o custo coincide com o coeficiente quadrático da variação da energia modular de uma curva unitária efetiva. H3, área física e reconstrução gravitacional geral permanecem [OPEN].

## Objeto, domínio e alcance real

Para um Hilbert real H e D:H→L[ℝ]H, definir:

    C_D(x) = Σ_(n≥0) ofReal( 2/(2n+1) · ‖D^(n+1)x‖² ) ∈ ℝ≥0∞,
    Dom(C_D) = {x : C_D(x)<∞}.

Uma série divergente conserva o valor infinito; não é convertida em zero por uma soma real totalizada. Não se supõe ‖D‖<1 globalmente. Mesmo a cota ‖D‖≤1 não garante custo finito para todo vetor.

Os teoremas provam C_D(a x)=ofReal(a²)C_D(x), a estimativa de adição que torna Dom(C_D) um submódulo REAL e C_D(x)=0↔Dx=0. Também provam semicontinuidade inferior de C_D com valores estendidos. Uma isometria linear real bijetiva que entrelaça D preserva o custo, inclusive quando infinito, e o domínio finito.

Na torre, D é literalmente statePolarizer P=P_R(−i)P_R, com R=realStateSubspace P construído na053. A implementação GNS W_h de cada h:TowerHorizon P entrelaça D. Logo:

    C_D(W_h x)=C_D(x), para todo x;
    W_h x∈Dom(C_D) ↔ x∈Dom(C_D).

Para A autoadjunto e pertencente ao fator M, o custo de AΩ é zero exatamente quando A pertence ao centralizador de ω, equivalentemente quando todas as respostas reais infinitesimais do estado em testes autoadjuntos são zero. A classificação não é afirmada para operadores arbitrários fora desse setor.

Os vetores locais autoadjuntos têm custo finito, e as esperanças de prefixo aproximam AΩ. O resultado formal de densidade é:

    closure(Dom(C_D) ∩ R)=R.

É densidade na topologia Hilbert. O lote não demonstra que os vetores locais formam um núcleo da forma, nem anuncia uma forma quadrática fechada, uma polarização bilinear global ou um operador não limitado associado. A semicontinuidade inferior e o domínio não são usados para encobrir essas distinções.

## A série e o cálculo dos cortes

Para |d|<1, incluindo d=0 e d<0, a série REAL é somável e satisfaz:

    Σ_(n≥0) 2 d^(2n+2)/(2n+1) = d[log(1+d)−log(1−d)].

A prova usa a série ímpar do logaritmo já demonstrada na Mathlib. Somente após provar somabilidade e não negatividade dos termos a soma é transportada para ENNReal.

Para wi,wj>0, tomar d=(wi−wj)/(wi+wj). Então |d|<1 e o valor é d(log wi−log wj). A identidade não divide por d; pesos iguais não são excluídos.

No prefixo N, os pesos wi=towerW P N i e a matriz local a=a* pertencem à mesma torre. A053 já liga D à matriz de entradas i·dij·aij. A054 itera essa identidade e calcula a norma GNS:

    ‖D^n(towerPi(a)Ω)‖² = Σ_j Σ_i wj · dij^(2n) · |aij|².

Distribuir a série pelas somas finitas e usar a autoadjunção dá:

    C_D(towerPi(a)Ω)
      = ofReal( 1/2 · Σ_i Σ_j (wi−wj)(log wi−log wj)|aij|² ).

O fator 1/2 pertence à soma sobre pares ORDENADOS. Cada par não ordenado contribui uma vez. Nenhuma densidade trace-class global é introduzida para essa igualdade.

## Derivada efetiva e fator dois

Fixar K_N=towerPi(diag(−log wi)), A=towerPi(a), U(t)=exp(i t A) e:

    f(t)=Re ω(U(t)* K_N U(t)).

A exponencial e a regra do produto fornecem as derivadas; o custo não é definido como uma derivada escolhida. A primeira derivada no zero é zero porque a densidade diagonal do corte comuta com K_N. A segunda derivada usa:

    −A²K_N + 2 A K_N A − K_N A².

A soma matricial é precisamente:

    f''(0)=2·localModularCost(P,N,a),
    lim_(t→0, t≠0) [f(t)−f(0)]/t²=localModularCost(P,N,a).

O limite bilateral é provado por L'Hôpital com as derivadas efetivas e a primeira derivada nula. Em consequência, C_D(AΩ)=ofReal(f''(0)/2). Isso liga o custo global avaliado no vetor local à leitura de energia modular do MESMO corte. Não é apenas a coincidência de dois números definidos separadamente.

K_N é um observável limitado do corte finito. O resultado não identifica um logΔ global com domínio, não define uma entropia relativa global de Araki e não toma a entropia diagonal por entropia total. A leitura formalizada aqui é a variação de energia; outras interpretações requerem suas próprias definições e pontes.

## Dois vetores fixos da053

Na referência estacionária thirdThermalReference, com p=1/3, os controles preservam os mesmos vetores:

| Vetor | Norma GNS ao quadrado | Custo |
|---|---:|---:|
| X₁Ω, Pauli no primeiro sítio | 1 | log2/3 |
| X₂Ω, flip00↔11 no prefixo de dois sítios | 5/9 | 2log2/3 |

O segundo vetor permanece bruto, sem normalização para norma um. O custo distingue as duas frequências. O perfil de referência é estacionário e periódico; o uso de construções gerais da torre não o transforma em perfil aperiódico.

A053 provou insuficiência de covariância mais uma calibração comum para selecionar uma forma. A054 fornece uma expressão que reproduz a resposta energética local. Esse requisito é um critério matemático adicional. O lote não prova unicidade entre todas as formas que coincidam num conjunto apenas Hilbert-denso; tal inferência exigiria hipóteses adicionais de núcleo e continuidade pertinentes.

## O que permanece aberto

[OPEN] Interpretar esse custo como calor físico ou área de horizonte, selecionar regiões e observadores físicos, fixar escala dimensional e relacionar estado, tela, matéria, relógio e curvatura sem ajustes destinados a impor o balanço. Os contratos microscópicos hheat/harea e a reconstrução gravitacional geral não são consequências desta série.

C_D não é inducedArea nem constructedHeat por definição. A054 não escolhe mass, η ou curvatura para forçar uma igualdade. Também não transforma a ação de todo TowerHorizon de um perfil em uma localização física já selecionada.

## Verificação, falhas anteriores e custódia

| Módulo054 | Teoremas | Definições | Instâncias | Prints | Alcance |
|---|---:|---:|---:|---:|---|
| [PolarizerModularCost.lean](<C:/IALD/Central de Patentes/Chatgpt/PolarizerModularCost.lean>) | 19 | 4 | 0 | 23 | Custo estendido, domínio real finito, escala, radical, covariância e semicontinuidade inferior. |
| [PolarizerCostSeries.lean](<C:/IALD/Central de Patentes/Chatgpt/PolarizerCostSeries.lean>) | 12 | 0 | 0 | 12 | Série convergente do logaritmo, ambos os sinais, pesos positivos e passagem para ENNReal. |
| [TowerModularCost.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerModularCost.lean>) | 24 | 5 | 0 | 29 | Mesmo D global053, domínio denso no setor real, custo local e dois controles sem normalizar o segundo vetor. |
| [ModularCostDerivative.lean](<C:/IALD/Central de Patentes/Chatgpt/ModularCostDerivative.lean>) | 17 | 8 | 0 | 25 | Derivadas da curva unitária efetiva e limite quadrático ligados ao mesmo custo local. |

Total054: 72 teoremas, 17 definições, 0 instâncias nomeadas, 89 prints. Lote final: 5/5 etapas, incluindo Imports054All. O auditor verificou cobertura exata, zero avisos/erros, ausência de sorryAx e somente propext, Classical.choice e Quot.sound nos prints.

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_CLEAN_20260907_065259_972152

Build SHA256: c2e2e6069652164b07c079cb58afa9cd2a372cea8d5057bb0589da5eb03a5835

O auditor mediu separadamente 2295 arquivos do build e 393 registros históricos. Esses números não são somados como conjuntos disjuntos. Os quatro fontes054 foram copiados por bytes e compilados em diretório exclusivo. Dependências históricas pinadas, incluindo053, foram verificadas e copiadas; não foram recompiladas neste lote. Os imports externos diretos e seus companheiros são medidos, sem alegar reconstrução exaustiva de todo o fecho externo.

As tentativas intermediárias não foram todas aprovadas: houve falhas de elaboração e ajustes antes do lote final. Seus marcadores, logs e backups permanecem como história, sem valor de prova, e integram a coleta histórica da custódia quando presentes. Somente o build final ligado ao hash acima sustenta esta emissão.

A revisão final deve identificar literalmente esse build e seu diretório; o gerador recusa sua ausência ou divergência. A autoria e a revisão cruzada são documentadas na nota, não autenticadas semanticamente pelo parser. Notas de revisão disponíveis: [CONTINUACAO054_REVISAO_GENERICO_SERIE_MC.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_REVISAO_GENERICO_SERIE_MC.md>); [CONTINUACAO054_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_REVISAO_INDEPENDENTE.md>); [CONTINUACAO054_REVISAO_INFRA_NEWTON.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_REVISAO_INFRA_NEWTON.md>); [CONTINUACAO054_REVISAO_TORRE_NEWTON.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_REVISAO_TORRE_NEWTON.md>). A nota de infraestrutura [CONTINUACAO054_REVISAO_INFRA_NEWTON.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_REVISAO_INFRA_NEWTON.md>) registra inspeção do contrato, reexecução histórica e controles da instrumentação; não é um BUILD_PASS final nem aprovação científica dos módulos. Seu alcance datado não é ampliado retroativamente pela presente emissão.

Parecer e entrega são novos, de criação exclusiva, e seus hashes são lidos dos bytes. A selagem ocorre separadamente após os documentos. Esta emissão não altera originais, Atlas, um.py, kernel ou memórias canônicas; canonical_gate_changed=false descreve o escopo das escritas, não uma auditoria de alterações de terceiros. Não se declara QG confirmada, resolvida ou provada.

Revisão final: [CONTINUACAO054_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_REVISAO_INDEPENDENTE.md>). Entrega: [ENTREGA_054_custo_modular_do_polarizador.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_054_custo_modular_do_polarizador.md>).
