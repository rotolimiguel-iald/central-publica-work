# Contrato de admissibilidade Q2 e comparação de fundos

10/09/2026, arco072. [DERIVED — auditoria escrita; KNOWN — importações delimitadas]. Somente arquivos novos em Chatgpt. Zero CAS, zero Lean; nenhum um.py executado/importado ou original alterado.

## 1. Resultado e fontes

A Q2 de069 fornece produtos temporais do sistema auxiliar Einstein–sigma, a quebra BV local e a consistência da primeira ordem não removida. A normalização071 pode fazê-los equivariantes sob O(4) na família que transporta simultaneamente os fundos. Isso não fornece uma primitiva admissível da quebra nem uma Ward de independência da cisão fundo–flutuação.

A presente frente constrói uma Ward anômala estendida em referência fixa e um controle explícito do transporte do CCR, na [demonstração associada](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>). A referência ainda permanece nos coeficientes; não se conclui a QME.

Fontes locais lidas e medidas antes/depois:

- [Q2 causal069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>), §§1–7.
- [Dicionário BV069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>).
- [Normalização O(4)071](<C:/IALD/Central de Patentes/Chatgpt/NORMALIZACAO_O4_CAUSAL_071_20260910_000602_682931/PROVA_NORMALIZACAO_O4_E_ANOMALIA.md>), §§3–8.
- [Retração relativa072](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>), sobretudo §§5–7. Sua CME estendida é entrada clássica.

Os pins estão no manifesto. Não se recaptura aqui o canônico, nem se atribui aprovação externa.

## 2. Campos e fundos efetivamente construídos

| Item | Contrato efetivo |
|---|---|
| Domínio | M=(0,π)×S³, ḡ=dr²−4cos²(r/2)γ, φ̄=id; suportes compactos interiores. Os extremos temporais não pertencem a M. |
| Propagação bosônica | Dez componentes métricas h e três componentes de ξ∈Γ(φ̄*TS³). O operador acoplado normaliza-se a onda; a forma de fibra da Hessiana é conservada nos Green. |
| Ghosts e auxiliar | c, c̄ e b de posto quatro. O auxiliar mantém os contatos do dicionário. O ghost é difeomórfico; O(4) rígido não virou gauge local. |
| Realidade/BV | c̄*=−c̄ e s₀c̄=−b. Antifields externos não têm contrações, mas suas inserções participam das identidades BV e dos contatos. |
| Expansão | g=ḡ+t h e φ=Exp_φ̄(tξ), t formal distinto do tempo r. Trata-se do fibrado global pullback, sem uma carta escalar que omita parte da imagem de φ̄. |
| Ação inicial | t⁻² vezes a ação expandida, retirada a constante. O termo linear some porque o fundo físico é on-shell. Isso não autoriza apagar tadpoles sob variações arbitrárias de fundo. |
| EFT | São permitidos novos operadores locais a cada ordem/truncagem. Contratermos de laço podem ter zero, uma ou duas pernas. |
| Covariância | Embeddings transportam todos os dados de fundo. O(4) transporta também φ̄; em um centro formal fixo, só seu estabilizador age dessa maneira sem comparação adicional. |
| Estado | Hadamard realiza a álgebra; a escolha global de modos não se torna coeficiente local de contratermo. O limite adiabático é algébrico, não de estados. |

[KNOWN] A importação de Hollands usada por069 é a construção tensorial/Grassmann de §3.5 e a liberdade/recíproca do Teorema2. T4 controla variações suaves da métrica; T5 trata famílias analíticas de métricas analíticas; T11 é Leibniz/ação por partes. T11 não é uma Ward de mudança de fundo. A remoção de anomalias Yang–Mills não é importada para Einstein–sigma. [Fonte primária, 0705.3340v4](https://arxiv.org/pdf/0705.3340v4).

## 3. A primitiva precisa pertencer à classe de normalização

Na primeira aridade em que duas prescrições diferem, com ordens inferiores iguais, a diferença local tem representação

\[
D_n=\sum_{|\alpha|\leq N}C_\alpha(x)\nabla^\alpha\delta_{\rm Diag},
\qquad N\leq\lfloor{\rm sd}-4(n-1)\rfloor,
\tag{1}
\]

se a cota for não negativa. Os coeficientes têm tipos tensorais/grades das inserções e jatos finitos dos dados admitidos. A escrita em um ponto é local, não uma coordenada global.

Para que uma primitiva corrija Q2, são necessários simultaneamente:

1. Localidade e suporte na diagonal para a aplicação multilinear inteira, com compatibilidade entre aridades/inserções.
2. Ghost, paridade, realidade graduada, tipos tensorais e covariância na categoria de todos os fundos transportados.
3. Ordem de jatos finita por coeficiente e a cota de escala da ordem perturbativa, incluindo curvaturas, acoplamentos, ghosts e fontes. Ordem local finita, sozinha, não satisfaz uma cota fixada.
4. Regularidade suave/analítica efetivamente imposta, globalidade no alvo, independência funcional dos campos e ação por partes.
5. Normalização das inserções lineares, EOM e contatos; ao exigir uma Ward de fundo, também a hierarquia de inserções marcadas.

Assim a_N=sB+dC em uma álgebra maior não paga uma família de contratermos com essas propriedades. Também não se deve exigir arbitrariamente que B seja uma densidade antifield-free natural do campo completo: uma densidade integralmente covariante desse tipo já é s-fechada modulo d e, em geral, não cancela uma quebra não nula. A classe deve conter a estrutura BV necessária.

## 4. Suave e analítico são contratos diferentes

Q2_069 declara coeficientes suaves nos fundos e usa a expansão geométrica de escala; O4_071 conserva a classe geométrica adotada e a suavidade global do alvo. Nenhuma nota enuncia analiticidade conjunta em toda família possível do mapa de fundo, nem prova que toda primitiva suave071 satisfaça essa versão forte.

Uma aplicação pode escolher a classe forte, com dependência analítica conjunta nos dados analíticos. Então também a primitiva e sua construção devem preservar essa propriedade. Exp da esfera redonda é analítica perto da seção zero; não torna analítico um coeficiente C∞ inicial. Pode-se, alternativamente, escolher regularidade suave microlocal apropriada, mas deve-se apresentar o teorema de normalização para os produtos/identidades do multiplet efetivo; não basta trocar o adjetivo de T5.

Controle elementar: f(z)=exp(−1/z²) para z>0 e f(z)=0 para z≤0 é suave; na família analítica z(u)=u, a composição não é analítica em zero. Uma homotopia em C∞ não paga automaticamente a alternativa forte.

[KNOWN] Khavkine–Melati–Moretti classificam renormalizações suaves de potências de Wick para fibrados vetoriais naturais com campos de fundo. Isso oferece uma rota para especificar a liberdade suave, mas não é, por si, o teorema de todos os produtos temporais BV interagentes do Einstein–sigma. [Fonte primária, 1710.01937](https://arxiv.org/pdf/1710.01937).

A média O(4)071 age na fibra afim das extensões de uma aridade, com ordens inferiores já invariantes. Conserva as cotas comuns e as identidades daquele espaço. Não converte uma primitiva não admissível em admissível, nem identifica invariância diagonal com dependência só dos campos completos.

## 5. Escala, pernas e contatos

A contagem069 é

\[
\delta=2+2L+\sum_v(d_v-2),\qquad
\sum_v(v-2)=E+2L-2.
\tag{2}
\]

Na segunda fórmula v é valência e E conta pernas externas; d_v é ordem diferencial. As igualdades controlam graus a laços/pernas/truncagem especificados; não proíbem novos invariantes nem dizem que todo coeficiente permitido é não nulo.

As dimensões devem acompanhar a normalização efetiva dos campos. Na apresentação geométrica, g e φ podem ter dimensão zero, ∂ dimensão um, κ dimensão −2 e c_sigma,Λ dimensão dois. Reescalar campos canonicamente altera sua atribuição; o peso dos ghosts e de Ω acompanha o de s. Não se misturam apresentações para fabricar uma cota. A retração072 controla peso relativo de u,v e ordem por coeficiente; ainda se confere (1).

P_gr G_gr^F=Id contém os contatos. Aplicar EOM a produtos temporais pode gerar delta e suas derivadas. Ação por partes não os elimina. Uma igualdade modulo d multiplicada por cutoff f tem também termo df; a Ward sem esses termos vale somente onde os cutoffs relevantes são constantes. Ω e a variação da parte quadrática exigem o mesmo cuidado.

A extensão com fontes da nota associada admite tadpoles t⁻¹θ. Ela é organizada em multigrau: a grau externo k fixo há no máximo k desses vértices. As séries normalizadas são Laurent em t com parte negativa finita nessa graduação, não automaticamente séries só com potências não negativas. Vértices quadráticos de mudança têm grau externo positivo. O controle completo está na seção7 daquela nota.

## 6. A obrigação adicional de comparar fundos

[KNOWN] Fröb, Teorema3, exige uma derivação verdadeira da álgebra livre, local/covariante e preservando o suporte das inserções. Teoremas6–7 identificam o termo clássico BV e a consistência. Diferenciar um kernel não fornece automaticamente essa hipótese. [Fonte primária, 1803.10235v3](https://arxiv.org/pdf/1803.10235).

A nota associada prova a falha já no CCR. Derivadas do propagador conectam pontos separados; antes do transporte, esse defeito não é simplesmente uma anomalia diagonal à qual se aplique uma homotopia de densidades.

[KNOWN] Taslimi Tehrani–Zahn usam acordo perturbativo, equação76, e a condição adicional de gauge A_int,1(δ̄_aΨ)=0, equação95/Teoremas3.13–3.15. Sua seção4 deixa aberta a ocorrência de obstruções correspondentes em gravidade, pois o argumento de renormalizabilidade usado em Yang–Mills não se transfere. Não se fecha Einstein–sigma mudando nomes. [Fonte primária, 1804.07640v3](https://arxiv.org/pdf/1804.07640).

[KNOWN] O resultado de Drago–Hack–Pinamonti começa com perturbações quadráticas escalares sem derivadas. Não é usado aqui como prova do multiplet com símbolo principal variável e ghosts. [Fonte primária, 1502.02705](https://arxiv.org/pdf/1502.02705).

Há ainda a diferença de domínio: Q2_069 usa um fundo on-shell; pares B,Ω livres admitem variações arbitrárias. Exigir que Ω satisfaça a equação tangente do fundo desfaz a hipótese de doublet livre. A construção nova conserva o operador livre em B0 on-shell e todos os termos de diferença, inclusive lineares/quadráticos, como inserções formais. Não pressupõe uma CME quadrática off-shell.

## 7. Fronteira após esta entrega

[DERIVED] Estão construídos o defeito de Leibniz, sua parte antissimétrica no CCR, o reparo retardado de primeira ordem e a Ward anômala estendida com fontes centrais em referência fixa. O setor de inserções exclui os conjugados de fundo, conforme a demonstração.

[OPEN] Ainda faltam a normalização de acordo perturbativo com inserções/contatos para comparar os T_B e o transporte compatível requerido. Mesmo na referência fixa, a retração B→campos completos preserva B0 nos coeficientes: é necessária uma primitiva admissível nessa categoria ou um levantamento natural que elimine a referência. H¹,⁴ sem esses espectadores não é automaticamente consumido.

[OPEN] Permanecem a remoção causal da quebra em todas as ordens, o quociente/estado físico interagente e as obrigações globais/UV. O defeito calculado não prova anomalia física não removível.
