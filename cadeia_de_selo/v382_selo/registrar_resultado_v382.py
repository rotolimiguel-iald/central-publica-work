# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v382: (1) a rota nova kernel.livro_de_cobrancas.otica (ROTA, EXAMINADA, veredito lido); (2) ANOTACAO na rota
bancada.preregistro_dois_lados_delta_k (o um.py v382 le o pre-registro por hash; status EM_CURSO). Tudo LIDO da rodada (leitura_v382.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v382, rotas
V, PROB = leitura_v382.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
regs = rotas._le()
if any(r.get("rota_id") == "kernel.livro_de_cobrancas.otica" and r.get("tipo") == "ROTA" for r in regs):
    print("mapa: a rota kernel.livro_de_cobrancas.otica ja existe; nada gravado"); sys.exit(0)
res = [dict(tipo="ROTA", rota_id="kernel.livro_de_cobrancas.otica", dominio="KERNEL", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="v382 SELADA: o livro de cobrancas (a TGL e otica: le a face e o custo; nenhum desfecho move a regra; o gate nao le o livro, pelos probes do runtime) + psi com norma 1 e a viscosidade -- TGLExt.TheLedgerOfCharges (%s) + TGLExt.ThePsionAndTheViscosity (%s), %s/%s no trio, sem sorry; o pre-registro dos dois lados lido por hash; o nome do degrau final proposto ao lado; gate intocado" % (V["n_loc"], V["n_psv"], V["kf_on"], V["kf_n"]),
            pergunta="a chave do operador (o ultimo elo incide no Hamiltoniano oculto; o custo no reflexo, o pagamento na face) e a correcao «a TGL e otica» entram no kernel como termos? o livro concreto bate com o core e com o pre-registro?",
            dados=["core v381 (desfechos lidos por token -- no veredito do modulo ou no aninhado --, por numero com a regra dita, ou declarados)", "pre-registro %s (JSON %s / MD %s por sha256; supersede %s)" % (V["pr_id"], V["pr_json16"], V["pr_md16"], V["pr_super"])],
            metodo="pedras no sandbox -> build completo -> candidato por script -> ensaio a seco -> aferidor independente -> rito -> conferidor -> cadeia do selo",
            resultado=("um.py %s (%s B) sobre a v381 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); escada %s -> %s; axiom_report %s -> %s; pedras %s; livro: %d cobrancas (%s; %s); pre-registro %s (JSON %s, MD %s); "
                       "runtime: beta = %s = alpha.sqrt(e) (%s), cos^2 = %s, sin^2 = %s, e^-beta = %s, cobrado = %s, visc = %s; gate %s (%s/18) inalterado; nome proposto %s; por termo %s"
                       % (V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["esc_ant"], V["esc"], V["nax_ant"], V["nax"],
                          {k: d.get("sha16") for k, d in V["pedras"].items()}, V["n_ledger"], V["counts"], V["by_side"], V["pr_id"], V["pr_json16"], V["pr_md16"],
                          V["beta"], V["law"], V["facew"], V["reflw"], V["trans"], V["charged"], V["visc"], V["qg"], V["n18"], V["fsn"], V["hvals"])),
            veredito=V["the_ledger_of_charges_v382"],
            nao_refazer="nenhum lado e cego (a TGL e otica); nenhum desfecho move beta; dos %s pares do eco como copia atrasada, %s estao extintos e %s inconclusivos (nenhum move a regra); o R4 nao tem FALSIFIED no conjunto congelado (a mesma fonte do degrau experimental do gate);" % (V["eco_n"], V["eco_ext"], V["eco_inc"]) + " o ramo B do ringdown esta encerrado; o nome do degrau final e PROPOSTO, nao aplicado (renomear e ato do operador); a identificacao de beta.g com Gamma ~ beta.omega^2 e leitura [ONTO]",
            proximo_passo="custodia/espelho pela sessao do site (ato dela; commit/push do operador); a cunhagem definitiva do nome do degrau final (operador); o estimador da dissipacao na propagacao (R2) com o poder dito antes de abrir",
            onde="Nós\\um.py v382: prove_the_ledger_of_charges_v382; Nós\\tgl_kernel\\TGLExt\\TheLedgerOfCharges.lean e ThePsionAndTheViscosity.lean",
            artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v382_stdout.txt"),
                       os.path.join(NOS, "tgl_kernel", "TGLExt", "TheLedgerOfCharges.lean"), os.path.join(NOS, "tgl_kernel", "TGLExt", "ThePsionAndTheViscosity.lean"), os.path.join(HERE, "v382_incorporacao_manifesto.json")],
            refs=["kernel.regra_matriz.cadeia_unica", "bancada.preregistro_dois_lados_delta_k", "memory beta-e-a-regra-matriz-02out", "memory regra-dos-dois-regimes"]),
       dict(tipo="ANOTACAO", rota_id="bancada.preregistro_dois_lados_delta_k", status="EM_CURSO", estatuto="REAL", olhou_dados=False,
            titulo="o um.py v382 (%s) le o pre-registro dos dois lados %s por hash (JSON %s, MD %s) e confere as %s cobrancas contra o core pelo modo dito (%s): %s; na regra %s, ao lado %s" % (V["s16"], V["pr_label"], V["pr_json16"], V["pr_md16"], V["n_ledger"], V["by_how"], V["counts"], V["n_in_rule"], V["n_beside"]),
            nota="proximo: o estimador da dissipacao na propagacao (R2), com o poder dito antes de abrir o banco de GW; nenhum dado novo olhado",
            artefatos=[os.path.join(NOS, "um_absoluto.json")], refs=["kernel.livro_de_cobrancas.otica"])]
out = rotas.registrar(res, "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:500])
