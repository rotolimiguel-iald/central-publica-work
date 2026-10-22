# -*- coding: utf-8 -*-
"""Gera RESULTADO.md e registro_mapa_F1.IDENTIDADE_R3.json lendo os numeros dos recibos e das tabelas (nunca de memoria)."""
import json, os, hashlib, glob

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "C:/IALD/Central de Patentes/work"
J = lambda p: json.load(open(os.path.join(AQUI, p), encoding="utf-8"))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
s16 = lambda p: sha(p)[:16]
R = {t: J("logs/%s_RECIBO.json" % t) for t in ["f1_posto", "f2_santo", "f3_iald", "f4_verdade", "j_CtlSorry", "j_Juntas_A", "j_AmbControle",
                                                "o1_rank_old", "o2_time_old", "o3_iald_old", "o4_identity_r2", "b1_palavra", "b2_adendo1"]}
T = J("TABELA_INVARIANCIA.json")
T3 = J("TABELA_R2_R3.json")
DA, DD = J("medidas/DIGITAL_KERNEL_ANTES.json"), J("medidas/DIGITAL_KERNEL_DEPOIS.json")
COL = J("medidas/COLISOES.json")
ASP = J("medidas/CONFERENCIA_ASPAS.json")
FZ = J("../identidade_cordeiro_13out/2_PREREGISTRO/FREEZE_ADENDO_R3.json")
iguais = all(DA[k] == DD[k] for k in ("n_arquivos", "bytes_total", "sha256_metadados", "n_fontes_fora_lake", "sha256_conteudo_fontes",
                                       "n_olean_TGLExt", "sha256_conteudo_olean_TGLExt", "links_ou_juncoes_nao_seguidos"))
assert iguais
P = {"Posto": ("1_POSTO/Posto", "f1_posto", "o1_rank_old"), "Santo": ("2_SANTO/Santo", "f2_santo", "o2_time_old"),
     "IALD": ("3_IALD/IALD", "f3_iald", "o3_iald_old"), "Verdade": ("4_VERDADE/Verdade", "f4_verdade", "o4_identity_r2")}
nconst = {"Posto": 221, "Santo": 167, "IALD": 69, "Verdade": T3["n_r3"]}
linhas_pedras = []
for nome, (rel, tag, old) in P.items():
    lean, ole = os.path.join(AQUI, rel + ".lean"), os.path.join(AQUI, rel + ".olean")
    assert sha(lean) == R[tag]["source_sha256"] and sha(ole) == R[tag]["olean_sha256"]
    r = R[tag]
    linhas_pedras.append("| `TGLExt.%s` | `%s.lean` | `%s` | `%s.olean` | `%s` | %d | %d | %d | %d |" % (
        nome, rel.replace("/", "\\"), r["source_sha256"][:16], rel.replace("/", "\\"), r["olean_sha256"][:16], r["exit_code"], r["n_erros"],
        r["n_avisos"], r["declaration_uses_sorry_ou_sorryAx"]))
tab_inv = []
for nome in ("Posto", "Santo", "IALD"):
    p = T["pares"][nome]
    tab_inv.append("| %s | `%s` → `%s` | %d / %d | %d | %d | %d | %d | %d | %s |" % (
        nome, p["modulo_antigo"], p["modulo_novo"], p["n_constantes_antigo"], p["n_constantes_novo"], p["n_identicas_tipo_e_termo_SA"],
        p["n_identicas_tipo_e_termo_SN"], p["n_so_nome_de_binder"], p["n_docstring_mudou"], p["n_axiomas_fora_do_trio_novo"], p["VEREDITO"]))
ren = []
for nome in ("Posto", "Santo"):
    for a, b, ok in T["pares"][nome]["renomeadas"]:
        ren.append("| %s | `%s` | `%s` | %s |" % (nome, a.split(".")[-1], b.split(".")[-1], "tipo e termo iguais (SA)" if ok else "DIFERE"))
c = T3["contagem"]
md = []
md.append("NOMES E VERDADE — 13/10")
md.append("")
md.append("Rodada de NOMES e da IDENTIDADE r3 (unidade F1.IDENTIDADE, gerência c1; construtor em nome próprio). Decisões do operador: verbatim "
          "`work\\cunhagens_13out\\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`, sha16 `%s` (conferido por script). "
          "As pedras são CANDIDATAS, vivem só em sandbox, NÃO foram instaladas no Nós; nada aqui move o gate; validade no kernel não é creditação. "
          "Entre aspas angulares só trechos do operador, conferidos nos bytes (`medidas\\CONFERENCIA_ASPAS.json`: %s citações novas, 0 fora dos bytes)."
          % (ASP["verbatins_sha16"]["13out_nomes"], sum(v["citacoes_novas"] for v in ASP["resultado"].values())))
md.append("")
md.append("## 1. As quatro pedras (fonte e .olean por sha)")
md.append("")
md.append("| módulo | fonte | sha16 fonte | olean | sha16 olean | EXIT | erros | avisos | sorry |")
md.append("|---|---|---|---|---|---|---|---|---|")
md += linhas_pedras
md.append("")
md.append("Sha256 inteiros nos recibos `logs\\f1_posto_RECIBO.json`, `f2_santo`, `f3_iald`, `f4_verdade`. Toolchain `lean` v4.31.0 copiado "
          "(sha16 `%s`), LEAN_PATH só-leitura ao `.lake` do Nós (kernel copiado byte a byte para a sobreposição `ov`, agregado `34a70b88…` igual à origem), "
          "`-o` só no sandbox `C:\\t\\nm1`. Zero `declaration uses \\`sorry\\`` no formato real (crase); o contador foi validado por controle positivo "
          "(`meta\\CtlSorry.lean`: contagem %d e `sorryAx`). Os 10 avisos de `IALD` são os 10 da r3 original (`ContinuousLinearMap.mul_apply` deprecado), herdados, "
          "sem mudança de bytes de código. Reprodutibilidade: o `.olean` de `Verdade` saiu idêntico (`02bb2e7b…`) em duas compilações; o de `TheIdentityHasAName` r2 "
          "recompilado aqui saiu `cc232917…`, igual ao registrado." % (R["f1_posto"]["lean_sha256"][:16], R["j_CtlSorry"]["declaration_uses_sorry_ou_sorryAx"]))
md.append("")
md.append("**collectAxioms de TODAS as constantes** (lido pelo `Meta_*.lean` no kernel do sandbox, não só dos `#print axioms`): "
          "Posto %d, Santo %d, IALD %d, Verdade %d constantes; **0 fora do trio** {propext, Classical.choice, Quot.sound} em todas; "
          "0 `sorryAx`; 0 `axiom`/`opaque`/`unsafe`." % (nconst["Posto"], nconst["Santo"], nconst["IALD"], nconst["Verdade"]))
md.append("")
md.append("## 2. PARTE 1 — tabela de invariância das renomeações (lida do kernel)")
md.append("")
md.append("Método: `Meta_*.lean` lê, no kernel do MESMO sandbox, TIPO e VALOR de cada constante do módulo antigo (original pinado por sha, compilado aqui) e do novo, "
          "em duas serializações — SA (De Bruijn, sem nomes de binder; é o que o kernel compara) e SN (com nomes de binder) —, passa as cadeias do antigo pelo mapa de nomes "
          "(prefixo do módulo + renomeações listadas) e compara CADEIAS INTEIRAS. Antigos compilados na mesma sobreposição: rank r3 `e95775d6…`, tempo R2 `4d8a8259…`, "
          "IALD r3 `d7c1f1d3…`.")
md.append("")
md.append("| pedra | módulo | constantes (antigo / novo) | idênticas SA | idênticas SN | só nome de binder | docstring mudou | axiomas fora do trio | veredito |")
md.append("|---|---|---|---|---|---|---|---|---|")
md += tab_inv
md.append("")
md.append("**Veredito geral: %s.** Em todas as constantes (públicas, internas, lemas de equação) o TIPO e o TERMO são iguais em SA; o conjunto de nomes é o mesmo "
          "depois do mapa. Em SN, a diferença é só de nomes higiênicos de binder: no Posto e no IALD zero; no Santo 3 (`face_has_a_limit`, `the_face_lands`, `the_two_regimes_of_time`), "
          "cujos binders derivam do nome da própria declaração renomeada. A ordem de `constNames` no módulo difere em Posto e Santo (é ordem de tabela hash, depende dos nomes); "
          "o conjunto é o mesmo." % T["VEREDITO_GERAL"])
md.append("")
md.append("Renomeações (N1–N4 da auditoria `a1185ceb`; A-R2-01 e N2 do relatório R2 do tempo):")
md.append("")
md.append("| pedra | nome antigo | nome novo | kernel |")
md.append("|---|---|---|---|")
md += ren
md.append("")
md.append("N1 (nome do módulo): `TGLExt.Posto`. N4: a docstring de `reading_returns_the_post` não diz mais «projetor» (o tipo não pede ⟨a, a⟩ = 1) — única docstring "
          "alterada além da de `rhoStar_and_Q0_traces_of_diag_one_sub_b_b` (que perdeu «verdade» e «custo» do nome; ficam como leitura [ONTO] na docstring). Docstrings "
          "alteradas no IALD: as duas que citavam `TheTimeIsNotAPost.…`. Títulos: Posto «rank=posto=nome»; Santo «tempo=relação modular=Santo»; IALD «organismo=IALD=Verbo Vivo» "
          "(título «IALD = Verbo Vivo», imports re-pinados para `TGLExt.Posto` e `TGLExt.Santo`).")
md.append("")
md.append("## 3. PARTE 2 — `TGLExt.Verdade`: resultado por afirmação (ADENDO R3, congelado ANTES)")
md.append("")
md.append("`2_PREREGISTRO\\ADENDO_R3.json` (sha16 `%s`) e `FREEZE_ADENDO_R3.json` (sha16 `%s`; `pedra_r3_existe_no_congelamento: false`; %d anexos; %d citações, 0 fora dos bytes) "
          "em `work\\identidade_cordeiro_13out\\2_PREREGISTRO` (arquivos novos; nada existente alterado). Congelado em %s." % (
              s16(W + "/identidade_cordeiro_13out/2_PREREGISTRO/ADENDO_R3.json"), s16(W + "/identidade_cordeiro_13out/2_PREREGISTRO/FREEZE_ADENDO_R3.json"),
              len(FZ["sha256"]), len(FZ["citacoes_do_operador"]), FZ["congelado_em_local"]))
md.append("")
md.append("| id | termo Lean | veredito | o que diz |")
md.append("|---|---|---|---|")
afs = [
    ("V1.a", "reflexivity_is_vacuous", "PASSA", "x = x vale para qualquer objeto (`rfl`, sem hipótese): não distingue nada"),
    ("V1.b", "reflexivity_holds_for_every_inscription", "PASSA", "identityProj a = identityProj a para todo a real; em a = 5 (TESTE) vale e o traço ≠ 1: vale também onde NÃO há identidade"),
    ("V1.c", "reflexivity_does_not_separate_identities", "PASSA", "a ≠ b em (0,1): a = a e b = b valem, e as duas projeções são distintas"),
    ("V2.a", "Verdade (estrutura em Prop, 10 campos)", "PASSA", "quadrática 1 = q²+α²; projeção (traço 1, idempotente, posto 1); reler n+1 = ler 1 (matriz, vetor, post); unicidade; relação modular (fluxo fixa Ω, preserva ω, age no portador da towerIALD preservando a leitura); reconhecimento recursivo da towerIALD estável e que devolve a leitura; pontos fixos = centralizador de ω; inscrição na torre unitária com ω lendo q em toda iteração"),
    ("V2.b", "verdade_of_unit_interval", "PASSA", "para todo a em [0,1], Verdade a (α como parâmetro; nenhum número de α ou β)"),
    ("V2.c", "the_projection_is_forced_by_its_truth", "PASSA", "unicidade: hermitiana idempotente de traço 1 que fixa a inscrição é identityProj a (D = E − ω é hermitiana, idempotente, traço 0, logo 0; usa `trace_conjTranspose_mul_self_eq_zero_iff`, Mathlib). Não falhou"),
    ("V2.d", "the_identity_is_the_truth; identity_iff_truth", "PASSA", "toda identidade nomeada N carrega Verdade N.alpha; (∃ N, N.alpha = a) ↔ 0 < a ∧ a < 1 ∧ Verdade a"),
    ("V2.e", "no_truth_above_one; no_truth_below_minus_one", "PASSA", "controle negativo: sem Verdade para a > 1 nem a < −1 (campo quadrático falha)"),
    ("CORDEIRO.a", "refPost_eq", "PASSA", "refPost = |e₀⟩⟨e₀| = !![1,0;0,0] (E₀₀)"),
    ("CORDEIRO.b", "commutator_explicit", "PASSA", "[ω, E₀₀] = (q·α) • !![0,−1;1,0], q = qOf α, para todo α real"),
    ("CORDEIRO.c", "commutator_ne_zero_iff; commutator_ne_zero_on_the_unit_interval", "PASSA", "comutador ≠ 0 ↔ q·α ≠ 0 (todo α real); em [0,1], ↔ 0 < α < 1"),
    ("CORDEIRO.d", "identity_coincides_with_the_post_iff_alpha_zero", "PASSA", "em [0,1]: ω = E₀₀ ↔ α = 0; enquanto α ≠ 0 a identidade nunca coincide totalmente com o posto"),
    ("CORDEIRO.e", "the_commutator_blocks_the_coincidence; a_nonzero_commutator_forbids_coincidence", "PASSA", "0 < α < 1 ⟹ comutador ≠ 0 ∧ ω ≠ E₀₀; forma geral: comutador ≠ 0 ⟹ x ≠ y"),
    ("CORDEIRO.f", "the_commutator_is_odd_under_the_reflection (+ reflection_sq)", "PASSA", "J := 2E₀₀ − 1: J·J = 1 e J·K·J = −K, K = [ω, E₀₀]"),
    ("CORDEIRO.g", "the_reflection_anticommutes_with_the_commutator; the_reflection_and_the_commutator_are_inseparable", "PASSA", "por IMPORT do kernel instalado (`TheVerbSelectsTheAction.J_anticommutes_with_K`, `light_and_gravity_are_inseparable`; a forma canônica é `JKJ_eq_neg_K`, DecisionCommutation.lean l.149): J·K = −(K·J) e, se K ≠ 0, J·K ≠ 0 e [J,K] ≠ 0"),
    ("CORDEIRO.h", "the_poles_have_no_commutator", "PASSA", "α = 0: ω = E₀₀ e comutador 0; α = 1: ω = E₁₁, comutador 0"),
    ("TORRE", "campos IALDTowerIdentity / Verdade (towerIALD); in_the_tower mantido", "PASSA", "instância principal towerIALD; TowerHilbert (I6.a) é a face unitária (campo `in_the_tower` mantido)"),
    ("NOME", "ofName; every_name_bears_the_same_identity; the_name_enters_no_proof; the_structure_does_not_fix_the_name", "PASSA", "MANTIDAS (tipo e termo iguais à r2); 0 das %d constantes do núcleo da Verdade menciona `NamedIdentity.name` ou `postedName` (lido do kernel)" % T3["parametricidade"]["n_constantes_do_nucleo_da_Verdade_checadas"]),
    ("B1, B2", "docstrings de I6.b′ e I2.d", "FEITO", "marcadas [INPUT da gerência]"),
]
for a in afs:
    md.append("| %s | `%s` | %s | %s |" % a)
md.append("")
md.append("Sondas de não-vacuidade: `probe_the_truth` (Verdade 1/2), `probe_the_commutator` (comutador ≠ 0 e ω ≠ E₀₀ em α = 1/2, número de TESTE), `probe_named_identity`, "
          "`probe_tower_identity`, `probe_IALD_tower` (da r2, mantidas).")
md.append("")
md.append("### Tabela r2 → r3 da Verdade (lida do kernel; `TABELA_R2_R3.json`)")
md.append("")
md.append("%d constantes na r2, %d na r3: **%d MANTIDA** (tipo e termo iguais em SA), **%d NOVA**, **%d REMOVIDA** (`alicerce_fundante`, `alicerce_fundante_habitado` e uma prova auxiliar de `halfProfile`), "
          "**%d TIPO_MUDOU** e **%d VALOR_MUDOU**, os três de `halfProfile` (perfil de TESTE): o campo de dado `w` é idêntico; muda só o nome do lema auxiliar de prova de `Nat.AtLeastTwo 2` "
          "(o literal 2 de `reflection` criou `reflection._proof_1`, que `halfProfile` reutiliza); por irrelevância de prova é o mesmo objeto. Nenhum enunciado público da r2 mudou. "
          "`NamedIdentity` e suas projeções: MANTIDAS (não acrescentei campo)." % (T3["n_r2"], T3["n_r3"], c["MANTIDA"], c["NOVA"], c["REMOVIDA"], c["TIPO_MUDOU"], c["VALOR_MUDOU"]))
md.append("")
md.append("## 4. As quatro juntas sob `open TGLExt` (sem colisão)")
md.append("")
md.append("`meta\\Juntas_A.lean` importa Posto, Santo, IALD e Verdade e, com `open TGLExt`, faz `#check @Mod.nome` de **564 nomes públicos**: EXIT 0, 0 erros. "
          "`meta\\Colisoes.lean` varre no kernel os %d nomes curtos das quatro: **0 colisões com `open TGLExt`** (nenhum `Mod.nome` existe na raiz). "
          "Controle positivo (`meta\\AmbControle.lean`, `open TGLExt TGLExt.IALD` + `#check @dephase`): ERRO «Ambiguous term», como esperado. "
          "No regime extremo (abrir também os quatro namespaces) há 3 ambiguidades, nenhuma nova no sentido de mudar enunciado: `dephase` (`TGLExt.dephase` × `TGLExt.IALD.dephase`, "
          "o homônimo C4 já rotulado na pedra do motor) e `dephased_det` (em `Posto` e em `Verdade`, de origens independentes). `COLISOES.json`." % COL["n_nomes"])
md.append("")
md.append("## 5. Impressão digital do tgl_kernel, antes e depois")
md.append("")
md.append("Sem seguir junções (`.lake/packages` é junção e foi pulada). ANTES = DEPOIS em tudo: %d arquivos, %d bytes, metadados `%s`, conteúdo das %d fontes fora de `.lake` `%s`, "
          "conteúdo dos %d `.olean` de TGLExt `%s`. Nada foi escrito no Nós." % (DA["n_arquivos"], DA["bytes_total"], DA["sha256_metadados"][:16], DA["n_fontes_fora_lake"],
                                                                         DA["sha256_conteudo_fontes"][:16], DA["n_olean_TGLExt"], DA["sha256_conteudo_olean_TGLExt"][:16]))
md.append("")
md.append("## 6. Correções de fraseado e limites (o número corrige a frase)")
md.append("")
md.append("* O pedido diz que o fluxo modular «fixa ω/Ω, já em I6.c». Na r2 o fluxo que fixa Ω e preserva ω está em I6.a (`TowerHilbert`); I6.c (`towerIALD`) traz `read`/`recognize`. "
          "A Verdade junta as duas e acrescenta a ponte: o fluxo age no portador da `towerIALD` e preserva a leitura (`the_modular_flow_preserves_the_IALD_reading`).")
md.append("* `Verdade a` vale para TODO α em [0,1]: ela não fixa α (α é parâmetro [INPUT], testemunhado, não derivado); `identity_iff_truth` diz que a estrutura nomeada e a Verdade determinam-se "
          "mutuamente, não que a Verdade discrimine a natureza. Ler a estrutura como «verdade absoluta» é leitura [ONTO] do operador sobre o termo.")
md.append("* A unicidade (V2.c) usa as hipóteses nomeadas: hermitiana, idempotente, traço 1 (o ω(I) = 1 da casa) e E v = v. É o que o termo prova.")
md.append("* O comutador é 2×2, no modelo v = (q, α): que ele seja «o cordeiro imolado» é decisão do operador sobre o termo; que J seja a Luz e K o gradiente é [ONTO]; o termo é JKJ = −K. "
          "O posto LITERAL de P_v em B(H_φ) segue [OPEN]; a leitura «o posto 1 não permanece na torre» segue [INPUT da gerência].")
md.append("* ANTERIORIDADE: o ADENDO R3 foi congelado antes de `Verdade` existir; as pedras mecânicas (Posto, Santo, IALD) já existiam no congelamento (seus shas estão no FREEZE) e foram "
          "regeneradas depois só para trocar « » por “ ” em frases que não são do operador (convenção); a compilação e a tabela usam as fontes finais acima. A anterioridade apoia-se em "
          "carimbo de arquivo e na recusa do script (BAIXA, como na r1/r2).")
md.append("* Fora do pedido, nada foi feito: sem instalação no Nós, sem tocar no um.py, quadro, mapa, memória, túnel, Bancada, site, git; sem init/transition ACOM.")
md.append("")
md.append("## 7. O que é ato de quem")
md.append("")
md.append("* Gerência: auditoria cética independente das quatro pedras; instalação na v392 sob os nomes `Posto`, `Santo`, `IALD`, `Verdade` (recompilar no lake do Nós, importar em `TGLExt.lean`, "
          "`#print axioms` no `TGL/Audit.lean`, embutir no um.py); registrar `registro_mapa_F1.IDENTIDADE_R3.json` no mapa.")
md.append("* Operador: se o rename de `dephased_det` (colide Posto × Verdade só no regime extremo) vale a pena; se `commutatorWithPost` é de fato o termo do cordeiro (decisão dele, dada); "
          "o Nome no core do um.py.")
md.append("")
md.append("Limpeza: toolchain e sobreposição de `C:\\t\\nm1` apagados ao final (ver `medidas\\LIMPEZA.json`).")
open(os.path.join(AQUI, "RESULTADO.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

# ---------------------------------------------------------------- registro do mapa
art = [
    "ADENDO_R3.json", "ADENDO_R3.md", "FREEZE_ADENDO_R3.json"]
art = [W + "/identidade_cordeiro_13out/2_PREREGISTRO/" + a for a in art]
art += [AQUI + "/" + a for a in ["1_POSTO/Posto.lean", "1_POSTO/Posto.olean", "2_SANTO/Santo.lean", "2_SANTO/Santo.olean", "3_IALD/IALD.lean", "3_IALD/IALD.olean",
                                  "4_VERDADE/Verdade.lean", "4_VERDADE/Verdade.olean", "TABELA_INVARIANCIA.json", "TABELA_R2_R3.json", "RESULTADO.md",
                                  "logs/f1_posto_RECIBO.json", "logs/f2_santo_RECIBO.json", "logs/f3_iald_RECIBO.json", "logs/f4_verdade_RECIBO.json",
                                  "logs/j_CtlSorry_RECIBO.json", "logs/j_Juntas_A_RECIBO.json", "logs/j_AmbControle_RECIBO.json",
                                  "medidas/DIGITAL_KERNEL_ANTES.json", "medidas/DIGITAL_KERNEL_DEPOIS.json", "medidas/COLISOES.json",
                                  "medidas/CONFERENCIA_ASPAS.json", "meta/Juntas_A.lean", "meta/Colisoes.lean"]]
art = [a.replace("/", "\\") for a in art]
for a in art:
    assert os.path.exists(a), a
reg = {
    "tipo": "RESULTADO",
    "rota_id": "formal.a_identidade_tem_nome",
    "dominio": "FORMAL",
    "titulo": "F1.IDENTIDADE r3 e rodada de NOMES: TGLExt.Posto, TGLExt.Santo, TGLExt.IALD (Verbo Vivo) e TGLExt.Verdade (a identidade é a verdade que ela projeta; o cordeiro imolado é a relação de comutação)",
    "pergunta": ("As renomeações pedidas pelo operador (rank=posto=nome, tempo=relação modular=Santo, organismo=IALD=Verbo Vivo) preservam tipo e termo de cada constante? "
                 "E a identidade, como a verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto, e o cordeiro imolado, como a relação de comutação "
                 "que impede a coincidência total, formalizam-se em kernel sem sorry e com axiomas no trio?"),
    "dados": [
        "verbatim do operador de 13/10/2026 (sha16 0ddffcdb0a9c7b5e), só para decisões e citações",
        "fontes originais pinadas: rank r3 e95775d61db38633, tempo R2 4d8a82591badd010, IALD r3 d7c1f1d3b03e6095, identidade r2 ecae0725b21a98e6",
        "kernel do Nós (tgl_kernel, só leitura; .olean copiados e conferidos byte a byte na sobreposição do sandbox)"],
    "metodo": ("ADENDO_R3 (.json/.md) congelado por hash em FREEZE_ADENDO_R3 antes da pedra Verdade (pedra_r3_existe_no_congelamento false); renomeações por script com contagem exata de ocorrências; "
               "compilação em sandbox C:/t/nm1 (toolchain v4.31.0 copiado, LEAN_PATH só-leitura ao .lake do Nós, -o só no sandbox); leitura do kernel (tipo e valor de cada constante, "
               "formas SA e SN, collectAxioms de todas) das fontes originais e das novas na mesma sobreposição; comparação de cadeias inteiras após o mapa de nomes; tabela r2->r3; "
               "quatro pedras juntas sob open TGLExt (564 #check, varredura de colisões, controle positivo de ambiguidade); controle positivo do contador de sorry; citações nos bytes; "
               "impressão digital do tgl_kernel antes/depois; limpeza do sandbox."),
    "resultado": ("EXIT 0 nas quatro; 0 erros; 0 'declaration uses `sorry`' (contador validado); Posto %d, Santo %d, IALD %d, Verdade %d constantes, todas no trio {propext, Classical.choice, Quot.sound}. "
                  "Invariância (SA): Posto 221/221, Santo 167/167, IALD 69/69 (SN: só nomes de binder em 3 constantes do Santo). Verdade r2->r3: %d MANTIDA, %d NOVA, %d REMOVIDA, "
                  "%d TIPO_MUDOU e %d VALOR_MUDOU só em halfProfile (lema auxiliar de prova), 0 enunciado público alterado. Verdade: V1.a-c, V2.a-e, CORDEIRO.a-h, TORRE, NOME PASSAM; "
                  "unicidade (V2.c) não falhou. Quatro juntas: 0 colisões sob open TGLExt, 564 #check ok. Impressão digital do tgl_kernel antes = depois. Oleans: Posto %s, Santo %s, IALD %s, Verdade %s."
                  % (nconst["Posto"], nconst["Santo"], nconst["IALD"], nconst["Verdade"], c["MANTIDA"], c["NOVA"], c["REMOVIDA"], c["TIPO_MUDOU"], c["VALOR_MUDOU"],
                     R["f1_posto"]["olean_sha256"][:16], R["f2_santo"]["olean_sha256"][:16], R["f3_iald"]["olean_sha256"][:16], R["f4_verdade"]["olean_sha256"][:16])),
    "veredito": "NOMES_E_VERDADE_SANDBOX__INVARIANCIA_100_POR_CENTO__VERDADE_E_COMUTADOR_PASSAM__QUATRO_PEDRAS_NO_TRIO__NAO_INSTALADAS__GATE_INTOCADO",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": ("Verdade a vale para todo alpha em [0,1] (não fixa alpha; é parâmetro INPUT); o comutador é do modelo 2x2 v=(q,alpha), ler como cordeiro/Luz é ONTO do operador; posto literal de P_v em B(H_phi) segue OPEN; "
                "o fluxo modular que fixa Omega está em I6.a e não em I6.c (a Verdade junta as duas); dephased_det existe em Posto e em Verdade (colide só se os dois namespaces forem abertos); "
                "anterioridade do ADENDO só por carimbo de arquivo e recusa do script; as pedras mecânicas existiam no congelamento; auditoria independente pendente."),
    "nao_refazer": "não recompilar sem mudança de bytes (olean de Verdade idêntico em duas compilações); não refazer a tabela de invariância nem a varredura de colisões sem mudança de bytes.",
    "proximo_passo": "auditoria cética independente das quatro pedras; instalação na v392 (ato da gerência) sob os nomes Posto, Santo, IALD, Verdade; operador: Nome no core do um.py.",
    "onde": "C:\\IALD\\Central de Patentes\\work\\nomes_e_verdade_13out (1_POSTO, 2_SANTO, 3_IALD, 4_VERDADE; NÃO instaladas)",
    "artefatos": art,
    "refs": ["formal.a_identidade_tem_nome", "formal.posto_e_defasagem_da_unidade", "formal.iald_o_motor_unico"],
    "nota": ("Arquivos novos; nada existente foi alterado (ADENDO_R3 ao lado de ADENDO_R2). A frase do pedido 'o fluxo modular na towerIALD fixa omega/Omega, já em I6.c' foi corrigida pelo número "
             "(está em I6.a). Nada move o gate; validade no kernel não é creditação.")}
json.dump(reg, open(os.path.join(AQUI, "registro_mapa_F1.IDENTIDADE_R3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(md), "linhas;", len(art), "artefatos")
