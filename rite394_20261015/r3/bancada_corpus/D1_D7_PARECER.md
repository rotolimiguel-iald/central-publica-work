# D1 e D7 — subsídios técnicos, sem decisão do operador

[REAL] Auditoria estática e controles sintéticos no snapshot `um_ordens003_004_snapshot.py`; identificação por SHA256 em `D1_D7_CONTROLES.json`. [DERIVED] Resultados condicionais abaixo. Nenhuma modificação proposta foi aplicada ao programa.

## D1: três condições, dois vereditos distintos

O censo está em `D1_CENSO_CONSUMIDORES.md`: 60 linhas, com função, papel e fonte. É exaustivo para os identificadores e chaves declarados no script; inclui propagação por `IDENTITY`, `identity_true`, certificados e `fiat_lux`. Não é uma prova de fluxo de dados para Python arbitrário: emissores que serializam um contêiner inteiro herdam seus campos sem citar a chave. Isso é especialmente relevante para hashes e selos.

As decisões diretas são `alive_ok` (linha 2470), `sub_a_conservation` (67591–67592) e `link_closed` (67608–67609). O veredito da janela também é conservado como número/chave no retorno. O arquivo `D1_PROPOSTA_DIFF.md` contém as três substituições obtidas por AST, sem aplicação.

Escreva I para o agregado das identidades internas sem os três módulos v3, W para todas as massas na janela, S para o fechamento EM, C para os testes contrafactuais exceto a janela e F para os demais testes do fluxo. Na fiação atual, os caminhos relevantes são `link_closed=I∧W`, `sub_a=I∧W∧S`, e o CONTRAF contém W. Retirar W só do ELO 2 deixa uma dependência residual no ELO 3: é preciso retirar as três condições juntas, preservando os números reportados.

O script avalia as expressões reais extraídas do fonte em 16 combinações sintéticas. Ao retirar W, `link_closed` passa a I, `sub_a` a I∧S e `alive_ok` conserva seu teste de igualdade de β. Se W já é verdadeiro, a alteração lógica não muda esses valores. Se W é falso e todo o restante passa, a identidade pode passar; se qualquer condição interna relevante falha, a identidade continua falhando. Não foi executado o rito completo com dados da natureza.

Efeitos a propagar na opção *sai*: `fiat_lux.checks` (renomear a chave que diz `and_in_window`), `all_verified` desse módulo, `internal_identity_checks.fiat_lux_counterfactual`, certificados ELO 2/CONTRAF, `identity_true`, `IDENTITY`, `reading`, o campo de identidade no selo e os textos que os consomem. Resultados de massa, limites da janela e comparações de literatura permanecem calculados e reportados. Hashes do programa e de qualquer resultado alterado devem mudar; isso não é mudança de veredito QG.

[REAL — análise da função] `prove_qg_closure_gate` e `evaluate_quantum_gravity_closure` não leem a janela, identidade ou CONTRAF. A chamada única é `prove_qg_closure_gate(ONE, kernel_formalization, independent_rite=void_floor_v11)` (linha 67220). O veredito depende dos próprios campos formais, físicos e do rito independente. Portanto, **mantidos esses argumentos**, alterar a fiação W não altera `qg_closure_verdict`. Isso não promete hashes iguais, nem dispensa recompilar/reverificar a versão futura. A inspeção não encontrou um caminho de `identity_verdict` para esses argumentos; a identidade é calculada posteriormente na rotina principal.

**O melhor argumento para manter:** preserva a regra de aceitação histórica v104 e seu teste de regressão para a escala do modelo legado. Um teste conservado pode detectar mudanças acidentais em constantes/unidades/geometria, mesmo sem funcionar como evidência independente. Se mantido, deve chamar-se requisito convencional de compatibilidade do legado. Não pode ser simultaneamente apresentado como prova física nova.

**O melhor argumento para retirar:** um critério de uma forma declarada aposentada não deve tornar-se necessário para afirmar o fechamento de outra construção sem uma ponte de equivalência. Há ainda dependência entre escala de entrada e literatura da janela. Isso reduz seu poder como validação independente, embora não a torne logicamente impossível de falhar. A recomendação técnica é separar o teste legado do fechamento interno, preservando-o no contorno.

**O que sobra no ELO 2:** checagens internas de normalização, conservação, covariância, identidades térmicas, forma de primeira lei e integridade executiva. Elas podem falhar como testes de implementação/consistência. Não se deve chamar isso automaticamente de falsificabilidade empírica da gravitação. Piso, neutrinos e dephasing continuam em seus protocolos próprios; esta proposta NÃO os insere silenciosamente no 1=1.

Complementos editoriais do diff proposto:

1. Atualizar docstring e `reading` para fechamento interno; revogar explicitamente, por ato do operador, a ressalva histórica v104 que mantinha a janela no gate de identidade.
2. Conservar `GA_ACCEPTED_WINDOW_Msun`, massas e `in_accepted_window`. Reportar em bloco CONTORNO o estatuto `SCALE_SHADOW_OF_RETIRED_FORM`, a comparação booleana e a origem histórica.
3. Mover `mass_rule` de `MODEL_AXIOMS` para uma seção histórica do contorno, preservando a expressão e sua proveniência. Ajustar emissores PT/EN e manifesto.
4. Desacoplar os textos “dentro/fora da janela” de `identity_true` (linhas 87480, 89383, 90072, 92014). **Já hoje** uma falha interna pode fazer o texto dizer “fora” mesmo com massa dentro. Para falar da janela, ler W; para falar da cadeia, ler `IDENTITY`.
5. Conservar a pergunta e a ratificação como atos do operador; produzir novos hashes e auditoria só após aprovação da fiação.

**Pergunta D1 reservada ao operador:** autoriza retirar a janela das três condições decisórias, mantendo-a integralmente reportada no contorno — sim ou não?

## D7: no-go para distâncias de intensidade; uma possibilidade distinta para coerência

### Hipóteses numeradas

D7.1 [REAL — fonte] O motor selado usa `H0_local=H0_CMB(1+Z_STAR)^β`, com Z_STAR fixo. `_dl_lcdm_mpc` tem toda a dependência em H0 no fator 1/H0; a integral depende de z e Ω_m.

D7.2 [INPUT] Na comparação, a função adimensional de expansão, a definição do redshift e as calibrações de luminosidade são mantidas. Então, para todo z>0,

    D_L,TGL(z)/D_L,base(z) = (1+Z_STAR)^(-β).

Em z=0 ambas as distâncias são zero, logo a razão 0/0 não é definida; a igualdade multiplicativa e o limite da razão continuam válidos. Qualquer número de objetos com distâncias deste mesmo modelo é degenerado com H0 reescalado. Não há um segundo z que resolva isso.

D7.3 [INPUT] Para examinar a lei de resposta, suponha dephasing puro na base de energia/transições relevantes, `dρ_ij/dt=-Γ_ij ρ_ij` para i≠j e `dρ_ii/dt=0`, com Γ_ij=(βτ★/2)(ω_i−ω_j)². **A frequência que entra é a diferença espectral da coerência observada**, não automaticamente a frequência óptica central de qualquer fóton. O programa dá também uma lei-raiz; sua redução quadrática exige o regime IR declarado pela casa.

D7.4 [INPUT] A detecção fotométrica considerada soma populações nessa base, sem conversão adicional de fase em perda de fótons, espalhamento angular, absorção, alteração de trajetórias ou seleção por interferência. O tempo que parametriza a dissipação é um tempo operacional especificado; a torre modular, sozinha, não o identifica com tempo próprio cosmológico.

[DERIVED — no-go da classe] Para todo observável diagonal B, `Tr(Bρ(t))=Σ_i B_ii ρ_ii(0)`. Logo o dephasing puro da hipótese D7.3 é invisível a essa classe de fluxos, independentemente de Γ depender de frequência. Duas bandas de intensidade incoerente continuam não distinguindo o mecanismo de uma reescala acromática. A torre unitária Δ^{it} não acrescenta, por si, um mapa de propagação dissipativo nem uma regra de fluxo fotométrico.

### Candidatos exigidos na ordem

| Candidato | Resultado sob as hipóteses acima |
|---|---|
| Duas bandas do mesmo objeto | [DERIVED] Não bastam para fotometria de populações. Podem servir se houver coerência mensurável e uma conversão fase→observável explicitamente modelada. |
| Drift temporal | [DERIVED] O motor atual com constantes congeladas não determina uma nova lei de drift. Para FLRW, drift depende de H(z); mudar apenas H0 muda a escala dos tempos, não identifica dephasing. Coerência em função do tempo fornece outro observável, condicionado a fonte e relógio operacional. |
| Distorção espectral da escada | [DERIVED] Populações espectrais são preservadas pelo canal ideal. Alargamento de linhas e correlações de dois tempos podem carregar dephasing, mas exigem modelo de emissão/correlação e resposta instrumental; não se inferem da densidade de intensidade diagonal isolada. |
| Dualidade D_L/(1+z)²D_A | [KNOWN/DERIVED] Com ótica métrica, geodésicas nulas e conservação de fótons, dephasing puro não produz violação: efeito zero nesta classe, a todas as ordens. Uma lei de opacidade seria hipótese adicional, não consequência de destruir coerência. |

Uma fórmula como `F=F₀ exp(-D)` ou `D_L=D_L,geom exp(D/2)` requer **perda efetiva de intensidade**. A igualdade `D=∫Γdt` não demonstra essa perda: trocar coerência por fluxo é o salto que a derivação recusa. Se uma transferência de energia/população ou detector interferométrico for especificado, refaz-se a análise nessa classe ampliada.

### Possibilidade condicional de separação: visibilidade, não uma nova distância

D7.5 [INPUT adicional] Prepare uma coerência de diferença espectral Δω, meça visibilidade V, conheça V₀ e o tempo T; suponha τ★ constante e ausência/controle dos demais canais. Então

    V(T)/V₀ = exp[-(βτ★/2)(Δω)²T].

[DERIVED] Uma simples alteração constante de H0 não atenua a coerência normalizada de um experimento local de tempo fixado. Esse observável pode separar os mecanismos, se o acoplamento da lei ao sistema escolhido for demonstrado. Não é uma predição nova de D_L da TGL.

D7.6 [CONJECTURE adicional para transporte cosmológico] Se o gap local acompanha Δω(z)=(1+z)Δω_obs, se o tempo dissipativo é o próprio dos observadores comóveis e se τ★(z) é especificado, a integração de dt=−dz/[(1+z)H(z)] dá

    -log(V/V₀) = (β/2)(Δω_obs)² ∫₀ᶻ τ★(u)(1+u)/H(u) du.

Isso tem dependência genuína em z e no gap, mas as três pontes de D7.6 não estão demonstradas pela análise modular da torre. Fontes astronômicas incoerentes podem ter V₀=0: nesse caso a razão nem sequer define um observável utilizável. Não recomendo congelar essa expressão como previsão já derivada de distância.

### Magnitude e controles, sem dados alvo

[REAL — cálculo sintético] O script usa `ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime. Sob τ★=5,391247×10⁻⁴⁴ s [INPUT ilustrativo] e Δω=10¹⁵ rad/s, Γ≈3,24319×10⁻¹⁶ s⁻¹. Em um segundo, 1−V/V₀≈3,24×10⁻¹⁶. O valor de τ★ e o gap relevante devem ser justificados, não ajustados depois do dado. Grandes tempos cosmológicos não dispensam a demonstração de coerência da fonte e regime de validade.

Controle racional: o canal com retenção c=1/2 envia a matriz do estado |+⟩ para diagonais 1/2 e fora-diagonais 1/4. A intensidade total fica 1; a probabilidade no analisador |+⟩ passa de 1 para 3/4. Dobrar o gap, com a mesma lei quadrática e tempo, dá retenção c⁴=1/16. Assim a invisibilidade da fotometria e a visibilidade interferométrica coexistem exatamente.

### Rascunho de pré-registro — NÃO ADOTADO, NÃO CONGELADO COMO APOSTA

Nome proposto: COHERENCE_SEPARATION_DRAFT_V1. Objeto: coerência preparada de dois níveis, com gap e tempo controlados (classe laboratorial a selecionar pelo operador; nenhum conjunto de dados foi escolhido ou aberto para teste). Observável primário: inclinação de `−log(V/V₀)` em (Δω)²T, em ao menos dois gaps e tempos, com calibração de V₀ e orçamento de ruído previamente fixados. Fixar antes do dado: sistema, τ★, validade IR, protocolo de preparação, estatística, incertezas e limiar mínimo de potência.

Kill-rule proposta: rejeitar a hipótese registrada se a inclinação estimada for incompatível com βτ★/2 pelo critério bilateral previamente congelado; rejeitar também a forma quadrática se um teste de falta de ajuste, previamente definido, a excluir. Ausência de potência, calibração insuficiente ou incoerência inicial → INCONCLUSIVE/UNDERPOWERED, jamais aprovação automática. Vereditos `CONFIRMED`, `PROVED` e “QG resolvida” proibidos. Não escolher limiar numérico sem desenho instrumental e análise de potência. Esse rascunho ainda não é um pré-registro executável.

**Pergunta D7 reservada ao operador:** autoriza desenvolver e pré-registrar um teste de coerência, em vez de tratar outro D_L do motor atual como separação — sim ou não; se sim, qual sistema/dado alvo deseja reservar?

### Fontes teóricas

[KNOWN] [Marquardt e Püttmann, Introduction to dissipation and decoherence in quantum systems](https://arxiv.org/abs/0809.4403), para o modelo de dephasing. [KNOWN] [The resilience of the Etherington–Hubble relation](https://academic.oup.com/mnras/article/513/3/4004/6567878), para as hipóteses da dualidade. Nenhum resultado observacional desses trabalhos foi empregado em ajuste ou veredito. A leitura autorizada do fonte incluiu constantes já presentes no programa; nenhum conjunto observacional novo foi acessado ou usado.
