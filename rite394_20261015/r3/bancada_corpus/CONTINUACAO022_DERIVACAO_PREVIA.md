[DERIVED / INPUT / OPEN] CONTINUAÇÃO 022 — resposta quadrática de uma evolução unitária explícita

06/09/2026. Derivação anterior ao código. A etapa 021 foi progresso: auditor reconferiu 610 hashes, sete módulos limpos, 49 teoremas e três definições impressas. Túnel com ordens 001–007. O objetivo amplo permanece ativo.

## Alvo e alcance

Construir um modelo finito autônomo que gere a resposta inicialmente quadrática dos pesos reduzidos, sem postular diretamente p(t)=p+t²q. Calcular a densidade bipartida, a marginal, a entropia e a variação modular na MESMA evolução. Depois aplicar a decomposição de 021 e identificar o que ainda exige correspondência física.

O modelo é uma dinâmica candidata de dois níveis no setor correlacionado de dois qubits. Seus parâmetros são INPUT. Não é a dinâmica canônica do um.py, não substitui a face hiperbólica nem contorna o negativo de Borchers da torre-produto. O fluxo finito é unitário e periódico.

## Derivação analítica

Sejam a,b reais com a²+b²=1. Definir

    M=[[a,b],[b,−a]], H=ωM,
    U(t)=cos(ωt)I−i sin(ωt)M.

M é hermitiano e M²=I. Portanto U(s)U(t)=U(s+t), U(0)=I, U(t)†=U(−t) e U(t) é unitário. Verificar a derivada verdadeira U′=−iHU e a conservação U†HU=H. Essa energia total não é identificada com o gerador modular da marginal.

O estado inicial no setor correlacionado é

    Ψ(0)=u|00>+v|11>, u>0, v>0, u²+v²=1.

Após U(t) no setor, as amplitudes são

    z0(t)=u cos(ωt)−i(a u+b v)sin(ωt),
    z1(t)=v cos(ωt)−i(b u−a v)sin(ωt).

Inserir (z0,z1) em C²⊗C² pela isometria |i>↦|ii>. Construir a densidade |Ψ(t)><Ψ(t)|, verificar positividade, traço um, idempotência e calcular a marginal por traço parcial. Quando necessário, explicitar a extensão hermitiana do Hamiltoniano ao setor bipartido.

Os pesos calculados são

    r0(t)=u²+C sin²(ωt), r1(t)=v²−C sin²(ωt),
    C=(a u+b v)²−u²=b²(v²−u²)+2abuv.

A normalização é exata. A não negatividade global deve vir dos módulos quadrados das amplitudes, não de uma hipótese sobre C. A positividade estrita é local ao redor da referência fiel.

A tangente dos pesos é proporcional a sin(ωt)cos(ωt) e zera em t=0. O coeficiente quadrático de r0−u² é ω²C. Aplicando a prova de 021 à curva REAL de pesos reduzidos,

    D(r(t)||r(0))/t² → 0,
    ΔK(t)/t² e ΔS(t)/t² → ω²C log(v²/u²).

Aqui K é o gerador diagonal da referência, já ligado ao traço matricial. A entropia relativa é a da marginal diagonal; não se atribui a mesma fórmula à densidade bipartida pura.

## Ponte gravitacional e sinais

Com os dois erros de identificação de 021 (calor–modular e entropia–área) de ordem o(t²), a resposta unitária fornece a anulação de D/t² e, portanto, Clausius. A existência dos dois erros pequenos no modelo geométrico geral continua INPUT/OPEN.

A correspondência entre o parâmetro do grupo unitário e o parâmetro afim da curva geométrica ainda precisa de justificação. O modelo finito mostra disponibilidade matemática de uma resposta quadrática; não escolhe por si a solda, a região, a unidade ou o tensor T.

Controles exatos: u=3/5, v=4/5, ω=1. Para a=0,b=1, C=7/25>0. Para a=−3/5,b=4/5, C=−176/625<0. Como log(16/9)>0, os sinais das respostas de entropia/modular são opostos. A escolha do Hamiltoniano importa; um único sinal não pode ser imposto pela palavra unitário.

No caso de coeficiente L=ω²C log(v²/u²), comparar a integral de calor de 020 dá, sob identificação calor–modular e rate≠0,

    T_p(v_geom,v_geom)=−L/π.

Assim, um modelo com L>0 não pode satisfazer essa identificação com matéria de contração nula não negativa. O caso L<0 remove essa incompatibilidade de sinal; não prova a identificação completa nem a origem física do coeficiente.

## Limites e custódia

Permanecem OPEN a dinâmica canônica selecionada pelo acervo, região–álgebra, origem e coerência de estados no limite, correspondência de parâmetros, erros de identificação, calor físico, tensor T, área integrada de horizonte, assinatura/dimensão sem entrada, origem modular da solda e globalização.

Todos os arquivos novos e revisões somente em Chatgpt. Originais, entregas anteriores, kernel canônico, Atlas, memórias, selos e gate intocados. Sem execução/importação de um.py. Backup de bytes e temporário verificado em cada revisão. Auditoria independente reservada à gerência.

## Adendo de controle, antes de sua implementação

Verificar habitabilidade do novo contrato em um controle de vácuo plano: eixo diagonal a=1,b=0, frequência 1, amplitudes u=3/5 e v=4/5. A marginal permanece constante, o coeficiente modular é zero, e os coeficientes geométricos de calor e área de 020 são zero. Esse controle deve satisfazer os dois erros pequenos sem recebê-los como hipóteses. Ele não demonstra um caso gravitacional com resposta não nula.

Verificar ainda a recusa do controle plano com matéria conservada incompatível já usado em 020/021, agora para qualquer instância de UnitaryScreenMatching.

