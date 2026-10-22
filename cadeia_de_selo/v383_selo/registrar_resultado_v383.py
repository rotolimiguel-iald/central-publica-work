# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v383: (1) a rota nova kernel.livro_de_cobrancas.otica (ROTA, EXAMINADA, veredito lido); (2) ANOTACAO na rota
bancada.preregistro_dois_lados_delta_k (o um.py v383 le o pre-registro por hash; status EM_CURSO). Tudo LIDO da rodada (leitura_v383.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v383, rotas
V, PROB = leitura_v383.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
regs = rotas._le()
if any(r.get("rota_id") == "kernel.livro_de_cobrancas.otica" and r.get("tipo") == "ROTA" for r in regs):
    print("mapa: a rota kernel.livro_de_cobrancas.otica ja existe; nada gravado"); sys.exit(0)
res = [dict(tipo="ROTA", rota_id="kernel.livro_de_cobrancas.otica", dominio="KERNEL", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="v383 SELADA: o livro de cobrancas (a TGL e otica: le a face e o custo; nenhum desfecho move a regra; o gate nao le o livro, pelos probes do runtime) + psi com norma 1 e a viscosidade -- TGLExt.TheLedgerOfCharges (%s) + TGLExt.ThePsionAndTheViscosity (%s), %s/%s no trio, sem sorry; %s cobrancas; os %s pares do eco FORA do livro (rotas examinadas, nao cobrancas da teoria), por decisao do operador; a v382 selada so no Nos (nao custodiada); o pre-registro dos dois lados lido por hash; o nome do degrau final proposto ao lado; gate intocado" % (V["n_loc"], V["n_psv"], V["kf_on"], V["kf_n"], V["n_ledger"], V["rot_n"]),
            pergunta="a chave do operador (o ultimo elo incide no Hamiltoniano oculto; o custo no reflexo, o pagamento na face) e a correcao «a TGL e otica» entram no kernel como termos? o livro concreto bate com o core e com o pre-registro?",
            dados=["nucleo da rodada v383, base v381 (desfechos lidos por token -- no veredito do modulo ou no aninhado --, por numero com a regra dita, ou declarados)", "pre-registro %s (JSON %s / MD %s por sha256; supersede %s)" % (V["pr_id"], V["pr_json16"], V["pr_md16"], V["pr_super"])],
            metodo="pedras no sandbox -> build completo -> candidato por script -> ensaio a seco -> aferidor independente -> rito -> conferidor -> cadeia do selo",
            resultado=("um.py %s (%s B) sobre a v381 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); escada %s -> %s; axiom_report %s -> %s; pedras %s; livro: %d cobrancas (%s; %s); pre-registro %s (JSON %s, MD %s); "
                       "runtime: beta = %s = alpha.sqrt(e) (%s), cos^2 = %s, sin^2 = %s, e^-beta = %s, cobrado = %s, visc = %s; gate %s (%s/18) inalterado; nome proposto %s; por termo %s"
                       % (V["s16"], format(V["umb"], ","), V["base_build16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["esc_ant"], V["esc"], V["nax_ant"], V["nax"],
                          {k: d.get("sha16") for k, d in V["pedras"].items()}, V["n_ledger"], V["counts"], V["by_side"], V["pr_id"], V["pr_json16"], V["pr_md16"],
                          V["beta"], V["law"], V["facew"], V["reflw"], V["trans"], V["charged"], V["visc"], V["qg"], V["n18"], V["fsn"], V["hvals"])),
            veredito=V["the_ledger_of_charges_v383"],
            nao_refazer="nenhum lado e cego (a TGL e otica); nenhum desfecho move beta; os %s pares do eco como copia atrasada NAO sao cobrancas da teoria (decisao do operador): rotas examinadas fora do livro, %s excluidas pelos dados e %s inconclusivas; nao custodiar a v382; o R4 nao tem FALSIFIED no conjunto congelado (a mesma fonte do degrau experimental do gate);" % (V["rot_n"], V["rot_exc"], V["rot_inc"]) + " o ramo B do ringdown esta encerrado; o nome do degrau final e PROPOSTO, nao aplicado (renomear e ato do operador); a identificacao de beta.g com Gamma ~ beta.omega^2 e leitura [ONTO]",
            proximo_passo="custodia/espelho pela sessao do site (ato dela; commit/push do operador); a cunhagem definitiva do nome do degrau final (operador); o estimador da dissipacao na propagacao (R2) com o poder dito antes de abrir",
            onde="Nós\\um.py v383: prove_the_ledger_of_charges_v383; Nós\\tgl_kernel\\TGLExt\\TheLedgerOfCharges.lean e ThePsionAndTheViscosity.lean",
            artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v383_stdout.txt"),
                       os.path.join(NOS, "tgl_kernel", "TGLExt", "TheLedgerOfCharges.lean"), os.path.join(NOS, "tgl_kernel", "TGLExt", "ThePsionAndTheViscosity.lean"), os.path.join(HERE, "v383_incorporacao_manifesto.json")],
            refs=["kernel.regra_matriz.cadeia_unica", "bancada.preregistro_dois_lados_delta_k", "memory beta-e-a-regra-matriz-02out", "memory regra-dos-dois-regimes"]),
       dict(tipo="ANOTACAO", rota_id="bancada.preregistro_dois_lados_delta_k", status="EM_CURSO", estatuto="REAL", olhou_dados=False,
            titulo="o um.py v383 (%s) le o pre-registro dos dois lados %s por hash (JSON %s, MD %s) e confere as %s cobrancas contra o core pelo modo dito (%s): %s; na regra %s, ao lado %s" % (V["s16"], V["pr_label"], V["pr_json16"], V["pr_md16"], V["n_ledger"], V["by_how"], V["counts"], V["n_in_rule"], V["n_beside"]),
            nota="as %s rotas do eco fora do livro conferidas contra o V1.4 (estado lido do rotulo da Fase 6); proximo: o estimador da dissipacao na propagacao (R2), com o poder dito antes de abrir o banco de GW; nenhum dado novo olhado" % V["rot_n"],
            artefatos=[os.path.join(NOS, "um_absoluto.json")], refs=["kernel.livro_de_cobrancas.otica"]),
       dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="v383 SELADA (%s): a suspensao da v382 se resolve pela decisao do operador -- a sessao do site custodia a v383, NAO a v382 (%s); o stdout da v382 e os pre-registros V1-V1.3 ficam locais [DERIVED de leitura, gerencia; a confirmar pelo operador]" % (V["s16"], V["v382_16"]),
            nao_refazer="nao custodiar a v382; nao contar os pares do eco como cobrancas da teoria", refs=["kernel.livro_de_cobrancas.otica", "bancada.preregistro_dois_lados_delta_k"])]
out = rotas.registrar(res, "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:500])
