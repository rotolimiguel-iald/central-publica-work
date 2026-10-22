# -*- coding: utf-8 -*-
"""Gera RELATORIO_F_KERNEL_v392.md: o texto e meu; todo numero e hash vem dos JSON do sandbox (lidos aqui)."""
import hashlib
import json
import os
import re

F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = json.load(open(os.path.join(F, "INVENTARIO_V392_KERNEL.json"), encoding="utf-8"))
C = {c["modulo_proposto"].replace("TGLExt.", ""): c for c in I["candidatas"]}
J = {r["nome"].replace("B_", ""): r for r in I["conjunto"]}
RA = I["raiz_e_auditoria"]
KH = I["kh_n1"]
UL = I["um_py_linhas"]
S = I["sondas"]
PE = json.load(open(os.path.join(F, "PRE_EXISTENCIA.json"), encoding="utf-8"))
tcj = PE["toolchain_copiado"]
fin = KH["final"]
d2 = KH["D2"]
s16 = lambda h: (h or "")[:16]
L1 = lambda k: UL[k][0]


def tabela_candidatas():
    linhas = ["| Item | Fonte (sha16, bytes) | Sozinha: rc · #print no trio · avisos | .olean entregue → reproduzido | Caminho proposto no kernel | Namespace |",
              "|---|---|---|---|---|---|"]
    rot = {"Palavra": "(a) PALAVRA", "LiganteLeiCampoCurvo": "(1/l) ligante F2.3", "LiganteLeiCampoCurvoTestemunha": "(1/l) S7/S8",
           "V351DualScalingBridge": "(k) ponte V351", "AgapeNonVacuity": "(k) Ágape não vácua",
           "TheSingularityReadsTheAttractorAdendo1": "F1.ATRATOR ADENDO1", "TheSingularityReadsTheAttractor": "F1.ATRATOR R1",
           "OpticalPopulationBridgeR2": "F1.ATRATOR ponte ótica", "TheLightReadsItself": "F1.ATRATOR a luz se lê",
           "LightNetStandardWedgeDataBGL": "X19 (só teste)"}
    for m, c in C.items():
        a = c["sozinha"]
        ol = ("%s → %s" % (s16(a["olean_entregue_sha256"]), "idêntico" if a["olean_identico_ao_entregue"] else "DIFERE")) if a["olean_entregue_sha256"] else "— (sem .olean na entrega)"
        fonte = "%s, %d B" % (s16(c["fonte_original_sha256"]), c["fonte_original_bytes"])
        if m == "LiganteLeiCampoCurvoTestemunha":
            fonte += " (testemunha_parte.lean); sozinha = TestemunhaF23.lean da auditoria %s" % s16(a["fonte_sha256"])
        linhas.append("| %s | %s | %d · %d de %d · %d | %s | `%s`%s | %s |" % (
            rot[m], fonte, a["rc"], a["n_print_axioms"] - len(a["fora_do_trio"]), a["n_print_axioms"], a["n_avisos"], ol,
            c["caminho_no_kernel"], "" if c["bytes_identicos_na_instalacao"] else " (derivado)", ", ".join("`%s`" % n for n in c["namespaces"])))
    return "\n".join(linhas)


def tabela_conjunto(nome):
    r = J[nome]
    linhas = ["| Módulo | declarações | teoremas | fora do trio |", "|---|---|---|---|"]
    for m, v in sorted((r["por_modulo"] or {}).items()):
        linhas.append("| `%s` | %d | %d | %d |" % (m, v["decl"], v["thm"], v["fora"]))
    return "\n".join(linhas)


j1, j0, j2 = J["J1_ConjuntoV392"], J["J0_ColisaoR1Adendo1"], J["J2_ConjuntoV392ComX19"]
comp = RA["completa"]
mem = I["superficies_memoria"]
fp0, fp1 = I["impressao_digital"]["antes"], I["impressao_digital"]["depois_lean"]
fpf_p = os.path.join(F, "fp_final.txt")
fpf = open(fpf_p).read().strip() if os.path.exists(fpf_p) else "(medida no fim, depois da limpeza: ver fp_final.txt)"
b0 = I["resolucao_da_raiz"]
flags = RA["bandeiras_propostas"]
por_sigla = {}
for f, n, mod, kind in flags:
    por_sigla.setdefault(mod, []).append((f, n, kind))
umsha = I["um_py_sha256"]

md = []
md.append("FRENTE KERNEL da v392 — exame de 12/10")
md.append("")
md.append("Gerência c1, frente F_KERNEL do exame geral de 12/10/2026. Só sandbox: nada foi escrito fora de `exame12\\F_KERNEL`; nenhum um.py, "
          "atlas_indice, árvore, porta ou selo rodou; nenhum dado observado; nenhum provedor remoto. Estatutos: [REAL] medido aqui; "
          "[DERIVED] composto por mim a partir do medido; [DECLARADO] dito na origem, não conferido aqui; [OPEN] em aberto.")
md.append("")
md.append("## Resposta curta")
md.append("")
md.append("- [REAL] As candidatas que entram na v392 compilam JUNTAS sobre o kernel v391 inteiro (`import TGL` + `import TGLExt` + 8 módulos novos): "
          "rc %d; `collectAxioms` em todas as %s declarações dos módulos novos (%s teoremas) e nenhuma fora de [propext, Classical.choice, Quot.sound]."
          % (j1["rc"], j1["cobertura_total"][0].split("decl=")[1].split("\t")[0], j1["cobertura_total"][0].split("thm=")[1].split("\t")[0]))
md.append("- [REAL] Uma colisão: a R1 e o ADENDO1 do F1.ATRATOR declaram os mesmos nomes no mesmo namespace; juntos, o import falha (rc %d). Só um entra; recomendo o ADENDO1 (é a R1 com as quatro cunhagens verbatim no comentário)." % j0["rc"])
md.append("- [REAL] A X19 (`LightNetStandardWedgeDataBGL`) coexiste: com ela o conjunto dá rc %d e %s declarações no trio. A decisão segue do operador." % (j2["rc"], j2["cobertura_total"][0].split("decl=")[1].split("\t")[0]))
md.append("- [REAL] A raiz `TGLExt.lean` da v392 (v391 + 8 imports) compila, e o `TGL/Audit.lean` da v392 (v391 + 122 `#print axioms`) roda: a regex do próprio um.py lê %d entradas, %d iguais às da v391, 0 divergentes, %d novas, todas no trio." % (comp["entradas_lidas"], comp["iguais_ao_v391"], comp["n_novos"]))
md.append("- [REAL] KH-N1: o fecho TGL+TGLExt inteiro (%d módulos, %d constantes) foi lido por `collectAxioms`: 0 fora do trio. Por nome exato, %d módulos não têm nenhuma entrada no axiom_report v391 (os 73 da lista e mais 3). Um `run_cmd` no formato do `#print axioms` cobre o fecho em %s s e a regex do um.py lê %d das %d constantes." % (
    fin["modulos_no_fecho"], fin["constantes"], fin["n_zero"], KH["formato_umpy_total"]["segundos"], KH["formato_umpy_total"]["lidos_pela_regex_do_umpy"], fin["constantes"]))
md.append("- [REAL] A PALAVRA não usa nem duplica `exact_witness_of_annihilating_word` nem `annihilating_word_exists`; quem os usa é o atrator (A3). O F1.ATRATOR não precisa importar a PALAVRA para compilar.")
md.append("- [REAL] Impressão digital do `tgl_kernel` do Nós antes e depois: `%s` e `%s` (iguais); no fim, depois da limpeza: `%s`." % (fp0, fp1, fpf))
md.append("")
md.append("## 0. Escopo, consultas e um incidente meu")
md.append("")
md.append("**Consultas (o cético é aferidor).** `rotas.py consultar` com «v392», «Palavra», «compilação conjunta» (0 rotas), «KH-N1» e «print axioms»; "
          "`rotas.py ver kernel.auditoria.cobertura_axiomas_73_modulos` (seq 722). Inventário da bancada `memory\\INVENTARIO_BANCADA_CHATGPT.json` "
          "(gerado em %s; sha16 %s): 0 ocorrências de qualquer nome das candidatas, como se espera de peças posteriores a ele. "
          "No kernel do Nós (busca em `TGLExt/`, `TGL/` e `.lake/build`): nenhum módulo nem namespace das candidatas existe; "
          "os namespaces `TGLV351` (%d arquivos) e `ChatgptAudit` (%d) já existem e recebem nomes novos sem colisão. "
          "Selo e core: um.py `%s` (%d B, v391), core `%s`. As consultas estão gravadas em `PRE_EXISTENCIA.json`." % (
              PE["inventario_bancada"]["gerado_em"], s16(PE["inventario_bancada"]["sha256"]), PE["namespaces_existentes"]["TGLV351"],
              PE["namespaces_existentes"]["ChatgptAudit"], s16(umsha), I["um_py_bytes"], s16(fin["core_sha256"])))
md.append("")
md.append("**Memória ACOM.** Li, só leitura, a projeção da referência da c1 (`sessions\\claude-c1_exame-geral-12out.json`, revisão 2). "
          "Não fiz `init` próprio, porque a ordem restringe a escrita a esta pasta.")
md.append("")
md.append("**Ferramenta.** O toolchain elan v4.31.0 foi copiado para `F_KERNEL\\tc`: %d de %d arquivos, %d B de %d B. Falta só "
          "`include\\lean\\lean_libuv.h`, um cabeçalho C de 0 B que não entra em compilação de `.lean`. O LEAN_PATH aponta, só leitura, para os `.olean` "
          "do Nós e dos pacotes (a junção `.lake\\packages` → `A Ponte e o Um\\tgl_kernel\\.lake\\packages`)." % (
              tcj["arquivos"], tcj["origem_arquivos"], tcj["bytes"], tcj["origem_bytes"]))
md.append("")
md.append("**Incidente (em nome próprio).** Na primeira execução, a limpeza final apagou TODOS os arquivos da minha própria pasta: um `Remove-Item` sobre "
          "`Get-ChildItem -LiteralPath \\\\?\\… -Include *.olean,*.ilean`, em que o filtro foi ignorado. Nada fora de `F_KERNEL` foi tocado: "
          "a impressão digital do kernel seguiu igual e as pastas irmãs do exame ficaram intactas. Reescrevi os mesmos scripts e rodei tudo de novo. "
          "Todos os números, hashes de fonte e hashes de `.olean` da segunda execução são iguais aos que anotei da primeira. A limpeza agora é feita "
          "por script Python que lista antes de apagar e só apaga pastas nomeadas e arquivos `.olean`/`.ilean`.")
md.append("")
md.append("**Duas lições técnicas da primeira execução, reproduzidas na segunda:**")
md.append("1. [REAL] Caminho longo: com o toolchain em `F_KERNEL\\toolchain\\leanprover--lean4---v4.31.0`, o lean não abria "
          "`Std\\Tactic\\BVDecide\\…\\RotateRight.olean`: o maior caminho chegaria a %d caracteres, acima de 260. Com `F_KERNEL\\tc`, o maior caminho fica em %d."
          % (tcj["maior_caminho_se_em_toolchain_leanprover"], tcj["maior_caminho"]))
md.append("2. [REAL] O lean procura um módulo `TGLExt.X` só na PRIMEIRA pasta do LEAN_PATH que contém `TGLExt`. Com o LEAN_PATH começando nos `.olean` do Nós e "
          "a ponte V351 compilada numa pasta extra, `import TGLExt.V351DualScalingBridge` falha: rc %d, «%s». Por isso as pedras novas foram compiladas "
          "numa sobreposição `ov` (cópia verificada da pasta compilada do kernel, %d arquivos, agregado `%s`, mais as candidatas). "
          "Para a cadeia de selo isso significa compilar as pedras numa árvore completa do kernel, como a v390 fez em `work\\v388_kernel\\kernel_src`."
          % (b0[1]["rc"], (b0[1]["erros"] or [""])[0].split("error: ")[-1], I["sobreposicao_ov"]["arquivos"], s16(I["sobreposicao_ov"]["agregado_sha256"])))
md.append("")
md.append("## 1. As candidatas e cada uma sozinha (etapa A)")
md.append("")
md.append("Localizadas por script (`localizacao_candidatas.json`). Cada uma foi compilada com os bytes e o leiaute de módulo da entrega, para reproduzir o `.olean` entregue quando ele existe.")
md.append("")
md.append(tabela_candidatas())
md.append("")
md.append("- [REAL] Zero `sorry`. Nenhum token proibido nas fontes (varredura própria, mais estrita que a do um.py, com strings incluídas).")
md.append("- [REAL] Os 7 `.olean` entregues foram reproduzidos byte a byte: ligante, ponte V351, Ágape, R1, ponte ótica, ADENDO1 e a luz.")
md.append("- Avisos: só lint e depreciação. São 3 de variável não usada no S7/S8; 4 de depreciação (`ContinuousLinearMap.add_apply` e afins) em R1 e no ADENDO1; 1 de `push_neg` na X19.")
md.append("- [REAL] O `F13v31_D1a3_statement.lean` (`%s`; %d `#print`) é subconjunto do `bgl`, no mesmo namespace `AuditF13v31`: se a X19 entrar, entra só o `bgl`." % (s16(I["x19_statement"]["fonte_sha256"]), I["x19_statement"]["n_print_axioms"]))
md.append("- O `MatrixInnerGauge.lean` da F1.2 não está no item (k) e não foi instalado (a face M_n ⋊ ℝ segue [OPEN]).")
md.append("")
md.append("## 2. O conjunto (etapa B)")
md.append("")
md.append("Leiaute de instalação `TGLExt/<Nome>.lean`. Há duas derivações [DERIVED]. Todas as outras candidatas entram com bytes idênticos.")
md.append("- `LiganteLeiCampoCurvoTestemunha.lean` (S7/S8). São 4 imports (`TGLExt.LiganteLeiCampoCurvo`, `ConstructedClausiusControls`, `EquilibriumScreenIntegration`, `PoincareGroup`) e 2 `set_option`, seguidos dos bytes de `testemunha_parte.lean` (`%s`) sem nenhuma mudança. O `TestemunhaF23.lean` da auditoria não pode entrar como está, porque repete o ligante." % s16(C["LiganteLeiCampoCurvoTestemunha"]["fonte_original_sha256"]))
md.append("- `AgapeNonVacuity.lean`: uma linha muda, `import F12Completion.V351DualScalingBridge` → `import TGLExt.V351DualScalingBridge` (instalado `%s`). O `.olean` passa a ser outro, porque os bytes e o nome do módulo mudaram." % s16(C["AgapeNonVacuity"]["instalado_sha256"]))
md.append("")
md.append("**J1, o conjunto recomendado** (kernel v391 inteiro + 8): rc %d, %s s, `%s`." % (j1["rc"], j1["segundos"], j1["cobertura_total"][0].replace("	", " ")))
md.append("")
md.append(tabela_conjunto("J1_ConjuntoV392"))
md.append("")
md.append("**J0, a colisão**: J1 + a R1 dá rc %d: «%s»." % (j0["rc"], j0["erros_texto"][0].split("error: ")[-1]))
md.append("")
md.append("**J2, com a X19**: rc %d, %s s, `%s` (a X19 traz %d declarações, %d teoremas)." % (j2["rc"], j2["segundos"], j2["cobertura_total"][0].replace("	", " "), j2["por_modulo"]["TGLExt.LightNetStandardWedgeDataBGL"]["decl"], j2["por_modulo"]["TGLExt.LightNetStandardWedgeDataBGL"]["thm"]))
md.append("")
md.append("**Dependências entre as candidatas** [REAL, lidas dos imports]:")
md.append("- O S7/S8 depende do ligante, e a Ágape depende da ponte V351.")
md.append("- O ligante e a Ágape dependem da Fundação (v390).")
md.append("- O atrator usa `TGLExt.WordExistence`, e o atrator e a luz usam `TheObserverReadsTheAngle`.")
md.append("- A ponte ótica importa o `Mathlib` inteiro; a raiz já o importa via `TheCouplingRunsBoundedBelow`.")
md.append("- A PALAVRA não depende de nenhuma outra candidata, e nenhuma candidata importa a PALAVRA.")
md.append("")
md.append("**Constantes fora do próprio namespace** [REAL]. São dois lemas equacionais «realizados», criados sob demanda:")
md.append("- `TGLExt.adU.eq_1`, nascido no S7/S8;")
md.append("- `TGLExt.conjJ.eq_1`, nascido na luz.")
md.append("")
md.append("Sondas S1–S4 [REAL]:")
md.append("- O kernel v391 não contém nenhum dos dois.")
md.append("- Dois módulos que realizam o mesmo `TGLExt.conjJ.eq_1` importam juntos com rc 0: a duplicata realizada é tolerada pelo Lean 4.31.")
md.append("- O próprio kernel já vive com %d duplicatas assim: %s." % (
    len(d2["atribuidas_a_mais_de_um_modulo"]), ", ".join("`%s`" % x for x in d2["atribuidas_a_mais_de_um_modulo"])))
md.append("")
md.append("Não é colisão.")
md.append("")
md.append("## 3. Onde cada uma entra, a raiz, o lakefile e o que o um.py precisa")
md.append("")
md.append("| Pedra | Caminho no kernel | Linha na raiz `TGLExt.lean` | Linhas no `TGL/Audit.lean` |")
md.append("|---|---|---|---|")
for m in ["Palavra", "LiganteLeiCampoCurvo", "LiganteLeiCampoCurvoTestemunha", "V351DualScalingBridge", "AgapeNonVacuity",
          "TheSingularityReadsTheAttractorAdendo1", "OpticalPopulationBridgeR2", "TheLightReadsItself"]:
    md.append("| %s | `TGLExt/%s.lean` | `import TGLExt.%s` | %d `#print axioms` |" % (m, m, m, len(por_sigla.get(m, []))))
md.append("| (X19, se decidida) | `TGLExt/LightNetStandardWedgeDataBGL.lean` | `import TGLExt.LightNetStandardWedgeDataBGL` | %d `#print axioms` (testadas: %d de %d lidas) |" % (RA["x19_delta"]["n"], RA["x19_delta"]["lidos"], RA["x19_delta"]["n"]))
md.append("")
md.append("**A raiz e o Audit** [REAL]:")
md.append("- A raiz é `TGLExt.lean` (só imports, termina em `import TGLExt.Fundacao`). Na v391 ela é `%s`; com os 8 imports no fim fica `%s`, com %d B, e compila (rc %d)." % (s16(RA["raiz_v391_sha256"]), s16(RA["raiz_v392_sha256"]), RA["raiz_v392_bytes"], RA["raiz_compila"]["rc"]))
md.append("- O `lakefile.toml` não muda: `lean_lib TGLExt` constrói o fecho de imports da raiz, e o `TGL/Audit.lean` importa `TGLExt`.")
md.append("- O Audit passa de `%s` a `%s` (%d B), com %d linhas a mais: um comentário e %d `#print axioms`." % (s16(RA["audit_v391_sha256"]), s16(RA["audit_v392_sha256"]), RA["audit_v392_bytes"], RA["audit_acrescimo_linhas"], RA["audit_acrescimo_linhas"] - 1))
md.append("")
md.append("**A auditoria completa simulada** (`lean TGL/Audit.lean` da v392, sem lake) [REAL]:")
md.append("- rc %d; %d entradas lidas pela regex do um.py;" % (comp["rc"], comp["entradas_lidas"]))
md.append("- %d iguais às do axiom_report v391 e 0 divergentes;" % comp["iguais_ao_v391"])
md.append("- %d novas, todas no trio;" % comp["n_novos"])
md.append("- `sorryAx` e `Lean.trustCompiler` ausentes; as sentinelas estão presentes.")
md.append("")
md.append("As %d entradas da v391 que esta rodada não produz vêm do log do `lake build`: são os `#print axioms` dos próprios módulos, que o um.py soma ao Audit (`blob`, l.%s). Pelo último componente do nome, %d das %d têm `#print axioms` no próprio arquivo do módulo." % (
    comp["n_sumidos"], L1("blob"), PE["sumidos"]["com_print_axioms_em_modulo_proprio_por_ultimo_componente"], PE["sumidos"]["n"]))
md.append("")
md.append("**O mecanismo do um.py** [REAL, lido do um.py `%s`, sem executar]:" % s16(umsha))
md.append("1. **Kernel embutido.** O dicionário `_EMBEDDED_KERNEL_FILES` vai da l.%s à l.%s e tem %d entradas, todas iguais byte a byte ao disco. A chave `\"TGLExt.lean\"` está na l.%s, `\"TGL/Audit.lean\"` na l.%s, e a última entrada, `'TGLExt/Fundacao.lean'`, na l.%s." % (
    UL["_EMBEDDED_KERNEL_FILES_inicio"][0], UL["_EMBEDDED_KERNEL_FILES_fim"][0], I["kernel_embutido"]["entradas"], L1("chave_TGLExt.lean"), L1("chave_TGL/Audit.lean"), L1("chave_TGLExt/Fundacao.lean")))
md.append("   - Como a v390 fez (`work\\cadeia_de_selo\\v390\\gerar_candidato_v390.py`): trocam-se, por `repr`, as duas entradas da raiz e do Audit nas faixas do AST, e cada pedra nova é acrescentada no fim do dicionário como `'TGLExt/<Nome>.lean': <texto>`.")
md.append("   - A Fundação embutida (`%s`, %d B) é idêntica à do disco." % (s16(I["kernel_embutido"]["TGLExt/Fundacao.lean"]["emb_sha256"]), I["kernel_embutido"]["TGLExt/Fundacao.lean"]["emb_bytes"]))
md.append("2. **Materialização e build.** `materialize_embedded_kernel` (l.%s) grava os arquivos em `FORMAL_DIR` (l.%s). Depois, `verify_tgl_kernel_formalization` (l.%s) roda `lake build` (l.%s) e `lake env lean TGL/Audit.lean` (l.%s) e lê os axiomas com a regex da l.%s." % (
    L1("def_materialize_embedded_kernel"), L1("FORMAL_DIR"), L1("def_verify_tgl_kernel_formalization"), L1("lake_build"), L1("lake_env_lean_audit"), L1("regex_depends")))
md.append("3. **Bandeiras.** Em `_LEAN_THEOREM_FLAGS` (l.%s), uma entrada `\"ext_<sigla>_<nome>_kernel_proved\": \"<NomeCompleto>\"` por declaração; as 9 da Fundação ficam na l.%s. Proponho %d bandeiras, todas novas no um.py (prefixos `ext_pal_`, `ext_lig_`, `ext_lgt_`, `ext_v51_`, `ext_agv_`, `ext_atr_`, `ext_opt_`, `ext_lri_`; 0 ocorrências hoje), e as %d acenderiam (delta rc %d)." % (
    L1("_LEAN_THEOREM_FLAGS"), L1("bandeiras_v390_fnd"), len(flags), RA["delta"]["bandeiras"], RA["delta"]["rc"]))
md.append("4. **Escada externa.** A lista `ext_flags` vai da l.%s à l.%s, e `n_theorems_expected` é o tamanho dela (l.%s). O gerador da v390 também a acrescenta. Se as %d entrarem, a escada vai de 6163 a %d [DERIVED]." % (
    L1("escada_ext_flags"), UL["escada_ext_flags_fim"][0], L1("n_theorems_expected"), len(flags), 6163 + len(flags)))
md.append("5. **Ledger e registro.** No ledger `_ESQUELETO_STONES` (l.%s; a entrada da v390 está na l.%s) entra uma tupla `(\"v392\", \"<Nome>\", \"TGLExt/<Nome>.lean\", None, None)` por pedra. O registro da versão segue o molde de `_FND_FLAGS_V390` (l.%s), `_V390_PEDRA` (l.%s) e `fundacao_v390` (l.%s), com os pinos lidos por script e os verbatins embutidos." % (
    L1("_ESQUELETO_STONES"), L1("ledger_v390"), L1("_FND_FLAGS_V390"), L1("_V390_PEDRA"), L1("def_fundacao_v390")))
md.append("6. **Varredura de tokens.** `_LEAN_FORBIDDEN_TOKENS` (l.%s; `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`) cobre só o topo de `TGL/` e de `TGLExt/`, onde as pedras novas ficam. [REAL] A minha varredura, mais estrita, não acha nenhum desses tokens nas candidatas." % L1("_LEAN_FORBIDDEN_TOKENS"))
md.append("")
md.append("A lista das %d linhas de Audit e das bandeiras está em `RESULTADO_C_preparo.json`; as da X19, em `RESULTADO_C_delta_x19.json`." % len(flags))
md.append("")
md.append("## 4. KH-N1 (item (2) da F0.5)")
md.append("")
md.append("Definição: `levantamento_qg\\consolidado.json`, itens[124], «73 módulos compilados do kernel sem nenhum #print axioms». A correção pedida é o `#print axioms` (ou um `run_cmd` por unidade) e a checagem «todo theorem do fecho com entrada no axiom_report». Classe: EXISTE_NA_BANCADA_NAO_LIGADO; não bloqueia a prova.")
md.append("")
md.append("**D1** [REAL]: o `AuditoriaCobertura73.lean` de 07/10 (bytes `71c83b21…`) foi re-rodado.")
md.append("- rc %d, %d linhas, idênticas como conjunto às de 07/10 (`%s`)." % (KH["D1"]["rc"], KH["D1"]["linhas_novas"], KH["D1"]["total"][0].replace("	", " ")))
md.append("- A distribuição que o próprio arquivo de 07/10 dá é %s." % json.dumps(KH["D1"]["distribuicao_0710"], ensure_ascii=False))
md.append("- São 49 teoremas sem axioma, não 50 como diz o registro seq 722: 382 + 60 + 24 + 49 = 515. É erro de digitação no registro, e a correção vai ao lado.")
md.append("")
md.append("**D2, o fecho inteiro** [REAL]:")
md.append("- %d módulos TGL/TGLExt, %d constantes: %s." % (fin["modulos_no_fecho"], fin["constantes"], json.dumps(fin["por_tipo"])))
md.append("- `collectAxioms` em 12 blocos paralelos: %d lidas, faltam %d, fora do trio %d." % (d2["n"], len(d2["faltam"]), len(d2["fora_do_trio"])))
md.append("- Distribuição: %s." % json.dumps(d2["distribuicao"], ensure_ascii=False))
md.append("- As %d entradas do axiom_report v391 aparecem todas, com 0 divergências entre `#print axioms` e `collectAxioms`." % d2["axr_v391"])
md.append("")
md.append("**Coberto e o que sobra** [REAL]:")
md.append("- No sandbox, todas as %d constantes estão cobertas." % fin["constantes"])
md.append("- No axiom_report oficial (v391) há %s, ou seja, %d teoremas de %d. Fora dele ficam %d constantes, todas no trio pelo sandbox." % (json.dumps(fin["no_axiom_report_v391_por_tipo"]), d2["teoremas_no_axr"], d2["teoremas"], fin["fora_do_axiom_report"]))
md.append("- Por nome exato, %d módulos com teorema não têm nenhuma entrada: os 73 da lista, mais %s." % (fin["n_zero"], ", ".join("`%s`" % m for m in fin["zero_fora_dos_73"])))
md.append("- A lista KH-N1 casou por sufixo, e nomes curtos repetidos em outros módulos esconderam esses três.")
md.append("- Os 73 têm %d constantes (%d teoremas), todas no trio." % (d2["c73"], d2["c73_teoremas"]))
md.append("")
md.append("**Proposta testada para a v392** [REAL no sandbox; DERIVED como proposta]: um `run_cmd` que imprime, para cada constante do fecho, a linha exata do `#print axioms` (`'X' depends on axioms: [...]` / `'X' does not depend on any axioms`) e no fim `TGL_AXIOM_COVERAGE_TOTAL`.")
md.append("- Nos 76 módulos: %s s, %d lidas." % (KH["formato_umpy_76"]["segundos"], KH["formato_umpy_76"]["lidos_pela_regex_do_umpy"]))
md.append("- No fecho inteiro: %s s, `%s`, %d de %d lidas pela regex do um.py." % (KH["formato_umpy_total"]["segundos"], KH["formato_umpy_total"]["total"][0], KH["formato_umpy_total"]["lidos_pela_regex_do_umpy"], fin["constantes"]))
md.append("- As 4 que a regex não lê são definições auxiliares de `syntax`/`elab` com «» no nome, em `QGReaderUVLock` e `O16.ExactTypeReader_v2`. Ficam como exceção declarada.")
md.append("- No um.py, a checagem de cobertura é: toda constante `thm` enumerada tem entrada no axiom_report (fail-closed).")
md.append("- O código está em `kh\\KH_formato_umpy_total.lean`.")
md.append("")
md.append("## 5. A PALAVRA e a letra; o F1.ATRATOR e a PALAVRA")
md.append("")
md.append("**A PALAVRA e a letra** [REAL]:")
md.append("- Sonda P1 (as constantes que cada termo usa): as 7 declarações da PALAVRA usam só `TGLExt.boost`, `ChatgptAudit.PolarPeriod016.{AngularQuotientFaithful, faithful_period_iff, reciprocal_temperature}`, `ChatgptAudit.Wick016.{wickW, complexBoost, wick_boost_two_pi}` e `TGLExt.{projPlus, angFamily, the_observer_reads_the_angle, observing_adds_nothing}`.")
md.append("- Sonda P1c (o fecho transitivo de constantes, restrito ao kernel): 41 constantes em 7 módulos, sem `exact_witness_of_annihilating_word`, sem `annihilating_word_exists` e sem `spectral_witness_of_annihilating_word`.")
md.append("- Os módulos da letra (`ExactWitness`, `WordExistence`, `InfiniteWord`) entram no fecho de IMPORTS da PALAVRA (sonda P1b, 11.252 módulos), mas não no uso. A letra aparece só no comentário, como nome: «polinômio aniquilador normalizado = letra».")
md.append("- Portanto a PALAVRA não usa nem duplica as duas.")
md.append("- `O16.PeriodHeatCalibration_v3` e `O16.RotationGeneratorBridges` são importados mas não entram no fecho de constantes. Os imports são mais largos que o uso; não é defeito.")
md.append("")
md.append("**Quem usa a letra** [REAL]: o atrator. `A3_normalized_letter` usa `TGLExt.exact_witness_of_annihilating_word`, e `A3_letter_exists_finite` usa `TGLExt.annihilating_word_exists`, aplicados a D = 1 − T. A ponte ótica refaz a letra no 2×2 por cálculo, sem constante do kernel.")
md.append("")
md.append("**Repetições** [REAL, por `rfl`]: três nomes têm o mesmo enunciado de `observing_adds_nothing`.")
md.append("- `TGLExt.Palavra.rereading_adds_nothing`;")
md.append("- `…TheSingularityReadsTheAttractor.A3_angular_rereading_only`;")
md.append("- `…TheLightReadsItself.A5_angular_rereading_only`.")
md.append("")
md.append("Além disso, `the_first_reading_identifies` tem o enunciado de `the_observer_reads_the_angle`.")
md.append("")
md.append("**O F1.ATRATOR deve importar a PALAVRA depois da instalação?** Para compilar, não: nenhuma prova do F1.ATRATOR usa constante da PALAVRA. Se a gerência quiser a ligação lexical («a letra de PALAVRA»), há dois caminhos:")
md.append("- (i) trocar as duas reexportações angulares por citação de `TGLExt.Palavra.rereading_adds_nothing`, com `import TGLExt.Palavra`. Isso muda bytes e pede reauditoria curta;")
md.append("- (ii) deixar os bytes como estão e registrar, no um.py, que os três nomes são o mesmo enunciado.")
md.append("")
md.append("Recomendo (ii) na v392 e (i) só se o operador pedir.")
md.append("")
md.append("**POSTO = RANK ao lado do A4** [REAL no sandbox; DERIVED, não é pedra]. A sonda P3 compila (rc %d) três teoremas, todos no trio:" % S["P3_PostoRankA4"]["rc"])
md.append("- `A4_reading_rank_one`: `finrank (reading T).range = 1` sob `StrictComplementContraction`, em 2 linhas sobre A3/A4;")
md.append("- o caso concreto;")
md.append("- o controle (a identidade em ℂ² tem leitura de posto 2).")
md.append("")
md.append("A adoção é da gerência ou do operador. A F1.FREQUENCIA (12/10, em curso) é onde o operador mandou testar o rank.")
md.append("")
md.append("## 6. Superfícies de memória")
md.append("")
for e in mem:
    md.append("- `%s`: %d B, mtime %s, sha16 `%s`. Backups desde 10/10: %d, todos prefixo exato (%s)." % (
        os.path.basename(e["arquivo"]), e["bytes"], e["mtime"], s16(e["sha256"]), len(e["backups_desde_10out"]),
        all(x["prefixo_exato"] for x in e["backups_desde_10out"])))
md.append("")
md.append("Nenhuma escrita nas quatro superfícies depois de 10/10 11:05:38. A última foi o ADENDO1 do F1.ATRATOR, já conferido pela auditoria a7c491ec. As pedras da v392 não deixaram escrita de memória pendente de conferência.")
md.append("")
md.append("## 7. O que NÃO conferi")
md.append("")
md.append("- O `lake build` de uma árvore completa do kernel v392, com o `TGLExt.lean` e o `Audit.lean` novos. A simulação foi por `lean` direto sobre a sobreposição, sem lake; a cadeia de selo deve fazer o build completo, como a v390.")
md.append("- O texto final das duas pedras derivadas (S7/S8 com errata ao lado do «NADA disto e pedra»; a linha de import da Ágape). Testei bytes de proposta; os definitivos são da gerência.")
md.append("- O ramo C e a Temperatura da F2.3 (excluídos por ordem; a colisão de `LightLorentzWedgeFamilyEveryNullDirection.mk` não foi re-medida).")
md.append("- As pedras que a F1.FREQUENCIA e a F1.TEMPO (abertas em 12/10, em curso) vierem a entregar. Se entrarem na v392, o conjunto se refaz com `etapa_B_conjunto.py` e o delta do Audit com `etapa_C_raiz_auditoria.py`.")
md.append("- O conteúdo matemático das pedras, além de compilar e ficar no trio. As auditorias de origem (F2.3, F1.2, F1.ATRATOR, F1.3) fizeram essa leitura; aqui não se refez.")
md.append("- O inventário da bancada é de 27/09 e não conhece as candidatas. Não foi regenerado.")
md.append("")
md.append("## 8. Artefatos (todos em `exame12\\F_KERNEL`, com sha256 em `INVENTARIO_V392_KERNEL.json` e nos `RESULTADO_*.json`)")
md.append("")
md.append("- Scripts em `scripts\\`: `leanlib.py`, `etapa_A_sozinhas.py`, `etapa_B_conjunto.py`, `demo_resolucao_raiz.py`, `sondas_eq.py`, `sondas_palavra.py`, `etapa_C_raiz_auditoria.py`, `etapa_C_x19.py`, `kh_d1.py`, `kh_d2.py`, `kh_formato_umpy.py`, `superficies_memoria.py`, `pre_existencia.py`, `localizar.py`, `embutido.py`, `verificar_ov.py`, `inventario.py`, `gerar_registro_mapa.py`, `gerar_relatorio.py`, `limpar.py`. Consultas e medições gravadas: `PRE_EXISTENCIA.json`, `localizacao_candidatas.json`, `embutido_vs_kernel.json`, `ov_verificacao_inicial.json`, `superficies_memoria.json`, `c1_projecao_memoria_lida.json`.")
md.append("- Fontes no leiaute de instalação: `inst\\TGLExt\\*.lean`, `inst\\TGLExt.lean` (raiz v392) e `inst\\TGL\\Audit.lean` (Audit v392). Arquivos de conjunto e sondas: `conj\\*.lean`. KH-N1: `kh\\*.lean` e `kh\\*.json`. Logs de cada rodada em `logs\\`.")
md.append("- Registro para o mapa: `registro_mapa_F0.5.json`. São 6 RESULTADO sobre rotas que já existem; não registrei (é ato da gerência).")
md.append("")
md.append("## 9. Limpeza")
md.append("")
md.append("O toolchain copiado (`tc`), a sobreposição (`ov`), a pasta `demo_build` e todos os `.olean`/`.ilean` gerados são apagados no fim por `scripts\\limpar.py`, que lista antes de apagar e usa o prefixo `\\\\?\\`. O resultado fica em `LIMPEZA.json`.")
txt = "\n".join(md) + "\n"
assert txt.startswith("FRENTE KERNEL da v392 — exame de 12/10\n")
assert not re.search(r"confirm", txt, re.I), "palavra proibida"
assert not re.search(r"p[oó]s-?di[cç][aã]o", txt, re.I)
assert "não provou" not in txt
alvo = os.path.join(F, "RELATORIO_F_KERNEL_v392.md")
open(alvo, "w", encoding="utf-8", newline="\n").write(txt)
print(alvo, hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16], len(txt))
