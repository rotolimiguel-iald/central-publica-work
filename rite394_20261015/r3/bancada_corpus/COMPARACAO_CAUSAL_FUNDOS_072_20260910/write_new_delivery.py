from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

BASE = Path("C:/IALD/Central de Patentes/Chatgpt")
OUT = Path(__file__).resolve().parent
SOURCES = [
    BASE / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md",
    BASE / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md",
    BASE / "NORMALIZACAO_O4_CAUSAL_071_20260910_000602_682931/PROVA_NORMALIZACAO_O4_E_ANOMALIA.md",
    BASE / "RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md",
]


def pin(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def write_new(name, content):
    target = OUT / name
    temporary = OUT / (name + ".new_tmp")
    data = content.encode("utf-8")
    if target.exists() or temporary.exists():
        raise RuntimeError("Existing destination: " + str(target))
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != data:
        raise RuntimeError("Temporary verification failed")
    temporary.rename(target)
    if target.read_bytes() != data:
        raise RuntimeError("Final verification failed")
    return pin(target)


CONTRACT = r"""# Contrato de admissibilidade Q2 e comparação de fundos

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
"""


TRANSPORT = r"""# Defeito do CCR, transporte e Ward estendida em referência fixa

10/09/2026, arco072. [DERIVED — demonstrações escritas; KNOWN/INPUT — entradas explícitas]. Somente novos arquivos Chatgpt; zero CAS/Lean e nenhuma execução/importação de um.py.

## 1. Resultado e entradas

Demonstramos a falha da derivação ingênua de kernels variáveis, seu controle no CCR, um reparo simplético de primeira ordem e uma Ward anômala estendida em referência fixa. A última construção mantém B0 nos coeficientes e não prova exatidão/QME.

O contrato está em [Admissibilidade Q2](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>). A ação clássica estendida é entrada da [Retração relativa072, §6](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>). Dicionário e Q2_069 fornecem o diferencial livre nilpotente, os Green, contatos e a Ward anômala original. Nada abaixo modifica essas fontes.

## 2. Convenções

Basta o bloco bosônico para demonstrar a obstrução. Tome P_ε formalmente autoadjunto e Green-hiperbólico, com P₀=P e δP compacto nos coeficientes. Identifique antes os fibrados/densidades em um par dual de referência fixo. Para mapas próximos, pode-se usar transporte paralelo alvo entre pullbacks; os fatores de volume e forma de fibra da Hessiana são também transportados. Não se varia a métrica mantendo uma adjunção incompatível. Multiplicar a Hessiana por uma forma de fibra para normalizar a onda não permite descartá-la nos Green.

Escreva Gʳ,Gᵃ para Green retardado/avançado, (Gʳ)*=Gᵃ e E=Gʳ−Gᵃ. Para funcionais regulares e H−Hᵀ=iE, use

\[
F\star_B G=\mu\exp(\hbar\Gamma_{H_B})(F\otimes G).
\tag{1}
\]

Γ_H contrai uma derivada funcional de cada fator e μ os multiplica. Esta convenção põe i na parte antissimétrica de H. O argumento não depende de chamá-lo iG⁺ ou função de dois pontos.

## 3. Defeito de Leibniz e controle linear

Os operadores Γ com kernels independentes dos campos comutam. Derivar a série (1), mantendo coordenadas funcionais fixas, dá exatamente

\[
\boxed{\delta(F\star_B G)-(\delta F)\star_B G-F\star_B(\delta G)
=\hbar\mu\exp(\hbar\Gamma_{H_B})\Gamma_{\delta H_B}(F\otimes G).}
\tag{2}
\]

Os termos em que δ atua nos próprios funcionais já foram subtraídos. Para F_f(ϕ)=〈f,ϕ〉 e F_g lineares com testes fixos,

\[
[F_f,F_g]_{\star_B}=i\hbar E_B(f,g)\,1.
\tag{3}
\]

Uma derivação que anule F_f,F_g anularia o lado esquerdo. A derivada real do direito é iħδE_B(f,g). Logo, sempre que δE_B≠0, a derivada ingênua não é uma derivação dessa família identificada. Direções de simetria podem ter δE=0; não se afirma o contrário.

Uma troca de ordenação α_w=exp((ħ/2)Γ_w^diag), w=wᵀ, fixa os funcionais lineares e muda só a contração simétrica. Não altera (3), portanto não corrige δE≠0. Isso independe de positividade/cohomologia. O defeito (2) pode conectar pontos separados: antes de reparar a derivação, não é automaticamente uma quebra local diagonal da classe Q2.

### Controle concreto

Considere só como controle hiperbólico P=∂_t²−Δ_S³+m² em ℝ×S³, m>0, δP=χ(t), χ≥0 suave, compacta e não nula. No modo espacial constante,

\[
G^r(t,s)=\theta(t-s)\frac{\sin(m(t-s))}{m}.
\]

Para t>s e suppχ⊂(s,t),

\[
\delta E(t,s)=-\int_s^t
\frac{\sin(m(t-u))}{m}\chi(u)\frac{\sin(m(u-s))}{m}\,du.
\tag{4}
\]

Se 0<t−s<π/m, o resultado é estritamente negativo. Testes suaves próximos desses tempos conservam um pareamento não nulo. É um exemplo quadridimensional de variação do CCR, não um cálculo de anomalia física do Einstein–sigma.

## 4. Reparo por transporte retardado

Diferenciar P_εG_ε^{r/a}=1 e usar a condição de suporte do Green dá

\[
\delta G^{r/a}=-G^{r/a}\delta P G^{r/a}.
\tag{5}
\]

Consequentemente,

\[
\boxed{\delta E=-G^r\delta P G^r+G^a\delta P G^a
                  =-G^r\delta P E-E\delta P G^a.}
\tag{6}
\]

Na segunda igualdade os termos mistos cancelam. Perturbação compacta e suportes causais dão sentido aos produtos sobre testes. A (4) é a restrição da (6) ao modo constante.

Defina

\[
r_\varepsilon=1-\varepsilon G^r\delta P+O(\varepsilon^2).
\tag{7}
\]

Então (P+εδP)r_εu=Pu+O(ε²); soluções antigas vão a soluções novas e coincidem no passado da perturbação. Pela adjunção fixa,

\[
\boxed{r_\varepsilon E r_\varepsilon^*
=E-\varepsilon(G^r\delta P E+E\delta P G^a)+O(\varepsilon^2)
=E_\varepsilon+O(\varepsilon^2).}
\tag{8}
\]

O pullback do novo observável linear é F_f↦F_{r_ε*f}; (8) verifica seu novo CCR. É um certificado simplético infinitesimal, sem afirmar convergência ou transporte físico em todas as ordens.

Coloque A=−GʳδP. Após esse transporte, o defeito do kernel fica

\[
w=\delta H-AH-HA^*
 =\delta H+G^r\delta P H+H\delta P G^a.
\tag{9}
\]

As equações H−Hᵀ=iE e (6) dão w−wᵀ=0. Se os kernels Hadamard forem escolhidos compatíveis com o transporte, a diferença no mesmo operador é suave, e w é uma troca suave e simétrica de Wick. A simetria foi provada algebricamente; a suavidade exige essa comparação Hadamard, não decorre da simetria.

r*f=f−εδP Gᵃf pode ganhar suporte em suppδP∩J⁻(suppf), fora do suporte original. Logo o transporte não é uma derivação local que preserve estritamente o suporte de cada inserção. Não o inserimos diretamente nessa hipótese de um teorema de Ward. Tampouco (8) fixa a extensão de T_n às diagonais.

## 5. O que ainda exige acordo perturbativo

[KNOWN] A equação76 de Taslimi Tehrani–Zahn relaciona a derivada transportada de produtos, a variação das inserções e uma inserção retardada de δS₀, incluindo contatos. Sua conexão física usa também a condição de gauge da equação95; a seção4 deixa uma obrigação específica para gravidade. [Fonte primária, 1804.07640v3](https://arxiv.org/pdf/1804.07640).

[OPEN] Para o multiplet atual, precisam ser normalizados conjuntamente os termos quadráticos, ghosts/não mínimo, antifields, sigma e as inserções marcadas, nas cotas de Q2. Só então se compara a teoria com P_B livre àquela que trata P_B−P_B0 como interação. (8) não prova nem refuta essa normalização: evita saltá-la.

## 6. Construção em uma álgebra de referência fixa

Fixe B0=(ḡ0,φ̄0) on-shell, A0,B0, T0 da Q2_069 e seu diferencial ŝ₀ nilpotente, derivação graduada. Os kernels livres são os de B0.

Adicione fontes externas θ de ghost zero e ω de ghost um/paridade ímpar, com seus jatos. Use B_g=ḡ0+θ_g e B_φ=Exp_φ̄0(θ_φ), θ_φ∈Γ(φ̄0*TS³), formalmente perto da seção zero. Defina

\[
d_\theta\theta=\omega,\quad d_\theta\omega=0,\qquad
D_0=\widehat s_0+d_\theta.
\tag{10}
\]

No mapa original Ω_φ=d_θExp_φ̄0(θ_φ): o diferencial de Exp não é omitido. A apresentação é global no fibrado da referência e formal nas diferenças; o prolongamento aos jatos é evolutivo. θ,ω são centrais no sentido graduado, sem propagadores, e ŝ₀ os anula.

Se R é a álgebra formal dos jatos dessas fontes, A0,B0⊗R possui

\[
D_0^2=0,\qquad
D_0(F\star_0G)=D_0F\star_0G+(-1)^{|F|}F\star_0D_0G.
\tag{11}
\]

H_B0 não depende de θ, portanto não aparece (2). D₀ preserva suporte local das inserções. Trata-se de uma construção em esquema fixo, sem identificar d_θ com a derivada dos kernels de T_B.

### Produtos e identidade exata dos espectadores

Expanda cada inserção em coeficientes a_i(θ,ω,jatos) multiplicando operadores locais originais. Defina distribucionalmente

\[
T_n^{\rm ref}(a_1(x_1)O_1(x_1),\ldots,a_n(x_n)O_n(x_n))
=a_1(x_1)\cdots a_n(x_n)T_{0,n}(O_1(x_1),\ldots,O_n(x_n)),
\tag{12}
\]

com sinais de Koszul. Coeficientes suaves multiplicam distribuições renormalizadas. Quando se muda a representação por ação por partes, as derivadas dos a_i entram por Leibniz; não são tratados como constantes. A definição é compatível porque T0 satisfaz a mesma identidade.

A regra, aplicada a todas as inserções, preserva fatorização, graduação, realidade, suporte/regularidade e cotas quando se contabilizam os pesos externos. Não acrescenta linhas internas ou extensões singulares. A derivação das fontes obedece exatamente

\[
d_\theta T_n^{\rm ref}(F_1,\ldots,F_n)
=\sum_i(-1)^{|F_1|+\cdots+|F_{i-1}|}
T_n^{\rm ref}(F_1,\ldots,d_\theta F_i,\ldots,F_n).
\tag{13}
\]

Logo d_θ sozinho não tem anomalia. Isso não anula a anomalia das interações com inserções Ω.

## 7. Domínio BV, ação e filtração

As inserções contêm campos originais e seus antifields, mais θ,ω, mas são independentes dos conjugados θ*,ω*. ( , )_dyn é o antibracket dos campos originais/antifields, com coeficientes externos espectadores.

Essa restrição é essencial: fontes centrais sem Green não produzem automaticamente, por contrações, o antibracket de inserções arbitrárias com θ*. O mecanismo dinâmico usa EOM e contatos. Inserções dos conjugados de fundo exigiriam um dicionário quântico adicional, fora deste enunciado.

A ação da retração072 tem a forma ⟨θ*,ω⟩+Σ, com Σ independente desses conjugados. A férmion Ψ(fields,B), sem antifields, desloca θ* e acrescenta a Σ o termo de fonte proporcional a ωδ_θΨ. Não muda seu coeficiente ω nem gera dependência não linear em θ*,ω*. Separando novamente ⟨θ*,ω⟩, a CME implica

\[
d_\theta\Sigma+\tfrac12(\Sigma,\Sigma)_{\rm dyn}=0.
\tag{14}
\]

Os sinais são os da conjugação da nota072/dicionário069; o termo de fonte de gauge é conservado.

Escreva os campos completos em coordenadas de flutuação de B0 e separe Σ=Σ0,B0+V_ext. Todas as diferenças de gauge/cinética/fontes ficam em V_ext. A parte livre continua a mesma ação on-shell; termos constantes, lineares e quadráticos que surjam na reorganização não são apagados nem exigem uma CME quadrática off-shell.

Precisão de finitude: sob a organização t⁻², podem existir tadpoles t⁻¹θ (ou termos de grau externo maior). A grau externo total k fixo, contando θ,ω, no máximo k vértices assim podem entrar. Alterações quadráticas têm também grau externo positivo, logo seu número é limitado por k. Os vértices originais não quadráticos têm peso t^(n−2)≥1. Fixar o grau final em t, o grau externo, laços e truncagem limita os vértices positivos depois de contabilizar os negativos.

Assim, após fatorar os termos puramente centrais das matrizes relativas normalizadas, usa-se uma série Laurent em t com parte negativa finita a cada k (os tadpoles contribuem no mínimo −k), ou filtração combinada equivalente. Não se afirmou série só de potências não negativas em t. Termos de zero pernas t⁻², se presentes na reorganização, são centrais; mesmo antes de fatorá-los sua contribuição é finita a grau externo fixo, podendo exigir a cota −2k em vez de −k. A normalização relativa não apaga tadpoles que dependem dos campos.

Como d_θΣ0,B0=0, a equação (14) torna-se

\[
\mathcal M(V_{\rm ext})
:=s_0V_{\rm ext}+d_\theta V_{\rm ext}
 +\tfrac12(V_{\rm ext},V_{\rm ext})_{\rm dyn}=0.
\tag{15}
\]

s₀ é o operador clássico nas inserções, distinto da derivação ŝ₀ na álgebra. A igualdade local testada vale onde os cutoffs são constantes; a identidade completa conserva os termos df.

## 8. Ward anômala estendida e consistência

[KNOWN/INPUT] Usamos a Ward Q2_069, decorrente dos Teoremas3,6,7/equação154 de Fröb, com seu antibracket dinâmico e contatos. Suas hipóteses de derivação/localidade foram preservadas por (11). [Fonte primária, 1803.10235v3](https://arxiv.org/pdf/1803.10235).

A demonstração da extensão é direta: aplique a Ward original coeficiente a coeficiente aos funcionais de (12) e some (13). Para F par, ghost zero, compacto,

\[
\boxed{
D_0T^{\rm ref}(e_\otimes^{iF/\hbar})
=\frac{i}{\hbar}T^{\rm ref}
\left([\mathcal M(F)+\mathcal A^{\rm ref}(e_\otimes^F)]
       \otimes e_\otimes^{iF/\hbar}\right).}
\tag{16}
\]

A_ref é a extensão dos mapas locais originais aos coeficientes externos, incluindo suas derivadas quando aparecem nesses mapas. Não é declarada zero. d_θF vem de (13), sem pressupor Ward dos kernels variáveis. Diferenciar (16) em parâmetros de inserções dá as identidades polarizadas, com sinais graduados; não se provou apenas um vértice isolado.

A_ref começa em ħ, tem ghost um e jatos finitos por coeficiente na categoria de referência. Sua localidade também resulta da recorrência: D₀ é derivação, portanto o defeito na aridade nova cancela nos abertos de fatorização causal depois de subtrair as ordens inferiores; resta diagonal total. É precisamente a etapa que (2) impediria no procedimento ingênuo.

Com F=V_ext e cutoffs constantes, M=0. Está assim construído

\[
a_{\rm ext}^{\rm ref}=\mathcal A^{\rm ref}(e_\otimes^{V_{\rm ext}}).
\tag{17}
\]

Ele pode conter fontes Ω pelas inserções de V_ext, embora d_θ sozinho não tenha anomalia. A construção não pressupõe sua primitiva.

Defina nas inserções o diferencial clássico completo

\[
s_{\rm ext}^{\rm cl}=s_0+d_\theta+(V_{\rm ext},\cdot)_{\rm dyn}.
\tag{18}
\]

Leibniz graduada do antibracket e Jacobi dão (s_ext^cl)²=(M(V_ext),·)_dyn=0 na região de (15). Aplicar D₀ novamente a (16) dá a identidade de consistência original com d_θ sobre os coeficientes: (13) prolonga por Leibniz cada operação de inserção, os termos clássicos se juntam em M, e os demais são inserções de anomalia em anomalia.

Se as ordens inferiores foram removidas nesse esquema e a primeira quebra é ħ^N a_N^ref, os termos com duas anomalias começam em ordem superior. Portanto

\[
\boxed{s_{\rm ext}^{\rm cl}a_N^{\rm ref}+d_H b_N^{\rm ref}=0.}
\tag{19}
\]

Não se infere exatidão de (19), nem se transfere a conclusão à derivada ingênua de kernels variáveis.

Na avaliação θ=ω=0, incluindo jatos, T_ref reduz a T0 e a ação à da referência; d_θ tem fator ω e some. A (16) recupera a Ward original em B0. Esse é o levantamento efetivamente demonstrado: fontes formais na mesma álgebra. Não se identificaram todos os T_B de outra família independente.

## 9. B0 continua presente após a retração

A retração072 põe B=campos completos e Ω=s(campos completos), depois de desfazer o gauge por conjugação, e fornece a fórmula de transporte de primitivas quando elas existem na classe correta. Ela age nos doublets adicionados.

Ela não age na referência B0 dos kernels/normalização T0. Coeficientes locais de a_ext^ref podem conservar curvaturas de ḡ0, jatos de φ̄0 e os tensores permitidos nessa referência. A projeção gera, portanto, um cociclo no complexo com esses espectadores; H¹,⁴ de uma classe apenas dos campos completos não se aplica por identificação nominal.

[OPEN] É necessária uma primitiva admissível na categoria com B0 ou uma prova de levantamento natural/independência que remova a referência. Para comparar diretamente diferentes T_B, também continua necessário o acordo perturbativo com contatos e compatibilidade de gauge. O(4) diagonal transporta B0; não elimina sua dependência.

## 10. Estatuto

[DERIVED] As equações (2), (6), (8)–(13) e (16)–(19) dão o defeito, o reparo do CCR e a Ward anômala em referência fixa. A (14) consome a CME clássica072 no domínio explicitado. Entradas analíticas Q2 permanecem importações delimitadas.

[OPEN] Não foram demonstrados acordo perturbativo completo do multiplet, remoção admissível da anomalia, QME causal, independência física completa de fundo, estado interagente positivo ou fechamento UV. A falha da derivação ingênua é um controle de uma tentativa específica, não prova de anomalia não removível.
"""


def main():
    before = [pin(p) for p in SOURCES]
    artifacts = [
        write_new("CONTRATO_ADMISSIBILIDADE_Q2.md", CONTRACT),
        write_new("TRANSPORTE_E_WARD_REFERENCIA.md", TRANSPORT),
    ]
    after = [pin(p) for p in SOURCES]
    if before != after:
        raise RuntimeError("Sources changed; notes preserved, no clean manifest")
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "072: written Q2 admissibility audit, CCR transport and fixed-reference extended anomalous Ward",
        "status": "DERIVED_WRITTEN_WITH_EXPLICIT_INPUTS_AND_OPEN_CONTRACTS",
        "source_pins_before": before,
        "source_pins_after": after,
        "sources_unchanged": True,
        "artifacts": artifacts,
        "writer": pin(Path(__file__).resolve()),
        "primary_sources": [
            {"url": "https://arxiv.org/pdf/0705.3340v4", "sections": "3.5, T4/T5/T11, Theorem 2"},
            {"url": "https://arxiv.org/pdf/1803.10235", "version_read": "v3, 24 September 2019",
             "sections": "Theorems 3/6/7, equation154, locality and external antifields"},
            {"url": "https://arxiv.org/pdf/1804.07640", "version_read": "v3, 7 February 2020",
             "sections": "equations76/95, Theorems3.13/3.15, section4"},
            {"url": "https://arxiv.org/pdf/1710.01937", "scope": "smooth Wick powers; not full interacting BV Ward"},
            {"url": "https://arxiv.org/pdf/1502.02705", "scope": "quadratic scalar perturbative agreement, initially without derivatives"},
        ],
        "constructed": [
            "explicit Leibniz defect and linear CCR obstruction",
            "first-order retarded symplectic repair",
            "central spectator differential and exact coefficient Ward",
            "local extended anomaly and first-nonremoved-order consistency in a fixed reference category",
            "finite Laurent filtration with tadpoles at fixed external degree",
        ],
        "restrictions": [
            "no background-conjugate antifields in insertions",
            "reference B0 survives the relative doublet retraction",
            "no tadpole discarded by an off-shell free-CME assumption",
            "Hadamard smooth comparison is an extra hypothesis beyond symmetry of equation9",
        ],
        "open": [
            "all-order coupled perturbative agreement with marked insertions and contacts",
            "admissible primitive or natural lifting in the actual reference-background category",
            "causal QME, interacting physical quotient/state, global and UV questions",
        ],
        "new_lean_runs": 0,
        "new_cas_checks": 0,
        "um_py_executed_or_imported": False,
        "existing_files_modified": False,
        "external_approval_attributed": False,
    }
    result = write_new("MANIFESTO_COMPARACAO_072.json",
                       json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"folder": OUT.as_posix(), "artifacts": artifacts,
                      "manifest": result, "sources_unchanged": True}, ensure_ascii=True))


if __name__ == "__main__":
    main()
