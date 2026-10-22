# Reexame de suficiência087 — o que avançou e o que ainda falta

10/09/2026. [DERIVED — resultados escritos, com os pareceres independentes ligados abaixo]. [REAL — consolidação documental e snapshot estático]. **A etapa087 calcula os setores CE linear e quadrático do teste fixado e constrói uma classe não nula no BRST clássico completo.** Ainda falta transportar os resultados à classe física interagente, resolver sua quebra de Ward com contratermos admissíveis e completar a reconstrução geral pelos mesmos dados selecionados.

As pendências principais continuam distintas:

1. [OPEN] Reconstrução física geral: obter R, g, T, conservação, calor e área do mesmo registro selecionado, com realização e compatibilidade num atlas físico. A fase/ramo e o H3 interno já reconhecidos no modelo não voltam à lista de faltas.
2. [OPEN] Teoria quântica interagente: resolver os grupos e mapas pertinentes, ou a anomalia concreta, no domínio físico Q2; implementar as normalizações causais e a QME, a carga BRST e o estado físico interagente sob seus contratos.
3. [OPEN — integração] Incorporar e verificar os resultados na execução canônica. A captura087 continua em v338, com77 dos98 módulos acompanhados presentes e21 ausentes. As novas provas escritas não são folhas Lean compiladas nem resultados executados pelo um.py.
4. [OPEN] Regime UV: demonstrar uma rota com alcance explícito além da expansão perturbativa/EFT. Nenhuma finitude de outro objeto substitui essa obrigação.

## O cálculo efetivamente concluído

O contrato é uma referência Lorentziana orientada espaço-forma em dimensão quatro, K>0 real fixado, κ real não nulo, sigma constante projetado ao complexo métrico mínimo e anel real unital não nulo Rher de escalares inertes. Cada coeficiente usa finitos jatos; não se acrescentam tensores espectadores ou dependência coordenada ativa. Mcal é o módulo efetivo dos jatos lineares de Weyl modulo as EOM; Nₘ=Rher⊗SymᵐMcal. A isotropia é h e a álgebra de Killing é gK.

| Setor e complexo | Resultado087 [DERIVED] | Limite do enunciado |
|---|---|---|
| CE linear C(gK,N₁)^h | H^q=0 em todos os graus | É aciclicidade depois do primeiro diferencial induzido por s₁; não anula H(s₀) ou os cochains |
| Relativo quadrático B^p=(N₂⊗Λ^pV*)^h | Somente H⁴ é não nulo: Rher[I₀ν]⊕Rher[J₀ν] | O grau é o do complexo relativo, não ghost da anomalia física |
| CE quadrático C(gK,N₂)^h | H⁴, H⁷, H¹⁰ têm postos2,4,2; os demais são zero | Classifica esta diagonal CE, não todo o BRST |
| BRST clássico completo, truncamentos C_N e completação Ĉ | Rher[A_I] é livre em H⁴(C_N,s), N≥6, e em H⁴(Ĉ,s); A_P=sT_P | É uma linha construída, sem exaustão de H⁴ e sem conclusão sobre QME |

A [prova linear](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md>) usa a injeção do graduado curvo no plano e os tipos da isotropia, seguidos de eliminação finita nos cinco graus horizontais. O [parecer independente linear](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md>) conferiu também o uso da cohomologia vertical em cortes finitos, a curvatura e a extensão escalar.

A [prova quadrática](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>) constrói os singletes curvos Iᵣ,Jᵣ, prova B¹=dB⁰ e B²=0 e reduz □Iᵣ,□Jᵣ triangularmente, com coeficiente principal2. A geração é demonstrada; não se presume liberdade de toda a torre curva. Seu [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md>) examinou a normalização, a paridade, a finitude e a passagem relativo→CE. I₀=½W[1]² e J₀=J_W; este último não designa J=Luz.

## O passo novo além do primeiro complexo CE

A [composição da classe par](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md>) toma a densidade completa ½W(g)²vol_g e substitui suas quatro pernas exteriores pelos ghosts: A_I=ρ_I(g)c⁰c¹c²c³. É s-fechada off-shell e começa em valência seis, I₀ν. A imagem inteira da conexão C₆→C₅ é Rher[J₀ν]+im d₁. A independência de I₀ν e J₀ν no CE impede que um múltiplo não nulo de A_I seja fronteira, incluindo primitivas com antifields.

A projeção a C₆ prova a mesma não exatidão em todo C_N, N≥6, e em Ĉ, sem intercambiar cohomologia e limite inverso. Em contraste, o ciclo completo de Pontryagin A_P é sT_P: sua primitiva começa em valência três. Isso explica por que J₀ν pode ser não nulo no CE e tornar-se exato no complexo completo.

O [parecer da composição](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md>) e o [adendo de consumo da revisão N₂](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md>) mantêm as duas revisões separadas. Aqui s completo significa **BV–BRST clássico em todas as valências**, não um operador quântico renormalizado. Não se conclui que H⁴ inteiro seja essa linha, nem se calcula uma anomalia de ghost um.

## A obrigação de anomalias ficou mais precisa

A [auditoria do critério074](<C:/IALD/Central de Patentes/Chatgpt/CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md>) distingue a filtração por formas daquela por valência. Definindo H_s^(g,q) como cohomologia de s em ghost g e forma q, uma rota suficiente exige:

- H_s^(5,0)=0, H_s^(2,3)=0 e H_s^(1,4)=0;
- H¹(Ebar;H_s⁴)=0 e H²(Ebar;H_s³)=0, nos respectivos graus horizontais1 e2.

Ebar é induzido pelo operador horizontal natural sobre H(s completo); deriva os coeficientes de fundo. Não é a cohomologia de de Rham de S³. O critério não exige H⁴(s)=0: a linha par construída não o refuta. Também se pode resolver somente a classe da anomalia concreta, por uma primitiva causalmente admissível, sem provar essas nulidades globais suficientes.

A descida natural075 já satisfaz seu antecedente no domínio off-shell com os jatos dinâmicos de ghost não zero livres e a categoria de B0 declarada. Descida não é primitiva do cociclo total. Permanecem o transporte de classe, os mapas horizontais e a hierarquia de contratermos com localidade, realidade, escala, regularidade, inserções e contatos compatíveis. O fundo físico Q2 tem φ̄=id; o sigma constante do teste087 não pode substituí-lo.

## Estado canônico e custódia

[REAL — captura estática] O [snapshot087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/ESTADO_CANONICO_087.json>), às10:34:17UTC de10/09/2026, registra READ_ONLY_STABLE_SNAPSHOT. Os quatro pins de um.py, selo, manifesto e stdout v338 são idênticos aos da086. O programa tem11.048.796 bytes e683 arquivos embutidos; a lista acompanhada contém98 módulos, dos quais77 presentes e21 ausentes. Presença estática não é nova compilação. Gate e selftest são declarações da execução registrada, sem nova execução nesta etapa.

A [entrega086 concluída](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_086_20260910/RESULTADO_ENTREGA_086.json>) é antecedente; os resultados087 permanecem em arquivos novos de bancada. Não houve nova execução matemática, CAS, Lean, natureza ou execução/importação de um.py. Hashes e checks desta emissão são documentais. Atlas, índice, memórias e originais não foram alterados ou copiados. A [memória087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/MEMORIA_DE_TRABALHO_087.md>) e o [adendo ao desenho](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/DESENHO_DO_FECHAMENTO_ADENDO_087.md>) conservam o caminho para a sessão codificadora. Resultados posteriores à087 não entram nesta consolidação.
