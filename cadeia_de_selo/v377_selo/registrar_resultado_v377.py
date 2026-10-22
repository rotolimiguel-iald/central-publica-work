# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v377 (EXAMINADA), tudo LIDO da rodada (leitura_v377.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v377, rotas
V, PROB = leitura_v377.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
res = dict(tipo="ROTA", rota_id="um_py.v377.a_lei_da_dissipacao", dominio="UM_PY", status="EXAMINADA", estatuto="REAL",
           titulo="v377 SELADA: a lei da dissipação provada (H₀_local = H₀_fundo·(1+z)^β como implicação); a física é a leitura; as três fases da Bancada por hash; o desvio de β como foco",
           pergunta="A lei D1a pode ser provada no kernel sem hipótese nomeada? A física pode ser tipada como a leitura? As fases da Bancada entram no um.py por hash?",
           metodo="molde da v376: candidato (10 patches sobre a v376 selada), sandbox lake build rc 0, ensaio a seco PT/EN, aferidor independente, instalação com backup de bytes, rito, conferidor, cadeia pós-rito",
           resultado=("um.py %s (%s B) sobre a v376 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); bandeiras novas %s/%s; escada %s; K = %s; "
                      "the_dissipation_law_v377 = %s; physics_is_the_reading_v377 = %s; bancada_fases_v377 = %s; final_stone_reading_v377 = %s; "
                      "selo.um_version = %s; md canônico carimbado: %s; gate %s (%s/18) intocado; por termo %s; errata ao lado no módulo de Coma: %s"
                      % (V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["n_flags_on"], V["n_flags"], V["esc"], V["K"],
                         V["the_dissipation_law_v377"], V["physics_is_the_reading_v377"], V["bancada_fases_v377"], V["final_stone_reading_v377"],
                         V["um_version"], V["md_carimbo"], V["qg"], V["n18"], V["hvals"], V["coma_v377"])),
           veredito=V["the_dissipation_law_v377"], olhou_dados=True,
           nao_refazer="a v377 está selada e conferida; a lei da dissipação é implicação no kernel; as fases 1–3 estão no core por hash",
           proximo_passo="custódia/espelho pela sessão do site (ato dela; commit/push do operador); Fase 4 (o desvio) depois da decisão do operador sobre a variável assintótica; a pergunta do ângulo com o fator (1+β)",
           onde="Nós\\um.py v377: prove_the_dissipation_law_v377, prove_physics_is_the_reading_v377, prove_bancada_fases_v377, prove_final_stone_reading_v377; TGLExt/TheFlowLawD1a.lean; TGLExt/PhysicsIsTheReading.lean",
           artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v377_stdout.txt"),
                      os.path.join(NOS, "um_absoluto_forma_canonica.md"), os.path.join(NOS, "um_absoluto_manifest.md"),
                      os.path.join(NOS, "tgl_kernel", "TGLExt", "TheFlowLawD1a.lean"), os.path.join(NOS, "tgl_kernel", "TGLExt", "PhysicsIsTheReading.lean"), os.path.join(HERE, "v377_incorporacao_manifesto.json")],
           refs=["um_py.v376.o_todo_e_um", "kernel.pedra_final.espelhamento_j", "d1.fase1_eff_30set", "d1.fase2_dois_setores_30set", "d1.fase3_leitores_h0", "beta.desvio_como_foco"])
out = rotas.registrar([res], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:400])
