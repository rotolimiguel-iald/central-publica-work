# Continuação039 — cone local, assinatura e filtro global

[REAL — 50 teoremas e 9 definições compilados e auditados; interpretação física condicionada] 06/09/2026. Esta etapa atende ao programa espontâneo da ordem008 e investiga a folha ASSINATURA da ordem007. A árvore canônica foi relida como v325. A emergência gravitacional geral, a origem física de seus dados, H3 e globalização permanecem OPEN.

## O que a condição sobre o cone permite concluir

Em um bloco local M2, escrevemos X(t,x,y,z)=[[t+z,x-iy],[x+iy,t-z]]. As coordenadas descrevem todas as matrizes hermitianas complexas2x2, com inversa explícita. O determinante é t²-x²-y²-z². [KNOWN] Esta representação é conhecida: John Baez, [“Connection to special relativity”](https://math.ucr.edu/home/baez/diary/may_2024.html). A tarefa aqui é ligá-la, com tipos e hipóteses explícitos, aos objetos da torre existente.

Considere uma forma quadrática REAL q de dez coeficientes sobre essas quatro coordenadas. A hipótese é:
[INPUT] q(A)=0 para toda matriz local A positiva semidefinida e singular.
[INPUT] q(I)>0.

A dedução seleciona q(X)=a detX, com a=q(I)>0. Assim a expressão tem um sinal temporal positivo e três sinais espaciais negativos, salvo uma escala positiva. A condição q(I)=1 fixaria a escala em1, mas não é assumida.

A prova usa nove produtos externos vv*: seis direções axiais e três direções mistas, exatamente as da derivação prévia. Esses produtos são positivos e têm determinante zero. O vetor zero é permitido; o nome rankOneMatrix significa aqui o produto externo de posto no máximo um. Não se usa posto um como operador em Hilbert infinito. O arquivo antigo GeneralNullCone fornece apenas symmetricForm4, sua expressão irrestrita de dez coeficientes. O cone de Minkowski não é tomado como hipótese importada para obter a conclusão.

A hipótese de anulação NÃO decorre de positividade. O controle é a leitura Re Tr(A²), que em coordenadas hermitianas vale2(t²+x²+y²+z²), é positiva em I e vale1 na projeção diag(1,0). Portanto ela não satisfaz a hipótese de anulação nos positivos singulares.

A dedução é sobre uma forma quadrática, não sobre qualquer função homogênea de grau dois. Tampouco foi formalizada nesta etapa uma classificação de todos os raios extremos ou uma equivalência integral entre o cone PSD e o cone futuro.

## A redução efetiva do filtro global

P é thirdThermalReference; Q é amplitudeProfile b t; R é o likelihoodFilter global da030. O filtro local r0 é relativeFilter dos pesos de P e Q no sítio0. O resultado compilado é uma igualdade de OPERADORES para qualquer matriz complexa local X, sem exigir que X seja hermitiana:

E0^P(R pi0(X) R)=pi0(r0 X r0).

A construção passa por cortes finitos: weightedStepSlice(a tensor c)=omega_site(c) a; cada filtro adicional tem leitura omega_site(r_site²)=1. O traço parcial elimina o fator acrescentado em cada passo. A composição das esperanças fornece a indução até E0. Por fim, a convergência dos filtros prefixais em norma e a continuidade de expectationCLM dão a igualdade para R global.

Isso não assume um filtro de cauda global. Não troca uma igualdade de expectativas escalares por igualdade de operadores. A extração via expectationMatrix e a compressão por levelProject são consequências tipadas da mesma redução. A compressão GNS local atua no Hilbert de matrizes do bloco, de dimensão complexa quatro; não confundir com o espaço espinorial complexo2 usado nas matrizes da representação hermitiana.

## O filtro positivo e a fase têm ações distintas

Para p,q estritamente entre0 e1, os logaritmos locais existentes são ell0=log q-log p e ell1=log(1-q)-log(1-p). A matriz diagonal desses logaritmos é literalmente matrixLogRatio(siteW p)(siteW q), e exp(Llocal/2) é o relativeFilter existente.

Definindo chi=(ell0-ell1)/2 e c=exp(-(ell0+ell1)/4), temos
Rhat=c r0=diag(exp(chi/2),exp(-chi/2)).

Sua congruência X↦Rhat X Rhat* preserva o determinante para toda matriz X. Nas coordenadas hermitianas, ela transforma
t'=cosh(chi)t+sinh(chi)z,
z'=sinh(chi)t+cosh(chi)z,
x'=x, y'=y.

Já a fase U_theta=exp(i theta Llocal) preserva I e produz uma rotação no plano(x,y), com ângulo -theta(ell0-ell1)=-2theta chi na convenção X01=x-iy. Ambas usam o mesmo logaritmo, mas são ações diferentes.

A congruência positiva leva I a diag(exp chi,exp(-chi)), que difere de I quando chi não é zero. Portanto não é um automorfismo modular. Nenhum entrelaçamento unitário finito com um boost hiperbólico foi obtido ou afirmado.

A escala c não é gratuita na preparação de estados. O filtro r0 tem omega_p(r0²)=1; em geral omega_p(Rhat²)=c², diferente de1. Esta última avaliação é uma consequência analítica e sua distinção deve ser preservada ao interpretar o resultado.

A composição escrita no último módulo mantém c² visível:
c² E0^P(R pi0(X) R)=pi0(Rhat X Rhat*).
Para X hermitiano, o lado direito é o operador representado pela matriz transformada pelo boost acima. Não se afirma que o R global preserve o sítio0 por conjugação sem a esperança, nem que a esperança seja multiplicativa.

## Onde a reconstrução física ainda exige dados

[REAL — fonte existente consultada] siteOperator_injective torna a representação do M2 local fiel. Isso impede que a ligação ao bloco seja apenas um nome.

[DERIVED] Uma projeção mínima nesse M2 não é um raio extremo do cone global. Para as projeções em sítios diferentes, e0=e0e1+e0(I-e1); os dois termos são positivos não nulos e não proporcionais na representação-produto fiel. A extremalidade local não se transporta automaticamente para o fator inteiro.

[INPUT/OPEN] Permanecem: a escolha física do bloco, a razão para tratar os positivos singulares locais como direções nulas físicas, a identificação das quatro coordenadas com um espaço tangente, a solda e sua conexão, uma escala dimensional e a dinâmica que produz H3. Dimensão real4 em Herm2 decorre da escolha M2, não de omega(I)=1 isoladamente. Não se deduziram área física, curvatura geral, graviton ou lei de estabilização.

[OPEN] A ordem007C literal permanece não paga por esta etapa. A obstrução anterior ao entrelaçamento finito continua válida. O novo resultado constrói e controla outra ação, explicitando a representação e a redução; não renomeia essa ação como Delta^(it).

## Verificação e custódia

[REAL] Compilação serial concluída com exit0 no diretório CONTINUACAO039_CLEAN_20260906_185519_436442: quatro módulos, seguidos de Imports039All. A auditoria inspect_build() também terminou com exit0 e PASS; conferiu 2002 arquivos do build e 131 registros de evidência histórica, com possível sobreposição entre essas listas.

| Módulo | Teoremas | Definições | Impressões de axiomas |
|---|---:|---:|---:|
| HermitianLocalCoordinates | 11 | 3 | 14 |
| HermitianConeRigidity | 10 | 2 | 12 |
| LocalFilterLorentzAction | 19 | 3 | 22 |
| GlobalFilterLocalReduction | 10 | 1 | 11 |
| Total | 50 | 9 | 59 |

Nenhuma instância nova; nenhuma instância anônima. As 59 declarações têm cobertura exata por #print axioms. Todos os logs passaram sem erros ou avisos, e suas dependências axiomáticas estão contidas em {propext, Classical.choice, Quot.sound}. Não há sorry, admit, axiom ou native_decide nos fontes novos. A importação conjunta passou sem colisões.

As cinco tentativas anteriores rejeitadas permanecem preservadas, com FAILURE.json, fontes congelados e logs. As correções trataram elaboração, normalização e tipagem das provas; os enunciados finais mantêm os alvos da derivação anterior ao código.

A revisão matemática independente conferiu as coordenadas e a rigidez, bem como os fatores de rapididade, o sinal da rotação e o efeito da normalização. Quem escreveu cada componente não aprovou seu próprio resultado.

O auditor confere os bytes originais e compilados, os binários, logs, metadados, a ordem das compilações e a importação conjunta. Também verifica a igualdade dos conjuntos de entradas declaradas e congeladas, o primeiro caminho de resolução de cada importação local e a estabilidade dos registros antes e depois de cada comando.

O runner escolhe explicitamente fontes e binários dos clean035/036/037 por manifestos, evitando o olean de raiz obsoleto da035. Dependências históricas são pinadas, não recompiladas nesta etapa. A auditoria reconfere as compilações históricas035/036/037 por fontes, binários, logs e metadados. Na base035, as inserções determinísticas de nomes de instância são verificadas explicitamente, sem alegar igualdade falsa com os fontes anteriores. Fontes TGL/TGLExt sem pin histórico servem somente à descoberta de importações; esta rodada não prova sua correspondência com oleans. As dependências externas diretas de Mathlib/pacotes/stdlib são hasheadas; sua transitividade externa completa não foi recompilada nem integralmente hasheada.

A039 não modifica o resultado negativo da038: a norma da diferença de fase, naquela calibração e família, continua divergindo do déficit de área óptica em quarta ordem. A seleção condicional de uma forma de assinatura(1,3) não é uma prova de área, de dobra luminosa ou de estabilização.

Reprodução somente leitura, após a entrega: executar C:\Python314\python.exe -B audit_continuation039.py, com diretório de trabalho C:\IALD\Central de Patentes\Chatgpt. O runner clean_continuation039.py preserva seu marcador final e recusa sobrescrevê-lo; a gerência pode recompilar independentemente os quatro fontes entregues, na ordem da tabela e depois Imports039All, conforme ordem008.

Originais, um.py, kernel canônico, Atlas, memórias e gates permanecem read-only. Todos os arquivos e backups desta etapa ficam em Chatgpt. A entrega ao túnel permite à gerência auditar e decidir incorporação; não afirma que essa incorporação ocorreu.
