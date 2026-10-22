# Consulta matemática — polar do mapa gaussiano

2026-09-12T20:59:33.242354-03:00. **Somente leitura/análise conceitual; sem recompilação ou revisão DEV formal.** A fonte `BoundedInjectivePolar` ainda não foi anunciada congelada. Não se certifica integração, execução dos auxiliares novos ou alteração de memória.

**Diagnóstico:** a rota proposta é matematicamente válida, com obrigações concretas de restrição e densidade. Não identifiquei obstrução ou hipótese externa nova necessária para obter um vetor cíclico separante na mesma π. Ela não identifica o J desse vetor com o J polar já construído para o peso e, portanto, não conclui a inclusão inversa.

Escreva H=H_I, E=L²(ℝ,L²(ℝ,TowerHilbert P)), ρ=dualOrbitRepresentation|N, Ωg=scalarGaussianVacuum P e C=scalarGaussianGNSMap P. O espaço-alvo correto da unitária é K=closure(Ran C), subespaço fechado de E; não se deve fornecer `DenseRange C` no ambiente E inteiro sem prova.

1. **Obter o subespaço redutor.** Já existe Cπ(a)=ρ(a)C para todo a∈N (`scalarGaussianGNSMap_intertwines`). Aplicá-lo também a a* e passar ao fecho prova que K reduz ρ(N). Definir a restrição ρ_K como representação estrela e C_K:H→K por codRestrict. A completude de K vem do fechamento; C_K é injetivo e tem imagem densa por construção. O mapa C não precisa preservar H_I dentro de E.

2. **Igualdade com o espaço cíclico: dois sentidos distintos.** A identidade existente CΛ_I(a)=ρ(a)Ωg e a densidade de Λ_I(I) dão K⊆closure(ρ(N)Ωg). Para o sentido contrário basta provar Ωg∈K: usar X_h=regularAverage P h, h>0. Já existem X_h∈I, ‖X_h‖≤1 e X_h→1 fortemente. `dualOrbit_tendsto_of_uniformly_bounded` fornece ρ(X_h)Ωg→Ωg; cada termo é CΛ_I(X_h). Como K é fechado, Ωg∈K, e a invariância do item 1 dá closure(ρ(N)Ωg)⊆K. Usar h↓0 com filtro não vazio, ou uma sequência positiva; X_0=0 não é a identidade. Não é necessária igualdade I=nν, inversa de g ou continuidade geral da estrela em SOT.

3. **Polar limitado sem inversa limitada.** As fontes lidas seguem a construção correta D=(C_K* C_K)^(1/2), ‖Dx‖=‖C_Kx‖, ker D=0 e Ran D densa por auto-adjunticidade. A regra V(Dx)=C_Kx estende-se a uma isometria; sua imagem é fechada pela completude de H e densa em K, logo V:H≃ₗᵢK é unitária. `DenseLinearPolarExtension` pede as duas densidades e igualdade de normas explicitamente. Não exige um limite inferior positivo para C ou D. O primeiro módulo tem log autoral rc0 compatível com a fonte lida; o segundo foi examinado como fonte em desenvolvimento, sem aceitação por log histórico de bytes diferentes.

4. **Transportar a representação, não apenas os espaços.** `BoundedInjectivePolar_intertwines` exige C_K A=B C_K e C_K A*=B* C_K. Esses dois fatos são necessários para deduzir que C_K* C_K e sua raiz comutam com A, e então V A=B V por densidade de Ran D. Na aplicação, ambos vêm do mesmo entrelaçamento para a e a*, depois da restrição redutora. Só uma unitária abstrata H≃K não bastaria para afirmar que a representação transportada é a π existente.

5. **Vetor no mesmo H_I.** Após os itens anteriores, definir ξ=V⁻¹Ωg (com a pertinência Ωg∈K explícita). De Vπ(a)ξ=ρ_K(a)Ωg, a igualdade do item 2 dá ciclicidade. Se π(a)ξ=0, o entrelaçamento dá ρ(a)Ωg=0; `scalarGaussianVacuum_separating` devolve a=0. Assim ξ é separante para a imagem π(N). Não se pressupõe separação para B(E) nem para uma álgebra maior não identificada com ρ(N).

**Utilidade e fronteira modular.** Isso fornece uma realização cíclica separante da mesma representação, adequada para formular uma rota vetorial à inclusão inversa. O seu Tomita S_ξ e a conjugação J_ξ são objetos novos até demonstração de uma ponte com os do peso. O fato já existente `(C×C)(graph S)⊆graph S_g` (e seu transporte de fechos) não permite cancelar D na fatoração C=VD: D pode ter inversa não limitada e transportar normas de gráfico exige prova própria. Entrelaçamento com a ação esquerda também não identifica operadores antilineares não limitados. Para manter o alvo original, a obrigação relevante será ligar a conjugação polar transportada ao J do peso; exigir igualdade completa S_ξ=S pode ser mais forte que o necessário e não decorre desta etapa.

O vetor transportado representa o funcional gaussiano limitado a↦⟨Ωg,ρ(a)Ωg⟩, e não automaticamente o peso ν original. A expressão contém g² e o mesmo fator Haar; normalizar ξ, se desejado, requer sua norma explícita. Não tratar a existência de ξ como prova de KMS, identificação de Δ^it, traço ou mudança de flags.

Próximos enunciados úteis (obrigações propostas, não resultados Lean certificados nesta consulta): K redutor; Ωg∈K; K=closure(ρ(N)Ωg); existência de V com Vπ(a)=ρ_K(a)V e V|C_K|=C_K; ξ∈H_I cíclico e separante para a π existente. São suficientes para encerrar a preparação descrita pelo autor, preservando a ponte J_ξ↔J como questão posterior.

Pins das fontes consultadas, lidos por script na conclusão (não equivalem a congelamento/compilação independente):

| Fonte | SHA256 |
|---|---|
| DenseLinearPolarExtension.lean | `2352e0b01e9ba17bb01914e98d1a778e454202430ce9e9a2042532fd0c34c159` |
| BoundedInjectivePolar.lean | `4a019e0848af8b60961d4d5e3348c6d4c5db901b868f6a5692b73078a7f4c0c4` |
| ScalarGaussianGNSMap.lean | `6117bb893d263a1044e4d589428d8ec335ae9c2884291edce8bdd7b6a029db28` |
| ScalarGaussianVacuum.lean | `2b033f830a3b39bfbc2efcb54bddbfc96439533f3b4dc66fa03bb6aed59e9b27` |
| DualOrbitStrongLimits.lean | `6fdea7f8bb2fadb447c419c35ed5d03a6a622e51f3143623163afb6605179a64` |
| ScalarGNSCompletion.lean | `658c9b58fb79da9700d94c2e4f8cd1f52cad7f8b71eb98df3d5608a350106e5c` |
| DualSemifiniteIdeal.lean | `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3` |
| RegularApproximation.lean | `cf847f376210447912ca2d08644c06e66375a6f89e82cffe844a241f92c89414` |
| ScalarGaussianClosureTransport.lean | `040851e72886d52824c03a97488bc426c079ac21d83017f7c2a051b3af88864d` |

Nenhum rebuild, monólito, recorder, fonte autoral ou memória foi executado/alterado. Esta consulta não substitui o futuro parecer DEV com manifesto congelado.
