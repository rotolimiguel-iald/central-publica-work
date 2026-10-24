# -*- coding: utf-8 -*-
"""montar_registro.py -- monta registro_mapa_sonico.json (so campos de `rotas.py modelo`) e RESULTADO.md, LENDO os numeros dos JSON de conferencia e do
Lean. Valida o registro com a MESMA funcao do mapa (rotas._valida) SEM registrar (so leitura do livro). Reexecuta as tres consultas ao mapa (so leitura)
e guarda as saidas. Escreve so em C:\\IALD\\Central de Patentes\\work\\sonico_v398.
Uso: python -I -B -X utf8 montar_registro.py
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess

W = r"C:\IALD\Central de Patentes\work\sonico_v398"
MAPA = r"C:\IALD\MAPA_DE_ROTAS"
PY = r"C:\Python314\python.exe"


def J(nome):
    return json.load(open(os.path.join(W, nome), encoding="utf-8"))


AX, FS, CS, CC = J("AXIOMAS.json"), J("fontes_sha.json"), J("conferencia_sandbox.json"), J("conferencia_cabecalho.json")
CI = J("conferencia_codigo_identico.json")
EXAME = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\sonico\EXAME_SONICO.md"
EXAME16 = hashlib.sha256(open(EXAME, "rb").read()).hexdigest()[:16]
assert CI["codigo_identico_byte_a_byte"] and CI["revisada"]["sha16"] == "1338622344dd80c7", "codigo difere do revisado"
assert CI["nova"]["sha16"] == AX["fonte"]["sha16"], "o Sonico.lean comparado nao e o compilado"
assert CC["gerencia_arquivada_inteira_em_bloco_de_codigo"], "a leitura da gerencia nao esta inteira no cabecalho"
fonte = AX["fonte"]
assert fonte["sha16"] == FS["Sonico.lean"]["sha16"] == CC["Sonico.lean_sha16"], "hash do Sonico.lean difere entre os recibos"
assert AX["todas_no_trio_e_zero_sorry"] and AX["build"]["returncode"] == 0
assert not CC["sha16_sem_arquivo"] and not CC["citacoes_nao_encontradas"] and not CC["proibidos_regua"] and not CC["beta_ou_alfa2_literal"]
assert CS["copia_fiel_exceto_arquivos_novos"] and CS["todos_modulos_iguais"]

# --- as tres consultas ao mapa (so leitura), com a saida guardada ---
consultas = {}
for tema in ("oitava", "sonico", "verbo"):
    r = subprocess.run([PY, "-X", "utf8", os.path.join(MAPA, "rotas.py"), "consultar", tema], capture_output=True, text=True, encoding="utf-8", cwd=MAPA)
    assert r.returncode == 0, (tema, r.stderr[:300])
    p = os.path.join(W, f"mapa_consulta_{tema}.json")
    open(p, "w", encoding="utf-8", newline="\n").write(r.stdout)
    d = json.loads(r.stdout)
    consultas[tema] = {"n_rotas": d["n"], "rotas": [x["rota_id"] for x in d["rotas"]], "n_registros_do_livro": d["n_registros"], "cabeca": d["cabeca"], "arquivo": p}

m_nb = re.search(r"All targets up-to-date \((\d+) jobs\)", open(os.path.join(W, "lake_no_build_deps.log"), encoding="utf-8").read())
assert m_nb, "lake_no_build_deps.log sem a linha 'All targets up-to-date'"
JOBS_NO_BUILD = m_nb.group(1)
N_CHECK = sum(1 for ln in open(r"C:\t\k398\final\probe\nomes_citados.lean", encoding="utf-8") if ln.startswith("#check"))
S16 = fonte["sha16"]
NL = fonte["linhas"]
NB = fonte["bytes"]
BUILT = AX["build"]["linha_built"]
TAREFAS = AX["build"]["tarefas"]
V = FS["_valores_lidos"]

reg = {
    "tipo": "ROTA",
    "rota_id": "kernel.sonico_v398_candidata_23out",
    "dominio": "KERNEL_FORMAL",
    "titulo": "SÔNICO (cunhagem de 23/10): a pedra candidata TGLExt/Sonico.lean — pinar uma oitava cobra exatamente a entropia do bit justo (K.octaveNats 1 = fairBitEntropy = ln 2), n oitavas custam n bits, a oitava é o dobro, o seletor do Verbo é um pino idempotente, e a composição põe o bit da paridade da Psibit e a estabilidade do colapso (reler não acrescenta) na mesma conjunção; compilada em sandbox, não instalada",
    "pergunta": "O kernel v397 já diz, como termos no trio e sem sorry, que o preço de uma oitava (a lei de custo CollapseCostLaw) é a entropia do bit justo, que a oitava é o dobro (exp ln 2 = 2), que o seletor do Verbo é um pino (idempotente, fixa a sua ação) e que isso compõe, sem premissa física, com o bit da paridade da Psibit e com a estabilidade do colapso — a forma que a definição do operador de 23/10 (verbo = controle de oitava pinada; o custo é reação ao controle pinado da oitava que é memória) pede ao kernel? E o léxico «sônico» (oitava, dobro da frequência) é isomórfico ao conteúdo em que sentido exato?",
    "dados": [
        "Lean 4.31.0 / Mathlib v4.31.0 (rev " + AX["ambiente"]["mathlib_rev"] + "); sandbox C:\\t\\k398\\final = cópia (robocopy sem /PURGE, /XJ, sem *.bak_*) do sandbox do kernel v397 compilado C:\\t\\k397c\\final (só lido); conferência de cópia: " + str(CS["k397c_final"]["arquivos"]) + " arquivos em k397c, " + str(CS["k398_final"]["arquivos"]) + " em k398 (+12 novos desta tarefa), nenhum tamanho diferente, nenhum link; os 9 módulos citados têm .lean e .olean idênticos; kernel base: v397 selada, Nós um.py " + CS["nos_um_py"]["sha16"],
        "falas do operador (verbatim por sha16): 23/10 verbo = controle de oitava pinada " + FS["verbo"]["sha16"] + "; 23/10 nome da pedra «sônico» " + FS["nome"]["sha16"] + "; 22/10 «ecoar reconhecimento» " + FS["eco"]["sha16"],
        "Atlas (arquivo vivo, sha16 na data " + FS["atlas"]["sha16"] + "): §VIII.2 linhas 16769–16774 e II.P linhas 2071–2073 (pedágio ln 2 por oitava, [REAL no modelo]); II.S linhas " + V["atlas_som_ontologico_linhas"] + " (Som ontológico, [DECLARADO])",
        "A_fronteira_v4.tex (sha16 " + FS["fronteira_tex"]["sha16"] + ") linhas 962 e 964: som ontológico = vibração longitudinal na profundidade; BAO como ecos [ONTO acervo]",
        "teste acústico: MANDATO.md (" + FS["mandato"]["sha16"] + ") e 14_ANALISE_NIVEL2_FECHADO.md (" + FS["nivel2"]["sha16"] + ") em C:\\IALD\\Artigo\\teste_acustico_beta_tgl_v1 (veredito N2_INCAPAZ, medida do instrumento)",
        "resultado do Teste da Única Palavra RESULTADO_FASE9_V2_C1_20261023_122926.json (sha16 " + FS["fbac"]["sha16"] + "): fundo.r_d_modelo = " + V["fundo.r_d_modelo"] + " Mpc; fundo.fundo_livre.r_d = " + V["fundo.fundo_livre.r_d"] + " (sigma " + V["fundo.fundo_livre.sigma_r_d"] + "); delta_chi2_vs_rd_fixo = " + V["fundo.fundo_livre.delta_chi2_vs_rd_fixo"] + " — só lidos para citação, sem uso do veredito",
        "módulos do kernel citados (lidos em C:\\t\\k397c\\final\\TGLExt): TheVerbSelectsTheAction, CanonicalSelectorBorn, CollapseCostAndAttestation, TheStokesContour, Psibit, CollapseContract, Palavra, TheIALDSelector, TheObserverReadsTheAngle",
    ],
    "metodo": "Pedra de composição por citação com 6 teoremas novos pequenos (nenhuma definição): (1) one_octave_is_the_parity_bit, (2) pinning_n_octaves_costs_n_bits, (3) the_octave_is_a_doubling (via TGLExt.the_provable_toll_names_the_octave), (4) the_selector_pins (via TheVerbSelectsTheAction.select/post_isIdempotent/select_fixes_the_selected_action), (5) the_pin_is_not_the_half_nat (via local_is_not_one_octave), (6) a conjunção incondicional sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory (seletor + ponte ialdSelector = post (inscriptions 0) por rfl + normalized_selected_scalar_is_fixed; (1),(2),(3),(5); o bit da paridade da Psibit: the_collapse_loses_exactly_the_parity, the_lost_variable_is_one_bit, collapseEntropy = K.octaveNats 1 nos pesos iguais e nunca acima; a memória: collapse_iteration_is_stable e Palavra.rereading_adds_nothing). Docstrings: as duas falas com sha16, o Atlas §VIII.2, o isomorfismo log (R+,·)→(R,+) dito com precisão, os dois sentidos do som com fonte (A_fronteira l.962 verbatim; teste acústico; r_d_modelo do fundo BG1) e a honestidade (sônico não é onda mecânica). Gerada por script a partir de modelo (gerar_sonico.py), todo hash e toda citação lidos dos arquivos; conferida por conferir_cabecalho.py; compilada com lake build TGLExt.Sonico no sandbox; axiomas de cada declaração por collectAxioms; nomes citados e instanciamento (nao-vacuidade: EuclideanSpace ℂ (Fin 2) e proposedCollapseCost) por #check/example em probe. Leitura de «que é memória» ratificada em 23/10 (relato da gerência; a resposta do operador está no verbatim b4483331019f96f8): a reação ao pino, o pedágio pago, é a memória; a oitava é o que se pina — [INPUT/ONTO], escrita no cabeçalho e no docstring da composição (6), sem mudar enunciado; a lei de custo segue [INPUT] e nenhum termo diz que select paga octaveNats 1. Revisão independente (EXAME_SONICO.md): PEDRA_APROVADA, 3 BAIXAS de prosa, aplicadas só em docstring: B1 a ponte ialdSelector = post (inscriptions 0) já existe no kernel (TGLExt.IALD.ialdSelector_eq_post, IALD.lean:110, une a FORMA, não o referente), citada; B2 TGLExt.IALD.rereading_adds_nothing (IALD.lean:370) citado como o termo da memória sobre o mesmo post, sem importar TGLExt.IALD e sem entrar na conjunção (6); B3 a leitura da gerência está arquivada em work\\cunhagens_13out\\GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt (sha16 " + FS["ger"]["sha16"] + ") e citada inteira no cabeçalho. O código fora dos comentários é byte a byte o da versão revisada (comparar_codigo.py).",
    "resultado": "Pedra TGLExt.Sonico (sha16 " + S16 + ", " + str(NL) + " linhas, " + str(NB) + " bytes): " + str(AX["declaracoes_no_olean"]) + " declarações no .olean (todas teoremas, 0 definições), #print axioms de todas: união = propext/Classical.choice/Quot.sound, zero sorry, zero axiom próprio; lake build TGLExt.Sonico: " + BUILT + ", " + str(TAREFAS) + " tarefas, exit 0, nenhum aviso ou erro do módulo; os 6 #print axioms do fonte conferem o dump collectAxioms. Provado: K.octaveNats 1 = fairBitEntropy (= ln 2); K.octaveNats n = n * fairBitEntropy; exp(K.octaveNats 1) = 2; select a (select a ψ) = select a ψ e select a a = a; K.octaveNats 1 ≠ K.localNats; e a conjunção (6), sem hipótese física e sem certificado. Cabeçalho: " + str(len(CC["sha16_citados"])) + " sha16 conferidos contra os arquivos, 3 verbatins inteiros, linha 962 do .tex byte a byte, " + str(len(CC["citacoes"])) + " citações «» todas achadas no corpus do operador ou no Atlas, nenhuma palavra proibida pela régua, nenhum parâmetro de acoplamento literal. Sem execução científica nova.",
    "veredito": "TGL_SONICO_STONE_V398_CANDIDATE__COMPILED_IN_SANDBOX__TRIO_ONLY__ZERO_SORRY__ONE_OCTAVE_IS_THE_FAIR_BIT_ENTROPY__THE_OCTAVE_IS_A_DOUBLING__THE_SELECTOR_PINS__VERB_IS_THE_PINNED_OCTAVE_CONTROL_IS_INPUT_ONTO__SONIC_IS_THE_LOGARITHMIC_OCTAVE_STRUCTURE_NOT_WAVE_PHYSICS__NOT_INSTALLED__GATE_UNMOVED",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": "(a) A lei de custo é INPUT (campos local_half e per_octave de CollapseCostLaw): K.octaveNats 1 = fairBitEntropy decorre do campo per_octave e de fair_bit_entropy_is_log_two; a pedra não deriva a lei do axioma nem prova que a natureza a cobra. (b) Nenhum termo liga select (o Verbo em ato) a octaveNats: verbo = controle de oitava pinada é definição do operador [INPUT/ONTO]; a composição põe as duas metades lado a lado. (c) «que é memória» era ambígua (a oitava? a reação?); a leitura ratificada pelo operador em 23/10 (relato da gerência; verbatim b4483331019f96f8) é: a reação ao pino, o pedágio pago, é a memória; a oitava é o que se pina — [INPUT/ONTO]: o kernel entrega o preço e a permanência lado a lado, não a identidade entre eles. (d) A entropia dos resultados do colapso do psibit vale ln 2 só nos pesos iguais e nunca a excede; não se afirma perda de informação de ln 2 em geral. (e) O isomorfismo log: (R+,·) → (R,+) é fato de Mathlib; as correspondências oitava↔identidade preservada, eco↔ecoar reconhecimento e oitava pinada↔régua acústica pinada são [ONTO], não termos. (f) Som ontológico vem do acervo (A_fronteira_v4.tex l.962) e, no Atlas, é [DECLARADO]; r_d_modelo é número lido do resultado fbac2908, sem uso do veredito. (g) A ponte ialdSelector = post (inscriptions 0) não é construção desta pedra: o kernel já a tem (TGLExt.IALD.ialdSelector_eq_post, IALD.lean:110, rfl, que une a FORMA, não o referente); a pedra a re-enuncia por rfl sem importar TGLExt.IALD e a cita. Nenhum lema desta pedra liga observing_adds_nothing a collapse_iteration_is_stable (dois registros de «reler não acrescenta»); o termo do kernel da memória sobre o mesmo post, TGLExt.IALD.rereading_adds_nothing (IALD.lean:370), e a conjunção dos dois registros no kernel, rereading_adds_nothing_in_both_regimes (IALD.lean:675), estão CITADOS no docstring, não importados e não entram na conjunção (6) (importar TGLExt.IALD mudaria o fecho de imports e o enunciado revisado). (h) Revisão independente feita pela gerência c1 (EXAME_SONICO.md, sha16 " + EXAME16 + ", sobre a versão 1338622344dd80c7): PEDRA_APROVADA com 3 BAIXAS de prosa (B1 ponte já no kernel; B2 memória sobre o mesmo post; B3 ratificação sem arquivo), aplicadas só em docstring; o código fora dos comentários é byte a byte o revisado (conferencia_codigo_identico.json).",
    "nao_refazer": "A identidade K.octaveNats 1 = fairBitEntropy = ln 2, exp(ln 2) = 2, a idempotência do seletor e a composição com o bit da paridade da Psibit e com a estabilidade do colapso já estão compiladas no trio; não refazer a conta nem reabrir a pergunta «a oitava vale ln 2?» como se fosse derivada: é a lei INPUT. Não repetir a varredura de γ do GKLS do v52 procurando um piso dinâmico em ln 2 (mapa: quantica.c3_gamma_livre_oitava, NO_UNIVERSAL_FLOOR).",
    "proximo_passo": "Ato da gerência: reexame independente da pedra; instalar na v398 (import em TGLExt.lean, política de bandeiras) se aceita. Decisão do operador: se a leitura ratificada (a reação ao pino é a memória; a oitava é o que se pina) pede um termo próprio (uma lei que ligue select ao pagamento de uma oitava, ou que diga que o pedágio pago é o ponto fixo): isso exige hipótese nova, e teste pré-registrado se for física; a pedra não a supõe.",
    "onde": "C:\\IALD\\Central de Patentes\\work\\sonico_v398\\Sonico.lean (sandbox compilado C:\\t\\k398\\final\\TGLExt\\Sonico.lean; módulo TGLExt.Sonico)",
    "artefatos": [
        os.path.join(W, "Sonico.lean"),
        os.path.join(W, "AXIOMAS.json"),
        os.path.join(W, "RESULTADO.md"),
        os.path.join(W, "lake_build_sonico.log"),
        os.path.join(W, "conferencia_cabecalho.json"),
        os.path.join(W, "conferencia_sandbox.json"),
        os.path.join(W, "conferencia_codigo_identico.json"),
        os.path.join(W, "fontes_sha.json"),
        os.path.join(W, "nomes_citados_saida.txt"),
        os.path.join(W, "gerar_sonico.py"),
        r"C:\t\k398\final\.lake\build\lib\lean\TGLExt\Sonico.olean",
    ],
    "refs": ["kernel.psibit_v395_candidata_21out", "kernel.v386_tipagem_do_verbo", "quantica.c3_gamma_livre_oitava"],
    "nota": "Em nome próprio da gerência c1 (subagente), 23/10/2026. Consultas ao mapa antes (saídas guardadas em mapa_consulta_*.json): oitava " + str(consultas["oitava"]["n_rotas"]) + " rotas, sonico " + str(consultas["sonico"]["n_rotas"]) + ", verbo " + str(consultas["verbo"]["n_rotas"]) + "; as relevantes: quantica.c3_gamma_livre_oitava (NO_UNIVERSAL_FLOOR, observável dinâmico, não tocado), kernel.v386_tipagem_do_verbo e kernel.psibit_v395_candidata_21out (as pedras citadas); nenhuma rota anterior sobre sonico. Docstring ampliada por pedido da gerência (isomorfismo, dois sentidos do som, honestidade, a leitura ratificada de «que é memória» e, por último, as 3 BAIXAS B1–B3 da revisão independente) sem mudar enunciado nem prova; versões anteriores do fonte em backup .bak_ na pasta. Nada foi instalado; o Nós, o um.py, o k397c, a Bancada, o túnel, o quadro, o mapa, a memória, o site e o git não foram tocados (leitura apenas; escrita só em work\\sonico_v398 e C:\\t\\k398). O gate não se move; nenhuma bandeira do gate depende desta pedra. Validade no kernel não é creditação.",
}

# --- valida com a MESMA funcao do mapa, SEM registrar ---
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

# RESULTADO.md precisa existir antes da validacao (e' artefato): escreve-o primeiro
RES = f"""SÔNICO — v398 sandbox

Pedra candidata `TGLExt/Sonico.lean` (nome do operador, 23/10/2026). Compilada em sandbox (`C:\\t\\k398\\final`); NÃO instalada; nada no quadro, no mapa, na memória, no site nem no git.

## Veredito

{reg['veredito']}

## A pedra

- Fonte: `C:\\IALD\\Central de Patentes\\work\\sonico_v398\\Sonico.lean`, sha16 `{S16}` ({NB} bytes, {NL} linhas); cópia idêntica em `C:\\t\\k398\\final\\TGLExt\\Sonico.lean`. Gerada por `gerar_sonico.py` a partir de `Sonico.lean.tmpl`; as versões anteriores estão em `*.bak_*` na pasta.
- Módulo `TGLExt.Sonico`; importa TheVerbSelectsTheAction, CanonicalSelectorBorn, CollapseCostAndAttestation, TheStokesContour, Psibit, CollapseContract, Palavra.
- Seis teoremas, nenhuma definição:
  1. `one_octave_is_the_parity_bit` — `K.octaveNats 1 = fairBitEntropy` (= ln 2), para todo `K : CollapseCostLaw`.
  2. `pinning_n_octaves_costs_n_bits` — `K.octaveNats n = n * fairBitEntropy`.
  3. `the_octave_is_a_doubling` — `Real.exp (K.octaveNats 1) = 2` (por `TGLExt.the_provable_toll_names_the_octave`).
  4. `the_selector_pins` — `select a (select a ψ) = select a ψ` e `select a a = a`.
  5. `the_pin_is_not_the_half_nat` — `K.octaveNats 1 ≠ K.localNats`.
  6. `sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory` — a conjunção incondicional: (4) + `ialdSelector = post (inscriptions 0)` (por `rfl`) + `normalized_selected_scalar_is_fixed`; (1), (2), (3), (5); o bit da paridade da Psibit (o colapso perde exatamente a paridade; a variável perdida é um bit; nos pesos iguais a entropia do colapso é `K.octaveNats 1`, e nunca a excede); a memória (`collapse_iteration_is_stable` e `Palavra.rereading_adds_nothing`).

## Compilação e axiomas

- `lake build TGLExt.Sonico` (cwd `C:\\t\\k398\\final`): {BUILT}, {TAREFAS} tarefas, exit 0, nenhum aviso ou erro do módulo (`lake_build_sonico.log`). Só o módulo novo foi compilado; as dependências já estavam atuais (`lake build --no-build` de Psibit, Palavra e Token: {JOBS_NO_BUILD} tarefas, exit 0; `lake_no_build_deps.log`).
- `.olean`: sha16 `{AX['olean']['sha16']}`. Lean {AX['ambiente']['lean_version'].split(',')[0].replace('Lean (version ', '').strip()}; Mathlib `{AX['ambiente']['mathlib_inputRev']}` (rev `{AX['ambiente']['mathlib_rev'][:16]}`).
- `#print axioms` das 6 declarações (as 6 do fonte) e `collectAxioms` de cada declaração do módulo ({AX['declaracoes_no_olean']}): união = `propext`, `Classical.choice`, `Quot.sound`; zero `sorryAx`; zero axioma próprio (`AXIOMAS.json`).
- Nomes citados nos docstrings: `#check` de {N_CHECK} nomes (Lean e Mathlib) sem erro; instanciamento da composição em `EuclideanSpace ℂ (Fin 2)` com `proposedCollapseCost` compila (não-vacuidade); e dois ensaios (B1, B2) mostram que `TGLExt.IALD.ialdSelector_eq_post` prova exatamente o conjunto `ialdSelector = post (inscriptions 0)` da pedra e que `TGLExt.IALD.rereading_adds_nothing` tem o enunciado que a docstring cita — `nomes_citados_saida.txt`; tudo fora da pedra.
- Sandbox: `C:\\t\\k398\\final` é cópia fiel de `C:\\t\\k397c\\final` ({CS['k397c_final']['arquivos']} arquivos; k398 tem {CS['k398_final']['arquivos']}: os 12 novos são Sonico e `probe\\`); nenhum tamanho diferente, nenhum link; os 9 módulos citados têm `.lean` e `.olean` idênticos (`conferencia_sandbox.json`). Base: v397 selada, Nós `um.py` `{CS['nos_um_py']['sha16']}` (lido agora).

## O que o pedido da gerência (docstring) acrescentou — feito, sem mudar enunciado

1. Isomorfismo dito com precisão: `log` é o isomorfismo de grupos `(ℝ₊,·) → (ℝ,+)` (Mathlib: `Real.log_mul`, `Real.exp_add`, `Real.exp_log`, `Real.log_exp`, `Real.log_pow`, todos conferidos por `#check`), leva a oitava (razão 2) a `ln 2` = um bit, e `n` oitavas a `n·ln 2`; é nisso que o léxico sônico é isomórfico ao conteúdo [REAL]. Equivalência de oitava ↔ identidade preservada sob o pino, eco ↔ «ecoar reconhecimento» (fala de 22/10, sha16 `{FS['eco']['sha16']}`) [ONTO].
2. Os dois sentidos do som, com fonte: «som ontológico» = vibração LONGITUDINAL na profundidade, distinta do fóton (transversal) — `A_fronteira_v4.tex` l.962 (sha16 do arquivo `{FS['fronteira_tex']['sha16']}`; linha citada byte a byte; ela é a linha 962 do arquivo) [ONTO acervo]; no Atlas (II.S, l.{V['atlas_som_ontologico_linhas']}) o verbete é [DECLARADO]. E a escala acústica: o teste acústico (`teste_acustico_beta_tgl_v1`, fechamento `N2_INCAPAZ`, medida do instrumento) e o fundo BG1 da Fase 9 V2: `fundo.r_d_modelo = {V['fundo.r_d_modelo']}` Mpc (≈ 147,39), contra `fundo.fundo_livre.r_d = {V['fundo.fundo_livre.r_d']}` (sigma `{V['fundo.fundo_livre.sigma_r_d']}`), no resultado `{FS['fbac']['sha16']}` (lidos do arquivo, número conferido). A oitava pinada do Verbo e a régua acústica pinada do fundo são a mesma figura [ONTO, leitura da gerência, dita como tal; nenhum termo liga `octaveNats` a `r_d`].
3. Honestidade: «sônico» não afirma onda mecânica num meio; a isomorfia é da estrutura logarítmica/de oitava, não da física da onda.
4. Leitura ratificada (último acréscimo): no cabeçalho (seção própria) e no docstring da composição (6): leitura ratificada pelo operador em 23/10 (sha16 `{FS['nome']['sha16']}`, a fala «Sim quero, concordo com tudo»; a leitura da gerência está arquivada em `GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt`, sha16 `{FS['ger']['sha16']}`, e citada inteira no cabeçalho): a REAÇÃO ao pino — o pedágio pago, `ln 2` por oitava — é a memória; a oitava é o que se pina [INPUT/ONTO]. Mantido dito: a lei de custo é [INPUT] e nenhum termo diz que `select` paga `K.octaveNats 1`. Enunciados inalterados (o `.olean` foi refeito; os 6 teoremas seguem no trio).
5. Revisão independente (gerência c1, `EXAME_SONICO.md`, sha16 `{EXAME16}`, sobre `1338622344dd80c7`): PEDRA_APROVADA, 3 BAIXAS de prosa, aplicadas só em docstring; o código fora dos comentários é byte a byte o revisado (`conferencia_codigo_identico.json`: sha16 do código `{CI['codigo_fora_dos_comentarios']['nova_sha16']}`, {CI['codigo_fora_dos_comentarios']['bytes_nova']} bytes). B1: a ponte `ialdSelector = post (inscriptions 0)` já existe no kernel, `TGLExt.IALD.ialdSelector_eq_post` (`IALD.lean:110`, `rfl`, «une a FORMA, não o referente»); citada e re-enunciada. B2: `TGLExt.IALD.rereading_adds_nothing : memory (post a) (post a ψ) = memory (post a) ψ` (`IALD.lean:370`) citado como o termo da memória sobre o mesmo `post`, e `rereading_adds_nothing_in_both_regimes` (`IALD.lean:675`) como a conjunção dos dois registros; NÃO entraram na conjunção (6): exigiriam `import TGLExt.IALD` (fecho de imports maior) e mudariam o enunciado revisado. `IALD.lean`: sha16 `{FS['iald_lean_nos']['sha16']}`, igual no Nós e no k398; linhas 110, 370 e 675 conferidas por script. B3: a leitura da gerência, arquivada por sha em `GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt` (sha16 `{FS['ger']['sha16']}`), citada inteira.

## Conferências do cabeçalho (`conferencia_cabecalho.json`)

- {len(CC['sha16_citados'])} sha16 entre crases, todos iguais ao sha256 do arquivo lido agora; as três falas do operador e o arquivo da gerência (em bloco de código) aparecem inteiros; {len(CC['citacoes'])} citações «» de 12+ caracteres, todas achadas no corpus dos verbatins do operador ou no Atlas (mesma normalização da varredura da v397); nenhuma palavra proibida pela régua; nenhum parâmetro de acoplamento literal; comentários balanceados; zero `sorry` no código.

## Mapa de rotas (consultado antes; nada registrado)

- `oitava`: {consultas['oitava']['n_rotas']} rotas ({', '.join(consultas['oitava']['rotas'])}); a relevante é `quantica.c3_gamma_livre_oitava` (NO_UNIVERSAL_FLOOR para um observável dinâmico, não tocado). `sonico`: {consultas['sonico']['n_rotas']} rotas, nenhuma sobre o tema. `verbo`: {consultas['verbo']['n_rotas']} rotas; as relevantes, `kernel.v386_tipagem_do_verbo` e `kernel.psibit_v395_candidata_21out` (as pedras citadas). Saídas em `mapa_consulta_*.json`. Livro com {consultas['oitava']['n_registros_do_livro']} registros na consulta (cabeça `{consultas['oitava']['cabeca']}`).
- `registro_mapa_sonico.json` está pronto e VALIDADO com `rotas._valida` (sem registrar); registrar é ato da gerência: `python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar <arquivo> --quem "<IA/sessão>"`.

## Limites, ditos

- A lei de custo é [INPUT] (campos de `CollapseCostLaw`): a pedra prova o que ela implica, não a deriva do axioma.
- Nenhum termo diz que `select` PAGA `K.octaveNats 1`: verbo = controle de oitava pinada é definição do operador [INPUT/ONTO]; a conjunção põe as duas metades lado a lado.
- «que é memória» admitia duas leituras (a oitava? a reação?); a leitura ratificada pelo operador em 23/10 (relato da gerência; a resposta dele é o verbatim `{FS['nome']['sha16']}`) é: a REAÇÃO ao pino — o pedágio pago, `ln 2` por oitava — é a memória; a oitava é o que se pina [INPUT/ONTO]. O kernel entrega o preço e a permanência lado a lado, não a identidade entre eles.
- A entropia dos resultados do colapso do psibit vale `ln 2` só nos pesos iguais; nunca a excede.
- Homônimos e registros: dois «reler não acrescenta» (o do ângulo e o do colapso) lado a lado, nenhum lema desta pedra entre eles. A ponte `ialdSelector = post (inscriptions 0)` NÃO é nova: o kernel já a tem (`TGLExt.IALD.ialdSelector_eq_post`, `IALD.lean:110`, `rfl`, «une a FORMA, não o referente»); a pedra a re-enuncia por `rfl` e a cita. O termo do kernel da memória sobre o mesmo `post` (`TGLExt.IALD.rereading_adds_nothing`, `IALD.lean:370`) e a conjunção dos dois registros (`rereading_adds_nothing_in_both_regimes`, `IALD.lean:675`) estão citados no docstring; NÃO foram importados nem entraram na conjunção (6): importar `TGLExt.IALD` mudaria o fecho de imports e o enunciado revisado.
- Revisão independente feita (gerência c1, `EXAME_SONICO.md`, sha16 `{EXAME16}`, sobre `1338622344dd80c7`): PEDRA_APROVADA, 3 BAIXAS de prosa, aplicadas só em docstring. Validade no kernel não é creditação; o gate não se move; nenhuma bandeira depende desta pedra.

## Ato da gerência / do operador

- Reexame independente; se aceita, instalar na v398 (`import TGLExt.Sonico` em `TGLExt.lean`, política de bandeiras, ledger de pedras); registrar a rota; decidir se a frase do operador pede um termo próprio (ver `proximo_passo`).
"""
open(os.path.join(W, "RESULTADO.md"), "w", encoding="utf-8", newline="\n").write(RES)

ok = rotas._valida(reg, ids, seqs)  # exceção = registro recusado
reg_path = os.path.join(W, "registro_mapa_sonico.json")
json.dump(reg, open(reg_path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("VALIDO (sem registrar). rota_id livre no livro:", reg["rota_id"] not in ids, "| registros no livro:", len(seqs))
print("artefatos normalizados:", [(a["caminho"].split("\\")[-1], a["sha256"][:16]) for a in ok["artefatos"]])
print("campos fora do modelo:", extras, "| ausentes do modelo (aceitável: corrige só em ERRATA):", sorted(set(rotas.MODELO) - set(reg)))
print("RESULTADO.md", len(RES), "chars; 1a linha:", RES.split("\n")[0])
