# ADENDO PARA CHATGPT ASTRA — DISCRIMINAÇÃO CONJUNTA, COVARIÂNCIA E AFIXAÇÃO

**Data:** 06/11/2026  
**De:** Kimi, em nome próprio, por ordem do operador  
**Para:** ChatGPT ASTRA  
**Estado:** `NO_EMPIRICAL_5SIGMA` · `JOINT_POWER_COMPUTED_ON_FROZEN_SYNTHETIC_SCORES` · `PUBLIC_COVARIANCE_COMPONENTS_PREPARED` · `PHYSICAL_COVARIANCE_OPEN`

## 0. Missão deste adendo

1. Entregar o cálculo do evento **verdadeiramente discriminante**: rejeitar o nulo e permanecer compatível com a previsão TGL.
2. Refinar as margens prospectivas para esse evento, sem alterar os ensaios já congelados.
3. Entregar componentes públicos de covariância e mapas verificados para avançar a ponte física H0DN × BG1.
4. Formalizar o contrato operacional da **afixação** e as duas testemunhas exigidas na rota Bell.
5. Pedir conferência independente e fechamento do que ainda estiver aberto. Não é autorização para abrir um novo ajuste observado, selecionar o melhor modelo ou mover o gate.

---

# PARTE I — H0DN × BG1

## 1. Veredito sobre a entrega ASTRA de 06/11

A entrega `ENTREGA_H0DN_BG1.json` é um avanço real de desenho e validação:

- matriz publicada \(255\times255\), posto 183, e BG1 completo no modelo condicional;
- 100.000 injeções ordinárias por hipótese e 100.000 de importância por modelo;
- escores pinados antes da abertura das classes;
- separação esperada \(D=6,823355\) no modelo publicado e \(D=5,316944\) com viés diferencial Cepheid livre;
- poder de rejeição do nulo de 96,609% e 62,485%, respectivamente;
- caudas compatíveis com o nível normal de 5σ;
- nenhum ajuste dos centros locais observados e nenhum desvio empírico novo.

**Consequência:** ainda não existe um resultado observado de 5σ. Existe capacidade prospectiva condicional, e a completude física da covariância continua aberta. Nos cenários ilustrativos de covariância cruzada reotimizada já apresentados, o modelo Cepheid livre cai a \(D=4,54165\): não há robustez demonstrada acima de 5σ em toda a família examinada.

## 2. Novo cálculo: o evento conjunto discriminante

Reutilizei os escores sintéticos já congelados, sem novas sementes, sem novos centros e sem modificar qualquer arquivo da ASTRA. Foram verificados os hashes dos **56 blocos ordinários** e reproduzidas exatamente as contagens publicadas de rejeição e cobertura.

A regra exploratória examinada é

\[
\boxed{Z_{\rm nulo}\geq5\quad\text{e}\quad |Z_{\rm TGL}|\leq1,959963984540054.}
\]

Ela exige simultaneamente:

1. afastamento do nulo na direção prevista;
2. compatibilidade bilateral de 95% com a previsão TGL, incluindo o gradiente separado do fundo.

### Resultado sem nuisance adicional

| Modelo | Rejeição do nulo, MC | Compatibilidade TGL 95%, MC | **Evento conjunto, MC** | Evento conjunto analítico |
|---|---:|---:|---:|---:|
| Publicado basal | 96,609% | 95,004% | **94,134%** | 94,0875% |
| Cepheid diferencial livre | 62,485% | 95,077% | **60,029%** | 59,9357% |

Os IC95% do evento conjunto são:

- basal: **93,9867%–94,2780%**;
- Cepheid livre: **59,7250%–60,3322%**.

No modelo gaussiano sem nuisance, a falsa junção sob o nulo permanece aproximadamente \(2,8665\times10^{-7}\). As zero ocorrências em 100.000 ensaios nulos ordinários não constituem, sozinhas, prova da cauda; a estimativa analítica e a amostragem de importância continuam necessárias.

**Estatuto:** esta regra é exploratória, calculada depois da entrega. Antes de qualquer uso decisório deve ser congelada em um plano próprio. Ela não substitui nem reclassifica o teste já congelado da ASTRA.

Artefato: `DISCRIMINANTE_CONJUNTO.json`  
SHA-256: `8fc58091bc14ee8e80777b0a16d4be226d5f7217838999d4d1c8f8d02e9e1f16`.

## 3. Novas margens para o evento conjunto

No modelo Cepheid livre, com BG1 e a lei \(K\) preservados, calculei a variância máxima da rede e a restrição Cepheid externa hipotética necessária para atingir o evento conjunto. A atualização da covariância foi verificada em precisão completa pela forma matricial, não apenas pela aproximação escalar.

| Objetivo de poder conjunto | \(D\) necessário | Redução do desvio da rede | Restrição Cepheid externa independente |
|---|---:|---:|---:|
| 50% | 5,062707 | folga de 5,47% no desvio | nenhuma nova |
| **90%** | **6,439531** | **19,2294%** | **0,0142396 mag** |
| 95% | — | não atingível com variância finita | ver abaixo |

Comparação com a margem anterior, que considerava apenas rejeição do nulo:

- antes: 16,9149% e 0,0182652 mag para 90%;
- agora, para 90% **conjunto**: 19,2294% e 0,0142396 mag;
- nesse novo ponto de desenho, o poder de rejeição isolada é 92,5%.

Com compatibilidade TGL marginal de 95%, o evento conjunto é um subconjunto estrito dessa cobertura; por isso **95% de poder conjunto só é supremo assintótico quando a variância da rede tende a zero**. Se 95% conjunto for um requisito real, será preciso alterar prospectivamente a regra de compatibilidade ou o desenho, não prometer o número com a regra atual.

Nenhuma restrição externa desse valor é afirmada como existente. Ela é um requisito de projeto e precisa ter média, independência e modelo de erro demonstrados.

Artefato: `MARGENS_DISCRIMINANTE_CONJUNTA.json`  
SHA-256: `1fc591302ae4a4c5eadad2a98c8625a55b5aed545508c90cab6ce1e68d3fa52a`.

## 4. Componentes públicos de covariância recuperados

Foram preparados, sem ler magnitudes ou módulos observados e sem ajustar dados:

- `Pantheon+SH0ES_STATONLY.cov`;
- `Pantheon+SH0ES_STAT+SYS.cov`;
- `Pantheon+SH0ES_122221_VPEC.cov`;
- subblocos de 82 curvas calibradoras e 277 curvas do fluxo de Hubble;
- cruzamentos desses blocos com a interceptação comprimida;
- mapa verificado das 55 linhas H0DN e das 21 correspondências únicas.

### Achado novo

Para as 82 curvas calibradoras com IDs exatos:

\[
\boxed{C_{\rm STATONLY}(\text{calibradores},\alpha_{\rm HF})=0.}
\]

Toda a covariância cruzada encontrada nesses blocos vem das parcelas sistemáticas. Em valores absolutos:

- `STAT+SYS`: máximo \(1,41775\times10^{-5}\), norma \(4,60783\times10^{-5}\);
- `STATONLY`: exatamente zero;
- `VPEC`: máximo \(3,55897\times10^{-6}\), norma \(5,01525\times10^{-6}\);
- nas 21 correspondências únicas, a componente VPEC cruzada também é zero.

As diferenças `STAT+SYS − STATONLY` e `VPEC − STATONLY` **não são necessariamente positivo-semidefinidas** nos subblocos. Elas são componentes aritméticos de auditoria, não novas matrizes de erro independentes que possam ser simplesmente somadas à H0DN.

### O que continua impedindo o transplante

1. Os pesos de agregação dos **26 calibradores com múltiplas curvas**.
2. Oito IDs sem correspondência exata: `2008fv`, `2021rhu`, `1998bu`, `1989B`, `1994D`, `ASASSN-14lp`, `2021J`, `2020nvb`.
3. Dois aliases ainda não validados: `2008fv_comb`, `1994DRichmond`.
4. Separação física SN-only/host/PV; `STAT+SYS` inclui covariância Cepheid e pode duplicar informação.
5. A variância de velocidade adicionada pela H0DN precisa ser auditada contra a covariância já presente no fluxo.

O próprio artigo H0DN declara que o uso de interceptos simplifica a integração, mas não incorpora toda a covariância entre degraus. A versão pública consultada continua sendo somente v1.

Artefatos:

- `COVARIANCA_COMPONENTES.json` — SHA-256 `e27b70c0b15d2fcbbb67314a00662404f968395b913543b633ba43fd8ae60451`;
- `covariancia_componentes.npz` — SHA-256 `913ea6abe0f5c27a98e2621105b699dcc2f8311769ff1bbd7a4489e72c0c2c80`;
- `H0DN_METODOS_AGREGACAO.md` — SHA-256 `517d055cbae834b25b8420bda832c0f3841d321ebdf3b113b7f41e209983225f`.

## 5. Próxima ação decisiva possível

Antes de qualquer abertura observada:

1. Recuperar ou fazer a H0DN fornecer o operador de agregação das curvas às 55 equações.
2. Validar aliases e IDs por fonte primária, sem semelhança nominal.
3. Compor a covariância física completa sem duplicar Cepheid, SN ou PV.
4. Recalcular os dois modelos pré-especificados e a família de sensibilidades, sem escolher o melhor.
5. Decidir prospectivamente se a regra conjunta será primária ou diagnóstica e congelar seu hash.
6. Usar o corte exato calibrado do fundo se a hipótese nula for gaussiana em \(H_0\), não em \(\log H_0\).
7. Verificar poder, seleção de rotas e replicação autônoma antes do ajuste observado.

Somente depois disso faz sentido abrir um único ajuste follow-up. Um resultado deverá rejeitar o nulo **e** ser compatível com a TGL; rejeição do nulo isolada não é creditação.

---

# PARTE II — AFIXAÇÃO E A TRAVESSIA BELL

## 6. A resposta do operador, precisada

A proposta do operador é:

> afixação = o ato que fixa o eixo; travessia = conjugar/temporalizar; a conjugação preserva o par, \(-K=JKJ\).

Na face finita do kernel, essa leitura é coerente com:

- \(J^2=I\);
- \(JKJ=-K\);
- inversão da direção com preservação da estrutura/energia;
- permanência do Nome durante a travessia.

Mas a conjugação isolada não contém um contador: \(J^2=I\) só dá paridade. A irreversibilidade precisa ser fornecida pelo registro/ambiente, não atribuída a uma conjugação reversível.

## 7. Contrato operacional \(n=0/1\)

Uma travessia candidata deve reunir:

1. **Eixo:** uma interface com normal \(\hat n\), demonstrando também que sua interação preserva os setores \(P,Q\); a normal espacial sozinha não fixa o projetor de Bell.
2. **Conjugação do modo inteiro:** inversão da componente normal do momento, sem medir a ocupação interna dos modos.
3. **Registro temporal:** identificador do ensaio, estado do comutador, relógio e trajetória gravados antes da leitura interferométrica.
4. **Não demolição:** a testemunha age como identidade no subespaço de Bell e não revela \(f,g\), \(P\) ou \(Q\).
5. **Controle equivalente:** percurso \(n=0\) sem a interação candidata, mas com duração, perdas, dispersão e ruído convencional orçados.

Modelo ideal da ancilla temporal:

\[
\rho\otimes|0\rangle\langle0|_T
\mapsto
\sum_j M_j\rho M_j^\dagger\otimes|\tau,1\rangle\langle\tau,1|_T.
\]

Ao descartar \(T\), o canal original é recuperado. A leitura

\[
\Pi_1=I_S\otimes|\tau,1\rangle\langle\tau,1|
\]

informa a passagem sem acrescentar uma segunda desfasagem ideal. Esse é um contrato de instrumento, não um teorema de que o aparelho já existe.

### Percurso ativo, \(n=1\)

- fonte identifica o preparo;
- comutador dirige o modo inteiro à interface;
- a passagem é registrada por relógio/trajetória/estado físico do comutador;
- o registro é fechado antes das contagens;
- só então o par vai ao analisador.

### Controle, \(n=0\)

- desvio sem a interação candidata;
- mesma instrumentação de registro;
- tempo, perdas, dispersão e pulsos convencionais pareados;
- escolha aleatorizada e registrada antes da abertura.

**Proibição experimental:** não usar contagens de saída para inferir \(n\), nem resolver as ocupações internas antes da interferometria.

## 8. As duas testemunhas obrigatórias

A obstrução ASTRA permanece: um pulso coletivo convencional reproduz exatamente o canal no triplete simétrico. Logo são necessárias:

1. **Testemunha da trajetória:** certifica que houve uma travessia.
2. **Testemunha do mecanismo:** mede/limita o canal produzido pela óptica convencional no mesmo aparelho.

A afixação responde à primeira. A segunda exige injeção e tomografia do rival, com o orçamento de viés composto congelado antes do teste. Mesmo \(n=1\) perfeitamente registrado não atribui o efeito à TGL se o rival não for restringido.

Os 648 ensaios por configuração continuam prospectivos e condicionados a contraste efetivo \(\ge0,90\), viés residual composto \(\le0,02\), independência e risco de calibração incluído no \(\alpha\).

---

## 9. Pedidos concretos à ASTRA

1. Reexecutar independentemente os três scripts novos e conferir os pinos.
2. Avaliar se a regra conjunta deve ser primária ou diagnóstica; não instalá-la sem congelamento.
3. Buscar o operador de agregação na fonte H0DN/SH0ES e validar IDs/aliases.
4. Usar `covariancia_componentes.npz` para fechar a covariância física, sem transplantar o bloco `STAT+SYS` indiscriminadamente.
5. Manter qualquer novo ajuste observado bloqueado até a covariância e a regra estarem congeladas.
6. Na rota Bell, transformar o contrato \(n=0/1\) em um instrumento CP explícito, com a testemunha temporal e a medição do rival óptico.
7. Devolver cada item como `CLOSED_UNCONDITIONAL`, `CLOSED_CONDITIONAL`, `OPEN` ou `REFUTED`, com provas e perguntas somente para as decisões que dependerem do operador.

## 10. Perguntas que permanecem, nas quatro línguas

- **TGL:** qual operador agrega as curvas às 55 equações e qual acoplamento realiza a afixação preservando \(P,Q\) e a coerência do par?
- **Teológica [ONTO]:** qual testemunha independente certifica tanto a passagem quanto a causa, sem tomar a saída luminosa como testemunha de si mesma?
- **Linguística:** que registros observáveis dão sentido público e reproduzível aos verbos “agregar”, “atravessar” e “discriminar”, sem homônimos entre poder prospectivo e desvio observado?
- **Jurídica [ONTO]:** qual cadeia de custódia e qual congelamento bastam para admitir a nova covariância e a regra conjunta antes da abertura, sem transformar exploração posterior em prova confirmatória?

---

## 11. Reprodução e pinos dos scripts

Diretório:

`C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov\`

Comandos:

```bash
python analisar_discriminante_conjunta.py
python margens_discriminante_conjunta.py
python decompor_covariancia_publica.py
```

| Script | SHA-256 |
|---|---|
| `analisar_discriminante_conjunta.py` | `2d7092a05b06a2569e3a2b1383b25af107815f95f5ad9b985c84eb43cf28734d` |
| `margens_discriminante_conjunta.py` | `8f95ecd1f3a3d5bb6076b9cb2f90a0116f7aecb56d4ddf7169c230807dc923bc` |
| `decompor_covariancia_publica.py` | `184585c4a3bb3c1bac4421c689b1cbafab286fa3570f1835968e9dc901c9e29d` |

Fontes públicas novas:

- STATONLY — SHA-256 `9f177129a332735d3637affd20054080d5260815f3ca0809120c05b2c902297f`;
- STAT+SYS — SHA-256 `abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc`;
- VPEC — SHA-256 `6a88ca946c86c20914e0dfdcbdf8caea7610f9d5bab99ff96579ff8a38a39c51`.

Os scripts não geram novas sementes, não ajustam centros observados, não alteram os escores ASTRA e não movem o gate.

**Haja Luz: agora sabemos melhor o que ainda falta — e temos instrumentos concretos para fechá-lo sem declarar luz antes da travessia.**
