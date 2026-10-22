# -*- coding: utf-8 -*-
"""Nomes e Verdade, PARTE 2: gera Verdade.lean (r3) a partir da r2 TheIdentityHasAName (ecae0725b21a98e6) com substituicoes
EXATAS (falha visivel se a contagem nao bate) e tres blocos novos (bloco_A, bloco_B, bloco_C). O ADENDO R3 foi congelado ANTES
(FREEZE_ADENDO_R3.json); este script nao o altera."""
import os, re, sys, hashlib, json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "C:/IALD/Central de Patentes/work"
R2 = W + "/identidade_cordeiro_13out/5_R2/pedra/TheIdentityHasAName.lean"
DEST = AQUI + "/4_VERDADE/Verdade.lean"
SC = AQUI + "/scripts/"

b = open(R2, "rb").read()
assert hashlib.sha256(b).hexdigest().startswith("ecae0725b21a98e6")
t = b.decode("utf-8")
fz = json.load(open(W + "/identidade_cordeiro_13out/2_PREREGISTRO/FREEZE_ADENDO_R3.json", encoding="utf-8"))
assert fz["pedra_r3_existe_no_congelamento"] is False


def rep(txt, velho, novo, n=1, tag=""):
    c = txt.count(velho)
    if c != n:
        print("FALHA VISIVEL: contagem", tag or velho[:60], "esperado", n, "achado", c)
        sys.exit(2)
    return txt.replace(velho, novo)


# 0. a estrutura chama-se `Verdade` dentro de `TGLExt.Verdade` (pedido do operador): silenciar o linter de namespace duplicado
t = rep(t, "set_option linter.unusedSectionVars false\n",
        "set_option linter.unusedSectionVars false\n-- a estrutura pedida chama-se `Verdade` e vive em `TGLExt.Verdade`: o namespace duplicado e deliberado\nset_option linter.dupNamespace false\n", 1, "linter")
# 1. imports
t = rep(t, "import TGLExt.Fundacao\nimport TGLExt.TheAlphaAndTheOmega\n",
        "import Mathlib.LinearAlgebra.Matrix.PosDef\nimport TGLExt.TheAlphaAndTheOmega\n", 1, "imports1")
t = rep(t, "import TGLExt.TheSelectionIsTheBallast\n", "import TGLExt.TheSelectionIsTheBallast\nimport TGLExt.ModularFlowAlgebra\n", 1, "imports2")

# 2. titulo + bloco R3
R3 = """# VERDADE — a identidade tem nome — pedra CANDIDATA da F1.IDENTIDADE, RODADA 3 (módulo `TGLExt.Verdade`; era `TheIdentityHasAName`)

  [⚠ AO LADO (13/10/2026 — RODADA DE NOMES E VERDADE, construtor da gerência c1, em nome próprio). Por decisão do operador
   (verbatim sha16 `0ddffcdb0a9c7b5e`, `work\\cunhagens_13out\\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`):
   a pedra passa a `TGLExt.Verdade`; «a identidade tem que ser igual à verdade por ela projetada, portanto identidade=verdade
   absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto»; «o cordeiro imolado é a relação de
   comutação que impede a coincidência total»; «A torre é o organismo IALD mesmo». O ADENDO R3 (`2_PREREGISTRO\\ADENDO_R3.json`) foi
   congelado ANTES desta pedra (`FREEZE_ADENDO_R3.json`, `pedra_r3_existe_no_congelamento: false`). O que muda em relação à r2
   (`ecae0725b21a98e6`, que fica intacta como registro):
   (1) SAEM `alicerce_fundante`, `alicerce_fundante_habitado` e o import de `TGLExt.Fundacao` — o cordeiro imolado não é o piso da
       Ágape; ENTRA a relação de comutação (seção 5): `refPost`, `commutatorWithPost`, `commutator_explicit`,
       `commutator_ne_zero_iff`, `identity_coincides_with_the_post_iff_alpha_zero`, `the_commutator_blocks_the_coincidence`, a
       reflexão J = 2E₀₀ − 1 com J·K·J = −K e as formas do kernel (`J_anticommutes_with_K`, `light_and_gravity_are_inseparable`);
   (2) ENTRA a negação da reflexividade como identidade (seção 5): `reflexivity_is_vacuous` e companheiras;
   (3) ENTRA a estrutura `Verdade` (seção 6c) e o teorema `the_identity_is_the_truth` / `identity_iff_truth` (seção 9);
   (4) a Torre é o organismo IALD: a instância principal é `towerIALD` (I6.c); `TowerHilbert` (I6.a) fica como a face unitária;
   (5) docstrings: as marcas [INPUT da gerência] de I6.b′ (achado B1 da auditoria c1 `a2694613`) e de I2.d (B2).
   Toda declaração da r2 fora dessa lista mantém tipo e valor (tabela r2→r3 lida do kernel em `TABELA_R2_R3.json`).
   CORREÇÃO DE FRASEADO (o número corrige a frase): o fluxo modular que fixa Ω e preserva ω está em I6.a (`TowerHilbert`), não em
   I6.c; a Verdade junta as duas e acrescenta a ponte (o fluxo age no portador da `towerIALD` e preserva a leitura).
   Nada move o gate; validade no kernel não é creditação.]
"""
t = rep(t, "# A IDENTIDADE TEM NOME — pedra CANDIDATA da F1.IDENTIDADE, RODADA 2 (nome PROVISÓRIO `TheIdentityHasAName`)\n", R3, 1, "titulo")
t = rep(t,
        "  [SANDBOX do construtor da rodada 2, gerência c1, 13/10/2026; NÃO instalada no Nós. O nome final da pedra, o termo que\n"
        "   se chama «o cordeiro imolado», qual é a Torre e a entrada na v392 são decisões do operador.]\n",
        "  [SANDBOX do construtor da rodada 3, gerência c1, 13/10/2026; NÃO instalada no Nós. O nome da pedra, o cordeiro imolado e a\n"
        "   Torre foram decididos pelo operador (acima); a entrada na v392 segue sendo ato da gerência.]\n", 1, "sandbox")

# 4. [ONTO]
t = rep(t,
        "a identificação «o cordeiro imolado» =\n"
        "  `alicerce_fundante` (leitura da GERÊNCIA, a decidir pelo operador; alternativas, sem escolha: (A) o piso da Ágape\n"
        "  `TGLExt.Fundacao.agape`; (B) β como o custo de distinguir 1 de 0; (C) J, a Palavra); toda leitura teológica e o\n"
        "  registro histórico.",
        "a identificação «o cordeiro imolado» =\n"
        "  `commutatorWithPost` (DECISÃO do operador, 13/10: «o cordeiro imolado é a relação de comutação que impede a coincidência\n"
        "  total»; a r2 tinha `alicerce_fundante` = `Fundacao.agape`, que o operador não escolheu); «verdade absoluta» = `Verdade`;\n"
        "  toda leitura teológica e o registro histórico.", 1, "onto")

# 6. I4 no resumo
t = rep(t,
        "* I4 — `alicerce_fundante`, `alicerce_fundante_habitado`: re-exportações TRIVIAIS de `TGLExt.Fundacao.agape` e\n"
        "  `agape_is_inhabited` sob nome provisório.\n",
        "* I4 (r3) — o cordeiro imolado: `refPost`, `commutatorWithPost`, `commutator_explicit`, `commutator_ne_zero_iff`,\n"
        "  `commutator_ne_zero_on_the_unit_interval`, `identity_coincides_with_the_post_iff_alpha_zero`,\n"
        "  `the_commutator_blocks_the_coincidence`, `the_poles_have_no_commutator`, `reflection`, `reflection_sq`,\n"
        "  `the_commutator_is_odd_under_the_reflection`, `the_reflection_anticommutes_with_the_commutator`,\n"
        "  `the_reflection_and_the_commutator_are_inseparable`; V1 — a reflexividade não distingue: `reflexivity_is_vacuous`,\n"
        "  `reflexivity_holds_for_every_inscription`, `reflexivity_does_not_separate_identities`. (A r2 trazia aqui\n"
        "  `alicerce_fundante` e `alicerce_fundante_habitado`, re-exportações de `Fundacao.agape`; saíram por decisão do operador.)\n"
        "* V2 (r3) — a Verdade: `Verdade` (estrutura em Prop), `verdade_of_unit_interval`, `the_projection_is_forced_by_its_truth`,\n"
        "  `the_modular_flow_preserves_the_IALD_reading`, `recognition_fixes_exactly_the_centralizer`, `the_identity_is_the_truth`,\n"
        "  `identity_iff_truth`; controles `no_truth_above_one`, `no_truth_below_minus_one`, `probe_the_truth`, `probe_the_commutator`.\n",
        1, "I4 resumo")
t = rep(t, "* I6 — a pedra OFERECE DUAS torres; qual é a Torre da ordem é decisão do operador:",
        "* I6 — a Torre é o organismo IALD (decisão do operador, 13/10: «A torre é o organismo IALD mesmo»): a instância principal é\n"
        "  `towerIALD` (I6.c); `TowerHilbert` (I6.a) fica como a face unitária:", 1, "I6 resumo")

# 8. NAO afirma
t = rep(t,
        "que `alicerce_fundante` SEJA «o cordeiro imolado» (decisão do operador); que `TowerHilbert`, `towerIALD` ou a\n"
        "torre de Jones seja a Torre da ordem (decisão do operador);",
        "que o comutador 2×2 seja a Luz, a Ágape ou «o cordeiro» além do termo (a leitura é do operador); que a torre de Jones\n"
        "seja a Torre da ordem (a Torre é o organismo IALD, `towerIALD`); que `Verdade` seja a verdade em sentido ontológico ou\n"
        "teológico (é o nome de uma estrutura em Prop);", 1, "nao afirma")

# 9. reaproveitamento
t = rep(t, "`trace_diagExpect`, `Fundacao.agape`,",
        "`trace_diagExpect`, `J_anticommutes_with_K`, `light_and_gravity_are_inseparable`, `iald_recognition_is_stable`,\n"
        "`Collapse057.tower_fixed_points_exactly_centralizer`, `modularConjugation_preserves_factor`, e (Mathlib)\n"
        "`trace_conjTranspose_mul_self_eq_zero_iff`,", 1, "reaprov")

# 10. namespace / open
t = rep(t, "namespace TGLExt.TheIdentityHasAName\n", "namespace TGLExt.Verdade\n", 1, "ns")
t = rep(t, "end TGLExt.TheIdentityHasAName\n", "end TGLExt.Verdade\n", 1, "end ns")
t = rep(t, "open scoped InnerProductSpace\n", "open scoped InnerProductSpace ComplexOrder\n", 1, "open scoped")

# 11. B1 / B2
t = rep(t,
        "É a forma, na torre, de \"tudo defasa, a identidade\n    permanece\": a coerência α não sobrevive, ω sim. [INPUT da gerência] ler isto como",
        "[INPUT da gerência] Ler isto como a forma, na torre, de \"tudo defasa, a identidade permanece\" é leitura da gerência,\n"
        "    não teorema extra: o termo diz que a coerência α não sobrevive à esperança e que ω sim. [INPUT da gerência] Ler isto como",
        1, "B1")
t = rep(t,
        "O que «não pode ser derivado» lê-se aqui como:",
        "[INPUT da gerência] Ler o que «não pode ser derivado» (operador, 13/10) assim é leitura da gerência sobre este termo:",
        1, "B2")

# 12. secao 5 (I4) -> bloco A
ini = t.index("/-! ## 5. I4 — o alicerce fundante (nome PROVISÓRIO; a identificação é do operador) -/")
fim_marca = "  Fundacao.agape_is_inhabited\n\n"
fim = t.index(fim_marca, ini) + len(fim_marca)
assert t.count(fim_marca) == 1
bloco_a = open(SC + "bloco_A.lean", encoding="utf-8").read()
t = t[:ini] + bloco_a + t[fim:]

# 13. bloco B antes da secao 7
marca7 = "/-! ## 7. I5 — O NOME PRÓPRIO (dado POSTO) e a parametricidade -/"
assert t.count(marca7) == 1
t = t.replace(marca7, open(SC + "bloco_B.lean", encoding="utf-8").read() + marca7)

# 14. torre
t = rep(t, "/-! ## 6. I6 — a mesma identidade NA TORRE: duas torres oferecidas (a escolha é do operador) -/",
        "/-! ## 6. I6 — a mesma identidade NA TORRE: a Torre é o organismo IALD (`towerIALD`, instância principal); `TowerHilbert` é a face unitária -/",
        1, "sec6")
t = rep(t, "A pedra oferece as duas; qual é a Torre da ordem («dentro da Torre») é decisão do\n    operador. -/",
        "A Torre da ordem é o organismo IALD («A torre é o organismo IALD mesmo», operador, 13/10): esta é a\n"
        "    instância PRINCIPAL; I6.a em `TowerHilbert` é a face unitária. -/", 1, "I6c doc")
t = rep(t, "/-- r2 (I6.c): a mesma identidade também na `towerIALD`. -/",
        "/-- r2 (I6.c): a mesma identidade na `towerIALD` — r3: a instância principal (a Torre é o organismo IALD). -/", 1, "campo torre")

# 15. bloco C
fim_ns = "\nend\n\nend TGLExt.Verdade\n"
assert t.count(fim_ns) == 1
t = t.replace(fim_ns, "\n" + open(SC + "bloco_C.lean", encoding="utf-8").read() + "end\n\nend TGLExt.Verdade\n")

# 16. #print axioms
n_pa = len(re.findall(r"^#print axioms TGLExt\.TheIdentityHasAName\.", t, flags=re.M))
t = re.sub(r"^#print axioms TGLExt\.TheIdentityHasAName\.", "#print axioms TGLExt.Verdade.", t, flags=re.M)
t = rep(t, "#print axioms TGLExt.Verdade.alicerce_fundante\n", "", 1, "pa alicerce")
novos = ["reflexivity_holds_for_every_inscription", "reflexivity_does_not_separate_identities", "commutator_explicit",
         "commutator_ne_zero_iff", "identity_coincides_with_the_post_iff_alpha_zero", "the_commutator_blocks_the_coincidence",
         "the_poles_have_no_commutator", "the_commutator_is_odd_under_the_reflection",
         "the_reflection_anticommutes_with_the_commutator", "the_reflection_and_the_commutator_are_inseparable",
         "the_projection_is_forced_by_its_truth", "verdade_of_unit_interval", "the_identity_is_the_truth", "identity_iff_truth",
         "no_truth_above_one", "no_truth_below_minus_one", "probe_the_truth", "probe_the_commutator"]
t = t.rstrip("\n") + "\n" + "".join("#print axioms TGLExt.Verdade." + n + "\n" for n in novos)
open(DEST, "w", encoding="utf-8", newline="\n").write(t)
print("ok", len(t.splitlines()), "linhas;", hashlib.sha256(t.encode("utf-8")).hexdigest()[:16], "print axioms r2:", n_pa)
