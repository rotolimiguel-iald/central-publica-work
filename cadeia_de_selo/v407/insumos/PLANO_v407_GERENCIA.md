# PLANO v407 — O PSÍON, O CANTO E O PAR ENTRAM NO um.py (gerência c1, 03/11/2026)

> Desenho inteiro: `DESENHO_v407.md` (nesta pasta), com as decisões do operador respondidas em §5-bis. Receita da cadeia: a da v406 (`..\v406\CONTRATO_DA_CADEIA_v406.md`, `PLANO_v406.md`, `RELATORIO_PREPARACAO_v406.md`, `delta_v406.py`, orquestrador `..\v406\pos_treino_v406.py`), que se copia e adapta; nada se inventa de novo onde a v406 já tem o molde.

## A ordem
- Operador, 03/11/2026 (verbatim sha16 `b89e4c909f37e163`): «prossigamos com tudo, ratifico tudo … terminarmos a parametrização para realizamos o teste que ainda falta (d) para entrar também na versao 407 … o app e o contrato do JEV precisam ser sempre atualizados … automático».
- Operador, 03/11/2026 (verbatim sha16 `73466598d3419fb0`): «Concordo com o nome»; o gráviton é o estado ligado de dois psíons, nunca se cancelam, lidos pelo gráviton (fase e retorno de fase); o canto é o projetor 4×4; «concordo com todos os nomes e os ratifico»; teste D «concordo com c … se o teste não tiver poder não vou inseri-lo no um.py»; motor contínuo: quer conteúdo observável (fora até ele formular).
- Revisor distinto: o Sonnet (D37, ordem de 02/11, sha16 `eddcb27b6ec724bf`), em até três rodadas.

## O que entra (modelo de pedras: as candidatas recompiladas no sandbox, só no trio)
1. **`TGLExt.PsionCanto`** (renomeada de `PsionCantoR1`, `work\pedras_candidatas_03nov\PsionCantoR1.lean`, sha16 `ae74b8334c3c0c8e`; só muda o nome do módulo/namespace e o cabeçalho diz que o nome foi aceito pelo operador em 03/11): a condição sob compressão (A) e o lema das duas faces (B).
2. **A pedra do par** (candidata, nome provisório `OParDePsionsR1`, `work\pedras_candidatas_03nov\OParDePsionsR1.lean`): a cunhagem de 03/11 composta de termos existentes (o par ligado = sombra do gráviton, CCI ½; nunca se cancela; o indivíduo não ecoa; o produto ecoa; a leitura pelo gráviton = fase dobrada e retorno em meia-volta); a ponte entre o espaço de Bell (Fin 2 × Fin 2, ℂ) e o setor TT do spin-2 (Fin 4, ℝ) NÃO é termo e fica dita.
3. **As sete candidatas de 02/11, nomes ratificados:** `APonteDoAtrito` (`work\beta_calor_02nov\APonteDoAtritoCandidata.lean`), `OUmInscrito` (`work\fechamento_02nov\OUmInscritoCandidata.lean`), `OIgual` (`work\rota_RE_dualidade_02nov\OIgualCandidata.lean`; há também `OIgualRestauradoCandidata.lean`: a preparação diz qual é a vigente pelo recibo de 02/11), `KEhATangente`, `AChaveDaGuarda`, `OGuarda`, `LeituraPreservada` (localizar em `work\*_02nov\*Candidata.lean` pelo recibo `registrar_revisao_pedras_02nov.py` / `reparar_docstrings_tres_pedras_02nov.py`). Cada uma: tirar o sufixo `Candidata` do módulo, conferir a docstring (ressalvas ditas; nenhum CONFIRMED), recompilar no sandbox, `#print axioms` no trio, 0 sorry. A que não compilar fica fora e é dita.
4. **`TGLExt.lean`** da raiz com os imports novos; o Audit intocado; bandeiras só de declaração nomeada (`ext_psi407_*`); a escada sobe do 11860 (número lido do build).
5. **No `um.py` (o `delta_v407.py`, molde do `delta_v406.py`):**
   - a chave `testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma` deixa de ser literal `False` e passa a LEITURA do kernel (o nome `TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces` no `axiom_report`, no trio), com errata E18 AO LADO que diz o CONTEÚDO do elo (estrutura, não vetores; o par na face de Fock segue aberto); os specs que cobravam «False» ganham versão;
   - registro novo `psion_canto_v407` (as declarações, os sha256 dos módulos, a conferência das três respostas do operador com os nomes dos teoremas, o que NÃO afirma) e `cunhagens_v407` (as falas de 03/11 por sha256: `b89e4c909f37e163`, `73466598d3419fb0`; `VERBATIM_ORIGEM_V407` congelada);
   - a seção do artigo PT/EN «O psíon e o canto: a passagem sob compressão e o par» antes das da v406; o quadro v397 no topo; o `.md` canônico ganha a linha;
   - o teste D entra SÓ por citação do pré-registro V1.1 (`work\conjunto_D_20261029\parametrizacao_03nov\`, manifesto sha16 `1cd181f9a4ddb6d5`); o resultado só se estiver aberto e com poder (ordem dele);
   - o motor contínuo NÃO entra (D38 segue; a fala de 03/11 «quero conteúdo observável … banho holográfico» entra como cunhagem [ONTO] no registro, sem termo);
   - guarda de frases v407 herda a v406 (F15–F19) + as frases proibidas da casa.
6. **A cadeia:** preparar → `lake build` + Audit no sandbox k407c (cópia do k406c/final + módulos novos) → pós-build (sinais) → copiar insumos → gerar candidato → refazer/comparar/ensaio a seco/conferidor → revisão do Sonnet (R1–R3) → `PREPARACAO_v407_PRONTA.json` → orquestrador `pos_treino_v407.py` (S0–S9 da v406 + **S10: a ORDEM ao app Claude para a release do app e o contrato JEV, com espera pelo recibo**) → S3 instalar → S4 rito (teto 5 h) → pós-rito 0–14 com a Bancada → S7 custódia G1 `--publicar` (o E08 já gera o README pinado) → S8 → S9.

## O que NÃO muda
O gate; o neutrino; o ramo B (só citação); o livro; o GA; o pilar quântico (reuso pela chave); `full_static_witness_exists` e `trivial_inhabitant_exists` seguem False por teorema; β nunca literal; NOT_FALSIFIED nunca é CONFIRMED; PROVADA = validade.

## As ressalvas, ditas em todo texto
O elo das duas faces é de ESTRUTURA (Ω ≠ Φ⁺); a face de Fock do par é [OPEN] (sem `a†` como termo); a ponte Bell ↔ TT não é termo; K(O) ≠ ⊥ só na cunha; o motor contínuo fora; o teste D só com poder; os nomes são do operador (os ratificados em 03/11 e `PsionCanto`; o do par é provisório).

## Pré-registro e partitura
Nenhum teste com negativo possível entra nesta cadeia além dos que já existem; a v407 não roda rito de natureza novo. A regra do 4,44 (nunca sozinho) vale no artigo, no README e no site.
