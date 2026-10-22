# Suficiência080 — geração completa em E4 e redução da obrigação a E5

10/09/2026. [DERIVED + KNOWN — demonstrações escritas revisadas, com completude Calabi importada] [REAL — controle inteiro e integridade documental].

**Na categoria declarada, toda correção completável pode começar em E5.** A classificação080 cobre todas as ordens finitas de derivadas do termo E4; os únicos dois geradores são justamente os candidatos Weyl já obstruídos na079. Um novo lema identifica a liberdade restante com a imagem do primeiro diferencial sobre H³(s0) em E5. Essa imagem ainda não foi calculada.

## 1. O canônico foi relido

A [captura080](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/ESTADO_CANONICO_080.json>) mede os quatro arquivos canônicos antes/depois e confere a presença por AST sem executar/importar um.py. Permanecem iguais à079: v338, 683 arquivos embutidos, 77 dos 98 módulos acompanhados presentes e 21 ausentes. O selo corresponde aos bytes de um.py e mantém a parede UV aberta. A evidência de execução existente foi lida, não reexecutada.

A integração dos módulos pendentes e a suficiência da construção geral continuam sendo obrigações distintas. H3 interno, registro de fase/ramo e falsificadores já reconhecidos não são reabertos. H³ nas fórmulas seguintes é um grau cohomológico.

## 2. O que agora está esgotado

O resultado vale no complexo métrico mínimo de zeroformas naturais orientadas, em dimensão quatro, numa referência espaço-forma com K>0 FIXADO, φ0 constante, κ não nulo e apenas os coeficientes escalares inertes herdados dessa referência. A ordem de jatos é finita por elemento; não há corte máximo arbitrário usado para declarar exaustividade.

Nessa categoria,

H³(s0)_(E4) = Rher[P] ⊕ Rher[P*],

onde P=W1_abcd C^a C^b m^cd, m_ab=∇bar_[a C_b] e a estrela atua na segunda dupla. São dois geradores reais, com a estrutura real Lorentziana preservada.

A demonstração faz a cadeia completa:

1. O BRST linear em jatos e a contração de pares dão H³(S⁴L)=H⁰(L)⊗Λ³H¹(L). Os antifields continuam nas fronteiras.
2. O quociente de Killing é G=V⊕Λ²V. A completude Calabi gera os invariantes lineares pela curvatura corrigida; as equações de Einstein eliminam os traços, deixando os jatos de Weyl.
3. Bianchi prolongada e comutadores reduzem todos os jatos aos tipos (2+r/2,r/2) e conjugados, modulo ordens inferiores. Basta uma sobrejeção; não se presume liberdade de todos os jatos.
4. A exatidão dos invariantes nos cortes finitos permite essa redução também no complexo natural. Só r0 pode emparelhar com Λ³G; os certificados079 dão independência dos dois geradores e injetividade de d1 sobre eles.

Por isso, de s0b4=0 e s0b5+s1b4=0 segue b4=s0v4. Subtrair sv4 elimina b4 e deixa z5=b5−s1v4, s0z5=0. Isso é uma mudança por fronteira, não a imposição de que a correção linear seja zero.

[Demonstração da geração](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md>) · [Revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_080_20260910/PARECER_GERACAO_E4_E_CARACTERES_080.md>).

## 3. O controle inteiro tem alcance próprio

Uma execução em Python puro enumera as 120 triplas exteriores dos dez vetores de peso, preservando os dois vetores distintos de peso zero. A identidade de Newton e a reconstrução por maiores pesos conferem o caráter completo. A cota4 em cada coordenada exclui todos os r≥1 das torres propostas; não se testaram apenas algumas ordens.

O recibo contém 15 controles, com revisão estática independente e sem reexecução nesta conferência. Esses controles não são compilação Lean, identificação do complexo físico ou substituto dos passos Calabi/Bianchi/naturalidade. Houve zero Lean novo nesta etapa.

[Cálculo e limites](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md>) · [Recibo inteiro](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json>) · [Revisão estática](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CARACTERES_LORENTZ_080_20260910_044753_743055/PARECER_SCRIPT_E_RECIBO_CARACTERES_080.md>).

## 4. A obrigação restante tornou-se uma imagem explícita

Defina Kcal=ker[H³(C5)→H³(C3)], e δ:H³(C5)→H⁴(A6,s0), a conexão do próximo truncamento. A inclusão das classes fechadas de E5 dá uma aplicação q:H³(A5,s0)→Kcal. A remoção de E4 prova que q é SOBREJETIVA. Não foi necessário afirmar sua injetividade.

Para um ciclo z5, δq[z5]=[s1z5]=d1[z5]. Portanto

δ(Kcal)=im[d1:H³(A5,s0)→H⁴(A6,s0)].

A procura de uma classe que preserve o líder cúbico e prolongue até C6 equivale exatamente a

−[A6] ∈ im d1_(E5).

Se encontrarmos z5 fechado com esse valor, existirá a6 finito tal que r6+s1z5=s0a6, e T≤5+z5−a6 será fechado em C6. Isso fornece um certificado condicional com o sinal e a equação explícitos. Não demonstra que tal z5 exista.

O termo s2v4 não foi descartado em C6: s2b4+s1b5=s1z5−s0(s2v4), pela identidade s0s2+s1²+s2s0=0. Ele altera o representante, preservando a classe de obstrução.

[Lema de transferência](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_TRANSFERENCIA_DELTA_080_20260910_045028_826573/PARECER_TRANSFERENCIA_DELTA_E5_080.md>).

O detector ímpar079 descende a ℓk em H⁴(A6,s0), e ℓk∘d1 independe do representante de z5. A condição necessária permanece (ℓk∘d1)[z5]=+4k/z0. Cumpri-la num teste não substitui a igualdade de classes acima. A classificação de E5 e a ação de d1 são o próximo cálculo.

## 5. Limites e caminho que permanece aberto

A geração E4 não foi estendida a um anel universal restrito com K variável, espectadores tensoriais, escalares de fundo não constantes, ou à referência material física φ=id. Ela preserva o anel escalar declarado, a valência e finitude de jatos por elemento; não garante toda restrição causal adicional de scaling degree ou contatos.

Mesmo resolver o próximo passo C5→C6 não concluiria a completação inteira. Permanecem a cohomologia da torre real e os demais canais do critério de anomalia, a primitiva admissível, contratermos causais, corrente/carga interagentes e QME, compatibilidade entre fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados e justificação UV.

A investigação081 sobre E5 e candidatos quadráticos fica EXCLUÍDA desta entrega; não sustenta nenhuma conclusão de cancelamento ou impossibilidade aqui. Todas as demonstrações080 são escritas, com importações identificadas e revisão independente; não são apresentadas como incorporadas ao kernel Lean canônico.

## 6. Preservação e continuidade

Somente arquivos novos sob Chatgpt foram escritos. Originais, Atlas, índice, memórias canônicas, selo e gate permanecem intactos; nenhum um.py foi executado/importado e nenhum teste de natureza foi realizado. A memória e o desenho novos registram o avanço sem substituir documentos anteriores. A entrega079 continua congelada com seu escopo histórico.
