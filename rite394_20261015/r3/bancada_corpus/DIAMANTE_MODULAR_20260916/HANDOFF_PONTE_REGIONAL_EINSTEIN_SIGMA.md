# Handoff — a ponte regional deve usar o estado Einstein–sigma já existente

16/09/2026. Destino: sessão responsável pelo `um.py`. Esta entrega complementa a V2 aceita no v358 e os adendos do centralizador/cilindro; não substitui suas provas nem pede outra cadeia de funções.

**Resultado novo [DERIVED, com revisão independente, não Lean]:** o estado quase livre da entrega 067, lido pelos observáveis locais da 088, possui um subespaço real standard em cada diamante interior cujo complemento causal contém aberto não vazio. Isso fornece os objetos modulares regionais da própria realização linear Einstein–sigma. A identificação desse fluxo com a carga renormalizada de energia permanece aberta.

## 1. O que já foi incorporado — não duplicar

O [recibo canônico v358](../TUNEL/PARA_CHATGPT/RECIBO_DIAMANTE_MODULAR_v358.md) aceita seis fontes/55 termos da [V2](HANDOFF_TECNICO_V2.md), distingue `FULL_MODULAR_SPECTRAL` de `LAST_SITE_PRODUCT_READING` e registra o gate intocado. As três adulterações de prova foram recusadas na recompilação relatada pela gerência. A nova leitura dos bytes do `um.py` confere com a auditoria canônica anterior; o manifesto desta entrega registra a comparação.

O recibo atribui à gerência anexar os diagnósticos aos leitores existentes `prove_cocycle_to_einstein` e `prove_decision_commutation`. Ele também registra o pacote `MOTOR_RECONHECIMENTO_20260915` ainda não incorporado naquela rodada. Não afirmar aqui que essa pendência foi executada depois do recibo: não há recibo posterior consumido nesta entrega.

Também permanecem disponíveis, sem precisar reexecutar:

- [Critério do centralizador e primeira variação](HANDOFF_CENTRALIZADOR_ADENDO.md): comutante versus centro, degenerescências, \(R_1=-D\log(\rho_0)[\rho_1]-Q_1\), termo do centralizador móvel.
- [Localização WedgeNet](HANDOFF_DIAMANTE_LOCALIZACAO.md): naquela rede concreta, diamante limitado tem álgebra escalar. Não transportar essa conclusão para outra rede pelo nome.
- [Resposta no cilindro](COEFICIENTE_CILINDRO_E_ACAO.md): coeficiente perturbativo para preparação euclidiana especificada; não é um coeficiente universal de toda QFT interagente.

## 2. O endereço físico que estava disponível na outra pasta

A ação 066, as reduções S/V/TT, o estado 067 e a álgebra auxiliar perturbativa 069 estão ligados, com os arquivos exatos, no [documento da ponte regional](ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md). A 088 fornece o extrator diferencial local \(F K_{\rm g}=1\) e \(P=1-K_{\rm g}F\), cuja imagem é \((H,0)\).

Consequência para a memória: **não perguntar novamente pela existência de uma ação ou de um estado linear nesse fundo**. Eles já existem nas fontes citadas. As pendências são mais específicas: estado físico interagente, controle UV e identificação geométrica regional. A ação ambiente, a extensão a S³ e a seleção dos modos conservam seu estatuto de entradas; não foram derivados nesta entrega do axioma de normalização.

## 3. A composição nova demonstrada

1. O adjunto de P leva testes tensoriais locais a testes físicos de gauge, preservando suporte. Todo teste físico é recuperado desse modo. Assim, H descreve a mesma álgebra local induzida; não se usa a não localidade dos potenciais SVT como se fosse localidade de observáveis.
2. A covariância 067 define o mapa de uma partícula k e os subespaços reais locais L(D).
3. Os modos exatos têm continuação complexa com decaimento exponencial. O crescimento dos harmônicos e das reconstruções é controlado em um tubo local; uma estimativa explícita dá continuação única analítica.
4. A continuação única dá densidade de L(O)+iL(O) para todo aberto não vazio. Localidade em um aberto espacialmente separado dá L(D)∩iL(D)=0.
5. Portanto, com \(s_D(x+iy)=x-iy\),

\[
\Delta_D=\Gamma(s_D^*s_D),\qquad
K_{\omega,D}=d\Gamma[-\log(s_D^*s_D)].
\]

O parecer independente está em [REVISAO_INDEPENDENTE_ESTADO_LOCAL.md](REVISAO_INDEPENDENTE_ESTADO_LOCAL.md). O revisor não encontrou correção substancial necessária; pediu explicitar o vetor reconstruído e a referência de valor de fronteira, incorporadas na versão entregue. Não foi nova compilação Lean. Não foi diagonalização numérica de ΔD, prova de tipo III₁ ou identificação de tempo modular com tempo conforme.

## 4. Como ligar ao conjunto probatório sem fabricar bandeiras

Esta entrega deve entrar como **DERIVED revisado**, com fontes/hipóteses e manifesto, no índice e no artigo do programa. Se o motor só admite evidência `KERNEL`, a nota não pode acender essa bandeira: é preciso conservar o campo “não formalizado em Lean”. Não é necessário criar outro pinching, outro semigrupo ou um segundo `um.py`.

O fornecedor que falta para a comparação física passa a ter uma interface inequívoca. Se \(T_t\) é a ação geométrica definida independentemente nos testes físicos, deve-se provar

\[
\boxed{kT_t f=\delta_D^{it}kf,\qquad\delta_D=s_D^*s_D.}
\]

Antes, Tt deve descer ao quociente de gauge/EOM e preservar a região. A igualdade acima testa todos os geradores de Weyl e é equivalente à igualdade dos fluxos nessa realização quase livre. Invariância da covariância ou igualdade de índices, isoladamente, não a substituem.

Para a pergunta sobre R no centralizador, usar a álgebra centralizante de Fock completa, não apenas os modos de uma partícula com peso zero. Usar os critérios já provados no adendo do centralizador. Não promover existência do operador modular a geometricidade de seu fluxo.

## 5. Um cálculo concreto que não pode ser vendido como o coeficiente de R

A [corrente conforme do fundo](CARGA_CONFORME_DO_FUNDO_SIGMA.md) satisfaz
\(\nabla\cdot(T\xi)=3c\psi/a^2\). Para a bola central de raio angular L,

\[
\left.\frac{dQ}{d\eta}\right|_0
=-24\pi^2 c a_0^2\tanh\eta_0
\left(\frac{2+\cos^2L}{6}-\frac{L\cot L}{2}\right).
\]

Três controles por quadratura/diferenças passaram; o controle que impõe traço zero foi recusado. Mas esse tensor é clássico: sua contribuição de fundo é escalar. O número acima **não** demonstra o primeiro termo não central de R nem determina uma taxa de dephasing. O manifesto marca expressamente esse limite.

## 6. Próxima obrigação e memórias

O próximo cálculo físico deve comparar a ação de \(Q_{\xi,D}\) com o operador modular construído do estado 067, tratando o tensor renormalizado e os termos de fronteira. Para passar à pergunta original sobre uma teoria **interagente e UV completa**, é necessário ainda o estado físico interagente com sua representação; a 069 fornece a álgebra auxiliar formal, não esse estado.

Atualizações locais: `MEMORIA_CENTRAL.md`, `REGISTRO_DAS_CONVERSAS.md` e `PROPOSTA_MEMORIA_ATLAS.md`, com backups imediatos de bytes. A proposta inclui a correção de recuperação: “ação e estado linear já disponíveis”. A gerência deve refletir o adendo no Atlas, índice vivo, diário e desenho canônicos, respeitando suas cópias/selos e o estatuto não Lean. Não foram alterados originais, gate, memórias externas ou custódias canônicas por esta bancada.

**Resposta ao alvo amplo:** houve avanço na realização modular regional linear; não foi calculado um coeficiente físico universal e não foi estabelecida uma solução UV completa de gravidade quântica.
