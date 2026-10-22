# Consulta — pares gaussianos e reconstrução pelo J original

CONSULTA_PARES_GAUSSIANOS_RECONSTRUCAO

Data: 2026-09-12T23:28:06.205079-03:00. Escopo: leitura e análise conceitual; nenhuma recompilação, implementação, execução de helpers/monólito ou escrita de memória. Pareceres custodiados preservados.

**[DERIVED — rota a formalizar] A etapa proposta é concreta e não circular.** Ela permite passar da álgebra de operadores com pares para uma álgebra densa de vetores direitos, com multiplicações limitadas e involução fechável. Não identifica ainda o fecho dessa involução com F, nem reconstrói R=Jπ(b)J.

## 1. Ponte gaussiana no domínio escalar completo

Fixar H=H_I, M=π(N), N_aux=ρ(N), C=`scalarGaussianGNSMap P`, Ω_g=`scalarGaussianVacuum P`. F é o adjunto máximo do S original. A igualdade da imagem ρ(N) com `dualOrbitVonNeumann N` já está na fonte; não depende de provar agora que M é VNA.

**[REAL — enunciados lidos]** `ScalarGaussianGNSMap.lean:32` dá Cπ(a)=ρ(a)C em todo H; o lema de inscrição na linha 42 ainda recebe a∈I uniforme. `ScalarWeightOrbit.lean` fornece a fórmula a.e. da inscrição para todo a∈nν, com o mesmo fator positivo √dualHaarFactor. `ScalarWeightAction.lean:54` dá a densidade da inscrição completa Λν.

**[OPEN — próximo lema]** Estender exatamente para todo a∈nν:

`C Λν(a) = ρ(a) Ω_g`.

O argumento a.e. usa as fórmulas dos dois lados e uma interseção finita de eventos para cada a fixo. Não divide por g, não supõe inversa limitada de C e não uniformiza eventos a.e. para todos os a. Alternativamente, pode usar a e_h∈I, convergência das inscrições e continuidade dos operadores; nenhuma igualdade I=nν é necessária.

Para cada B∈N_aux', definir:

`R_B=C* B C`,  `η_B=C*(BΩ_g)`,  `ζ_B=C*(B*Ω_g)`.

Tomar adjuntos do entrelaçamento em a* dá C*ρ(a)=π(a)C*. Logo, para todo a∈nν,

`R_B Λν(a)=C*Bρ(a)Ω_g=π(a)η_B`,

`R_B* Λν(a)=C*B*ρ(a)Ω_g=π(a)ζ_B`.

Isso instancia `ScalarRightAdjointPair` e, por `ScalarRightAdjointPair.lean:128`, dá η_B∈D(F) e Fη_B=ζ_B, no F original. Também ||R_B||≤||B|| pela contratibilidade de C. B não precisa preservar closure(Ran C): C* já tem contradomínio H. Não substituir C pela unitária polar V; a inscrição acima é de C, não de V.

## 2. Unicidades e álgebra vetorial

As duas unicidades propostas são adequadas e usam evidência existente:

- Para o mesmo R, comparar a=e_h, h>0: π(e_h)(η−η')=0. `ScalarRightAdjointPair.lean:34` permite passar a h→0 e obter η=η'; repetir para R* e os vetores adjuntos.
- Para o mesmo η, RΛν(a)=R'Λν(a) em todos os a∈nν. Densidade de Λν e continuidade dão R=R'. Não se afirma continuidade da aplicação η↦R na norma de H.

Definir E como o conjunto de vetores que admitem um par, e R_η como seu operador único. As operações já construídas em `ScalarPairedRightAlgebra.lean` transportam-se a E. Com a convenção explícita

`η ∘ ζ := R_η ζ`,  `η^♯ := Fη`,

obtém-se `R_(η∘ζ)=R_η R_ζ` e `R_(η^♯)=R_η*`. O vetor adjunto do produto é R_ζ* Fη; portanto `(η∘ζ)^♯=ζ^♯∘η^♯`. Essa ordem é a da álgebra de vetores direitos com sua representação por multiplicação à esquerda; não trocar silenciosamente pelo produto da álgebra original.

A norma é a herdada de H. Valem `||η∘ζ||≤||R_η||·||ζ||` e `⟨η∘ζ,χ⟩=⟨ζ,η^♯∘χ⟩`. Associatividade, linearidade e involutividade seguem das operações de pares e das unicidades. Não é necessário postular unidade, norma submultiplicativa dos vetores ou involução limitada.

## 3. Densidade: o ganho e sua fronteira

A órbita N_aux'Ω_g é densa porque Ω_g é separante para N_aux. C injetivo implica Ran C* densa. Assim `{C*BΩ_g:B∈N_aux'}` é denso em H, e E também. Esta é a mesma família utilizada em `ScalarTomitaAdjoint.lean:75` para densidade de D(F), agora com um operador direito e seu adjunto associados explicitamente.

Há igualmente uma prova curta de densidade dos produtos. Para h>0, `K_h(I)=R_h*R_h` já tem par por `ScalarCommutantSandwich`; seja u_h seu vetor. Para η∈E, `u_h∘η=K_h(I)η→η`. Com E denso, o espaço gerado pelos produtos é denso em H. Não se exige que R_h, isoladamente, já tenha vetor adjunto.

Finalmente, a involução em E é restrição do F fechado. É, portanto, fechável. Estes passos dão uma rota para formalizar os axiomas usuais de uma álgebra de Hilbert esquerda de vetores direitos, com álgebra de von Neumann gerada igual a M' pelo resultado operatorial existente. O completamento Hilbert dessa álgebra seria H; isso não a torna automaticamente uma álgebra de Hilbert *full*.

**[OPEN] A igualdade de gráficos ainda exige prova própria:**

`closure {(η,Fη):η∈E} = graph F`.

Sabe-se apenas inclusão e densidade da primeira coordenada. Um alvo equivalente, mais localizado, é `closure(E ∩ Fix F)=Fix F`, em norma de H. A equivalência usa a decomposição de y∈D(F) em `(y+Fy)/2 + i·(y−Fy)/(2i)` e a estabilidade de E por F. No sentido inverso, simetrizar aproximações de gráfico produz vetores fixos. A densidade de E em H, sozinha, não prova essa condição. `scalarTomitaStandardSubspace` existente trata Fix S; para empregar Fix F é preciso a especialização correspondente, sem identificar os dois subespaços.

Na fonte primária, a passagem de 5.11 para 5.12 é justamente mais forte que densidade Hilbert e geração do comutante: identifica o subespaço real que permite conservar o mesmo J antes da simetria de 5.13. A construção proposta não autoriza pular essa identificação. [Rieffel–Van Daele, §5](https://msp.org/pjm/1977/69-1/pjm-v69-n1-p17-s.pdf).

## 4. Ordem sugerida e limite da consulta

Próximos enunciados concretos: inscrição gaussiana completa; par C*BC; unicidades de vetor/operador; subespaço vetorial E e operações acima; densidade de E e dos produtos; fechabilidade da involução. Em seguida, tratar explicitamente a identificação do seu gráfico com F, ou uma reconstrução limitada equivalente que preserve o J original.

Provar M VNA é útil para converter uma futura reconstrução no bicomutante em pertença à imagem efetiva π(N). A equivalência gaussiana dá uma restrição fiel e redutora da VNA auxiliar, mas essa transferência de fechamento ainda precisa de lema; isometria de norma, sozinha, não fornece fechamento WOT. Não reabri aqui a busca global da infraestrutura topológica da Mathlib.

Não obtido nesta consulta: pertença de C*BC a JMJ, inversa de comutantes, identificação de J do vetor gaussiano com J do peso, KMS, fluxo modular, traço, alteração de gate ou runtime. Nenhum novo resultado Lean foi certificado.

## Proveniência

Custódia mãe efetivamente lida por bytes: `paired_right_custody.json`, SHA256 `ea48a2d143f117d7385ebda9a36685720056c51ae4b764185d5c719d72a48989`. Sua verificação autoral foi somente lida; não foi reexecutada. Pins e linhas das declarações consultadas: [consultation_pins.json](C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/consulta_pares_gaussianos_20260912_232806_205079/consultation_pins.json). Os resultados antigos são herdados; as novas fórmulas deste documento são análise de prova a formalizar, não novas compilações.
