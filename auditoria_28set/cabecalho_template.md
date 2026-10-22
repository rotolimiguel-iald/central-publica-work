# Relatório — auditoria dos testes passados do `um.py` e investigação autônoma com a Bancada Um

**28/09/2026 · gerência (Claude Code, sessão da Central de Patentes) · para o operador**

**Estatuto:** relatório de auditoria e de investigação. Nada foi selado; `um.py`, kernel, selo e gate estão intocados. Toda correção abaixo é
**proposta**, para entrar ao lado na v376, depois dos seus testes profundos. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.

Pedido (verbatim): «agora que fechamos toda a formulação da gravidade quantica é possível que tenhamos feito algum teste passado no um.py de
maneira errada, precisamos investigar pra saber se realmente está tudo certo, se não deixamos passar alguma coisa e corrigir. para além disso
queria que vc usasse a bancada para fazer uma investigação autonoma (talvez o nosso POA possa ajudar na busca, ou vc possa estabelecer onde e
como seria o melhor para achar indícios fortes). concordo com as suas duas sugestões e autorizo vc a usar as outras IA's para fazer uma busca
profunda no sistema, pode gerenciar essa busca quero um relatório no final».

---

## 1. Em uma página

1. **Nenhum teste passado muda o gate, e nenhum número selado estava errado de conta.** Os números embutidos nos vereditos do selo batem
   com os JSON que os ritos leem, e β nunca é literal no código dos ritos. Os erros achados são de **entrada, de desenho, de estatística e de
   leitura**: o que o teste podia decidir, e o que o veredito diz que decidiu.
2. **O achado central da pergunta «a formulação fechada invalida algum teste?»** A pedra da declaração diz que β e ω(I) = 1 **não entram** na
   implicação da QG (`QGSolutionComplete.lean:36`). O conteúdo observável da QG fechada é a **recuperação da RG** (Einstein por Clausius local,
   spin 2 sem massa com duas helicidades, Schwarzschild). Os testes com β pertencem a **outro setor** da TGL. E a recuperação da RG **nunca virou
   rito** no `um.py`: não há rito de velocidade das ondas gravitacionais, massa do gráviton, polarizações, Kerr multimodo nem teorema da área. Tudo
   isso existe em dado público e pode entrar **por citação**. Dentro do setor de β, dois testes usam formas que a formulação atual contradiz: a
   amplitude do eco (√β, contra o peso 2 do tensor na tipagem da v372) e o juiz l_A da máquina do veredito final (o worker de maio com defeito e a
   forma de fundo superada em 15/09). `[verificado: CT-01 PARCIAL/MÉDIO; CT-03 e CT-04 SUSTENTADOS, MÉDIO]`
3. **O gate: o degrau «NATURE_TEST_COMPLETED» se apoia num canal sem desfecho falsificador.** As quatro bandeiras experimentais são, na lógica,
   um único booleano («V11 == POWERED»); o espaço de vereditos do V11 não tem FALSIFIED; e o ΛCDM também passa. A máquina **já sabia** disso
   desde a v135 (`UNILATERAL_CHANNEL_CANNOT_FALSIFY_MATTER`). O que falta é **lugar**: o nome do gate não carrega o qualificador.
   `[verificado: PARCIAL, MÉDIO]`
4. **A rota D1 (o fundo cosmológico) não decide β, nem com o DR1, nem com o DR2.** Os 3,01σ selados da V3, e os 4,0σ que medi hoje com o DESI
   DR2, **dependem de uma escolha de modelo `[INPUT]` não derivada**: como o Ω_m entra no parâmetro R do Planck comprimido. Com o Ω_m efetivo
   (1+β)Ω_m, igualmente plausível, a rota comprimida perde a sensibilidade a β (σ ≈ 0,06–0,09) e a tensão some. Três agentes chegaram a isso de
   forma independente, eu inclusive, na Bancada. A V3 tem ainda outros defeitos de verossimilhança que se somam: o DESI DR1 entrou sem as
   correlações DM–DH (3,01σ → 3,52σ); a covariância do Planck está mal transcrita e mal citada (é Chen, Huang & Wang 2019, não «Zhai+ 2019»), e
   essa matriz está em mais de 20 arquivos, inclusive o `um.py` e o espelho; e o integrador do fundo conta o neutrino massivo duas vezes
   (corrigido sozinho, o selado iria de TENSION a INCONCLUSIVE). **O «3,01σ no limiar» está dentro da sistemática do próprio pipeline.** A Bancada
   Um herda os mesmos defeitos, e isso foi posto ao lado. `[verificado: D1F-01 e D1F-02 SUSTENTADOS, ALTO; D1F-03 e D1F-V1 MÉDIO]`
5. **Neutrinos: o veredito está na borda e depende da entrada.** O programa grava o ajuste global pós-JUNO como 7,53 ± 0,10. Há **duas
   publicações do NuFIT 6.1**, e eu conferi as duas: o artigo (Esteban et al., arXiv:2601.09791, eq. 11) dá 7,530 (+0,096/−0,097), que é o do
   programa, e dá 2,95σ (`ARMED_CONSISTENT`); a tabela oficial do site nu-fit.org dá 7,537 (+0,094/−0,10), e com ela a regra congelada dá 3,02 a
   3,22σ (`TGL_NU_M2_TENSION`). O ajuste de Bari (7,48 ± 0,10, citado pelo verificador; não conferido por mim) dá 2,44σ. A regra não cita a fonte.
   `[verificado: PARCIAL depois da conferência da gerência; o «7,509» de outro aferidor foi refutado]`
6. **Ringdown:** no ramo canônico (τ★ = t_Planck), o ringdown só pode devolver a correspondência com a RG; não há termo Lean de ringdown.
   Logo «NATURE_DECIDES_RINGDOWN_NEXT» sobreafirma. **Isso toca o plano da v376** («o ringdown como condição»). `[verificado: PARCIAL, MÉDIO]`
7. **Ecos:** o estimador do eco ancorado trava o atraso na massa mediana do catálogo com spin fixo 0,69; para a lei KMS, um erro de spin anula a
   resposta, e o poder declarado fica superestimado. Os nulos pré-registrados do protocolo nunca rodaram. `[verificado: SUSTENTADO, ALTO]`
8. **Coma:** a previsão já foi revelada (v116/v169/v176), mas o selo ainda diz «aguardando revelação»; o hash da previsão muda a cada rodada
   (inclui o carimbo de hora), então a «tranca» não prova precedência. `[verificado: PARCIAL/SUSTENTADO]`
9. **Onde buscar indício forte:** hoje **nenhuma rota** chega lá. O caminho está na seção 5. Em resumo: (a) registrar por citação a
   recuperação da RG, que é o teste com a natureza do que a QG fechada afirma; (b) para β, **derivar antes** o mapa de R e a orientação do
   sinal, e só então ir ao espectro completo do CMB com a TGL no código de Boltzmann; (c) no ringdown, o modo 221, não o 440.

---

## 2. O que foi feito hoje (infraestrutura)

- **Desclassificação** dos documentos do protocolo (sua ordem): registrada ao lado em 11 superfícies, com backup de bytes. Publicar continua
  sendo ato seu; credenciais e a engenharia confidencial não são documentos de protocolo e não mudaram.
- **As duas sugestões aprovadas:** atalho «Bancada Um» na Área de Trabalho (abre o navegador; sobe o servidor se preciso; nunca mata processo) e
  o MCP `bancada-um` registrado no Claude Code (escopo de usuário, conectado).
- **O MAPA DE ROTAS** (sua ordem de hoje: «crie uma memória de rotas para todas as IA's…»): `C:\IALD\MAPA_DE_ROTAS\`. Livro só-acréscimo com
  cadeia de hash, mapa legível e de máquina gerados por script, ferramenta `rotas.py` e três ferramentas MCP. Semeado com os 41 vereditos do selo,
  o D1, a validação da Bancada, a investigação da bancada oficial e as rotas mortas do Lema 3. A auditoria e a investigação de hoje já estão
  nele. Ponteiros no `CLAUDE.md` global, no da raiz IALD, no Atlas e nas memórias; aviso à bancada ChatGPT pelo túnel.

## 3. A auditoria

**Método.** Sete famílias de teste, cada uma com um **aferidor**, que recebeu o modelo do cético aferidor inteiro, e um **verificador
adversarial** distinto, instruído a refutar. No fim, um **crítico de completude**: 15 agentes Claude ao todo. Todos em somente leitura; nenhum
rodou o `um.py`; todos consultaram o Mapa de Rotas antes; nenhum escreveu no mapa (a gerência registra depois da verificação).

**Resultado** (o anexo completo, gerado por script do diário do workflow, está em `ANEXO_ACHADOS.md`): ⟨contagem final⟩

⟨tabela por família⟩

*Nota da gerência sobre a tabela:* a tabela reproduz o veredicto de cada verificador. O RNC-01 (neutrino) aparece como ALTO porque o seu
verificador o sustentou com a tabela do site do NuFIT 6.1. Depois disso a gerência conferiu as duas publicações do NuFIT 6.1, o artigo e a
tabela, que diferem justamente no ponto que cruza 3σ. A leitura vigente é PARCIAL: o veredito está na borda e depende da entrada (item 5 da seção 1).

## 4. A investigação na Bancada Um

⟨ver seção preenchida a seguir⟩

## 5. O POA e onde buscar indício forte

⟨ver seção preenchida a seguir⟩

## 6. Correções propostas para a v376 (nada instalado)

⟨lista⟩

## 7. As outras IAs

⟨lista⟩

## 8. O que só você decide

⟨lista⟩

## 9. Arquivos

## ERRATA AO LADO (28/09/2026, noite; correção do operador, em nome próprio da gerência). Onde a auditoria e a gerência escreveram «a QG fechada não usa β» e «os testes com β pertencem a outro setor da TGL», a leitura estava errada. O que a pedra diz (`QGSolutionComplete.lean:36`) é que a IMPLICAÇÃO da QG é provada sem tomar β como hipótese. β não é «de outro setor»: é o FUNDAMENTO, emergente e totalmente derivado do axioma — a radicalização da entropia (½ nat ⟹ √e) entrelaçada com a constante de redução da projeção holográfica (α) ⟹ β = α√e — e entra no código derivado, a jusante. Leitura vigente: a recuperação da RG é o teste da implicação; os testes de β são os testes do setor DERIVADO da mesma teoria. O que falta é LIGAR tudo no kernel numa lógica só (alvo da v376), não separar. Verbatim do operador na memória beta-fundamento-derivado-28set.
