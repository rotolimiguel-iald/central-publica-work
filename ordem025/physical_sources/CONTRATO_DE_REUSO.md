# PONTE PARCIAL — peças autorais recuperadas para massa e Clausius/H3

Em nome de codex-gerente-tgl, 25/10/2026, F1.PONTE_NOMEADA, reivindicação 1217. Continuação da ORDEM 025; fonte vigente da quarta fala é apenas o recorte declarado do ADENDO A. Esta camada é documental e algébrica, candidata à gerência. Não houve nova compilação Lean, execução/importação de um.py ou consulta a dados observados. A fonte atual lida é um.py **v401**; as peças v394 que ela conserva continuam com seus nomes históricos.

## 1. O que o levantamento resolve

A energia do boost já chega ao calor na construção óptica, e uma família curva com correspondência de área em todas as direções já existe. Portanto, não se deve registrar genericamente “falta construir o calor” ou “não há habitante de H3”. Falta ligar a realização física da ORDEM 025 aos fornecedores corretos, com a mesma fonte, estado e geometria. Essa distinção reduz a próxima construção e evita refazer as pedras existentes.

| Peça | Estatuto e alcance | Próximo consumidor |
|---|---|---|
| `PonteDaEscalaDual`: p⁺=τ, p⁻=μ²/τ, m²=E²−p² | [REAL — build anterior custodiado]; equivariância e casca para μ² fornecido | Fornecedor físico da massa e normalização dimensional |
| Energia confinada, potenciais e modos de cavidade | [DECLARADO] nas fontes; mínimos e resíduos [DERIVED] sob as hipóteses de `MASS_SOURCES` | Estado, ocupações, acoplamentos e contorno independentes do resultado |
| Clock local → densidade → fluxo de contorno | [DERIVED] condicional ao kernel local, identificação do lapse e regime fraco | Massa gravitante do perfil especificado; identificação com massa invariante ainda separada |
| Origem de energia Gibbs finita | [DERIVED] no contrato conservado pela v401 | Elimina Eref livre dado o estado/clock; não seleciona κ ou V0 físicos |
| `boost_energy_flux_constructed`, `boost_energy_heat_constructed` | EXISTE E ESTÁ LIGADO na família óptica; fonte Lean e auditoria histórica recuperadas | Identificar a carga da ORDEM 025 com o mesmo tensor/fluxo |
| `matched_constructed_area`, `matched_wave_einstein_from_area` | EXISTE E ESTÁ LIGADO na família plane-wave construída | Identificar o sistema físico com essa família, conservando a seleção explícita dos coeficientes |
| `MaxwellBoostChargeAssemblyR1` | EXISTE NA BANCADA, fiação condicional da cunha padrão | Mesmo Q físico, `BoostChargeIdentity`, estado regular de carga não nula |
| `metric_einstein_from_screen_clausius` e colagens | EXISTE E ESTÁ LIGADO como implicação condicional | Mesmo g,T conservado e H3 em todo ponto/direção |

Fontes integrais por arquivo, SHA256 e linhas: `MASS_SOURCES.json`, `H3_SOURCES.json`, `ROOT_SOURCES.json`. Estatuto de leitura de uma fonte não substitui recompilação; o build da ORDEM 025 é reaproveitado pelo recibo anterior.

## 2. Seleção da massa: receitas concretas, tipos diferentes

O texto autoral de luz confinada escreve mc²=∫g|γ|²dV e, no caso estacionário, mc²=hν. O espectro de cavidade fornece k_n=nπ/L, dadas a geometria e as condições de contorno. O potencial quártico já escrito fornece, no ramo radial real com λ>0,

    V(x)=λ(x²−v²)²/4 + μ₀²x²/2,
    V'(x)=x[λ(x²−v²)+μ₀²],
    x₀²=v²−μ₀²/λ,   V''(x₀)=2(λv²−μ₀²).

O ramo não nulo requer λv²>μ₀². A curvatura vira massa/frequência de excitação somente com cinética, unidades e normalização definidas. A expansão histórica em x=v deixa V'(v)=μ₀²v: essa parcela não pode ser omitida sem condição adicional. O potencial sêxtico e sua condição de estabilidade também já constam do acervo. São fornecedores condicionais de amplitudes e massas de campo, não um valor de massa corporal determinado apenas por τ. Os parâmetros acima não são o μ² do lift por identidade de nome.

A trilha do clock é mais direta para um corpo no regime fraco. Com u=log(R_mod/θ_M), a receita existente dá

    ρ_eff=−c² Δu/(4πG),
    M(B)=−c²/(4πG) ∮∂B ∂n u dA.

Assim, um fluxo de contorno determinado independentemente permite calcular a massa gravitante sem escolher toda a densidade interna. Mas a normalização assintótica não escolhe o fluxo. O controle algébrico desta consulta usa u_A=A(3−r²/R²) no interior e 2AR/r no exterior: u e sua derivada casam, u→0, porém M=2Ac²R/G. A e 2A produzem massas diferentes com a mesma normalização. É um controle do mapa de Poisson, C¹ e por partes C²; não se afirma que esses perfis sejam realizados pelo kernel modular físico ou satisfaçam a ação completa.

Também não se confunde essa massa gravitante efetiva com (i) o parâmetro de massa de uma equação de campo; (ii) `amplitudeMass`/`mass`, coeficiente de uma fonte de radiação; (iii) a massa invariante μ²=p⁺p⁻ do corpo. A identificação entre elas precisa de energia total, unidades, domínio e condições de conservação do mesmo sistema.

A v401 conserva `v394_gibbs_root_parameters` (um.py:220759–220805): Eref=(ħ/P)log[2cosh(PΩ)], P=2π/κ. Isso fixa a origem positiva de energia do estado Gibbs finito especificado. κ e V0 continuam entradas. O próprio contrato recusa identificá-lo automaticamente com −log Δ ou com uma calibração física universal.

## 3. Clausius/H3: o que está pronto e onde está a seleção

`BoostHeatConstruction.lean:34–56,91–104` identifica T(χ,k)dA e sua integral com o calor construído. `mass` nessa fonte é amplitude de `waveMatter`; não é a massa de repouso. Na sua tela óptica,

    equilíbrio quadrático ⇔ η(a+c)=2π·mass.

O símbolo c nessa fórmula é um coeficiente transversal da geometria, não a velocidade da luz. Os requisitos ópticos e a orientação de integração permanecem os do módulo.

`PlaneWaveEntropyMatching.lean:28–38,82–138` constrói uma família com a+c=2π·amplitudeCoupling(b)/η. Nela existem tela, calor, área e Einstein para todos os pontos/direções admitidos. A soma foi escolhida para o casamento; `shear` permanece livre. `state_alone_not_curvature_coordinate` mostra que o mesmo estado não seleciona a coordenada completa de curvatura dessa família. Isso limita a inferência “o estado sozinho escolhe a geometria”, não invalida H3 já construído na família.

O módulo geral explicita a dívida exata:

    MetricScreenClausius ⇔ Ric(k,k)=(2π/η)T(k,k).

Para Einstein com Λ constante entram g lorentziana suave, T simétrico e conservado, região aberta/preconexa, telas e essa relação em todos os pontos e direções nulas. Reconstruir qualquer T por rótulos unitários não o seleciona: `realized_source_eq` recebe g,T e devolve o T fornecido; conservação também é hipótese no consumidor geral.

Há uma rota quântica pronta de composição: `MaxwellBoostChargeAssemblyR1` deriva a normalização 2π a partir de `BoostChargeIdentity` e preserva o mesmo Q no H3 da cunha padrão. Faltam o fornecedor físico simultâneo dos campos dessa interface e sua ligação à realização da ORDEM 025; o adaptador não prova sozinho H3 curvo universal.

## 4. A ação completa foi recuperada; não repetir suas variações

R84–R90 já tratam a construção baseada no mesmo P, as variações e a fonte. No ramo real de 1-forma da R88, com f=F0+ξu, u=g⁻¹(A,A), a projeção nula da equação métrica estacionária é

    2f Ric(k,k)=T_M(k,k)+T_rest(k,k)
                +2ξ Hess(u)(k,k)−2ξ R A(k)².

Essa expressão é condicional à estacionariedade da mesma ação e às convenções declaradas. Para a fonte que efetivamente entra no calor, as parcelas de melhoria não podem ser descartadas ou renomeadas por conveniência. R89 já isolou o resíduo entre a equação de Euler da 1-forma e a EOM escalar pretendida; R90 preserva a pendência de representação e estacionariedade da ação completa. O critério humano de reconhecimento está compreendido; não se faz novamente a pergunta abstrata sobre identidade.

## 5. Contrato mínimo da próxima ligação

1. **Fornecedor do mesmo objeto físico.** Dar o mapa do elemento do core para estado/campo, com unidades e domínio. A receita autoral de energia confinada, a de clock ou a de modos pode fornecer energia/massa quando seus dados forem especificados. Não escolher μ² para acertar a conclusão.
2. **Fonte e carga comuns.** Construir T a partir desse mesmo estado/ação, com simetria, conservação e regularidade. Identificar a carga nula/fluxo correspondente a τ normalizado. A identidade de escala exp(−s) sozinha não identifica carga de translação, carga de boost e integral de calor.
3. **Compatibilidade das representações.** A ORDEM 025 usa eixo espacial 1, a tela óptica usa eixo 3 e k=(1/2,0,0,1/2). Explicitar o mapa de eixos, a normalização e a rapidez. O parâmetro do boost e o parâmetro afim do calor não são o mesmo por nome; o boost óptico curvo não é um Killing global automático.
4. **Seleção da geometria/área.** Reutilizar a família plane-wave como realização limitada, ou demonstrar a estacionariedade completa que forneça a relação nula em toda direção para a fonte física escolhida. Acrescentar `harea` produz um contrato condicional válido, mas não descarrega essa hipótese.
5. **Consumidores prontos.** Aplicar a ponte da escala, o calor construído, `metric_einstein_from_screen_clausius` e as colagens já existentes. Não reconstruir E=mc², a lei exponencial, Raychaudhuri ou a implicação Clausius→Einstein.

O ganho desta rodada é localizar fornecedores concretos e a junção que falta. Não foi demonstrado que exista um único fornecedor físico satisfazendo simultaneamente esse contrato. A próxima etapa material deve fornecer esse objeto ou uma subfamília precisamente delimitada; repetir inventário/provas antigas ou perguntar novamente a regra de identidade não resolve a pendência.

## 6. Erratas e limites que acompanham o reuso

- **Correção ao lado de M11 de MASS_SOURCES:** a fórmula histórica de Chandrasekhar não é adotada como previsão vigente. `tgl_paper_unified.py:17878–17898` retira expressamente G→G(1−β) e a validação por essa massa. O relatório preserva a fonte histórica para rastreabilidade; sua utilização é subordinada a esta errata. Os números empíricos citados nessa passagem não foram reavaliados aqui.
- A fórmula-beta de massa do Grande Atrator também está retirada no programa atual. A forma antiga não é um seletor recuperável por mera remissão. R13–R16 já mostram as dependências de amplitude, fonte e calibração; seus cálculos não foram refeitos.
- Os controles de quarta ordem ou igualdade finita não excluem H3 infinitesimal. A liberdade de shear não nega que Ricci possa satisfazer Einstein.
- A busca foi dirigida às fontes enumeradas; nenhuma alegação de ausência em todo C:\IALD. Os anexos guardam cobertura, linhas e hashes. Nenhuma alteração de kernel, um.py, Bancada, dados ou gate; nenhum sinal estatístico novo foi produzido.
