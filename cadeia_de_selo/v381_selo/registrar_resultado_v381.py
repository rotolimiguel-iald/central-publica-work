# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v381 (a rota kernel.regra_matriz.cadeia_unica, PROPOSTA -> EXAMINADA), tudo LIDO da rodada (leitura_v381.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v381, rotas
V, PROB = leitura_v381.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
res = dict(tipo="RESULTADO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL",
           titulo="v381 SELADA: a regra matriz do operador (dez nomes, nove elos: oito «havendo» ditos + a radicalização pela Meia-Nat) num só termo no kernel — TGLExt.TheMatrixRule (24 declarações, %s/%s no trio, sem sorry); o critério de parada tipado (CustoPago); a lei precede a cobrança; gate intocado" % (V["kf_on"], V["kf_n"]),
           resultado=("um.py %s (%s B) sobre a v380 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); escada %s → %s; axiom_report %s → %s; pedra %s; runtime: beta = %s = alpha.sqrt(e) (%s), theta_M = %s, sin^2 = %s, |spec| = %s, cadeia %s; "
                      "veredito %s; selo.um_version = %s; md carimbado: %s; gate %s (%s/18) intocado; por termo %s"
                      % (V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["esc_ant"], V["esc"], V["nax_ant"], V["nax"], V["pedras"].get("TheMatrixRule", {}).get("sha16"),
                         V["beta"], V["law"], V["theta"], V["refl"], V["specmod"], V["chain"], V["the_matrix_rule_v381"], V["um_version"], V["md_carimbo"], V["qg"], V["n18"], V["hvals"])),
           veredito=V["the_matrix_rule_v381"], olhou_dados=False,
           nao_refazer="beta nao se deriva DO DADO (e a regra; a forma alpha.sqrt(e) e derivada do axioma por termo, v376); os elos sao termos ja existentes em pedras anteriores (fato provado, definicao nomeada ou campo do binder; conjuncao, nao deducao); o nono elo (sinal -> registro) e a radicalizacao cujo operador e a Meia-Nat, dito pelo operador (seq 269), nao leitura da gerencia (ERRATA seq 270); a ordem e [INPUT/ONTO]; onde o elo nao tem hipotese a forma «havendo X ha Y» e ordem ontologica dita; o espectro tipado e Spec S(theta), a identificacao com Gamma ~ beta.omega^2 e leitura [ONTO]",
           proximo_passo="custodia/espelho pela sessao do site (ato dela; commit/push do operador); o estimando da Bancada sobre o espectro do gradiente (pre-registrar); as decisoes do operador (registro do H0; particao; neutrino; nome do degrau final do gate)",
           onde="Nós\\um.py v381: prove_the_matrix_rule_v381; Nós\\tgl_kernel\\TGLExt\\TheMatrixRule.lean",
           artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v381_stdout.txt"),
                      os.path.join(NOS, "tgl_kernel", "TGLExt", "TheMatrixRule.lean"), os.path.join(HERE, "v381_incorporacao_manifesto.json")],
           refs=["um_py.v380.fases_5_6_7_por_hash", "gw.eco_radical.v3", "memory beta-e-a-regra-matriz-02out"])
out = rotas.registrar([res], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:400])
