# Aplicação da descida075: jatos dinâmicos livres e domínio da referência

10/09/2026. [DERIVED — auditoria e composição escrita] [KNOWN — contrato primário identificado]. O antecedente off-shell da descida é fornecido para os campos, ghosts e antifields dinâmicos da Q2, antes de qualquer quociente por suas equações. A referência B0 continua restrita ao domínio em que a construção causal existe. Demonstramos abaixo por que essa restrição apenas nos coeficientes não impede a descida em jatos livres de ghost não zero.

A conclusão é uma aplicação da descida natural no esquema de referência real das notas, com os antecedentes causais e de classe já explicitados. Não é uma identidade da anomalia em todos os jatos livres de B0, uma remoção da classe total ou uma QME. Nenhum original, um.py, Lean ou CAS foi executado ou alterado.

## 1. Fonte primária e distinção dos espaços

[KNOWN] Consultei diretamente o [PDF primário de Fröb, 1803.10235v3](https://arxiv.org/pdf/1803.10235v3). Referências verificadas: §2, pp.4–7, eqs.6,19,24; Teorema3, pp.17–19, eqs.70–76; §4, p.32, eqs.137–139; Teorema6, p.34; eq.154 e Teorema7, pp.36–37.

A₀ é definido antes do ideal I₀ das equações livres. A passagem a A₀/I₀ é posterior. Os mapas de anomalia têm domínio e contradomínio no espaço F de funcionais locais polinomiais; não no quociente por EOM. Antifields são centrais e não propagantes, mas permanecem argumentos. O Teorema7 dá consistência nesse espaço e usa a fidelidade da inserção temporal off-shell. O fundo que define a ação livre é uma entrada separada; não é tornado arbitrário por essa propriedade.

Essa é a importação primária usada aqui. O HTML disponível estava incompleto depois do início da seção2; a conferência dos teoremas foi feita no PDF. Não se atribui a Fröb uma aplicação já demonstrada ao nosso fundo ou uma classe de contratermos mais ampla que a das notas.

## 2. Rastreio local: o que foi e o que não foi quocientado

| Etapa | Espaço efetivamente usado | Relações que não foram impostas |
|---|---|---|
| [Q2_069, linha107](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md:107>) | Inserções locais de flutuações, ghosts e antifields; imagem na álgebra auxiliar livre off-shell. | Nenhuma EOM dinâmica, nenhum valor particular de ghost ou antifield. |
| [Q2_069, linha52](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md:52>) | Antifields entram polinomialmente como fontes externas e seus jatos. | Ausência de propagador não significa antifield zero ou jatos fixados. |
| [Ward072, linha120](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:120>) | Um esquema T₀ e seus kernels na referência B0 on-shell. | A referência não se torna um campo dinâmico sujeito ao mesmo teste de liberdade de Z. |
| [Ward072, linha122](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:122>) | Extensão por jatos formais de θ e ω; θ tem ghost0, ω tem ghost1. | Não se impõe d_Hω=0; seus jatos são fontes livres. |
| [Ward072, linha167](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:167>) | Antibracket dinâmico e coeficientes θ,ω, sem θ*,ω*. | Não se criou um antibracket de inserções contendo conjugados dos fundos. |
| [Ward072, linha237](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:237>) | Consistência da primeira quebra no complexo clássico estendido, modulo divergência. | Não há projeção a soluções dinâmicas ou ao quociente físico. |

A álgebra representada em estados físicos e a construção P0 são posteriores e não são usadas nesta inferência. Um ideal das EOM dinâmicas destruiria justamente a liberdade de variação de Z exigida pela prova075. A fonte causal examinada não realiza essa passagem antes de estabelecer a consistência.

Não se usa uma apresentação com quatro componentes sigma independentes sujeitas depois a uma restrição algébrica. Os campos perturbativos sigma vivem no fibrado tangente de posto três sobre φ0; seus antifields no dual densitizado. Liberdade dos jatos significa liberdade nesses fibrados, não liberdade fictícia de quatro coordenadas ambientes redundantes.

## 3. Da Ward off-shell à consistência local utilizável

[DERIVED — composição das identidades já disponíveis]. Denote por A_N o primeiro coeficiente não removido da anomalia avaliada na interação escolhida. No esquema estendido, escreva
\[
 \mathsf s=s_0+d_\theta+(V_{\rm ext},\,\cdot\,)_{\rm dyn}.
\]
A [Ward072, eqs.14–19](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:171>) conserva a CME completa, inclusive os termos de fonte do gauge, e separa o operador clássico nas inserções da derivação quântica. Em uma região O onde os cutoffs relevantes são constantes, \(\mathcal M(V_{\rm ext})=0\) e \(\mathsf s^2=0\).

A consistência é uma identidade de funcionais locais off-shell. O termo de inserção da CME desaparece em O. A parcela com uma anomalia inserida em outra tem ordem superior à primeira quebra: a anomalia exterior começa ao menos em ħ, e a interior começa em ħ^N. Basta a cota N+1; não se exige que todas as anomalias polarizadas inferiores tenham desaparecido para afirmar artificialmente a cota 2N. Resulta
\[
 \mathsf s A_N=0
 \quad\text{como funcional local em O, sem EOM dinâmicas.}
 \tag{1}
\]
A formulação ordinária em densidades é \(\mathsf s a_4^1+d_H\beta_3^2=0\), com os termos de cutoff mantidos fora de O. A nota069 já registra essa relação na [linha118](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md:118>); a extensão072 a registra na eq.19.

Uma passagem segura ao primeiro descendente evita escolher inicialmente uma corrente coordenada: tome \(F_4^2=\mathsf s a_4^1\). Variações arbitrárias dos geradores Z, com suporte compacto interior em O, aplicadas a (1), dão
\[
 \mathcal E_Z(F_4^2)=0 .
 \tag{2}
\]
É uma conclusão em jatos livres de Z. Em campos ímpares, polarize com parâmetros independentes e faça a variação par; a comparação é coeficiente a coeficiente na álgebra de Grassmann. Não se avalia um estado ou uma trajetória para deduzir (2).

O [adendo do primeiro descendente075](<C:/IALD/Central de Patentes/Chatgpt/DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md>) usa exatamente (2). Sua integração por partes covariante fornece, para cada grau Euler N_Z>0,
\[
 F_{N_Z}=d_H\bigl(\Theta_{F_{N_Z}}[Z]/N_Z\bigr).
 \tag{3}
\]
Como F tem ghost2, não existe componente N_Z=0 quando todos os geradores de ghost não zero foram contabilizados. A corrente natural de (3), com o sinal oposto, é o primeiro descendente. A prova q<4 completa então a cadeia. Esta composição não resolve a cohomologia de s; constrói os representantes da descida.

Se a Ward global conserva termos suportados onde o cutoff varia, eles não desaparecem por decreto: a localidade da anomalia os mantém fora das variações suportadas em O. Para retornar a densidades testadas, \(d_H(\chi J)=d\chi\wedge J+\chi d_HJ\) deve ser conservado. A construção local não é uma Ward sem contatos em toda a variedade.

## 4. Por que B0 on-shell não invalida a prova em Z

A frase “off-shell” precisa indicar de quais variáveis se fala. [Ward072, linha120](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:120>) fixa B0 on-shell. [Q2_069, linha56](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md:56>) declara naturalidade conjunta dos dados transportados; isso não transforma a referência em jatos arbitrários sem equações. Não encontrei nessas fontes uma identidade causal já estabelecida para todos os jatos livres de B0 com sua própria parte quadrática fora das soluções.

Há, porém, um resultado suficiente que não precisa dessa ampliação.

**Lema de estabilidade em coeficientes de fundo.** Seja K um anel de coeficientes de ghost zero, com derivadas horizontais, e J um ideal diferencial de K. Trabalhe com jatos livres de Z e, quando necessário, de Y dinâmico sobre K/J. Suponha que as conexões de quantização sejam naturais, independentes de Z e regulares nessa categoria. Os operadores de descida075 e de primeira variação descem ao quociente por J.

**Demonstração.** Linearizar em Z anula os elementos de J e conserva J vezes qualquer expressão. Extrair símbolos, aplicar ∂p e contração, e dividir pelos inteiros positivos r+n−q usam apenas operações lineares e escalares reais invertíveis. Multiplicações por conexões conservam J. A derivada horizontal conserva J por sua hipótese diferencial. A subtração \(P-d_HQ\), a quantização covariante, a integração por partes e a avaliação v=Z conservam, portanto, J. A independência dos jatos de v continua válida sobre K/J: esses jatos pertencem a um módulo livre sobre esse anel. A identidade de Koszul dos símbolos é algébrica sobre esse anel, sem exigir que ele seja um domínio. A indução na ordem do operador permanece finita. ∎

Pode-se tomar J como ideal prolongado das equações universais apenas de B0, ou como o ideal de relações de coeficientes válido na categoria de referências admitida, desde que seja diferencial. O caso de uma referência fixada também pode ser lido diretamente em coeficientes suaves dessa referência. O resultado continua off-shell nos campos dinâmicos. Ele não permite incluir em J relações diferenciais que atinjam Z.

A naturalidade conserva seu sentido: se a entrada é uma família natural na categoria de referências permitida, todas as operações são equivariantes e fornecem uma família natural nessa mesma categoria. Uma expressão avaliada numericamente em um único conjunto de campos não é promovida a tal família; a entrada local/covariante vem de Q2 e de sua extensão.

Essa passagem não levanta a identidade a todos os jatos livres de B0. Por exemplo, um múltiplo da EOM escalar de B0 por \(\mathrm{div}_{g_0}c\,dV_{g_0}\) desaparece nas referências on-shell e pode não desaparecer em jatos arbitrários. É um controle da não injetividade da restrição, não uma anomalia calculada. Para retirar essa restrição seria preciso uma construção off-shell da família de referência, com sua ação e Ward compatíveis, ou uma prova de levantamento. A descida aqui paga não exige esse passo.

## 5. Fontes centrais de ghost positivo: três rotas tipadas

Na álgebra quântica, “central” descreve os produtos e propagadores; não decide a liberdade horizontal dos argumentos. Os antifields dinâmicos e ω são fontes centrais, mas ambos possuem jatos livres na construção examinada. Uma constante ímpar ζ com d_Hζ=0 seria diferente: poderia ter ghost positivo e grau Euler zero se deixada nos coeficientes. Essa variável não pode ser ignorada para invocar a prova.

As rotas admissíveis são:

1. **Descida na extensão inteira.** Inclua os jatos de ω em Z, juntamente com ghosts e antifields dinâmicos de ghost não zero. θ fica em Y. A [eq.12 da Ward072](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:144>) é uma extensão formal nas fontes; não avalia um perfil especial de ω. As conexões podem ser tomadas nos fibrados fixos de B0. Não é necessário acrescentar θ*,ω* para fazer uma variação horizontal dos argumentos ω. Essa operação não reivindica um novo antibracket quântico para esses conjugados.

2. **Restrição à teoria original da referência.** Avalie θ=ω=0 com todos os jatos, como na [linha243](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:243>). Esse é um mapa de complexos para o diferencial da teoria original, pois d_θ tem fator ω. A consistência original é recuperada e não sobra ghost central positivo de fonte. A avaliação preserva os antifields dinâmicos; não é o quociente por EOM.

3. **Projeção relativa depois de desfazer o gauge.** Use a [retração072, eqs.3.2–4.4](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>) no domínio corrigido por [sua precisão de fontes](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md>). O mapa apropriado é
\[
 p(B)=\Phi,\qquad p(\Omega)=s\Phi,\qquad pD=sp,\qquad pd_H=d_Hp.
\]
Assim \(a'=pC_\Psi^{-1}a_{\rm ref}\) satisfaz consistência relativa no complexo mínimo dos campos completos, mantendo B0 como coeficiente de ghost zero. O parceiro Ω não é posto em zero nessa seção: é substituído por sΦ, expressão nos ghosts dinâmicos. A subálgebra não contém B*,Ω*, e a conjugação utilizada a preserva.

A terceira rota é uma aplicação clássica em jatos formais na vizinhança da diagonal. Sua naturalidade e domínio são os da retração, não de uma avaliação de campos finitos fora dessa vizinhança. Para a pergunta sobre quais geradores entram em Z, ela elimina a ambiguidade. Para uma conclusão em completação causal mais restrita, sua continuidade e a contagem das inserções ainda precisam ser conservadas na aplicação escolhida.

A teoria métrica Q2 não introduziu ghosts constantes de supersimetria ou um ghost de gauge O(4). Parâmetros auxiliares de polarização são auxiliares de extração de coeficientes e não devem ser incorporados como novos coeficientes físicos de ghost positivo.

## 6. Finitude, fontes e o alcance realmente pago

A cada coeficiente de laço, valência e grau externo, a Ward072 fornece expressões de jatos finitos. A linearização e integração por partes são finitas nesse coeficiente. Se Z inclui ω, conte v_ω como uma fonte do mesmo grau externo: a retirada e a reposição preservam esse grau, assim como preservam o grau dos campos dinâmicos quando a variação é dinâmica. Derivar um jato troca sua ordem, não seu número de fatores.

Por isso a descida horizontal não cria uma perda de t: é diferente de b_N=t⁻¹B_N. Na apresentação com conexões fixadas por B0, conserva cada multigrau da entrada. Isso não reclassifica os tadpoles t⁻¹θ da [Ward072, linha184](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:184>) como elementos de R_L. A série Laurent e suas cotas são as já atribuídas àquela extensão; no setor original sem fontes, o controle Rees075 pode ser usado diretamente. A aplicação reiterada de s consome o controle de classe do diferencial pertinente, que permanece visível.

Conservar esses graus não demonstra todos os limites de escala, contatos, independência funcional e relações entre aridades de uma normalização causal. A descida é uma construção de densidades/correntes. Uma primitiva do cociclo total ainda é outro problema.

## 7. Resultado e contrato residual mínimo

[DERIVED, consumindo Q2_069/Ward072] A primeira quebra consistente pode receber uma DESCIDA NATURAL no esquema de referência, antes de impor EOM dinâmicas, com B0 na categoria em que as fontes causais foram construídas. Para a extensão, ω deve entrar nos geradores livres Z ou ser removido por uma das projeções compatíveis descritas. Os conjugados de fundos permanecem fora do domínio. A passagem ao primeiro descendente é fornecida pelo adendo075, e a restrição somente de coeficientes B0 não invalida o seu argumento.

Para aplicar isso a um coeficiente concreto, o contrato verificável é: esquema off-shell auxiliar; primeira ordem não removida e CME local com cutoffs; representante natural local na classe formal escolhida; jatos livres de todos os geradores de ghost não zero usados; conexões independentes desses geradores; filtração adequada às fontes. Não é necessário pedir de novo uma prova de liberdade dos jatos dinâmicos após um quociente que Q2 não fez.

[OPEN] Não foram produzidos coeficientes explícitos da anomalia, sua primitiva total, as nulidades de H(s)/grupos horizontais com coeficientes, a admissibilidade de sua remoção, P2 ou QME. Também não foram identificados os produtos T_B de fundos variáveis com o esquema de referência fixa por acordo perturbativo. O levantamento a jatos totalmente livres de B0 continua distinto da aplicação relativa suficiente acima.

## 8. Custódia

As fontes locais abaixo foram lidas ou consultadas nas seções indicadas e medidas antes/depois. A nota principal de descida075 foi consultada quanto aos enunciados, hipóteses e controle perturbativo; esta contribuição não substitui sua revisão matemática integral. O adendo do primeiro descendente foi lido integralmente. A fonte primária foi conferida pela ferramenta web, sem atribuir-lhe um hash local não medido.

Nenhuma fonte foi modificada. Os controles do manifesto são documentais, não uma execução das provas. Somente esta nota e seu manifesto são novos.


| Fonte local | Bytes | SHA-256 |
|---|---:|---|
| [PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>) | 16140 | 7884a4da5030c5befdad567cff75f4011add1a571a1bb36dee7e9da5a39b6676 |
| [TRANSPORTE_E_WARD_REFERENCIA.md](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>) | 15834 | befb2e2f9060d3e65be4dc09b7744aac3bc195d915390eb784f04026b873bd8e |
| [CONTRATO_ADMISSIBILIDADE_Q2.md](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>) | 11570 | bc995257abcd25925fb50be98878698be90680723238fc07beefe35c874b40ee |
| [RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>) | 12878 | c38ef7de2b20108d8a3dbcc7890936ffd1d8be6d4cd77e52ce4ba98c2221a252 |
| [PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md>) | 2510 | 3506da8bc9d4ca9ca8a2434e7771a77068ffd144c78f488ea60afc24f668917c |
| [DESCIDA_NATURAL_POR_OPERADORES.md](<C:/IALD/Central de Patentes/Chatgpt/DESCIDA_NATURAL_SIMBOLOS_075_20260910/DESCIDA_NATURAL_POR_OPERADORES.md>) | 19357 | 9a4224aaa1cc2cc92cb694a9c4d663cfb8dbb3f17fa7271c64605bbad9140ea8 |
| [ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md](<C:/IALD/Central de Patentes/Chatgpt/DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md>) | 5442 | b5012c189b4176c5cfb056af8f91b9736478a733f550d4980730e36762d14528 |
