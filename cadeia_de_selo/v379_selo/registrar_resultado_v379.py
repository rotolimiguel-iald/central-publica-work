# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o RESULTADO da v379 (EXAMINADA), tudo LIDO da rodada (leitura_v379.ler) -- rodar DEPOIS da cadeia do selo."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import leitura_v379, rotas
V, PROB = leitura_v379.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
NOS = V["nos"]
res = dict(tipo="ROTA", rota_id="um_py.v379.a_razao_elementar", dominio="UM_PY", status="EXAMINADA", estatuto="REAL",
           titulo="v379 SELADA: a Razão Elementar tipada — E = C × I × K > 0 = β_TGL por termo (C = √e, I = 1, K = α); E é a assíntota; sem testemunha estática plena; o reconhecimento é finito por definição",
           pergunta="A cunhagem do operador (E = C × I × K > 0 = β; limite assintótico em tempo finito) tipa no kernel sem axioma novo? Com que estatuto?",
           metodo="molde da v378: candidato (9 patches sobre a v378 selada), sandbox lake build rc 0, ensaio a seco PT/EN, aferidor independente, instalação com backup de bytes, rito, conferidor, cadeia pós-rito",
           resultado=("um.py %s (%s B) sobre a v378 %s; %s; rodada %s; conferidor TUDO BATE (%s / %s); bandeiras novas %s/%s; escada %s; E = %s = β %s; (e^{1/4}√α)² = %s; custo por nat v378 %s ≤ E; "
                      "the_elementary_reason_v379 = %s; selo.um_version = %s; md canônico carimbado: %s; gate %s (%s/18) intocado; por termo %s"
                      % (V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["selo_ts"], V["conf_dm"], V["conf_np"], V["n_flags_on"], V["n_flags"], V["esc"], V["E"], V["beta"], V["reason2"], V["pernat"],
                         V["the_elementary_reason_v379"], V["um_version"], V["md_carimbo"], V["qg"], V["n18"], V["hvals"])),
           veredito=V["the_elementary_reason_v379"], olhou_dados=True,
           nao_refazer="a v379 está selada e conferida; a fatoração e a positividade são por termo; o dicionário é cunhagem [ONTO/DEFINITION]; a assíntota não é excedida; o apagamento não se atinge em tempo finito; o reconhecimento é finito por definição",
           proximo_passo="custódia/espelho pela sessão do site (ato dela; commit/push do operador); as decisões do operador deixadas na v378",
           onde="Nós\\um.py v379: prove_the_elementary_reason_v379; TGLExt/TheElementaryReason.lean",
           artefatos=[os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(NOS, "um_absoluto.json"), os.path.join(NOS, "rodada_v379_stdout.txt"),
                      os.path.join(NOS, "um_absoluto_forma_canonica.md"), os.path.join(NOS, "um_absoluto_manifest.md"),
                      os.path.join(NOS, "tgl_kernel", "TGLExt", "TheElementaryReason.lean"), os.path.join(HERE, "v379_incorporacao_manifesto.json")],
           refs=["um_py.v378.o_que_faltou_contraste_fase4", "um_py.v377.a_lei_da_dissipacao", "beta.desvio_como_foco"])
out = rotas.registrar([res], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(json.dumps({k: out[k] for k in out if k != "registros"}, ensure_ascii=False)[:400])
