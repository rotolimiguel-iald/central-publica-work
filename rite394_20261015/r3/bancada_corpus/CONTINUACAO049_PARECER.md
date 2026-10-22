# Continuação049 — operador positivo auto-adjunto e subespaço padrão contínuo

[REAL — compilado e auditado na bancada] Emissão UTC: 2026-09-07T02:37:54.023525+00:00

Este lote constrói um modelo explícito em H=L²(ℝ,dξ;ℂ), com operador de Tomita de um subespaço real padrão. É um novo modelo nesta bancada, definido por multiplicadores; não foi demonstrado que ele seja a representação física selecionada pela torre anterior ou por ω(I)=1.

## Resultado e domínio efetivo

Para cada c real, T_c é o operador parcial cujo domínio e valor foram provados exatamente:

    D(T_c) = {f ∈ L² : ξ ↦ exp(-cξ) f(ξ) pertence a L²},
    (T_c f)(ξ) = exp(-cξ) f(ξ), quase em toda parte.

[REAL] T_c é positivo, auto-adjunto no sentido do adjunto de LinearPMap e fechado. A prova inclui densidade do domínio e igualdade maximal T_c*=T_c; não se limita à simetria do pareamento.

[REAL] Jf(ξ)=conj(f(-ξ)) é antiunitária involutiva. S_c=JT_c tem o mesmo domínio, é antilinear fechado, preserva esse domínio e satisfaz S_c²f=f nele. A fórmula concreta foi verificada quase em toda parte:

    (S_c f)(ξ) = exp(cξ) conj(f(-ξ)),
    J S_c f = T_c f.

[REAL] K_c=Fix(S_c) é um subespaço real fechado e padrão. A soma algébrica é exatamente D(T_c)=K_c+iK_c; seu fecho é H. O código não substitui essa soma algébrica por H. Na decomposição f=h+ik, S_c f=h-ik.

[REAL] Para c≠0, T_c f=z f implica f=0 para todo candidato z complexo. A prova usa que as fibras de exp(-cξ) têm medida zero. Ela não anuncia a classificação absolutamente contínua do espectro. O controle c=0 dá domínio inteiro, T_0=I e S_0=J.

## Como as hipóteses foram pagas

Os pesos positivos limitados a,b satisfazem a²+b²=1 e b=exp(-cξ)a. O fonte usa a expressão equivalente simétrica a=exp(cξ/2)/sqrt(exp(cξ)+exp(-cξ)), b=exp(-cξ/2)/sqrt(exp(cξ)+exp(-cξ)). As propriedades dos multiplicadores A=M_a e B=M_b são provadas, incluindo A injetivo, A/B auto-adjuntos, AB=BA e A²+B²=I.

O grafo de T é {(Ah,Bh)}. Sua caracterização Bx=Ay paga fechamento e maximalidade do adjunto: a recíproca recupera o parâmetro por h=Ax+By. A positividade vem do pareamento dos multiplicadores. Para S, o grafo é uma pré-imagem contínua do grafo de T; não se supõe uma isometria falsa para o produto usual de norma máximo.

[KNOWN] A passagem de involução antilinear fechada para seu subespaço real padrão é um resultado conhecido; este lote fornece sua formalização e uma instância explícita. Referência: [Brunetti–Guido–Longo, proposição 2.3, p.5](https://arxiv.org/pdf/math-ph/0203021). O artigo emprega dados de representação de Poincaré e relações modulares em sua construção geométrica; tais dados não são automaticamente importados para049.

## Verificação formal

| Módulo novo | Teoremas | Definições | Prints | Alcance |
|---|---:|---:|---:|---|
| [BoundedGraphOperator.lean](<C:/IALD/Central de Patentes/Chatgpt/BoundedGraphOperator.lean>) | 14 | 3 | 17 | Parametrização limitada do grafo, domínio denso, fechamento, adjunto maximal e positividade. |
| [ClosedAntilinearStandardSubspace.lean](<C:/IALD/Central de Patentes/Chatgpt/ClosedAntilinearStandardSubspace.lean>) | 8 | 4 | 12 | FixS fechado real, separação, domínio como K+iK e subespaço padrão. |
| [ContinuousModularMultipliers.lean](<C:/IALD/Central de Patentes/Chatgpt/ContinuousModularMultipliers.lean>) | 34 | 11 | 45 | Pesos explícitos, multiplicadores A/B, reflexão-conjugação J e identidades. |
| [BoundedGraphStandardSubspace.lean](<C:/IALD/Central de Patentes/Chatgpt/BoundedGraphStandardSubspace.lean>) | 6 | 2 | 8 | S=JT, invariância do domínio, involução e construção do subespaço padrão. |
| [ContinuousModularDomain.lean](<C:/IALD/Central de Patentes/Chatgpt/ContinuousModularDomain.lean>) | 13 | 1 | 14 | Grafo ae, domínio MemLp, ausência de autovetores e controle c=0. |
| [ContinuousModularStandardSubspace.lean](<C:/IALD/Central de Patentes/Chatgpt/ContinuousModularStandardSubspace.lean>) | 10 | 2 | 12 | Instância concreta, JS=T, decomposição de Tomita e fórmula ae. |

Totais lidos do marcador: 85 teoremas, 23 definições, 0 instâncias próprias, 108 prints. Compilação serial de 7 etapas, incluindo Imports049All. Zero erros/avisos. Cobertura exata de axiomas; apenas propext, Classical.choice e Quot.sound.

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO049_CLEAN_20260907_022910_709711

Build SHA256: c04c4413652ca5869ca35ca8d4b684616e725e43ae86fa438564ee31f946dc20

83 entradas congeladas coincidem antes/depois; 31 artefatos da compilação final. O auditor conferiu 108 registros de evidência do build. Fontes/copias exatas, ambiente explícito e hash dos artefatos próprios preservados. A metadata por etapa vincula o snapshot global e registra a comparação feita pelo runner.

A fronteira externa mede os imports diretos Mathlib/stdlib e seus companheiros, executável e configurações. Não recompila Mathlib nem mede toda sua dependência transitiva. Nenhum olean histórico Chatgpt ou do kernel canônico entra na cadeia local destes seis módulos.

## O que continua aberto

[OPEN] Identificar formalmente T_c com Δ_c^(1/2), construindo e relacionando os operadores e seus domínios; provar o cálculo funcional que identifica as fases com Δ_c^(it); estabelecer a ação geométrica, a inclusão semilateral e Bisognano–Wichmann; construir a rede de álgebras/estado e sua relação com a torre.

[OPEN] Seleção física de c, região–álgebra, dimensão e assinatura físicas, protocolo/escala de área, H3 e reconstrução gravitacional geral. Ausência de autovetores elimina uma característica do modelo anterior, mas não demonstra por si a realização de Borchers ou a gravidade.

Os módulos anteriores e originais permanecem fora da escrita deste lote. canonical_gate_changed=false é uma declaração de escopo: este lote não escreve no gate canônico. Não é uma auditoria de alterações de terceiros no canônico. O resultado é matemático no modelo explicitado; não é confirmação física.

Revisão independente: [CONTINUACAO049_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO049_REVISAO_INDEPENDENTE.md>).
