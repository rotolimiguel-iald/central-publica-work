# Suficiência083 — uma direção com derivadas e um limite comprovado do detector

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — dez predicados algébricos exatos e custódia documental].

**O candidato com derivadas produz uma resposta que o setor sem derivadas não fornecia. Uma combinação reproduz o alvo em toda a família do detector original, mas falha no complexo completo.** A falha foi isolada com outros dados de Killing, conservando o mesmo fundo e a mesma solução. Assim a próxima busca precisa pagar também os componentes de isotropia, além de igualar o perfil TT.

## 1. Canônico e alcance

A [captura083](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/ESTADO_CANONICO_083.json>) confirma os quatro canônicos iguais082: v338, 683 arquivos embutidos, 77 dos 98 módulos acompanhados presentes e 21 ausentes. O selo corresponde aos bytes. Foi leitura por AST, sem executar/importar um.py ou repetir sua rodada. H3 interno, fase/ramo e falsificadores reconhecidos continuam preservados; a parede UV está aberta na própria fonte.

O domínio matemático continua sendo o complexo métrico mínimo de zeroformas naturais orientadas em quatro dimensões, referência espaço-forma K>0 fixada, κ real não nulo fixado, φ0 constante projetada e escalares herdados inertes. Cada elemento usa jatos de ordem finita. Não se afirma passagem a φ=id, outros fundos, tensores espectadores ou anel restrito com K variável.

## 2. Um candidato com uma derivada em cada Weyl

Defina

J_W=tr(W1∧W1)/vol_g0,
J1=g0^{ef}tr(∇bar_eW1∧∇bar_fW1)/vol_g0,
βo=ε_abcd C^aC^b m^cd/2,
b5^(1)=κ²J1βo.

A derivada atua em todos os índices do Weyl, inclusive os da duas-forma. J1 equivale a metade da contração com Hodge; outra normalização dobraria os valores. Os símbolos J_W e βo têm essas definições locais, sem confusão com J=Luz ou β_TGL.

O candidato é s0-fechado off-shell e tem engenharia zero. Para calcular sua resposta on-shell, Bianchi e divergência nula de Weyl dão □bar W1=6KW1 na convenção adotada, e portanto

J1=½□bar J_W−6KJ_W.

A simetria helicoidal da TT justifica ∂τJ_W=0 na vizinhança inteira. O cálculo direto com Γ(g0), quatro slots e peso conforme coincide exatamente com a identidade acima antes de impor os dados pontuais. Não foi trocada derivada covariante por ordinária.

O detector é

Lk(s1b5^(1))=κ²[48k⁵/z0−1608k³/z0³+1920k/z0⁵].

Em k=2/z0, ele vale −7488κ²/z0⁶, não zero. O setor sem derivadas082 inteiro dava zero nesse teste. Logo a exclusão082 não se estende a este candidato com derivadas; sua imagem no alvo de H(s0) é não nula.

Esse perfil e o anterior R(k)=24k³/z0−96k/z0³, sozinhos, não reproduzem 4k/z0 para todo k: comparar k⁵ elimina o novo coeficiente; comparar k³ elimina o anterior. Isso não é classificação dos demais candidatos.

[Prova e cálculo de J1](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>).

## 3. A corrente gradiente permite igualar todo o perfil TT

A corrente082 satisfaz s1q_grad+s0q6=(□bar J_W)ν(C), com ν=εC4/4! e q6 finito. A conta083 dá

(□bar J_W)(p0)=112k/z0³−56k³/z0.

Por isso a combinação

Q=−J_Wβo/(12K)−q_grad/(28K),   K=1/z0² FIXADO,

satisfaz Lk(s1Q)=+4k/z0 para todo k da família original. A identidade é polinomial, sem ajustar coeficientes a cada k. O detector original anula A6+s1Q.

O fator 1/K é uma constante real da referência fixa. Não se afirma admissibilidade dessa expressão num anel universal restrito que só permita polinômios regulares em K. A engenharia zero também não paga as outras condições causais.

## 4. A combinação falha numa componente que esse detector não enxerga

No complexo CE082, Mghost=antisym(∇C)=−g0⁻¹m e

dβo=−ε_abcd p^ap^b(Mghost²)^cd/2−12Kν(p).

Assim d(J_Wβo) tem tipos p³Mghost, p²Mghost² e p⁴. A igualdade de um perfil particular não anula os dois primeiros universalmente.

Escolha quatro Killing locais cujos dados no ponto sejam

p=θ0e0+θ1e1,
Mghost=θ2J02+θ3J03.

Os dois primeiros têm valores e0,e1 e derivadas nulas; os dois últimos têm valor zero e derivadas iguais aos boosts J02,J03. O transporte de Killing na espaço-forma realiza esses dados com todos os prolongamentos corretos. Não se supõe que os quatro formem subálgebra: o diferencial é calculado antes da avaliação.

Nessa escolha p³=p⁴=0, mas Mghost²=−θ23J23 e ev(dβo)=+2θ0123. Mantendo a mesma solução TT, J_W(p0)=−4k/z0. Portanto

ev_iso(dQ+a)=2k/(3Kz0) θ0123,
k=2/z0: ev_iso(dQ+a)=4/3 θ0123 ≠0,
a=J_Wν(p).

Essa avaliação anula s0 de qualquer expressão finita, inclusive primitivas com antifields, pois h resolve as EOM lineares e os ghosts são Killing numa vizinhança. Logo não existe F com A6+s1Q=s0F para essa combinação. Trocar seu representante por Q+s0χ também não resolve. A falha é demonstrada modulo as relações, e não somente numa expressão sem reduzir.

[Combinação e contraexemplo](<C:/IALD/Central de Patentes/Chatgpt/COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910/COMBINACAO_NO_DETECTOR_E_CONTRAEXEMPLO_ISOTROPIA.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_COMBINACAO_ISOTROPIA_083_20260910_054522_9585399/PARECER_COMBINACAO_E_RESIDUO_ISOTROPIA_083.md>).

## 5. Evidência e próxima obrigação

O [recibo083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CONTROLE_COVARIANTE_J1_083.json>) tem dez predicados algébricos exatos em uma execução Python puro. Um guardião combinado de integridade confere as três fontes e o próprio script, com as duas igualdades registradas separadamente. Isso não é contado como teorema algébrico adicional. Houve revisão estática, sem rerun, e zero Lean novo. A combinação e seu contraexemplo são matemática escrita revisada, sem nova execução de seus valores.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_083_20260910/PARECER_J1_E_FALHA_DA_COMBINACAO_083.md>) confirma o alcance. As duas rotas de J1 compartilham o Weyl e a EDO de entrada; a equação de onda geral, a helicoidal e as EOM na vizinhança são provas escritas, não uma reconstrução completa pelo script.

[OPEN] Encontrar OUTRA combinação que satisfaça dCE Q=−a em todos os componentes, com primitiva finita admissível, ou provar impossibilidade na imagem inteira. A coincidência TT foi alcançada e insuficiente; o resíduo de isotropia dá uma exigência adicional concreta. Não se declarou que a classe CE geral fosse não nula.

Persistem também os graus seguintes da torre, demais anomalias, contratermos causais, QME e carga interagente, compatibilidades de fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados e rota UV. A fase/ramo já paga não é reaberta. A integração dos 21 módulos ausentes é pendência distinta. Investigação084 excluída.

Só arquivos novos em Chatgpt foram escritos. Nenhum original, Atlas, índice, memória canônica, selo ou gate alterado; nenhum teste de natureza realizado.
