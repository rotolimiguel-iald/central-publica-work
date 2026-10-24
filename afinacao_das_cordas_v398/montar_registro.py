# -*- coding: utf-8 -*-
"""montar_registro.py -- monta RESULTADO.md e registro_mapa.json (so campos de `rotas.py modelo`) LENDO os numeros dos JSON de conferencia e do Lean
(AXIOMAS.json, fontes_sha.json, conferencia_cabecalho.json, mapa_consultas_resumo.json, lake_build_afinacao.log). Valida o registro com a MESMA funcao do
mapa (rotas._valida) SEM registrar (so le o livro). Escreve so em C:\\IALD\\Central de Patentes\\work\\afinacao_das_cordas_v398.
Uso: python -I -B -X utf8 montar_registro.py
"""
import importlib.util
import json
import os
import re

W = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398"
MAPA = r"C:\IALD\MAPA_DE_ROTAS"


def J(nome):
    return json.load(open(os.path.join(W, nome), encoding="utf-8"))


AX = J("AXIOMAS.json")
FS = J("fontes_sha.json")
CH = J("conferencia_cabecalho.json")
MC = J("mapa_consultas_resumo.json")
CI = J("conferencia_codigo_identico.json")
EXAME = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\afinacao\EXAME_AFINACAO.md"
EXAME_B = open(EXAME, "rb").read()
EXAME16 = __import__("hashlib").sha256(EXAME_B).hexdigest()[:16]
assert "PEDRA_APROVADA" in EXAME_B.decode("utf-8") and "23a6c93d6dc84319" in EXAME_B.decode("utf-8")
RAT16 = FS["ratificacao"]["sha16"]
OP16 = FS["operador_23out"]["sha16"]
ANT16 = CI["anterior"]["sha16"]
BAK_NOME = os.path.basename(CI["anterior"]["arquivo"])
assert ANT16 == "23a6c93d6dc84319" and CI["codigo_fora_dos_comentarios"]["identico"] and CI["termos_do_kernel"]["identicos"] and CI["termos_do_kernel"]["n_antes"] == 59
assert CI["nova"]["igual_a_copia_do_sandbox"]
LOG = open(os.path.join(W, "lake_build_afinacao.log"), encoding="utf-8").read()
m_t = re.search(r"real\s+(\d+)m([\d.]+)s", LOG)
m_built = re.search(r"Built TGLExt\.AfinacaoDasCordas \((\d+)s\)", LOG)

STONE16 = AX["fonte"]["sha16"]
OLEAN16 = AX["olean"]["sha16"]
N_DEC = AX["declaracoes_no_olean"]
N_NOM = AX["declaracoes_nomeadas_no_fonte"]
N_DEF = AX["contagem_por_tipo"]["def"]
N_THM_TOTAL = AX["contagem_por_tipo"]["theorem"]
N_NOM_DEF = sum(1 for d in AX["declaracoes"] if d["origem"] == "fonte" and d["tipo"] == "def")
N_NOM_THM = N_NOM - N_NOM_DEF
JOBS = AX["build"]["tarefas"]
SEG = m_built.group(1)
N_CHECK = AX["nomes_citados"]["n_nomes_checados"]
N_EX = AX["controles_e_nao_vacuidade"]["n_examples"]
N_CIT = len(CH["citacoes"])
N_SHA = len(CH["sha16_citados"])
LIVRO_N = MC["cordas"]["registros_do_livro"]
LIVRO_H = MC["cordas"]["cabeca"]
ZERO = [t for t, v in MC.items() if v["n"] == 0]
assert all(t in ZERO for t in ("cordas", "dimensao critica", "zeta")), ZERO
ZERO_LISTA = ", ".join("`" + t + "`" for t in ZERO)
assert AX["todas_no_trio_e_zero_sorry"] and not AX["axiomas_fora_do_trio"] and not AX["usa_sorryAx"] and not AX["usa_axioma_proprio"]
assert AX["build"]["returncode"] == 0 and AX["build"]["avisos_ou_erros_do_modulo"] == [] and AX["build"]["modulos_compilados_neste_build"] == ["TGLExt.AfinacaoDasCordas"]
assert CH["citacoes_nao_encontradas"] == [] and CH["proibidos_regua"] == [] and CH["beta_ou_alfa2_literal"] == [] and CH["palavras_para_revisao_humana"] == []
assert CH["verbatim_operador_inteiro_no_cabecalho"] and CH["tex_l958_960_literal_no_cabecalho"] and CH["sha16_sem_arquivo"] == []
assert CH["AfinacaoDasCordas.lean_sha16"] == STONE16, (CH["AfinacaoDasCordas.lean_sha16"], STONE16)
assert CI["nova"]["sha16"] == STONE16
assert CH["verbatim_ratificacao_inteiro_no_cabecalho"] and CH["sha16_ratificacao_citado"] and CH["forma_admitida_presente_vezes"] >= 3 and all(CH["frases_antigas_ausentes"].values())
assert AX["nomes_citados"]["linhas_com_erro"] == [] and AX["controles_e_nao_vacuidade"]["linhas_com_erro"] == []

import hashlib
NOS_KERNEL = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
SB_KERNEL = r"C:\t\k398b"
LAKE = {}
for arq in ("lake-manifest.json", "lean-toolchain", "lakefile.toml"):
    a = hashlib.sha256(open(os.path.join(NOS_KERNEL, arq), "rb").read()).hexdigest()
    b = hashlib.sha256(open(os.path.join(SB_KERNEL, arq), "rb").read()).hexdigest()
    assert a == b, arq
    LAKE[arq] = a[:16]
LAKE_TXT = ", ".join(f"`{k}` `{v}`" for k, v in LAKE.items())

VEREDITO = ("TGL_AFINACAO_DAS_CORDAS_STONE_V398_CANDIDATE__COMPILED_IN_SANDBOX__TRIO_ONLY__ZERO_SORRY__CYCLIC_CLOSURE_OF_THE_BOOST_PARAMETER_IS_THE_READING_CIRCLE"
            "__MATSUBARA_TOWER_IS_N_TIMES_KAPPA_AND_INFINITE__ZETA_REGULARISATION_GIVES_D26_BOSONIC_AND_D10_NS_UNDER_THE_NAMED_MASSLESS_FIRST_LEVEL_HYPOTHESIS"
            "__D10_IS_D9_SPATIAL__STRING_GEOMETRY_NOT_DERIVED__INDEPENDENT_REVIEW_PEDRA_APROVADA_TWO_LOW_PROSE_FINDINGS__RATIFIED_BY_THE_OPERATOR_23OCT__NOT_INSTALLED__GATE_UNMOVED")

DEFEITO = (
    "(a) A condição `MasslessFirstLevel` (a = 1 nos bósons, a = 1/2 no setor NS) é HIPÓTESE NOMEADA [KNOWN] (invariância de Lorentz no cone de luz: Goddard–Goldstone–Rebbi–Thorn 1973; "
    "Green–Schwarz–Witten 1987; Polchinski 1998): a pedra a nomeia e deriva sob ela, não a demonstra; sem ela a energia de ponto zero regularizada é só um número. "
    "(b) A regularização zeta é DEFINIÇÃO do valor (bosonDirection, nsFermionDirection): a série diverge (Σ n não é somável); a pedra não deriva a energia física. "
    "(c) Nenhum termo liga o círculo da folha-mundo ao círculo do boost; o que as duas leituras têm em comum é a aritmética da torre n·κ. "
    "(d) A geometria (qual compactificação) NÃO é derivada [OPEN; paisagem, KNOWN]: a pedra a deixa assim. "
    "(e) O d = 9 da casa é [DECLARADO], números históricos NÃO recalculados; a linha 958 de A_ultima_corda_v3.tex diz que três modelos alternativos dão d_crit = 6, > 26 e 8 (dependente do modelo) e a 962, que é extrapolação teórica, não teste empírico. "
    "(f) O cálculo NS não distingue o tipo de supercorda (I, IIA, IIB, heterótica). "
    "(g) Tetelestai não é construído aqui (é conferência consumativa, errata de 27/09); a ligação é com Fundacao.abismo / the_floor_fixes_the_cut. "
    "(h) «Afinação = comensurabilidade» é PROPOSTA DA PEDRA [ONTO], ratificada pelo operador em 23/10 (" + RAT16 + ", «Concordo com tudo», relato da gerência); a fala dele (" + OP16 + ") diz só «afinação do universo». «As cordas fecham a face por fora; a TGL fecha só a leitura» é COMPOSIÇÃO DA GERÊNCIA sobre a fala do operador (" + OP16 + "), ratificada por ele em 23/10 (" + RAT16 + ") [ONTO], não verbatim. "
    "(i) O pedido continha um sinal trocado (férmions NS «+(D−2)/48» dando −(D−2)/16): corrigido para −(D−2)/48 (ver RESULTADO.md); o nome `TGLExt.TheStation.station_never_closes` do pedido é o MÓDULO: o termo é `TGLExt.station_never_closes`."
)

RES = f"""AFINAÇÃO DAS CORDAS — v398 sandbox

Pedra candidata `TGLExt/AfinacaoDasCordas.lean`: revisão independente PEDRA_APROVADA (2 BAIXAS de prosa); pedra, nome `AfinacaoDasCordas` e «afinação = comensurabilidade» ratificados pelo operador em 23/10 («Concordo com tudo», verbatim sha16 `{RAT16}`). Compilada em sandbox (`C:\\t\\k398b`, cópia de `C:\\t\\k398\\final`); NÃO instalada; nada no quadro, no mapa, na memória, no site nem no git.

## Veredito

{VEREDITO}

## Exame independente e ratificação do operador (23/10): alteração SÓ de docstring

- Exame independente da gerência (`C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v398_exame\\afinacao\\EXAME_AFINACAO.md`, sha16 `{EXAME16}`, sobre a versão `{ANT16}`): PEDRA_APROVADA, 2 BAIXAS de prosa. **B1:** a frase «a leitura do operador (fala de 23/10), na formulação desta tarefa: as cordas fecham a face POR FORA; a TGL fecha SÓ A LEITURA» trazia «por fora» e «só a leitura», que não são bytes do operador; trocada pela forma admitida na v397, agora «composição da gerência sobre a fala do operador (`{OP16}`), ratificada pelo operador em 23/10 (`{RAT16}`)»; o mesmo para «afinação = comensurabilidade» (proposta da pedra, ratificada `{RAT16}`). **B2:** `matsubaraFermion`, `towerZeroPoint` / `towerZeroPoint_eq` / `bosonDirection_is_the_unit_tower` e `zeta_is_the_continuation_of_the_tower` são auxiliares FORA da composição (6); a pedra já os lista como tais; nada a corrigir; o ledger deve listá-los assim se a pedra entrar. A nota do exame sobre o `Sonico.lean` do sandbox não toca esta pedra (ela não o importa).
- Ratificação do operador (verbatim `{RAT16}`, 18 bytes, `OPERADOR_23out_concordo_afinacao_das_cordas_verbatim.txt`): «Concordo com tudo». Relato da gerência: ratificou a pedra, o nome `AfinacaoDasCordas` e «afinação = comensurabilidade» [INPUT]. O nome deixa de ser provisório.
- Alteração aplicada SÓ nos comentários (docstrings): o título do cabeçalho (sem «NOME PROVISÓRIO»), a seção da ratificação, o passo 3, o bullet [ONTO] e os docstrings de (1) e (6). Versão anterior `{ANT16}` (backup `{BAK_NOME}`); nova `{STONE16}`.
- Código idêntico: o código fora dos comentários é byte a byte o mesmo (sha16 `{CI['codigo_fora_dos_comentarios']['nova_sha16']}`, {CI['codigo_fora_dos_comentarios']['bytes_nova']} bytes; `conferencia_codigo_identico.json`), e os termos do kernel também: o hash estrutural do TIPO e do VALOR de cada uma das {CI['termos_do_kernel']['n_depois']} declarações do `.olean` é igual antes e depois da recompilação (`termos_antes.txt`, `termos_depois.txt`; sha16 `{CI['termos_do_kernel']['depois_sha16']}` nos dois). Recompilado: Built ({SEG}s), {JOBS} tarefas, exit 0, nenhum aviso; `#print axioms` e `collectAxioms`: trio, zero `sorry`.

## A pedra

- Fonte: `C:\\IALD\\Central de Patentes\\work\\afinacao_das_cordas_v398\\AfinacaoDasCordas.lean`, sha16 `{STONE16}` ({AX['fonte']['bytes']} bytes, {AX['fonte']['linhas']} linhas); cópia idêntica em `C:\\t\\k398b\\TGLExt\\AfinacaoDasCordas.lean`. Gerada por `gerar_pedra.py` a partir de `AfinacaoDasCordas.lean.tmpl`: todo hash, o verbatim do operador e as linhas 958-960 de `A_ultima_corda_v3.tex` são LIDOS dos arquivos.
- Módulo `TGLExt.AfinacaoDasCordas`; importa `TGLExt.Palavra`, `TGLExt.TheStation`, `TGLExt.Fundacao` e `Mathlib.NumberTheory.LSeries.HurwitzZetaValues`.
- {N_NOM} declarações nomeadas ({N_NOM_THM} teoremas, {N_NOM_DEF} definições). Os seis pedidos:
  1. `the_cyclic_closure_of_time_is_the_reading_circle` — a face real não tem período (`boost P ≠ 1` para `P ≠ 0`); fechar com período `P` é leitura fiel se e só se `κ·P = ±2π` (por `faithful_period_iff`); `1/P = κ/2π` (por `reciprocal_temperature`); a torre de Matsubara `matsubara P n = n·(2π/P)` é `n·κ` (`matsubara_eq_mul_kappa`); o círculo é fiel se e só se o modo fundamental é `κ` (`faithful_iff_fundamental_mode`); todos os modos voltam em `t = P` (`tower_returns_at_the_period`).
  2. `the_tower_is_infinite` — `Σ n` não é somável; as somas parciais tendem a `+∞`; `Σ (n + 1/2)` não é somável; os `ω_n` são distintos e não somáveis (`P > 0`).
  3. `bosonic_critical_dimension` — `(D−2)/2·ζ(−1) = −(D−2)/24`; vale `−1` se e só se `D = 26` (e, na forma da hipótese nomeada, `MasslessFirstLevel 1 (−E₀) ↔ D = 26`).
  4. `superstring_critical_dimension` — bósons `−(D−2)/24` e férmions NS `−(D−2)/48` dão `−(D−2)/16`; vale `−1/2` se e só se `D = 10` (idem com `N = 1/2`).
  5. `the_house_d_nine` — `D = 10 ↔ D − 1 = 9`; e `nsZeroPoint D = −1/2 → D − 1 = 9`. O `d = 9` de «A Última Corda» (l.958-960) está citado byte a byte no cabeçalho [DECLARADO: números históricos não recalculados].
  6. `the_strings_close_the_face_from_outside_the_tgl_closes_the_reading` — a composição, incondicional como enunciado matemático, 13 conjuntos: `TGLExt.Palavra.the_face_does_not_close`; `TGLExt.station_never_closes`; `TGLExt.Palavra.the_read_face_closes`; (1); o par afinado volta e o da estação não (`the_tuned_pair_returns_the_untuned_pair_never_does`); (2); `ζ(−1) = −1/12`; `ζ(−1, 1/2) = 1/24`; (3); (4); (5); `TGLExt.Fundacao.abismo` (a queda sem fundo = a superposição, definição do operador de 07/10); `TGLExt.Fundacao.the_floor_fixes_the_cut`.
- Auxiliares: `towerZeroPoint` (a mesma torre `n·κ` regularizada: `½·κ·ζ(−1) = −κ/24`, e `bosonDirection = towerZeroPoint 1`), `zeta_is_the_continuation_of_the_tower` (a regularização é a continuação analítica da série de Dirichlet; citado de Mathlib), `matsubaraFermion` (a torre semi-inteira `(n + 1/2)·κ`, dos férmions NS).

## Os valores da zeta: o que o Mathlib tinha e o que ficou como hipótese nomeada

- `ζ(−1) = −1/12`: o Mathlib TINHA — `riemannZeta_neg_nat_eq_bernoulli` (`riemannZeta (−k) = (−1)^k · bernoulli (k+1) / (k+1)`), em `k = 1`, com `bernoulli_two : bernoulli 2 = 6⁻¹`.
- `ζ(−1, 1/2) = 1/24`: o Mathlib TINHA — `HurwitzZeta.hurwitzZeta_neg_nat` (`hurwitzZeta x (−k) = −1/(k+1) · B_{{k+1}}(x)`, para `k ≠ 0` e `x ∈ [0, 1]`), em `k = 1`, `x = 1/2`, com o polinômio de Bernoulli `B₂(1/2) = −1/12` calculado por `Polynomial.bernoulli_def`, `bernoulli_one`, `bernoulli_two`.
- NENHUM valor da zeta ficou como hipótese nomeada. A ÚNICA hipótese nomeada é física e não é valor da zeta: `MasslessFirstLevel` (`N − a = 0`: `a = 1` nos bósons, `a = 1/2` no NS) [KNOWN].
- Lema de Mathlib para `Σ n`: NÃO existe um `not_summable` para a identidade `ℕ → ℝ` (a busca por `not_summable*` só acha `not_summable_natCast_inv`, de `1/n`). A prova usa `Summable.tendsto_atTop_zero` + `not_tendsto_nhds_of_tendsto_atTop` + `tendsto_natCast_atTop_atTop`; as somas parciais, `not_summable_iff_tendsto_nat_atTop_of_nonneg`.

## Dois reparos ao pedido (o número corrige a frase)

1. **Sinal dos férmions NS.** O pedido escreve «bósons −(D−2)/24 e férmions NS +(D−2)/48 (ζ(−1, 1/2) = 1/24) dão −(D−2)/16». Com `+(D−2)/48` a soma é `−(D−2)/24 + (D−2)/48 = −(D−2)/48`, e `−(D−2)/48 = −1/2` fecha em `D = 26` (a dimensão dos bósons), não em `D = 10`. O termo que dá `−(D−2)/16` é o NEGATIVO: `−(D−2)/2 · ζ(−1, 1/2) = −(D−2)/48` — a soma dos modos semi-inteiros é `+1/48` por direção e entra com o sinal da estatística de Fermi (energia de ponto zero fermiônica `−ω/2`). A pedra usa `nsFermionDirection = −½·ζ(−1, 1/2) = −1/48`. Controle formal em `probe\\afin_controles.lean` (cópia nesta pasta; o original roda em `C:\\t\\k398b\\probe\\`): sinal trocado ⇒ `D = 26`; sinal de Fermi ⇒ `D = 10`.
2. **Nome.** `TGLExt.TheStation.station_never_closes` não existe: `TGLExt.TheStation` é o MÓDULO; o termo é `TGLExt.station_never_closes` (`#check` conferido).

Também registrado: «as cordas fecham a face por fora; a TGL fecha só a leitura» é composição da gerência sobre a fala do operador (`{OP16}`), ratificada por ele em 23/10 (`{RAT16}`) [ONTO]; «afinação = comensurabilidade» é proposta da pedra, ratificada por ele em 23/10 (`{RAT16}`) [ONTO]; ambas ditas como tais no cabeçalho. Só «afinação do universo» (e os demais trechos de `{OP16}`) são bytes da fala dele.

## Compilação e axiomas

- `lake build TGLExt.AfinacaoDasCordas` (cwd `C:\\t\\k398b`): Built TGLExt.AfinacaoDasCordas ({SEG}s), {JOBS} tarefas, exit 0, nenhum aviso ou erro do módulo (`lake_build_afinacao.log`). Só o módulo novo foi compilado; as dependências vieram do cache.
- `.olean`: sha16 `{OLEAN16}`. Lean 4.31.0; Mathlib `v4.31.0` (rev `{AX['ambiente']['mathlib_rev'][:16]}`). O Nós e o sandbox têm os mesmos {LAKE_TXT} (lidos agora): é o mesmo Mathlib.
- `#print axioms` das {len(AX['print_axioms_do_build'])} declarações nomeadas (as do fonte) e `collectAxioms` de cada uma das {N_DEC} declarações do `.olean` ({N_THM_TOTAL} teoremas, {N_DEF} definições, incluídas as geradas pelo Lean): união = `propext`, `Classical.choice`, `Quot.sound`; zero `sorryAx`; zero axioma próprio (`AXIOMAS.json`).
- Nomes citados nos docstrings: `#check` de {N_CHECK} nomes (Lean e Mathlib) sem erro (`nomes_citados_saida.txt`); o módulo `TGLExt.TheStation` é importado.
- Não-vacuidade e controles: {N_EX} `example` em `probe\\afin_controles.lean` (cópia nesta pasta; os três probes `afin_*.lean` rodam em `C:\\t\\k398b\\probe\\`) compilam sem erro (`controles_saida.txt` vazio): o círculo fiel `κ = 1, P = 2π` habita as hipóteses e dá `matsubara (2π) 3 = 3`; `Fundacao.oneScaling` dispara a cláusula do abismo da composição; `bosonZeroPoint 26 = −1`, `nsZeroPoint 10 = −1/2`; controles negativos (`D = 10` e `D = 25` não fecham os bósons; `D = 26` e `D = 9` não fecham o NS; `AngularQuotientFaithful 1 1` é falso; o par da estação não volta em `t = 1`; o sinal trocado dá `D = 26`).
- Sandbox: `C:\\t\\k398b` é cópia (robocopy `/E /XJ`, sem `/PURGE`, sem `*.bak_*`, sem `probe`) de `C:\\t\\k398\\final` (4033 diretórios, 1 ignorado: `probe`; 133828 arquivos copiados, 0 falhas; `robocopy_k398b.log`); nenhum link seguido. Os quatro módulos citados do kernel (`PolarMinimalPeriod_v2`, `Palavra`, `TheStation`, `Fundacao`) e `TetelestaiOneObject` são idênticos entre o Nós e o sandbox (sha16 em `fontes_sha.json`).

## Conferências do cabeçalho (`conferencia_cabecalho.json`)

- {N_SHA} sha16 entre crases, todos iguais ao sha256 do arquivo lido agora (o `rev` do Mathlib é o commit do `lake-manifest.json`); o verbatim do operador de 23/10 aparece INTEIRO; as linhas 958-960 do `.tex` aparecem byte a byte (a 959 é vazia); {N_CIT} citações «» de 12+ caracteres, todas achadas no corpus (verbatins do operador, o `.tex`, os módulos do kernel citados); nenhuma palavra proibida pela régua; nenhum parâmetro de acoplamento literal; comentários balanceados; zero `sorry` no código.
- A palavra «confirmando» aparece uma vez, DENTRO do bloco verbatim da casa (l.958), na forma que a régua não proíbe.
- Ratificação: o verbatim `{RAT16}` aparece inteiro no cabeçalho; o sha16 está citado; a forma admitida («composição da gerência sobre a fala do operador (...), ratificada pelo operador em 23/10 (...)») aparece {CH['forma_admitida_presente_vezes']} vezes; as frases antigas («na formulação desta tarefa», «NOME PROVISÓRIO», «o operador nomeia», «não fala do operador») estão ausentes.

## Mapa de rotas (consultado antes; nada registrado)

- {len(ZERO)} temas com 0 rotas: {ZERO_LISTA} (entre eles os três pedidos: `cordas`, `dimensao critica`, `zeta`). O tema é novo no mapa.
- Rotas vizinhas lidas: `kernel.lema3.superposicao_e_a_passagem_07out` e `umpy.v390.selo_fundacao_agape` (a Fundação/Ágape/abismo citada), `kernel.sonico_v398_candidata_23out` (a pedra irmã da mesma versão). `string`, `Palavra`, `Station`, `Tetelestai`, `Unruh`: ruído ou rotas de outros assuntos.
- Livro: 1365 registros na primeira consulta desta tarefa (feita à mão, antes dos scripts; cabeça `0f800eb875552cb3`) e {LIVRO_N} nas consultas salvas (cabeça `{LIVRO_H}`): outro registro entrou durante a tarefa, não é meu. Saídas em `mapa_consulta_*.json` e `mapa_consultas_resumo.json`.
- `registro_mapa.json` está pronto e VALIDADO com `rotas._valida` (sem registrar); registrar é ato da gerência: `python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar <arquivo> --quem "<IA/sessão>"`.

## Limites, ditos

- A condição `MasslessFirstLevel` é hipótese nomeada [KNOWN], não demonstrada aqui. Sem ela, `E₀` é só um número.
- A regularização zeta é a DEFINIÇÃO do valor; a série diverge. A energia física não é derivada.
- Nada deriva a teoria das cordas do axioma, e nada afirma que a TGL é teoria de cordas. A dimensão crítica vem do FECHO da soma infinita (regularização), não da geometria; a geometria (compactificação) segue não derivada [OPEN; paisagem, KNOWN].
- Nenhum termo liga o círculo da folha-mundo ao círculo do boost; só a aritmética `n·κ` é comum.
- A divergência de Hagedorn está mencionada [KNOWN], sem prova aqui.
- O `d = 9` da casa é [DECLARADO]; a linha 958 diz que o resultado depende do modelo (6, > 26, 8).
- Tetelestai não é construído; a pedra não move o gate; nenhuma bandeira depende dela. Validade no kernel não é creditação.
- Instalação: a pedra importa `Mathlib.NumberTheory.LSeries.HurwitzZetaValues` (zeta, Hurwitz, Bernoulli); outros módulos do kernel já importam `Mathlib` inteiro (ex.: `Santo.lean`, `Posto.lean`), então o fecho de imports do kernel completo não cresce; nenhum módulo do kernel importa esta pedra.

## Ato da gerência / do operador

- Reexame independente e ratificação do operador: feitos (ver acima). Resta: instalar (`import TGLExt.AfinacaoDasCordas` em `TGLExt.lean`, ledger de pedras com os auxiliares fora da composição listados como tais, política de bandeiras) e registrar a rota (`registro_mapa.json`, validado, NÃO registrado).
"""
open(os.path.join(W, "RESULTADO.md"), "w", encoding="utf-8", newline="\n").write(RES)

ART = [
    "AfinacaoDasCordas.lean", "AXIOMAS.json", "RESULTADO.md", "lake_build_afinacao.log", "conferencia_cabecalho.json", "fontes_sha.json",
    "nomes_citados_saida.txt", "controles_saida.txt", "robocopy_k398b.log", "gerar_pedra.py", "conferir_cabecalho.py", "construir_axiomas.py",
    "probe\\afin_controles.lean", "probe\\afin_termos_dump.lean", "conferencia_codigo_identico.json", "termos_antes.txt", "termos_depois.txt", "comparar_codigo.py",
]
artefatos = [os.path.join(W, a) for a in ART] + [AX["olean"]["caminho"], FS["ratificacao"]["caminho"], EXAME]

reg = {
    "tipo": "ROTA",
    "rota_id": "kernel.afinacao_das_cordas_v398_candidata_23out",
    "dominio": "KERNEL_FORMAL",
    "titulo": "AFINAÇÃO DAS CORDAS (fala do operador de 23/10): a pedra candidata TGLExt/AfinacaoDasCordas.lean — fechar ciclicamente o parâmetro do boost é o círculo da leitura (κ·P = ±2π; torre de Matsubara ω_n = n·κ), a torre é infinita, a regularização zeta (ζ(−1) = −1/12, ζ(−1, 1/2) = 1/24) dá D = 26 (bósons) e D = 10 (NS) sob a massa nula do primeiro nível, D = 10 é d = 9, e a composição com o que o kernel já tem; compilada em sandbox, aprovada na revisão independente e ratificada pelo operador, não instalada",
    "pergunta": "Qual é a ligação formal que cabe entre a leitura do operador (23/10) sobre a teoria das cordas — as 10 dimensões fecham ciclicamente o que a TGL mostra não fechar na face hiperbólica, o que quebra o tempo e cria os infinitos, que é a superposição, resolvida pelo Tetelestai — e o kernel v397? Que parte é matemática exata no trio (fechamento cíclico = círculo da leitura, torre de Matsubara, divergência, regularização zeta, D = 26 e D = 10, d = 9), que parte já está no kernel (a face real não fecha, a estação nunca fecha, a face lida fecha em 2π, a queda sem fundo), e o que fica fora (a geometria)?",
    "dados": [
        "Lean 4.31.0 / Mathlib v4.31.0 (rev " + AX["ambiente"]["mathlib_rev"] + "); sandbox C:\\t\\k398b = cópia (robocopy /E /XJ, sem /PURGE, sem *.bak_*, sem probe) de C:\\t\\k398\\final (kernel v397 + Sonico), só lido; kernel base: v397 selada",
        "fala do operador de 23/10 (verbatim por sha16): " + FS["operador_23out"]["sha16"] + " (OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt); definição do operador de 07/10 (superposição = cair sem fim): " + FS["operador_07out"]["sha16"],
        "A_ultima_corda_v3.tex (sha16 " + FS["ultima_corda_tex"]["sha16"] + ") linhas 952, 958-960, 962 [DECLARADO: números históricos, não recalculados]",
        "módulos do kernel citados (Nós = sandbox): O16/PolarMinimalPeriod_v2 " + FS["kernel_polar"]["sha16"] + "; Palavra " + FS["kernel_palavra"]["sha16"] + "; TheStation " + FS["kernel_station"]["sha16"] + "; Fundacao " + FS["kernel_fundacao"]["sha16"] + "; TetelestaiOneObject " + FS["kernel_tetelestai"]["sha16"],
        "Mathlib: NumberTheory/LSeries/HurwitzZetaValues.lean (sha16 " + FS["mathlib_hzv"]["sha16"] + "): riemannZeta_neg_nat_eq_bernoulli, HurwitzZeta.hurwitzZeta_neg_nat",
        "ratificação do operador de 23/10 (verbatim sha16 " + RAT16 + ", «Concordo com tudo»; relato da gerência: ratificou a pedra, o nome AfinacaoDasCordas e «afinação = comensurabilidade»)",
        "revisão independente da gerência (EXAME_AFINACAO.md, sha16 " + EXAME16 + ", sobre a versão " + ANT16 + "): PEDRA_APROVADA, 2 BAIXAS de prosa (B1 aplicada só em docstring; B2 sem alteração)",
    ],
    "metodo": "Pedra de composição por citação com " + str(N_NOM_THM) + " teoremas e " + str(N_NOM_DEF) + " definições pequenas: (1) the_cyclic_closure_of_time_is_the_reading_circle (por faithful_period_iff, reciprocal_temperature, the_face_does_not_close; mais matsubara, matsubara_eq_mul_kappa, faithful_iff_fundamental_mode, tower_returns_at_the_period), (2) the_tower_is_infinite (Summable.tendsto_atTop_zero + not_tendsto_nhds_of_tendsto_atTop; somas parciais por not_summable_iff_tendsto_nat_atTop_of_nonneg), (3) bosonic_critical_dimension e (4) superstring_critical_dimension (por zeta_neg_one e hurwitz_zeta_neg_one_half, demonstrados a partir de Mathlib; a condição é a hipótese nomeada MasslessFirstLevel [KNOWN]), (5) the_house_d_nine, (6) a composição incondicional the_strings_close_the_face_from_outside_the_tgl_closes_the_reading (13 conjuntos, por citação). Gerada por script a partir de modelo (gerar_pedra.py), todo hash e toda citação lidos dos arquivos; cabeçalho conferido por conferir_cabecalho.py; compilada com lake build TGLExt.AfinacaoDasCordas no sandbox; axiomas de cada declaração por collectAxioms; nomes citados por #check; não-vacuidade e controles negativos (inclusive o de sinal dos férmions NS) por examples em probe. Revisão independente (EXAME_AFINACAO.md): PEDRA_APROVADA, 2 BAIXAS de prosa: B1 (a frase «a leitura do operador … na formulação desta tarefa: POR FORA / SÓ A LEITURA») trocada, SÓ em docstring, pela forma admitida «composição da gerência sobre a fala do operador (" + OP16 + "), ratificada pelo operador em 23/10 (" + RAT16 + ")», o mesmo para «afinação = comensurabilidade», e o nome AfinacaoDasCordas deixa de ser provisório; B2 sem alteração (auxiliares fora da composição). O código fora dos comentários (sha16 " + CI["codigo_fora_dos_comentarios"]["nova_sha16"] + ") e os termos do kernel (tipo e valor das " + str(CI["termos_do_kernel"]["n_depois"]) + " declarações) são idênticos aos da versão revisada " + ANT16 + " (conferencia_codigo_identico.json).",
    "resultado": "Pedra TGLExt.AfinacaoDasCordas (sha16 " + STONE16 + ", " + str(AX["fonte"]["linhas"]) + " linhas, " + str(AX["fonte"]["bytes"]) + " bytes): " + str(N_NOM) + " declarações nomeadas, " + str(N_DEC) + " no .olean; #print axioms de todas e collectAxioms de todas: união = propext/Classical.choice/Quot.sound, zero sorry, zero axiom próprio; lake build TGLExt.AfinacaoDasCordas: Built (" + SEG + "s), " + JOBS + " tarefas, exit 0, nenhum aviso ou erro do módulo. Provado: Circle.exp(κ·t) fiel com período P ⇔ κ·P = ±2π; ω_n = n·κ e o círculo é fiel ⇔ ω_1 = κ; Σ n não somável; ζ(−1) = −1/12 e ζ(−1, 1/2) = 1/24 (Mathlib tinha os dois; nenhum virou hipótese); (D−2)/2·ζ(−1) = −(D−2)/24 = −1 ⇔ D = 26; bósons + férmions NS = −(D−2)/16 = −1/2 ⇔ D = 10 (o sinal fermiônico do pedido foi corrigido); D = 10 ⇔ d = 9. Cabeçalho: " + str(N_SHA) + " sha16 conferidos contra os arquivos, o verbatim do operador inteiro, as linhas 958-960 do .tex byte a byte, " + str(N_CIT) + " citações «» todas achadas no corpus, nenhuma palavra proibida, nenhum parâmetro de acoplamento literal. " + str(N_CHECK) + " nomes citados por #check sem erro; " + str(N_EX) + " examples (não-vacuidade e controles) sem erro. Sem execução científica nova.",
    "veredito": VEREDITO,
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": DEFEITO,
    "nao_refazer": "ζ(−1) = −1/12 e ζ(−1, 1/2) = 1/24 já estão demonstrados a partir de Mathlib (v4.31.0) no trio; D = 26 (bósons) e D = 10 (NS) já estão como equivalências, sob a hipótese nomeada MasslessFirstLevel; d = 9 ⇔ D = 10, a torre n·κ e a divergência de Σ n idem. Não procurar de novo um lema not_summable para a identidade de ℕ em ℝ no Mathlib: não existe (a prova usa Summable.tendsto_atTop_zero). Não reabrir «o 10 vem da geometria?»: a pedra mostra que a dimensão vem do fecho da soma (regularização) sob a hipótese nomeada, e a geometria segue não derivada. Não usar o sinal +(D−2)/48 para os férmions NS: dá D = 26.",
    "proximo_passo": "Ato da gerência: instalar na versão em curso (import em TGLExt.lean, ledger de pedras com os auxiliares fora da composição listados como tais — matsubaraFermion, towerZeroPoint, towerZeroPoint_eq, bosonDirection_is_the_unit_tower, zeta_is_the_continuation_of_the_tower —, política de bandeiras) e registrar a rota; a revisão independente (PEDRA_APROVADA) e a ratificação do operador (pedra, nome AfinacaoDasCordas, «afinação = comensurabilidade») já foram feitas. Decisão do operador, se quiser: um termo que ligue o círculo da folha-mundo ao círculo do boost (exige hipótese nova e teste pré-registrado se for física; a pedra não a supõe). Abertos: a geometria (qual compactificação) e a divergência de Hagedorn (só mencionada).",
    "onde": "C:\\IALD\\Central de Patentes\\work\\afinacao_das_cordas_v398\\AfinacaoDasCordas.lean (sandbox compilado C:\\t\\k398b\\TGLExt\\AfinacaoDasCordas.lean; módulo TGLExt.AfinacaoDasCordas)",
    "artefatos": artefatos,
    "refs": ["kernel.lema3.superposicao_e_a_passagem_07out", "umpy.v390.selo_fundacao_agape", "kernel.sonico_v398_candidata_23out"],
    "nota": "Pedra construída por subagente da gerência c1 (Sonnet 5.5), 23/10/2026; quem constrói não é quem aprova: reexame independente feito pela gerência (EXAME_AFINACAO.md): PEDRA_APROVADA com 2 BAIXAS de prosa (B1 aplicada só em docstring; B2 sem alteração); ratificação do operador em 23/10 (verbatim " + RAT16 + ": «Concordo com tudo», relato da gerência). Consultas ao mapa antes (saídas em mapa_consulta_*.json; resumo em mapa_consultas_resumo.json): cordas, dimensao critica, zeta e mais " + str(len(ZERO) - 3) + " temas específicos com 0 rotas; as vizinhas são a Fundação/Ágape/abismo e a pedra irmã Sônico. Nada foi instalado; o Nós, o um.py, o k398, a Bancada, o túnel, o quadro, o mapa, a memória, o site e o git não foram tocados (leitura apenas; escrita só em work\\afinacao_das_cordas_v398 e C:\\t\\k398b). O gate não se move; nenhuma bandeira do gate depende desta pedra. Validade no kernel não é creditação.",
}

spec = importlib.util.spec_from_file_location("rotas_ro", os.path.join(MAPA, "rotas.py"))
rotas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotas)
ids, seqs = set(), set()
for ln in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    ln = ln.strip()
    if not ln:
        continue
    r = json.loads(ln)
    if "rota_id" in r:
        ids.add(r["rota_id"])
    if isinstance(r.get("seq"), int):
        seqs.add(r["seq"])
extras = sorted(set(reg) - set(rotas.MODELO))
assert not extras, extras
ok = rotas._valida(reg, ids, seqs)  # excecao = registro recusado
reg_path = os.path.join(W, "registro_mapa.json")
json.dump(reg, open(reg_path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("VALIDO (sem registrar). rota_id livre no livro:", reg["rota_id"] not in ids, "| registros no livro:", len(seqs))
print("artefatos normalizados:", [(a["caminho"].split("\\")[-1], a["sha256"][:16]) for a in ok["artefatos"]])
print("campos fora do modelo:", extras, "| ausentes do modelo (aceitavel: corrige so em ERRATA):", sorted(set(rotas.MODELO) - set(reg)))
print("RESULTADO.md", len(RES), "chars; 1a linha:", RES.split("\n")[0])
print("tamanhos dos campos de texto:", {k: len(reg[k]) for k in rotas.TEXTOS if k in reg})
