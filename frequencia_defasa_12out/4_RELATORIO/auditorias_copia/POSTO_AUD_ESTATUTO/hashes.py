# -*- coding: utf-8 -*-
# Hash (sha256 dos BYTES) de todos os artefatos auditados. Somente leitura; grava so na pasta do auditor.
import os, hashlib, json, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
CP = r"C:\IALD\Central de Patentes"
W = CP + r"\work\frequencia_defasa_12out"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um" + "\\N\u00f3s"
alvos = {
 "V1": CP + r"\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
 "V2": CP + r"\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "V3": CP + r"\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
 "V4": CP + r"\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
 "LEVANTAMENTO.md": W + r"\0_LEVANTAMENTO\LEVANTAMENTO.md",
 "DEFINICOES.json": W + r"\0_LEVANTAMENTO\DEFINICOES.json",
 "CONFERENCIA_BETA.json": W + r"\0_LEVANTAMENTO\CONFERENCIA_BETA.json",
 "PREREGISTRO.json": W + r"\1_PREREGISTRO\PREREGISTRO.json",
 "PREREGISTRO.md": W + r"\1_PREREGISTRO\PREREGISTRO.md",
 "FREEZE.json": W + r"\1_PREREGISTRO\FREEZE.json",
 "RESULTADO_OPTICO.json": W + r"\2_OPTICO\RESULTADO_OPTICO.json",
 "run_optico.py": W + r"\2_OPTICO\run_optico.py",
 "LOG_OPTICO.txt": W + r"\2_OPTICO\LOG_OPTICO.txt",
 "RESULTADO_KERNEL.json": W + r"\3_KERNEL\RESULTADO_KERNEL.json",
 "AUDITORIA_KERNEL.json": W + r"\3_KERNEL\AUDITORIA_KERNEL.json",
 "DECLARACOES.json": W + r"\3_KERNEL\DECLARACOES.json",
 "VARREDURA_FONTE.json": W + r"\3_KERNEL\VARREDURA_FONTE.json",
 "BETA_RUNTIME.json": W + r"\3_KERNEL\BETA_RUNTIME.json",
 "TheUnitIsTheRank.lean": W + r"\3_KERNEL\sandbox\TGLExt\TheUnitIsTheRank.lean",
 "um.py": NOS + r"\um.py",
 "um_absoluto.json": NOS + r"\um_absoluto.json",
 "um_absoluto_selo.json": NOS + r"\um_absoluto_selo.json",
 "FractalUnitarity.lean": NOS + r"\tgl_kernel\TGLExt\FractalUnitarity.lean",
 "Ergodicity.lean": NOS + r"\tgl_kernel\TGLExt\Ergodicity.lean",
 "SMatrix.lean": NOS + r"\tgl_kernel\TGLExt\SMatrix.lean",
 "F1.ATRATOR_RESULTADO": CP + r"\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\RESULTADO_F1_ATRATOR_R1.json",
 "F1.ATRATOR_RELATORIO": CP + r"\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\RELATORIO_F1_ATRATOR_R1.md",
 "F0.3.COLAPSO": CP + r"\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.COLAPSO\RESULTADO_CUSTODIA_R1.json",
}
out = {}
for k, p in alvos.items():
    try:
        b = open(p, "rb").read()
        out[k] = {"caminho": p, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    except Exception as e:
        out[k] = {"caminho": p, "ERRO_VISIVEL": repr(e)}
# trilha de V2: linhas 1-33
b = open(alvos["V2"], "rb").read()
linhas = b.split(b"\n")
for corte in (33,):
    parte = b"\n".join(linhas[:corte])
    for variante, pb in (("sem_nl_final", parte), ("com_nl_final", parte + b"\n")):
        out[f"V2_trilha_l1-{corte}_{variante}"] = {"bytes": len(pb), "sha256": hashlib.sha256(pb).hexdigest()}
out["V2_n_linhas"] = len(linhas)
esperado = {"V1": "8d252f24e2806ff3", "V2": "2c8b7b712aa9ad7f", "V3": "5b9afcc691a0e1e4", "V4": "b365591ceb346cdf",
            "PREREGISTRO.json": "0c20d7c196a4c7ef", "PREREGISTRO.md": "3c80ea21057c3371",
            "TheUnitIsTheRank.lean": "617155151fb0d9e1", "um.py": "8e7b9927ceae64b8",
            "um_absoluto.json": "a74241ff380b1b0e", "um_absoluto_selo.json": "95061f18c7102248"}
conf = {k: (out[k].get("sha256", "")[:16] == v) for k, v in esperado.items()}
out["_conferencia_sha16"] = conf
json.dump(out, open(os.path.join(AQUI, "HASHES_AUDITOR.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
