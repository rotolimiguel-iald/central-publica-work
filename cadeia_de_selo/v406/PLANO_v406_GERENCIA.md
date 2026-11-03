# PLANO v406 — O FECHAMENTO ENTRA NO um.py (gerência c1, 02/11/2026)

> Este é o plano da preparação que `fechar_preparacao_v406.py` cita. O desenho inteiro está em `work\fechamento_02nov\DESENHO_v406.md` (o que muda) e as medidas em `DESENHO_v406_MEDIDO_02nov.md`; a receita da cadeia em `RECEITA_CADEIA_DE_SELO_v404_para_v405_para_a_v406.md`; o contrato para os scripts em `CONTRATO_DA_CADEIA_v406.md`; a ratificação do que entra em `RATIFICACAO_R10_c1_02nov.md` (sha16 `846c999d6284f338`).

## A ordem
- Operador, 02/11/2026 (verbatim sha16 `f3998f01262aad6b`): «perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.»
- Prioridade (sha16 `9978862f60cfbf29`): «a construção da passagem para o contínuo é o que mais importa».
- Execução (sha16 `b5717ff445a883cd`): «quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor».
- Revisor (sha16 `eddcb27b6ec724bf`): «designe para o Sonnet revisar tudo, ele é tão capaz quanto».

## O que entra (bundle de 301; modelo da v394)
1. Os 300 módulos da bancada do ChatGPT (missão F1.FECHO_20261015, 15 e 16/10/2026), recompilados do fonte na integração R3 de 02/11 (300/300, 0 falhas; cada fonte conferida por sha256 contra o recibo da bancada antes da normalização), e a candidata `CanonicalFullTGLWitnessR1` (nome provisório da gerência: os nomes das pedras são do operador).
2. A raiz `TGLExt.lean` com dois imports; o Audit intocado; 1794 bandeiras só de declaração nomeada (`ext_fch406_*`); escada 10066 → 11860.
3. O registro com função `fechamento_v406` (as 8 âncoras, os 301 sha256, as quatro chaves lidas do kernel, o que fica False por teorema, a escada, o gate) e os specs `cunhagens_v406` (23 falas de 02/11) e `kh_n1_cobertura_v406`.
4. As quatro chaves de testemunha deixam de ser literal `False` e passam a leitura do kernel (`_v406_certificado_habitado`), com a errata E14 ao lado; os specs antigos que cobravam «falso» ganham versão (E17); `rede_fock_v394` ganha a troca dita de veredito.
5. A seção do artigo PT/EN «O fechamento: a passagem para o contínuo e o certificado habitado» e a linha do `.md`, antes das da v405; o quadro v397 fica no topo.

## O que NÃO muda
O gate (`evaluate_quantum_gravity_closure`, `prove_qg_closure_gate`), o neutrino, o ramo B, o livro, o GA; `full_static_witness_exists` e `trivial_inhabitant_exists` seguem False por teorema; o pilar quântico (REUSE pela chave de cache); a seção do selo pela própria tecnologia; o número da massa; nenhum dado novo; nenhum rito de natureza.

## A cadeia (na ordem; cada passo com o seu recibo)
preparar bundle → `lake build` + Audit no sandbox k406c (medido: 1736 s + 280 s) → `pos_build_kernel_v406.py` (40 sinais) → `copiar_insumos_v406.py` → `gerar_candidato_v406.py` (32 patches) → `refazer_candidato_v406.sh --regerar` (comparar, ensaio a seco, esperados, conferidor negativo/positivo, citações, diff e pinos, conferência do instalar/rito, p00) → `pos_rito\montar_textos_v406.py` + harnesses → B(n) pré-selo (`bateria_pre_selo\rodar_bn_pre_selo_v406.sh`, B15) → `pino_memoria_py_v406.py` → revisão de terceiro (Sonnet; `revisao_terceiro\PEDIDO_REVISAO_v406.md`) → `gerar_relatorio_v406.py` (PRONTA) → `fechar_preparacao_v406.py` → orquestrador `orquestrador\pos_treino_v406.py` (tarefa `IALD_pos_treino_v406`): instalar → rito → pós-rito 0–14 (Bancada por PID) → G1 `--publicar` → relatório.

## As ressalvas, ditas em todo texto
K(O) ≠ ⊥ só na cunha; «núcleo II∞» [KNOWN/DECLARADO]; traço ENNReal cíclico, não linear; R7 Codex×Codex e a revisão distinta do Sonnet; #eval removidos; R4/R5 fora; duas chaves False por teorema e o lema que falta; o nome provisório. Validade no kernel não é creditação; `NOT_FALSIFIED` nunca é confirmação; o gate não se move.

## Decisões da gerência (D34–D40) e erratas (E14–E17)
Em `delta_v406.py` (`DECISOES`, `ERRATAS_V406`), embutidas no candidato e no registro. As decisões do operador pendentes (nomes das pedras candidatas; motor contínuo no pilar, v407; README pinado e a linha do 4,44 no site) ficam no manual da gerência da custódia.
