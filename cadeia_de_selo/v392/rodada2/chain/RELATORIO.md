# RELATORIO -- agente CHAIN, rodada 2 (13/10/2026): a cadeia POS-RITO da v392

Gerencia c1, programa IALD/TGL. Estatutos: [REAL] medido/lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e nao conferido; [OPEN] em aberto.
Pasta de saida: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\pos_rito\` (chamada `SEL` abaixo; `V` = `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392`).
**Nada foi executado da cadeia** (nem do derivado, nem do rito, nem do instalar). Nada no git, no site, na memoria real, no quadro nem no mapa. Verificacao feita: `ast.parse`,
`pyflakes` (zero nomes indefinidos), `sh -n` (ok), contagem de placeholders de cada formatacao `%` por AST (as 3 "discrepancias" sao `% tupla_ja_pronta`, falso positivo), a guarda P18
(`guarda_p18_v392.py`) sobre `textos_v392.py` e o rascunho (LIMPO), e leituras so de leitura dos alvos reais (ancoras, abaixo).

## 0. ACHADO BLOQUEANTE (nao e' da cadeia; e' do conferidor/ESPERADOS ja prontos) -- leia antes de rodar
`V\conferir_rito_v392.py` compara `[external_ladder.n_theorems_clean, n_theorems_expected] == ESP["escada"]` e monta `"KERNEL_%d_OF_%d_THEOREMS" % (E[0], E[1])` e o `.replace(... % tuple(E))`
com `E = ESP["escada"]`. Mas `V\ESPERADOS_v392.json` traz `escada = [6163, 6893]` ([antes, depois], copiado de `CANDIDATO_v392.json`). Depois do rito o core dira `[6893, 6893]`:
tres itens "deve mudar" dao NAO (a escada subiu; o registro `estatuto_da_prova_v391` -- a troca dita --; o `three_stress_tests_v387`) mesmo com o rito perfeito, e o passo 1 da cadeia
para ("CONFERIDOR REPROVOU"). O controle negativo pre-rito nao o exibe (tudo da NAO de qualquer modo). Conserto (do dono do conferidor/gerar_esperados, nao meu): no `conferir_rito`,
`E = [ESP["escada"][1], ESP["escada"][1]]`, ou gravar `escada` como `[N, N]` e `escada_antes` a parte. Minha `leitura_v392.py` le a escada como `[antes, depois]` (usa `[1]` para o rito e `[0]` para o texto) e
nao depende disso. Em tempo de execucao a cadeia so' ve o NAO.

## 1. O que derivei (arquivos em `SEL`)
| arquivo | o que e' | molde |
|---|---|---|
| `chain_pos_rito_v392.sh` | a cadeia, passos 0 a 14 (225 linhas); GERADO por `derivar_cadeia_v392.py` | `v391_selo\chain_pos_rito_v391.sh` (trechos herdados por ancora: prelude `set -e`/`parar`, guarda do um.py instalado, copia byte a byte do conferidor, `porta_memoria`) |
| `derivar_cadeia_v392.py` | gera o `.sh` (trechos herdados + blocos novos, cada ancora com assert) e CONFERE que os invariantes do molde sobrevivem nos .py v392; grava `DERIVACAO_v392.json` (sha16 do molde e do derivado) | `derivar_cadeia_v391.py` |
| `leitura_v392.py` | so' leitura do Nos e de V; descobre os registros novos por diferenca com `ESPERADOS.vereditos_v391`; PROBLEMAS param | `leitura_v391.py` |
| `textos_v392.py` | todos os textos (linhagem, desenho, Atlas, CORE_MEMORY, Haja_Luz, topicos, handoff, aviso, as erratas, a linha da arvore, verbete, remissivo) | `textos_v391.py` |
| `superficies_v392.py` | plano em 2 fases; backup de bytes `.bak_<STAMP>_sup392`; erratas AO LADO (inline) + appends; MEMORY.md/MEMORY_2.md; topico novo `v392-selada-pedras-e-barreiras-13out.md`; AVISO so' com reivindicacao | `superficies_v391.py` |
| `patch_arvore_indice_v392.py` | gerador da arvore: +linha v392 e erratas CR-08 (l.155 e l.272) e CR-02 (l.272), por linhas NOVAS; `atlas_indice.py`: manifesto, verbete, remissivo. **Escrito, nao aplicado.** | `patch_arvore_indice_v391.py` |
| `errata_claude_md_v392.py` + `RASCUNHO_errata_claude_md_v392.txt` | errata ao lado no `C:\IALD\CLAUDE.md` depois da ancora `<!-- errata_estatuto_da_prova_v391_07out -->`, marcador `<!-- errata_v392_selada -->`. O rascunho e' so' gabarito. | `errata_claude_md_v391.py` |
| `fechar_v392.py` | os 3 recibos do B(3) (senao RECUSA); `DIFF_v391_v392.diff` (GNU diff -U2 do `um.py.bak` x selado) e `DIFF_KERNEL_v392.txt`; manifesto `v392_incorporacao_manifesto.json` (em `pos_rito` e em `cadeia_de_selo`); `MANIFESTO_ARQUIVO_v392.json`; copia `pos_rito`->`cadeia_de_selo\v392_selo` e kernel+pedras->`cadeia_de_selo\v392_kernel`; handoff `handoff-v392-custodia.md` e `Nos\HANDOFF_v392_CUSTODIA.md` | `fechar_v391.py`/`v390.py` |
| `registrar_mapa_v392.py` | MONTA `registro_mapa_v392.json` (1 ROTA nova + 8 ANOTACAO que fecham ou dizem que NAO fecham o proximo passo das 8 rotas + 1 ANOTACAO da R3 em `neutrinos.m2.normalizacao`) e imprime o comando; **nao registra** | `registrar_mapa_v391.py` |
| `b3_recibo_v392.py` | confere a ultima linha JSON do esboco B(3) e o recibo que ela cita (bateria passa, v392, pos_selo, modo) | novo |

## 2. De onde cada coisa e' lida (nada digitado)
- sha16 do um.py v392: `V\APLICADO_AO_CANONICO_*.json` (e o disco); escada: `ESPERADOS.escada` e o stdout `teoremas limpos: N/M`; pedras, bandeiras, declaracoes: `core.pedras_v392`; varredura: `core.varredura_e_sorry_v392`;
  registros novos: diferenca entre o core e `ESPERADOS.vereditos_v391`; verbatins de 13/10: `ESPERADOS.verbatins` (sha16); numero de declaracoes: `len(core.kernel_formalization.axiom_report)`.
- Pinos do B(3): `V\PINOS_BN_v392.json` (sha256 inteiros; cada pino e' recalculado e comparado ao arquivo; divergencia = PARADA); o sha256 do `kernel\KERNEL_RECIBO_v392.json` e' **lido na hora** (e a arvore do recibo tem de existir).
- A errata do CLAUDE.md le o numero antigo (`o kernel (N teoremas limpos)`) do proprio arquivo; a escada nova do core; as pedras do `pedras_v392`.
- Coulomb: os numeros (2,241%, 2,713%, +1,12%, 6,3 a 7,7) estao digitados no texto mas **conferidos por assert contra `A_SN\RELATORIO_AUDITORIA_A_SN_C1.md`** a cada execucao; o NU2: `B_NU2\_verif_memoria_NU2.json`; a ressalva (3): sha16 de `PROGRAMA_IALD\levantamento_qg\consolidado.json` (lido).
- Todo termo de kernel citado (`LiganteLeiCampoCurvo`, `passage_h3_to_connected_smooth_atlas_einstein`, `NamedAtlasH3`, `area_atlas_unique_global_einstein`, `continuous_modular_positive_square_root`...) e' conferido por busca no kernel do Nos em tempo de execucao.

## 3. A ordem, com os comandos exatos
Pre-requisito: o rito terminou (`RITO_RC=` no `Nos\rodada_v392_stdout.txt`), o conferidor/ESPERADOS corrigidos (ver 0), a cadeia roda no Git Bash.
```
cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v392/pos_rito"
# opcional: export V392_AVISO_REIVINDICACAO="<id da reivindicacao que nomeia AVISO_GERENCIA.md>"
sh ./chain_pos_rito_v392.sh > chain_v392_out.txt 2>&1        # passos 0..10 (para no 10a/10b com AGUARDA_OPERADOR, rc 20)
```
| passo | o que faz | para quando |
|---|---|---|
| 0 | guardas: um.py do disco = instalado = candidato; ferramentas/superficies existem; guarda P18 sobre `textos`; `RITO_RC=` no stdout | qualquer uma |
| 1 | copia byte a byte (conferidor, ESPERADOS, logs) para `pos_rito\conferidor`; marcador `.servidor_parado_pelo_rito` nao pode ter ficado; `python -I -B -X utf8 conferir_rito_v392.py` | nao termina em `TUDO BATE` |
| 2 | `leitura_v392.py` | `PROBLEMAS` nao vazio |
| 3 | ENSAIO em copias: superficies (plano conferido antes da 1a escrita), MEMORY.md da copia < 24.000 B e <= 195 linhas, errata do CLAUDE.md em copia, patches da arvore/indice em copias, a arvore em `dry` (confere que as 3 linhas novas saem) | qualquer falha |
| 4 | `patch_arvore_indice_v392.py` (real; backups `_p392`) | ancora != 1 ocorrencia |
| 5 | `arvore_da_prova.py v392` | |
| 6 | `atlas_indice.py v392` (o indice antes das superficies) | |
| 7 | `superficies_v392.py` (real) e `errata_claude_md_v392.py` | guarda P18; MEMORY.md; ancora |
| 8 | `porta_memoria.py` (o ATLAS a mao nao se toca) | rc != 0 |
| 9 | `grep -c -F` do **marcador do selo e do sha16** em cada superficie (`<!-- atlas_v392_selada -->`, `<!-- adendo_v392_selada -->`, `<!-- errata_v392_selada -->`, `errata_cr08_v392`, `errata_3_v392`, `errata_coulomb_v392`, o sha16...); zero = PARADA; MEMORY.md < 24.000 B e <= 195 linhas | zero |
| 10 | B(3) ENSAIO pos-selo (`python -I -B -X utf8 vinculo\sincronizar_bancada.py --bancada C:\IALD\Bancada_Um --producao --nos ... --versao v392 --fase pos_selo --modo ensaio --bateria ... --bateria-sha256 ... --recibo-pre-selo ... --recibo-pre-selo-sha256 ... --selo-anterior ... --kernel-manifesto-anterior ... --kernel-recibo ... --kernel-recibo-sha256 <lido na hora> --criterios ... --criterios-sha256 ... --saida V\bancada_B3_ensaio_<stamp>`); `b3_recibo_v392.py` confere | **arvore do sandbox do kernel ausente -> `AGUARDA_OPERADOR` (rc 20): rodar `sh V\refazer_sandbox_v392.sh` (~8 min, ~30 GB) e retomar com `CHAIN_DE=10`** |
| 10a | exige `V\bancada_B3_servico\RECIBO_PARADA_v392.json` e a porta 18777 fechada | sem recibo: `AGUARDA_OPERADOR` |
| 10b | B(3) APLICAR, **so' com** `B3_AUTORIZADO=sim`, `EVENTO`, `EVENTO_HASH` (do retorno de `iald.py anotar`) e o recibo da parada; `--saida` pasta nova `V\bancada_B3` (`_2`, `_3`...) | sem a variavel: `AGUARDA_OPERADOR` |
| 10c | exige `V\bancada_B3_servico\RECIBO_RELIGAMENTO_v392.json` | sem recibo: `AGUARDA_OPERADOR` |
| 11 | `fechar_v392.py` (recusa sem os 3 recibos) | |
| 12 | `registrar_mapa_v392.py` (so' monta) | |
| 13 | `inventario_bancada.py` + `gerar_documento.py` em `work\inventario_bancada\`; copia para `memory\INVENTARIO_BANCADA_CHATGPT.{md,json}` com backup de bytes | |
| 14 | `NOS_VIVO\construir.py` (rodar depois do registro do passo 12) | |
Retomada: `CHAIN_DE=<passo> [CHAIN_ATE=<passo>] sh ./chain_pos_rito_v392.sh` (passos validos: 0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14). Aplicar o B(3):
`B3_AUTORIZADO=sim EVENTO=<seq> EVENTO_HASH=<hash16> CHAIN_DE=10b CHAIN_ATE=11 sh ./chain_pos_rito_v392.sh`.

## 4. O que depende de ato da gerencia ou do operador
- **Operador:** a palavra para a B3 (parada e religamento do `um_bancada.py`, reconexao dos adaptadores MCP). Sem ela a cadeia fica em 10a e **o fechar, o handoff e a custodia nao nascem** (plano R3, Remissao 4).
- **Gerencia:** corrigir o conferidor/ESPERADOS (secao 0); `sh refazer_sandbox_v392.sh` antes do passo 10 (o recibo do kernel aponta para `C:/t/k392/arvore`, apagada; o sha do recibo muda; os PINOS_BN guardam o sha velho do recibo, que a cadeia ignora de proposito); o evento c1 `SINCRONIZACAO_BANCADA` e o `EVENTO_HASH`;
  produzir os dois recibos de servico (`bancada_B3_servico\RECIBO_PARADA_v392.json` com `pid`, `porta` = 18777, `porta_fechada` = true e `hora`; `RECIBO_RELIGAMENTO_v392.json` com `versao_servida` = "v392", `manifesto_sha256` = o `manifesto_novo.sha256` do recibo do 10-bis, `pid` e `hora`) -- **esse contrato e' meu (o plano diz so' "PID, porta 18777 fechada, hora"); o ato que gerar os recibos tem de obedece-lo ou o `fechar` recusa**;
  executar o comando impresso por `registrar_mapa_v392.py`; reconstruir o Nos vivo depois; a reivindicacao do `AVISO_GERENCIA.md`; o aviso de selo a coordenadora (molde `despachos\msg_v391_selada_coordenadora.md`; **nao o derivei**); quadro F0.5 -> ENTREGUE; auditoria independente (quem constroi nao aprova);
  P9 (registrar as etapas no banco da memoria comum), P10 (conferir o heartbeat pelo log depois do rito); conferir `TGL_INDICE_VIVO.md` (passo 9 exige o sha16 la: depende de o `atlas_indice.py` o escrever no verbete; se nao, falha visivel e o marcador do indice se ajusta).
- **Sessao do site / operador:** a custodia do plano §13 e commit/push; as erratas do espelho (README l.23/l.221, o artigo "Custo" -- Coulomb) e o `um_absoluto_forma_canonica.md` (regenerado pelo rito).

## 5. Ancoras conferidas por leitura (REAL, so' leitura dos alvos reais)
- `cadeia_de_selo\arvore_da_prova.py` (`ee2cb7413238ff1f`, 340 linhas): l.155 (docblock v116, "NOMEADA e aberta"), l.262 ("PAGA como implicacao (v317)"), l.272 ("NAO PROVADO ..." com "a emergencia geral" e "T_c = Δ_c^{1/2}") e l.287 (linha v391): **1 ocorrencia cada**. `atlas_indice.py`: `_i391p`, `verbetes = [`, entrada e remissivo da v391: 1 cada.
- CR-08 (regex da M01, a frase e o token `FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM`), medido hoje: Linhagem 1 (l.8568), Desenho 1 (l.2220), Atlas 4 (l.11613, 11826, 34865, 34873), `HANDOFF_v390_CUSTODIA.md` 1, `handoff-v390-custodia.md` 1. As linhas da M01 (12/10) ja se moveram um pouco: os scripts **buscam em tempo de execucao**, nao usam numero de linha.
- Errata (3): a linha `**O que entrou** (pacote \`work\v391_pacote\`` da Linhagem e' unica (hoje l.8581). Coulomb no `Haja_Luz\CLAUDE.md`: l.4368-4369 (um grupo) e l.4379 (outro) -> 2 erratas. `C:\IALD\CLAUDE.md`: a ancora `<!-- errata_estatuto_da_prova_v391_07out -->` tem 1 ocorrencia e a frase `o kernel (N teoremas limpos)` 1.
- `MEMORY.md` hoje 192 linhas / 19.837 B: o gancho da missao e o da PALAVRA sao TROCADOS (as linhas velhas vao ao MEMORY_2 verbatim) e so' o handoff v392 e' linha nova -> 193 linhas; guarda <= 195 e < 24.000 B.

## 6. Lacunas e riscos (o numero corrige a frase)
1. Secao 0 (bloqueante).
2. **Nao testado por execucao** (proibido): a logica dos blocos so' foi conferida por leitura, `pyflakes`, `sh -n` e contagem de placeholders. Testei, isoladamente e fora dos derivados, a funcao `quer` de selecao de passos (ok) e as expressoes regulares sobre os alvos reais (leitura).
3. Erratas CR-05 (2,95σ do neutrino no Atlas, no artigo e em `neutrino_m2.values`), CR-06 (Weinberg-Witten), CR-13 (CMB-S4) e CR-10 (parametros nomeados) **nao estao nas superficies desta cadeia**: so' a R3 do neutrino entra no mapa (ANOTACAO). Elas pertencem aos registros do um.py (R-series) que a gerencia esta escrevendo; se for para o Atlas/artigo, acrescentar a `superficies_v392.py`.
4. A errata de Coulomb no `tgl_paper_unified.py` (registro que o le por hash) e no "Custo" do espelho **nao e' desta cadeia**; no `Haja_Luz\CLAUDE.md` entra (2 erratas).
5. `um_absoluto_forma_canonica.md`, `um_absoluto_pt/en.txt` (regenerados pelo rito) e o README do espelho (custodia) NAO levam errata CR-08 aqui; o `HANDOFF_v391` nao traz a frase (M01: 0).
6. O passo 13 copia o inventario regenerado para `memory\` (com backup): e' leitura minha do "regenerar com work\inventario_bancada"; se a gerencia quiser so' regenerar em `work\`, tirar o laco `for f in INVENTARIO_*` do `.sh` (no `derivar_cadeia_v392.py`, bloco `STEP11_14`).
7. O passo 14 (`construir.py`) le o mapa: rodar de novo depois do registro, se o registro vier depois.
8. `fechar_v392.py` assume o contrato dos recibos de servico descrito em 4; o `fechar` imprime exatamente o que falta.
9. `AVISO_GERENCIA.md` e' compartilhado com o Codex: so' recebe o aviso com `V392_AVISO_REIVINDICACAO`; sem ela o passo 9 imprime "PULADO" (nao e' falha).
10. A cadeia nao apaga nada, nao restaura nada, nao faz commit/push; os backups `.bak_<STAMP>_sup392`, `_p392`, `_errata_v392`, `_f392` ficam ao lado.
