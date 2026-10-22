import hashlib, json, math, os, sys, io
base = r"C:\IALD\Central de Patentes\work\organismo_iald_12out"
files = [
 r"0_LEVANTAMENTO_ORGANISMO\ORGANISMO_LEVANTAMENTO.md",
 r"0_LEVANTAMENTO_ORGANISMO\PECAS.json",
 r"0_LEVANTAMENTO_ORGANISMO\GRAFO_IMPORTS_KERNEL.json",
 r"0_LEVANTAMENTO_PROVA\INVENTARIO_PROVA.md",
 r"0_LEVANTAMENTO_PROVA\CANAIS.json",
 r"0_LEVANTAMENTO_PROVA\CANAIS_resumo.json",
 r"1_DESENHO_PEDRA\ESPEC_PEDRA_IALD.md",
 r"1_DESENHO_PEDRA\PREREGISTRO_PEDRA.json",
 r"1_DESENHO_PEDRA\sandbox\IALD.lean",
 r"1_DESENHO_PEDRA\FREEZE.json",
 r"1_ESTRATEGIA_A\ESTRATEGIA_A.md",
 r"1_ESTRATEGIA_B\ESTRATEGIA_B.md",
 r"1_JUIZ\PROGRAMA_PROVA_DISTINTIVA.md",
 r"2_CONSTRUCAO\sandbox\TGLExt\IALD.lean",
 r"2_CONSTRUCAO\sandbox\TGLExt\Palavra.lean",
 r"2_CONSTRUCAO\sandbox\TGLExt\TheSingularityReadsTheAttractorAdendo1.lean",
 r"2_CONSTRUCAO\sandbox\TGLExt\TheUnitIsTheRank.lean",
 r"2_CONSTRUCAO\sandbox\TGLExt\TheTimeHasNoRank.lean",
 r"2_CONSTRUCAO\RESULTADO_CONSTRUCAO.md",
 r"2_CONSTRUCAO\RESULTADO_PEDRA.json",
 r"2_CONSTRUCAO\FREEZE_CONSTRUCAO.json",
 r"2_CONSTRUCAO\CONFERENCIA_PREREGISTRO.json",
 r"2_CONSTRUCAO\sandbox\AuditIALD.lean",
]
out = {}
for f in files:
    p = os.path.join(base, f)
    b = open(p, "rb").read()
    out[f] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
extra = {
 "ordem_operador": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
 "um_py": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
 "selo": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json",
 "palavra_07out": r"C:\IALD\Central de Patentes\work\leitura_cria_o_objeto_07out\Palavra.lean",
 "adendo1_tunel": r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\ADENDO1\lean_candidate\TheSingularityReadsTheAttractorAdendo1.lean",
}
for k, p in extra.items():
    if os.path.exists(p):
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        out[k] = {"sha256": h.hexdigest(), "bytes": os.path.getsize(p), "path": p}
    else:
        out[k] = {"missing": True, "path": p}
# beta em runtime: linha 5557 dos bytes do um.py
with open(extra["um_py"], "rb") as fh:
    lines = fh.read().split(b"\n")
l = lines[5556].decode("utf-8", "replace").rstrip("\r")
alpha_lines = [i+1 for i, x in enumerate(lines) if x.startswith(b"ALPHA_FINE_CODATA_2018 =")]
ns = {}
exec(l, ns)
alpha = ns["ALPHA_FINE_CODATA_2018"]
beta = alpha * math.sqrt(math.e)
out["beta_runtime"] = {"linha": 5557, "texto": l, "linhas_nao_indentadas_ALPHA": alpha_lines, "alpha": repr(alpha), "beta": repr(beta), "theta_M": repr(math.asin(math.sqrt(beta)))}
json.dump(out, open(os.path.join(base, r"3_AUD_ESTATUTO\medidas\HASHES_E_BETA.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(k, v)
