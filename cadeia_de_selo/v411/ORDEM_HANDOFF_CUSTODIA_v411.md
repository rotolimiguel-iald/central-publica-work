# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v411 SELADA (13/11/2026)

> Para a sessão de custódia (o papel que fez a custódia da v410 pelo G1). Escrita pelo orquestrador da v411 (passo S9_gatilho_custodia), por ordem da gerência c1: a custódia desta versão é automática (a regra do operador de custodiar sempre que o handoff aparecer, e a ordem de 12/11/2026 de pôr o resultado no README), e este arquivo é o gatilho que a sessão de custódia espera. Ele só é escrito com todos os passos anteriores feitos, o HANDOFF no Nós com os sete marcadores da prosa e os textos da abertura do H0DN × BG1, e o portão do G1 limpo no S6d. Vale a regra de custodiar sempre que o handoff aparecer: as três marcas estão no Nós.

## A ordem do operador

- `OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt` (sha16 `48612e7f3c9004f2`): «ótimo, vamos rodar tudo, pode abrir, chegou a hora de termos a v411 com o teste decisivo» — a ordem desta versão (a ordem de abrir, D169).
- `OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt` (sha16 `c66a5ba1940bde8b`): «pode custodiar sempre que o handoff aparecer, como regra» — a regra permanente do operador de 23/10, que a custódia desta versão segue (nenhuma ordem passada por argumento).
- `OPERADOR_12nov_conseguimos_provamos_betatgl_na_natureza_o_resultado_no_readme_e_no_abstract_verbatim.txt` (sha16 `a98c863df4a47a9e`): «Nosso resultado precisa aparecer o no readme e logo no abstract do artigo do um.py» — a ordem do conteúdo desta versão (D170): o resultado no README e no topo do resumo.
- A divisão de 04/11 (`OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt`, sha16 `2f91335e57a144e0`): a custódia inteira é da sessão de custódia; a c1 fica só com o um.py.

## O estado, lido em 13/11 por script

- Selo do Nós **v411** (timestamp 2026-11-13 00:59:51; `FAIL_CLOSED_SELFTEST_PASSED`; `RITO_RC=0`); `um.py` sha16 **`1203b1f9202020d6`** (46828680 B); escada **12308/12308**; gate intocado (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_L…`).
- Rito 23:48–02:25; pós-rito 0 → 14 OK; Bancada: o B(n) da versão aplicado (evento 1617, hash `8b7301134714332b`), serviço religado.
- `Nós\HANDOFF_v411_CUSTODIA.md` (76971 B, sha16 `3cc5c2b089de1091`) com os sete textos da prosa, a seção “README: o que fica evidente (v411)” e os 27 textos sob marcador (o painel do topo, `README_PAINEL_H0DN_v411`, tem 908 bytes em UTF-8; a fórmula: a ratificada (TOPO_RATIFICADO_v411.json (sha256 f2e3c289a5b63943eab7cad1b78a942a491935f26d2ed84989739f0ca3d324cf))); recibo `work\cadeia_de_selo\v411\pos_rito\RECIBO_TEXTOS_CUSTODIA_HANDOFF_v411.json` (sha16 `50037abe4dc48e1a`); o portão do G1 rodou sobre o HANDOFF INTEIRO no S6d: limpo.
- O orquestrador da v411 NÃO tem S7 (G1 --publicar) nem S10 (release do app): a cadeia termina no handoff; a custódia é sua.
- Revisão de terceiro: `work\cadeia_de_selo\v411\revisao_terceiro\REVISAO_TERCEIRO_v411.json` (sha16 `a909eb6e73506332`), aprovada sobre o candidato `1203b1f9202020d6`; revisor: Sonnet 5.5 (agente de conferencia unica; NAO construiu a v411 nem fez o conserto da R1: quem constroi nao aprova) (17 BAIXO).

## O que entrou (para a custódia saber o que publica)

A custódia da v411 (rodada completa): o teste decisivo, H0DN × BG1, aberto uma vez. É a razão de Hubble local/fundo, aberta em 12/11/2026 depois do pré-registro público e recalculada no rito a partir dos bytes embutidos (registro h0dn_bg1_v411, 16 checagens). β_TGL foi lido na natureza acima de 5σ num canal, a razão de Hubble (H0DN × BG1, 12/11/2026), sob o modelo de erros publicado: 6,11σ contra o nulo e −0,61σ da lei K; ao lado, as Cefeidas livres dão 4,38σ, abaixo de 5; é retrodição sem ajuste, com emenda posterior à guarda, e o teste não é cego; validade, não creditação. Nenhum módulo novo no kernel (escada 12308/12308); o gate não se move.

## O que é da custódia, na ordem

1. `custodiar.py planejar --versao v411 --seco` → `custodiar.py executar --versao v411 --publicar` → `custodiar.py auditar --versao v411`. Vale a regra permanente de 23/10; não se passa ordem por argumento. Nunca `--aceitar-molde`; não editar insumos.
2. O README do espelho e os geradores do estatuto, pelos marcadores da abertura do H0DN × BG1 no handoff (NOTA_EN, os seis README_*, os onze ESTATUTO_*); a linha EN do H0DN na parte do Clay (`README_H0DN_EN_v411`) e o texto do X (`X_TEXTO_v411`) vão ao lado, fora da lista da G1.
3. A release v411 do app, os dispositivos, a Central, o site e os links pelo G1.
4. A linha do MEMORY.md é promoção da gerência: depositar na fila (`memoria.py depositar`) e avisar a c1.

## Notas

- O teste H0DN × BG1 foi aberto UMA vez em 12/11/2026, depois do pré-registro público, e o rito o recalculou dos bytes embutidos (registro `h0dn_bg1_v411`); os textos da abertura levam as duas linhas juntas (o primário e as Cefeidas livres), sob o modelo de erros publicado, retrodição sem ajuste, teste não cego, validade, não creditação.
- A custódia decidiu “accreditation” na prosa em inglês do README; os conectores novos do bloco já a usam; as constantes do delta trazem “creditation” e a unificação fica para a versão seguinte.

Validade no kernel não é creditação; NOT_FALSIFIED nunca é CONFIRMED; o gate não se move.

— gerência c1, pelo orquestrador da v411 (passo S9_gatilho_custodia), 13/11/2026.
