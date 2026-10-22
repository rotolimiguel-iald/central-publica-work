# Dados canônicos para a perturbação limitada de Araki — 09/09/2026

[REAL — leitura e recibo] O par concreto (M, Ω), com M = theFactorObject P e Ω = hOmega P, fornece os dados cíclico-separantes requeridos pela formulação de Araki informada pela revisão primária da raiz. A ação usada na interação é o grupo modular desse mesmo par, pela cadeia S†S = Δ e sua caracterização espectral total. P : SiteProfile permanece arbitrário: não se impõe perfil tracial, periodicidade, limite uniforme inferior dos pesos ou comutação de V com o estado.

[DERIVED + KNOWN] Aplicar o teorema válido de perturbação limitada a esse par e a V = V* ∈ M fornece existência matemática do vetor perturbado cíclico e separante e, após normalização, do estado fiel normal correspondente. Esta nota não deve converter a falta de um construtor Lean próprio de Araki em falta de existência matemática. O artigo primário e o sinal de sua notação estão sob revisão da raiz, em ESTADO_ARAKI_20260909; esta auditoria confere os referentes locais.

## 1. Objetos e enunciados do mesmo perfil

Todos os caminhos desta seção têm raiz C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/. A evidência JSON traz caminhos absolutos, linhas medidas, bytes, hashes atuais, pins do recibo e linhas de axiomas.

| Dado | Fonte e enunciado | Alcance exato |
|---|---|---|
| Perfil | TowerDefinite.lean:53, SiteProfile | w : ℕ → ℝ; ∀n, 0 < w n < 1. |
| Hilbert | TowerHilbert.lean:37, TowerHilbert | Completion (TowerPre P); Hilbert complexo completo por instâncias da biblioteca. |
| Vetor normalizado | TowerHilbert.lean:42, hOmega; :46 hOmega_inner_self; :53 hOmega_norm | Ω é o vetor identidade e ‖Ω‖ = 1. |
| Álgebra de von Neumann | TheFactorObject.lean:67, theFactorObject | VonNeumannAlgebra (TowerHilbert P), construída como bicomutante da imagem da torre. O teorema de Araki não exige aqui um tipo particular de fator. |
| Ciclicidade | TheFactorObject.lean:95, factor_omega_cyclic | MΩ denso em H, sem hipótese adicional. |
| Separação | RightMult.lean:570, factor_omega_separating | A ∈ M e AΩ = 0 implicam A = 0; a prova usa o comutante e a órbita direita densa. |
| Funcional concreto | TheFactorObject.lean:103, omegaState | ω(A) = ⟨Ω,AΩ⟩; é uma função, ainda não um registro abstrato de estado normal. :109 omegaState_pi identifica o estado em cada andar. |
| Normalidade formal citada pelo contrato | NoNormalTrace.lean:61, SeqWOTContinuous; :72 omegaState_seqWOT | Continuidade para sequências limitadas convergentes em WOT. Não é o enunciado completo de normalidade σ-fraca. |

[DERIVED] Positividade, normalização e fidelidade do funcional seguem dos mesmos objetos: ω(A* A) = ‖AΩ‖²; ω(1) = ‖Ω‖² = 1; o anulamento usa factor_omega_separating. Não há dependência da escolha de uma medida externa ou de outro estado.

[KNOWN — tradução matemática aplicável] Um funcional vetorial sobre uma álgebra de von Neumann concreta é normal. TheImportedExpectation.lean:114–127 distingue corretamente esta normalidade plena da consequência sequencial tipada. Também há lastro formal posterior para redes gerais: ExpectationNormality.lean:99–110 fornece supremum e convergência forte de redes positivas dirigidas limitadas. Avaliar em Ω e aplicar a continuidade do produto interno dá a convergência do estado. Os teoremas :140 e :155 desse arquivo são de normalidade da ESPERANÇA, não devem ser renomeados como teoremas do estado.

## 2. Por que α é o grupo modular de Ω

1. ClosedTomitaOperator.lean:121, closedTomita_graph_eq, identifica o grafo com o fecho do grafo real de AΩ ↦ A*Ω. :135 prova que é fechado; :141, domínio denso; :156–164 coloca AΩ no domínio e identifica a ação. Não é um operador escolhido só pelo nome.
2. ClosedModulatorCandidate.lean:37–42 define A = JS. ModulatorPositive.lean:82 prova positividade; ModulatorSelfAdjoint.lean:122 prova auto-adjunticidade. ModulatorPolar.lean:59–69 reúne positividade, auto-adjunticidade, injetividade, imagem densa e S = JA.
3. ModularSquare.lean:27–51 define o domínio de A² e Δ = A². ModularSquareAdjoint.lean:148 prova Δ auto-adjunto. TomitaAdjoint.lean:84–98 identifica o domínio de composição e S†S = Δ. A observação histórica de que o quadrado seria tarefa separada em ModulatorPolar:55–56 foi superada por essas fontes.
4. ModularFlowSpectrum.lean:26–29 usa os autovalores λ = towerW_i/towerW_j > 0; :62–78 prova simultaneamente a ação de Δ por λ e do fluxo por exp(it log λ) nos MESMOS vetores. :98 prova totalidade do span; :106 prova unicidade do operador limitado com essa ação.
5. ModularPower.lean:28 chama esse grupo deltaImaginaryPower; a abreviação vem acompanhada da caracterização espectral e unicidade em :30–39. A interpretação como Δ^{it} usa o dicionário usual do cálculo espectral do Δ positivo auto-adjunto, agora com aplicabilidade sustentada por uma família total e a unicidade provadas.
6. ModularFlowAlgebra.lean:63 define modularConjugation pelo automorfismo de conjugação da unidade modular; :67 identifica sua restrição local; :112 preserva M nos dois sentidos. ModularFlowHilbert.lean:104 dá continuidade forte em todo vetor. ModularPower.lean:49–69 fixa Ω, preserva ω e reúne grupo/continuidade/invariância de M.

[REAL + DERIVED/KNOWN na tradução espectral] A convenção local é α_t(A) = Δ^{it} A Δ^{-it}; em cada andar, α_t(a) = ρ^{it} a ρ^{-it}. ModularFlowLevel.lean:28 define modularPhase(t,r) = exp(i t r). Não trocar por α_{−t} sem transportar explicitamente o sinal do Hamiltoniano na referência importada.

## 3. Standard form, cone natural e KMS

[REAL — resultado de busca delimitada] Na árvore TGLExt canônica, não foi localizado objeto nomeado NaturalCone/naturalCone/natural_cone/StandardForm/standardForm/standard_form nem referência a cone self-dual na varredura desta auditoria. ClosedAntilinearStandardSubspace.lean trata um subespaço real padrão de um Hilbert; seu cabeçalho :11–14 e a importação :32 deixam claro outro objeto. Não o usar como forma padrão da álgebra M.

[KNOWN — aplicabilidade] O par cíclico e separante de uma álgebra de von Neumann fornece sua representação padrão e o cone natural na teoria usual. Pela leitura primária enviada pela raiz, Araki Corolário 4.4 é formulado diretamente para Ψ cíclico-separante e h = h* ∈ M; portanto um registro Lean separado do cone não é uma hipótese adicional necessária para esta aplicação.

[REAL — limite do enunciado] RightMult.tState_kms e FiniteTomita.gibbs_kms são identidades KMS de Gibbs em andares finitos. A invariância modularConjugation_preserves_state prova estacionariedade; isoladamente, estacionariedade não é a condição KMS analítica. A interpretação KMS do estado de referência é a aplicação da teoria modular ao par já identificado; a do estado perturbado vem do teorema de Araki/identificação de sua ação modular. Não se deve declarar que a estacionariedade, sozinha, provou o enunciado de faixa complexa.

## 4. Perturbação efetiva e convenções de cociclo

[REAL — lote 63] Em Chatgpt/INTERACAO_LOCAL_SOMAVEL_20260909_143042_266556/AdmissiblePauliInteraction.lean:12, SummableCouplingData contém a prova de Σ|c_j| < ∞. certifiedInteraction P c é o limite normado de Σ c_j X_j X_{j+1}. :26 e :30 provam auto-adjunticidade e pertença a M; :38 limita sua norma. O perfil P é o mesmo da construção acima. A propriedade de ser um operador contínuo linear já o torna limitado.

[REAL — lote 63] DUHAMEL_UNITARIO_20260909_153247_640286/PauliCocycleGenerator.lean:19 e :28–32 provam para o cociclo construído:
- u(0) = 1 e u'(0) = iV (u(0) é fornecido pelo módulo de cociclo);
- u'(t) = u(t) · i α_t(V), na norma dos operadores;
- u(s+t) = u(s) α_s(u(t)), com a α canônica.

DINAMICA_MODULAR_PERTURBADA_20260909_155658_929243/PauliPerturbedDynamics.lean:16–24 define β_t = Ad(u_t) ∘ α_t. Seus resultados de grupo, fator e norma são prévios e não ficam reabertos nesta nota. A continuidade temporal em norma é provada para observáveis cuja órbita α já seja contínua em norma; isso inclui V. A continuidade forte de α e a continuidade em norma de u também sustentam a continuidade forte da dinâmica implementada, por composição usual. Não exigir continuidade em norma de α em todo B(H).

[DERIVED — controle finito da normalização] Na convenção α_t(a)=ρ^{it}aρ^{-it} e u_t=exp(it(logρ+V))exp(−it logρ), a densidade normalizada é
ρ_V = exp(logρ+V)/Z, Z = Tr exp(logρ+V) > 0.
Então ρ_V^{it}ρ^{-it} = Z^{−it}u_t. A fase central não altera Ad(u_t), mas altera a derivada na origem por −i log Z · 1. Esta fórmula é um controle de sinal/normalização; esta nota não a apresenta como nova prova Lean nem define traço global onde ele não existe. No caso geral Z deve vir da norma quadrada do vetor perturbado, não de um traço global do fator.

A raiz está conferindo a correspondência entre o parâmetro h do artigo (convenção H = −log Δ) e nosso V. O mapa de sinal deve ser registrado antes de chamar o cociclo normalizado de derivada de Connes do estado normalizado.

## 5. O que já não é uma falta e o que precisa de ligação explícita

[DERIVED + KNOWN] A existência matemática do estado perturbado fiel normal para esse V limitado já tem suas hipóteses locais disponíveis. Não restringir essa conclusão ao estado de Bloch, ao perfil tracial ou ao centralizador. Não exigir que se reprove integralmente Araki para aplicar uma importação matemática válida.

[OPEN — tradução/formalização interna, não inexistência matemática] Restam para a aplicação ser um objeto explícito do programa:
1. Registrar o enunciado importado de Araki com sua referência primária, a convenção de sinal e o transporte dos dados (M, Ω, α, V) já demonstrados; construir/nomear seu vetor e o normalizador, distinguindo resultado KNOWN aplicado de teorema Lean novo.
2. Ligar o estado normalizado e seu grupo modular à β já construída; registrar KMS no sentido analítico correto. Uma prova de preservação do estado, isolada, não substitui essa ligação.
3. Identificar o cociclo proveniente do teorema com o nosso cociclo, usando as mesmas convenções e a unicidade apropriada da equação diferencial; separar a fase central de normalização. Nenhum desses pontos autoriza introduzir a derivada do limite como hipótese: ela já foi provada.

As rotas canônicas anteriores têm escopo útil porém distinto. TowerGibbsPerturbation.lean:27 define filtro DIAGONAL finito; :137/:151/:157 provam separação/fidelidade/seqWOT desse vetor. LikelihoodCocycle.lean:98–107 prova que o cociclo é fixado por α antes de usar a lei torcida, e trabalha sobre thirdThermalReference. Essa rota não instancia automaticamente o novo XX fora do centralizador. Ela não invalida a aplicação geral de Araki ao novo V.

O tratamento de interações gerais locais em andamento é uma generalização da classe de V; a aplicação matemática a cada V limitado auto-adjunto do fator mantém os mesmos dados de referência. Não implica retirada da parede UV, nem fechamento de todas as anomalias de uma teoria relativística.

## 6. Evidência medida

Resultado desta auditoria: **PASS_REFERENCE_DATA_SCOPE**, 98/98 verificações.
Foram medidos 25 arquivos canônicos selecionados e seus binários canônicos/copias pinadas. Os 20 nomes centrais selecionados aparecem no FullTGLAudit do último build com axiomas contidos no trio propext, Classical.choice, Quot.sound.

O recibo incremental tem 21 processos exit 0, FullTGLAudit com 5348 linhas e NewModulesAudit com 1098. O recibo é de escopo incremental: os módulos canônicos foram carregados de binários pinados, sem recompilação de suas fontes nessa corrida, e não afirma hash de toda dependência transitiva externa. Essa limitação permanece explícita no JSON.

Arquivos desta entrega:
- [Evidência de dados e pins](C:/IALD/Central de Patentes/Chatgpt/MAPA_ARAKI_REFERENCIA_20260909_165524_615258/EVIDENCIA_DADOS_REFERENCIA.json).
- [Manifesto](C:/IALD/Central de Patentes/Chatgpt/MAPA_ARAKI_REFERENCIA_20260909_165524_615258/MANIFESTO_MAPA.json).

Nenhum um.py foi executado ou importado. Nenhum arquivo original, memória canônica ou fonte congelada foi modificado.
