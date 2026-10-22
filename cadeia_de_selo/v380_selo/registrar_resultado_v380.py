# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v380 (EXAMINADA), tudo LIDO da rodada (leitura_v380.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v380, rotas
V, PROB = leitura_v380.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
res = dict(tipo="ROTA", rota_id="um_py.v380.fases_5_6_7_por_hash", dominio="UM_PY", status="EXAMINADA", estatuto="REAL",
           titulo="v380 SELADA: as Fases 5, 6 (ECO V3 + V4 + V5) e 7 da Bancada, o banco de GW e seis erratas da auditoria (+1 da v378, +1 nota) ao lado, lidos por hash; sem kernel novo; gate intocado",
           pergunta="O que a Bancada mediu em 01/10 (SH0ES; o eco como resposta radical da fronteira; os cronômetros com covariância completa) entra no programa terminal por hash, com os estatutos ditos?",
           metodo="molde da v379 sem kernel: candidato (7 patches sobre a v379 selada), ensaio a seco PT/EN, aferidor independente, instalação com backup de bytes, rito, conferidor, cadeia pós-rito",
           resultado=("um.py %s (%s B) sobre a v379 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); escada %s inalterada; H0 escada %s ± %s; KMS todos z_excl %s/%s (sist. %s), O4 cego %s/%s; MAY sist. %s; V4 sin2θ×MAY z_excl %s (controles %sσ); "
                      "V5 (DEC) z_excl %s/%s (O4 %s/%s), R3 sem poder %sσ (rótulo %s; cláusula V5 %s); T z do ganho %s → %s; U ln B %s → %s; banco %s/%s; veredito %s; selo.um_version = %s; md carimbado: %s; gate %s (%s/18) intocado; por termo %s"
                      % (V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["esc"], V["h0_v"], V["h0_s"], V["k6_z1"], V["k6_z2"], V["k6_sys"], V["o6_z1"], V["o6_z2"], V["m6_sys"], V["v4_z2"], V["v4_ctrl"],
                         V["v5_z1"], V["v5_z2"], V["v5_o1"], V["v5_o2"], V["v5_r3p"], V["v5_r3lab"], V["v5_clausula"], V["t7_diag"], V["t7_m20"], V["u7_diag"], V["u7_m20"], V["gb_ok"], V["gb_n"], V["bancada_fases_5_6_7_v380"], V["um_version"], V["md_carimbo"], V["qg"], V["n18"], V["hvals"])),
           veredito=V["bancada_fases_5_6_7_v380"], olhou_dados=True,
           nao_refazer="a v380 está selada e conferida; falsificar o par (leitura, lei) não falsifica a teoria; as três leis de atraso do acervo (MAY, KMS, DEC) estão medidas com o mesmo estimador; a covariância dos cronômetros está medida",
           proximo_passo="custódia/espelho pela sessão do site (ato dela; commit/push do operador); as decisões do operador: lei de atraso derivada e peso do gráviton; leitura «sombra»; qual fundo é o fundo",
           onde="Nós\\um.py v380: prove_bancada_fases_5_6_7_v380",
           artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v380_stdout.txt"),
                      os.path.join(NOS, "um_absoluto_forma_canonica.md"), os.path.join(NOS, "um_absoluto_manifest.md"), os.path.join(HERE, "v380_incorporacao_manifesto.json")],
           refs=["um_py.v379.a_razao_elementar", "gw.eco_radical.v3", "d1.fase7_cc_covariancia_01out", "d1.fase5_sh0es_01out"])
out = rotas.registrar([res], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:400])
