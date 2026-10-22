[DERIVED / KNOWN / OPEN] Ordem 006 — demonstração anterior aos novos módulos, 05/09/2026.

## A. Esperança do centralizador

No andar N, a densidade é diagonal d_i=towerW(P,N,i)>0. Defina D_N(a)_ij=a_ij se d_i=d_j, e zero caso contrário: exatamente specExpect d a da casa. Trata-se de pinching pelos autoespaços da densidade, não apenas eliminação de todas as entradas fora da diagonal. Pesos degenerados preservam blocos inteiros.

[DERIVED] D_N(a) comuta com diag(d). O estado ponderado satisfaz φ(D_N(a)b)=φ(bD_N(a)) para todo b. Se a já comuta com diag(d), D_N(a)=a. Para b no centralizador, φ(b†(a−D_N(a)))=0, termo a termo: as entradas de b fora de blocos iguais são zero e as de a−D_N(a) dentro desses blocos são zero. Isso dá os quatro campos no domínio local; positividade/contração seguem da representação como soma de compressões por projeções ortogonais.

Usando a esperança de andar já construída, ω(π_N(a)B)=φ_N(a E_N^mat(B)) e ω(Bπ_N(a))=φ_N(E_N^mat(B)a), para B∈M. Logo um a que comuta com a densidade do andar produz π_N(a) no CENTRALIZADOR GLOBAL de ω. Esse fato elimina uma extensão por densidade neste passo local. Para B∈M_ω, E_N(B) também pertence ao centralizador local, por bimodularidade e preservação de ω. Isso permite provar ortogonalidade do pinching de a contra TODOS os B do centralizador global quando a é local.

[KNOWN/DERIVED analítico, formalização a medir] Para perfil constante p≠1/2, as razões de pesos dos andares são potências de p/(1−p). Com ℓ=log(p/(1−p))≠0 e T=2π/|ℓ|, U_T=1 no domínio local denso e portanto em H. A periodicidade aqui é a do fluxo da representação produto; identificá-la com o grupo T do fator de Powers é uma afirmação adicional de classificação, não necessária à construção.

Para x∈M, E(x) é definido pela integral FRACA de σ_t(x) sobre [0,T], dividida por T. Equivalentemente, integrar t↦σ_t(x)ξ em H para cada ξ: continuidade forte e ‖σ_t(x)ξ‖≤‖x‖‖ξ‖ dão um operador limitado. Não se pressupõe continuidade na norma de B(H) de t↦σ_t(x): isso pode falhar. Somas de Riemann convergem fortemente vetor a vetor; pertencer a M segue do bicomutante, que é fortemente fechado. Cada aplicação normal pode ser integrada fracamente; a normalidade da média deve ser justificada, não deduzida de continuidade WOT-sequencial por mero nome.

A média fica fixa pelo fluxo periódico. A identificação Fix(σ)=M_ω vem de Tomita/KMS ou, nesta torre, do pinching local mais aproximação E_N: E_N comuta com o fluxo, E_N(x)Ω→xΩ, e a contração dos E_N permite estender ao fecho. A construção Lean completa demanda produzir o operador médio e esses lemas de passagem ao limite; um campo assumindo o resultado não conta como habitante.

Em p=1/2, todas as densidades locais são escalares. O estado produto é tracial em M, M_ω=M e E=id. Para um perfil geral, o fluxo pode ser aperiódico, mas NÃO necessariamente: o perfil alternado 1/3,2/3 já tem razões em potências de 2 e período comum. A rota geral é o teorema ergódico médio em H, com passagem da projeção de H ao operador de M ainda a demonstrar. Estacionariedade é suficiente, não necessária, para periodicidade.

## B. Rede e inclusão meio-lateral

[DERIVED] O fluxo manda cada gerador do sítio n em outro gerador do MESMO sítio. Pelo adjoin, σ_t(A(I))⊆A(I); aplicar −t dá igualdade. Como σ_t é conjugação unitária, transporta comutantes e bicomutantes: σ_t(A(I)'')=A(I)''. Vale para qualquer perfil produto, não apenas estacionário. Portanto vale para todos os prefixos e caudas. Se uma construção de shift θ tiver imagem exatamente T₁, essa imagem é invariante; não é preciso fabricar θ para provar o enunciado sobre T₁.

Correção de escopo: a inexistência do shift normal para PERFIS ARBITRÁRIOS não diz que estacionariedade é necessária. Ela fornece uma hipótese suficiente para a identificação natural M(P)→T₁(P); perfis não estacionários equivalentes adequadamente podem permitir extensão. A formulação anterior “exige perfil estacionário” é forte demais.

A definição usual de inclusão meio-lateral usa σ_t(N)⊆N num semieixo, NÃO exige estrita inclusão em cada tempo como parte da condição fraca. Igualdade para todo t satisfaz essa desigualdade. Logo é falso negar a condição fraca só por invariância bilateral. O teorema correto é: igualdade impede compressão ESTRITA; e uma inclusão própria invariante de álgebras com estado normal fiel não pode ter Ω cíclico para N no Hilbert GNS de M. De fato, a esperança preservadora do estado projeta H sobre fecho(NΩ); se NΩ fosse denso, E(x)Ω=xΩ e separância daria E=id, logo N=M. No produto, a falha é explícita: T₁Ω=Ω₀⊗H_tail, subespaço próprio.

Assim, as caudas de sítios não fornecem a inclusão própria com vetor comum cíclico/separante exigida para uma translação de Wiesbrock não trivial. “Standard” pode exigir ainda ciclicidade no comutante relativo; não confundir essa condição extra com a ciclicidade básica para N.

Fontes primárias: [Takesaki 1972](https://www.sciencedirect.com/science/article/pii/0022123672900043); [Araki–Zsidó, extensão do teorema de Borchers](https://arxiv.org/abs/math/0412061); [Correa da Silva–Lechner, Modular Structure and Inclusions of Twisted Araki-Woods Algebras](https://arxiv.org/abs/2212.02298). O negativo pedido será formulado nesse alcance preciso, sem alterar a definição para torná-lo verdadeiro.

Adendo bibliográfico: corrigida a autoria do terceiro artigo após consulta à página primária. A versão anterior à correção permanece em backup byte a byte; esta correção não altera a derivação anterior ao código.

## C. Admissibilidade e sequência de leitura

Esta bancada JÁ leu as seis razões na ordem 005. Não existe cegueira retroativa: qualquer critério proposto agora é pós-conhecimento, mesmo se sua justificativa for independente. Nenhum dado cinemático novo será aberto nesta ordem.

As hipóteses efetivas são realização da borda auto-conjugada, lei radial e normalização do gradiente de potencial. Morfologia, raio, rotação versus dispersão e virialização não as implicam. A condição v_c=βc/√(2π) é a própria normalização M/R sob dinâmica newtoniana; usar velocidades para selecionar objetos que já a satisfazem seleciona o consequente, embora não leia uma coluna chamada massa. Para sistemas suportados por dispersão, a conversão exige Jeans, anisotropia e perfis; não há igualdade universal σ=v_c sem essas hipóteses.

É possível definir um teste cinemático independente para REFUTAR a ponte quando seu regime for válido; não um filtro que transforme a mesma concordância em predição independente de massa. Com o acervo numérico autorizado aqui, há R e M das seis âncoras, mas não perfis, erros, anisotropia ou observáveis de borda capazes de certificar admissibilidade. A classificação correta para as seis é INDETERMINADA, não “aglomerados entram, galácticas saem”. As seis razões podem ser reapresentadas depois dessa classificação, sem usá-las como critério.

Não foi demonstrado que nenhum critério futuro possa existir; foi identificado que as premissas atuais não fornecem um critério observacional independente executável para as seis âncoras. A saída (iii) permanece enunciado condicional sem domínio físico certificado e não autoriza reinstauração como lei de fonte validada. A decisão histórica/editorial é do operador.
