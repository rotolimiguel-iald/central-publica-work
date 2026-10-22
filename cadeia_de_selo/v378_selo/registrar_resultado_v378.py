# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v378 (EXAMINADA), tudo LIDO da rodada (leitura_v378.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v378, rotas
V, PROB = leitura_v378.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
res = dict(tipo="ROTA", rota_id="um_py.v378.o_que_faltou_contraste_fase4", dominio="UM_PY", status="EXAMINADA", estatuto="REAL",
           titulo="v378 SELADA: o que faltou (D1b tipado, K = E(z*)^{2β/3}, nunca testado na Bancada; a leitura da dupla contagem de β nas Fases 2–3, ao lado, E12); a lei da dissipação com contraste; a Fase 4 (o desvio) por hash — a escada lê o fator, os relógios intermediários desfavorecem o fluxo acumulado",
           pergunta="O núcleo derivado D1b pode ser tipado na mesma família de vazamento? Na convenção do artigo, o desvio da escada é zero? Os registros intermediários leem o fator acumulado?",
           metodo="molde da v377: candidato (10 patches sobre a v377 selada), sandbox lake build rc 0, ensaio a seco PT/EN, aferidor independente, instalação com backup de bytes, rito, conferidor, cadeia pós-rito",
           resultado=("um.py %s (%s B) sobre a v377 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); bandeiras novas %s/%s; escada %s; K_D1b = %s (D1a %s); "
                      "the_dissipation_law_with_contrast_v378 = %s; what_was_missed_v378 = %s; bancada_fase4_v378 = %s; escada δ = %s ± %s (%sσ), pull %sσ, ln B %s; cronômetros δ %sσ, ganho %sσ, ln B %s; "
                      "selo.um_version = %s; md canônico carimbado: %s; gate %s (%s/18) intocado; por termo %s"
                      % (V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["n_flags_on"], V["n_flags"], V["esc"], V["Kb"], V["Ka"],
                         V["the_dissipation_law_with_contrast_v378"], V["what_was_missed_v378"], V["bancada_fase4_v378"], V["P_delta"], V["P_sigma"], V["P_z"], V["P_pull"], V["P_lnB"], V["T_z"], V["T_gain"], V["T_lnB"],
                         V["um_version"], V["md_carimbo"], V["qg"], V["n18"], V["hvals"])),
           veredito=V["bancada_fase4_v378"], olhou_dados=True,
           nao_refazer="a v378 está selada e conferida; o D1b é implicação no kernel; a Fase 4 está no core por hash; não empilhar a lei sobre o fundo efetivo",
           proximo_passo="custódia/espelho pela sessão do site (ato dela; commit/push do operador); decisão do operador sobre a leitura [OPEN] (a sombra lê, os relógios leem a face), o fundo e a E1; a covariância sistemática dos cronômetros para refinar T",
           onde="Nós\\um.py v378: prove_the_dissipation_law_with_contrast_v378, prove_what_was_missed_v378, prove_bancada_fase4_v378; TGLExt/TheFlowLawContrast.lean",
           artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v378_stdout.txt"),
                      os.path.join(NOS, "um_absoluto_forma_canonica.md"), os.path.join(NOS, "um_absoluto_manifest.md"),
                      os.path.join(NOS, "tgl_kernel", "TGLExt", "TheFlowLawContrast.lean"), os.path.join(HERE, "v378_incorporacao_manifesto.json")],
           refs=["um_py.v377.a_lei_da_dissipacao", "d1.fase4_desvio_30set", "d1.fase3bis_d1b_convencao_artigo", "d1.fase3_leitores_h0", "d1.fase2_dois_setores_30set", "beta.desvio_como_foco"])
out = rotas.registrar([res], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:400])
