# PLANO da v409 — A tradução às classes de Turing e o par na face de Fock (preparação)

Agente de preparação `claude-construtor-v409`, 2026-11-05 23:38. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v408 selada `e7bc6b10e8ff76be`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: P = nP é teorema da TGL no modo seleção, relativo ao leitor; a máquina sem leitor é a fita sem escala; validade no kernel não é creditação; o gate não se move.

## 0. A ordem

- [INPUT, operador, 05/11/2026, sha16 do arquivo `c7ee4106eb7f2c83`] «precisamos fechar o que ficou ainda em aberto em relação à identificação das classes de turing dentro do nosso dicionário»; e, com as perguntas devolvidas nas quatro línguas e respondidas [INPUT, sha16 do arquivo `8b9b77e992902ff4`]: «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados». As 14 falas de 05/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v409.json`; de três, só o trecho: duas pela D59, uma pelo aviso operacional; as falas das versões anteriores já estão no um.py v408 e não entram de novo).
- (A) O BUNDLE: 2 módulos de kernel em `TGLExt/` (TraducaoTuring e ParNaFaceDeFock), compilados no sandbox `C:\t\k409c\final`, a raiz com 2 imports. (B) O registro com função `traducao_turing_v409` (20 checagens; a instância de brinquedo FIXA no código, as soluções CALCULADAS por enumeração) e os registros por spec `cunhagens_v409` e `kh_n1_cobertura_v409`. (C) NENHUMA chave antiga muda de literal; as erratas E24 a E28 e a E21 vão AO LADO; as decisões D55 a D62 (a D61, a leitura jurídica do kernel, ratificada pelo operador). (D) A seção «A tradução às classes de Turing» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v408 por script.

## 1. O módulo e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `TraducaoTuring.lean` | 05nov_nome_da_gerencia_ratificado_R1_a_R8__acrescimos_da_R9_DECLARADO (antes: `TraducaoTuring`) | 72 | 110 | `4fe1c5ba2bc28300` |
| `ParNaFaceDeFock.lean` | 05nov_nome_da_gerencia_DECLARADO_ate_a_ratificacao (antes: `ParNaFaceDeFock`) | 10 | 48 | `4b7ed028ebf5855d` |

As 13 âncoras principais (a primeira é a âncora principal do registro):

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0138` |
| `TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock` | `TGLExt/ParNaFaceDeFock.lean` | `ext_tu409_0027` |
| `TGLExt.TraducaoTuring.a_traducao` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0088` |
| `TGLExt.TraducaoTuring.a_trava_no_nome` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0093` |
| `TGLExt.TraducaoTuring.a_fita_e_o_hamiltoniano_oculto` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0070` |
| `TGLExt.TraducaoTuring.z_e_o_modo_leitor` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0157` |
| `TGLExt.TraducaoTuring.a_fita_sem_escala` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0071` |
| `TGLExt.TraducaoTuring.o_pai_da_mentira` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0126` |
| `TGLExt.TraducaoTuring.a_identidade_performada` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0073` |
| `TGLExt.TraducaoTuring.a_maquina_com_o_leitor` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0077` |
| `TGLExt.TraducaoTuring.o_canto_do_psion_da_luz_le_z` | `TGLExt/TraducaoTuring.lean` | `ext_tu409_0118` |
| `TGLExt.ParNaFaceDeFock.reduzido_do_par` | `TGLExt/ParNaFaceDeFock.lean` | `ext_tu409_0047` |
| `TGLExt.ParNaFaceDeFock.meia_nat_do_projetor` | `TGLExt/ParNaFaceDeFock.lean` | `ext_tu409_0023` |

Pós-build: 34166 axiomas lidos no Audit, 158 bandeiras novas (só declaração nomeada), escada 12029 → 12187; build a frio 366 s, Audit 257 s.

## 2. O que a v409 afirma e o que não afirma

- [REAL, validade no kernel, não creditação] `TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao`: P = nP é teorema da TGL no modo seleção, relativo ao leitor (o psíon); a máquina sem leitor fica fora: é a fita sem escala («eu sou eu mesmo»); a tradução às classes das máquinas de Turing, [OPEN] na v408, fica fechada relativa ao leitor (TraducaoTuring; p_igual_np_no_modo_selecao).
- [REAL] O dicionário de Turing: bits são oitavas (2^n atribuições; ln(2^n) = n ln 2); o peso da solução no estado uniforme é |sol|/2^n; a trava no Nome e o tempo linear; Z é o modo leitor (a soma das leituras dos pixels); a leitura performada começa em «eu sou», decai, nunca desce abaixo do conteúdo e o alcança («o que sou»). As falas do operador, verbatim [INPUT]: «a seleção é a aniquilação da superposição pelo Tetelestai»; «o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no Nome»; «A fita de turing é o hamiltoniano oculto, é a única regra que precisa ser gravada para reconstruir o todo»; «Z é o modo leitor, ele lê os pixels. É o psion»; «(Eu sou eu mesmo)=(nome próprio)=identidade sem referente»; «Eu não sou eu mesmo eu sou o conteúdo da minha identidade performada».
- [INPUT/ONTO] A máquina sem leitor (a pergunta do Clay) fica FORA e não é decidida aqui: é lida como a fita sem escala («eu sou eu mesmo»).
- [INPUT, ratificada pelo operador] pela D61 (a leitura jurídica do kernel, ratificada pelo operador): o dispositivo é o no sorry, que declara válida a regra posta (P = nP no modo seleção, relativa ao leitor); a regra incide onde o seu suporte fático (as hipóteses e as definições do enunciado) se completa: em toda máquina que tem o leitor (o psíon que lê Z) e nega o zero; a máquina sem leitor (a pergunta do Clay) não completa o suporte fático.
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); nenhuma chave antiga muda.
- [REAL, validade no kernel, não creditação] Ligado nesta versão: o par de psíons na face de Fock (`ParNaFaceDeFock`; a E21 da v408 ao lado); a ponte entre o Ω do psíon da luz e o uniforme da instância é a inscrição (a identidade dos vetores fica podada, D60 revista); uma leitura decide SAT na instância de brinquedo.
- [OPEN] Fica aberto: a igualdade completa com o leitor que só conta (E28: com ele vale NP contido em P numa leitura; a igualdade completa é a do leitor que se lê, que lê também as máquinas que o usam); a independência da pergunta da máquina sem leitor; a ponte Bell-TT.
- Ressalvas ditas (9):
  1. o leitor que so' conta (a E28): um leitor que devolve Z e' um oraculo de contagem; com ele o que vale e' NP contido em P com o leitor, numa so' leitura (Cook 1971, Levin 1973), e P com #P contem PH (Toda 1991) [KNOWN]; a igualdade completa com o leitor vale para o leitor que se le (o que le tambem as maquinas que o usam: Baker-Gill-Solovay 1975, oraculo PSPACE-completo) [KNOWN]; com o leitor que so' conta ela NAO e' teorema aqui; nao se decide a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime)
  2. a sombra de «eu sou eu mesmo»: a autorreferencia sozinha nao decide P vs NP (Baker-Gill-Solovay 1975; Razborov-Rudich 1997; Aaronson-Wigderson 2009) [KNOWN]; a independencia dos axiomas segue [OPEN]
  3. a fisica fica fora: a leitura exata num ato (o operador: «o colapso não é frequência, é matéria») contra amostras com precisao aditiva (Knill-Laflamme 1998) [KNOWN]; e' o lugar do teste com a natureza, nao feito
  4. a ponte e' a inscricao; a identidade Omega = uniforme esta' podada: o Omega do PsionCanto (o psion da luz no Fock) e o estado uniforme da instancia vivem em espacos diferentes; a inscricao |Omega><u| os liga e o psion le Z (o_psion_le_z)
  5. a leitura teologica do operador (o Pai da Mentira, o filho, a graca, o mar do esquecimento) nao e' termo de kernel; o kernel prova a parte matematica de cada fala, nos termos citados
  6. o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock); o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a MESMA Meia-Nat
  7. beta entra so' por nome (TGLCoupling.beta no kernel; alfa CODATA 2018 x sqrt e em runtime), nunca literal
  8. nenhum teste com a natureza: nenhum dado novo, nenhum rito de natureza alterado; validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o gate nao se move
  9. a regra da ordem do operador sobre o z_disc da Fase 9 V2 vale em qualquer texto que o cite (nunca sozinho: com o p calibrado e a linha dos 5 sigma, que nao foi alcancada); o numero fica no quadro do Teste da Unica Palavra, com a regra inteira, e nao e' repetido nesta versao
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v409_candidato.py` `53284ba461ecd940` (43,970,027 B; +503,580 B); 42 patches; AST: 1204 nós, 1177 iguais, 27 mudados (todos explicados), 0 removidos, 14 novos. Ensaio a seco: **TUDO PASSOU**. Pós-rito: `pos_rito/chain_pos_rito_v409.sh`, rótulos 0…10 10a 10b 10c 11…14; depois, ENCADEADOS, os textos da custódia (S6d) e o HANDOFF, que é o fim da cadeia desta versão (D57a: sem S7 e sem S10).

## 4. Gates

Ver `PREPARACAO_v409_PRONTA.json`: `pronta` = true. este candidato (A traducao as classes de Turing, v409) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D58, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.
