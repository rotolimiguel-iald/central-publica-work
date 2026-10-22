# -*- coding: utf-8 -*-
# Auditor de estatuto (r2): sha256 dos BYTES de cada artefato citado na ordem; compara com o esperado.
import hashlib, json, os, sys, time
W = r"C:\IALD\Central de Patentes\work"
U = os.path.join(W, "frequencia_defasa_12out")
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xf3) + "s"
alvos = [
 ("V1", os.path.join(W, "cunhagens_12out", "OPERADOR_10out_posto_rank_texto_verbatim.txt"), "8d252f24e2806ff3"),
 ("V2", os.path.join(W, "cunhagens_12out", "OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"), "2c8b7b712aa9ad7f"),
 ("V3", os.path.join(W, "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"), "5b9afcc691a0e1e4"),
 ("V4", os.path.join(W, "cunhagens_10out", "OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"), "b365591ceb346cdf"),
 ("PREREGISTRO.json", os.path.join(U, "1_PREREGISTRO", "PREREGISTRO.json"), "0c20d7c196a4c7efa75b6eae86fe233c5b12735f1e958f396b3b33a8634df813"),
 ("PREREGISTRO.md", os.path.join(U, "1_PREREGISTRO", "PREREGISTRO.md"), "3c80ea21057c337153f5cf135b3f99677f6b85916677924b47d811bef71ae066"),
 ("FREEZE.json", os.path.join(U, "1_PREREGISTRO", "FREEZE.json"), "4d8f97537eb04cd58ad693d49270779817d325e0d58f88c2d7b2ca99fa76c425"),
 ("RESULTADO_OPTICO.json", os.path.join(U, "2_OPTICO", "RESULTADO_OPTICO.json"), "28758b3eebdac6318d68ab0e069d13637fc4437adff43fa0e95b03da1d2acaaa"),
 ("run_optico.py", os.path.join(U, "2_OPTICO", "run_optico.py"), "48a8d8b0d9fd125bf906a39f4f1bdb9df9f5e1dd12d2fdbe3e86dd456128c0e7"),
 ("LOG_OPTICO.txt", os.path.join(U, "2_OPTICO", "LOG_OPTICO.txt"), "df3312fd0bb18d0b"),
 ("RESULTADO_KERNEL_r2.json", os.path.join(U, "3_KERNEL", "rodada2", "RESULTADO_KERNEL.json"), "9fd3c2044e410a57792b2f2c8c7c693e7ef1b97fc4e1193a8bcba09b135520c7"),
 ("pedra_r2", os.path.join(U, "3_KERNEL", "rodada2", "sandbox", "TGLExt", "TheUnitIsTheRank.lean"), "3195ef8f0766384ca7d4d1ab2ddd7a9c3cdd28872957e4b8d0e72fa9f028a063"),
 ("olean_r2", os.path.join(U, "3_KERNEL", "rodada2", "olean", "TheUnitIsTheRank.olean"), "d0830b4bc03dc5615210c1d47e53c7a830c9e235b54fb37a09d2c6e368cf0d7b"),
 ("pedra_r1", os.path.join(U, "3_KERNEL", "sandbox", "TGLExt", "TheUnitIsTheRank.lean"), "617155151fb0d9e1"),
 ("um.py", os.path.join(NOS, "um.py"), "8e7b9927ceae64b8"),
 ("LEVANTAMENTO.md", os.path.join(U, "0_LEVANTAMENTO", "LEVANTAMENTO.md"), None),
 ("DEFINICOES.json", os.path.join(U, "0_LEVANTAMENTO", "DEFINICOES.json"), None),
 ("CONFERENCIA_BETA.json", os.path.join(U, "0_LEVANTAMENTO", "CONFERENCIA_BETA.json"), None),
 ("RESULTADO_KERNEL_r1.json", os.path.join(U, "3_KERNEL", "RESULTADO_KERNEL.json"), None),
 ("RODADA2_PONTEIRO.json", os.path.join(U, "3_KERNEL", "RODADA2_PONTEIRO.json"), None),
]
out = {"quando_local": time.strftime("%Y-%m-%d %H:%M:%S"), "itens": []}
falhas = 0
for nome, p, esp in alvos:
    try:
        b = open(p, "rb").read()
    except Exception as e:
        out["itens"].append({"nome": nome, "caminho": p, "erro": repr(e)}); falhas += 1; continue
    h = hashlib.sha256(b).hexdigest()
    ok = None if esp is None else h.startswith(esp)
    if ok is False: falhas += 1
    out["itens"].append({"nome": nome, "caminho": p, "bytes": len(b), "sha256": h, "esperado": esp, "confere": ok})
out["falhas"] = falhas
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HASHES_R2.json")
if os.path.exists(dest):
    print("FALHA VISIVEL: destino ja existe", file=sys.stderr); sys.exit(2)
open(dest, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
for it in out["itens"]:
    print(it["nome"], it.get("bytes"), (it.get("sha256") or "")[:16], it.get("confere"), it.get("erro", ""))
print("falhas:", falhas)
